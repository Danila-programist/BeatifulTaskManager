from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class BaseTask(BaseModel):
    title: str = Field(..., max_length=256)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


class TaskRequest(BaseTask):
    pass


class TaskResponse(BaseTask):
    task_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    user_id: UUID
