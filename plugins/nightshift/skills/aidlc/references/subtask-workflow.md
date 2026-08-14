# Hierarchical mission workflow

When the host supports hierarchical execution, intake and frame produce a bounded ordered
`subtask_plan` after the mission is clear and the parent plan is approved. Each child has an id,
goal, observable `done_when`, and dependencies only on earlier children. The orchestrator starts
the first eligible child and resumes the exact mission using its `mission_id` and `bundle_ref`.

The default mode is `gated`: after each child completes, persist its summary and pause for
`proceed`, `stop`, or `revise`. `mode: yolo` removes only these between-child summary gates. It
does not bypass plan approval, verification, review, merge, or release gates; blocked children
still stop the mission. Existing parallel workstreams remain an explicit opt-in and are not
silently converted into sequential subtasks.

## Model planning and usage

Intake classifies each execution step using complexity, context size, reasoning needs, gate or
review sensitivity, cache opportunity, and cost ceiling. It records a `model_plan` beside the
subtask plan:

```yaml
model_plan:
  - subtask_id: inspect
    step: investigate
    model_hint: balanced
    rationale: broad repository context, low implementation risk
    estimate: {input_tokens: 12000, output_tokens: 3000, cost_usd: 0.08}
    pricing_ref: provider-catalog-2026-08
```

Estimates are planning data, not spend. The host records an append-only usage ledger for every
physical model attempt: requested and resolved model, phase/step/subtask, input/output/cache
tokens, cost, pricing source, and availability. Unknown values remain `unavailable`; never
invent a token count or a zero-dollar cost. Published `MISSION.md` results should show planned
estimates separately from observed totals, with per-model and per-step breakdowns and variance
when both sides are known.

Claude hosts may use skills plus subagent/task surfaces; Codex hosts may use plugin skills plus
subagent, app-server, or CLI surfaces. Adapters select tools without changing this persisted
bundle contract.
