# Integration maturity model

## Level 0 — simulation (implemented)

Synthetic plant only. CI exercises safety invariants, failure injection and audit output.

## Level 1 — shadow

Read-only, one-way data replication into a segregated research environment. Proposed outputs are compared with operator/DCS actions and can never reach control equipment.

The repository now implements the point registry, historian replay, field-data validation, a capability-limited OPC UA reader boundary and a shadow evaluator. See [real-dcs-data.md](real-dcs-data.md). A site-specific SDK bridge and cybersecurity approval are still required before connecting to any plant network.

Exit evidence: data-quality handling, replay determinism, cybersecurity review, scenario coverage, documented false-positive/negative rates and operator review.

## Level 2 — advisory

Recommendations appear in a separate interface and require a qualified operator to independently assess and enter any action through existing procedures.

Exit evidence: human-factors validation, approval workflow, clear uncertainty and rationale, alarm-load assessment, training and management of change.

## Level 3 — controlled write

Only narrowly scoped, reversible, rate-limited commands behind deterministic permissions and independent protection. This level is intentionally not implemented.

Exit evidence must be defined per site through the applicable safety lifecycle and regulatory process. Repository tests alone can never authorize this mode.

## OPC UA direction

A future read-only adapter should require certificate-based application identity, endpoint allowlisting, `SignAndEncrypt`, current secure profiles, user/role authorization, certificate lifecycle management and complete audit correlation. The `None` profile is for isolated testing only.

