import uuid

import pytest
from pydantic import ValidationError

from app.api.schemas import BaseUser, RegisterUser, LoginUser, DatabaseUser


def test_baseuser_valid_username():
    user = BaseUser(username="validusername")
    assert user.username == "validusername"


def test_baseuser_too_short_username():
    with pytest.raises(ValidationError):
        BaseUser(username="sh")  


def test_registeruser_valid_data():
    user = RegisterUser(
        username="validuser",
        email="test@example.com",
        password="StrongPass123",
        first_name="John",
        last_name="Doe",
    )
    assert user.username == "validuser"
    assert user.email == "test@example.com"
    assert user.password == "StrongPass123"


def test_registeruser_invalid_email():
    with pytest.raises(ValidationError):
        RegisterUser(
            username="validuser",
            email="invalid-email",
            password="StrongPass123",
            first_name="John",
            last_name="Doe",
        )


def test_registeruser_short_password():
    with pytest.raises(ValidationError):
        RegisterUser(
            username="validuser",
            email="test@example.com",
            password="short",
            first_name="John",
            last_name="Doe",
        )


def test_registeruser_short_username():
    with pytest.raises(ValidationError):
        RegisterUser(
            username="sh",  
            email="test@example.com",
            password="StrongPass123",
            first_name="John",
            last_name="Doe",
        )


def test_loginuser_valid_data():
    user = LoginUser(username="validuser", password="StrongPass123")
    assert user.username == "validuser"
    assert user.password == "StrongPass123"


def test_databaseuser_valid_data():
    user_id = uuid.uuid4()
    user = DatabaseUser(
        user_id=user_id,
        username="validuser",
        email="test@example.com",
        password_hash="hashedpassword",
        first_name="John",
        last_name="Doe",
        is_active=True,
        created_at="2025-01-01T12:00:00Z"
    )
    assert user.user_id == user_id
    assert user.is_active is True
    assert user.username == "validuser"


def test_databaseuser_invalid_uuid():
    with pytest.raises(ValidationError):
        DatabaseUser(
            user_id="not-a-uuid",
            username="validuser",
            email="test@example.com",
            password_hash="hashedpassword",
            first_name="John",
            last_name="Doe",
            is_active=True,
            created_at="2025-01-01T12:00:00Z"
        )
