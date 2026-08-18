# Architecture

## 1. Trust boundaries

The architecture deliberately splits intelligence from authority.

1. **Process boundary** — a simulator today; read-only historians or OPC UA subscriptions may be added in shadow mode.
2. **Intelligence boundary** — state estimation, planning, optimization and explanation. Components may be probabilistic and replaceable.
3. **Authority boundary** — deterministic validation of freshness, permissions, invariants, rate limits and command envelopes.
4. **Protection boundary** — independent BMS/FSSS, ETS, SIS and hardwired/mechanical protection. This boundary is never controlled by the agent runtime.

No planner response is executable by itself. A command must have a known schema, current process context, allowed operating mode, bounded authority, successful deterministic validation and an audit record.

## 2. Control-time hierarchy

| Time scale | Example responsibility | Intended implementation |
|---|---|---|
| milliseconds | equipment protection, servo loops | certified deterministic systems; out of scope |
| 100 ms–seconds | PID/basic regulatory control | existing DCS/PLC or future verified runtime |
| seconds–minutes | coordinated control, constraint optimization | governed workflows/MPC/agents |
| minutes–hours | soot blowing, efficiency, dispatch planning | agents with approval and replay |
| days–months | tuning, maintenance, configuration generation | offline agents and engineering workflow |

## 3. Runtime transaction

Every cycle follows a transaction-like path:

1. acquire timestamped measurements;
2. validate quality, freshness and source identity;
3. construct a versioned process context;
4. request a proposal from one or more planners;
5. evaluate deterministic safety invariants and command envelopes;
6. simulate, recommend, or execute according to deployment mode;
7. append inputs, model/version, proposal, verdict and outcome to audit storage;
8. fall back on timeout, invalid output, unsafe state or infrastructure failure.

The prototype implements steps 3–8 against a teaching simulator. Data-quality validation and real adapters are roadmap items.

## 4. Planned extension points

- `PlantPort`: measurements, quality metadata and simulation stepping;
- `PlannerPort`: rules, MPC, RL policies, LLM tools or ensembles;
- `SafetyPolicy`: site-specific constraints compiled to deterministic checks;
- `ApprovalPort`: four-eyes approval and shift handover;
- `ExecutionPort`: simulation, shadow comparison, advisory ticket, or controlled write;
- `AuditSink`: append-only local records, signed event streams or compliant historian.

Real write adapters will not be accepted until the project has a versioned safety policy format, authentication/authorization model, freshness checks, replay harness, conformance suite and explicit maintainer approval policy.

