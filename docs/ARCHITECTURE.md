# Repository architecture v1.0

| Layer | Location | Contract |
| --- | --- | --- |
| Entry and runtime policy | BOOTLOADER.md, AGENTS.md, instructions/ | Verified startup and source-controlled behavior |
| Program and contributors | config/ | Public identity/role configuration; no credentials |
| Work planning | tasks/ | Scoped owned paths, dependency graph, acceptance rules |
| Coordination | refs/heads/claims/<task> | Atomic acquisition and retained release markers |
| Worker state | sessions/ | One writer per session; runtime, base, claims, journal and handoff |
| Research proposals | candidates/, experiments/ | Assumptions, alternatives, code and failed results |
| Evidence | artifacts/ | Immutable selected input/output bytes plus manifests |
| Source lineage | sources/imports/ | Versioned snapshots, hashes and adaptation map |
| Benchmark control | benchmarks/ | Preregistrations and receipts with separate C12 lanes |
| Review and integration | reviews/, state/ | Scoped review, integrated milestones and append-only updates |
| Automation | scripts/, tests/, .github/ | Integrity checks and tested cooperative tooling |

One task may have many runs, one session owns a held task claim, and each run links back to its session and source revision. A contributor may run multiple isolated sessions. Sessions do not share working directories or writable experiment outputs.

Spatial/Particles/Lab are program boundaries here, not installed packages. Future implementation directories must enter through scoped tasks and explicit API contracts. The architecture intentionally preserves the upstream claim protocol and artifact schema while adapting runtime identity, benchmark evidence and product boundaries.
