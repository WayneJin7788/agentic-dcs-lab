# Agentic DCS Lab

Agentic DCS Lab is a simulation-first, auditable, safety-separated reference framework for researching governed agentic workflows in coal-fired power-plant control.

> **Research software. Not for production control.** It is not plant-, SIL-, type-, or regulator-certified. Never connect this repository to a live DCS write path or use it to replace BMS/FSSS, ETS, SIS, mechanical protection, or emergency manual shutdown.

The long-term research goal is to migrate suitable control intent from proprietary DCS configuration into open, testable, replayable, approvable and fail-safe workflows. It is explicitly **not** an attempt to let an LLM directly operate valves. Deterministic basic control and independent protection remain outside the AI trust boundary.

The v0.2 prototype adds a vendor-neutral point registry, data quality/freshness/range validation, deterministic historian replay, a capability-limited OPC UA read boundary, and a shadow evaluator with no execution API. It retains the boiler-turbine simulator, deterministic safety governor, planner-failure fallback, and JSONL audit records. See the [Chinese README](README.md), [architecture](docs/architecture.md), [real DCS data guide](docs/real-dcs-data.md), [safety case](docs/safety-case.md), and [roadmap](ROADMAP.md).

```bash
python -m venv .venv
python -m pip install -e .
agentic-dcs --steps 300 --target-load 300
python examples/run_shadow_replay.py
```

Apache-2.0 licensed. Contributions are welcome, subject to the safety and data-handling rules in [CONTRIBUTING.md](CONTRIBUTING.md).

