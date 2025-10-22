from app.utils import pwd_manager


def test_hash_password_returns_hashed_value(plain_password: str):
    hashed = pwd_manager.hash_password(plain_password)

    assert isinstance(hashed, str)
    assert hashed != plain_password
    assert hashed.startswith("$2b$") or hashed.startswith(
        "$2a$"
    ), "bcrypt-хэши должны начинаться с $2b$ или $2a$"


def test_verify_password_success(plain_password: str):
    hashed = pwd_manager.hash_password(plain_password)
    assert pwd_manager.verify_password(plain_password, hashed) is True


def test_verify_password_fail(plain_password: str):
    hashed = pwd_manager.hash_password(plain_password)
    assert pwd_manager.verify_password("WrongPassword!", hashed) is False
