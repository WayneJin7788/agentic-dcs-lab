from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .models import ActuatorCommand, Measurement


@dataclass
class BoilerTurbinePlant:
    """Small deterministic teaching model; not a validated power-plant model."""

    load_mw: float = 280.0
    steam_pressure_mpa: float = 16.2
    drum_level_mm: float = 0.0
    oxygen_pct: float = 3.8
    fuel_pct: float = 55.0
    feedwater_pct: float = 55.0
    air_pct: float = 58.0
    throttle_pct: float = 55.0
    timestamp_s: float = 0.0
    seed: int = 7

    def __post_init__(self) -> None:
        self._random = Random(self.seed)

    def observe(self) -> Measurement:
        return Measurement(
            timestamp_s=self.timestamp_s,
            load_mw=self.load_mw,
            steam_pressure_mpa=self.steam_pressure_mpa,
            drum_level_mm=self.drum_level_mm,
            oxygen_pct=self.oxygen_pct,
            fuel_pct=self.fuel_pct,
            feedwater_pct=self.feedwater_pct,
            air_pct=self.air_pct,
            throttle_pct=self.throttle_pct,
        )

    def step(self, command: ActuatorCommand, dt_s: float = 1.0) -> Measurement:
        self.fuel_pct = command.fuel_pct
        self.feedwater_pct = command.feedwater_pct
        self.air_pct = command.air_pct
        self.throttle_pct = command.throttle_pct

        demand_mw = 5.15 * self.throttle_pct
        available_mw = 5.35 * self.fuel_pct
        self.load_mw += dt_s * (min(demand_mw, available_mw) - self.load_mw) / 18.0

        pressure_drive = 0.035 * (self.fuel_pct - self.throttle_pct)
        self.steam_pressure_mpa += dt_s * (
            pressure_drive - 0.08 * (self.steam_pressure_mpa - 16.5)
        )

        evaporation = self.fuel_pct * 0.98
        self.drum_level_mm += dt_s * (
            0.45 * (self.feedwater_pct - evaporation) - 0.018 * self.drum_level_mm
        )

        oxygen_target = 2.0 + 0.065 * max(0.0, self.air_pct - 0.88 * self.fuel_pct)
        self.oxygen_pct += dt_s * (oxygen_target - self.oxygen_pct) / 10.0

        self.load_mw += self._random.uniform(-0.03, 0.03)
        self.timestamp_s += dt_s
        return self.observe()

