---
name: missions
description: "Inspect durable Nightshift missions and explicitly start the next eligible subtask when the user wants to progress a mission."
---

# /missions — inspect and progress durable work

Use this skill to discover durable Nightshift missions and their nested subtasks. When the user
explicitly asks to start or proceed to the next subtask, use the host's mission action rather than
changing bundle files.

## Inspect

Prefer the host's mission-registry or mission-observation capability. Show the mission ID, target,
status, parent and child relationships, current gate, and durable bundle path. Include the mission
start time, elapsed wall time, current stage, model calls, input/output tokens, attempt and retry
counts, and known API-equivalent cost when the event ledger provides them. Report unavailable
metrics explicitly. Do not infer live state from conversation history, temporary logs, or filename
patterns alone.

## Start the next subtask

For an explicit request to proceed, invoke this skill with the mission ID:

```text
/nightshift:missions <mission-id> --next
```

The action resolves the mission to its running job, verifies that the persisted workflow is at an
approval gate, starts exactly one eligible child, persists the transition, and returns the new
subtask plus the current mission summary. It refuses when the plan is missing, a child is already
running, dependencies are blocked, or the mission is complete. It never bypasses plan approval,
verification, review, merge, or release gates. In `mode: yolo`, child completion may auto-advance;
this explicit action remains useful for a gated mission or a paused/resumed operator session.

Do not edit mission artifacts directly and do not infer a subtask from conversation history.

## Output

Keep inspection and progression results concise. Include the selected subtask, its dependencies,
the new mission/job state, execution metrics, and any refusal or unavailable host capability. For a
parent with children, include per-child timing and usage when available.
