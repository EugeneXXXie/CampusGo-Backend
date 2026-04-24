from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ActivityComment(Base):
    __tablename__ = "activity_comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("activity_comments.id", ondelete="CASCADE"), nullable=True)
    content: Mapped[str] = mapped_column(String(500))
    status: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    activity = relationship("Activity", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("ActivityComment", remote_side=[id])
