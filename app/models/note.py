import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Note(Base):
    __tablename__ = "notes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'archived', 'trash')",
            name="ck_notes_status",
        ),
        Index("ix_notes_user_id", "user_id"),
        Index("ix_notes_created_at", "created_at"),
        Index("ix_notes_updated_at", "updated_at"),
        Index("ix_notes_status_updated_at", "status", "updated_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(120), nullable=False, default="", server_default=text("''")
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, default="", server_default=text("''")
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="active", server_default=text("'active'")
    )
    pinned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    user: Mapped["User"] = relationship(back_populates="notes")