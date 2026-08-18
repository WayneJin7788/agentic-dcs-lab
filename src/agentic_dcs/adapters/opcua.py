from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from ..telemetry import PointRegistry, PointSample, TelemetryValidationError
from .base import ReadOnlyUaClient


@dataclass(frozen=True)
class OpcUaReadOnlyPolicy:
    endpoint_url: str
    allowed_hosts: tuple[str, ...]
    security_mode: str = "SignAndEncrypt"
    identity_kind: str = "certificate"

    def validate(self) -> None:
        endpoint = urlparse(self.endpoint_url)
        if endpoint.scheme != "opc.tcp" or not endpoint.hostname:
            raise TelemetryValidationError("an opc.tcp endpoint with a hostname is required")
        if endpoint.hostname not in self.allowed_hosts:
            raise TelemetryValidationError("OPC UA endpoint is not allowlisted")
        if self.security_mode != "SignAndEncrypt":
            raise TelemetryValidationError("OPC UA SignAndEncrypt is mandatory")
        if self.identity_kind == "anonymous":
            raise TelemetryValidationError("anonymous OPC UA identity is forbidden")


class OpcUaReadOnlyAdapter:
    """A capability-limited OPC UA reader; this class intentionally has no write API."""

    def __init__(
        self,
        client: ReadOnlyUaClient,
        registry: PointRegistry,
        policy: OpcUaReadOnlyPolicy,
    ) -> None:
        policy.validate()
        self._client = client
        self._registry = registry
        self.policy = policy

    async def read_once(self) -> list[PointSample]:
        points = list(self._registry.points.values())
        raw_values = await self._client.read_values([point.source_address for point in points])
        if len(raw_values) != len(points):
            raise TelemetryValidationError("OPC UA read returned an incomplete frame")
        return [
            PointSample(
                key=point.key,
                value=float(result.value),
                source_timestamp_s=result.source_timestamp_s,
                quality=result.quality,
            )
            for point, result in zip(points, raw_values, strict=True)
        ]
