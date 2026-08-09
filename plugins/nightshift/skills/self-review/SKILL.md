---
name: self-review
description: "build subskill. A fresh-context review of the local diff against the approved plan, definition of done, and diff-hygiene rules, before any PR is opened. Catches scope creep and plan/design gaps early."
---

# /self-review — review the diff before the PR

Review the working diff with fresh eyes before it becomes a PR. Prefer a fresh-context subagent
when the runtime supports one; otherwise review deliberately in the current session, as if you
hadn't written the code.

## Check

- The diff delivers the approved plan and satisfies the definition of done — no more, no less.
- Tests and local-check evidence actually cover the changed surface.
- Security and data-isolation requirements are implemented, not assumed.
- Rollout/observability expectations from `frame` are handled or explicitly not needed.
- No unrelated files, speculative refactors, broad reformatting, or generated docs/comments.
- The change stays one coherent PR unless the plan approved a split.
- The repo-owned check/spec for the approved verification shape exists or was updated and matches
  the plan's observable acceptance conditions.
- **Multi-surface (web/mobile) consistency** — if this repo ships a **mobile app alongside the web
  app** (a `mobile-app/`, `mobile/`, `apps/mobile`, or React Native / Expo package), and the diff
  changes a **shared** feature, API contract, validation rule, or user-facing behavior, did it
  update **both** surfaces consistently? A web-only diff that leaves the mobile app on the old
  behavior is a finding — **unless** the approved plan explicitly scoped the change to one surface.
  Grep the mobile package for the symbols/endpoints/strings this diff changes; treat a silent
  divergence as a `plan-gap`/`correctness` finding, an intended one (per the plan) as no finding.
- **Existing tests this change breaks** *(a lens, not a rule)* — grep the repo's test files for the
  symbols/strings this diff changes (renamed/removed UI text, deleted controls, changed signatures).
  If the diff changes behavior an existing test asserts but does **not** also update that test, raise
  it as a finding — a stale test that encodes the old behavior turns green-locally into red-CI. Weigh
  it; it is a flag, not an automatic rewind.
- **Verification actually ran.** A check you could not run (deps failed to install, a tool missing) is
  **unproven**, not passing — never record or imply verification passed when it did not run. If the
  local checks could not run, say so plainly; the harness records verification unproven and the land
  gate blocks on it rather than waving it through on the PR's CI alone.
- Any external identifiers written into config — repo slug, clone URL, deploy project/service names
  — are verified against the real source (`git remote -v`, `gh repo view`, the deploy platform),
  not inferred from the folder name. Treat an unverified identifier as a finding.

## Output

- **Clean** → return `advance`; `build` proceeds to verification and the PR.
- **Fixable within the plan** → return the specific issues for `implement` to address before the
  PR is opened.
- **Plan/design gap** → return:
  ```yaml
  outcome: rewind
  rewind_to: blueprint | plan
  note: <why the local implementation can't safely proceed as planned>
  ```

Cite specifics (file, line, why). Vague unease isn't a finding.

### Structured findings record

Read and follow [`references/findings-record.md`](references/findings-record.md). Always write that
record when the host provides an artifact destination, including for a clean review. The handoff's
`outcome` remains the routing spine; the record makes the evidence inspectable beside it.
