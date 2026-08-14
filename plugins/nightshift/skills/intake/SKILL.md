---
name: intake
description: "Turn a freeform, plain-language change request into a structured mission (ask, done_state, done_when, halts) for the aidlc orchestrator. Runs once at the start of a job, before the phase loop. Asks for clarification when the request is too vague to define done."
---

# /intake — prompt → mission

Convert the user's freeform request into the `mission` the `aidlc` orchestrator carries through
the whole loop. This is the only place a vague request gets sharpened; once `intake` returns,
later phases trust the mission and do not re-litigate the goal.

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

## Output — when the mission is clear

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
then: frame          # or build, when --skip-frame
note: <one line: the goal as you understood it>
```

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
