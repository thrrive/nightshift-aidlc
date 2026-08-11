# Red-team review protocol

Apply all five lenses separately. Record one row per lens using the shared review contract, even
when a lens is `not-applicable`; the note must explain why.

## 1. Requirements and correctness

- Map every `done_when` condition to an implementation step and observable check.
- Challenge edge cases, empty states, ordering, concurrency, error recovery, and downstream
  consumers.
- Flag silent multi-surface divergence unless the mission explicitly approves it.
- Look for scope that is missing, smuggled in, or too broad to review coherently.

## 2. Architecture and security

- Test trust boundaries, authorization, tenant/user isolation, secret handling, and hostile input.
- Examine cache keys, shared state, data retention, migration compatibility, and dependency seams.
- Ask what happens during partial deployment and whether the sequence remains reversible.
- Reject identifiers or external assumptions inferred without checking their authoritative source.

## 3. Tests and oracles

- Identify the repository-owned checks that touch each changed behavior and any stale expectation the
  plan must update.
- Name the concrete defect each important test should catch. A test name or green command is not
  enough if its assertions cannot detect the failure.
- Require golden fixtures to come from an independent prior behavior or approved specification, not
  from the implementation they are meant to validate.
- Plan a negative-space probe for high-risk behavior when practical: the reviewed behavior passes,
  while deliberately reversing the relevant change makes the named check fail for the right reason.

## 4. Delivery and operations

- Check migration/code ordering, backward compatibility, observability, rollback, and blast radius.
- Match the verification shape to the real surface: browser, API, CLI, library, or custom.
- Distinguish a check that will run from evidence that it already ran. Before implementation,
  behavioral proof remains future work.
- Ensure a half-deployed or failed verification path cannot be reported as success.

## 5. Adversarial lifecycle

- Model retries, duplicate events, interrupted runs, stale revisions, and conflicting concurrent
  changes.
- Challenge the plan from an attacker, operator, maintainer, and end-user perspective.
- Ask how the proposed remediation could create a new regression elsewhere.
- Identify paths the plan cannot prove and carry them as residual risk instead of hiding them.

## Round discipline

Keep finding IDs stable across rounds. A fixed finding records what changed and which updated plan
or blueprint was re-reviewed. Re-run the affected lens plus `adversarial-lifecycle`; do not clear a
finding because the author says it was addressed. After the host's bounded round limit, preserve the
ledger and return `CONDITIONAL`/`needs_human`.
