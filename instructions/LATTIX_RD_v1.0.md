# Lattix research and development program v1.0

## Mission and scope

Develop reusable, inspectable spatial computation upstream of rendering and below application-specific simulation. The commercial hypothesis is that explicit limits, portable reference behavior and reproducible failure reports reduce lifecycle cost enough to justify integration effort. This is a CANDIDATE value proposition until supported by matched measurements and customer evidence.

Spatial is the reusable indexing/query core. Particles is a bounded reference solver. Lab is the conformance, inspection and profiling surface. Unity/Unreal are integration ecosystems; PhysX/Havok/FleX comparisons must state solver scope. Custom compute code is the closest architectural comparison.

## Evidence and promotion

| Label | Permitted meaning |
| --- | --- |
| HYPOTHESIS / CANDIDATE | Proposed mechanism, feature, benefit or result requiring a discriminating test |
| ANALOGY | Explanatory similarity; no equivalence proof |
| CONDITIONAL / DERIVED | Consequence of explicit assumptions, within their scope |
| EXACT | Proof or reproducible exact calculation in a specified domain |
| NUMERICAL | Approximate computation with precision, tolerance and workload stated |
| EMPIRICAL | Observed measurement with execution environment and uncertainty |
| FIT | Choices selected against exposed targets; fitting history retained |
| FAILED / NO-GO | Failed declared gate or obstruction with exact hypotheses |
| OPEN | Missing definition, evidence or dependency |

Machine manifests use HYPOTHESIS, ANALOGY, CONDITIONAL, EXACT, NUMERICAL, EMPIRICAL, FIT, FAILED or OPEN. CANDIDATE, DERIVED and NO-GO are prose categories whose assumptions must accompany the appropriate manifest label. Workflow status and evidence label are different fields.

Preregistration is required for confirmatory comparative benchmark claims, not for exploratory coding. Freeze workloads, algorithms, capacities, quality gates, hardware/driver policy, warmups, repetitions, exclusions and statistics before measured targets are exposed. An amendment after exposure is exploratory unless evaluated on fresh independent data.

Implementation milestones, scoped correctness, measured speed, portable determinism, engine integration and product readiness are separate promotions. A CPU oracle cannot establish GPU timing. A hash cannot prove content correctness. CI cannot approve its own scientific interpretation.

## Program boundaries

- C12A: spatial correctness and resource/performance behavior independent of the particle solver.
- C12B: matched sphere-contact quality and performance; preserve historical B1–B5 definitions when their source packages are reconciled.
- C12C: transfer, synchronization, adapter overhead and effort, including zero-copy only where measured and supported.
- Keep historical C12 records unchanged. Missing previous packages are SOURCE_INTAKE_OPEN; do not reconstruct their numeric gates from memory.
- Native engine adapters, broad hardware coverage and solver expansion remain independent work items. This framework does not implement them.

## Ownership and releases

Follow the live claim protocol and contributor registry. Capture per-session evidence; integrate shared summaries through reviewed PRs. Use append-only updates and explicit amendments. Source snapshots are immutable; upstream changes require a new provenance import and dependency review. Do not rewrite frozen results to match current marketing.

Keep diagnostics on research/evidence surfaces. Marketing may describe defined architecture and verified features, but cannot promote proposed speedups or make comprehensive physics-engine replacement claims. UD lineage is source attribution, not inherited physical validation.
