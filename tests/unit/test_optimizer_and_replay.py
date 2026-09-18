"""Unit tests for OR-Tools optimizer and replay validator."""
import pytest
from app.directives.engine import ConstrainedScenario, DirectiveEngine
from app.models.directive import (
    DirectiveInterpretationEntry,
    DirectiveType,
    MinimumBatteryReserveAdjustment,
    NoChargeWindowAdjustment,
    NoDischargeWindowAdjustment,
    SolarReductionAdjustment,
)
from app.models.request import BatterySpec, HourData
from app.optimizer.solver import EnergyOptimizer
from app.validation.replay import ReplayValidator


@pytest.fixture
def base_scenario():
    # 24 hours with variable tariffs and solar
    hours = []
    for h in range(24):
        solar = 50.0 if 10 <= h <= 15 else 0.0
        demand = 80.0 if 17 <= h <= 21 else 40.0
        tariff = 15.0 if 17 <= h <= 21 else 5.0
        hours.append(HourData(hour=h, demand_kwh=demand, solar_kwh=solar, tariff_bdt_per_kwh=tariff))

    battery = BatterySpec(
        capacity_kwh=100.0,
        initial_energy_kwh=20.0,
        minimum_energy_kwh=10.0,
        max_charge_kwh_per_hour=30.0,
        max_discharge_kwh_per_hour=40.0,
    )
    return hours, battery


def test_optimizer_baseline_solve(base_scenario):
    hours, battery = base_scenario
    directives = []
    scenario = DirectiveEngine.apply_directives("test_base", hours, battery, directives)

    optimizer = EnergyOptimizer()
    hourly_plan, total_grid, total_cost, peak_grid = optimizer.solve(scenario)

    assert len(hourly_plan) == 24
    assert total_cost > 0.0
    assert total_grid > 0.0

    # Replay validate
    val_res = ReplayValidator.validate_plan(scenario, hourly_plan, total_grid, total_cost, peak_grid)
    assert val_res.is_valid is True
    assert len(val_res.errors) == 0


def test_optimizer_solar_reduction(base_scenario):
    hours, battery = base_scenario
    # Reduce solar at hours 12, 13 to 0.0
    directives = [
        DirectiveInterpretationEntry(
            note_index=0,
            applies=True,
            directive_type=DirectiveType.SOLAR_REDUCTION,
            structured_adjustment=SolarReductionAdjustment(hours=[12, 13], factor=0.0),
            explanation="Solar offline hours 12, 13",
        )
    ]
    scenario = DirectiveEngine.apply_directives("test_solar_red", hours, battery, directives)
    assert scenario.solar_usable[12] == 0.0
    assert scenario.solar_usable[13] == 0.0

    optimizer = EnergyOptimizer()
    hourly_plan, total_grid, total_cost, peak_grid = optimizer.solve(scenario)

    val_res = ReplayValidator.validate_plan(scenario, hourly_plan, total_grid, total_cost, peak_grid)
    assert val_res.is_valid is True


def test_replay_validator_detects_energy_balance_error(base_scenario):
    hours, battery = base_scenario
    scenario = DirectiveEngine.apply_directives("test_err", hours, battery, [])

    optimizer = EnergyOptimizer()
    hourly_plan, total_grid, total_cost, peak_grid = optimizer.solve(scenario)

    # Intentionally corrupt hour 0 grid value
    corrupted_plan = [p.model_copy() for p in hourly_plan]
    corrupted_plan[0].grid_kwh += 10.0

    val_res = ReplayValidator.validate_plan(scenario, corrupted_plan, total_grid, total_cost, peak_grid)
    assert val_res.is_valid is False
    assert any("Energy balance violation" in err for err in val_res.errors)
