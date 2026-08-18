from __future__ import annotations

from dataclasses import dataclass

from .models import (
    ActuatorCommand,
    Decision,
    DecisionStatus,
    Measurement,
    SafetyLimits,
    Setpoints,
)


@dataclass(frozen=True)
class ProcessContext:
    measurement: Measurement
    setpoints: Setpoints
    load_error_mw: float
    pressure_error_mpa: float
    level_error_mm: float
    oxygen_error_pct: float


class ObserverAgent:
    def analyze(self, measurement: Measurement, setpoints: Setpoints) -> ProcessContext:
        return ProcessContext(
            measurement=measurement,
            setpoints=setpoints,
            load_error_mw=setpoints.target_load_mw - measurement.load_mw,
            pressure_error_mpa=setpoints.target_pressure_mpa - measurement.steam_pressure_mpa,
            level_error_mm=setpoints.target_drum_level_mm - measurement.drum_level_mm,
            oxygen_error_pct=setpoints.target_oxygen_pct - measurement.oxygen_pct,
        )


class PlannerAgent:
    """Replaceable example planner. It intentionally uses transparent heuristics."""

    def propose(self, context: ProcessContext) -> ActuatorCommand:
        m = context.measurement
        fuel = m.fuel_pct + 0.028 * context.load_error_mw + 0.7 * context.pressure_error_mpa
        throttle = m.throttle_pct + 0.035 * context.load_error_mw - 0.25 * context.pressure_error_mpa
        feedwater = m.feedwater_pct + 0.06 * context.level_error_mm + 0.35 * (fuel - m.fuel_pct)
        air = m.air_pct + 0.55 * (fuel - m.fuel_pct) + 0.8 * context.oxygen_error_pct
        return ActuatorCommand(fuel, feedwater, air, throttle)


class SafetyGovernor:
    """Deterministic invariant and rate-limit enforcement, independent of the planner."""

    def __init__(self, limits: SafetyLimits | None = None) -> None:
        self.limits = limits or SafetyLimits()

    def evaluate(
        self,
        measurement: Measurement,
        proposed: ActuatorCommand,
        previous: ActuatorCommand,
    ) -> Decision:
        hard_stop_reasons: list[str] = []
        if measurement.steam_pressure_mpa > self.limits.max_pressure_mpa:
            hard_stop_reasons.append("steam pressure above hard limit")
        if measurement.steam_pressure_mpa < self.limits.min_pressure_mpa:
            hard_stop_reasons.append("steam pressure below hard limit")
        if abs(measurement.drum_level_mm) > self.limits.max_abs_drum_level_mm:
            hard_stop_reasons.append("drum level outside hard limit")
        if measurement.oxygen_pct < self.limits.min_oxygen_pct:
            hard_stop_reasons.append("oxygen below combustion safety limit")

        if hard_stop_reasons:
            return Decision(
                proposed=proposed,
                applied=previous,
                status=DecisionStatus.REJECTED,
                reasons=hard_stop_reasons,
            )

        applied_values: dict[str, float] = {}
        reasons: list[str] = []
        for name, value in proposed.as_dict().items():
            old = getattr(previous, name)
            rate_limited = max(
                old - self.limits.max_delta_pct_per_step,
                min(old + self.limits.max_delta_pct_per_step, value),
            )
            bounded = max(
                self.limits.min_actuator_pct,
                min(self.limits.max_actuator_pct, rate_limited),
            )
            applied_values[name] = bounded
            if abs(bounded - value) > 1e-9:
                reasons.append(f"{name} clamped by bounds/rate limit")

        applied = ActuatorCommand(**applied_values)
        status = DecisionStatus.CLAMPED if reasons else DecisionStatus.ACCEPTED
        return Decision(proposed=proposed, applied=applied, status=status, reasons=reasons)


class FallbackController:
    def hold(self, measurement: Measurement) -> ActuatorCommand:
        return ActuatorCommand(
            measurement.fuel_pct,
            measurement.feedwater_pct,
            measurement.air_pct,
            measurement.throttle_pct,
        )

