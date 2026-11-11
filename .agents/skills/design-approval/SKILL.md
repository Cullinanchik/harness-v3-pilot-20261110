---
name: design-approval
description: Consume a required, approved local Claude Design export in an enrolled Work, Fix or Review run. Excludes generating designs, granting approval and tasks without a design requirement.
---

Require a current Work, Fix or Review request; this is a consumer, not an owner
approval action. Read `request.design`. When `required` is true, require `approved_spec` and a human
design approval bound to the current `design_digest`; placement or an agent message
cannot grant it. Use only the local exported files under `.agent/tasks/<task-id>/design/`
and the approved components/tokens recorded in `DESIGN.md`. Never call Claude Design,
copy credentials or change the design decision from an implementation or review session.

Routine UI fixes reuse approved project components and tokens; do not request a new
design run for every small change. Report a changed design revision/export so the
controller can return to Design or Design Approval; never move the card yourself.
In Review, a targeted visual comparison is optional
only when a real exported preview exists; do not install or launch a large browser
stack for backend-only tasks.
