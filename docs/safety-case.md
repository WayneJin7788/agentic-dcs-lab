# Preliminary safety case

This is a research argument structure, not a certified safety case.

## Top claim

The v0.1 repository can be used for offline education and simulation experiments without providing a mechanism to command a real plant.

## Evidence in v0.1

- The only process implementation is an in-memory teaching simulator.
- No production protocol or write adapter is included.
- Every planner proposal passes through a separate deterministic governor.
- Output bounds and per-cycle change limits are tested.
- Unsafe measured pressure, drum level or oxygen causes proposal rejection and output hold.
- Planner exceptions produce a fallback decision and do not stop the runtime.
- Measurements, proposals, applied values, verdicts and reasons are auditable.

## Assumptions

- Users obey the non-production warning and do not repurpose the simulator port as a live write path.
- The simplified model is treated as pedagogical, not as an identified model of any unit.
- Independent protection functions remain available and outside this software.

## Known gaps before shadow mode

- sensor quality, timestamp freshness and bad-value handling;
- redundant data-source reconciliation;
- authenticated and encrypted read-only protocol adapter;
- configuration signing and supply-chain provenance;
- deterministic replay across runtime versions;
- alarm rationalization and operator human-factors review;
- site HAZOP/LOPA and cybersecurity risk assessment.

## Additional gates before any controlled write

Controlled write is a research-stage destination, not a promised feature. At minimum it requires site-specific hazard analysis, safety requirements specification, independent verification and validation, formal management of change, segmented OT architecture, least privilege, two-person approval where appropriate, bounded command leases, watchdogs, tested bumpless fallback, disaster recovery, operator training and acceptance by the asset owner and relevant authorities.

AI/agent software must never become the sole layer preventing a hazardous event.

