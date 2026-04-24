from datetime import datetime

from app.schemas.common import APIModel


class UserProfile(APIModel):
    id: int
    phone: str
    nickname: str
    avatar: str
    gender: int
    college: str
    grade: str
    bio: str
    role: str
    status: int
    created_at: datetime


class UserSummary(APIModel):
    id: int
    nickname: str
    avatar: str
    college: str
    grade: str
    bio: str
