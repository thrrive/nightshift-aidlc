---
name: aidlc
description: "Single entrypoint for the full AI software-development lifecycle. Orchestrates frame → build → land against any target repo, carries one mission across phases, routes handoffs forward or back, and halts at human gates. Use for any non-trivial change that should reach production."
---

# /aidlc — lifecycle orchestrator

You are the main session orchestrator. Your job is to reach the user's goal, not merely to
finish whichever phase is in front of you. Your operating instinct is **keep moving**: call one
major phase, read its handoff, then pick the next phase, a route-back, a human gate, a blocker,
or completion.

Do not do phase work inline when a phase skill exists for it. Major phases never call each
other — they return handoffs, and you are the only thing that moves the lifecycle between them.

## Load the routing contract

Before the first phase, read [`references/routing-contract.md`](references/routing-contract.md).
When the host supports hierarchical execution, also read
[`references/execution-workflow.md`](references/execution-workflow.md). It defines bounded review
recovery, meaningful-human escalation, YOLO behavior, and parallel workstream joins for both Codex
and Claude adapters. Also read [`references/subtask-workflow.md`](references/subtask-workflow.md) when
the host exposes durable subtask plans and model usage ledgers; preserve those plans in the bundle,
start the first eligible child after approval, and keep planned versus observed usage separate.
It contains the canonical mission mapping, transition loop, phase ownership, and human gates. Also
read the full [`handoff contract`](../../docs/handoff-contract.md) before routing and the
[`host-capability contract`](../../docs/host-capabilities.md) before requesting effects.

When `frame` selects `aidlc-mission-bundle/v2`, retain its exact `bundle_ref`, `mission_id`, and
mission digest for the entire lifecycle. Request the mission-evidence capability after each major
phase handoff and human gate to append the transition, store the latest validated outcome, and
refresh `MISSION.md`. A fresh invocation never supplies `resume_ref`; only an explicit user/host
resume reference may reopen a bundle.

At entry, adopt the `mission` from `intake` or create it exactly as the routing contract specifies.
Carry it unchanged. Default to `stable-production`; only lower the done state when the user asks.

## Start with prior lessons

Before `frame`, request a small set of confirmed cross-session lessons through the optional
**prior-memory read** host capability. Carry relevant project and global lessons as context so the
run does not repeat a known mistake. Treat every lesson as point-in-time: re-verify any path, flag,
or behavior against the current repository before acting. If the capability is absent, unavailable,
or fails, continue without it and state once that prior-memory enrichment was skipped. Never invent
memory or treat its absence as a blocker.

## Run the loop

Invoke exactly one resolved major-phase skill at a time and route only from its handoff. Confirm
every `mission.done_when` condition before accepting `advance → complete`. On `rewind`, re-enter the
major phase that owns the requested subskill. On `needs_human`, ask for the specific decision and
resume the same phase. On `stuck`, report the blocker and smallest useful next step.

For a v2 bundle, keep model and tool evidence honest. The host records each physical LLM attempt as
its own `llm_call`, including retries, and records tool operations separately as `tool_call` events.
Never synthesize a model name, token count, duration, or cost the host did not observe. Unknown
values remain `unavailable`; a known `$0` requires the same source provenance as any other cost.
Do not place raw prompts, model responses, tool arguments/results, credentials, or secret-bearing
logs in the portable ledger or projection.

Whenever you pause or finish, end the response with a fenced YAML handoff that uses the exact
canonical field names from `docs/handoff-contract.md`. Do not replace `mission`, `outcome`, `then`,
`rewind_to`, `outputs`, `note`, or `blockers` with prose aliases. At a routine human gate, include
the phase handoff unchanged and explain the pending gate immediately before it.

Emit conditional routing fields exactly: an `advance` includes `then` and omits `rewind_to`; a
`rewind` includes `rewind_to` and omits `then`; `needs_human` and `stuck` omit both. Never render an
inapplicable field with `null`.

## Capture lessons at the end

When the mission settles — **complete**, or terminally **stuck/failed** after you have exhausted
the options — distil at most a handful of durable lessons supported by run evidence. Worth
proposing: a red-team or review finding that reshaped the work, a failure and verified fix, or an
operator correction turned into a concrete rule. Do not restate the task.

Submit them through the optional **lesson proposal** host capability. Mark each proposal as
project-scoped or global and attach the evidence that supports it. The host owns persistence and
any review gate; the skill never writes shared memory directly. If the capability is absent,
unavailable, or fails, finish normally and state once that lesson capture was skipped.

Never implement before plan approval. Never merge against repository policy. Never silently widen
scope. Do not stop at a phase boundary merely because a phase finished; stop only when the mission
is complete, a human gate is open, a real blocker exists, or an explicit halt applies.

In `mode: yolo`, advance through routine plan, subtask, and review transitions automatically. Do
not ask for a routine proceed/approve response. Surface only the meaningful decisions and blockers
listed in `references/execution-workflow.md`; preserve every recovery attempt and human escalation
in the mission evidence.

## Overrides

`frame`, `build`, `land`, and every subskill can be overridden per repo/user/runtime. Always
invoke the resolved skill by name so overrides take effect. If a capability a phase needs is
unavailable, that phase should return `stuck` with the smallest useful next step — don't
improvise around a missing capability.
