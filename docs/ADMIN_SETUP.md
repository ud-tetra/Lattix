# Administration and enforcement status

The repository installs instructions, cooperative claims, contributor profiles, issue/PR templates and a read-only CI workflow. These files do not enable GitHub branch protection, invite collaborators or grant access.

At bootstrap, the GitHub rulesets endpoint returned an empty list. Classic branch-protection settings were not verified. Administration-setting mutations are not exposed by the connected content/Git interface, so the settings below remain **ADMIN_ACTION_REQUIRED**, not configured claims.

- Require PRs on main and the passing check **Lattix integrity**. Disallow force pushes and branch deletion on main.
- Require reviews appropriate to actual collaborators. Do not require an unavailable independent reviewer in a sole-owner repository or label constructor review independent.
- Preserve normal creation and fast-forward updates under rd/* and claims/*; coordination uses exact-SHA leases. Do not apply rules that make release markers impossible.
- Grant individual least-privilege repository access separately from config/contributors.json. Never share personal tokens in the repository or local profile.
- Confirm Actions is enabled. The workflow uses contents: read, pinned checkout and persist-credentials: false; no pull_request_target execution of untrusted code.
- Review CODEOWNERS and the contributor roster together. CODEOWNERS requests review only when server settings and eligible accounts support it; it is not access control.
- Optional merge queue and signing requirements depend on available collaborators and repository plan. Record policy changes as amendments.

Claims protect compliant competing clients at a task key. A repository writer can bypass file policy. A digest detects changed bytes relative to a manifest; it is not cryptographic authorship, hardware attestation or immutable external storage. Git history itself remains subject to administrator powers.

GitHub Pages, web deployment, package publication, secret stores and large artifact hosting are not configured by this bootstrap.
