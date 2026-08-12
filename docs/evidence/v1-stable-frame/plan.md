# Stable-v1 implementation plan

## Goal

Publish a defensible stable Nightshift AIDLC v1 and then return immediately to the combined
Nightshift rearchitecture program.

## Done state and done-when conditions

`merged`, proven by the five observable conditions in `mission.json`.

## What changes

1. Freeze `v1.0.0-rc.1` metadata and backward-compatibility checks in one release PR.
2. Merge, tag, and publish the candidate; install only from that immutable tag.
3. Run two fresh external missions, deliberately retaining a human gate and evidence-driven rewind.
4. Record qualification evidence, update stable release metadata, and verify the candidate and
   stable schemas are contract-identical.
5. Merge, annotate, and publish `v1.0.0`.
6. Update Nightshift's combined master plan and resume its next ready rearchitecture slice.

## Components affected

Public plugin package, compatibility CI, release documentation, and later the Nightshift program
status document.

## Pull-request scope

Two ordered PRs are required: an immutable candidate before dogfood, then evidence-only stable
promotion. Combining them would make the tested artifact mutable and invalidate the proof.

## Verification

Run package, schema, integrity, manifest, installation/load, and external mission checks. Evidence
must name exact revisions and preserve all lifecycle artifacts.

## Rollout and observability

Use annotated Git tags and GitHub prerelease/release records. Keep `v0.1.0` as rollback. No runtime
migration exists.

## Risks

- Circular proof: prevented by tagging before dogfood.
- Synthetic lifecycle claims: prevent by using fresh host processes and durable artifacts.
- Compatibility drift: freeze preview fixtures and compare schemas between RC and stable.
- Release metadata divergence: validate manifests and deterministic integrity manifest in CI.

## Test strategy

Local package/schema/manifest validations before each commit; GitHub package CI on each PR; host
load and mission checks against the tag after merge.

## Definition of done

All mission conditions are observably satisfied and the subsequent Nightshift work item is claimed.

## Out of scope

Private execution-plane implementation, hosted workers, and redesigning the canonical contract.
