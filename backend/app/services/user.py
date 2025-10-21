from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.schemas import DatabaseUser, RegisterUser
from app.models import User

class UserModel:
    def __init__(self, db: AsyncSession):
        self._session = db

    async def get_user(self, username: str) -> Optional[DatabaseUser]:
        stmt = select(User).where(User.username == username)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def add_new_user(self, user: RegisterUser) -> None:
        ...





