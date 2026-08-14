# Changelog

All notable package changes are recorded here. Releases follow semantic versioning.

## Unreleased

- Add the host-neutral hierarchical mission workflow contract: ordered subtasks, gated versus YOLO
  continuation, per-step model planning, and estimate-versus-observed usage/cost publication.

## 1.0.0-rc.3

- Add the portable `cli/psdlc missions` command for parent missions and indented subtasks.
- Add multi-repository roots, status filtering, and JSON output to the mission view.
- Publish local Mission Control startup and terminal-view guidance in the package README.

## 1.0.0-rc.2

- Add the negotiated `aidlc-mission-bundle/v2` evidence format with one generated `MISSION.md`,
  hidden JSON/JSONL machine state, immutable mission identity, and explicit resume semantics.
- Record lifecycle attempts and rewinds plus distinct LLM/tool events with model, usage, cost source,
  duration, and explicit unavailable values; never translate missing attribution to zero.
- Add bundle/event schemas, collision/replay/redaction/uncertainty fixtures, negative-space checks,
  a reusable mission template, and a representative evaluation case.
- Keep v1 mission/outcome routing and the legacy peer-file Frame bundle compatible through explicit
  host format negotiation.

## 1.0.0-rc.1

- Freeze the stable v1 lifecycle candidate with unchanged canonical `mission`, `outcome`, and
  routing semantics.
- Add executable backward-compatibility checks for every valid handoff published in `0.1.0`.
- Document additive adoption of evidence-backed review and durable frame artifacts across hosts.

- Add one evidence-backed review contract shared by red-team, self-review, and change review.
- Require pinned review subjects, five independent adversarial lenses, explicit proof ceilings,
  stable finding IDs, remediation history, and residual-risk reporting.
- Fail closed on missing, malformed, partial, or all-error review evidence, while preserving work
  for human judgment after bounded remediation rounds.
- Add a versioned review schema and review-attestation capability without coupling skills to a
  model provider or execution host.
- Persist the complete frame bundle in a user-visible invocation workspace before plan approval;
  temporary files and conversation history can no longer be its only copies.
- Add a visible `nightshift/<mission-slug>/` fallback for projects without a feature-docs convention
  and fail honestly when no durable destination is authorized.

## 0.1.0

- Add deterministic conformance checks and representative router, frame, build, and land evals.
- Require schema-valid terminal handoffs and mutually exclusive routing fields.
- Prove local installation in Claude Code and Codex from the generated package.
- Complete a read-only frame mission and a browser-verified PR-ready mission from the package.

## 0.1.0-rc.1

- Freeze the v1 mission, outcome, and workstream schemas.
- Define host-neutral capabilities and explicit degradation behavior.
- Package the complete frame, build, verify, and land skill machine for Claude Code and Codex.
