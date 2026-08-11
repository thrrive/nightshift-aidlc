---
name: self-review
description: "build subskill. Runs an evidence-backed fresh-context review of the exact diff, remediates in-scope defects, and rewinds plan or design gaps before reviewed delivery."
---

# /self-review — make the diff earn delivery

Review the exact working diff against the approved plan and `mission.done_when`. Prefer a
fresh-context reviewer when the host supports one; otherwise separate the review deliberately and
record `same-session`. Never imply independent review that did not occur.

Read and follow [`references/findings-record.md`](references/findings-record.md). Use the shared
[`review contract`](../../docs/review-contract.md) for proof states, lenses, decision rules, and the
machine-readable record.

## Process

1. Pin the reviewed base/head revisions or equivalent immutable diff. A moving or unknown subject
   is `CONDITIONAL`, not clean.
2. Map every approved requirement to the changed implementation, affected consumers, and relevant
   checks. Inspect for omitted surfaces as well as erroneous changed lines.
3. Run the five review lenses. Include security/isolation, rollout/observability, diff hygiene,
   compatibility, error paths, and adversarial lifecycle behavior.
4. Examine test oracles, not just test presence. State the concrete defect each important changed
   test would catch and use a negative-space probe for high-risk behavior when practical.
5. Bind behavioral claims only to checks the host observed against the pinned subject. A cited
   command, path, or model-written report cannot promote a claim to `PROVEN`.
6. Give each finding a stable ID and disposition. Return in-scope defects to `implement`; route an
   unsafe approved-plan assumption to the earliest frame artifact that can resolve it.
7. Re-review every fix on the new subject and check that remediation did not create another gap.
   Preserve the full finding history.

## Routing

- `PASS` → return `advance` to verification and reviewed delivery.
- `REQUEST_CHANGES` → return `rewind` to `implement`, `blueprint`, or `plan` with the evidence-bound
  findings.
- `CONDITIONAL` → return `needs_human` when the review subject, output, required evidence, or
  accepted residual prevents an honest decision.

Unavailable checks are `UNPROVEN`. Missing, malformed, partial, or all-error reviewer output holds
the gate. After bounded remediation rounds, preserve the reviewable work and return `needs_human`;
never silently convert the last result to a pass.
