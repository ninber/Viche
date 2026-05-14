from fastapi.testclient import TestClient

from app.main import create_app


def test_openapi_contains_health_route() -> None:
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/v1/health" in paths
    assert "/v1/members/register" in paths
    assert "/v1/proposals" in paths
    assert "/v1/eligibility-pools" in paths
    assert "/v1/sortitions" in paths
    assert "/v1/public/proposals" in paths


def test_system_overview_exposes_plan_modules() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/system")

    assert response.status_code == 200
    payload = response.json()
    assert payload["canonical_language"] == "uk-UA"
    modules = {module["key"]: module for module in payload["modules"]}
    assert set(modules) >= {
        "membership",
        "journal",
        "proposals",
        "federation",
    }
    assert modules["membership"]["status"] == "pilot"
    assert modules["journal"]["status"] == "pilot"
    assert modules["proposals"]["status"] == "pilot"
    assert modules["sortition"]["status"] == "pilot"


def test_federation_node_metadata() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/federation/node")

    assert response.status_code == 200
    payload = response.json()
    assert payload["node_id"] == "LOCAL-VICHE"
    assert "viche-federation-0.1" in payload["protocol_versions"]
