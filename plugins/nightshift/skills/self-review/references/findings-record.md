# Self-review findings and remediation record

Emit the full shape defined by the shared
[`review contract`](../../../docs/review-contract.md) and its
[`review.schema.json`](../../../schemas/aidlc/v1/review.schema.json). Set `stage` to `self-review`
and `reviewed_subject.kind` to `revision-diff`.

## Required self-review content

- Put the exact base/head revisions in `reviewed_subject` when the host resolves them. Otherwise
  identify the stable equivalent in `refs` and cap the decision at `CONDITIONAL` if it can move.
- Include all five lens rows. `not-applicable` requires a specific reason; it is not a shortcut for
  omitted inspection.
- State at least one `core` claim for each material `done_when` condition. Claims about executed
  behavior require `executed` or `behavior-sensitive` proof.
- Set `proof_ceiling` to the strongest state the observed evidence can support, never the desired
  verdict.
- Use stable finding IDs across implementation/review rounds. A fixed finding retains its original
  text and evidence, records the remediation, and names the revision in `verified_on`.
- Put accepted uncertainty in `residual_risks`. A high or blocking accepted risk requires human
  judgment and a `CONDITIONAL` decision.
- Put a one-sentence implementation summary in `build_summary`; keep the decision rationale in
  `note`. The host may use the summary when composing reviewed-change evidence.

## Decision audit

Before returning `PASS`, confirm all of the following:

1. `parse_status` is `complete`, `evidence_complete` is true, and the subject is pinned.
2. Every required lens is complete or has a defensible `not-applicable` reason.
3. No core claim is `REFUTED` or `UNPROVEN`; each claim meets its declared proof requirement.
4. No blocking/high finding is `open`, `rewind`, or accepted without human authority.
5. Every fixed blocking/high finding was re-reviewed on the current subject.
6. The strongest proof state does not exceed what host-observed evidence supports.

If any condition fails, return `REQUEST_CHANGES` when additional implementation or frame work can
resolve it; otherwise return `CONDITIONAL` and request the smallest human decision or missing proof.
