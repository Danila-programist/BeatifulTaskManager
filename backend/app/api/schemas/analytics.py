from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, model_validator


class UserInfo(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    first_name: str
    last_name: str


class TasksOverview(BaseModel):
    total_tasks: int = Field(default=0, ge=0)
    active_tasks: int = Field(default=0, ge=0)
    completed_tasks: int = Field(default=0, ge=0)
    completion_rate: Optional[int] = None

    @model_validator(mode="after")
    def calculate_completion_rate(self) -> "TasksOverview":
        if self.total_tasks > 0:
            self.completion_rate = round(
                (self.completed_tasks / self.total_tasks) * 100, 2
            )
        else:
            self.completion_rate = None
        return self


class ProductivityMetrics(BaseModel):
    tasks_created_today: int = Field(default=0, ge=0)
    tasks_completed_today: int = Field(default=0, ge=0)
    tasks_created_this_week: int = Field(default=0, ge=0)
    tasks_completed_this_week: int = Field(default=0, ge=0)


class RecentActivity(BaseModel):
    last_task_created: Optional[datetime] = None
    last_task_completed: Optional[datetime] = None
    most_active_day: Optional[str] = None


class TasksCreatedByWeekday(BaseModel):
    monday: int = Field(default=0, ge=0)
    tuesday: int = Field(default=0, ge=0)
    wednesday: int = Field(default=0, ge=0)
    thursday: int = Field(default=0, ge=0)
    friday: int = Field(default=0, ge=0)
    saturday: int = Field(default=0, ge=0)
    sunday: int = Field(default=0, ge=0)


class AnalyticsManager(BaseModel):
    user_info: UserInfo
    tasks_overview: TasksOverview
    productivity_metrics: ProductivityMetrics
    recent_activity: RecentActivity
    tasks_created_by_weekday: TasksCreatedByWeekday
