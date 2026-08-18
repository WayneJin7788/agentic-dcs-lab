from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class OperatingMode(StrEnum):
    SIMULATION = "simulation"
    SHADOW = "shadow"
    ADVISORY = "advisory"
    CONTROLLED_WRITE = "controlled_write"


class DecisionStatus(StrEnum):
    ACCEPTED = "accepted"
    CLAMPED = "clamped"
    REJECTED = "rejected"
    FALLBACK = "fallback"


@dataclass(frozen=True)
class Measurement:
    timestamp_s: float
    load_mw: float
    steam_pressure_mpa: float
    drum_level_mm: float
    oxygen_pct: float
    fuel_pct: float
    feedwater_pct: float
    air_pct: float
    throttle_pct: float


@dataclass(frozen=True)
class Setpoints:
    target_load_mw: float = 300.0
    target_pressure_mpa: float = 16.7
    target_drum_level_mm: float = 0.0
    target_oxygen_pct: float = 3.5


@dataclass(frozen=True)
class ActuatorCommand:
    fuel_pct: float
    feedwater_pct: float
    air_pct: float
    throttle_pct: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyLimits:
    min_pressure_mpa: float = 13.0
    max_pressure_mpa: float = 18.2
    max_abs_drum_level_mm: float = 180.0
    min_oxygen_pct: float = 1.8
    max_delta_pct_per_step: float = 2.5
    min_actuator_pct: float = 0.0
    max_actuator_pct: float = 100.0


@dataclass
class Decision:
    proposed: ActuatorCommand
    applied: ActuatorCommand
    status: DecisionStatus
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

