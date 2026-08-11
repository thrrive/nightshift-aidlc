# Durable frame-artifact contract

Frame work must survive the conversation and remain easy for the user to find before approving
implementation. This contract is portable: it defines durability and placement without assuming a
specific agent SDK, filesystem API, or hosted artifact service.

## Storage identities

- **Invocation root** — the user-visible directory or project from which an interactive mission
  was started. For a local agent, this is normally its starting working directory.
- **Durable artifact store** — a host-managed location the user can reopen after the agent session
  ends. A hosted run may use this instead of a local invocation root.
- **Scratch storage** — an agent sandbox, operating-system temporary directory, transient message,
  or session-only filesystem. Scratch may help execution, but it never counts as the sole durable
  copy of frame work.

The host must identify the invocation root or durable store explicitly. Do not infer a different
checkout, create a repository, or escape the user-authorized root merely to persist artifacts.

## Bundle resolution

Resolve one bundle root before `investigate`, then pass it unchanged through every frame subskill:

1. Use the target's declared feature-docs path when it is writable and user-visible.
2. Otherwise use a user-selected durable destination.
3. Otherwise, for an interactive local run, create `nightshift/<mission-slug>/` under the
   invocation root—even when the target repository does not exist yet.

Derive `mission-slug` from the ask using only lowercase letters, digits, and hyphens. Remove path
separators and traversal components, keep it short enough to remain readable, and use a neutral
fallback such as `mission` when no characters remain. If the destination already belongs to the
same mission, reuse it on rewind or resume. If it belongs to another mission, append a stable host
run reference or the smallest available numeric suffix; never overwrite the other bundle.

## Required bundle

Persist each artifact as soon as its owning step completes:

```text
<bundle-root>/
  mission.json
  investigation.md
  blueprint.md
  plan.md
  redteam-review.json
  handoff.yaml
```

`mission.json` carries the canonical unchanged mission. The Markdown files contain the complete
reviewable output, not a pointer to hidden scratch content. `redteam-review.json` follows the shared
review contract. Write `handoff.yaml` before presenting the plan-approval gate and list all durable
paths in its `outputs` field.

Rewinds update the same logical files so the bundle remains coherent. A host may retain version
history or additional provenance, but the user-facing bundle always represents the current review
subject. Do not place credentials, raw secret-bearing logs, or unrelated repository content in it.

## Failure and degradation

Before requesting plan approval, confirm that the durable copies exist and tell the user the exact
paths or artifact references. A temporary path may be reported as execution detail, but must not
appear in `outputs` as the only copy.

If neither an authorized invocation-root write nor a durable artifact store is available, return
`needs_human`. Include the proposed bundle inline so the work is recoverable, and ask the user to
choose a durable destination or explicitly accept an inline-only review for this mission. Never
claim that conversation content or scratch files were persisted.
