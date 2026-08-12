# Stable-v1 blueprint

## Approach

Create and publish `v1.0.0-rc.1` as the immutable candidate. Add frozen `v0.1.0` handoffs to CI,
align public manifests and compatibility documentation, and validate both plugin layouts. Install
the tagged candidate in fresh host environments and run two complete external missions. Promote
the same contract to `v1.0.0` only after retaining the mission evidence.

## Components affected

- Public package metadata and documentation.
- Schema compatibility test fixtures and validation scripts.
- Release evidence artifacts; no private Nightshift runtime or external target product code.

## Data and contract changes

No canonical v1 field or routing-semantic change. The release adds tests and metadata around the
already additive optional review contract.

## Rollout and observability

Publish an annotated prerelease tag first. Candidate rollback is the existing `v0.1.0` tag.
Qualification records exact tag, commit, host, target revision, lifecycle outcomes, checks, and
artifacts. Stable promotion uses a second reviewed PR and annotated release.

## Verification shape

Custom release qualification: package/schema checks, Claude and Codex manifest/load checks, two
fresh Git repository missions from the immutable tag, one exercised rewind, one exercised human
gate, and direct inspection that canonical schemas did not change during qualification.
