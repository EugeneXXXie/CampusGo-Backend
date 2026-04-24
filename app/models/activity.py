from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("activity_categories.id"), index=True)
    title: Mapped[str] = mapped_column(String(100))
    cover: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text)
    activity_time: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String(255))
    max_participants: Mapped[int] = mapped_column(Integer)
    current_participants: Mapped[int] = mapped_column(Integer, default=0)
    audit_required: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="open")
    contact_info: Mapped[str] = mapped_column(String(100))
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="activities")
    category = relationship("ActivityCategory", back_populates="activities")
    signups = relationship("ActivitySignup", back_populates="activity", cascade="all, delete-orphan")
    comments = relationship("ActivityComment", back_populates="activity", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="activity", cascade="all, delete-orphan")
