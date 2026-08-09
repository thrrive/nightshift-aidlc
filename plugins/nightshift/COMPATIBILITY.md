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
