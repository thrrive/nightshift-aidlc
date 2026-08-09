---
name: plan
description: "frame subskill. Synthesizes a human-approvable implementation plan and definition of done from investigation and blueprint outputs. The plan is what the human approves before any code is written."
---

# /plan — synthesize the implementation plan

Produce the document a human approves before implementation starts. Read and follow
[`references/plan-template.md`](references/plan-template.md). If invoked standalone without
investigation/blueprint context, run `investigate` and `blueprint` first, or ask for the smallest
missing input.

## Rules

- Describe **behavior and components**, not exact file edits or function signatures.
- Default to **one PR per goal**. Split only for a multi-step release, dependency ordering,
  atomic-rollout risk, or an explicit user request — and say why.
- Make **Verification** concrete: choose browser, API, CLI, library, or a justified custom shape and
  state the observable result that proves the change. This is the contract `verify` checks; prefer
  repo-owned checks and specs.
- Carry forward the mission's `done_state`, the rollout path, the approval gate, and any
  observability needs so `land` can later confirm the requested state was actually reached. If
  the user didn't ask for something narrower, plan for **stable production**.
- Don't pre-bless gratuitous docs, comments, or unrelated refactors.
- When the implementation genuinely decomposes into **independent, file-disjoint work items**
  (separate components, no shared files), the plan **may** declare them as `workstreams` in the
  handoff so the build fans out to parallel sub-agents — see the contract in
  [`docs/handoff-contract.md`](../../docs/handoff-contract.md): explicit path ownership
  (component-wise disjoint, validated), ordered merge, at most 8 items, one PR regardless.
  Decompose only when the boundaries are real; a plan that would make two streams touch the
  same file (shared types, lockfiles, a common index) belongs to a single agent. Default is
  no decomposition.

Write to the target's feature-docs path when it has one; otherwise return the plan inline.
Return `advance` to `redteam` when complete.
