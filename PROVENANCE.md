# Clean-room provenance

Nightshift AIDLC is original work derived from public software-delivery patterns and from operating
the Nightshift project itself. The public package is generated from an explicit portable-source
allowlist; release automation refuses unlisted files.

The package excludes the private Nightshift runtime, control plane, target and model registries,
credentials, hosted execution, SecondBrain implementation, and shared agent-kernel implementation.
It must not contain copied employer code, text, configuration, comments, identifiers, or internal
terminology. Every release candidate is scrubbed and reviewed before publication.

The generated `PACKAGE-MANIFEST.json` records a SHA-256 digest for every packaged file so reviewers
can inspect the exact artifact contents.
