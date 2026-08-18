from __future__ import annotations

from dataclasses import dataclass

from .agents import FallbackController, ObserverAgent, PlannerAgent, SafetyGovernor
from .audit import JsonlAuditSink
from .models import ActuatorCommand, Decision, DecisionStatus, Setpoints
from .plant import BoilerTurbinePlant


@dataclass(frozen=True)
class RunResult:
    steps: int
    final_load_mw: float
    final_pressure_mpa: float
    final_drum_level_mm: float
    rejected_decisions: int
    clamped_decisions: int


class ControlRuntime:
    def __init__(
        self,
        plant: BoilerTurbinePlant | None = None,
        setpoints: Setpoints | None = None,
        audit: JsonlAuditSink | None = None,
    ) -> None:
        self.plant = plant or BoilerTurbinePlant()
        self.setpoints = setpoints or Setpoints()
        self.observer = ObserverAgent()
        self.planner = PlannerAgent()
        self.governor = SafetyGovernor()
        self.fallback = FallbackController()
        self.audit = audit or JsonlAuditSink()

    def run(self, steps: int = 300, fail_planner_at: int | None = None) -> RunResult:
        measurement = self.plant.observe()
        previous = self.fallback.hold(measurement)
        rejected = 0
        clamped = 0

        for index in range(steps):
            context = self.observer.analyze(measurement, self.setpoints)
            try:
                if fail_planner_at is not None and index == fail_planner_at:
                    raise RuntimeError("injected planner failure")
                proposed = self.planner.propose(context)
                decision = self.governor.evaluate(measurement, proposed, previous)
            except Exception as exc:  # boundary intentionally catches replaceable planner failures
                hold = self.fallback.hold(measurement)
                decision = Decision(
                    proposed=hold,
                    applied=hold,
                    status=DecisionStatus.FALLBACK,
                    reasons=[f"planner unavailable: {type(exc).__name__}"],
                )

            self.audit.record(measurement, decision)
            rejected += decision.status == DecisionStatus.REJECTED
            clamped += decision.status == DecisionStatus.CLAMPED
            previous = decision.applied
            measurement = self.plant.step(decision.applied)

        return RunResult(
            steps=steps,
            final_load_mw=measurement.load_mw,
            final_pressure_mpa=measurement.steam_pressure_mpa,
            final_drum_level_mm=measurement.drum_level_mm,
            rejected_decisions=rejected,
            clamped_decisions=clamped,
        )

