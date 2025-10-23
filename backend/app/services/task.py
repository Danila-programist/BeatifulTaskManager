from typing import List, Optional
from uuid import UUID


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Task, User


class TaskService:
    def __init__(self, db: AsyncSession, username: str):
        self._session = db
        self._username = username

    async def _get_user_id(self) -> Optional[UUID]:
        stmt = select(User.user_id).where(User.username == self._username)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_tasks(self) -> List[Task]:

        user_id = await self._get_user_id()
        if not user_id:
            return []

        stmt = (
            select(Task)
            .where(and_(Task.user_id == user_id, Task.is_active == True))
            .order_by(Task.created_at.desc())
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()
