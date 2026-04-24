from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _get_serializer() -> URLSafeTimedSerializer:
    settings = get_settings()
    return URLSafeTimedSerializer(settings.secret_key, salt="campusgo-access-token")


def create_access_token(user_id: int) -> str:
    serializer = _get_serializer()
    return serializer.dumps({"user_id": user_id})


def parse_access_token(token: str) -> int:
    settings = get_settings()
    serializer = _get_serializer()

    try:
        data = serializer.loads(token, max_age=settings.access_token_expire_minutes * 60)
    except SignatureExpired as exc:
        raise ValueError("登录状态已过期，请重新登录") from exc
    except BadSignature as exc:
        raise ValueError("无效的登录凭证") from exc

    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        raise ValueError("无效的登录凭证")
    return user_id
