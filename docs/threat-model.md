# Threat model

## Assets

Personnel safety, equipment integrity, grid obligations, environmental compliance, process availability, configuration provenance, model artifacts, credentials, audit history and confidential plant data.

## Representative threats

| Threat | Example | Required controls |
|---|---|---|
| forged telemetry | replayed or manipulated process values | authenticated source, freshness/sequence checks, plausibility and redundancy |
| prompt/tool injection | historian text or operator note changes planner behavior | structured data boundary, tool allowlist, no untrusted text in authority logic |
| excessive authority | planner writes outside assigned loop | least privilege, per-tag allowlist, command envelope and expiring lease |
| unsafe model drift | policy degrades after fuel/equipment change | drift monitoring, replay benchmark, approval and rollback |
| supply-chain compromise | malicious dependency or model | pinning, SBOM, signing, review and isolated build |
| loss of communications | planner or network timeout | deterministic local fallback and watchdog |
| audit tampering | incident trail modified | append-only signed records and external retention |
| common-cause failure | AI and protection share dependencies | independent protection, power, networks and logic solvers |

## Prohibited design patterns

- unauthenticated OPC UA `None` security profile outside isolated test rigs;
- direct natural-language-to-actuator execution;
- shared credentials or all-tags write permission;
- fail-open behavior on timeout or schema error;
- hidden online learning in a production control path;
- sending plant-sensitive data to external models without authorization.

