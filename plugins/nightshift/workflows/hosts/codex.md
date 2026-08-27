# Codex host mapping

Codex does not require a `/workflows` command. The portable dispatcher can start the same named
workflow definitions through `/nightshift:workflow`; bind their capability calls to the
deterministic host runner. The runner owns bounded retries, review gates, workstream joins, and
durable `execution_state`; the model session supplies only the requested phase work and evidence.

Canonical entrypoints are `/nightshift:workflow nightshift-aidlc <request>` for the full lifecycle
and `/nightshift:workflow nightshift-missions-next <mission-id>` for one explicit child transition.
The skill fallbacks remain `/nightshift:aidlc` and `/nightshift:missions <mission-id> --next`.

For live progress and intervention, bind the workflow to a Codex app-server session rather than a
one-shot command. Forward mission boundary events to the active session and send operator replies
with `turn/steer`; after a gate, resume the same thread and mission reference. If no app-server
bridge is available, the skill must print progress and the exact human question in the current
session and provide the command/reference needed to resume.
