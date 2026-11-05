# Multi-user and runtime configuration

## Identities and roles

[config/contributors.json](../config/contributors.json) is the public roster. Each contributor has a unique ID (normally their GitHub login), GitHub identity and allowed roles. Bootstrap currently registers the repository owner only. Add real collaborators by PR; GitHub repository access must be granted separately by an administrator. Never invent users or put tokens in the roster.

| Role | Responsibility |
| --- | --- |
| maintainer | Policy, task creation, contributor registry and source amendments |
| researcher | Scoped implementations, candidates, experiments and evidence |
| reviewer | Declared-scope review; identify relationship to constructor |
| integrator | Dependency reconciliation, checks, shared state and release |

A person may hold several roles. A role label does not grant GitHub permissions or create independent review. The CLI validates the declared identity/role against the roster; it cannot authenticate the human behind a command. Claims coordinate compliant users, not malicious writers.

## Configure a runtime

Copy [runtime.local.example.json](../config/runtime.local.example.json) to config/runtime.local.json (ignored by Git), edit actor/role/model, and invoke bootstrap without --actor. Alternatively pass --actor and --role explicitly. Do not put secrets in either file. If model identity is not exposed, use unknown. Every boot records the profile snapshot for audit.

```bash
cp config/runtime.local.example.json config/runtime.local.json
python3 scripts/lattix.py bootstrap --runtime "human + Python" --task TASK --goal "Declared objective" --session UNIQUE_SESSION
```

For simultaneous workers use separate clones or worktrees, unique session IDs, branches rd/<task>/<session>, and disjoint task scopes. Check every held remote claim before choosing a task. Distinct task names do not protect overlapping paths. Shared tooling, roster, instruction or state changes require an integration task rather than concurrent edits.

## Resume and handoff

Do not call bootstrap on an existing session. Read its record and journal, verify current actor and live claim SHA, inspect the current work branch, and run the required checks. If a different person takes over, the prior owner releases or abandons, the next person creates a new session and atomically acquires the released marker. No time-based takeover is implemented.

Checkpoint with status handoff or blocked and name the precise missing dependency. Release only after integration or explicit abandonment. A maintainer-assisted exceptional recovery must preserve the old SHA and an incident record; never quietly replace a held claim.
