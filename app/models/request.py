"""Request models for the GridWise Energy Optimization API."""
from typing import List
from pydantic import BaseModel, Field, field_validator


class HourData(BaseModel):
    """Hourly forecast and tariff data."""
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    demand_kwh: float = Field(..., ge=0.0, description="Campus electricity demand in kWh")
    solar_kwh: float = Field(..., ge=0.0, description="Available solar generation forecast in kWh")
    tariff_bdt_per_kwh: float = Field(..., ge=0.0, description="Grid electricity price in BDT/kWh")


class BatterySpec(BaseModel):
    """Campus battery storage specifications."""
    capacity_kwh: float = Field(..., gt=0.0, description="Total battery storage capacity in kWh")
    initial_energy_kwh: float = Field(..., ge=0.0, description="Battery energy state at start of day in kWh")
    minimum_energy_kwh: float = Field(..., ge=0.0, description="Baseline minimum battery reserve level in kWh")
    max_charge_kwh_per_hour: float = Field(..., ge=0.0, description="Maximum charge rate in kWh/hour")
    max_discharge_kwh_per_hour: float = Field(..., ge=0.0, description="Maximum discharge rate in kWh/hour")

    @field_validator("initial_energy_kwh")
    @classmethod
    def validate_initial_energy(cls, v: float, info) -> float:
        # Note: cross-field check with capacity_kwh is also validated at model level
        return v

    def model_post_init(self, __context) -> None:
        if self.initial_energy_kwh > self.capacity_kwh + 1e-6:
            raise ValueError(f"initial_energy_kwh ({self.initial_energy_kwh}) cannot exceed capacity_kwh ({self.capacity_kwh})")
        if self.minimum_energy_kwh > self.capacity_kwh + 1e-6:
            raise ValueError(f"minimum_energy_kwh ({self.minimum_energy_kwh}) cannot exceed capacity_kwh ({self.capacity_kwh})")


class OptimizationRequest(BaseModel):
    """Root optimization request payload matching canonical specification Section 10.1."""
    scenario_id: str = Field(..., min_length=1, description="Unique identifier for the optimization scenario")
    operator_notes: List[str] = Field(..., min_length=1, max_length=3, description="1 to 3 natural language operator directives")
    hours: List[HourData] = Field(..., min_length=24, max_length=24, description="Hourly forecast data for all 24 hours")
    battery: BatterySpec = Field(..., description="Battery system specifications")

    @field_validator("hours")
    @classmethod
    def validate_hours_sequence(cls, v: List[HourData]) -> List[HourData]:
        if len(v) != 24:
            raise ValueError(f"Expected exactly 24 hourly entries, got {len(v)}")
        hours_seen = [item.hour for item in v]
        if hours_seen != list(range(24)):
            raise ValueError("hours array must contain hours 0 through 23 in exact ascending order")
        return v
