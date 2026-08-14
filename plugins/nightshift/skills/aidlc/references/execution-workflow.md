# Execution workflow: recovery, YOLO, and parallel work

The execution policy is host-neutral. Codex and Claude adapters may use different task or
subagent APIs, but they must preserve the same mission state, review routing, retry budgets, and
evidence.

## Policy block

When a host supports hierarchical execution, the frame handoff may carry this additive block:

```yaml
execution:
  mode: gated | yolo
  recovery:
    max_per_finding: 2
    max_per_subtask: 3
    max_per_mission: 8
  human_escalation:
    - meaningful_scope_diversion
    - safety_or_policy_decision
    - unresolved_redteam_finding
    - unresolved_code_review_finding
    - blocked_or_ambiguous_execution
```

Defaults are bounded and may be lowered by the target. A host must not raise them silently. Every
retry increments a durable loop counter and records the finding, route, attempt, and result.

## Normal routing

Classify each finding before selecting a route:

| Finding | Automatic route | Escalate when |
| --- | --- | --- |
| In-scope implementation defect | `self-review → implement` | retry budget is exhausted |
| Red-team design gap | `redteam → blueprint` | the fix changes the mission or accepted risk |
| Red-team sequencing/proof gap | `redteam → plan` | requirements or done-when conditions change |
| Actionable code-review defect | `pr-drive → build` | it is disputed, out of scope, or budget is exhausted |
| Verification failure caused by the change | `verify → build` | root cause is external or unclear |
| Scope, safety, policy, credential, or merge decision | `needs_human` | always |

The loop returns to the earliest phase that can resolve the finding. It does not open a second
mission or a second PR. The original finding remains in the evidence ledger, linked to its
remediation and follow-up review.

## YOLO semantics

`mode: yolo` removes routine pauses only. It may automatically approve the parent plan, advance
eligible children, accept a clean review result, and continue a bounded recovery route. It must
surface the mission when a human decision is meaningful: scope diversion, safety or policy,
unresolved red-team or code-review findings, blocked execution, or an exhausted retry budget.

Merge and release actions still obey the target's advertised authorization policy. A host may
automate them only when that policy explicitly authorizes automatic delivery; otherwise the
authorization itself is a meaningful human decision.

## Parallel workstreams

If the approved frame handoff contains validated, path-disjoint `workstreams`, `build` may fan them
out to one host subagent/task per item. Each workstream gets an isolated workspace, branch, event
lane, and usage ledger. The host must enforce a concurrency limit and may run fewer streams than
requested.

1. Validate ownership and dependencies before fan-out.
2. Start all currently eligible workstreams through the host's subagent/task capability.
3. Join at the completion barrier; a failed or blocked stream prevents the join from passing.
4. Merge successful branches in declared item order with `--no-ff` or the host equivalent.
5. Treat a merge conflict as a finding and route to `implement` or `needs_human` according to scope.
6. Run self-review and verification on the merged result, never on individual branches alone.
7. Aggregate per-stream summaries and usage into the one mission and one PR.

If the host lacks a subagent/task capability, execute the same workstreams sequentially and record
that parallelism was unavailable. Do not silently run concurrent writers without isolated paths.

## State required for resume

Persist at least:

```yaml
execution_state:
  loop_iteration: 0
  recovery_attempts: {finding-id: 0}
  active_workstreams: []
  completed_workstreams: []
  join_status: pending | ready | blocked
  last_route: <phase and step>
```

Resume by the immutable mission/bundle reference and this state. Never infer a retry, completed
stream, or join result from chat history.
