from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_comment import ActivityComment
from app.models.activity_signup import ActivitySignup
from app.models.favorite import Favorite
from app.models.message import Message
from app.models.user import User


def serialize_user_summary(user: User) -> dict:
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "college": user.college,
        "grade": user.grade,
        "bio": user.bio,
    }


def serialize_comment(comment: ActivityComment) -> dict:
    reply_to = comment.parent.user.nickname if comment.parent is not None and comment.parent.user is not None else None
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "user_name": comment.user.nickname if comment.user is not None else "",
        "parent_id": comment.parent_id,
        "reply_to": reply_to,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
    }


def serialize_message(message: Message | None) -> dict | None:
    if message is None:
        return None
    return {
        "id": message.id,
        "type": message.type,
        "title": message.title,
        "content": message.content,
        "is_read": message.is_read,
        "related_id": message.related_id,
        "created_at": message.created_at.isoformat(),
    }


def serialize_signup(signup: ActivitySignup) -> dict:
    return {
        "id": signup.id,
        "activity_id": signup.activity_id,
        "user_id": signup.user_id,
        "status": signup.status,
        "remark": signup.remark,
        "created_at": signup.created_at.isoformat(),
        "user": serialize_user_summary(signup.user),
    }


def serialize_activity(
    db: Session,
    activity: Activity,
    *,
    current_user: User | None,
    include_comments: bool,
) -> dict:
    is_favorite = False
    signup_status = "none"

    if hasattr(activity, "_is_favorite"):
        is_favorite = bool(activity._is_favorite)  # type: ignore[attr-defined]
    elif current_user is not None:
        is_favorite = (
            db.scalar(
                select(Favorite).where(Favorite.user_id == current_user.id, Favorite.activity_id == activity.id)
            )
            is not None
        )

    if hasattr(activity, "_signup_status"):
        signup_status = str(activity._signup_status)  # type: ignore[attr-defined]
    elif current_user is not None:
        signup = db.scalar(
            select(ActivitySignup).where(
                ActivitySignup.user_id == current_user.id,
                ActivitySignup.activity_id == activity.id,
            )
        )
        if signup is not None:
            signup_status = signup.status

    summary = activity.description[:60]

    comments = []
    if include_comments:
        comments = [serialize_comment(item) for item in sorted(activity.comments, key=lambda row: row.created_at)]

    return {
        "id": activity.id,
        "title": activity.title,
        "cover": activity.cover,
        "description": activity.description,
        "summary": summary,
        "activity_time": activity.activity_time.isoformat(),
        "location": activity.location,
        "max_participants": activity.max_participants,
        "current_participants": activity.current_participants,
        "audit_required": activity.audit_required,
        "status": activity.status,
        "contact_info": activity.contact_info,
        "view_count": activity.view_count,
        "is_favorite": is_favorite,
        "signup_status": signup_status,
        "owner": serialize_user_summary(activity.owner),
        "category": {
            "id": activity.category.id,
            "name": activity.category.name,
        },
        "comments": comments,
        "created_at": activity.created_at.isoformat(),
    }
