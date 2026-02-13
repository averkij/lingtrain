"""Editor service - migrated from a-studio/backend/editor.py + editor_helper.py"""

import json
import logging
import sqlite3

from app.models.alignment import Alignment
from app.services.file_storage import get_alignment_db_path

logger = logging.getLogger(__name__)

# Edit operation constants (from a-studio constants.py)
TYPE_FROM = "from"
TYPE_TO = "to"
EDIT_ADD_PREV_END = "edit_add_prev_end"
EDIT_ADD_NEXT_END = "edit_add_next_end"
EDIT_ADD_CANDIDATE_END = "edit_add_candidate_end"
EDIT_DELETE_LINE = "edit_delete_line"
EDIT_CLEAR_LINE = "edit_clear_line"
EDIT_LINE = "edit_line"
EDIT_TRY_SET_LINE_IDS = "edit_try_set_line_ids"
ADD_EMPTY_LINE_BEFORE = "add_empty_line_before"
ADD_EMPTY_LINE_AFTER = "add_empty_line_after"


def _get_db_path(user_id: int, alignment: Alignment) -> str:
    return str(
        get_alignment_db_path(
            user_id, alignment.lang_from, alignment.lang_to, alignment.guid
        )
    )


def _parse_json_array(json_str):
    if not json_str:
        return []
    try:
        return json.loads(json_str)
    except Exception:
        return []


def _update_processing(db, text_type, processing_id, text_ids, text_to_update):
    if text_type == TYPE_FROM:
        db.execute(
            "update processing_from set text_ids = :text_ids, text = :text where id = :id",
            {"text_ids": text_ids, "text": text_to_update, "id": processing_id},
        )
    else:
        db.execute(
            "update processing_to set text_ids = :text_ids, text = :text where id = :id",
            {"text_ids": text_ids, "text": text_to_update, "id": processing_id},
        )


def _clear_processing(db, text_type, processing_id):
    if text_type == TYPE_FROM:
        db.execute(
            'update processing_from set text_ids = "[]", text = "", initial_id = NULL where id = :id',
            {"id": processing_id},
        )
    else:
        db.execute(
            'update processing_to set text_ids = "[]", text = "", initial_id = NULL where id = :id',
            {"id": processing_id},
        )


def _add_empty_processing_line(db, batch_id):
    from_id = db.execute(
        "insert into processing_from(batch_id, text_ids, text) values (:batch_id, :text_ids, :text)",
        {"batch_id": batch_id, "text_ids": "[]", "text": ""},
    ).lastrowid
    to_id = db.execute(
        "insert into processing_to(batch_id, text_ids, text) values (:batch_id, :text_ids, :text)",
        {"batch_id": batch_id, "text_ids": "[]", "text": ""},
    ).lastrowid
    return from_id, to_id


def _get_processing_text(db_path, text_type, processing_id):
    with sqlite3.connect(db_path) as db:
        if text_type == TYPE_FROM:
            cur = db.execute(
                "select text from processing_from where id = :id",
                {"id": processing_id},
            )
        else:
            cur = db.execute(
                "select text from processing_to where id = :id",
                {"id": processing_id},
            )
        res = cur.fetchone()
    return res if res else ("",)


def get_processing_page(user_id: int, alignment: Alignment, count: int, page: int) -> dict:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    if not _file_exists(db_path):
        return {"items": [], "meta": {}, "proxy_from_dict": {}, "proxy_to_dict": {}}

    index = helper.get_flatten_doc_index(db_path)
    shift = (page - 1) * count
    pages = list(zip(index[shift: shift + count], range(shift, shift + count)))
    res, proxy_from_dict, proxy_to_dict = helper.get_doc_items(pages, db_path)

    lines_count = len(index)
    total_pages = (lines_count // count) + (1 if lines_count % count != 0 else 0)
    meta = {"page": page, "total_pages": total_pages}
    return {
        "items": res,
        "meta": meta,
        "proxy_from_dict": proxy_from_dict,
        "proxy_to_dict": proxy_to_dict,
    }


def get_processing_by_ids(user_id: int, alignment: Alignment, index_ids: list[int]) -> dict:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    index = helper.get_flatten_doc_index(db_path)
    index_items = [(index[i], i) for i in index_ids if i < len(index)]
    data, proxy_from_dict, proxy_to_dict = helper.get_doc_items(index_items, db_path)

    res = {}
    valid_ids = [i for i in index_ids if i < len(index)]
    for i, item in zip(valid_ids, data):
        res[i] = item

    return {
        "items": res,
        "proxy_from_dict": proxy_from_dict,
        "proxy_to_dict": proxy_to_dict,
    }


def get_processing_meta(user_id: int, alignment: Alignment) -> dict:
    db_path = _get_db_path(user_id, alignment)
    with sqlite3.connect(db_path) as db:
        batch_ids = [x[0] for x in db.execute("select batch_id from batches").fetchall()]
    return {"batch_ids": batch_ids, "align_guid": alignment.guid}


def get_doc_index(user_id: int, alignment: Alignment) -> list:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    return helper.get_clear_flatten_doc_index(db_path)


def edit_doc(user_id: int, alignment: Alignment, data) -> None:
    from lingtrain_aligner import aligner, helper

    db_path = _get_db_path(user_id, alignment)

    update_index = True

    with sqlite3.connect(db_path) as db:
        index = aligner.get_doc_index(db)

        if (
            data.batch_id < 0
            or data.batch_id >= len(index)
            or data.batch_index_id < 0
            or data.batch_index_id > len(index[data.batch_id])
        ):
            return

        direction = 3 if data.text_type == TYPE_TO else 1
        line_ids = _parse_json_array(index[data.batch_id][data.batch_index_id][direction])

        if data.operation in (EDIT_ADD_PREV_END, EDIT_ADD_NEXT_END):
            target_batch_id = data.batch_id
            if data.target == "next":
                if data.batch_index_id + 1 >= len(index[data.batch_id]):
                    target_batch_id = data.batch_id + 1
                    target_index_id = 0
                else:
                    target_index_id = data.batch_index_id + 1
            else:
                if data.batch_index_id - 1 < 0:
                    if target_batch_id > 0:
                        target_batch_id = data.batch_id - 1
                        target_index_id = len(index[target_batch_id]) - 1
                    else:
                        return
                else:
                    target_index_id = data.batch_index_id - 1

            if target_batch_id >= len(index) or target_index_id >= len(
                index[target_batch_id]
            ):
                return

            processing_target_id = index[target_batch_id][target_index_id][0]
            text_to_edit = _get_processing_text(db_path, data.text_type, processing_target_id)[0]
            text_to_update = (text_to_edit + data.text).strip()

            processing_text_ids = _parse_json_array(
                index[target_batch_id][target_index_id][direction]
            )
            new_ids = processing_text_ids + line_ids
            new_ids = json.dumps(sorted(list(set(new_ids))))

            index[target_batch_id][target_index_id][direction] = new_ids
            _update_processing(db, data.text_type, processing_target_id, new_ids, text_to_update)

        elif data.operation == EDIT_ADD_CANDIDATE_END:
            processing_target_id = index[data.batch_id][data.batch_index_id][0]
            text_to_edit = _get_processing_text(db_path, data.text_type, processing_target_id)[0]
            text_to_update = (text_to_edit + data.candidate_text).strip()

            processing_text_ids = _parse_json_array(
                index[data.batch_id][data.batch_index_id][direction]
            )
            new_ids = processing_text_ids + [data.candidate_line_id]
            new_ids = json.dumps(sorted(list(set(new_ids))))

            index[data.batch_id][data.batch_index_id][direction] = new_ids
            _update_processing(db, data.text_type, processing_target_id, new_ids, text_to_update)

        elif data.operation == ADD_EMPTY_LINE_BEFORE:
            from_id, to_id = _add_empty_processing_line(db, data.batch_id)
            index[data.batch_id].insert(data.batch_index_id, (from_id, "[]", to_id, "[]"))

        elif data.operation == ADD_EMPTY_LINE_AFTER:
            from_id, to_id = _add_empty_processing_line(db, data.batch_id)
            index[data.batch_id].insert(data.batch_index_id + 1, (from_id, "[]", to_id, "[]"))

        elif data.operation == EDIT_LINE:
            processing_target_id = index[data.batch_id][data.batch_index_id][0]
            _update_processing(
                db, data.text_type, processing_target_id, json.dumps(line_ids), data.text
            )
            update_index = False

        elif data.operation == EDIT_CLEAR_LINE:
            processing_target_id = index[data.batch_id][data.batch_index_id][0]
            index[data.batch_id][data.batch_index_id][direction] = "[]"
            _clear_processing(db, data.text_type, processing_target_id)

        elif data.operation == EDIT_DELETE_LINE:
            index[data.batch_id].pop(data.batch_index_id)

        elif data.operation == EDIT_TRY_SET_LINE_IDS:
            lines_to_edit = []
            for bid, batch in enumerate(index):
                for id, line_info in enumerate(batch):
                    actual_ids = _parse_json_array(line_info[1])
                    if len(actual_ids) == 1 and actual_ids[0] == data.line_id_from:
                        lines_to_edit.append({
                            "batch_id": bid, "batch_index_id": id,
                            "line_info": line_info, "update_to": data.line_id_to,
                        })
                    elif len(actual_ids) == 1 and actual_ids[0] == data.line_id_from + 1:
                        lines_to_edit.append({
                            "batch_id": bid, "batch_index_id": id,
                            "line_info": line_info, "update_to": data.line_id_to + 1,
                        })
                    if len(lines_to_edit) == 2:
                        break
                else:
                    continue
                break

            if len(lines_to_edit) < 2:
                return

            direction = 3  # right side (to)
            for line in lines_to_edit:
                processing_target_id = index[line["batch_id"]][line["batch_index_id"]][2]
                new_ids = json.dumps([line["update_to"]])
                text = helper.get_splitted_to_by_id(db_path, [line["update_to"]])
                if not text:
                    return
                text = text[0][1]
                _update_processing(db, TYPE_TO, processing_target_id, new_ids, text)
                index[line["batch_id"]][line["batch_index_id"]][direction] = new_ids

        else:
            return

        if update_index:
            aligner.update_doc_index(db, index)


def split_sentence(user_id: int, alignment: Alignment, data) -> None:
    from lingtrain_aligner import aligner, helper

    db_path = _get_db_path(user_id, alignment)

    helper.ensure_splitted_pk_is_not_exists(db_path, data.direction)
    helper.insert_new_splitted_line(db_path, data.direction, data.line_id)
    helper.update_splitted_text(db_path, data.direction, data.line_id, data.part1)
    helper.update_splitted_text(db_path, data.direction, data.line_id + 1, data.part2)
    helper.update_processing_mapping(db_path, data.direction, data.line_id)
    aligner.update_index_mapping(db_path, data.direction, data.line_id)


def get_candidates(
    user_id: int,
    alignment: Alignment,
    text_type: str,
    index_id: int,
    count_before: int,
    count_after: int,
    shift: int,
) -> list:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    index = helper.get_clear_flatten_doc_index(db_path)

    if index_id < 0 or index_id >= len(index):
        return []

    direction = 3 if text_type == TYPE_TO else 1
    if index_id > 0:
        line_ids = _parse_json_array(index[index_id - 1][direction])
    else:
        line_ids = _parse_json_array(index[index_id][direction])

    while index_id > 0:
        if not line_ids:
            index_id -= 1
            line_ids = _parse_json_array(index[index_id][direction])
        else:
            break

    if not line_ids or index_id == 0:
        line_id = 1
    else:
        line_id = line_ids[0]

    id_from = line_id - count_before + shift
    id_to = line_id + count_after + shift

    return _get_candidates_page(db_path, text_type, max(0, id_from), max(id_to, 10))


def switch_excluded(user_id: int, alignment: Alignment, line_id: int, text_type: str) -> None:
    db_path = _get_db_path(user_id, alignment)
    with sqlite3.connect(db_path) as db:
        table = "splitted_from" if text_type == "from" else "splitted_to"
        exclude = db.execute(
            f"select exclude from {table} where id=:id", {"id": line_id}
        ).fetchone()
        if exclude:
            db.execute(
                f"update {table} set exclude=:exclude where id=:id",
                {"exclude": (exclude[0] + 1) % 2, "id": line_id},
            )


def get_splitted_by_ids(
    user_id: int, alignment: Alignment, direction: str, ids: list[int]
) -> dict:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    res = {}
    if not ids:
        return res

    if direction == "from":
        for row in helper.get_splitted_from_by_id(db_path, ids):
            res[row[0]] = {"t": row[1], "p": row[2] if row[2] else "", "e": row[3] == 1}
    else:
        for row in helper.get_splitted_to_by_id(db_path, ids):
            res[row[0]] = {"t": row[1], "p": row[2] if row[2] else "", "e": row[3] == 1}

    return res


def get_line_position(
    user_id: int, alignment: Alignment, lang: str, line_id: int
) -> int:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    direction = "from" if lang == alignment.lang_from else "to"
    index = helper.get_flatten_doc_index(db_path)
    direction_pos = 1 if direction == "from" else 3
    for i, item in enumerate(index):
        ids = json.loads(item[0][direction_pos])
        if line_id in ids:
            return i
    return -1


def get_alignment_marks(user_id: int, alignment: Alignment) -> dict:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)
    meta_dict = helper.get_meta_dict(db_path)
    res = {alignment.lang_from: [], alignment.lang_to: []}

    for mark_name in meta_dict:
        for mark_tuple in meta_dict[mark_name]:
            val = mark_tuple[0]
            idx = mark_tuple[1]
            pid = mark_tuple[2]
            mid = mark_tuple[3]
            if mark_name.endswith("from"):
                res[alignment.lang_from].append(
                    (val, idx, mark_name[: len(mark_name) - 5], pid, mid)
                )
            else:
                res[alignment.lang_to].append(
                    (val, idx, mark_name[: len(mark_name) - 3], pid, mid)
                )

    return res


def add_alignment_mark(user_id: int, alignment: Alignment, data) -> bool:
    from lingtrain_aligner import helper, preprocessor

    db_path = _get_db_path(user_id, alignment)

    if (
        data.type in preprocessor.MARKS_FOR_ADDING
        and data.val_from
        and data.val_to
        and data.par_id_from >= 0
        and data.par_id_to >= 0
    ):
        helper.add_meta(
            db_path, data.type, data.val_from, data.val_to, data.par_id_from, data.par_id_to
        )
        return True
    return False


def bulk_add_alignment_mark(user_id: int, alignment: Alignment, raw_info: str) -> bool:
    from lingtrain_aligner import helper, preprocessor

    db_path = _get_db_path(user_id, alignment)

    if not raw_info:
        return False

    text_info = raw_info.split("\n")
    info = [
        (x.split(",")[0], x.split(",")[1], x.split(",")[2])
        for x in text_info
        if len(x.split(",")) > 2
    ]
    info.sort(key=lambda x: x[1])
    for i in range(0, len(info), 2):
        if i + 1 < len(info):
            helper.add_meta(
                db_path,
                preprocessor.IMAGE,
                info[i][0],
                info[i + 1][0],
                info[i][1],
                info[i + 1][1],
                info[i][2],
                info[i + 1][2],
            )
    return True


def edit_alignment_mark(user_id: int, alignment: Alignment, data) -> bool:
    from lingtrain_aligner import helper

    db_path = _get_db_path(user_id, alignment)

    if data.mark_id > 0 and data.operation == "delete":
        helper.delete_meta(db_path, data.mark_id)
        return True

    if data.operation == "edit" and data.value and data.par_id >= 0 and data.mark_id > 0:
        helper.edit_meta(db_path, data.type, data.direction, data.mark_id, data.par_id, data.value)
        return True

    return False


def _get_candidates_page(db_path, text_type, id_from, id_to):
    res = []
    with sqlite3.connect(db_path) as db:
        if text_type == TYPE_FROM:
            for row_id, splitted, proxy in db.execute(
                "SELECT sf.id, sf.text, sf.proxy_text FROM splitted_from sf WHERE sf.id >= :id_from and sf.id <= :id_to ORDER BY sf.id",
                {"id_from": id_from, "id_to": id_to},
            ):
                res.append({"id": row_id, "text": splitted, "proxy": proxy})
        elif text_type == TYPE_TO:
            for row_id, splitted, proxy in db.execute(
                "SELECT st.id, st.text, st.proxy_text FROM splitted_to st WHERE st.id >= :id_from and st.id <= :id_to ORDER BY st.id",
                {"id_from": id_from, "id_to": id_to},
            ):
                res.append({"id": row_id, "text": splitted, "proxy": proxy})
    return res


def _file_exists(path: str) -> bool:
    import os
    return os.path.isfile(path)
