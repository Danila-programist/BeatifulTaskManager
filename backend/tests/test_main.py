class TestMain:
    def test_invalid_endpoint_returns_404(self, client):
        """Тест что несуществующий эндпоинт возвращает 404"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_docs_available(self, client):
        """Тест что Swagger документация доступна"""
        response = client.get("/docs")
        assert response.status_code == 200
