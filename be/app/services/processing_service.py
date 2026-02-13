"""Processing service - adapted from a-studio/backend/align_processor.py"""

import logging
import os
import queue
import sqlite3
import time
from dataclasses import dataclass
from multiprocessing import Process, Queue

import matplotlib

matplotlib.use("Agg")

from sqlalchemy.orm import Session

from app import config
from app.database import SessionLocal
from app.models.alignment import Alignment, AlignmentState
from app.models.alignment_progress import AlignmentProgress
from app.services.file_storage import get_alignment_db_path, get_vis_img_path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AlignmentInfo:
    """Detached snapshot of Alignment fields for use outside the DB session."""
    id: int
    guid: str
    lang_from: str
    lang_to: str
    total_batches: int

    @staticmethod
    def from_orm(a: Alignment) -> "AlignmentInfo":
        return AlignmentInfo(
            id=a.id,
            guid=a.guid,
            lang_from=a.lang_from,
            lang_to=a.lang_to,
            total_batches=a.total_batches,
        )

FINISH_PROCESS = "finish_process"


def _update_progress_in_new_session(alignment_id: int, batch_id: int) -> None:
    """Insert alignment progress in a fresh DB session (for use in subprocess)."""
    db = SessionLocal()
    try:
        existing = (
            db.query(AlignmentProgress)
            .filter(
                AlignmentProgress.alignment_id == alignment_id,
                AlignmentProgress.batch_id == batch_id,
            )
            .first()
        )
        if not existing:
            db.add(AlignmentProgress(alignment_id=alignment_id, batch_id=batch_id))
            db.commit()
    finally:
        db.close()


def _increment_state_in_new_session(alignment_id: int, state: int) -> None:
    """Update alignment state with current batch count in a fresh DB session."""
    db = SessionLocal()
    try:
        count = (
            db.query(AlignmentProgress)
            .filter(AlignmentProgress.alignment_id == alignment_id)
            .count()
        )
        alignment = db.get(Alignment, alignment_id)
        if alignment:
            alignment.state = state
            alignment.curr_batches = count
            db.commit()
    finally:
        db.close()


def _update_state_in_new_session(
    alignment_id: int,
    state: int,
    curr_batches: int | None = None,
    total_batches: int | None = None,
) -> None:
    """Update alignment state in a fresh DB session."""
    db = SessionLocal()
    try:
        alignment = db.get(Alignment, alignment_id)
        if alignment:
            alignment.state = state
            if curr_batches is not None:
                alignment.curr_batches = curr_batches
            if total_batches is not None:
                alignment.total_batches = total_batches
            db.commit()
    finally:
        db.close()


def _get_progress_in_new_session(alignment_id: int) -> tuple[int, int]:
    """Get current/total batches in a fresh DB session."""
    db = SessionLocal()
    try:
        alignment = db.get(Alignment, alignment_id)
        if alignment:
            return alignment.curr_batches, alignment.total_batches
        return 0, 0
    finally:
        db.close()


class AlignmentProcessor:
    """Processor with parallel texts alignment logic."""

    def __init__(
        self,
        proc_count,
        db_path,
        alignment_id,
        res_img_best,
        lang_name_from,
        lang_name_to,
        align_guid,
        model_name,
        embed_batch_size,
        normalize_embeddings,
        mode="align",
        operation=None,
        plot_info=False,
        plot_regression=False,
        use_proxy_from=False,
        use_proxy_to=False,
    ):
        from lingtrain_aligner import constants as la_con

        self.proc_count = proc_count
        self.queue_in = Queue()
        self.queue_out = Queue()
        self.db_path = db_path
        self.alignment_id = alignment_id
        self.res_img_best = res_img_best
        self.lang_name_from = lang_name_from
        self.lang_name_to = lang_name_to
        self.tasks_count = 0
        self.align_guid = align_guid
        self.model_name = model_name
        self.mode = mode
        self.embed_batch_size = embed_batch_size
        self.normalize_embeddings = normalize_embeddings
        self.operation = operation or la_con.OPERATION_CALCULATE_CUSTOM
        self.plot_info = plot_info
        self.plot_regression = plot_regression
        self.use_proxy_from = use_proxy_from
        self.use_proxy_to = use_proxy_to

    def add_tasks(self, task_list):
        for i, task in enumerate(task_list):
            self.queue_in.put((i, task))
        for i in range(self.proc_count):
            self.queue_in.put((-1, FINISH_PROCESS))
        self.tasks_count = len(task_list)

    def work(self, queue_in, queue_out):
        while True:
            try:
                task_index, task = queue_in.get_nowait()
            except queue.Empty:
                time.sleep(0.01)
            else:
                try:
                    if task == FINISH_PROCESS:
                        break
                    if self.mode == "align":
                        self.process_batch_wrapper(*task)
                    elif self.mode == "resolve":
                        self.resolve_batch_wrapper(*task)
                except Exception as e:
                    logger.error(f"Task failed: {e}", exc_info=True)
                    queue_out.put("error")

    def handle_result(self, queue_out):
        from lingtrain_aligner import aligner, vis_helper

        counter = 0
        error_occured = False
        result = []

        while counter < self.tasks_count:
            result_code, batch_number, texts_from, texts_to, shift, window = (
                queue_out.get()
            )

            if result_code == AlignmentState.DONE:
                result.append((batch_number, texts_from, texts_to, shift, window))
                _update_progress_in_new_session(self.alignment_id, batch_number)
                _increment_state_in_new_session(
                    self.alignment_id, AlignmentState.IN_PROGRESS
                )
            elif result_code == AlignmentState.ERROR:
                error_occured = True
                _increment_state_in_new_session(
                    self.alignment_id, AlignmentState.ERROR
                )
                break

            counter += 1

        result.sort()
        with sqlite3.connect(self.db_path) as db:
            aligner.write_processing_batches(db, result)
            aligner.create_doc_index(db, result)

        for batch_id, _, _, shift, window in result:
            aligner.update_history(
                self.db_path,
                [batch_id],
                self.operation,
                parameters={"shift": shift, "window": window},
            )

        for batch_id, _, _, shift, window in result:
            vis_helper.visualize_alignment_by_db(
                self.db_path,
                self.res_img_best,
                lang_name_from=self.lang_name_from,
                lang_name_to=self.lang_name_to,
                batch_ids=[batch_id],
                transparent_bg=True,
                show_info=self.plot_info,
                show_regression=self.plot_regression,
            )

        if not error_occured:
            curr_batches, total_batches = _get_progress_in_new_session(
                self.alignment_id
            )
            if curr_batches == total_batches:
                _update_state_in_new_session(
                    self.alignment_id, AlignmentState.DONE
                )
            else:
                _update_state_in_new_session(
                    self.alignment_id, AlignmentState.IN_PROGRESS_DONE
                )

    def start_align(self):
        workers = [
            Process(
                target=self.work, args=(self.queue_in, self.queue_out), daemon=True
            )
            for _ in range(min(self.proc_count, self.tasks_count))
        ]
        for w in workers:
            w.start()

        align_handler = Process(
            target=self.handle_result, args=(self.queue_out,)
        )
        align_handler.start()
        align_handler.join()

    def process_batch_wrapper(
        self,
        lines_from_batch,
        lines_to_batch,
        proxy_from,
        proxy_to,
        line_ids_from,
        line_ids_to,
        batch_number,
        shift,
        window,
    ):
        from lingtrain_aligner import aligner

        try:
            texts_from, texts_to = aligner.process_batch(
                self.db_path,
                lines_from_batch,
                lines_to_batch,
                line_ids_from,
                line_ids_to,
                batch_number,
                self.model_name,
                window,
                self.embed_batch_size,
                self.normalize_embeddings,
                show_progress_bar=False,
                save_pic=True,
                lang_name_from=self.lang_name_from,
                lang_name_to=self.lang_name_to,
                img_path=self.res_img_best,
                show_info=self.plot_info,
                show_regression=self.plot_regression,
                use_proxy_from=self.use_proxy_from,
                use_proxy_to=self.use_proxy_to,
            )
            self.queue_out.put(
                (AlignmentState.DONE, batch_number, texts_from, texts_to, shift, window)
            )
        except Exception as e:
            logger.error(e, exc_info=True)
            self.queue_out.put((AlignmentState.ERROR, -1, [], [], -1, -1))

    def start_resolve(self):
        resolve_handler = Process(
            target=self.handle_resolve, args=(self.queue_out,), daemon=True
        )
        resolve_handler.start()

        workers = [
            Process(
                target=self.work, args=(self.queue_in, self.queue_out), daemon=True
            )
            for _ in range(min(self.proc_count, self.tasks_count))
        ]
        for w in workers:
            w.start()

    def resolve_batch_wrapper(
        self, batch_id, batch_amount, handle_start, handle_finish
    ):
        from lingtrain_aligner import aligner, resolver, constants as la_con

        try:
            # Strategy 1: iterative with increasing chain length
            steps = 3
            for i in range(steps):
                min_chain_length = 2 + i
                max_conflicts_len = 6 * (i + 1)
                conflicts, _ = resolver.get_all_conflicts(
                    self.db_path,
                    min_chain_length=min_chain_length,
                    max_conflicts_len=max_conflicts_len,
                    batch_id=batch_id,
                )
                resolver.resolve_all_conflicts(
                    self.db_path,
                    conflicts,
                    self.model_name,
                    show_logs=False,
                    use_proxy_from=self.use_proxy_from,
                    use_proxy_to=self.use_proxy_to,
                )
                params = {"min_chain_length": min_chain_length, "max_conflicts_len": max_conflicts_len}
                if batch_id == -1:
                    params["batch_amount"] = batch_amount
                aligner.update_history(
                    self.db_path, [batch_id], la_con.OPERATION_RESOLVE, parameters=params
                )

            # Strategy 2: negative length correction
            min_chain_length = 2
            max_conflicts_len = 26
            conflicts, rest_conflicts = resolver.get_all_conflicts(
                self.db_path,
                min_chain_length=min_chain_length,
                max_conflicts_len=max_conflicts_len,
                batch_id=batch_id,
            )
            resolver.correct_conflicts(
                self.db_path,
                rest_conflicts,
                batch_id=batch_id,
                min_chain_length=min_chain_length,
                max_conflicts_len=max_conflicts_len,
                handle_start=handle_start,
                handle_finish=handle_finish,
            )
            resolver.resolve_all_conflicts(
                self.db_path,
                conflicts,
                self.model_name,
                show_logs=False,
                use_proxy_from=self.use_proxy_from,
                use_proxy_to=self.use_proxy_to,
            )
            params = {"min_chain_length": min_chain_length, "max_conflicts_len": max_conflicts_len}
            if batch_id == -1:
                params["batch_amount"] = batch_amount
            aligner.update_history(
                self.db_path, [batch_id], la_con.OPERATION_RESOLVE, parameters=params
            )

            # Strategy 3: edge handling
            conflicts, _ = resolver.get_all_conflicts(
                self.db_path,
                min_chain_length=min_chain_length,
                max_conflicts_len=max_conflicts_len,
                batch_id=batch_id,
                handle_start=handle_start,
                handle_finish=handle_finish,
            )
            resolver.resolve_all_conflicts(
                self.db_path,
                conflicts,
                self.model_name,
                show_logs=False,
                use_proxy_from=self.use_proxy_from,
                use_proxy_to=self.use_proxy_to,
            )
            aligner.update_history(
                self.db_path, [batch_id], la_con.OPERATION_RESOLVE, parameters=params
            )

            self.queue_out.put((AlignmentState.DONE, batch_id))

        except Exception as e:
            logger.error(e, exc_info=True)
            self.queue_out.put((AlignmentState.ERROR, []))

    def handle_resolve(self, queue_out):
        from lingtrain_aligner import vis_helper

        counter = 0
        error_occured = False
        result = []

        while counter < self.tasks_count:
            result_code, batch_number = queue_out.get()
            if result_code == AlignmentState.DONE:
                result.append(batch_number)
            elif result_code == AlignmentState.ERROR:
                error_occured = True
                _increment_state_in_new_session(
                    self.alignment_id, AlignmentState.ERROR
                )
                break
            counter += 1

        vis_helper.visualize_alignment_by_db(
            self.db_path,
            self.res_img_best,
            lang_name_from=self.lang_name_from,
            lang_name_to=self.lang_name_to,
            batch_ids=result,
            transparent_bg=True,
            show_info=self.plot_info,
            show_regression=self.plot_regression,
        )

        if not error_occured:
            curr_batches, total_batches = _get_progress_in_new_session(
                self.alignment_id
            )
            if curr_batches == total_batches:
                _update_state_in_new_session(
                    self.alignment_id, AlignmentState.DONE
                )
            else:
                _update_state_in_new_session(
                    self.alignment_id, AlignmentState.IN_PROGRESS_DONE
                )


def start_alignment(user_id: int, alignment: AlignmentInfo, data) -> None:
    from lingtrain_aligner import aligner, constants as la_con

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )
    res_img_best = str(get_vis_img_path(user_id, alignment.guid))

    lines_from = aligner.get_splitted_from(db_path)
    lines_to = aligner.get_splitted_to(db_path)
    proxy_from = aligner.get_proxy_from(db_path)
    proxy_to = aligner.get_proxy_to(db_path)

    batch_ids = data.batch_ids
    if data.align_all:
        batch_ids = list(range(alignment.total_batches))

    batch_ids = [x for x in batch_ids if x < alignment.total_batches][
        : alignment.total_batches
    ]
    if not batch_ids:
        return

    task_list = [
        (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
            data.batch_shift,
            data.window,
        )
        for (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
        ) in aligner.get_batch_intersected(
            lines_from,
            lines_to,
            n=config.ALIGNER_BATCH_SIZE,
            window=data.window,
            batch_ids=batch_ids,
            batch_shift=data.batch_shift,
            iter3=proxy_from,
            iter4=proxy_to,
        )
    ]

    proc = AlignmentProcessor(
        config.ALIGNER_PROCESSORS,
        db_path,
        alignment.id,
        res_img_best,
        alignment.lang_from,
        alignment.lang_to,
        alignment.guid,
        model_name=config.ALIGNER_MODEL,
        embed_batch_size=config.ALIGNER_EMBED_BATCH_SIZE,
        normalize_embeddings=config.ALIGNER_NORMALIZE_EMBEDDINGS,
        operation=la_con.OPERATION_CALCULATE_CUSTOM,
        plot_info=True,
        plot_regression=False,
        use_proxy_from=data.use_proxy_from,
        use_proxy_to=data.use_proxy_to,
    )
    proc.add_tasks(task_list)
    proc.start_align()


def align_next(user_id: int, alignment: AlignmentInfo, data) -> None:
    from lingtrain_aligner import aligner, constants as la_con

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )
    res_img_best = str(get_vis_img_path(user_id, alignment.guid))

    # Determine next batch IDs
    with sqlite3.connect(db_path) as align_db:
        batch_ids_rows = align_db.execute("select batch_id from batches").fetchall()
    processed = [x[0] for x in batch_ids_rows]
    last_batch_id = max(processed) + 1 if processed else 0
    batch_ids = list(range(last_batch_id, last_batch_id + data.amount))

    batch_ids = [x for x in batch_ids if x < alignment.total_batches][
        : alignment.total_batches
    ]
    if not batch_ids:
        return

    lines_from = aligner.get_splitted_from(db_path)
    lines_to = aligner.get_splitted_to(db_path)
    proxy_from = aligner.get_proxy_from(db_path)
    proxy_to = aligner.get_proxy_to(db_path)

    task_list = [
        (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
            data.batch_shift,
            data.window,
        )
        for (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
        ) in aligner.get_batch_intersected(
            lines_from,
            lines_to,
            n=config.ALIGNER_BATCH_SIZE,
            window=data.window,
            batch_ids=batch_ids,
            batch_shift=data.batch_shift,
            iter3=proxy_from,
            iter4=proxy_to,
        )
    ]

    proc = AlignmentProcessor(
        config.ALIGNER_PROCESSORS,
        db_path,
        alignment.id,
        res_img_best,
        alignment.lang_from,
        alignment.lang_to,
        alignment.guid,
        model_name=config.ALIGNER_MODEL,
        embed_batch_size=config.ALIGNER_EMBED_BATCH_SIZE,
        normalize_embeddings=config.ALIGNER_NORMALIZE_EMBEDDINGS,
        operation=la_con.OPERATION_CALCULATE_CUSTOM,
        plot_info=True,
        plot_regression=False,
        use_proxy_from=data.use_proxy_from,
        use_proxy_to=data.use_proxy_to,
    )
    proc.add_tasks(task_list)
    proc.start_align()


def resolve_conflicts(user_id: int, alignment: AlignmentInfo, data) -> None:
    from lingtrain_aligner import constants as la_con

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )
    res_img_best = str(get_vis_img_path(user_id, alignment.guid))

    batch_ids = data.batch_ids
    batch_ids = [x for x in batch_ids if x < alignment.total_batches][
        : alignment.total_batches
    ]
    if not batch_ids:
        return

    proc = AlignmentProcessor(
        config.ALIGNER_PROCESSORS,
        db_path,
        alignment.id,
        res_img_best,
        alignment.lang_from,
        alignment.lang_to,
        alignment.guid,
        model_name=config.ALIGNER_MODEL,
        embed_batch_size=config.ALIGNER_EMBED_BATCH_SIZE,
        normalize_embeddings=config.ALIGNER_NORMALIZE_EMBEDDINGS,
        mode="resolve",
        operation=la_con.OPERATION_RESOLVE,
        plot_info=True,
        plot_regression=False,
        use_proxy_from=data.use_proxy_from,
        use_proxy_to=data.use_proxy_to,
    )
    proc.add_tasks(
        [
            (batch_id, alignment.total_batches, data.handle_start, data.handle_finish)
            for batch_id in batch_ids
        ]
    )
    proc.start_resolve()


def stop_alignment(db: Session, alignment: Alignment) -> None:
    alignment.state = AlignmentState.IN_PROGRESS_DONE
    db.commit()


def get_conflicts(user_id: int, alignment: Alignment, handle_edges: str) -> dict:
    from lingtrain_aligner import resolver

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )

    handle_start = handle_edges in ("start", "both")
    handle_finish = handle_edges in ("finish", "both")

    conflicts, rest = resolver.get_all_conflicts(
        db_path,
        min_chain_length=2,
        max_conflicts_len=20,
        batch_id=-1,
        handle_start=handle_start,
        handle_finish=handle_finish,
    )
    stat1 = resolver.get_statistics(conflicts, print_stat=False)
    stat2 = resolver.get_statistics(rest, print_stat=False)
    res = [(x, stat1[x]) for x in stat1]
    res.extend([(x, stat2[x]) for x in stat2])
    res.sort(key=lambda x: x[1], reverse=True)
    return {"items": res}


def show_conflict(
    user_id: int, alignment: Alignment, conflict_id: int, handle_edges: str
) -> dict:
    from lingtrain_aligner import resolver

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )

    handle_start = handle_edges in ("start", "both")
    handle_finish = handle_edges in ("finish", "both")

    conflicts, rest = resolver.get_all_conflicts(
        db_path,
        min_chain_length=2,
        max_conflicts_len=20,
        batch_id=-1,
        handle_start=handle_start,
        handle_finish=handle_finish,
    )
    conflicts.extend(rest)
    if not conflicts:
        return {"from": [], "to": []}

    idx = conflict_id % len(conflicts)
    splitted_from, splitted_to = resolver.show_conflict(
        db_path, conflicts[idx], print_conf=False
    )
    return {"from": splitted_from, "to": splitted_to}


def update_visualization(
    user_id: int, alignment: Alignment, batch_ids: list[int], update_all: bool
) -> None:
    from lingtrain_aligner import vis_helper
    from app.services.file_storage import get_vis_img_path

    db_path = str(
        get_alignment_db_path(user_id, alignment.lang_from, alignment.lang_to, alignment.guid)
    )
    res_img_best = str(get_vis_img_path(user_id, alignment.guid))

    if update_all:
        batch_ids = list(range(alignment.total_batches))

    batch_ids = [x for x in batch_ids if x < alignment.total_batches][
        : alignment.total_batches
    ]
    if not batch_ids:
        return

    vis_helper.visualize_alignment_by_db(
        db_path,
        res_img_best,
        lang_name_from=alignment.lang_from,
        lang_name_to=alignment.lang_to,
        batch_ids=batch_ids,
        transparent_bg=True,
        show_info=True,
        show_regression=False,
    )
