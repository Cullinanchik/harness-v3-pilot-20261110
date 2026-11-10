# Harness v3 pilot
Only this synthetic repository and current task branch are in scope. Never inspect credentials or change host services.
The controller owns transitions, retries, approvals, publication and merge. Do not move tasks, approve work, push or merge.
Read the current request.json, BRIEF and request.role contract. A bootstrap without request must only reply `ок`.
Use current request.recovery and the installed report --recover/checkpoint commands when required; do not invent approvals.
Work/Fix run quick checks or targeted tests. The separate controller Verify runs the full suite after commit and settled native session.
Commit task-owned files before final quick check and scripts/pipeline-report; Review reads saved Verify evidence.
Respond in Russian. Do not create other tasks or agents. No external data/network is needed for the application.
