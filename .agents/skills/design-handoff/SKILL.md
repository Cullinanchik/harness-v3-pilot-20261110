---
name: design-handoff
description: Describe or validate a required private Claude Design export at the controller-owned Design boundary. Excludes ordinary UI implementation, owner approval and replacement HTML prototypes.
---

A design-required task pauses at the **Design** stage until a complete local export exists.
Do not continue to coding and never substitute ordinary HTML generation for Claude Design.

The Spec role already wrote the decision in `.agent/tasks/<task-id>/design.json` and
`DESIGN.md`. The target workflow is automatic generation/export by the verified Claude
Design interactive CLI/PTY adapter on the Design stage; the pipeline only consumes the
resulting private local bundle. Determine availability and export authorization from
the current controller request/status. This skill does not establish login, adapter
verification or enablement and cannot authorize a launch. If the required adapter or
authorized export is unavailable, report that fact; the controller owns the pause.
Do not ask the owner to copy files, use DesignSync `create_project` or ordinary HTML as a
substitute. The verifier below exists for the adapter's output, not as a user workflow.

After a real authorized export, put a private bundle under `.agent/tasks/<task-id>/design/`.
`design-export.json` must contain the real project identity and revision:

```json
{
  "schema": "claude-design-export/v1",
  "project": {
    "id": "private project id",
    "uri": "https://claude.ai/design/p/project-id",
    "revision": "exact export revision"
  },
  "visibility": "private",
  "files": ["index.html", "assets/app.css"],
  "preview": "preview.png"
}
```

The verified adapter writes the bundle and the controller runs the digest verifier. For
adapter development only, the same check can be run as:

```sh
python3 -m dev_pipeline.design_artifact .agent/tasks/<task-id>/design
python3 -m dev_pipeline.design_artifact --verify .agent/tasks/<task-id>/design
```

The mutable project URL alone is not evidence. The owner approves a digest over the
project id, exact revision and every local file/preview digest. A changed revision,
export or preview invalidates design approval, checks, review and acceptance. Never
read or copy credentials, cookies or tokens; keep artifacts private and out of public
sharing. This is a local consumer boundary, not a fabricated Design HTTP API.
