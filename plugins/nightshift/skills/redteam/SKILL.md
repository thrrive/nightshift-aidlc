---
name: redteam
description: "frame subskill. Adversarial review of the implementation plan and blueprint before human approval. Hunts for correctness, security, isolation, scope, and verification gaps. Rewinds to blueprint or plan on a material issue."
---

# /redteam — break the plan before it ships

Read the plan and blueprint as a skeptic whose job is to find what's wrong *before* code is
written. Assume the plan is flawed and try to prove it. A clean pass is earned, not assumed.

## Attack the plan along these lines

- **Correctness** — does the approach actually satisfy every requirement? Edge cases, empty
  states, error paths, concurrency, ordering of migrations vs. code.
- **Data isolation & security** — if data is per-user/per-tenant, does the plan keep it scoped?
  Any path where one user's data could reach another is a stop-the-line finding. Check authz,
  query scoping, cache keys, and anything shared.
- **Blast radius & rollout** — what breaks if this is half-deployed? Is the rollout reversible?
  Are migrations backward-compatible in the order they apply?
- **Scope discipline** — is the plan one coherent change, or is it smuggling unrelated refactors,
  broad reformatting, or speculative work? Flag scope creep now.
- **Multi-surface (web/mobile) consistency** — if this repo ships a **mobile app alongside the
  web app** (look for a `mobile-app/`, `mobile/`, `apps/mobile`, or React Native / Expo package),
  and the change touches a **shared** feature, API contract, validation rule, or user-facing
  behavior, does the plan keep **both** surfaces consistent? A change that updates only the web
  surface and silently leaves the mobile app on the old behavior is a **material gap** — unless the
  plan **explicitly scopes** the change to one surface (the mission asked for a web-only or
  mobile-only deviation, stated in the plan's scope / out-of-scope / verification). Rewind a plan
  that diverges the surfaces without saying so; accept a divergence the plan names on purpose.
- **Verifiability** — did the plan select the right verification shape, and is its pass condition
  observable? A browser-only plan for a library or a unit-only plan for a user flow is a gap.
- **Existing tests this change breaks** *(a lens to apply, not a rule)* — does the change alter
  behavior an existing test already asserts? Enumerate the tests that touch the surface this plan
  changes (specs, fixtures, snapshots). If any encode the *old* behavior, the plan must say it
  updates them — a green local check that leaves a stale test asserting old behavior is a CI
  failure waiting to happen. A behavior change with no corresponding test update is a flag to
  raise and weigh, not automatically a rewind.

## Output

- **Clean** → return `advance`; `frame` finalizes for the human approval gate.
- **Material gap** → return:
  ```yaml
  outcome: rewind
  rewind_to: blueprint | plan
  note: <the specific gap and why it blocks>
  ```
  Send design-level gaps to `blueprint`, plan/scope/definition gaps to `plan`.

Be specific and evidence-based. "This feels risky" is not a finding; "the migration drops a
column the running app still reads, so a half-deploy 500s" is.
