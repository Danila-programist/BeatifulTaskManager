import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestMain:
    async def test_invalid_endpoint_returns_404(self, client: AsyncClient):
        response = await client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    async def test_docs_available(self, client: AsyncClient):
        response = await client.get("/docs")
        assert response.status_code == 200

    async def test_openapi_available(self, client: AsyncClient):
        response = await client.get("/openapi.json")
        assert response.status_code == 200
