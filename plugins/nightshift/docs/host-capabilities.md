# Host capability contract

## Contents

- [Availability and degradation](#availability-and-degradation)
- [Target metadata](#target-metadata-required)
- [Durable frame artifacts](#durable-frame-artifacts-required-for-plan-approval)
- [Mission evidence](#mission-evidence-optional-across-the-full-lifecycle)
- [Workspace](#workspace-required-for-build)
- [Verification](#verification-required-unless-waived)
- [Review attestation](#review-attestation-optional)
- [Pull request](#pull-request-required-for-pr-ready-and-beyond)
- [Release](#release-conditionally-required)
- [Prior-memory read](#prior-memory-read-optional)
- [Lesson proposal](#lesson-proposal-optional)

The AIDLC skill kit defines lifecycle behavior. The host supplies optional or required capabilities
for effects outside that behavior. A skill asks for a capability by purpose; it never assumes a
particular command, process model, storage engine, agent SDK, or service.

This separation keeps the public phase machine usable in an interactive agent, a local runner, or a
hosted execution plane. Nightshift may bind these ports to its private runtime. Other hosts may bind
them differently or leave optional ports absent.

## Availability and degradation

A host capability reports one of three states:

- **available** — invoke it and retain the returned evidence;
- **unavailable** — follow the capability's documented fallback and state the omission once;
- **failed** — retain the error as a warning or blocker according to whether the capability is
  optional or required.

Never invent a result for an unavailable capability. Optional enrichment must not block a mission.
A phase effect required by `mission.done_when` must fail honestly with `stuck` when no suitable
capability exists and the user has not explicitly waived it.

Capabilities return structured results and evidence references. Display text is a derived view, not
the only retained result. A host may implement several capabilities in one service, but skills must
address them by purpose so implementations remain replaceable.

## Target metadata (required)

Purpose: resolve stable target identity and the checks, delivery policy, verification shape, and
release expectations needed to form an observable mission.

```yaml
request:
  target_ref: <user or host supplied reference>
result:
  target_ref: <stable canonical reference>
  default_branch: <branch or revision>
  contribution_rules: [<path or reference>]
  checks: [<declared local or CI check>]
  verification_shape: browser | api | cli | library | custom
  delivery: pull-request | commit | patch | report
  release_required: true | false
```

The target resolver supplies metadata, not execution authority. If no target can be resolved, intake
returns `needs_human`; later phases return `stuck` rather than guessing a repository or release.

## Durable frame artifacts (required for plan approval)

Purpose: retain the complete pre-implementation review bundle in a user-visible location that
survives the agent session.

```yaml
request:
  mission: <canonical unchanged mission>
  invocation_root: <authorized user-visible starting workspace, when local>
  feature_docs_path: <optional target-declared path>
  resume_ref: <optional existing bundle reference>
  supported_formats: [aidlc-mission-bundle/v2, aidlc-frame-bundle/v1]
result:
  bundle_ref: <stable durable reference>
  mission_id: <opaque immutable identity when v2 is selected>
  format: aidlc-mission-bundle/v2 | aidlc-frame-bundle/v1
  storage: invocation-workspace | host-artifact-store
  outputs:
    projection: <MISSION.md reference when v2 is selected>
    machine_root: <hidden .aidlc reference when v2 is selected>
    mission: <reference when v1 is selected>
    investigation: <reference when v1 is selected>
    blueprint: <reference when v1 is selected>
    plan: <reference when v1 is selected>
    review: <reference when v1 is selected>
    handoff: <reference when v1 is selected>
```

Resolve the bundle once before investigation and reuse it across rewinds. A fresh invocation omits
`resume_ref`; a host must never infer resume from a matching slug. With v2, it allocates a unique
mission ID and exclusively creates `nightshift/missions/<mission-slug>--<mission-id>/`. With v1,
the interactive fallback remains `nightshift/<mission-slug>/` under `invocation_root`. An
operating-system temporary directory, transient agent sandbox, or conversation is not a durable
result. Full format, placement, collision, and fallback rules live in the [durable frame-artifact
contract](frame-artifacts.md) and [human-first bundle contract](mission-bundles.md).

When no authorized durable destination is available, `frame` returns `needs_human` with inline
recovery content and asks for a destination or explicit inline-only waiver. It must not advance to
the routine plan-approval gate while implying that temporary work is durable.

## Mission evidence (optional across the full lifecycle)

Purpose: append safe, structured execution evidence and refresh the human `MISSION.md` projection
after Frame. A host that selects `aidlc-mission-bundle/v2` for Frame must keep this capability
available for that mission or report the document as stale; other hosts may omit it.

```yaml
request:
  bundle_ref: <exact v2 bundle reference>
  mission_id: <immutable identity>
  expected_mission_sha256: <canonical mission digest>
  operation: append-event | store-review | update-outcome | refresh-projection
  event: <schema-valid safe event, for append-event>
result:
  status: appended | duplicate | updated | rejected | failed
  event_ref: <optional immutable reference>
  sequence: <optional assigned monotonic sequence>
  projection_ref: <MISSION.md reference after refresh>
  evidence: []
```

The host owns one serialized, idempotent writer per bundle. It assigns sequence numbers, rejects a
mismatched mission identity/digest, and deduplicates retries by `event_id`. It applies
authorization, minimization, and redaction before persistence. Raw prompts, raw model responses,
tool arguments/results, credentials, and secret-bearing logs do not belong in portable events.

An LLM event reports model, usage, cost source, cost, and duration when observable. An unavailable
value is explicit and is never converted to numeric zero. Tool calls are separate events. Full
event semantics and projection requirements are in [`mission-bundles.md`](mission-bundles.md).

## Workspace (required for build)

Purpose: prepare and identify the isolated location in which changes may be written.

```yaml
request:
  target_ref: <stable target reference>
  base_revision: <resolved branch or commit>
  resume_ref: <optional existing workspace reference>
result:
  workspace_ref: <opaque stable reference>
  branch_ref: <optional delivery branch>
  isolation: worktree | clone | sandbox | in-place
  evidence: [<creation or reuse record>]
```

The host owns filesystem mechanics, cleanup, and concurrency. Reuse the returned `workspace_ref` on
route-backs. `in-place` is valid only when explicitly selected by target policy; never silently fall
back to it when isolated preparation fails.

## Verification (required unless waived)

Purpose: execute the verification shape approved in the plan and return structured proof.

```yaml
request:
  target_ref: <stable target reference>
  workspace_ref: <prepared workspace>
  revision: <exact revision under test>
  shape: browser | api | cli | library | custom
  acceptance: [<observable condition>]
  changed_surface: [<component or path>]
result:
  status: passed | failed | unproven | waived
  checks: [<check name and result>]
  evidence: [<report, trace, log, screenshot, or artifact reference>]
  note: <one-line classification>
```

Use the target's existing verification implementation when available. A user-facing web change
normally selects `browser`; an API, command-line tool, library, worker, or infrastructure change may
select another shape. `waived` is valid only when the mission explicitly carries `no-verify`.
Unavailable or failed execution is `unproven`, never `passed`.

## Review attestation (optional)

Purpose: bind a review to an exact subject and expose checks the host actually observed, so a
reviewer cannot promote a self-reported command or artifact to behavioral proof.

```yaml
request:
  target_ref: <stable target reference>
  workspace_ref: <prepared workspace>
  stage: redteam | self-review | change-review
  subject_refs: [<plan artifact or exact revision>]
result:
  subject_refs: [<resolved immutable references>]
  reviewer_context: fresh | same-session | unknown
  observed_checks:
    - name: <check or probe>
      status: passed | failed | unproven
      behavior_sensitive: true | false | unknown
      evidence: [<host-owned result reference>]
```

The capability may prepare an independent reviewer context, but it does not decide the review.
When unavailable, the skill still performs static inspection and reports the weaker proof ceiling.
Only host-observed checks against the pinned subject can support `PROVEN`; model-written paths,
commands, or summaries remain self-attestation.

## Pull request (required for `pr-ready` and beyond)

Purpose: deliver the prepared change and observe its review/check state without binding the skill to
one source-control provider or command-line client.

Supported operations are capability-advertised rather than assumed:

```yaml
operations:
  - open          # create the review request for an exact branch/revision
  - observe       # checks, review, comments, mergeability, head revision
  - respond       # reply to or resolve feedback when authorized
  - update_body   # apply composed evidence summary when supported
  - merge         # only after policy and human/automatic authorization
```

Opening returns a stable URL/reference and head revision. Observation returns structured checks,
reviews, feedback threads, and mergeability with provenance. If body composition is available, give
it phase artifacts and structured findings; provider-specific formatting and attribution belong to
the adapter. Without it, use a concise host-neutral summary and retain the underlying artifacts.

If the requested done state requires a pull request and this capability is unavailable, return
`stuck`. Never substitute an unreviewed direct push. A host that lacks write operations may still
observe an existing pull request.

## Release (conditionally required)

Purpose: determine release readiness and, after an authorized merge, observe the configured release
to the mission's requested environment.

```yaml
request:
  target_ref: <stable target reference>
  revision: <exact release revision>
  environment: production | staging | custom
  operation: preview-status | production-status | health | rollback-reference
result:
  status: green | red | pending | not-required | unavailable
  provider_ref: <optional opaque provider reference>
  evidence: [<build, deployment, health, or rollback reference>]
  note: <one-line classification>
```

When target metadata says no release exists and `done_state` is `merged`, use `not-required` and
finish after the authorized merge. When release evidence is part of `done_when`, an unavailable
capability blocks completion. Skills never infer provider credentials, status mappings, or health
URLs; the adapter owns those details.

## Prior-memory read (optional)

Purpose: retrieve a small set of confirmed, cross-session lessons relevant to the target and current
request before framing begins.

Conceptual request:

```yaml
target_ref: <stable repository or project reference>
ask: <mission.ask or the verbatim pre-intake request>
limit: <small positive integer>
```

Conceptual result:

```yaml
lessons:
  - id: <stable reference>
    scope: project | global
    text: <durable lesson>
    provenance: <optional source reference>
    recorded_at: <optional timestamp>
```

Treat every lesson as point-in-time context, not current repository fact. Re-check paths, flags, and
behavior before acting. If the capability is unavailable or fails, continue without prior lessons
and record that memory enrichment was skipped.

## Lesson proposal (optional)

Purpose: propose a few durable lessons after a mission settles. This capability does not grant the
skill direct authority to mutate shared memory.

Conceptual request:

```yaml
target_ref: <stable repository or project reference>
run_ref: <optional host run reference>
proposals:
  - scope: project | global
    text: <concrete reusable rule>
    evidence: [<artifact, finding, or event reference>]
```

Conceptual result:

```yaml
status: accepted | review-pending | unavailable
proposal_refs: []
```

Propose only lessons supported by run evidence: a correction, a failure and verified fix, or a
review finding that materially changed the work. Do not save task summaries, guesses, credentials,
or transient values. A host may require review before a project lesson is durable and should require
review before a global lesson affects unrelated projects. If the capability is unavailable or
fails, finish the mission and state that lesson capture was skipped.

## Adapter boundary

The portable kit contains the capability purposes and fallback rules above. Nightshift's concrete
workspace, browser runner, source-control client, PR-body composer, and release provider stay in the
private execution plane. Another host may supply different implementations without changing the
phase machine or handoff schemas.
