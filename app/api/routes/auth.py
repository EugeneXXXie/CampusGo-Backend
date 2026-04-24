from fastapi import APIRouter, Depends

from app.api.deps import DbSession, get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import success_response
from app.schemas.user import UserProfile
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: DbSession) -> dict:
    user = register_user(db, payload)
    return success_response(UserProfile.model_validate(user).model_dump(), "注册成功")


@router.post("/login")
def login(payload: LoginRequest, db: DbSession) -> dict:
    token, user = login_user(db, payload)
    return success_response(
        {
            "access_token": token,
            "token_type": "bearer",
            "user": UserProfile.model_validate(user).model_dump(),
        },
        "登录成功",
    )


@router.get("/me")
def me(current_user=Depends(get_current_user)) -> dict:
    return success_response(UserProfile.model_validate(current_user).model_dump())
