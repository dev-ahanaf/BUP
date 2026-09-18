"""Optimization service orchestrating interpretation, constraint application, solving, validation, and response assembly."""
from typing import List
from app.directives.engine import DirectiveEngine
from app.llm.interpreter import DirectiveInterpreter
from app.models.directive import DirectiveInterpretationEntry, DirectiveType
from app.models.request import OptimizationRequest
from app.models.response import HourlyPlanEntry, OptimizationResponse
from app.optimizer.solver import EnergyOptimizer
from app.validation.replay import ReplayValidator
from app.utils.logging import logger


class OptimizationService:
    """End-to-end service for smart campus energy dispatch optimization."""

    def __init__(
        self,
        interpreter: DirectiveInterpreter = None,
        optimizer: EnergyOptimizer = None,
    ) -> None:
        self.interpreter = interpreter or DirectiveInterpreter()
        self.optimizer = optimizer or EnergyOptimizer()

    async def process_scenario(self, request: OptimizationRequest) -> OptimizationResponse:
        """Execute the full optimization pipeline for a given scenario request."""
        logger.info(f"Starting pipeline for scenario '{request.scenario_id}'")

        # Step 1: Interpret operator notes into validated directives
        interpreted_directives = await self.interpreter.interpret(
            operator_notes=request.operator_notes,
            battery_capacity_kwh=request.battery.capacity_kwh,
        )

        # Step 2: Apply directives to build constrained operational profile
        constrained_scenario = DirectiveEngine.apply_directives(
            scenario_id=request.scenario_id,
            hours_data=request.hours,
            battery=request.battery,
            directives=interpreted_directives,
        )

        # Step 3: Solve MILP dispatch problem via OR-Tools
        hourly_plan, total_grid_kwh, total_cost_bdt, peak_grid_kwh = self.optimizer.solve(
            constrained_scenario
        )

        # Step 4: Perform independent replay validation
        val_result = ReplayValidator.validate_plan(
            scenario=constrained_scenario,
            hourly_plan=hourly_plan,
            total_grid_kwh=total_grid_kwh,
            total_cost_bdt=total_cost_bdt,
            peak_grid_kwh=peak_grid_kwh,
        )
        if not val_result.is_valid:
            error_msg = "; ".join(val_result.errors)
            logger.error(f"Replay validation failure on scenario '{request.scenario_id}': {error_msg}")
            raise ValueError(f"Generated dispatch plan failed replay validation: {error_msg}")

        # Step 5: Assemble structured plan summary
        plan_summary = self._generate_plan_summary(
            request=request,
            directives=interpreted_directives,
            hourly_plan=hourly_plan,
            total_cost=total_cost_bdt,
            total_grid=total_grid_kwh,
            peak_grid=peak_grid_kwh,
        )

        return OptimizationResponse(
            scenario_id=request.scenario_id,
            directive_interpretation=interpreted_directives,
            hourly_plan=hourly_plan,
            total_grid_kwh=total_grid_kwh,
            total_cost_bdt=total_cost_bdt,
            peak_grid_kwh=peak_grid_kwh,
            plan_summary=plan_summary,
        )

    def _generate_plan_summary(
        self,
        request: OptimizationRequest,
        directives: List[DirectiveInterpretationEntry],
        hourly_plan: List[HourlyPlanEntry],
        total_cost: float,
        total_grid: float,
        peak_grid: float,
    ) -> str:
        """Construct a detailed, informative summary of the optimized schedule."""
        applied_directives = [d for d in directives if d.applies]
        charge_hours = [p.hour for p in hourly_plan if p.battery_action == "charge"]
        discharge_hours = [p.hour for p in hourly_plan if p.battery_action == "discharge"]

        lines = [
            f"Scenario '{request.scenario_id}' optimized successfully with total electricity cost of {total_cost:.2f} BDT.",
            f"Key Metrics: Total Grid Import = {total_grid:.2f} kWh, Peak Grid Import = {peak_grid:.2f} kWh, Battery Neutrality = {request.battery.initial_energy_kwh:.2f} kWh.",
        ]

        if applied_directives:
            lines.append(f"Applied {len(applied_directives)} operational directive(s):")
            for d in applied_directives:
                lines.append(f" - [{d.directive_type.value}]: {d.explanation}")
        else:
            lines.append("No active operational constraints were applied (all notes informational or no-op).")

        if charge_hours:
            lines.append(f"Battery charging scheduled during hours: {charge_hours}.")
        if discharge_hours:
            lines.append(f"Battery discharging scheduled during hours: {discharge_hours}.")

        return "\n".join(lines)
