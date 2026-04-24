from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import DbSession, get_current_user, get_optional_user
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.schemas.common import success_response
from app.services.activity_service import (
    bump_view_count,
    create_activity,
    delete_activity,
    get_activity_or_none,
    list_activities,
    update_activity,
)
from app.services.serializers import serialize_activity

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.get("")
def get_activities(
    db: DbSession,
    current_user=Depends(get_optional_user),
    keyword: str = Query("", description="关键字"),
    category_id: int | None = Query(None),
    status_text: str | None = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
) -> dict:
    items, total = list_activities(
        db,
        current_user=current_user,
        keyword=keyword,
        category_id=category_id,
        status=status_text,
        page=page,
        page_size=page_size,
    )
    return success_response(
        {
            "items": [serialize_activity(db, item, current_user=current_user, include_comments=False) for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@router.get("/{activity_id}")
def get_activity(activity_id: int, db: DbSession, current_user=Depends(get_optional_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    activity = bump_view_count(db, activity)
    return success_response(serialize_activity(db, activity, current_user=current_user, include_comments=True))


@router.post("")
def create_new_activity(payload: ActivityCreate, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = create_activity(db, payload, current_user)
    activity = get_activity_or_none(db, activity.id)
    assert activity is not None
    return success_response(serialize_activity(db, activity, current_user=current_user, include_comments=True), "活动创建成功")


@router.put("/{activity_id}")
def edit_activity(activity_id: int, payload: ActivityUpdate, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    activity = update_activity(db, activity, payload, current_user)
    activity = get_activity_or_none(db, activity.id)
    assert activity is not None
    return success_response(serialize_activity(db, activity, current_user=current_user, include_comments=True), "活动更新成功")


@router.delete("/{activity_id}")
def remove_activity(activity_id: int, db: DbSession, current_user=Depends(get_current_user)) -> dict:
    activity = get_activity_or_none(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="活动不存在")
    delete_activity(db, activity, current_user)
    return success_response(True, "活动删除成功")
