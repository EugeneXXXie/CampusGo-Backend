from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_signup import ActivitySignup
from app.models.user import User
from app.services.activity_service import recompute_activity_status
from app.services.message_service import create_message


def _get_signup_or_error(db: Session, signup_id: int) -> ActivitySignup:
    signup = db.scalar(select(ActivitySignup).where(ActivitySignup.id == signup_id))
    if signup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报名记录不存在")
    return signup


def _ensure_activity_owner(activity: Activity, user: User) -> None:
    if activity.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只有活动发起人可以执行该操作")


def create_signup(db: Session, activity: Activity, user: User) -> ActivitySignup:
    if activity.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能报名自己发起的活动")
    if activity.status == "ended":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="活动已结束")
    if activity.current_participants >= activity.max_participants:
        activity.status = "full"
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="活动人数已满")

    signup = db.scalar(
        select(ActivitySignup).where(
            ActivitySignup.activity_id == activity.id,
            ActivitySignup.user_id == user.id,
        )
    )
    if signup is not None and signup.status not in {"cancelled", "rejected"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="你已经报过名了")

    if signup is None:
        signup = ActivitySignup(activity_id=activity.id, user_id=user.id, remark="")
        db.add(signup)

    if activity.audit_required:
        signup.status = "pending"
    else:
        signup.status = "approved"
        activity.current_participants += 1
        recompute_activity_status(activity)

    create_message(
        db,
        user_id=activity.user_id,
        message_type="signup",
        title="有人报名了你的活动",
        content=f"{user.nickname} 报名了「{activity.title}」",
        related_id=activity.id,
    )
    db.commit()
    db.refresh(signup)
    return signup


def list_signups(db: Session, activity: Activity, user: User) -> list[ActivitySignup]:
    _ensure_activity_owner(activity, user)
    return list(
        db.scalars(
            select(ActivitySignup).where(ActivitySignup.activity_id == activity.id).order_by(ActivitySignup.created_at.asc())
        )
    )


def approve_signup(db: Session, signup_id: int, user: User) -> ActivitySignup:
    signup = _get_signup_or_error(db, signup_id)
    activity = db.get(Activity, signup.activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    _ensure_activity_owner(activity, user)
    if signup.status != "pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="只有待审核报名可以通过")
    if activity.current_participants >= activity.max_participants:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="活动人数已满")

    signup.status = "approved"
    activity.current_participants += 1
    recompute_activity_status(activity)
    create_message(
        db,
        user_id=signup.user_id,
        message_type="review",
        title="报名审核通过",
        content=f"你报名的「{activity.title}」已经通过审核",
        related_id=activity.id,
    )
    db.commit()
    db.refresh(signup)
    return signup


def reject_signup(db: Session, signup_id: int, user: User) -> ActivitySignup:
    signup = _get_signup_or_error(db, signup_id)
    activity = db.get(Activity, signup.activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    _ensure_activity_owner(activity, user)
    if signup.status != "pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="只有待审核报名可以拒绝")

    signup.status = "rejected"
    create_message(
        db,
        user_id=signup.user_id,
        message_type="review",
        title="报名审核未通过",
        content=f"你报名的「{activity.title}」未通过审核",
        related_id=activity.id,
    )
    db.commit()
    db.refresh(signup)
    return signup


def cancel_signup(db: Session, signup_id: int, user: User) -> ActivitySignup:
    signup = _get_signup_or_error(db, signup_id)
    if signup.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能取消自己的报名")

    activity = db.get(Activity, signup.activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")

    if signup.status == "approved" and activity.current_participants > 0:
        activity.current_participants -= 1
        recompute_activity_status(activity)

    signup.status = "cancelled"
    db.commit()
    db.refresh(signup)
    return signup
