from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.user import User


def create_message(
    db: Session,
    *,
    user_id: int,
    message_type: str,
    title: str,
    content: str,
    related_id: int | None = None,
) -> Message:
    message = Message(
        user_id=user_id,
        type=message_type,
        title=title,
        content=content,
        related_id=related_id,
        is_read=False,
    )
    db.add(message)
    db.flush()
    return message


def list_messages(db: Session, user: User) -> list[Message]:
    return list(db.scalars(select(Message).where(Message.user_id == user.id).order_by(Message.created_at.desc())))


def read_message(db: Session, user: User, message_id: int) -> Message | None:
    message = db.scalar(select(Message).where(Message.id == message_id, Message.user_id == user.id))
    if message is None:
        return None

    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


def read_all_messages(db: Session, user: User) -> int:
    result = db.execute(update(Message).where(Message.user_id == user.id).values(is_read=True))
    db.commit()
    return result.rowcount or 0
