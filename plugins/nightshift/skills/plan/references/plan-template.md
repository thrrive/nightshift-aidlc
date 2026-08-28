# Implementation-plan template

Produce every section below. Write `none` with a reason when a section does not apply.

## Goal

State in one or two sentences what changes for the user when this ships.

## Done state and done-when conditions

Copy the mission's exact `done_state` and list the observable conditions that prove it.

## What changes

Give ordered steps. Name the component and behavioral change in each step; leave exact function
signatures and speculative file edits to implementation.

## Components affected

Name only the affected surfaces: web, API, worker, database, mobile, infrastructure, or other.

## Pull-request scope

Use one coherent change by default. If multiple reviewed changes are necessary, explain why and
define their order. Name the primary feature pull request and any companion API-test pull request,
their dependency, shared acceptance evidence, and the review/check signal required for each.

## Verification

Choose the approved browser, API, CLI, library, or custom shape. State the behavior to prove, exact
observable acceptance conditions, and expected evidence. Identify the repository-owned check for
that shape or plan the smallest focused check needed. Prefer browser proof for user-facing web
behavior; do not require it for unrelated targets.

### Pre-production validation matrix

State the planned proof for each dimension. Mark the first two as deterministic checks and the
remaining three as reviewer reasoning. Name the exact command, flow, artifact, or oracle and
record environmental caveats instead of treating unavailable execution as a pass.

- `regression-safety` — existing behavior that must remain green.
- `acceptance-behavior` — end-to-end behavior in the target shape.
- `acceptance-criteria` — mapping from every criterion to implementation and evidence.
- `design-quality` — patterns, abstractions, boundaries, security, and extension points.
- `test-validity` — tests, oracle sensitivity, and any negative-space probe.

## Rollout and observability

Specify migration order, compatibility, flags, rollback, logs, and metrics as applicable.

## Risks

List the two to four most important failure modes and their mitigations.

## Test strategy

State what runs before commit and what CI must pass.

## Definition of done

Use a short, objectively verifiable checklist. Include the approved verification shape passing,
all five validation-matrix rows resolved, every declared pull request reviewed, and any configured
release/rollout and issue-tracker update completed unless the mission explicitly waives that step.

## Out of scope

Name adjacent work this plan deliberately excludes.
