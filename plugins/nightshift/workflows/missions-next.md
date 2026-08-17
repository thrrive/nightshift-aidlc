---
name: nightshift-missions-next
description: "Start exactly one dependency-ready subtask for an approved durable mission."
entry_skill: /nightshift:missions
capability: mission_registry.next_subtask
state: subtask_workflow
---

# Next-subtask workflow

Accept an immutable `mission_id` and call the host's `mission_registry.next_subtask` capability.
The host must:

1. Resolve the mission to its durable job and verify the mission identity.
2. Confirm the persisted subtask workflow is at `ready` or `awaiting_approval`.
3. Select exactly one pending child whose dependencies are complete.
4. Persist the child transition atomically and return its ID, goal, dependencies, and mission state.

Return `needs_human` or `stuck` without mutation when the plan is missing, a child is already
running, dependencies are blocked, the mission is complete, or the host capability is unavailable.
This action never bypasses plan approval, verification, review, merge, or release gates. In YOLO
mode, a successful child summary may trigger the same action automatically, subject to the
mission's recovery and human-escalation policy.
