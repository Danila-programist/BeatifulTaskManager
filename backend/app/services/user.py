from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas import DatabaseUser, RegisterUser
from app.models import User
from app.utils import pwd_manager

class UserService:
    def __init__(self, db: AsyncSession):
        self._session = db
        self._pwd_manager = pwd_manager

    async def get_user(self, username: str) -> Optional[DatabaseUser]:
        stmt = select(User).where(User.username == username)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def add_new_user(self, user: RegisterUser) -> None:
        new_user: User = User(
            username=user.username,
            email=user.email,
            password_hash=self._pwd_manager.hash_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
        ) 

        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)





