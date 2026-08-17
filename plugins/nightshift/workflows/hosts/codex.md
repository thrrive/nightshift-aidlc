# Codex host mapping

Codex does not require a `/workflows` command. The portable dispatcher can start the same named
workflow definitions through `/nightshift:workflow`; bind their capability calls to the
deterministic host runner. The runner owns bounded retries, review gates, workstream joins, and
durable `execution_state`; the model session supplies only the requested phase work and evidence.

Canonical entrypoints are `/nightshift:workflow nightshift-aidlc <request>` for the full lifecycle
and `/nightshift:workflow nightshift-missions-next <mission-id>` for one explicit child transition.
The skill fallbacks remain `/nightshift:aidlc` and `/nightshift:missions <mission-id> --next`.
