Use the Nightshift `frame` skill for this mission:

> Add a read-only JSON export command to a small Python library. Stop after a human-approvable plan.

Use these settled facts: the package is `samplelib` on Python 3.11; the command is
`python -m samplelib export-json`; it writes the current in-memory configuration dictionary as JSON
to standard output; read-only means it must not mutate that dictionary or write files; standard-
library dependencies only. No repository is attached, so keep component names generic. Produce a
concise plan with an observable CLI verification condition and return the canonical phase handoff.
Assume the host provides a durable invocation root at `/work/samplelib-mission` and allows writes
there.
Do not ask follow-up questions, implement the change, or enter another major phase.
