"""Documents router - file upload, listing, deletion, splitted preview"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentOut
from app.services import document_service
from app.services.file_storage import get_splitted_dir

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/aligner/documents", tags=["documents"])


@router.get("/", response_model=list[DocumentOut])
def list_documents(
    lang: str = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return document_service.list_documents(db, user.id, lang)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    lang: str = Form(...),
    clean_text: bool = Form(False),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Check if file with same name+lang already exists
    docs = document_service.list_documents(db, user.id, lang)
    for doc in docs:
        if doc.name == file.filename:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="File already exists",
            )

    content = await file.read()
    document_service.save_uploaded_file(user.id, lang, file.filename, content, clean_text)
    doc = document_service.register_document(db, user.id, lang, file.filename)
    return DocumentOut.model_validate(doc)


@router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc = document_service.get_document_by_guid(db, user.id, guid)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    document_service.delete_document(db, user.id, guid)


@router.get("/{guid}/splitted")
def get_splitted(
    guid: str,
    count: int = Query(50),
    page: int = Query(1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc = document_service.get_document_by_guid(db, user.id, guid)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    raw = document_service.get_splitted_page(user.id, doc.lang, doc.name, count, page)
    items = raw.get("items", {}).get(doc.lang, [])
    meta = raw.get("meta", {}).get(doc.lang, {})

    # Mark short codes to full names
    mark_names = {
        "au": "author", "ti": "title", "h1": "h1", "h2": "h2",
        "h3": "h3", "h4": "h4", "h5": "h5", "pa": "paragraph",
        "qt": "qtext",
    }

    lines = []
    for parsed, line_number in items:
        # parsed is a defaultdict(bool) with 'text' key and mark flag keys
        if hasattr(parsed, "get"):
            text = parsed.get("text", "")
            mark = None
            for code, name in mark_names.items():
                if parsed.get(code):
                    mark = name
                    break
        else:
            text = str(parsed)
            mark = None
        lines.append({"id": line_number, "text": text, "mark": mark})
    return {
        "lines": lines,
        "total": meta.get("lines_count", 0),
        "page": meta.get("page", page),
        "count": count,
    }


@router.get("/{guid}/splitted/download")
def download_splitted(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc = document_service.get_document_by_guid(db, user.id, guid)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    path = get_splitted_dir(user.id, doc.lang) / doc.name
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Splitted file not found")

    return FileResponse(str(path), filename=doc.name)


@router.get("/{guid}/marks")
def get_marks(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc = document_service.get_document_by_guid(db, user.id, guid)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    raw_marks = document_service.get_document_marks(user.id, doc.lang, doc.name)
    # raw_marks is list of tuples: (text, line_index, mark_type)
    marks = []
    for m in raw_marks:
        marks.append({"text": m[0], "line": m[1] + 1, "type": m[2]})
    return {"marks": marks}
