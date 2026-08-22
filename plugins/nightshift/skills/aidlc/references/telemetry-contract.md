# Direct-run telemetry contract

Record a lifecycle trail for every `/aidlc` invocation. When the host exposes the v2 mission-
evidence capability, use its append-only ledger and preserve the host's provenance. When that
capability is unavailable, use the compatible v1 fallback below so a mission remains observable
after the session ends.

## v1 fallback

Write an append-only `<bundle-root>/events.jsonl` beside the v1 mission artifacts. Create it before
the first phase starts and append one JSON object per line. Never rewrite prior records. Each record
must contain `sequence`, `event_id`, `mission_id`, `type`, `phase`, `step`, `status`, and
`occurred_at`; include `subtask_id` and `step_attempt` for child work and retries.

Record mission start and finish, every phase/subskill start and finish, approval or refusal gates,
rewinds, verification, and terminal outcomes. For each physical model call, append an `llm_call`
record with the observed model, input/output token counts, duration, cost, and provenance. Record
retries as separate calls with incremented attempts. If the host cannot observe a value, write
`unavailable` with its provenance; never estimate or substitute zero.

Keep the ledger safe for sharing: do not include raw prompts, model responses, tool arguments or
results, credentials, or secret-bearing logs. The ledger is evidence for inspection and metrics,
not a replacement for the canonical mission or handoff contract.
