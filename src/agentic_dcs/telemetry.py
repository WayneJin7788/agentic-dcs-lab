from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .models import Measurement


class DataQuality(StrEnum):
    GOOD = "good"
    UNCERTAIN = "uncertain"
    BAD = "bad"


class TelemetryValidationError(ValueError):
    """Raised when field data is unsafe to consume."""


@dataclass(frozen=True)
class PointDefinition:
    key: str
    source_address: str
    engineering_unit: str
    minimum: float
    maximum: float
    max_age_s: float
    required: bool = True
    writable: bool = False

    def __post_init__(self) -> None:
        if not self.key or not self.source_address or not self.engineering_unit:
            raise TelemetryValidationError("point key, address and unit are required")
        if self.minimum >= self.maximum:
            raise TelemetryValidationError(f"invalid range for {self.key}")
        if self.max_age_s <= 0:
            raise TelemetryValidationError(f"max_age_s must be positive for {self.key}")
        if self.writable:
            raise TelemetryValidationError(
                f"point {self.key} is writable; the field-data layer is read-only"
            )


@dataclass(frozen=True)
class PointSample:
    key: str
    value: float
    source_timestamp_s: float
    quality: DataQuality


class PointRegistry:
    def __init__(self, points: list[PointDefinition]) -> None:
        self.points = {point.key: point for point in points}
        if len(self.points) != len(points):
            raise TelemetryValidationError("duplicate point key")

    @classmethod
    def from_json(cls, path: str | Path) -> PointRegistry:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls([PointDefinition(**item) for item in payload["points"]])

    def addresses(self) -> list[str]:
        return [point.source_address for point in self.points.values()]


class MeasurementAssembler:
    REQUIRED_KEYS = {
        "load_mw",
        "steam_pressure_mpa",
        "drum_level_mm",
        "oxygen_pct",
        "fuel_pct",
        "feedwater_pct",
        "air_pct",
        "throttle_pct",
    }

    def __init__(self, registry: PointRegistry) -> None:
        missing = self.REQUIRED_KEYS - registry.points.keys()
        if missing:
            raise TelemetryValidationError(f"registry missing canonical points: {sorted(missing)}")
        self.registry = registry

    def assemble(self, samples: list[PointSample], now_s: float) -> Measurement:
        by_key = {sample.key: sample for sample in samples}
        if len(by_key) != len(samples):
            raise TelemetryValidationError("duplicate samples in frame")
        values: dict[str, Any] = {"timestamp_s": now_s}

        for key in self.REQUIRED_KEYS:
            definition = self.registry.points[key]
            sample = by_key.get(key)
            if sample is None:
                raise TelemetryValidationError(f"missing required point: {key}")
            if sample.quality is not DataQuality.GOOD:
                raise TelemetryValidationError(f"non-good quality for {key}: {sample.quality}")
            age_s = now_s - sample.source_timestamp_s
            if age_s < 0 or age_s > definition.max_age_s:
                raise TelemetryValidationError(f"stale or future timestamp for {key}: {age_s=}")
            if not definition.minimum <= sample.value <= definition.maximum:
                raise TelemetryValidationError(f"out-of-range value for {key}: {sample.value}")
            values[key] = sample.value

        return Measurement(**values)
