from app.schemas.common import APIModel
from app.schemas.user import UserProfile


class RegisterRequest(APIModel):
    phone: str
    password: str
    nickname: str
    avatar: str = ""
    gender: int = 0
    college: str = ""
    grade: str = ""
    bio: str = ""


class LoginRequest(APIModel):
    phone: str
    password: str


class LoginData(APIModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
