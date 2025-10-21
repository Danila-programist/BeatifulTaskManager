import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)


class RegisterUser(BaseUser):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    #is_active: bool = True
    #created_at: datetime = datetime.now()


class LoginUser(BaseUser):
    password: str


class DatabaseUser(BaseUser):
    user_id: uuid.UUID
    email: EmailStr
    password_hash: str 
    first_name: str
    last_name: str
    is_active: bool 
    created_at: datetime 