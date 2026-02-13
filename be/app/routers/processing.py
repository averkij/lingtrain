"""Processing router - aligned pairs, editing, splitting, candidates"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.alignment import EditRequest, SplitRequest
from app.services import alignment_service, editor_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/aligner/processing", tags=["processing"])


@router.get("/{guid}/page")
def get_processing_page(
    guid: str,
    count: int = Query(50),
    page: int = Query(1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    return editor_service.get_processing_page(user.id, alignment, count, page)


@router.post("/{guid}/page/by-ids")
def get_processing_by_ids(
    guid: str,
    index_ids: list[int],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    return editor_service.get_processing_by_ids(user.id, alignment, index_ids)


@router.get("/{guid}/meta")
def get_processing_meta(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    return {"meta": editor_service.get_processing_meta(user.id, alignment)}


@router.get("/{guid}/index")
def get_doc_index(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    return {"items": editor_service.get_doc_index(user.id, alignment)}


@router.post("/{guid}/edit")
def edit_processing(
    guid: str,
    data: EditRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    editor_service.edit_doc(user.id, alignment, data)
    return {"status": "ok"}


@router.post("/{guid}/split")
def split_sentence(
    guid: str,
    data: SplitRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if data.direction not in ("from", "to"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid direction"
        )

    editor_service.split_sentence(user.id, alignment, data)
    return {"status": "ok"}


@router.get("/{guid}/candidates")
def get_candidates(
    guid: str,
    text_type: str = Query("to"),
    index_id: int = Query(...),
    count_before: int = Query(10),
    count_after: int = Query(10),
    shift: int = Query(0),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if text_type not in ("from", "to"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid text_type"
        )

    candidates = editor_service.get_candidates(
        user.id, alignment, text_type, index_id, count_before, count_after, shift
    )
    return {"items": candidates}


@router.post("/{guid}/exclude")
def switch_excluded(
    guid: str,
    line_id: int = Query(...),
    text_type: str = Query("from"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    editor_service.switch_excluded(user.id, alignment, line_id, text_type)
    return {"status": "ok"}


@router.get("/{guid}/splitted/{direction}")
def get_splitted_by_ids(
    guid: str,
    direction: str,
    ids: str = Query("[]"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if direction not in ("from", "to"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid direction"
        )

    import json
    try:
        id_list = json.loads(ids)
    except Exception:
        id_list = []

    return {"items": editor_service.get_splitted_by_ids(user.id, alignment, direction, id_list)}


@router.get("/{guid}/find/{lang}/{line_id}")
def get_line_position(
    guid: str,
    lang: str,
    line_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    pos = editor_service.get_line_position(user.id, alignment, lang, line_id)
    return {"pos": pos}
