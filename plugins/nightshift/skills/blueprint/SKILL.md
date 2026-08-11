---
name: blueprint
description: "frame subskill. Turns investigation findings into a technical approach: components touched, data/contract changes, rollout and observability expectations, and the appropriate browser, API, CLI, library, or custom verification shape."
---

# /blueprint — the technical approach

Decide *how* the change is built, at the level of components and contracts — not exact file
edits or function signatures. The plan and the implementer fill in the mechanics later.

## Decide and record

- **Approach** — the design that satisfies the requirements while fitting the repo's existing
  patterns. Prefer the smallest design that is correct and consistent with prior art.
- **Components affected** — the modules, routes, schema, jobs, or UI surfaces that change, and
  how they connect. Call out anything shared across users/tenants (isolation is a correctness
  property, not a nice-to-have).
- **Data & contract changes** — schema migrations, API/shape changes, new env/config. Note
  backward-compatibility and ordering constraints.
- **Rollout & observability** — how the change reaches production safely and how you'd know it's
  working (or not) afterward. Keep it proportional to risk.
- **Verification shape** — choose browser, API, CLI, library, or a justified custom form and
  describe the observable result that counts as proof. Name the user flow, request/response,
  command contract, public API, or other behavior the build must exercise.

## Output

Return the approach with the sections above. Keep it decision-dense; omit detail the plan and
implementer can infer. Persist the complete result as `blueprint.md` in the durable bundle supplied
by `frame` before returning; never substitute a scratch-only path. Return `advance` to `plan`.
