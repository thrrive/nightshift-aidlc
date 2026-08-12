---
name: implement
description: "build subskill. Writes the change against the approved plan with focused, well-scoped commits that match the target repo's conventions. No scope creep, no unrelated refactors."
---

# /implement — write the change

Execute the approved plan. Stay inside its scope; the plan is the contract.

Work inside the `workspace_ref` that `build` prepared through the
[`workspace capability`](../../docs/host-capabilities.md#workspace-required-for-build). Reuse that
workspace on route-backs. Do not create or switch to a different branch, sandbox, clone, or worktree,
and do not touch another checkout; the host owns isolation and workspace lifecycle.

## How to work

- **Match the surrounding code.** Follow the repo's naming, structure, idioms, and comment
  density. Read neighboring files before adding new ones; reuse existing helpers over inventing.
- **Follow the plan, not your preferences.** If the plan and reality disagree, stop and return a
  rewind — don't quietly redesign mid-implementation.
- **Keep the diff focused.** Only touch what the change requires. No drive-by reformatting,
  speculative abstraction, or unrelated fixes. If you spot something worth doing later, note it;
  don't do it now.
- **Write the tests the plan calls for** alongside the code, using the repo's existing test
  conventions.
- **Honor security & isolation rules** from investigation/redteam exactly — especially any
  per-user/per-tenant data scoping. These are correctness requirements.
- **Commit in focused units** with the repo's required commit-message format/trailers.
- **Return safe evidence.** Name changed components and check references, but do not place raw model
  output, credentials, environment values, or secret-bearing tool arguments/results in a v2 mission
  event or `MISSION.md` projection.

## Output

Return a summary of what changed (by component) and which checks you expect to pass. Return
`advance` to `self-review`. If implementation reveals the plan is wrong or incomplete, return
`rewind` with the specific gap instead of forcing the change through.
