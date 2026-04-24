from app.schemas.common import APIModel


class CommentCreate(APIModel):
    content: str
    parent_id: int | None = None
