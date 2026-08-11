# Evidence-backed review contract

Red-team, self-review, and reviewed-change agents examine different artifacts, but they use the
same vocabulary for evidence and decisions. This contract makes a review inspectable without
binding the skills to a model provider, agent SDK, source-control service, or execution plane.

The machine-readable shape is [`schemas/aidlc/v1/review.schema.json`](../schemas/aidlc/v1/review.schema.json).
A review record may extend a phase outcome under `review`; it never replaces the canonical
`mission` and `outcome` routing fields.

## Review stages and subjects

| Stage | Subject that must be pinned | What the decision means |
|---|---|---|
| `redteam` | the exact blueprint and plan artifacts | the proposed work is coherent enough for human plan approval |
| `self-review` | the exact base/head revision or equivalent diff | the implementation is ready for independent verification and reviewed delivery |
| `change-review` | the exact reviewed-change revision | the observed revision has no unresolved review blocker |

Record stable subject references. For a diff, include both base and head revisions when the host
can resolve them. A review of an unknown or moving subject is `CONDITIONAL`, never `PASS`.

## Independent lenses

Every review covers these five lenses. Independence means a deliberate second perspective, not
necessarily five model calls. A host may assign lenses to fresh-context agents or different model
families; a single capable reviewer may run them separately when fan-out is unavailable.

1. `requirements-correctness` — requirements, invariants, edge cases, consumers, and scope.
2. `architecture-security` — boundaries, authorization, isolation, compatibility, and rollout.
3. `tests-oracles` — test coverage and whether assertions would detect the predicted defect.
4. `delivery-operations` — checks, observability, migration order, rollback, and release behavior.
5. `adversarial-lifecycle` — partial failure, concurrency, hostile inputs, and regressions caused by
   remediation itself.

Mark a lens `partial`, `failed`, or `not-applicable` explicitly. Do not turn a missing reviewer,
tool error, empty response, or malformed response into clean evidence.

## Claims and proof states

State the important claims a decision relies on. A core claim names its boundary, the proof it
requires, and the evidence actually observed.

| State | Meaning |
|---|---|
| `REFUTED` | observed evidence contradicts the claim |
| `UNPROVEN` | required evidence is absent or cannot be evaluated |
| `STATIC_ONLY` | repository or artifact inspection supports the claim, but behavior did not run |
| `PARTIAL` | relevant behavior ran, but coverage, binding, or sensitivity is incomplete |
| `PROVEN` | the host observed a behavior-sensitive check against the pinned subject |

`PROVEN` is deliberately narrow. A model citing a path, command, or prose report is self-attestation,
not proof that the command ran or that its oracle was capable of failing. Static claims may require
only `STATIC_ONLY`; behavior claims must not be promoted past the strongest host-observed evidence.
The record's `proof_ceiling` is the strongest state the evidence source can honestly support.

For changed tests, name the concrete defect each important assertion should catch. When practical,
use a negative-space probe: demonstrate that the check passes on the reviewed subject and fails
when the relevant behavior is deliberately reversed or removed. A collection or compilation error
does not count as a killed defect; classify the probe as unproven.

## Findings and remediation

Every finding has a stable ID, severity, lens, locus, evidence, and disposition. Keep the same ID
through subsequent rounds. A fix records what changed and the subject on which the fix was
re-reviewed; it does not disappear from history. `accepted-risk` requires an explicit residual risk
and human authority when the finding could affect the mission's done state.

After remediation, review the changed surface again and check for regressions introduced by the
fix. A previous clean statement cannot clear a later revision.

## Decision rules

- `REQUEST_CHANGES` when a core claim is `REFUTED` or a blocking/high finding remains open. Route
  to the earliest place that can safely resolve it.
- `CONDITIONAL` when parsing is incomplete, required lenses or evidence are missing, the reviewed
  subject is not pinned, a core claim is unproven, or an accepted residual needs human judgment.
- `PASS` only when the record is complete, every required lens ran or has a justified exclusion,
  required claim proof meets its declared level, and no blocking/high finding remains open.

A plan review may pass with a `STATIC_ONLY` ceiling because it decides plan coherence, not whether
future code already works. A behavioral implementation claim cannot pass on static inspection
alone. When bounded review/remediation rounds are exhausted, preserve the artifacts and return
`needs_human`; never silently convert the last result to a pass.

## Review-council compatibility

Nightshift may use a richer review-council artifact internally to retain per-reviewer outputs,
disagreement, and convergence history. That artifact is an execution detail, not a second public
decision system. Its aggregate maps to `change-review` here: reviewer claims use the same proof
states, unresolved disagreement becomes `CONDITIONAL`, a supported blocking objection becomes
`REQUEST_CHANGES`, and only a complete aggregate may become `PASS`.

The mapping is intentionally one way. A host may preserve more provenance than this portable
record requires, but it must not discard uncertainty, raise a proof state, or turn missing council
evidence into a pass while projecting the aggregate into the shared contract.
