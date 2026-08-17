# Nightshift workflows

These files are the portable workflow layer for hosts that support named workflows. They define
the lifecycle transitions, gates, recovery bounds, and host capability calls; they do not assume a
model provider, process runner, or storage engine.

`manifest.json` is the public registry. It gives each workflow a stable name, definition file,
entry skill, user-facing invocation, and fallback. The portable `/nightshift:workflow` dispatcher
loads this registry and delegates to the declared skill, so hosts can expose workflows without
duplicating the skill implementation.

Load `aidlc.md` for a complete software-delivery mission. Load `missions-next.md` for the explicit
one-subtask progression action. Host mappings live in `hosts/claude.md` and `hosts/codex.md`.

Hosts may expose these workflows through a native workflow command, a skill invocation, or a
deterministic runner. The mapping must preserve the same routes and gates.

Canonical portable commands:

```text
/nightshift:workflow nightshift-aidlc <change request>
/nightshift:workflow nightshift-missions-next <mission-id>
```

The direct skill fallbacks remain `/nightshift:aidlc <change request>` and
`/nightshift:missions <mission-id> --next`.
