"""Integration test verifying interpretation and dispatch resilience against paraphrased notes."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_paraphrased_notes(client):
    # Construct a valid 24-hour test request
    hours = []
    for h in range(24):
        hours.append({
            "hour": h,
            "demand_kwh": 60.0 if 18 <= h <= 21 else 30.0,
            "solar_kwh": 40.0 if 10 <= h <= 15 else 0.0,
            "tariff_bdt_per_kwh": 14.0 if 18 <= h <= 21 else 6.0,
        })

    battery = {
        "capacity_kwh": 100.0,
        "initial_energy_kwh": 30.0,
        "minimum_energy_kwh": 15.0,
        "max_charge_kwh_per_hour": 25.0,
        "max_discharge_kwh_per_hour": 35.0,
    }

    # Paraphrased notes:
    # 1. Solar drop by 40% from 11 AM to 2 PM
    # 2. Prevent charging from 6 PM until 9 PM
    # 3. Informational advisory
    req_payload = {
        "scenario_id": "paraphrase_test_1",
        "operator_notes": [
            "Heavy cloud cover anticipated between 11 AM and 2 PM; solar output will decrease by 40%.",
            "Peak evening grid congestion expected: please prohibit battery charging from 6 PM until 9 PM.",
            "Weather service confirms ambient temperatures will remain stable throughout the day.",
        ],
        "hours": hours,
        "battery": battery,
    }

    response = client.post("/optimize-energy", json=req_payload)
    assert response.status_code == 200
    data = response.json()

    directives = data["directive_interpretation"]
    assert len(directives) == 3

    # Check Note 0: solar reduction
    assert directives[0]["applies"] is True
    assert directives[0]["directive_type"] == "solar_reduction"
    assert directives[0]["structured_adjustment"]["hours"] == [11, 12, 13]
    assert abs(directives[0]["structured_adjustment"]["factor"] - 0.60) < 1e-3

    # Check Note 1: no charge window
    assert directives[1]["applies"] is True
    assert directives[1]["directive_type"] == "no_charge_window"
    assert directives[1]["structured_adjustment"]["hours"] == [18, 19, 20]

    # Check Note 2: no-op
    assert directives[2]["applies"] is False
    assert directives[2]["directive_type"] == "no_op"
    assert directives[2]["structured_adjustment"] is None

    # Check that plan has 24 hours
    assert len(data["hourly_plan"]) == 24
    # Check that no charging occurred at hours 18, 19, 20
    for h_entry in data["hourly_plan"]:
        if h_entry["hour"] in [18, 19, 20]:
            assert h_entry["battery_action"] != "charge"
