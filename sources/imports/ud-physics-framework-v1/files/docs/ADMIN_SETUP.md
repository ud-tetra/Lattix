# Administration and enforcement status

This repository includes runtime instructions, a cooperative task-claim protocol, issue/PR templates, and a validation workflow. File-based policy does not by itself enable server-enforced protections.

The GitHub connector used for initialization exposes repository content and Git operations but no administration-setting mutations. The following settings therefore require an administrator-capable interface and are not claimed as configured:

- Require pull requests on main and the passing check named "Discovery integrity".
- Disallow force pushes and deletion of main; preserve normal writes in discovery/* and claims/*.
- Require review according to available collaborators. A sole-owner repository should not require an unavailable reviewer or claim non-constructor review has happened.
- Use least-privilege per-runtime access where feasible. Never share personal access tokens through the repository.
- Confirm Actions is enabled; the workflow has contents: read and no write permissions. Untrusted PR code runs without repository write tokens.
- Optionally enforce a merge queue when there is enough integration traffic and the repository plan supports it.

Claims coordinate compliant clients only. A user with write access can ignore file policy; server permissions and branch rules are the enforcement boundary. Protecting main does not make a physical hypothesis true.

GitHub Pages is not enabled by this framework. GitHub's repository interface is the documentation destination requested here.
