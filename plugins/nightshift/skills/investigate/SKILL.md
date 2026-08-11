---
name: investigate
description: "frame subskill. Gathers the facts needed to design a change: requirements, current behavior, prior art, repo conventions, constraints, and the open questions that must be resolved before design. Reads code; does not modify it."
---

# /investigate — gather the facts

Build the factual ground the rest of `frame` stands on. Read widely, change nothing.

## Capture

- **Repo identity (confirm, never infer).** Establish the target's real GitHub slug, default
  branch, and clone URL from the source of truth — `git remote -v` and `gh repo view` — **not**
  from the local folder name. A checkout directory frequently differs from the repository slug, and
  guessing the slug silently breaks any later clone. The same discipline applies to deploy
  identifiers (e.g. platform project/service names): confirm them against the actual platform; if
  you can't, record them as open questions marked *needs-verification* rather than assuming they
  match the repo or folder name.
- **Requirements** — restate what the change must accomplish in concrete, testable terms. Tie
  each back to `mission.ask`.
- **Current state** — how the relevant surface behaves today: the code paths, data, and UI
  involved, and where the change will land.
- **Prior art** — existing patterns in this repo that already solve a similar problem. Reuse
  beats inventing; name the files and helpers worth following.
- **Conventions & constraints** — the repo's rules that bind this change: directory layout,
  naming, data-access patterns, security/isolation rules, framework/runtime version limits,
  test conventions. Read the repo's own guidance files (e.g. `CLAUDE.md`, `README`,
  `ARCHITECTURE`) and honor them.
- **Open questions** — anything genuinely ambiguous or risky that design needs settled. Mark
  which are blocking (only the user can answer) vs. resolvable during design. Phrase each blocking
  question so a one-line answer resolves it and tie it to the concrete surface it concerns (the
  real file, table, or screen) — these are the questions `frame` puts to the user before designing,
  so write them ready to ask, not as vague gestures.

## Output

Return a tight findings summary with those sections. Flag blocking open questions explicitly and
ready to ask — `frame` runs a clarification gate on them (probing the user when an operator is
present) before `blueprint`.

When `frame` supplies a durable bundle reference, persist the complete result as
`investigation.md` there before returning. Do not choose a different root or leave scratch storage
as the only copy. When invoked standalone, resolve the durable frame-artifact capability first.

Return `advance` to `blueprint` when the picture is solid enough to design against. Prefer
naming specific files/functions over vague gestures — the next steps build directly on this.
