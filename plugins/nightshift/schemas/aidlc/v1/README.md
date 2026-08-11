# AIDLC contract schemas — version 1

These JSON Schemas are the machine-readable, host-neutral contract for the public AIDLC skill kit:

- `mission.schema.json` validates the durable goal that phases carry unchanged;
- `outcome.schema.json` validates phase routing and embeds the mission;
- `review.schema.json` validates evidence-backed red-team, self-review, and change-review records;
- `workstreams.schema.json` validates the optional bounded parallel-build declaration.

The stable schema identifiers are `urn:nightshift:aidlc:v1:mission`,
`urn:nightshift:aidlc:v1:outcome`, `urn:nightshift:aidlc:v1:review`, and
`urn:nightshift:aidlc:v1:workstreams`. Consumers should pin
the directory version and must not resolve these identifiers over the network.

Validate an entire phase handoff against `outcome.schema.json`. The valid and invalid examples in
`fixtures/` are compatibility cases and are exercised by `tests/test_aidlc_schemas.py`.

## Validation boundary

Schema validation proves payload shape, enum values, conditional routing, workstream item bounds,
identifier format, and basic path safety. A runtime must additionally enforce unique workstream IDs
and component-wise ownership disjointness: no normalized workstream path may be a prefix of another
path, within or across items. JSON Schema cannot compare one item property with every peer property.
Nightshift's semantic validator remains the reference v1 implementation.

The optional `review` property binds a structured review record to a phase outcome. Its semantic
decision rules are documented in [`docs/review-contract.md`](../../../docs/review-contract.md).
Other phase-specific evidence such as verification and release results may extend an outcome object.
Mission and workstream objects are closed so their portable meaning cannot drift through private
runtime fields.

Any incompatible field, enum, or routing change requires a new schema-version directory. Additive
phase evidence may remain compatible because the outcome object deliberately permits extensions.
