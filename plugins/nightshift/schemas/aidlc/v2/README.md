# AIDLC human-first mission-bundle schemas — version 2

This directory versions the durable evidence envelope independently from the stable v1 lifecycle
wire contract:

- `bundle.schema.json` validates immutable identity, canonical mission digest, bundle format, and
  standard paths;
- `event.schema.json` validates append-only phase, attempt, model, tool, transition, and proof
  events.

An `aidlc-mission-bundle/v2` still stores the unchanged v1 `mission` in `.aidlc/mission.json` and the
latest v1 `outcome` in `.aidlc/latest-outcome.json`. Hosts therefore adopt the human-first evidence
format without changing phase routing or invalidating stored v1 handoffs.

JSON Schema validates each descriptor/event. `scripts/check_mission_bundles.py` additionally checks
ledger semantics that require peer comparison: one mission identity, unique event IDs, and a
contiguous monotonic sequence. The host writer must enforce those invariants atomically.

Fixtures distinguish known zero cost from unavailable attribution and reject raw tool payloads.
Full allocation, resume, redaction, projection, and negotiation behavior is documented in
[`docs/mission-bundles.md`](../../../docs/mission-bundles.md).
