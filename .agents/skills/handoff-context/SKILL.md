---
name: handoff-context
description: Persist compact run-bound context at the end of an enrolled Development Pipeline role or at an explicitly requested supported checkpoint. Excludes service reports and automatic session rotation.
---

Require a current runtime request and the matching task, role and run. This skill
does not enroll service work or create a missing runtime request.
Use `scripts/pipeline-report --task <task-id>` (Review and Debate also need --clean/--findings).
It records task, stage, run/session identity, SPEC digest, base, HEAD and working diff digest.
Use `--remaining` only for unfinished work in the current stage, never for open product
questions or a missing task brief; either would incorrectly block the handoff. Do not
fake readiness or weaken the gate. Include check result links with --checks and known live
processes with --process. Commit task-owned source/docs on the task branch before the final
quick check/handoff unless there are no source changes. Full tests belong only to the separate
controller-owned Verify stage; never launch them to prepare an agent handoff. Stop owned background work before declaring
a role ready.
Only when the current controller explicitly requests a checkpoint supported by this
run, finish the current tool call and use `--checkpoint --progress "completed item"`
with actual `--remaining "unfinished item"` or `--process "owned live process"`.
Without unfinished work or a live process, finalize normally; the CLI rejects an
empty checkpoint. Writing checkpoint.json alone does not prove that this protocol
supports session rotation. Never start a replacement session or reset the fix budget.

Keep a bounded continuation note in the current role's permitted output: completed
items with evidence paths and HEAD/run identity, decision references, actual remaining
work and the next action. Preserve pointers to request.context and owner_answers;
the note cannot replace frozen inputs, approvals or saved Verify evidence. Read the
evidence on resume if a note conflicts with it. Do not edit frozen SPEC/PLAN in Review
or Debate, create a parallel memory store or repeat the whole chat.
Before handoff, check that a reader can locate the governing decision, identify the
verified version, distinguish finished from pending work and find the next action.
On resume, load only the current request's role skills and needed artifacts, never
the next stage's skills, all logs or the whole library.
20–40k relevant input tokens is a soft guide; hard compaction remains enabled.
Record cache-hit claims only when actual runtime metrics are supplied.
