import unittest

from agentic_dcs.audit import JsonlAuditSink
from agentic_dcs.models import DecisionStatus
from agentic_dcs.runtime import ControlRuntime


class RuntimeTests(unittest.TestCase):
    def test_nominal_run_is_audited_and_moves_toward_target(self) -> None:
        audit = JsonlAuditSink()
        runtime = ControlRuntime(audit=audit)
        result = runtime.run(steps=120)
        self.assertEqual(len(audit.records), 120)
        self.assertGreater(result.final_load_mw, 280.0)
        self.assertLess(abs(result.final_drum_level_mm), 180.0)

    def test_planner_failure_falls_back_without_stopping_runtime(self) -> None:
        audit = JsonlAuditSink()
        result = ControlRuntime(audit=audit).run(steps=10, fail_planner_at=4)
        self.assertEqual(result.steps, 10)
        self.assertEqual(audit.records[4]["decision"]["status"], DecisionStatus.FALLBACK)


if __name__ == "__main__":
    unittest.main()
