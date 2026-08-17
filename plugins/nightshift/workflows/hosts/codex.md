# Codex host mapping

Codex does not require a `/workflows` command. Load the same workflow definitions as portable
instructions through the Nightshift skills, then bind their capability calls to the deterministic
host runner. The runner owns bounded retries, review gates, workstream joins, and durable
`execution_state`; the model session supplies only the requested phase work and evidence.

Entrypoints are `/nightshift:aidlc` for the full lifecycle and
`/nightshift:missions <mission-id> --next` for one explicit child transition.
