from datetime import datetime

from app.schemas.common import APIModel
from app.schemas.user import UserSummary


class ActivityBase(APIModel):
    category_id: int
    title: str
    cover: str = ""
    description: str
    activity_time: datetime
    location: str
    max_participants: int
    audit_required: bool = False
    contact_info: str


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(APIModel):
    category_id: int | None = None
    title: str | None = None
    cover: str | None = None
    description: str | None = None
    activity_time: datetime | None = None
    location: str | None = None
    max_participants: int | None = None
    audit_required: bool | None = None
    contact_info: str | None = None
    status: str | None = None


class ActivityListQuery(APIModel):
    keyword: str = ""
    category_id: int | None = None
    status: str | None = None
    page: int = 1
    page_size: int = 10


class CategoryData(APIModel):
    id: int
    name: str


class CommentData(APIModel):
    id: int
    user_id: int
    user_name: str
    parent_id: int | None
    reply_to: str | None = None
    content: str
    created_at: datetime


class ActivityData(APIModel):
    id: int
    title: str
    cover: str
    description: str
    summary: str
    activity_time: datetime
    location: str
    max_participants: int
    current_participants: int
    audit_required: bool
    status: str
    contact_info: str
    view_count: int
    is_favorite: bool
    signup_status: str
    owner: UserSummary
    category: CategoryData
    comments: list[CommentData] = []
    created_at: datetime
