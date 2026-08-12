# Stable-v1 investigation

## Requirements

- Fulfil OSS7 exactly: two complete external missions from one pinned public artifact, one rewind,
  one human gate, no canonical contract change, documented/tested compatibility, and `v1.0.0`.
- Preserve the already approved program boundary: this repository contains the public skills and
  contracts, while Nightshift rearchitecture resumes only after the stable release is proven.

## Current state

- Public `v0.1.0` exists at commit `08da4c6`; current `main` includes additive durable-frame and
  review-contract changes that are still recorded as Unreleased.
- The original `mission` and `workstreams` schemas are unchanged. `outcome` gained only an optional
  `review` property and remains able to validate every valid `v0.1.0` handoff.
- Package and schema checks pass, but CI does not yet freeze and revalidate the preview fixtures.
- No two prior missions meet the strict immutable-artifact evidence bar, so stable proof must be
  run fresh rather than inferred from earlier work.

## Constraints and conventions

- Use pull requests and semantic tags; do not change public contract fields during dogfood.
- Avoid circular evidence by tagging a release candidate before running the qualifying missions.
- Test both Claude Code and Codex package surfaces and retain durable mission artifacts.

## Open questions and resolution

- Which external repositories? Use fresh disposable Git repositories built from the existing
  dependency-free CLI and web fixtures. They are repositories other than the package repository,
  provide deterministic checks, and cannot contaminate user projects.
- How is the plan gate authorized? The user's explicit “finish” direction authorizes the approved
  OSS7 plan. A qualifying external mission will separately record its normal plan approval gate.
