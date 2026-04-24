from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.favorite import Favorite
from app.models.user import User


def add_favorite(db: Session, activity: Activity, user: User) -> bool:
    existed = db.scalar(
        select(Favorite).where(Favorite.user_id == user.id, Favorite.activity_id == activity.id)
    )
    if existed is not None:
        return True

    db.add(Favorite(user_id=user.id, activity_id=activity.id))
    db.commit()
    return True


def remove_favorite(db: Session, activity: Activity, user: User) -> bool:
    existed = db.scalar(
        select(Favorite).where(Favorite.user_id == user.id, Favorite.activity_id == activity.id)
    )
    if existed is None:
        return False

    db.delete(existed)
    db.commit()
    return False
