---
name: workflow
description: "Start a named Nightshift workflow and delegate execution to its portable skill entrypoint."
---

# /workflow — start a named workflow

Use this skill when the user wants to start Nightshift by workflow name rather than by selecting a
phase skill directly. The workflow bundle is the source of truth for ordering, gates, joins,
recovery bounds, and host capabilities; the referenced skill remains the source of truth for phase
behavior.

## Invocation

Accept a workflow name followed by its request arguments:

```text
/nightshift:workflow nightshift-aidlc <change request>
/nightshift:workflow nightshift-missions-next <mission-id>
```

Load `workflows/manifest.json`, reject unknown or malformed names, then load the selected workflow
definition. Delegate to its `entry_skill` without rewriting the workflow's routing or gates.

The `nightshift-aidlc` workflow delegates to `/nightshift:aidlc` for a complete mission. The
`nightshift-missions-next` workflow accepts exactly one mission ID and delegates to
`/nightshift:missions <mission-id> --next`; it starts one dependency-ready child and persists the
transition through the host mission capability.

If the host exposes a native named-workflow facility, preserve the same definitions and state
contract. This skill is the portable fallback for hosts that do not expose one.

Never infer a workflow or mission from conversation history, edit mission artifacts directly, or
bypass plan, review, verification, merge, or release gates.
