import unittest

from agentic_dcs.agents import SafetyGovernor
from agentic_dcs.models import ActuatorCommand, DecisionStatus, Measurement


def measurement(**overrides: float) -> Measurement:
    values = {
        "timestamp_s": 0.0,
        "load_mw": 300.0,
        "steam_pressure_mpa": 16.7,
        "drum_level_mm": 0.0,
        "oxygen_pct": 3.5,
        "fuel_pct": 55.0,
        "feedwater_pct": 55.0,
        "air_pct": 58.0,
        "throttle_pct": 55.0,
    }
    values.update(overrides)
    return Measurement(**values)


class SafetyGovernorTests(unittest.TestCase):
    def test_governor_rate_limits_every_output(self) -> None:
        previous = ActuatorCommand(50.0, 50.0, 50.0, 50.0)
        proposed = ActuatorCommand(90.0, 10.0, 90.0, 10.0)
        decision = SafetyGovernor().evaluate(measurement(), proposed, previous)
        self.assertEqual(decision.status, DecisionStatus.CLAMPED)
        self.assertEqual(decision.applied, ActuatorCommand(52.5, 47.5, 52.5, 47.5))

    def test_governor_rejects_unsafe_process_state(self) -> None:
        previous = ActuatorCommand(50.0, 50.0, 50.0, 50.0)
        proposed = ActuatorCommand(51.0, 51.0, 51.0, 51.0)
        decision = SafetyGovernor().evaluate(
            measurement(steam_pressure_mpa=19.0), proposed, previous
        )
        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.applied, previous)


if __name__ == "__main__":
    unittest.main()
