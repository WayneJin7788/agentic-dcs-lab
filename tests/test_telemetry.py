import tempfile
import unittest
from pathlib import Path

from agentic_dcs.adapters import CsvHistorianReplay, OpcUaReadOnlyAdapter, OpcUaReadOnlyPolicy
from agentic_dcs.adapters.base import UaReadValue
from agentic_dcs.telemetry import (
    DataQuality,
    MeasurementAssembler,
    PointDefinition,
    PointRegistry,
    PointSample,
    TelemetryValidationError,
)


def registry() -> PointRegistry:
    return PointRegistry(
        [
            PointDefinition(key, f"ns=2;s={key}", unit, low, high, 5)
            for key, unit, low, high in [
                ("load_mw", "MW", 0, 1200),
                ("steam_pressure_mpa", "MPa", 0, 35),
                ("drum_level_mm", "mm", -500, 500),
                ("oxygen_pct", "%", 0, 21),
                ("fuel_pct", "%", 0, 100),
                ("feedwater_pct", "%", 0, 100),
                ("air_pct", "%", 0, 100),
                ("throttle_pct", "%", 0, 100),
            ]
        ]
    )


class FakeUaClient:
    async def read_values(self, node_ids: list[str]) -> list[UaReadValue]:
        return [
            UaReadValue(value, source_timestamp_s=10, quality=DataQuality.GOOD)
            for value in [300, 16.7, 0, 3.5, 50, 50, 50, 50]
        ]


class TelemetryTests(unittest.TestCase):
    def test_registry_rejects_writable_points(self) -> None:
        with self.assertRaises(TelemetryValidationError):
            PointDefinition("x", "ns=2;s=x", "%", 0, 100, 1, writable=True)

    def test_assembler_rejects_bad_quality_and_stale_data(self) -> None:
        point_registry = registry()
        samples = [
            PointSample(key, 1, 10, DataQuality.GOOD) for key in point_registry.points
        ]
        samples[0] = PointSample(samples[0].key, 1, 0, DataQuality.BAD)
        with self.assertRaises(TelemetryValidationError):
            MeasurementAssembler(point_registry).assemble(samples, now_s=10)

    def test_csv_replay_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.csv"
            path.write_text(
                "timestamp_s,key,value,quality\n2,x,2,good\n1,x,1,good\n",
                encoding="utf-8",
            )
            frames = CsvHistorianReplay(path).frames()
        self.assertEqual([timestamp for timestamp, _ in frames], [1.0, 2.0])


class OpcUaTests(unittest.IsolatedAsyncioTestCase):
    async def test_adapter_is_allowlisted_encrypted_and_read_only(self) -> None:
        adapter = OpcUaReadOnlyAdapter(
            FakeUaClient(),
            registry(),
            OpcUaReadOnlyPolicy(
                endpoint_url="opc.tcp://dcs-gateway.local:4840",
                allowed_hosts=("dcs-gateway.local",),
            ),
        )
        samples = await adapter.read_once()
        self.assertEqual(len(samples), 8)
        self.assertTrue(all(sample.source_timestamp_s == 10 for sample in samples))
        self.assertFalse(hasattr(adapter, "write"))

    async def test_adapter_rejects_unapproved_endpoint(self) -> None:
        with self.assertRaises(TelemetryValidationError):
            OpcUaReadOnlyAdapter(
                FakeUaClient(),
                registry(),
                OpcUaReadOnlyPolicy(
                    endpoint_url="opc.tcp://unknown.local:4840",
                    allowed_hosts=("dcs-gateway.local",),
                ),
            )


if __name__ == "__main__":
    unittest.main()
