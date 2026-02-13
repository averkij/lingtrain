"""Marks router - alignment marks management"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.alignment import MarkAdd, MarkEdit
from app.services import alignment_service, editor_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/aligner/marks", tags=["marks"])


@router.get("/{guid}")
def get_alignment_marks(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    marks = editor_service.get_alignment_marks(user.id, alignment)
    return {"items": marks}


@router.post("/{guid}/add")
def add_mark(
    guid: str,
    data: MarkAdd,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if not editor_service.add_alignment_mark(user.id, alignment, data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parameters"
        )
    return {"status": "ok"}


@router.post("/{guid}/bulk-add")
def bulk_add_marks(
    guid: str,
    raw_info: str = "",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if not editor_service.bulk_add_alignment_mark(user.id, alignment, raw_info):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parameters"
        )
    return {"status": "ok"}


@router.post("/{guid}/edit")
def edit_mark(
    guid: str,
    data: MarkEdit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if not editor_service.edit_alignment_mark(user.id, alignment, data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parameters"
        )
    return {"status": "ok"}
