from fastapi import APIRouter, Depends

from app.api.deps import DbSession, get_current_user
from app.schemas.common import success_response
from app.services.message_service import list_messages, read_all_messages, read_message
from app.services.serializers import serialize_message

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.get("")
def get_messages(db: DbSession, current_user=Depends(get_current_user)) -> dict:
    items = list_messages(db, current_user)
    return success_response([serialize_message(item) for item in items])


@router.post("/read/{message_id}")
def mark_message_as_read(message_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    message = read_message(db, current_user, message_id)
    return success_response(serialize_message(message) if message else None, "已标记已读")


@router.post("/read-all")
def mark_all_messages_as_read(db: DbSession, current_user=Depends(get_current_user)) -> dict:
    count = read_all_messages(db, current_user)
    return success_response({"updated": count}, "全部已读")
