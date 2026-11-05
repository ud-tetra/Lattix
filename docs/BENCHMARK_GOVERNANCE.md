# C12 evidence governance v1.0

This repository implements the user's accepted three-lane comparison boundary. Earlier C12 source packages and numeric gates have not been imported in this bootstrap; reconciliation is a tracked prerequisite. Historical B1–B5 definitions must be preserved unchanged when sourced, not invented here.

| Lane | Subject | Required independent reporting | Prohibited inference |
| --- | --- | --- | --- |
| C12A | Spatial kernel | Exact indexing/query checks; build/query throughput; candidates; occupancy/spill; memory and failure behavior | Kernel win implies Lattix beats an entire engine |
| C12B | Particle reference solver | Matched scene, timestep, precision and sphere-contact quality gates alongside solver timings | Scoped result implies PhysX/Havok/FleX feature equivalence |
| C12C | Engine integration | CPU↔GPU copies, bytes/frame, synchronization, bridge overhead, ownership/lifetime and implementation effort | Zero-copy exists because the architecture could support it |

## Preregister

Create a draft from templates/preregistration.json under benchmarks/preregistrations/. Define workload distributions, seeds, capacities, overflow policy, baselines, build/compiler settings, timer semantics, repetitions, quality/error thresholds, exclusions and interpretation. Freeze through a versioned reviewed commit before target runs. Record that exact commit and file SHA-256 in each receipt. A changed protocol gets a new ID and amendment, never an edit to frozen history.

## Capture and report

CPU_REFERENCE, WEBGPU_HARDWARE and ENGINE_ADAPTER are separate execution modes. Record unavailable hardware as NOT_RUN. Actual runs require a source revision, device/software details, timing method and synchronization scope, metrics with units, protocol reference/digest and immutable run manifest. C12B receipts include quality gates; C12C includes measured transfer path, bytes/frame, synchronization and effort. FAIL and INCONCLUSIVE are preserved rather than removed.

Determinism must name the operation, input ordering, precision, backend and comparison rule. Reference semantics can be exact without guaranteeing identical floating-point GPU trajectories across hardware. Memory ceilings must include all relevant buffers and spill paths; overflow must produce inspectable receipts rather than silently dropped work.

The validator checks structural completeness, referenced bytes and lane fields. It does not replay a GPU run, assess a proof, certify preregistration chronology, authenticate a device, enforce numeric thresholds or grant marketing permission. Review must compare raw trials with the frozen acceptance rule and verify its commit predates exposure. Synthetic fixtures in tests are not product evidence.

## Promotion record

Record lane, scope, measured hardware, protocol version, run manifests, review relationship, passed/failed gates, remaining risks and permitted claims in reviews/. Promote lanes independently. Product integration and lifecycle savings require measured adoption evidence beyond kernel throughput.
