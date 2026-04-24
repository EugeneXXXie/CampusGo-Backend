from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_comment import ActivityComment
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.services.message_service import create_message


def list_comments(db: Session, activity_id: int) -> list[ActivityComment]:
    return list(
        db.scalars(
            select(ActivityComment)
            .where(ActivityComment.activity_id == activity_id)
            .order_by(ActivityComment.created_at.asc())
        )
    )


def create_comment(db: Session, activity: Activity, user: User, payload: CommentCreate) -> ActivityComment:
    parent = None
    if payload.parent_id is not None:
        parent = db.scalar(
            select(ActivityComment).where(
                ActivityComment.id == payload.parent_id,
                ActivityComment.activity_id == activity.id,
            )
        )
        if parent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="回复的评论不存在")

    comment = ActivityComment(
        activity_id=activity.id,
        user_id=user.id,
        parent_id=payload.parent_id,
        content=payload.content,
        status=1,
    )
    db.add(comment)
    db.flush()

    if parent is not None and parent.user_id != user.id:
        create_message(
            db,
            user_id=parent.user_id,
            message_type="comment",
            title="有人回复了你的评论",
            content=f"{user.nickname} 回复了你在「{activity.title}」下的评论",
            related_id=activity.id,
        )

    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment: ActivityComment, user: User) -> None:
    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能删除自己的评论")
    db.delete(comment)
    db.commit()
