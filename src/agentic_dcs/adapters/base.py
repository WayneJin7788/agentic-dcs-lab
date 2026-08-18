from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..telemetry import DataQuality


@dataclass(frozen=True)
class UaReadValue:
    value: float
    source_timestamp_s: float
    quality: DataQuality


class ReadOnlyUaClient(Protocol):
    async def read_values(self, node_ids: list[str]) -> list[UaReadValue]: ...
