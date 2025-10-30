from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.schemas import (
    DatabaseUser,
    UserInfo,
    TasksOverview,
    ProductivityMetrics,
    RecentActivity,
    TasksCreatedByWeekday,
)
from app.models import User, Task


class AnalyticsService:
    def __init__(self, db: AsyncSession, user: DatabaseUser):
        self._session = db
        self._user = user

    async def get_user_info(self) -> UserInfo:
        stmt = select(User).where(User.username == self._user.username)
        res = await self._session.execute(stmt)
        user = res.scalar_one_or_none()

        if not user:
            raise ValueError(f"User {self._user.username} not found")

        return UserInfo(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    async def get_tasks_overview(self) -> TasksOverview: 
        stmt = select(
            func.count(Task.task_id).label('total_tasks'),
            func.count(Task.task_id).filter(Task.status == 'pending').label('active_tasks'),
            func.count(Task.task_id).filter(Task.status == 'completed').label('completed_tasks')
        ).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True
        )
        
        res = await self._session.execute(stmt)
        stats = res.one()
        
        return TasksOverview(
            total_tasks=stats.total_tasks or 0,
            active_tasks=stats.active_tasks or 0,
            completed_tasks=stats.completed_tasks or 0
        )

    async def get_productive_metrics(self) -> ProductivityMetrics:
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())  
        
        created_today_stmt = select(func.count(Task.task_id)).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True,
            func.date(Task.created_at) == today
        )
        tasks_created_today = (await self._session.execute(created_today_stmt)).scalar() or 0
        
        completed_today_stmt = select(func.count(Task.task_id)).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True,
            Task.status == 'completed',
            func.date(Task.updated_at) == today
        )
        tasks_completed_today = (await self._session.execute(completed_today_stmt)).scalar() or 0
        
        created_week_stmt = select(func.count(Task.task_id)).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True,
            Task.created_at >= start_of_week
        )
        tasks_created_this_week = (await self._session.execute(created_week_stmt)).scalar() or 0
        
        completed_week_stmt = select(func.count(Task.task_id)).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True,
            Task.status == 'completed',
            Task.updated_at >= start_of_week
        )
        tasks_completed_this_week = (await self._session.execute(completed_week_stmt)).scalar() or 0
        
        return ProductivityMetrics(
            tasks_created_today=tasks_created_today,
            tasks_completed_today=tasks_completed_today,
            tasks_created_this_week=tasks_created_this_week,
            tasks_completed_this_week=tasks_completed_this_week
        )

    async def get_recent_activity(self) -> RecentActivity:
        last_created_stmt = select(Task).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True
        ).order_by(Task.created_at.desc()).limit(1)
        
        last_created_task = (await self._session.execute(last_created_stmt)).scalar_one_or_none()
        
        last_completed_stmt = select(Task).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True,
            Task.status == 'completed'
        ).order_by(Task.updated_at.desc()).limit(1)
        
        last_completed_task = (await self._session.execute(last_completed_stmt)).scalar_one_or_none()

        most_active_day_stmt = select(
            func.to_char(Task.created_at, 'FMDay').label('weekday'),
            func.count(Task.task_id).label('count')
        ).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True
        ).group_by('weekday').order_by(func.count(Task.task_id).desc()).limit(1)
        
        most_active_day_result = (await self._session.execute(most_active_day_stmt)).first()
        
        return RecentActivity(
            last_task_created=last_created_task.created_at if last_created_task else None,
            last_task_completed=last_completed_task.updated_at if last_completed_task else None,
            most_active_day=most_active_day_result.weekday if most_active_day_result else None
        )

    async def get_tasks_created_by_weekday(self) -> TasksCreatedByWeekday:
        weekday_stmt = select(
            func.extract('dow', Task.created_at).label('weekday_num'),
            func.count(Task.task_id).label('count')
        ).where(
            Task.user_id == self._user.user_id,
            Task.is_active == True
        ).group_by('weekday_num')
        
        result = await self._session.execute(weekday_stmt)
        weekday_data = result.all()
        
        weekday_counts = {
            0: 0,  # Monday
            1: 0,  # Tuesday
            2: 0,  # Wednesday
            3: 0,  # Thursday
            4: 0,  # Friday
            5: 0,  # Saturday
            6: 0   # Sunday
        }
        
        for row in weekday_data:
            weekday_counts[int(row.weekday_num)] = row.count
        
        return TasksCreatedByWeekday(
            monday=weekday_counts[0],
            tuesday=weekday_counts[1],
            wednesday=weekday_counts[2],
            thursday=weekday_counts[3],
            friday=weekday_counts[4],
            saturday=weekday_counts[5],
            sunday=weekday_counts[6]
        )
