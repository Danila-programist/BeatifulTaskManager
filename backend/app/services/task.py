from typing import List
from uuid import UUID


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, _and

from app.models import Task


class TaskService:
    def __init__(self, db: AsyncSession, user_id: UUID) -> List[Task]:
        self._session = db
        self._user_id = user_id

    async def get_user_tasks(self):
        stmt = (
            select(Task)
            .where(_and(Task.user_id == self._user_id, Task.is_active == True))
            .order_by(Task.created_at.desc())
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()
