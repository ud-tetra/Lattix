# Lattix Systems · Research & Development

**Inspectable spatial-compute infrastructure.** Lattix develops a reusable layer between spatial data and application-specific simulation, with explicit resource budgets, defined reference behavior, and reproducible evidence.

This repository is the governed R&D workspace for the product program. It currently contains the **research operating framework**, not a released SDK or a validated performance advantage. Start with [BOOTLOADER.md](BOOTLOADER.md) before making changes.

## Product program

| Component | R&D scope | Evidence boundary |
| --- | --- | --- |
| **Lattix Spatial** | Indexing, neighborhood queries, lookup and merge semantics, bounded resource behavior | C12A: spatial correctness, build/query throughput, occupancy, spill and failure behavior |
| **Lattix Particles** | Reference local-interaction simulation over Spatial | C12B: matched sphere-contact quality and performance within a declared solver scope |
| **Lattix Lab** | Conformance, inspection, profiling, reproducibility and hardware validation | Evidence capture across all lanes; CPU reference checks remain distinct from hardware results |
| **Engine integration** | Unity/Unreal adapter contracts, transfers and synchronization | C12C: measured copy paths, bridge cost and implementation effort |

Unity and Unreal are integration ecosystems. Physics suites are scoped solver comparators. Custom CUDA/HLSL/WebGPU implementations are architectural comparators. A spatial-kernel result cannot establish full-engine superiority, physics-suite equivalence, or zero-copy availability.

## Start, contribute, reproduce

- [Bootloader](BOOTLOADER.md) · [Contributor guide](CONTRIBUTING.md) · [Runtime instructions](AGENTS.md)
- [Architecture](docs/ARCHITECTURE.md) · [Workflow](docs/WORKFLOW.md) · [Multi-user configuration](docs/MULTI_USER.md)
- [Task coordination](docs/CONCURRENCY.md) · [Artifact capture](docs/ARTIFACTS.md) · [Research method](docs/RESEARCH_METHOD.md)
- [Benchmark governance](docs/BENCHMARK_GOVERNANCE.md) · [Current state](state/CURRENT.md) · [Roadmap and tasks](tasks/README.md)
- [Source lineage](docs/SOURCES.md) · [Administration and enforcement](docs/ADMIN_SETUP.md) · [Updates](state/UPDATES.md)

Python 3.11+ and Git are sufficient. No Python packages are required.

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

For work, use a unique session and a task claim before substantive edits. Configure your public contributor identity as described in [MULTI_USER.md](docs/MULTI_USER.md). Never commit credentials or private runtime settings.

## What this foundation provides

- Capability-aware boot reports and handoffs for human, Codex, Claude, Gemini and other runtimes.
- Atomic task ownership with retained release history; isolated work branches and explicit integration.
- Immutable run bundles with copies of selected inputs, SHA-256 digests, outputs, commands and source state.
- Versioned source imports, candidate records, typed mathematical receipts and benchmark receipts.
- Integrity CI, adversarial artifact tests, and concurrent claim/release tests.

The framework is adapted from [UD-Physics](https://github.com/ud-tetra/UD-Physics/tree/e400dfb715262a44b3bbb2e929c7b438028af67e). [The adaptation record](docs/ADAPTATION.md) pins the source and explains the Lattix-specific changes. UD research remains a separate upstream lineage; no physics claim or historical benchmark is promoted by this bootstrap. GitHub Pages and the public marketing site are outside this repository bootstrap.
