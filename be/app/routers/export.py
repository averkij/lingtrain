"""Export router - download processing results and books"""

import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.alignment import BookRequest, ExportRequest
from app.services import alignment_service, export_service
from app.services.file_storage import get_alignment_db_path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/aligner/export", tags=["export"])


@router.post("/{guid}/download/{file_format}")
def download_processing(
    guid: str,
    file_format: str,
    data: ExportRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    db_path = get_alignment_db_path(
        user.id, alignment.lang_from, alignment.lang_to, alignment.guid
    )
    if not db_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment DB not found")

    download_file = export_service.download_processing(
        user.id,
        alignment,
        file_format,
        side=data.side,
        paragraphs=data.paragraphs,
        direction=data.direction,
        left_lang=data.left_lang,
    )

    if not download_file or not os.path.isfile(download_file):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Export failed")

    return FileResponse(download_file, filename=os.path.basename(download_file))


@router.post("/{guid}/book/preview")
def get_book_preview(
    guid: str,
    data: BookRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    db_path = get_alignment_db_path(
        user.id, alignment.lang_from, alignment.lang_to, alignment.guid
    )
    if not db_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment DB not found")

    html = export_service.get_book_preview(
        user.id,
        alignment,
        par_direction=data.par_direction,
        left_lang=data.left_lang,
        style=data.style,
    )

    if not html:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty alignment or no data",
        )

    return {"items": html}


@router.post("/{guid}/book/download")
def download_book(
    guid: str,
    data: BookRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    alignment = alignment_service.get_alignment(db, user.id, guid)
    if not alignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment not found")

    db_path = get_alignment_db_path(
        user.id, alignment.lang_from, alignment.lang_to, alignment.guid
    )
    if not db_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alignment DB not found")

    download_file = export_service.download_book(
        user.id,
        alignment,
        par_direction=data.par_direction,
        left_lang=data.left_lang,
        style=data.style,
    )

    if not download_file or not os.path.isfile(download_file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty alignment or no data",
        )

    return FileResponse(
        download_file, filename=os.path.basename(download_file)
    )
