from __future__ import annotations

from dataclasses import dataclass

from .agents import FallbackController, ObserverAgent, PlannerAgent, SafetyGovernor
from .models import ActuatorCommand, Decision, Measurement, Setpoints


@dataclass(frozen=True)
class ShadowResult:
    measurement: Measurement
    decision: Decision


class ShadowEvaluator:
    """Evaluates field measurements without possessing an execution capability."""

    def __init__(self, setpoints: Setpoints | None = None) -> None:
        self.setpoints = setpoints or Setpoints()
        self.observer = ObserverAgent()
        self.planner = PlannerAgent()
        self.governor = SafetyGovernor()
        self.fallback = FallbackController()

    def evaluate(
        self,
        measurement: Measurement,
        previous: ActuatorCommand | None = None,
    ) -> ShadowResult:
        prior = previous or self.fallback.hold(measurement)
        context = self.observer.analyze(measurement, self.setpoints)
        proposed = self.planner.propose(context)
        decision = self.governor.evaluate(measurement, proposed, prior)
        return ShadowResult(measurement=measurement, decision=decision)
