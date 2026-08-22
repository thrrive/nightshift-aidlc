---
name: frame
description: "Major SDLC phase that turns a mission into an approved implementation plan. Composes investigate → blueprint → plan → redteam, produces the plan and definition of done, and returns a handoff for the human plan-approval gate. Does not write product code."
---

# /frame — requirements to an approved plan

Own the pre-implementation phase. Do **not** edit product code, commit, push, or open PRs.

`frame` composes its own subskills but must not call `build` or `land`. Return a handoff and let
the `aidlc` orchestrator route the next major phase.

## Process

1. Resolve one durable frame bundle using the
   [`frame-artifact contract`](../../docs/frame-artifacts.md). Pass that same bundle reference to
   every subskill and reuse it after clarification or rewind. Prefer
   `aidlc-mission-bundle/v2` when the host advertises it; otherwise use the compatible v1 peer-file
   bundle. A fresh invocation omits `resume_ref` and must receive a newly, exclusively allocated
   mission ID. Never infer resume from a matching slug.
2. Run **investigate** with the mission. Capture requirements, current state, prior art, repo
   conventions, constraints, and open questions.
3. **Clarify before designing.** Review the open questions investigate surfaced. If any are
   genuine ambiguities that change the shape of the work — unclear scope, undefined acceptance,
   more than one plausible interpretation, or an assumption that would be expensive to get wrong
   — resolve them *before* blueprint or plan. Bias toward asking: a wrong mission costs far more
   than one round of questions. Skip this round only when scope and acceptance are already
   unambiguous.
   - **When an operator is present (a command-line / interactive session):** put the questions to
     the user directly and wait for the answers before continuing. Keep them sharp — 2–4 questions
     a one-line answer resolves, each grounded in what investigate found (name the real files and
     surfaces), never an open-ended "tell me more". Fold the answers into the requirements, then
     proceed.
   - **When no operator can answer (headless run):** do not block. Proceed under the most
     reasonable interpretation, record both the questions and the assumptions you chose in the
     investigation output, and carry them in the handoff `note`/`blockers` so a human can correct
     course at the plan-approval gate.
   If a genuinely blocking unknown remains that you cannot answer or reasonably assume, return
   `needs_human` with the specific questions instead of designing on a guess.
4. Run **blueprint** with the investigation output. It produces the technical approach:
   components touched, data/contract changes, rollout + observability expectations, and the
   **verification shape** (browser, API, CLI, library, or custom) and its observable pass condition.
5. Run **plan** with the investigation + blueprint. It produces the human-approvable
   implementation plan and the definition of done.
6. Run **redteam** over the pinned plan + blueprint using the shared evidence-backed review
   contract. Rewind material gaps, hold incomplete evidence for human judgment, and finalize only
   after remediation is re-reviewed.

When the approved plan contains independent, path-disjoint work, declare validated `workstreams`
in the handoff and include bounded recovery limits plus meaningful-human escalation triggers from
[`../aidlc/references/execution-workflow.md`](../aidlc/references/execution-workflow.md).

Use subagents or background work where the runtime supports it, but the phase's result is a
single handoff. Enter each subskill by invoking it through the runtime's skill mechanism rather
than paraphrasing its text inline — the invocation is the step boundary the runtime records, and
it is what makes per-step attribution, timing, and overrides work downstream.

With a v2 bundle, request a safe event append at every subskill entry and exit, clarification,
rewind, review, and approval gate. Increment the step attempt on re-entry and preserve prior review
records. Refresh the generated `MISSION.md` after every material event. If the host cannot expose
per-call model, token, cost, or duration data, record explicit unavailable provenance rather than
omitting the logical step or rendering zero.

For a v1-only direct run, append the equivalent lifecycle and step records to the bundle-root
`events.jsonl` fallback. Include `subtask_id` and `step_attempt` for child work and retries, and
record observed model, token, duration, and cost fields for physical model calls; unknown values
remain explicitly unavailable.

## Artifacts

Before requesting plan approval, persist the selected format completely. In v2, confirm that
`MISSION.md`, `.aidlc/bundle.json`, `.aidlc/mission.json`, `.aidlc/events.jsonl`,
`.aidlc/latest-outcome.json`, and the immutable review attempt exist. In v1, persist
`mission.json`, `investigation.md`, `blueprint.md`, `plan.md`, `redteam-review.json`, and
`handoff.yaml`, and for a direct v1 run `events.jsonl`. Prefer a target-declared feature-docs location; otherwise use the selected
invocation-root fallback. Scratch, temporary, or conversation-only content is not the durable copy.
If no durable write is available, return `needs_human` with inline recovery content and ask for a
destination or explicit waiver. Tell the user the exact human document and machine root at the gate.

## Completion handoff

```yaml
mission: { ... }            # unchanged
outcome: advance | rewind | needs_human | stuck
then: build                                      # include only for advance
rewind_to: investigate | blueprint | plan | redteam  # include only for rewind
outputs: [ <durable mission + investigation + blueprint + plan + review + handoff paths> ]
note: <the plan in a sentence, plus the top risk>
blockers: []
review: { ... }             # red-team record for the finalized plan
rollout:
  target_environment: <production | staging | custom>
  deploy_path: <known, or "needs discovery">
  verify_shape: <what a passing check for this change looks like>
```

`then` and `rewind_to` are mutually exclusive. Omit the inapplicable field entirely; never emit it
as `null`.

When the plan is complete, return `outcome: advance` with `then: build`. Do **not** return
`needs_human` solely for routine plan approval; reserve it for a specific unresolved question or
action inside `frame`. `advance` means a human can now approve, refine, or reject the plan — it does
**not** mean implementation may begin. The orchestrator halts for that approval. Once approved, the
loop continues toward `mission.done_state`; approval is not implicitly scoped to "just open a PR"
unless the plan or the user says so.
