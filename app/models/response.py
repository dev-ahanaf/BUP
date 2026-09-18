"""Response models for the GridWise Energy Optimization API."""
from typing import List, Literal
from pydantic import BaseModel, Field
from app.models.directive import DirectiveInterpretationEntry


class HealthResponse(BaseModel):
    """Health check response."""
    status: Literal["ok"] = "ok"


class HourlyPlanEntry(BaseModel):
    """Hourly decision and energy state in the final schedule."""
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    grid_kwh: float = Field(..., ge=0.0, description="Electricity imported from the grid in kWh")
    solar_used_kwh: float = Field(..., ge=0.0, description="Solar energy used directly for demand or charging in kWh")
    battery_action: Literal["charge", "discharge", "idle"] = Field(
        ..., description="Battery action executed during this hour"
    )
    battery_kwh: float = Field(
        ..., ge=0.0, description="Energy transferred into (charge) or out of (discharge) battery in kWh"
    )
    battery_energy_after_kwh: float = Field(
        ..., ge=0.0, description="Remaining battery energy at the end of this hour in kWh"
    )


class OptimizationResponse(BaseModel):
    """Root optimization response payload matching canonical specification Section 10.2."""
    scenario_id: str = Field(..., description="Scenario identifier matching the request")
    directive_interpretation: List[DirectiveInterpretationEntry] = Field(
        ..., description="Interpreted operator directives in matching note_index order"
    )
    hourly_plan: List[HourlyPlanEntry] = Field(
        ..., min_length=24, max_length=24, description="Optimal 24-hour dispatch schedule"
    )
    total_grid_kwh: float = Field(..., ge=0.0, description="Sum of hourly grid imports in kWh")
    total_cost_bdt: float = Field(..., ge=0.0, description="Total electricity cost across all 24 hours in BDT")
    peak_grid_kwh: float = Field(..., ge=0.0, description="Maximum single-hour grid import in kWh")
    plan_summary: str = Field(..., description="Structured summary explaining the optimization strategy and cost impact")
