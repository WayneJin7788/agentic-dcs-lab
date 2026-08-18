from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .audit import JsonlAuditSink
from .models import Setpoints
from .runtime import ControlRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Agentic DCS Lab teaching simulator")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--target-load", type=float, default=300.0)
    parser.add_argument("--audit", default="artifacts/audit.jsonl")
    parser.add_argument("--fail-planner-at", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    runtime = ControlRuntime(
        setpoints=Setpoints(target_load_mw=args.target_load),
        audit=JsonlAuditSink(args.audit),
    )
    result = runtime.run(steps=args.steps, fail_planner_at=args.fail_planner_at)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()

