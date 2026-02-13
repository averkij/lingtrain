"""Alignment service - migrated from a-studio/backend/user_db_helper.py"""

import logging
import sqlite3
import uuid

from sqlalchemy.orm import Session

from app.models.alignment import Alignment, AlignmentState
from app.models.alignment_progress import AlignmentProgress
from app.models.document import Document
from app.services.file_storage import (
    get_alignment_db_path,
    get_db_dir,
    get_splitted_dir,
    get_proxy_dir,
)
from app import config

logger = logging.getLogger(__name__)


def list_alignments(db: Session, user_id: int) -> list[Alignment]:
    return (
        db.query(Alignment)
        .filter(Alignment.user_id == user_id, Alignment.is_deleted == False)
        .order_by(Alignment.created_at.desc())
        .all()
    )


def get_alignment(
    db: Session, user_id: int, guid: str
) -> Alignment | None:
    return (
        db.query(Alignment)
        .filter(
            Alignment.user_id == user_id,
            Alignment.guid == guid,
            Alignment.is_deleted == False,
        )
        .first()
    )


def create_alignment(
    db: Session,
    user_id: int,
    doc_from: Document,
    doc_to: Document,
    name: str,
) -> Alignment:
    from lingtrain_aligner import aligner

    guid = uuid.uuid4().hex
    lang_from = doc_from.lang
    lang_to = doc_to.lang

    db_dir = get_db_dir(user_id, lang_from, lang_to)
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / f"{guid}.db"

    splitted_from = get_splitted_dir(user_id, lang_from) / doc_from.name
    splitted_to = get_splitted_dir(user_id, lang_to) / doc_to.name
    proxy_from_path = get_proxy_dir(user_id, lang_from) / doc_from.name
    proxy_to_path = get_proxy_dir(user_id, lang_to) / doc_to.name

    with open(splitted_from, "r", encoding="utf8") as f:
        lines_from = f.readlines()
    with open(splitted_to, "r", encoding="utf8") as f:
        lines_to = f.readlines()

    lines_proxy_from, lines_proxy_to = [], []
    if proxy_from_path.is_file():
        with open(proxy_from_path, "r", encoding="utf8") as f:
            lines_proxy_from = f.readlines()
    if proxy_to_path.is_file():
        with open(proxy_to_path, "r", encoding="utf8") as f:
            lines_proxy_to = f.readlines()

    aligner.fill_db(
        str(db_path),
        lang_from,
        lang_to,
        lines_from,
        lines_to,
        lines_proxy_from,
        lines_proxy_to,
        doc_from.name,
        doc_from.guid,
        doc_to.name,
        doc_to.guid,
        name,
    )

    # Calculate total batches
    batch_size = config.ALIGNER_BATCH_SIZE
    with sqlite3.connect(str(db_path)) as align_db:
        len_from = align_db.execute(
            "select count(*) from splitted_from"
        ).fetchone()[0]

    is_last = len_from % batch_size > 0
    total_batches = len_from // batch_size + (1 if is_last else 0)
    if config.ALIGNER_MAX_BATCHES > 0:
        total_batches = min(config.ALIGNER_MAX_BATCHES, total_batches)

    alignment = Alignment(
        user_id=user_id,
        guid=guid,
        name=name,
        document_from_id=doc_from.id,
        document_to_id=doc_to.id,
        lang_from=lang_from,
        lang_to=lang_to,
        state=AlignmentState.INIT,
        curr_batches=0,
        total_batches=total_batches,
    )
    db.add(alignment)
    db.commit()
    db.refresh(alignment)
    return alignment


def delete_alignment(db: Session, user_id: int, guid: str) -> None:
    alignment = get_alignment(db, user_id, guid)
    if alignment:
        alignment.is_deleted = True
        db.commit()


def update_state(
    db: Session,
    alignment_id: int,
    state: int,
    curr_batches: int | None = None,
    total_batches: int | None = None,
) -> None:
    alignment = db.get(Alignment, alignment_id)
    if not alignment:
        return
    alignment.state = state
    if curr_batches is not None:
        alignment.curr_batches = curr_batches
    if total_batches is not None:
        alignment.total_batches = total_batches
    db.commit()


def update_progress(db: Session, alignment_id: int, batch_id: int) -> None:
    existing = (
        db.query(AlignmentProgress)
        .filter(
            AlignmentProgress.alignment_id == alignment_id,
            AlignmentProgress.batch_id == batch_id,
        )
        .first()
    )
    if not existing:
        progress = AlignmentProgress(
            alignment_id=alignment_id, batch_id=batch_id
        )
        db.add(progress)
        db.commit()


def get_batches_count(db: Session, alignment_id: int) -> int:
    return (
        db.query(AlignmentProgress)
        .filter(AlignmentProgress.alignment_id == alignment_id)
        .count()
    )


def increment_state(db: Session, alignment_id: int, state: int) -> None:
    count = get_batches_count(db, alignment_id)
    alignment = db.get(Alignment, alignment_id)
    if alignment:
        alignment.state = state
        alignment.curr_batches = count
        db.commit()


def upload_proxy(
    user_id: int, alignment: Alignment, direction: str, content: str
) -> None:
    from lingtrain_aligner import aligner

    lang = alignment.lang_from if direction == "from" else alignment.lang_to
    proxy_dir = get_proxy_dir(user_id, lang)
    proxy_dir.mkdir(parents=True, exist_ok=True)

    # Use alignment guid as proxy filename to avoid collisions
    proxy_path = proxy_dir / f"{alignment.guid}.proxy.txt"
    with open(proxy_path, "w", encoding="utf-8") as f:
        f.write(content)

    db_path = get_alignment_db_path(
        user_id, alignment.lang_from, alignment.lang_to, alignment.guid
    )
    aligner.load_proxy(str(db_path), str(proxy_path), direction)


def update_proxy_loaded(
    db: Session, alignment_id: int, direction: str
) -> Alignment | None:
    alignment = db.get(Alignment, alignment_id)
    if not alignment:
        return None
    if direction == "from":
        alignment.proxy_from_loaded = True
    else:
        alignment.proxy_to_loaded = True
    db.commit()
    db.refresh(alignment)
    return alignment
