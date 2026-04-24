from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nickname: Mapped[str] = mapped_column(String(50))
    avatar: Mapped[str] = mapped_column(String(255), default="")
    gender: Mapped[int] = mapped_column(Integer, default=0)
    college: Mapped[str] = mapped_column(String(100), default="")
    grade: Mapped[str] = mapped_column(String(50), default="")
    bio: Mapped[str] = mapped_column(String(255), default="")
    role: Mapped[str] = mapped_column(String(20), default="user")
    status: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    activities = relationship("Activity", back_populates="owner")
    signups = relationship("ActivitySignup", back_populates="user")
    comments = relationship("ActivityComment", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    messages = relationship("Message", back_populates="user")
