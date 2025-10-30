import pytest

from pydantic import ValidationError
from datetime import datetime

from app.api.schemas import (
    UserInfo,
    TasksOverview,
    ProductivityMetrics,
    RecentActivity,
    TasksCreatedByWeekday,
    AnalyticsManager
)


class TestUserInfo:
    
    def test_valid_user_info(self):
        user_info = UserInfo(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        assert user_info.username == "johndoe"
        assert user_info.email == "john@example.com"
        assert user_info.first_name == "John"
        assert user_info.last_name == "Doe"

    def test_username_too_short(self):
        with pytest.raises(ValidationError):
            UserInfo(
                username="jo",
                email="john@example.com",
                first_name="John",
                last_name="Doe"
            )

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserInfo(
                username="a" * 33, 
                email="john@example.com",
                first_name="John",
                last_name="Doe"
            )

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserInfo(
                username="johndoe",
                email="invalid-email",
                first_name="John",
                last_name="Doe"
            )

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            UserInfo(
                username="johndoe"
            )


class TestTasksOverview:
    
    def test_valid_tasks_overview(self):
        overview = TasksOverview(
            total_tasks=10,
            active_tasks=3,
            completed_tasks=7
        )
        assert overview.total_tasks == 10
        assert overview.active_tasks == 3
        assert overview.completed_tasks == 7
        assert overview.completion_rate == 70.0

    def test_completion_rate_calculation(self):
        overview = TasksOverview(
            total_tasks=5,
            active_tasks=2,
            completed_tasks=3
        )
        assert overview.completion_rate == 60.0

    def test_completion_rate_zero_total_tasks(self):
        overview = TasksOverview(
            total_tasks=0,
            active_tasks=0,
            completed_tasks=0
        )
        assert overview.completion_rate is None

    def test_completion_rate_rounding(self):
        overview = TasksOverview(
            total_tasks=3,
            active_tasks=1,
            completed_tasks=2
        )
        assert overview.completion_rate == 66.67

    def test_default_values(self):
        overview = TasksOverview()
        assert overview.total_tasks == 0
        assert overview.active_tasks == 0
        assert overview.completed_tasks == 0
        assert overview.completion_rate is None

    def test_negative_values(self):
        with pytest.raises(ValidationError):
            TasksOverview(
                total_tasks=-1,
                active_tasks=0,
                completed_tasks=0
            )


class TestProductivityMetrics:

    
    def test_valid_productivity_metrics(self):
        metrics = ProductivityMetrics(
            tasks_created_today=5,
            tasks_completed_today=3,
            tasks_created_this_week=15,
            tasks_completed_this_week=10
        )
        assert metrics.tasks_created_today == 5
        assert metrics.tasks_completed_today == 3
        assert metrics.tasks_created_this_week == 15
        assert metrics.tasks_completed_this_week == 10

    def test_default_values(self):
        metrics = ProductivityMetrics()
        assert metrics.tasks_created_today == 0
        assert metrics.tasks_completed_today == 0
        assert metrics.tasks_created_this_week == 0
        assert metrics.tasks_completed_this_week == 0

    def test_negative_values(self):
        with pytest.raises(ValidationError):
            ProductivityMetrics(
                tasks_created_today=-1,
                tasks_completed_today=0,
                tasks_created_this_week=0,
                tasks_completed_this_week=0
            )


class TestRecentActivity:

    
    def test_valid_recent_activity(self):
        last_created = datetime.now()
        last_completed = datetime.now()
        
        activity = RecentActivity(
            last_task_created=last_created,
            last_task_completed=last_completed,
            most_active_day="Monday"
        )
        assert activity.last_task_created == last_created
        assert activity.last_task_completed == last_completed
        assert activity.most_active_day == "Monday"

    def test_none_values(self):
        activity = RecentActivity()
        assert activity.last_task_created is None
        assert activity.last_task_completed is None
        assert activity.most_active_day is None

    def test_invalid_datetime(self):
        with pytest.raises(ValidationError):
            RecentActivity(
                last_task_created="invalid-datetime",
                last_task_completed=None,
                most_active_day="Monday"
            )


class TestTasksCreatedByWeekday:
    
    def test_valid_weekday_data(self):
        weekday_data = TasksCreatedByWeekday(
            monday=5,
            tuesday=3,
            wednesday=7,
            thursday=2,
            friday=4,
            saturday=1,
            sunday=0
        )
        assert weekday_data.monday == 5
        assert weekday_data.tuesday == 3
        assert weekday_data.wednesday == 7
        assert weekday_data.thursday == 2
        assert weekday_data.friday == 4
        assert weekday_data.saturday == 1
        assert weekday_data.sunday == 0

    def test_default_values(self):
        weekday_data = TasksCreatedByWeekday()
        assert weekday_data.monday == 0
        assert weekday_data.tuesday == 0
        assert weekday_data.wednesday == 0
        assert weekday_data.thursday == 0
        assert weekday_data.friday == 0
        assert weekday_data.saturday == 0
        assert weekday_data.sunday == 0

    def test_negative_values(self):
        with pytest.raises(ValidationError):
            TasksCreatedByWeekday(monday=-1)


class TestAnalyticsManager:
    
    def test_valid_analytics_manager(self):
        user_info = UserInfo(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        
        tasks_overview = TasksOverview(
            total_tasks=10,
            active_tasks=3,
            completed_tasks=7
        )
        
        productivity_metrics = ProductivityMetrics(
            tasks_created_today=2,
            tasks_completed_today=1,
            tasks_created_this_week=8,
            tasks_completed_this_week=5
        )
        
        recent_activity = RecentActivity(
            last_task_created=datetime.now(),
            last_task_completed=datetime.now(),
            most_active_day="Wednesday"
        )
        
        tasks_by_weekday = TasksCreatedByWeekday(
            monday=2,
            tuesday=3,
            wednesday=4,
            thursday=1,
            friday=2,
            saturday=0,
            sunday=0
        )
        
        analytics = AnalyticsManager(
            user_info=user_info,
            tasks_overview=tasks_overview,
            productivity_metrics=productivity_metrics,
            recent_activity=recent_activity,
            tasks_created_by_weekday=tasks_by_weekday
        )
        
        assert analytics.user_info == user_info
        assert analytics.tasks_overview == tasks_overview
        assert analytics.productivity_metrics == productivity_metrics
        assert analytics.recent_activity == recent_activity
        assert analytics.tasks_created_by_weekday == tasks_by_weekday

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            AnalyticsManager(
                user_info=UserInfo(
                    username="johndoe",
                    email="john@example.com",
                    first_name="John",
                    last_name="Doe"
                )
            )

    def test_invalid_nested_objects(self):
        with pytest.raises(ValidationError):
            AnalyticsManager(
                user_info=UserInfo(
                    username="jo",  
                    email="john@example.com",
                    first_name="John",
                    last_name="Doe"
                ),
                tasks_overview=TasksOverview(),
                productivity_metrics=ProductivityMetrics(),
                recent_activity=RecentActivity(),
                tasks_created_by_weekday=TasksCreatedByWeekday()
            )