# Concurrent runtime protocol v2.0

## Scope and migration

Version 2 retains atomic task ownership and adds released markers, so connector-only runtimes can complete a lifecycle without branch-deletion access. The original [v1.0 protocol](CONCURRENCY_v1.0.md) is preserved. Missing status in a legacy claim means held. No prior failed deletion is retroactively called successful.

Each runtime has its own session ID, branch and isolated checkout/worktree. Use discovery/<task>/<session>. Different tasks may run together only on disjoint owned paths. Existing candidates and shared files have one task owner; overlapping work uses the same task key or per-session proposals for an integrator.

Atomic acquisition protects one task ID, not arbitrary overlapping paths across different IDs. Scope planning remains required. Claims are cooperative coordination, not access-control permissions.

## Live state and audit chain

A coordination ref refs/heads/claims/<task> points to a commit containing claim.json. Fields include schema_version: 1, protocol_version: 2, task, session, status (held or released), created_at, base_revision, and owned_paths. Legacy claims without protocol_version/status remain held.

Read the exact live SHA and claim metadata. A ref's existence alone does not mean it is held. Never treat a session's local status as the live lock state. There is no automatic expiry or timestamp-based takeover.

## Acquisition

If the ref is absent, create a held claim commit and create the new ref atomically. Git uses an explicit empty expected-ref lease; the connector uses create_branch. Existing refs reject that operation.

If the ref points to a released marker, create a new held claim commit whose parent is that exact marker. Include previous_claim_sha. Update the ref with expected_sha equal to the marker and force=false. Git uses the same exact-SHA lease. Competing updates cannot both win. A held claim may not be reacquired or overwritten, including by another session on the same account.

Connector sequence: read live ref and claim.json; verify absence or released status; create a tree containing the proposed claim.json; create the claim commit (parent=marker when reacquiring, otherwise verified base); create the absent branch or update the released ref using an exact expected SHA. Save the returned claim SHA in the session. Work branches start from integrated main, never from the claim metadata commit.

## Release without deletion

After integration or explicit abandonment, the owning session reads its exact held claim. Create a child commit of that held SHA with the same task/session/owned paths and status=released, protocol_version=2, released_at, and released_from_sha. Update the coordination ref with expected_sha equal to the held SHA and force=false. Verify the live marker and metadata before recording success.

A stale SHA, wrong owner, already-released claim, or changed live ref rejects release. The ref and its history remain as an audit chain; a released marker is available for future atomic reacquisition. Physical deletion is neither required nor claimed. Git-only conditional deletion remains a legacy operation, not the normal protocol.

Git-capable authenticated runtimes can use scripts/discovery.py claim/release. Runtimes with GitHub connector write access but no Git push credentials use the connector sequence above. Do not hunt for credentials or weaken protections to make Git push succeed.

Release necessarily writes final session ownership metadata after changing the live ref. A closure-only follow-up may commit that session's release evidence and handoff without reacquiring the completed task; it may not change substantive research, shared state, or another session's files.

## Integration and handoff

Use focused PRs. Integrators claim integration-<scope> and serialize shared task/state/instruction/tooling changes. Merge current main into work branches, rerun checks, resolve conflicts explicitly, and never overwrite a newer head from a stale API snapshot. Use exact-head checks for API publication and merging.

Keep session journals and immutable per-run artifacts separate. CURRENT.md is an integrated milestone summary, not a realtime lock table. Constructor checks, separate-context LLM review, non-constructor review and independent empirical replication remain distinct.

Read-only runtimes may inspect, calculate privately and propose patches but do not claim write ownership. If access rules block a coordination update, record the blocker and continue only independent work. File policy does not substitute for server protections.
