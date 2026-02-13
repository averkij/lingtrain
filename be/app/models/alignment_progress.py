from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AlignmentProgress(Base):
    __tablename__ = "alignment_progress"
    __table_args__ = (
        UniqueConstraint("alignment_id", "batch_id", name="uq_alignment_batch"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    alignment_id: Mapped[int] = mapped_column(
        ForeignKey("alignments.id"), index=True
    )
    batch_id: Mapped[int] = mapped_column(Integer)

    alignment: Mapped["Alignment"] = relationship(
        back_populates="progress_entries",
    )


from app.models.alignment import Alignment  # noqa: E402, F811
