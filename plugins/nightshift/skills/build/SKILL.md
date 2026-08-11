---
name: build
description: "Major SDLC phase after plan approval. Prepares an isolated workspace, implements the approved change, runs declared checks, self-reviews, verifies with the target's approved shape, and delivers one reviewable change. Returns a handoff toward land."
---

# /build — approved plan to a verified change

Own implementation after plan approval or a `land` route-back. Delivering a pull request is not a
stopping point unless `mission.done_state` is `pr-ready`.

Compose `implement`, `self-review`, and `verify`; never call `land` or `frame`. Invoke resolved skills
by name so host overrides remain effective and step attribution stays intact.

## Inputs

- the unchanged `mission` and approved plan;
- investigation, blueprint, rollout, and verification-shape artifacts;
- resolved target metadata and available host capabilities;
- an optional existing `workspace_ref` and change reference on route-back.

## Process

1. Request the **workspace capability** for an isolated workspace on the resolved base revision.
   Reuse its opaque reference on route-back. Never silently fall back to in-place editing.
2. Re-read the plan and target contribution rules inside that workspace.
3. Identify the declared checks for the changed surface before editing.
4. Run **implement** against the approved plan.
5. Run relevant repo-owned tests, lint, type checks, builds, or equivalent checks. Never bypass
   contribution hooks.
6. Run **self-review** against the pinned diff, plan, and `done_when` using the shared
   evidence-backed review contract. Re-review remediation; a design gap returns `rewind`, an
   in-scope defect returns to implementation, and incomplete evidence holds for human judgment.
7. Run **verify** with the approved browser, API, CLI, library, or custom shape. Preserve its status
   and evidence without translating `unproven` into success.
8. Prepare focused commits or the host's equivalent reviewable revision.
9. If delivery is `pull-request`, request the **pull-request capability** to open one change by
   default. On route-back, update the existing change instead of opening another.
10. Return `advance` toward `land` only when the requested delivery artifact exists.

If a required capability is unavailable, return `stuck` with the smallest useful next step. Do not
replace isolation, verification, or reviewed delivery with a weaker unapproved mechanism.

## Pull-request evidence

Provide phase artifacts and structured findings to an available PR-body composer. Provider-specific
formatting, API calls, attribution, and authenticated user lookup belong to the host adapter. If no
composer exists, use a concise host-neutral summary of frame, build, review, and verification, and
retain links to the underlying evidence.

Always produce the self-review record, including the reviewed subject, independent lenses, core
claims, proof ceiling, stable findings, remediation, and residual risks. The host may choose its
artifact location; never hardcode a private runtime path.

## Guardrails

- One mission produces one reviewable change unless the approved plan explicitly splits it.
- Keep unrelated refactors, reformatting, and generated commentary out of the change.
- Never use a verification waiver to bypass repository checks or hooks.
- Never infer repository, account, or release identifiers from a folder name.

## Completion handoff

```yaml
mission: { ... }
outcome: advance | rewind | needs_human | stuck
then: land                                       # include only for advance
rewind_to: investigate | blueprint | plan | redteam  # include only for rewind
outputs: []
note: <what changed and how it was proven>
blockers: []
review: { ... }             # self-review record for the delivered revision
links:
  pr: <review URL when delivery is pull-request>
  commits: []
verify:
  shape: browser | api | cli | library | custom
  status: passed | failed | unproven | waived
  evidence: []
```

`then` and `rewind_to` are mutually exclusive. Omit the inapplicable field entirely; never emit it
as `null`.
