# Changelog

All notable package changes are recorded here. Releases follow semantic versioning.

## Unreleased

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
