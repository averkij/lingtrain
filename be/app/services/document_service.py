"""Document service - migrated from a-studio/backend/user_db_helper.py + misc.py"""

import logging
import uuid

from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.file_storage import (
    ensure_user_dirs,
    get_raw_dir,
    get_splitted_dir,
    get_proxy_dir,
)

logger = logging.getLogger(__name__)


def list_documents(
    db: Session, user_id: int, lang: str | None = None
) -> list[Document]:
    q = db.query(Document).filter(Document.user_id == user_id)
    if lang:
        q = q.filter(Document.lang == lang)
    return q.order_by(Document.created_at.desc()).all()


def get_document_by_guid(
    db: Session, user_id: int, guid: str
) -> Document | None:
    return (
        db.query(Document)
        .filter(Document.user_id == user_id, Document.guid == guid)
        .first()
    )


def register_document(
    db: Session, user_id: int, lang: str, name: str
) -> Document:
    doc = Document(
        user_id=user_id,
        guid=uuid.uuid4().hex,
        lang=lang,
        name=name,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def delete_document(db: Session, user_id: int, guid: str) -> None:
    doc = get_document_by_guid(db, user_id, guid)
    if not doc:
        return

    raw_path = get_raw_dir(user_id, doc.lang) / doc.name
    splitted_path = get_splitted_dir(user_id, doc.lang) / doc.name
    proxy_path = get_proxy_dir(user_id, doc.lang) / doc.name

    for p in (raw_path, splitted_path, proxy_path):
        if p.is_file():
            p.unlink()

    db.delete(doc)
    db.commit()


def save_uploaded_file(
    user_id: int,
    lang: str,
    filename: str,
    content: bytes,
    clean_text: bool = False,
) -> None:
    from lingtrain_aligner import splitter

    ensure_user_dirs(user_id, lang)

    raw_path = get_raw_dir(user_id, lang) / filename
    raw_path.write_bytes(content)

    splitted_path = get_splitted_dir(user_id, lang) / filename
    splitter.split_by_sentences_and_save(
        str(raw_path),
        str(splitted_path),
        lang,
        handle_marks=True,
        clean_text=clean_text,
    )


def get_splitted_page(
    user_id: int, lang: str, filename: str, count: int, page: int
) -> dict:
    from lingtrain_aligner import preprocessor

    splitted_path = get_splitted_dir(user_id, lang) / filename
    if not splitted_path.is_file():
        return {"items": {lang: []}, "meta": {lang: {}}}

    lines = []
    lines_count = 0
    symbols_count = 0
    shift = (page - 1) * count

    with open(splitted_path, mode="r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            lines_count += 1
            symbols_count += len(line)
            if count > 0 and (lines_count <= shift or lines_count > shift + count):
                continue
            parsed = preprocessor.parse_marked_line(line.strip())
            lines.append((parsed, lines_count))

    total_pages = (lines_count // count) + (1 if lines_count % count != 0 else 0)
    meta = {
        "lines_count": lines_count - 1,
        "symbols_count": symbols_count,
        "page": page,
        "total_pages": total_pages,
    }
    return {"items": {lang: lines}, "meta": {lang: meta}}


def get_document_marks(user_id: int, lang: str, filename: str) -> list:
    from lingtrain_aligner import preprocessor

    splitted_path = get_splitted_dir(user_id, lang) / filename
    if not splitted_path.is_file():
        return []

    marks = []
    with open(splitted_path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            preprocessor.extract_marks(marks, line.strip(), i)
    return marks
