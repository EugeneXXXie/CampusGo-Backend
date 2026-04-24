from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, get_current_user
from app.schemas.common import success_response
from app.services.activity_service import get_activity_or_none
from app.services.favorite_service import add_favorite, remove_favorite

router = APIRouter(tags=["favorites"])


@router.post("/api/activities/{activity_id}/favorite")
def favorite_activity(activity_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    add_favorite(db, activity, current_user)
    return success_response({"activity_id": activity_id, "is_favorite": True}, "收藏成功")


@router.delete("/api/activities/{activity_id}/favorite")
def unfavorite_activity(activity_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    remove_favorite(db, activity, current_user)
    return success_response({"activity_id": activity_id, "is_favorite": False}, "已取消收藏")
