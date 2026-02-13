"""Alignments router - create, list, align, resolve, conflicts"""

import logging
from threading import Thread

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.alignment import AlignmentState
from app.models.user import User
from app.schemas.alignment import (
    AlignmentCreate,
    AlignmentOut,
    AlignNext,
    AlignStart,
    ResolveRequest,
)
from app.services import alignment_service, processing_service
from app.services.document_service import get_document_by_guid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/aligner/alignments", tags=["alignments"])


@router.get("/", response_model=list[AlignmentOut])
def list_alignments(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return alignment_service.list_alignments(db, user.id)


@router.post("/", response_model=AlignmentOut, status_code=status.HTTP_201_CREATED)
def create_alignment(
    data: AlignmentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc_from = get_document_by_guid(db, user.id, data.document_from_guid)
    doc_to = get_document_by_guid(db, user.id, data.document_to_guid)
    if not doc_from or not doc_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source or target document not found",
        )

    alignment = alignment_service.create_alignment(
        db, user.id, doc_from, doc_to, data.name
    )
    return alignment


@router.delete("/{guid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alignment(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")
    alignment_service.delete_alignment(db, user.id, guid)


@router.post("/{guid}/align")
def start_alignment(
    guid: str,
    data: AlignStart,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    if data.align_all:
        alignment_service.update_state(
            db, alignment.id, AlignmentState.INIT, 0, alignment.total_batches
        )
    alignment_service.update_state(db, alignment.id, AlignmentState.IN_PROGRESS)

    # Run in background thread to not block the response
    thread = Thread(
        target=processing_service.start_alignment,
        args=(user.id, alignment, data),
        daemon=True,
    )
    thread.start()

    return {"status": "started"}


@router.post("/{guid}/align/next")
def align_next(
    guid: str,
    data: AlignNext,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    alignment_service.update_state(db, alignment.id, AlignmentState.IN_PROGRESS)

    thread = Thread(
        target=processing_service.align_next,
        args=(user.id, alignment, data),
        daemon=True,
    )
    thread.start()

    return {"status": "started"}


@router.post("/{guid}/align/stop")
def stop_alignment(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    processing_service.stop_alignment(db, alignment)
    return {"status": "stopped"}


@router.post("/{guid}/resolve")
def resolve_conflicts(
    guid: str,
    data: ResolveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    alignment_service.update_state(db, alignment.id, AlignmentState.IN_PROGRESS)

    thread = Thread(
        target=processing_service.resolve_conflicts,
        args=(user.id, alignment, data),
        daemon=True,
    )
    thread.start()

    return {"status": "started"}


@router.get("/{guid}/conflicts")
def get_conflicts(
    guid: str,
    handle_edges: str = Query("none"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    return processing_service.get_conflicts(user.id, alignment, handle_edges)


@router.get("/{guid}/conflicts/{conflict_id}")
def show_conflict(
    guid: str,
    conflict_id: int,
    handle_edges: str = Query("none"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    return processing_service.show_conflict(user.id, alignment, conflict_id, handle_edges)


@router.post("/{guid}/visualize")
def update_visualization(
    guid: str,
    batch_ids: list[int] = [],
    update_all: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    processing_service.update_visualization(user.id, alignment, batch_ids, update_all)
    return {"status": "ok"}


@router.post("/{guid}/proxy/{direction}", response_model=AlignmentOut)
async def upload_proxy(
    guid: str,
    direction: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if direction not in ("from", "to"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="direction must be 'from' or 'to'",
        )
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    content = (await file.read()).decode("utf-8")
    alignment_service.upload_proxy(user.id, alignment, direction, content)
    return alignment_service.update_proxy_loaded(db, alignment.id, direction)


@router.get("/{guid}/progress", response_model=AlignmentOut)
def get_progress(
    guid: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    db.refresh(alignment)
    return alignment
