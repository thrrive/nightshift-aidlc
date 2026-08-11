---
name: release-gate
description: "land subskill. Combines pull-request checks, review, verification, and any configured release-provider evidence; holds for merge authorization; then observes the requested environment. Supports deploy and no-deploy targets without binding the lifecycle to one provider."
---

# /release-gate — decide release readiness

Decide when the change is ready for its authorized delivery step, hold the merge decision as a human
gate by default, and confirm the requested post-merge state when a release exists.

## Readiness signals

Read every signal through its host capability and retain evidence. Classify required signals
deterministically; model judgment must not turn an unknown signal green.

1. **Change checks** — all required checks for the exact head revision pass.
2. **Review** — repository policy's required approvals are satisfied and no blocking feedback is
   unresolved.
3. **Verification** — the latest approved verification shape passed for the exact head revision.
   `waived` counts only when `no-verify` is in `mission.halts`; `unproven` never counts as passed.
4. **Release preview** — when target metadata requires pre-merge release evidence, the release
   capability reports `green`. A target without a release uses `not-required`.

Treat `pending` as not ready and re-observe with bounded cadence. Treat `red` as evidence for a
focused rewind when code can fix it. Treat unavailable required evidence as `stuck`; do not erase a
requirement merely because the host lacks its capability.

## Merge decision

Default to a human gate. Return `needs_human` with the exact change reference and readiness evidence.
Merge only when repository policy and an explicit human or previously approved automatic policy
authorize the pull-request capability's merge operation. Never assume that observing a green change
also grants merge authority.

For a no-release target whose `done_state` is `merged`, complete after the authorized merge. Do not
invent a production observation step.

The current Nightshift runtime permanently refuses `auto_merge: true`: it has no harness-produced
attestation source that can justify an unattended merge. Keep every target on `auto_merge: false`
and require explicit human authorization. Treat the refusal as a fail-closed policy result, not a
pending signal and not a code defect to route through repeated builds.

## After merge

When `done_when` requires a released environment, request production or staging status plus health
evidence for the merged revision. Return completion only when those observable conditions are green.
On failure, return `stuck` with provider evidence and any adapter-supplied rollback reference.

## Output

```yaml
ready_to_deploy:
  pr_checks: green | red | pending
  review: approved | pending | changes-requested
  verify: passed | failed | unproven | waived | pending
  release_preview: green | red | pending | not-required | unavailable
merge: needs_human | merged | auto-merged
observed:
  environment: production | staging | custom | not-required
  stable: true | false
  evidence: []
note: <one-line status>
```

Provider adapters may attach namespaced evidence fields, but portable routing uses the fields above.
