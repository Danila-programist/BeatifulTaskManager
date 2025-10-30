import pytest
from httpx import AsyncClient

from app.api.schemas.analytics import (
    UserInfo,
    TasksOverview,
    ProductivityMetrics,
    RecentActivity,
    TasksCreatedByWeekday,
    AnalyticsManager
)


class TestAnalyticsEndpoint:

    @pytest.mark.asyncio
    async def test_analytics_endpoint_success(
        self, authenticated_client: AsyncClient
    ):
        response = await authenticated_client.get("/api/v1/analytics")
        
        assert response.status_code == 200
        
        data = response.json()
        
        assert "user_info" in data
        assert "tasks_overview" in data
        assert "productivity_metrics" in data
        assert "recent_activity" in data
        assert "tasks_created_by_weekday" in data

        user_info = data["user_info"]
        assert "username" in user_info
        assert "email" in user_info
        assert "first_name" in user_info
        assert "last_name" in user_info
        
        tasks_overview = data["tasks_overview"]
        assert "total_tasks" in tasks_overview
        assert "active_tasks" in tasks_overview
        assert "completed_tasks" in tasks_overview
        assert "completion_rate" in tasks_overview
        
        productivity_metrics = data["productivity_metrics"]
        assert "tasks_created_today" in productivity_metrics
        assert "tasks_completed_today" in productivity_metrics
        assert "tasks_created_this_week" in productivity_metrics
        assert "tasks_completed_this_week" in productivity_metrics
        
        recent_activity = data["recent_activity"]
        assert "last_task_created" in recent_activity
        assert "last_task_completed" in recent_activity
        assert "most_active_day" in recent_activity
        

        tasks_by_weekday = data["tasks_created_by_weekday"]
        assert "monday" in tasks_by_weekday
        assert "tuesday" in tasks_by_weekday
        assert "wednesday" in tasks_by_weekday
        assert "thursday" in tasks_by_weekday
        assert "friday" in tasks_by_weekday
        assert "saturday" in tasks_by_weekday
        assert "sunday" in tasks_by_weekday

    @pytest.mark.asyncio
    async def test_analytics_endpoint_unauthorized(
        self, client: AsyncClient
    ):
        response = await client.get("/api/v1/analytics")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_analytics_endpoint_with_tasks_data(
        self, authenticated_client: AsyncClient
    ):
        tasks_data = [
            {
                "title": "Completed Task",
                "description": "A completed task",
                "status": "completed",
            },
            {
                "title": "In Progress Task", 
                "description": "A task in progress",
                "status": "in_progress",
            },
            {
                "title": "Pending Task",
                "description": "A pending task", 
                "status": "pending",
            },
        ]
        
        for task_data in tasks_data:
            await authenticated_client.post("/api/v1/tasks", json=task_data)

        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()

        assert data["tasks_overview"]["total_tasks"] == 3
        assert data["tasks_overview"]["active_tasks"] >= 1  
        assert data["tasks_overview"]["completed_tasks"] >= 1 
        
        completion_rate = data["tasks_overview"]["completion_rate"]
        assert completion_rate is None or 0 <= completion_rate <= 100
        
        assert data["recent_activity"]["last_task_created"] is not None

    @pytest.mark.asyncio
    async def test_analytics_endpoint_empty_data(
        self, authenticated_client: AsyncClient
    ):
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["tasks_overview"]["total_tasks"] == 0
        assert data["tasks_overview"]["active_tasks"] == 0
        assert data["tasks_overview"]["completed_tasks"] == 0
        assert data["tasks_overview"]["completion_rate"] is None
        
        assert data["productivity_metrics"]["tasks_created_today"] == 0
        assert data["productivity_metrics"]["tasks_completed_today"] == 0
        assert data["productivity_metrics"]["tasks_created_this_week"] == 0
        assert data["productivity_metrics"]["tasks_completed_this_week"] == 0
        
        assert data["tasks_created_by_weekday"]["monday"] == 0
        assert data["tasks_created_by_weekday"]["tuesday"] == 0
        assert data["tasks_created_by_weekday"]["wednesday"] == 0
        assert data["tasks_created_by_weekday"]["thursday"] == 0
        assert data["tasks_created_by_weekday"]["friday"] == 0
        assert data["tasks_created_by_weekday"]["saturday"] == 0
        assert data["tasks_created_by_weekday"]["sunday"] == 0

    @pytest.mark.asyncio
    async def test_analytics_endpoint_user_info_correct(
        self, authenticated_client: AsyncClient
    ):
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        user_info = data["user_info"]
        
        assert user_info["username"] == "testuser"
        assert user_info["email"] == "testuser@example.com"
        assert user_info["first_name"] == "Test"
        assert user_info["last_name"] == "User"

    @pytest.mark.asyncio
    async def test_analytics_endpoint_completion_rate_calculation(
        self, authenticated_client: AsyncClient
    ):
        completed_tasks = [
            {"title": f"Completed {i}", "status": "completed"}
            for i in range(3)
        ]
        active_tasks = [
            {"title": f"Active {i}", "status": "in_progress"}
            for i in range(2)
        ]
        
        for task_data in completed_tasks + active_tasks:
            await authenticated_client.post("/api/v1/tasks", json=task_data)
        
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        overview = data["tasks_overview"]
        
        assert overview["total_tasks"] == 5
        assert overview["completed_tasks"] == 3
        assert overview["completion_rate"] == 60.0

    @pytest.mark.asyncio
    async def test_analytics_endpoint_weekday_distribution(
        self, authenticated_client: AsyncClient
    ):
        for i in range(5):
            await authenticated_client.post("/api/v1/tasks", json={
                "title": f"Task {i}",
                "status": "pending"
            })
        
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        weekday_data = data["tasks_created_by_weekday"]
        
        total_weekday_tasks = (
            weekday_data["monday"] +
            weekday_data["tuesday"] +
            weekday_data["wednesday"] +
            weekday_data["thursday"] +
            weekday_data["friday"] +
            weekday_data["saturday"] +
            weekday_data["sunday"]
        )
        
        assert total_weekday_tasks == data["tasks_overview"]["total_tasks"]

    @pytest.mark.asyncio
    async def test_analytics_endpoint_recent_activity_populated(
        self, authenticated_client: AsyncClient
    ):

        await authenticated_client.post("/api/v1/tasks", json={
            "title": "Test Task",
            "status": "completed"
        })
        
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        recent_activity = data["recent_activity"]
        

        assert recent_activity["last_task_created"] is not None
        
        assert recent_activity["last_task_completed"] is not None
        
        assert recent_activity["most_active_day"] is not None

    @pytest.mark.asyncio
    async def test_analytics_endpoint_productivity_metrics(
        self, authenticated_client: AsyncClient
    ):
        for i in range(2):
            await authenticated_client.post("/api/v1/tasks", json={
                "title": f"Today Task {i}",
                "status": "completed" if i == 0 else "pending"
            })
        
        response = await authenticated_client.get("/api/v1/analytics")
        assert response.status_code == 200
        
        data = response.json()
        metrics = data["productivity_metrics"]
        
        assert metrics["tasks_created_today"] >= 0
        assert metrics["tasks_completed_today"] >= 0
        assert metrics["tasks_created_this_week"] >= 0
        assert metrics["tasks_completed_this_week"] >= 0
        
        assert metrics["tasks_created_today"] <= metrics["tasks_created_this_week"]
        assert metrics["tasks_completed_today"] <= metrics["tasks_completed_this_week"]