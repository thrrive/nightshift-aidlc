# Compatibility policy

The `mission` and `outcome` field names are the lifecycle spine. Patch and minor releases do not
remove fields, change enum meanings, move transition ownership, or turn an optional capability into
an unconditional requirement. New optional fields must preserve older valid handoffs.

The v1 JSON Schemas and fixtures define wire compatibility. A breaking schema or routing change
requires a new major version and a migration guide. Host-specific commands, storage, provider SDKs,
and execution strategies remain outside the portable contract.

The release candidate is tested against Claude Code and Codex plugin layouts. Other hosts may load
the skills directly when they preserve frontmatter, relative references, and the host-capability
semantics.

## Stable-v1 guarantees

Stable `1.x` releases preserve every valid `mission` and `outcome` handoff published in `0.1.0`.
CI validates frozen copies of those preview fixtures from `tests/compatibility/v0.1.0/` against the
current v1 schema. The evidence-backed `review` record and its host attestation are additive and
optional: hosts that implemented the preview contract may continue without them.

Upgrading a host does not authorize new effects. Workspace writes, verification, reviewed-change
operations, release actions, prior-memory reads, and lesson proposals retain the availability and
human-authorization rules in `docs/host-capabilities.md`. A host may adopt new optional evidence
fields incrementally without rewriting stored v1 missions or outcomes.
