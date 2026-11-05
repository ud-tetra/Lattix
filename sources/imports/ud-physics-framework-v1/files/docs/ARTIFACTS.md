# Running documentation and artifact capture

## Repository layout

| Path | Contents and ownership |
| --- | --- |
| tasks/<task>.json | Scope, dependencies, owned paths; task owner |
| sessions/<session>/record.json | Runtime, task, base revision, claim, status and next action |
| sessions/<session>/journal.md | Concise running notes and corrections; one owner |
| candidates/<candidate>/candidate.json | Hypothesis, map, assumptions, fits, targets and result |
| artifacts/<session>/<run>/manifest.json | Immutable run metadata and file digests |
| artifacts/<session>/<run>/files/ | Intentionally captured outputs |
| artifacts/<session>/<run>/inputs/ | Explicit input copies in run schema version 2 |
| sources/imports/<snapshot>/ | Read-only source snapshots with provenance |
| state/CURRENT.md | Integrated milestone summary; integrator only |

Capture useful reasoning, decisions, and reproducible evidence. Do not save hidden reasoning traces, credentials, personal data, full private chats, or automatic environment dumps. Selected public research notes and user-authorized source files are appropriate.

## Mathematical receipts

Use [templates/mathematical_receipt.json](../templates/mathematical_receipt.json) for consequential calculations. Store the filled receipt in the owning candidate/session directory, link it from the journal/handoff/PR, and capture it with the calculation code and results. Preserve source versions, exact factor origins, assumed/fitted choices, clock/metric/normalization conventions and checks actually executed. Existing receipts remain historical; do not retrofit an earlier run to imply this method was followed. The receipt format is runtime guidance; current CI does not automatically validate its mathematics.

## Commands

```bash
python3 scripts/discovery.py note --session SESSION --text "FIT: selected the exponent using the exposed target; next test is sensitivity."
python3 scripts/discovery.py new-candidate --session SESSION --id CANDIDATE --question "What is the residual response?"
python3 scripts/discovery.py capture --session SESSION --run RUN --evidence NUMERICAL --summary "Toy-model spectrum" --command "python3 analysis.py" --input analysis.py --artifact results.json
python3 scripts/discovery.py checkpoint --session SESSION --status handoff --finding "Conditional result; calibration remains fitted." --next "Compare a held-out regime."
python3 scripts/validate.py
```

Commands record work; capture does not execute or validate the supplied command. Include the actual executed command and its result in your journal. A manifest digest checks bytes, not scientific correctness. Changed inputs require a new run.

New captures use run schema version 2. Each explicit input is copied into inputs/ with a unique ID, digest, size, original basename, and repository-relative source path when available. External source paths are omitted; the selected bytes and logical ID are retained. Same-named inputs remain distinct. Validation checks input metadata, captured bytes, containment, and unmanifested files as well as outputs. Explicit input copies share the 10 MiB per-file limit.

Existing run schema version 1 remains readable. Its input metadata is checked for structure and ambiguous basenames, but hashes without preserved input bytes cannot independently verify historical source contents. Preserve that limitation; do not rewrite old run manifests to imply they originally captured inputs. Relative links inside artifact payloads or imported sources are data, not repository navigation links.

Run directories are immutable after capture. Use a new run ID for corrections and record which earlier run it supersedes. Validation rejects modified captured outputs and version-2 inputs. No binary artifacts, private conversation archives, or bulk source collections are imported automatically.

Keep normal Git files small (prefer below 10 MiB per file). Use release assets or another explicitly configured large-file destination for larger research outputs, with a durable link, digest, and provenance manifest; GitHub Actions artifacts alone are not permanent archival storage.

## Manual/connector capture

Use templates/session.json, templates/candidate.json, and templates/run_manifest.json. Generate SHA-256 values with a capable runtime; leave unavailable verification as NOT_RUN in the session. Do not substitute a Git object SHA for a SHA-256 file digest. A partial draft manifest belongs in the session directory until complete; put only valid finalized runs under artifacts/.

At milestones, include links to the candidate, code, run, limitations, and next discriminant in the session handoff and PR. CURRENT.md links integrated milestones rather than every note.
