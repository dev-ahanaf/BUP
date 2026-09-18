"""Unit tests for request and response Pydantic schema validation."""
import pytest
from pydantic import ValidationError
from app.models.request import BatterySpec, HourData, OptimizationRequest
from app.models.response import HealthResponse, OptimizationResponse


def test_battery_spec_validation():
    # Valid battery
    b = BatterySpec(
        capacity_kwh=100.0,
        initial_energy_kwh=20.0,
        minimum_energy_kwh=10.0,
        max_charge_kwh_per_hour=30.0,
        max_discharge_kwh_per_hour=40.0,
    )
    assert b.capacity_kwh == 100.0

    # Initial energy exceeds capacity
    with pytest.raises(ValidationError):
        BatterySpec(
            capacity_kwh=50.0,
            initial_energy_kwh=60.0,
            minimum_energy_kwh=10.0,
            max_charge_kwh_per_hour=30.0,
            max_discharge_kwh_per_hour=40.0,
        )


def test_optimization_request_hour_count():
    # Only 23 hours instead of 24
    hours = [HourData(hour=i, demand_kwh=50, solar_kwh=10, tariff_bdt_per_kwh=5) for i in range(23)]
    battery = BatterySpec(
        capacity_kwh=100.0,
        initial_energy_kwh=20.0,
        minimum_energy_kwh=10.0,
        max_charge_kwh_per_hour=30.0,
        max_discharge_kwh_per_hour=40.0,
    )

    with pytest.raises(ValidationError):
        OptimizationRequest(
            scenario_id="invalid_hours",
            operator_notes=["Normal operation."],
            hours=hours,
            battery=battery,
        )


def test_health_response():
    h = HealthResponse()
    assert h.status == "ok"
    assert h.model_dump() == {"status": "ok"}
