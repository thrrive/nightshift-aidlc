# Host progress and human-gate delivery

Keep the operator informed during a long workflow. A durable event ledger is not, by itself, a
live notification channel.

At invocation, every major-phase transition, every subtask start/finish, every retry, and every
human gate, emit a concise user-visible progress message through the host's current response
channel. Do not wait until the final handoff to report accumulated work. Include the mission
summary, phase or subtask, current state, and the next action; do not include raw model output or
secret-bearing tool data.

When `needs_human` is reached, immediately present the exact decision or action required in the
current interactive session, identify the durable mission/bundle reference, and stop. Do not only
write a handoff file or say that the mission is paused. After the operator answers, resume the same
mission and append the decision to its evidence.

## External host bridge

If the host offers a live workflow bridge, use it for both progress and human decisions. The bridge
subscribes to the mission event stream, renders boundary events in the host session, and routes the
operator's response back to the active turn. It must preserve the mission ID, event ID, sequence,
phase, subtask, and gate reference.

Codex adapters use `codex app-server --stdio`: stream notifications, use `turn/steer` for an
active turn, and resume the same thread after a parked gate. Claude adapters use the streaming
NDJSON interface: consume `--output-format stream-json` and inject a user turn through
`--input-format stream-json`. A one-shot CLI without an open input/control channel cannot receive
external intervention; in that case, use the explicit in-session question and resume command
fallback instead of claiming live steering.
