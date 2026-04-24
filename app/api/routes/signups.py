from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, get_current_user
from app.schemas.common import success_response
from app.services.activity_service import get_activity_or_none
from app.services.serializers import serialize_signup
from app.services.signup_service import (
    approve_signup,
    cancel_signup,
    create_signup,
    list_signups,
    reject_signup,
)

router = APIRouter(tags=["signups"])


@router.post("/api/activities/{activity_id}/signup")
def signup_activity(activity_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    signup = create_signup(db, activity, current_user)
    return success_response(serialize_signup(signup), "报名成功")


@router.get("/api/activities/{activity_id}/signups")
def get_activity_signups(activity_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    signups = list_signups(db, activity, current_user)
    return success_response([serialize_signup(item) for item in signups])


@router.post("/api/signups/{signup_id}/approve")
def approve(signup_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    signup = approve_signup(db, signup_id, current_user)
    return success_response(serialize_signup(signup), "审核通过")


@router.post("/api/signups/{signup_id}/reject")
def reject(signup_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    signup = reject_signup(db, signup_id, current_user)
    return success_response(serialize_signup(signup), "已拒绝报名")


@router.post("/api/signups/{signup_id}/cancel")
def cancel(signup_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    signup = cancel_signup(db, signup_id, current_user)
    return success_response(serialize_signup(signup), "已取消报名")
