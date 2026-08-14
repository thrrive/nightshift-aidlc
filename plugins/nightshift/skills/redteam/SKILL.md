---
name: redteam
description: "frame subskill. Runs an evidence-backed adversarial review of the blueprint and plan before human approval, then rewinds material gaps or holds incomplete evidence."
---

# /redteam — break the plan before it ships

Review the exact blueprint and plan as a skeptical second perspective. Assume an important claim is
wrong and try to demonstrate where it fails. A clean result is a structured decision supported by
inspection, not the absence of an obvious objection.

Read and follow [`references/review-protocol.md`](references/review-protocol.md). Use the shared
[`review contract`](../../docs/review-contract.md) for proof states, findings, remediation, and
decision rules.

## Process

1. Pin the blueprint and plan artifacts being reviewed. If they are missing or moving, return a
   `CONDITIONAL` record with `needs_human` rather than reviewing an inferred subject.
2. Extract the core claims that must hold for the plan to satisfy `mission.done_when`. Name each
   claim's boundary and required proof; do not treat plan prose as its own evidence.
3. Run the five independent lenses in the protocol. Use fresh context or reviewer fan-out when the
   host supports it, but never claim independence that did not occur.
4. Record evidence-bound findings with stable IDs. A vague concern is not a finding; cite the
   artifact, repository fact, invariant, or failure scenario that makes it actionable.
5. Route every material finding to the earliest artifact that can resolve it. Re-run all affected
   lenses after remediation and retain the finding history.
6. Persist the complete review record as `redteam-review.json` in `frame`'s durable bundle. Missing,
   malformed, partial, all-error, or scratch-only output is an evidence hold, never a clean pass.

## Routing

- `PASS` → return `advance`; `frame` may present the plan for human approval.
- `REQUEST_CHANGES` → return `rewind` to `blueprint` for design/boundary failures or `plan` for
  sequencing, scope, rollout, or proof gaps.
- `CONDITIONAL` → return `needs_human` with the missing evidence or accepted residual stated
  precisely.

In YOLO mode, a bounded `REQUEST_CHANGES` finding may automatically re-enter the owning frame
subskill and rerun this review. Escalate instead when the remediation changes mission scope,
done-when conditions, safety or policy posture, or the recovery budget is exhausted.

A plan review may have a `STATIC_ONLY` proof ceiling: it establishes that the plan is coherent and
evidence-aware, not that unbuilt behavior already works. Never promote a future behavior claim to
`PROVEN`.
