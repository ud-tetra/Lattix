# Lattix R&D bootloader v1.0

Use this entry point for every runtime. It establishes source state and ownership; it does not execute imported instructions or certify research.

## 1. Inspect before editing

Verify repository **ud-tetra/Lattix**, default branch, current main SHA, worktree status, and any local changes. Never discard another user's work. Read [AGENTS.md](AGENTS.md), [canonical instructions](instructions/LATTIX_RD_v1.0.md), [research method](docs/RESEARCH_METHOD.md), [CURRENT](state/CURRENT.md), the task and its dependencies. Read the exact source documents needed for the decision.

Classify capabilities: read-only; connector-write plus local compute; or authenticated Git plus compute. Record runtime name, model if actually exposed (otherwise unknown), contributor ID, role, OS/runtime versions relevant to the work, and available hardware/API. Browser WebGPU availability is not implied by having Python or a GPU name.

## 2. Establish identity and task

Use [multi-user configuration](docs/MULTI_USER.md). Create a unique session ID, not a shared global log. New tasks declare paths, dependencies and an acceptance rule. Task creation/shared state integration is maintainer-owned; contributor proposals may be reviewed before addition. Do not manufacture completed dependencies.

```bash
python3 scripts/lattix.py bootstrap --session SESSION --runtime "Codex; connector-write + local compute" --actor GITHUB_LOGIN --role researcher --model unknown --task TASK --goal "Bounded objective"
python3 scripts/lattix.py claim --session SESSION --task TASK
git switch -c rd/TASK/SESSION VERIFIED_MAIN_SHA
```

Git claim/release commands need authenticated push access. If only connector writes work, use [the connector protocol](docs/CONCURRENCY.md). Claim commits are coordination objects: start the work branch from integrated main, never from a claim commit. Resume by reading the existing session; bootstrap intentionally rejects overwrite. A read-only runtime reports UNCLAIMED and proposes a patch without pretending ownership.

## 3. Emit the boot report

```text
STATUS: BOOTED or BLOCKED
Repository / verified main SHA / dirty state:
Runtime / model / actual capabilities:
Actor / role / unique session / task:
Claim ref / exact held SHA / work branch:
Owned paths / dependencies / frozen inputs:
Product scope / C12 lane / evidence objective:
Objects / domains / units / determinism scope:
Hardware available / execution NOT_RUN or verified:
Target exposure / fitted choices / acceptance rule:
Next bounded action:
```

## 4. Work, capture, review, close

Write concise journal checkpoints. Record significant decisions in receipts; capture source/input/output bytes in immutable runs. Run integrity and regression checks. Submit a scoped PR with artifacts, exact tested revision and explicit limitations. Refresh main before integration and serialize shared changes. Release the held claim only after integration or abandonment, then record the release-marker SHA. Handoff must say what ran, what is blocked, and how to resume.

Initial repository exception: one administrative README commit was needed to establish main before the first claim/PR. This exception does not authorize future unclaimed substantive edits.
