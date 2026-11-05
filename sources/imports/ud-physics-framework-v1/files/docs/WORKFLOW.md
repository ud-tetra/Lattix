# Discovery workflow

1. Boot and claim a scoped task. Record source revision and target exposure.
2. Create a candidate record. State the question, objects, assumed map, fitted choices, and possible discriminating observable.
3. Apply the [UD mathematical analysis protocol](UD_MATHEMATICAL_METHOD_v1.0.md): select techniques by purpose, define typed domains and conventions, and preserve exact expressions/provenance. Create a mathematical receipt for consequential results. Build the smallest useful model. Keep conventional baselines and alternative explanations visible.
4. Record calculations, code, inputs, exclusions, residuals, and negative results. Use FIT for target-informed selection even if the selected arithmetic is exact.
5. Capture a run with source revision, command, explicit inputs, outputs, and SHA-256 digests. Uncommitted source is allowed in discovery, but the manifest must report a dirty source tree. Commit source before a confirmatory run.
6. Update only the owning session journal and candidate. Check dependencies after revisions. Maintain corrections as new entries/runs rather than rewriting a failed result away.
7. Run integrity checks and tooling tests, checkpoint, and open a focused PR. Make the result understandable without reading the chat.
8. Integrate at a milestone, update CURRENT.md under the integration claim, and release task ownership.

Candidate lifecycle: HYPOTHESIS → ACTIVE → PARKED / FAILED / EXPORT_CANDIDATE. These are workflow states, not confidence levels or mainline registry rungs.

A later evaluation on genuinely unused evidence may support an independent prediction. Historical target exposure remains part of provenance. Mainline transfer requires explicit user authorization and a fresh assessment under accepted mainline rules.
