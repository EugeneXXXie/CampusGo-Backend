from app.models.activity import Activity
from app.models.user import User


def test_models_have_tablenames() -> None:
    assert User.__tablename__ == "users"
    assert Activity.__tablename__ == "activities"
