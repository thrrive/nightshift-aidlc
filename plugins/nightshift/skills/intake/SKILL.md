---
name: intake
description: "Major SDLC phase that turns a plain-language request into an approved implementation plan. Resolves the mission, then composes investigate → blueprint → plan → redteam. Stops for plan approval and does not write product code."
---

# /intake — request → approved plan

Own the pre-implementation phase. Convert the user's freeform request into the `mission` the
`aidlc` orchestrator carries through the whole loop, then investigate, design, plan, and red-team
the work. Do **not** edit product code, commit, push, or open PRs.

## Inputs

- The freeform request (verbatim) — e.g. *"Add CSV export to the holdings table."*
- Resolved target metadata and host capabilities: repository, stack, checks, verification, and
  release shape. Use them to ground `done_when` in how *this* target proves and ships a change.
- Any lifecycle controls passed alongside the request (`--frame-only`, `--pr-only`,
  `--no-verify`, `--skip-frame`).

## Process

1. Preserve the request verbatim as `mission.ask`. Do not paraphrase or narrow it.
   Also set `mission.title`: a concise (≤ 8 words) summary of what the change is
   about, in your own words — a chat-thread-style label, not a copy of the ask.
2. Set `done_state`. Default **`stable-production`**. Lower it only on an explicit signal:
   `--frame-only` → `frame-approved`; `--pr-only` → `pr-ready`; "plan only" / "just open a PR,
   don't merge" / "staging only" → the matching state.
3. Derive `done_when` — the observable conditions that prove `done_state`. Ground them in the
   resolved target information, e.g. for a web app heading to production:
   - the change is implemented and merged via one PR;
   - the target's unit tests, lint, typecheck, and build pass;
   - an end-to-end check exercising the new behavior passes against the running app;
   - the configured production release is healthy.
   Trim conditions that don't apply to a lower `done_state`.
4. Translate lifecycle controls into `halts` (e.g. `--no-verify` → `["no-verify"]`). Host execution
   and performance options remain on the run request and never enter `mission` or `halts`.
5. **Vagueness check.** If you cannot write concrete `done_when` conditions because the request
   is ambiguous (unclear surface, undefined acceptance, multiple plausible scopes), return
   `needs_human` with **2–3 sharp, specific** questions — not an open-ended "tell me more".
   Prefer questions a one-line answer resolves.

6. When hierarchical execution is available, derive a bounded ordered `subtask_plan` after the
   mission is clear. Each child needs an id, goal, observable `done_when`, and dependencies only
   on earlier children. Derive a `model_plan` for each execution step: select a model hint from
   complexity, context, reasoning, gate sensitivity, caching, and cost; record rationale,
   expected input/output tokens, pricing reference, and estimated cost when known. These are
   estimates only; actual model usage and cost remain host-observed ledger data. Keep run mode and
   other host performance options out of the canonical mission.

## Turn the mission into a plan

Once the mission is clear, resolve one durable bundle using the
[`frame-artifact contract`](../../docs/frame-artifacts.md). Then run **investigate**,
**blueprint**, **plan**, and **redteam** in that order. Clarify genuine ambiguities before
blueprint; do not guess at a costly product decision. Rewind and re-review any material finding.

Persist the complete investigation, blueprint, plan, review, and handoff before the approval gate.
The plan must include the implementation sequence, files or components expected to change, proof
shape, risks, and observable definition of done.

## Output — when the plan is ready

```yaml
mission:
  title: <≤8-word summary, your words>
  ask: <request verbatim>
  done_state: stable-production
  done_when:
    - <observable condition>
    - <observable condition>
  halts: []
outcome: advance
then: build
note: <one line: the goal as you understood it>
```

Present a concise framing summary, then the complete human-readable plan, then the approval
question as the final visible content of the response. Do not append a YAML handoff, another
summary, or an invitation to start Build after it. Keep the canonical handoff in the durable
bundle for the orchestrator.

## Output — when clarification is needed

```yaml
outcome: needs_human
note: <what's ambiguous, in one line>
questions:
  - <sharp question 1>
  - <sharp question 2>
```

Do not invent a scope to avoid asking. A wrong mission is more expensive than one round of
questions.
