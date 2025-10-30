# pylint: disable=singleton-comparison
from typing import List, Optional
from uuid import UUID


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Task, User
from app.api.schemas import TaskRequest


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

    async def create_task(self, task_data: TaskRequest) -> Optional[Task]:
        user_id = await self._get_user_id()

        if not user_id:
            return None

        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=user_id,
        )

        self._session.add(new_task)
        await self._session.commit()
        await self._session.refresh(new_task)
        return new_task

    async def get_user_task_by_id(self, task_id: int) -> Optional[Task]:
        user_id = await self._get_user_id()
        if not user_id:
            return None

        stmt = select(Task).where(
            and_(
                Task.task_id == task_id,
                Task.user_id == user_id,
                Task.is_active == True,
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_task(self, task_id: int, task_data: TaskRequest) -> Optional[Task]:
        user_id = await self._get_user_id()
        if not user_id:
            return None

        task = await self.get_user_task_by_id(task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def delete_task(self, task_id: int) -> bool:
        user_id = await self._get_user_id()
        if not user_id:
            return False

        task = await self.get_user_task_by_id(task_id)
        if not task:
            return False

        task.is_active = False
        await self._session.commit()
        return True
