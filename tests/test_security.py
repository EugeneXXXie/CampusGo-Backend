from app.core.security import get_password_hash, verify_password


def test_password_hash_roundtrip() -> None:
    raw = "123456"
    hashed = get_password_hash(raw)

    assert hashed != raw
    assert verify_password(raw, hashed) is True
