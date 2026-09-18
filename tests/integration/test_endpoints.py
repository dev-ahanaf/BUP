"""Integration tests for API endpoints, error handling, and status codes."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_optimize_energy_missing_payload(client):
    response = client.post("/optimize-energy", json={})
    assert response.status_code == 422


def test_optimize_energy_invalid_hours(client):
    payload = {
        "scenario_id": "test_invalid",
        "operator_notes": ["Normal operations."],
        "hours": [{"hour": 0, "demand_kwh": 10, "solar_kwh": 0, "tariff_bdt_per_kwh": 5}],  # only 1 hour
        "battery": {
            "capacity_kwh": 100.0,
            "initial_energy_kwh": 20.0,
            "minimum_energy_kwh": 10.0,
            "max_charge_kwh_per_hour": 30.0,
            "max_discharge_kwh_per_hour": 40.0,
        },
    }
    response = client.post("/optimize-energy", json=payload)
    assert response.status_code == 422
