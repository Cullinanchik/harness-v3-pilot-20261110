---
name: verify-project
description: Run quick lint, typecheck or build checks during Work or Fix; full tests belong to the controller's separate Verify stage.
---

Read `.agent/project.json`. During Work/Fix run only `quick_checks` (lint, typecheck or build).
Run `scripts/agent-check --phase quick --output .agent/runtime/<task-id>/agent-check` from the Git root.
If no quick checks exist, report that fact; never fall back to the full `checks` list.
When needed for development, run only tests scoped to changed files or specific test names.
Record the exact selection and result; do not call targeted tests a passing full suite.
Never run a full suite during Work, Fix, Spec, Design, Review, approvals or deployment.
Inspect result.json and concise failure summaries; open only relevant log slices.
For an existing quick result run `scripts/agent-check --phase quick --validate <result.json>`.
Do not claim success for missing commands, timeout, changed source, or nonzero exit codes.
Any subsequent source/index/HEAD/policy change requires fresh quick checks and handoff.
Commit task-owned source/docs on the task branch before the final check; do not commit
runtime files or unrelated work. Do not merge to main or deploy.
After development is committed, the handoff is valid and the native session settles, the
controller moves the card to the separate Verify column and runs the mandatory full `checks`.
Success admits Review; failure returns to Fix, followed by Verify. Review consumes the saved
result, and source/policy changes require Verify again. Quick/targeted evidence never admits review.
Manual maintenance uses an explicitly announced Verify phase and `scripts/agent-check --phase verify`
only after development is finished. Installation validates and reuses its exact committed result.
