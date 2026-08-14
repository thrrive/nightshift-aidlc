# The handoff contract

Every phase in the loop is a self-contained step that reports back to the orchestrator with a
single structured **handoff**. The orchestrator never reaches inside a phase; it only reads the
handoff and decides where to go next. This is what lets the same loop run identically across
different agent runtimes and different target repos.

The versioned, machine-readable v1 definitions and compatibility fixtures live in
[`schemas/aidlc/v1/`](../schemas/aidlc/v1/). This document explains their lifecycle semantics;
the schemas are the cross-process shape contract.

Two objects flow through the system: the **mission** (the durable goal, set once and carried
unchanged) and the **outcome** (a phase's per-step report).

Durable evidence may use the version-negotiated [human-first mission bundle](mission-bundles.md).
This does not add fields to the canonical `mission` or change `outcome` routing. The bundle records
attempts, transitions, model/tool provenance, cost availability, and a generated `MISSION.md`
outside the wire handoff.

For hosts that support hierarchical execution, the bundle may additionally persist a bounded
`subtask_plan`, `model_plan`, `execution_mode`, and resumable workflow state. These are execution
metadata, not replacements for the canonical mission or outcome. `model_plan` estimates must be
clearly separated from the host-observed usage ledger.

## `mission` — the durable goal

```yaml
mission:
  ask: <the user's request, in their own words, verbatim>
  done_state: stable-production | merged | pr-ready | frame-approved | staging-stable | custom
  done_when:
    - <an observable condition that proves done_state is reached>
  halts: []          # explicit early-stop flags, e.g. ["frame-only"], ["no-verify"]
```

- `ask` is never rewritten. Phases derive work from it but must not silently narrow it.
- `done_state` defaults to **`stable-production`**. It is only lowered when the user explicitly
  asks for a narrower outcome (a flag, "plan only", "open a PR but don't merge", etc.).
  `merged` is the no-deploy terminal: for a target with no `deploy:` block, land drives the PR
  green (skipping the absent Railway signal), then the control plane merges it host-side — no
  deploy gate and no production observation.
- `done_when` is the checklist the orchestrator uses to decide the mission is actually complete
  — not "the last phase returned advance", but "these conditions are observably true".

## `outcome` — a phase's report

```yaml
mission: { ... }     # echoed back unchanged
outcome: advance | rewind | needs_human | stuck
then: frame | build | land | complete      # where to go when outcome == advance
rewind_to: investigate | blueprint | plan | redteam | build   # when outcome == rewind
outputs: []          # durable artifacts or user-visible paths the phase produced
note: <one-line result summary>
blockers: []         # concrete blockers when outcome == stuck
links:
  pr: <url>
  commits: []
  deploy: <url or run id>
```

### Outcome meanings

| `outcome` | Meaning | Orchestrator does |
|---|---|---|
| `advance` | Phase finished cleanly | Go to `then`. If `then` needs a human gate, ask first, then continue. |
| `rewind` | An earlier step must redo work | Re-enter the phase that owns `rewind_to` with the reason. |
| `needs_human` | A specific human decision/action is required | Ask exactly that, then resume the same phase. |
| `stuck` | No useful next step the agent can take | Surface the blocker + smallest next step and stop. |

## `workstreams` — the parallel-decomposition contract (optional)

A frame handoff **may** carry a `workstreams` block when the plan decomposes into independent
work items that sub-agents can build concurrently (#44). Absent means a single-agent build —
every handoff written before this block existed stays valid forever. Present means strictly
validated: this block authorizes parallel writers, so every ambiguity is rejected at plan time,
before any fan-out exists.

```yaml
workstreams:
  version: 1
  merge_strategy: ordered        # the only strategy in v1; merge order == items order
  items:
    - id: api-layer              # ^[a-z0-9][a-z0-9-]{0,31}$, unique — becomes the
                                 # ws/<id> branch and the event lane tag
      goal: <one-sentence independent work item>
      paths: [src/api/, tests/api/]   # ownership, component-wise prefixes
      model_hint: null           # reserved: a model registry id, consumed by live
                                 # fan-out; sits BELOW the per-job --model pin
                                 # (job pin > model_hint > segment routing)
```

- **Ownership is component-wise prefix, and disjoint.** `src/api` owns `src/api/handlers.py`
  but not `src/api-v2`. No path may be a component-wise prefix of another, within or across
  items — two sub-agents must never own the same files. Globs, `..`, absolute paths, and
  `.git` components are rejected. Existence is deliberately not checked: the work legitimately
  creates new paths.
- **Bounded by default:** at most 8 items. Runtime concurrency is the runner's concern, not the
  contract's — the block declares work, not parallelism.
- **Merge is ordered and never forced.** The executor merges `ws/<id>` branches back onto the
  job's single branch in items order (`--no-ff`); a conflict aborts to a clean tree and returns
  as a finding. Disjoint ownership cannot prevent every textual conflict (shared artifacts like
  lockfiles) and an ordered merge can be textually clean yet semantically stale — which is why
  self-review and verification always run on the **merged** result.
- **The spine is untouched:** one mission, one handoff per phase, one PR per job. Sub-agents are
  an execution detail inside a phase, never a fork of the lifecycle.
- **Schema plus semantic validation:** JSON Schema validates the block's shape, bounds, identifier
  format, and basic path safety. Unique IDs and pairwise, component-wise ownership disjointness
  remain runtime semantic checks because JSON Schema cannot compare one item property with every
  peer property.

## Rules the whole system relies on

1. **One owner of transitions.** Only the `aidlc` orchestrator moves between major phases. A
   phase may compose its own subskills, but it must never call a sibling major phase — it
   returns `advance`/`rewind` and lets the orchestrator route.
2. **`advance` is routing, not completion.** A phase returning `advance` with a non-`complete`
   `then` means "keep going" — the orchestrator continues unless a human gate, a `halts` flag,
   or a real blocker applies. Opening a PR is a waypoint, not the finish line, unless
   `done_state` is `pr-ready`.
3. **Human gates pause, they do not shrink the mission.** In gated mode, routine plan and
   between-child approvals pause. In YOLO mode, routine transitions auto-advance; only meaningful
   scope, safety, policy, unresolved-review, blocker, or exhausted-budget decisions surface to a
   human. After the human answers, work resumes toward the same `done_state`.
4. **Completion is checked against `done_when`.** The orchestrator only finishes when `then`
   is `complete` *and* every `done_when` condition is observably satisfied.
5. **Frame outputs survive the gate.** Before plan approval, `outputs` names the durable mission,
   investigation, blueprint, plan, red-team review, and handoff references defined in
   [`frame-artifacts.md`](frame-artifacts.md). Scratch or conversation-only references do not
   satisfy this field unless the user explicitly accepts an inline-only review.
6. **Evidence never rewrites routing.** In a v2 mission bundle, `.aidlc/latest-outcome.json` is the
   current validated routing snapshot and `events.jsonl` is append-only audit evidence.
   `MISSION.md` is generated for humans and is never parsed to decide the next phase.

See [`lifecycle.md`](lifecycle.md) for how the phases compose into the loop.
