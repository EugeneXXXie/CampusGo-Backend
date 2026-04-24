from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest


def register_user(db: Session, payload: RegisterRequest) -> User:
    existed = db.scalar(select(User).where(User.phone == payload.phone))
    if existed is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="手机号已注册")

    user = User(
        phone=payload.phone,
        password_hash=get_password_hash(payload.password),
        nickname=payload.nickname,
        avatar=payload.avatar,
        gender=payload.gender,
        college=payload.college,
        grade=payload.grade,
        bio=payload.bio,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> tuple[str, User]:
    user = db.scalar(select(User).where(User.phone == payload.phone))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="手机号或密码错误")

    token = create_access_token(user.id)
    return token, user
