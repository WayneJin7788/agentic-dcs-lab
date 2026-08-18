# Roadmap

## v0.1 — safe skeleton

- [x] boiler-turbine teaching simulator
- [x] observe/plan/govern/execute/audit workflow
- [x] deterministic bounds, rate limits and fallback
- [x] safety case, threat model and deployment maturity model
- [x] CI and contributor governance

## v0.2 — reproducible evaluation

- [ ] versioned scenario schema and scenario catalog
- [x] measurement quality/freshness model
- [x] deterministic CSV historian replay foundation
- [ ] golden traces and historian format plugins
- [ ] metrics: constraint violations, tracking error, settling time and intervention rate
- [ ] fault-injection matrix for sensor, actuator, planner and communications failures
- [ ] baseline PID and MPC planners for comparison

## v0.3 — configuration intelligence

- [ ] vendor-neutral control-logic intermediate representation
- [ ] import/export prototypes for sanitized IEC 61131-3 fragments
- [ ] static checks for dead logic, conflicting interlocks and undocumented bypasses
- [ ] agent-assisted configuration generation that only produces reviewable patches

## v0.4 — shadow laboratory

- [x] capability-limited read-only OPC UA boundary and policy checks
- [x] vendor-neutral point registry and canonical measurement mapping
- [ ] production OPC UA SDK bridge with site-managed PKI
- [ ] time-series connectors and digital-twin calibration API
- [ ] proposal-versus-DCS comparison dashboard
- [ ] model registry, signed policies and SBOM
- [ ] operator feedback workflow

## Future research

- hierarchical multi-agent coordination for boiler, turbine and auxiliaries;
- uncertainty-aware MPC/RL with runtime assurance;
- explainable abnormal-situation management;
- formal verification of workflow and safety-policy intermediate representations;
- cross-unit benchmarks using fully synthetic or legally shareable data.

There is no date commitment for controlled write. Safety evidence, not feature pressure, controls progression.

