from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import DbSession, get_current_user
from app.models.activity_comment import ActivityComment
from app.schemas.comment import CommentCreate
from app.schemas.common import success_response
from app.services.activity_service import get_activity_or_none
from app.services.comment_service import create_comment, delete_comment, list_comments
from app.services.serializers import serialize_comment

router = APIRouter(tags=["comments"])


@router.get("/api/activities/{activity_id}/comments")
def get_comments(activity_id: int, db: DbSession) -> dict:
    comments = list_comments(db, activity_id)
    return success_response([serialize_comment(item) for item in comments])


@router.post("/api/activities/{activity_id}/comments")
def post_comment(activity_id: int, payload: CommentCreate, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    comment = create_comment(db, activity, current_user, payload)
    return success_response(serialize_comment(comment), "评论成功")


@router.delete("/api/comments/{comment_id}")
def remove_comment(comment_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    comment = db.scalar(select(ActivityComment).where(ActivityComment.id == comment_id))
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")
    delete_comment(db, comment, current_user)
    return success_response(True, "评论已删除")
