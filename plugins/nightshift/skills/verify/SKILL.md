---
name: verify
description: "Proves a change with the target's approved verification shape: browser, API, CLI, library, or custom. Used by build and kept current by land. Returns structured evidence, rewinds on a product failure, and reports unavailable execution as unproven rather than passed."
---

# /verify — prove the changed behavior

Own the question "does this exact revision satisfy the approved acceptance conditions?" Use the
host's verification capability and retain structured evidence. Do not assume every target is a web
application or that every host uses the same runner.

## Process

1. Read the plan's verification shape and observable acceptance conditions.
2. Resolve the target's declared verification implementation. Prefer repo-owned checks and specs so
   proof versions with the product change.
3. Request verification for the exact `workspace_ref` and revision:
   - `browser` for a user-facing web flow;
   - `api` for request/response behavior;
   - `cli` for command behavior and exit/output contracts;
   - `library` for public API and integration behavior;
   - `custom` only when the plan explains why the standard shapes do not fit.
4. Classify the structured result:
   - acceptance conditions all proven → `advance`, `status: passed`;
   - product behavior is wrong → `rewind` to `build`, `status: failed`;
   - the capability, dependencies, environment, or target cannot execute → `stuck`,
     `status: unproven`, with the smallest useful next step.
5. Retain reports, logs, traces, screenshots, and other returned evidence references in the handoff.

If `"no-verify"` is in `mission.halts`, do not invoke the capability. Return `advance` with
`status: waived` and state that the user explicitly waived verification. No other condition may be
reported as waived.

An unavailable or failed verification capability is `unproven`, never `passed`. Do not replace the
approved check with an easier one merely because the intended implementation is unavailable.

## Handoff

```yaml
mission: { ... }
outcome: advance | rewind | stuck
rewind_to: build
note: <what passed, failed, or could not run>
verify:
  shape: browser | api | cli | library | custom
  status: passed | failed | unproven | waived
  checks: []
  evidence: []
```

## Data-isolation check

When the target stores scoped user, tenant, household, or organization data, include at least one
verification assertion that data remains inside the approved scope. Treat a failure as a
stop-the-line product defect, not a flaky check.
