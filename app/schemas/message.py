from datetime import datetime

from app.schemas.common import APIModel


class MessageData(APIModel):
    id: int
    type: str
    title: str
    content: str
    is_read: bool
    related_id: int | None
    created_at: datetime
