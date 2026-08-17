---
name: nightshift-aidlc
description: "Run one Nightshift mission from intake through frame, build, land, and completion."
entry_skill: /nightshift:aidlc
state: execution_state
---

# AIDLC workflow

Run exactly one mission through these ordered stages:

1. Load the routing, execution-workflow, handoff, and host-capability contracts.
2. Resolve or create the durable mission and bundle before investigation.
3. Run `intake`, then `frame` (`investigate → blueprint → plan → redteam`).
4. Stop at the plan-approval gate unless the mission is explicitly YOLO or frame-only.
5. Run `build` (`implement → self-review → verify`) against the approved plan.
6. Run `land` (`pr-drive → verify → release-gate`) until the requested done state is proven.
7. Return the canonical handoff and refresh durable mission evidence.

## Deterministic routing

Use the first phase that can resolve a finding. Red-team design gaps route to `blueprint`; proof
or sequencing gaps route to `plan`; implementation defects route from `self-review` to `implement`;
behavior failures route from `verify` to `build`; delivery findings route from `pr-drive` to `build`.
Scope, safety, policy, credential, merge, blocked, malformed, conditional, or exhausted findings
return `needs_human`.

Apply these defaults unless the target lowers them:

```yaml
recovery:
  max_per_finding: 2
  max_per_subtask: 3
  max_per_mission: 8
```

Every retry records the finding ID, route, attempt, result, and immutable mission/bundle reference.
Never infer a retry or completed step from conversation history.

## YOLO and joins

YOLO removes routine approval pauses only. It does not bypass meaningful human decisions or merge
and release authorization. For validated path-disjoint workstreams, start one isolated lane per
eligible stream, join all lanes, merge in declared order, then self-review and verify the merged
result. If parallel host capability is unavailable, run the same streams sequentially and record
that degradation.

## Adapter result

Persist `execution_state` with `loop_iteration`, `recovery_attempts`,
`active_workstreams`, `completed_workstreams`, `join_status`, and `last_route`. Return only the
canonical `mission`, `outcome`, and conditional routing fields defined by the handoff contract.
