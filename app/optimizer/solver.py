"""Mathematical optimization solver for 24-hour microgrid dispatch using OR-Tools."""
from typing import List, Tuple
from ortools.linear_solver import pywraplp

from app.config import settings
from app.directives.engine import ConstrainedScenario
from app.models.response import HourlyPlanEntry
from app.utils.logging import logger


class EnergyOptimizer:
    """Solves the 24-hour campus energy dispatch MILP problem using OR-Tools."""

    def __init__(self, solver_name: str = None, time_limit_seconds: float = None) -> None:
        self.solver_name = solver_name or settings.OPTIMIZER_SOLVER
        self.time_limit = time_limit_seconds or settings.OPTIMIZER_TIME_LIMIT_SECONDS

    def solve(self, scenario: ConstrainedScenario) -> Tuple[List[HourlyPlanEntry], float, float, float]:
        """Formulate and solve the 24-hour energy dispatch MILP.

        Returns:
            (hourly_plan, total_grid_kwh, total_cost_bdt, peak_grid_kwh)
        """
        # Create solver instance
        solver = pywraplp.Solver.CreateSolver(self.solver_name)
        if not solver:
            logger.warning(f"Solver '{self.solver_name}' unavailable, falling back to CBC")
            solver = pywraplp.Solver.CreateSolver("CBC")
            if not solver:
                raise RuntimeError("Failed to initialize OR-Tools linear solver (CBC).")

        solver.SetTimeLimit(int(self.time_limit * 1000))
        infinity = solver.infinity()

        battery = scenario.battery
        demand = scenario.demand
        solar_usable = scenario.solar_usable
        tariff = scenario.tariff
        min_reserve = scenario.min_battery_reserve
        charge_allowed = scenario.charge_allowed
        discharge_allowed = scenario.discharge_allowed
        max_grid = scenario.max_grid_import

        # 1. Variables
        grid = [solver.NumVar(0.0, max_grid[h] if max_grid[h] < 1e9 else infinity, f"grid_{h}") for h in range(24)]
        solar_used = [solver.NumVar(0.0, solar_usable[h], f"solar_used_{h}") for h in range(24)]
        charge = [solver.NumVar(0.0, battery.max_charge_kwh_per_hour if charge_allowed[h] else 0.0, f"charge_{h}") for h in range(24)]
        discharge = [solver.NumVar(0.0, battery.max_discharge_kwh_per_hour if discharge_allowed[h] else 0.0, f"discharge_{h}") for h in range(24)]
        energy_after = [solver.NumVar(min_reserve[h], battery.capacity_kwh, f"energy_after_{h}") for h in range(24)]

        # Binary mutual exclusion variables: is_charge and is_discharge
        is_charge = [solver.BoolVar(f"is_charge_{h}") for h in range(24)]
        is_discharge = [solver.BoolVar(f"is_discharge_{h}") for h in range(24)]

        # Peak grid tracking variable
        peak_grid = solver.NumVar(0.0, infinity, "peak_grid")

        # 2. Constraints
        for h in range(24):
            # Energy balance: grid[h] + solar_used[h] + discharge[h] == demand[h] + charge[h]
            solver.Add(grid[h] + solar_used[h] + discharge[h] - charge[h] == demand[h])

            # Binary indicator bounds for mutual exclusion
            solver.Add(charge[h] <= battery.max_charge_kwh_per_hour * is_charge[h])
            solver.Add(discharge[h] <= battery.max_discharge_kwh_per_hour * is_discharge[h])
            solver.Add(is_charge[h] + is_discharge[h] <= 1)

            # Battery energy state transitions
            if h == 0:
                solver.Add(energy_after[0] == battery.initial_energy_kwh + charge[0] - discharge[0])
            else:
                solver.Add(energy_after[h] == energy_after[h - 1] + charge[h] - discharge[h])

            # Peak tracking
            solver.Add(peak_grid >= grid[h])

        # End of day neutrality: E[23] == initial_energy_kwh
        solver.Add(energy_after[23] == battery.initial_energy_kwh)

        # 3. Objective Function: Minimize total electricity cost + tiny peak grid tie-breaker
        objective = solver.Objective()
        for h in range(24):
            objective.SetCoefficient(grid[h], tariff[h])
        objective.SetCoefficient(peak_grid, 1e-6)
        objective.SetMinimization()

        # 4. Solve
        status = solver.Solve()

        if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
            status_str = {
                pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
                pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
                pywraplp.Solver.ABNORMAL: "ABNORMAL",
                pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
            }.get(status, f"UNKNOWN_STATUS_{status}")
            logger.error(f"Solver failed with status {status_str} for scenario '{scenario.scenario_id}'")
            raise ValueError(f"Energy dispatch optimization is infeasible under provided constraints ({status_str}).")

        # 5. Extract and format solution
        hourly_plan: List[HourlyPlanEntry] = []
        raw_total_grid = 0.0
        raw_total_cost = 0.0
        raw_peak_grid = 0.0

        for h in range(24):
            g_val = max(0.0, grid[h].solution_value())
            s_val = max(0.0, solar_used[h].solution_value())
            c_val = max(0.0, charge[h].solution_value())
            d_val = max(0.0, discharge[h].solution_value())
            e_val = max(0.0, energy_after[h].solution_value())

            # Determine action and transfer quantity
            if c_val > 1e-4:
                action = "charge"
                b_kwh = c_val
            elif d_val > 1e-4:
                action = "discharge"
                b_kwh = d_val
            else:
                action = "idle"
                b_kwh = 0.0

            raw_total_grid += g_val
            raw_total_cost += g_val * tariff[h]
            if g_val > raw_peak_grid:
                raw_peak_grid = g_val

            hourly_plan.append(
                HourlyPlanEntry(
                    hour=h,
                    grid_kwh=round(g_val, 2),
                    solar_used_kwh=round(s_val, 2),
                    battery_action=action,
                    battery_kwh=round(b_kwh, 2),
                    battery_energy_after_kwh=round(e_val, 2),
                )
            )

        total_grid_kwh = round(raw_total_grid, 2)
        total_cost_bdt = round(raw_total_cost, 2)
        peak_grid_kwh = round(raw_peak_grid, 2)

        logger.info(
            f"Optimization succeeded: total_cost={total_cost_bdt:.2f} BDT, "
            f"total_grid={total_grid_kwh:.2f} kWh, peak_grid={peak_grid_kwh:.2f} kWh"
        )

        return hourly_plan, total_grid_kwh, total_cost_bdt, peak_grid_kwh
