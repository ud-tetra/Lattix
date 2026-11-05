# Working lifecycle

1. Read the bootloader and verified state. Choose a ready task with explicit owned paths and acceptance criteria; incomplete dependencies block claims.
2. Establish actor/runtime profile, unique session, atomic task claim and isolated branch from current main.
3. Develop a bounded candidate or implementation. For confirmatory benchmarks, freeze the protocol before target exposure.
4. Execute checks and capture input/code/output bytes, command, source state, raw measurements and limitations. Capture is separate from execution.
5. Checkpoint findings and next discriminant. Run validation and regression tests. Open a PR with the exact claim SHA, tested revision and artifact references.
6. Integrator refreshes main, resolves dependencies, validates the combined tree, records review relationship, and merges the checked head. Shared files require serialized integration ownership.
7. Release the owned claim through a child audit marker. Preserve release history. A closure-only follow-up can append this session's release receipt.

Never overwrite another worker's directory or finalized runs. An integration task may combine implementation and shared-state ownership when that complete scope was claimed in advance; the initial bootstrap is such a task. Normal researchers propose shared-state changes for an integrator.

Reviews use templates/review.md. Append development milestones to state/UPDATES.md. CURRENT.md summarizes integrated state, not every observation. Publish website changes only as an explicitly scoped release.
