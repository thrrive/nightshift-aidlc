---
name: pr-drive
description: "land subskill. Uses the host pull-request capability to monitor checks, review feedback, and mergeability; validates each item; and returns fix, respond, rewind, or human-decision outcomes until the change is ready or concretely blocked."
---

# /pr-drive — keep the reviewed change moving

Drive the pull request or equivalent reviewed change until it satisfies repository policy or is
blocked on a concrete decision. Read and write review state only through advertised pull-request
capability operations; do not assume a provider or command-line client.

## Observe

Request structured state for the exact change reference and retain evidence:

- required checks and logs for failures;
- review decision, requests, comments, and unresolved threads;
- automated-review findings and their effective reviewers;
- mergeability, branch policy, and exact head revision.

Use a material-change monitor when supported. Otherwise poll with bounded cadence. Never silently
spin, guess reviewer intent, or treat absence of a durable monitor as completion.

## Triage each item

Validate feedback against the approved plan, diff, repository rules, check evidence, and latest
verification.

- **Fix** — actionable and in scope: return a focused build rewind with evidence. In YOLO mode,
  apply the bounded recovery policy and continue automatically while the finding remains in scope.
- **Respond** — incorrect, duplicate, already handled, or out of scope: request a supported reply
  operation with evidence.
- **Rewind** — changes the goal or exposes a design gap: route to the owning phase.
- **Escalate** — requires a product, risk, policy, or authorization decision: `needs_human`. A
  repeated or disputed finding also escalates instead of looping indefinitely.

Rerun a likely infrastructure flake at most once when the capability supports it. A missing secret,
provider outage, or unavailable write operation is a blocker, not a code fix.

## Review-response trail

When authorized reply and body-update operations exist, connect each fixed finding to its follow-up
revision and resolve the originating thread. Keep the structured finding record authoritative;
provider-specific body formatting belongs to the adapter. If write operations are unavailable,
return the response actions as outputs rather than pretending they were posted.

## Output

Return the change URL/reference, head revision, check status, review status, mergeability, evidence,
and any focused rewind or human decision required.
