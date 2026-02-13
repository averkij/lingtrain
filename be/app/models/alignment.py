import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AlignmentState(enum.IntEnum):
    INIT = 0
    IN_PROGRESS = 1
    IN_PROGRESS_DONE = 2
    DONE = 3
    ERROR = 4


class Alignment(Base):
    __tablename__ = "alignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    guid: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    document_from_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), index=True
    )
    document_to_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), index=True
    )
    lang_from: Mapped[str] = mapped_column(String(10))
    lang_to: Mapped[str] = mapped_column(String(10))
    state: Mapped[int] = mapped_column(Integer, default=AlignmentState.INIT)
    curr_batches: Mapped[int] = mapped_column(Integer, default=0)
    total_batches: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_uploaded: Mapped[bool] = mapped_column(Boolean, default=False)
    proxy_from_loaded: Mapped[bool] = mapped_column(Boolean, default=False)
    proxy_to_loaded: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="alignments")
    document_from: Mapped["Document"] = relationship(
        back_populates="alignments_from",
        foreign_keys=[document_from_id],
    )
    document_to: Mapped["Document"] = relationship(
        back_populates="alignments_to",
        foreign_keys=[document_to_id],
    )
    progress_entries: Mapped[list["AlignmentProgress"]] = relationship(
        back_populates="alignment",
    )


from app.models.user import User  # noqa: E402, F811
from app.models.document import Document  # noqa: E402, F811
from app.models.alignment_progress import AlignmentProgress  # noqa: E402, F811
