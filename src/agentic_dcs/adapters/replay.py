from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from ..telemetry import DataQuality, PointSample


class CsvHistorianReplay:
    """Deterministic long-format historian replay: timestamp_s,key,value,quality."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def frames(self) -> list[tuple[float, list[PointSample]]]:
        grouped: dict[float, list[PointSample]] = defaultdict(list)
        with self.path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                timestamp_s = float(row["timestamp_s"])
                grouped[timestamp_s].append(
                    PointSample(
                        key=row["key"],
                        value=float(row["value"]),
                        source_timestamp_s=timestamp_s,
                        quality=DataQuality(row.get("quality", "good")),
                    )
                )
        return sorted(grouped.items())
