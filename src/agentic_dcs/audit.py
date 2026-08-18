from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import Decision, Measurement


class JsonlAuditSink:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self.records: list[dict[str, Any]] = []

    def record(self, measurement: Measurement, decision: Decision) -> None:
        item = {"measurement": asdict(measurement), "decision": asdict(decision)}
        self.records.append(item)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(item, ensure_ascii=False, default=str) + "\n")

