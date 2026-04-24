from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.activity import Activity
from app.models.activity_category import ActivityCategory
from app.models.activity_comment import ActivityComment
from app.models.activity_signup import ActivitySignup
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityUpdate


def recompute_activity_status(activity: Activity) -> None:
    if activity.status == "ended":
        return
    activity.status = "full" if activity.current_participants >= activity.max_participants else "open"


def ensure_activity_owner(activity: Activity, user: User) -> None:
    if activity.user_id != user.id:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只有发起人可以执行该操作")


def get_category_or_error(db: Session, category_id: int) -> ActivityCategory:
    category = db.get(ActivityCategory, category_id)
    if category is None:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="活动分类不存在")
    return category


def create_activity(db: Session, payload: ActivityCreate, user: User) -> Activity:
    get_category_or_error(db, payload.category_id)
    activity = Activity(
        user_id=user.id,
        category_id=payload.category_id,
        title=payload.title,
        cover=payload.cover,
        description=payload.description,
        activity_time=payload.activity_time,
        location=payload.location,
        max_participants=payload.max_participants,
        current_participants=0,
        audit_required=payload.audit_required,
        status="open",
        contact_info=payload.contact_info,
        view_count=0,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def update_activity(db: Session, activity: Activity, payload: ActivityUpdate, user: User) -> Activity:
    ensure_activity_owner(activity, user)
    data = payload.model_dump(exclude_unset=True)
    if "category_id" in data:
        get_category_or_error(db, data["category_id"])

    for key, value in data.items():
        setattr(activity, key, value)

    if activity.current_participants > activity.max_participants:
        activity.max_participants = activity.current_participants

    recompute_activity_status(activity)
    db.commit()
    db.refresh(activity)
    return activity


def delete_activity(db: Session, activity: Activity, user: User) -> None:
    ensure_activity_owner(activity, user)
    db.delete(activity)
    db.commit()


def get_activity_or_none(db: Session, activity_id: int) -> Activity | None:
    query = (
        select(Activity)
        .options(
            selectinload(Activity.owner),
            selectinload(Activity.category),
            selectinload(Activity.comments).selectinload(ActivityComment.user),
        )
        .where(Activity.id == activity_id)
    )
    return db.scalar(query)


def list_activities(
    db: Session,
    *,
    current_user: User | None,
    keyword: str = "",
    category_id: int | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[Activity], int]:
    conditions = []
    if keyword:
        pattern = f"%{keyword}%"
        conditions.append(
            or_(
                Activity.title.like(pattern),
                Activity.description.like(pattern),
                Activity.location.like(pattern),
            )
        )
    if category_id:
        conditions.append(Activity.category_id == category_id)
    if status:
        conditions.append(Activity.status == status)

    base_query = select(Activity).options(selectinload(Activity.owner), selectinload(Activity.category))
    total_query = select(func.count(Activity.id))

    for condition in conditions:
        base_query = base_query.where(condition)
        total_query = total_query.where(condition)

    total = db.scalar(total_query) or 0
    offset = max(page - 1, 0) * page_size
    items = list(
        db.scalars(base_query.order_by(Activity.created_at.desc()).offset(offset).limit(page_size))
    )

    if current_user is not None and items:
        activity_ids = [item.id for item in items]
        favorites = set(
            db.scalars(
                select(Favorite.activity_id).where(
                    Favorite.user_id == current_user.id,
                    Favorite.activity_id.in_(activity_ids),
                )
            )
        )
        signups = {
            row.activity_id: row.status
            for row in db.scalars(
                select(ActivitySignup).where(
                    ActivitySignup.user_id == current_user.id,
                    ActivitySignup.activity_id.in_(activity_ids),
                )
            )
        }
        for item in items:
            item._is_favorite = item.id in favorites  # type: ignore[attr-defined]
            item._signup_status = signups.get(item.id, "none")  # type: ignore[attr-defined]

    return items, total


def bump_view_count(db: Session, activity: Activity) -> Activity:
    activity.view_count += 1
    db.commit()
    db.refresh(activity)
    return activity
