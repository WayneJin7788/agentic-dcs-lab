from pathlib import Path

from agentic_dcs.adapters import CsvHistorianReplay
from agentic_dcs.shadow import ShadowEvaluator
from agentic_dcs.telemetry import MeasurementAssembler, PointRegistry

root = Path(__file__).parents[1]
registry = PointRegistry.from_json(root / "config" / "real-points.example.json")
assembler = MeasurementAssembler(registry)
evaluator = ShadowEvaluator()

for timestamp_s, samples in CsvHistorianReplay(root / "examples" / "historian.sample.csv").frames():
    measurement = assembler.assemble(samples, now_s=timestamp_s)
    result = evaluator.evaluate(measurement)
    print(timestamp_s, result.decision.status, result.decision.applied)
