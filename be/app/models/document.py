from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    guid: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    lang: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="documents")
    alignments_from: Mapped[list["Alignment"]] = relationship(
        back_populates="document_from",
        foreign_keys="[Alignment.document_from_id]",
    )
    alignments_to: Mapped[list["Alignment"]] = relationship(
        back_populates="document_to",
        foreign_keys="[Alignment.document_to_id]",
    )


from app.models.user import User  # noqa: E402, F811
from app.models.alignment import Alignment  # noqa: E402, F811
