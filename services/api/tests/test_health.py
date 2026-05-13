from fastapi.testclient import TestClient

from app.main import create_app


def test_openapi_contains_health_route() -> None:
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/v1/health" in response.json()["paths"]

