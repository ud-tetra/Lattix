# UD Physics — What-if Discovery

A separate Unified Dynamics research sandbox for hypothetical bridge candidates and correlations to physical spacetime. Target-informed fitting, analogy, and speculative physical maps are permitted; assumptions and evidence remain explicit.

## Start any LLM session here

Read [BOOTLOADER.md](BOOTLOADER.md), then [AGENTS.md](AGENTS.md) and the [Discovery instructions](instructions/UD_DISCOVERY_v1.2.md). Also load the [UD mathematical analysis protocol](docs/UD_MATHEMATICAL_METHOD_v1.0.md). Do not begin from remembered project state.

Copy this into a new runtime:

> Work in https://github.com/ud-tetra/UD-Physics. Read BOOTLOADER.md and follow its load order, including the UD mathematical analysis protocol. Report the repository revision, access capabilities, task, session ID, and evidence mode. Use the Discovery sandbox rules. Claim the task before editing, use an isolated branch/worktree, capture calculations and artifacts, and leave a reproducible handoff. Read-only access permits analysis but does not establish a write claim.

## Working routes

| Need | Start here |
| --- | --- |
| UD mathematical techniques and exactness | [docs/UD_MATHEMATICAL_METHOD_v1.0.md](docs/UD_MATHEMATICAL_METHOD_v1.0.md) |
| Calculation provenance receipt | [templates/mathematical_receipt.json](templates/mathematical_receipt.json) |
| Current integrated state | [state/CURRENT.md](state/CURRENT.md) |
| Simultaneous LLM sessions | [docs/CONCURRENCY.md](docs/CONCURRENCY.md) |
| Research workflow | [docs/WORKFLOW.md](docs/WORKFLOW.md) |
| Running documentation and artifact capture | [docs/ARTIFACTS.md](docs/ARTIFACTS.md) |
| Source imports and mainline boundary | [docs/SOURCES.md](docs/SOURCES.md) |
| Hosting and enforcement limitations | [docs/ADMIN_SETUP.md](docs/ADMIN_SETUP.md) |
| Sessions and handoffs | [sessions/README.md](sessions/README.md) |
| Research candidates | [candidates/README.md](candidates/README.md) |
| Tasks | [tasks/README.md](tasks/README.md) |
| Reusable templates | [templates](templates) |

## Runtime tools

Python 3.11+ and Git; no Python packages are required.

```bash
python3 scripts/discovery.py bootstrap --runtime "runtime/model as reported" --task setup-review --goal "Review repository readiness"
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The first command prints a unique session ID and creates its running record. Use that ID with `note`, `capture`, and `checkpoint`; see `python3 scripts/discovery.py --help`.

One held task claim has one owner; released audit markers permit exact-SHA reacquisition. Separate runtimes use separate branches. Per-session records avoid a shared append-only log. Pull requests integrate work; the default branch is the integrated snapshot. Claims are cooperative coordination, with atomic Git ref acquisition, not access-control permissions.

## Evidence boundary

EXACT mathematics remains scoped to its model. FIT does not become an independent derivation. Physical observations and hypothetical identifications remain distinct. Nothing in this repository automatically promotes a claim or writes to mainline UD.

This GitHub repository is the documentation and artifact destination. A separate GitHub Pages website has not been configured.
