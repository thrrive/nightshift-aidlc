---
name: land
description: "Major SDLC phase after a reviewable change exists. Drives checks and feedback, keeps verification current, evaluates configured release evidence, holds for merge authorization, and observes the requested post-merge state."
---

# /land — reviewed change to requested done state

Own the change from an open review through `mission.done_state`. Default completion is stable in the
requested environment, not merely green checks or a merge.

Compose `pr-drive`, `verify`, and `release-gate`; never call `build` or `frame`. Return `rewind` and
let the orchestrator route earlier work.

## Inputs

- the unchanged `mission` and pull-request/change reference;
- approved plan, rollout notes, and latest verification evidence;
- resolved target metadata;
- pull-request and, when applicable, release capabilities.

## Process

1. Run **pr-drive** through the pull-request capability. Observe checks, review, feedback,
   mergeability, and the exact head revision.
2. Re-run **verify** when the reviewed revision changes.
3. Classify red evidence:
   - in-scope defect → `rewind` to `build` with the evidence;
   - design or product gap → `rewind` to `frame`;
   - external or policy decision → `needs_human`;
   - unavailable required capability → `stuck`.
4. Continue observing while a required signal is pending. If no durable monitor exists, return
   `needs_human` with the exact resume condition.
5. Run **release-gate** when checks, review, and verification are ready for delivery evaluation.
6. Hold for merge authorization unless an explicit approved policy permits automatic merge.
7. After merge, complete immediately for a no-release `merged` mission. Otherwise observe the
   configured release and health evidence until every `done_when` condition is satisfied.

The current Nightshift runtime does not expose an approved automatic-merge policy. It refuses every
target configured with `auto_merge: true` because no harness-produced attestation source exists.
Keep targets on `auto_merge: false` and require the human merge gate; this is a fail-closed policy,
not a pending readiness signal.

## Completion handoff

```yaml
mission: { ... }
outcome: advance | rewind | needs_human | stuck
then: complete                                      # include only for advance
rewind_to: investigate | blueprint | plan | redteam | build  # include only for rewind
note: <review, merge, release, and stability result>
links:
  pr: <review URL>
  deploy: <optional release evidence URL or reference>
ready_to_deploy:
  pr_checks: green | red | pending
  review: approved | pending | changes-requested
  verify: passed | failed | unproven | waived | pending
  release_preview: green | red | pending | not-required | unavailable
observed:
  environment: production | staging | custom | not-required
  stable: true | false
  evidence: []
```

`then` and `rewind_to` are mutually exclusive. Omit the inapplicable field entirely; never emit it
as `null`. Design or plan gaps rewind to their owning `frame` subskill; code-fixable findings rewind
to `build`.
