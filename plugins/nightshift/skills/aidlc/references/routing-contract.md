# AIDLC routing contract

Read this reference before routing the lifecycle. Keep phase work inside the resolved phase skill;
the orchestrator alone owns transitions between major phases.

## Mission mapping

Adopt an existing intake mission or create this shape once:

```yaml
mission:
  ask: <the user's request, verbatim>
  done_state: stable-production | merged | pr-ready | frame-approved | staging-stable | custom
  done_when:
    - <observable condition that proves done_state>
  halts: []
```

Map lifecycle flags exactly:

- `--frame-only` sets `done_state: frame-approved`.
- `--pr-only` sets `done_state: pr-ready`.
- `--merged` sets `done_state: merged`; drive the reviewed change green, then request or perform
  the authorized merge for a target without a release requirement.
- `--no-verify` adds `"no-verify"` to `halts`.
- `--skip-frame` enters at `build` and is valid only when an approved plan is already in context.

Do not put host execution, cache, concurrency, or performance options in `mission` or `halts`.

## Transition loop

```text
phase = frame by default; build only for a valid --skip-frame mission
while the mission is not complete:
    h = run(phase) with the unchanged mission and current artifacts

    if h.outcome == "advance":
        if h.then == "complete":
            confirm every mission.done_when condition, then finish
        else if entering h.then crosses a human gate:
            request the gate; after approval, phase = h.then
        else:
            phase = h.then

    elif h.outcome == "rewind":
        phase = the major phase that owns h.rewind_to

    elif h.outcome == "needs_human":
        request the specific decision or action, then re-run the same phase

    elif h.outcome == "stuck":
        report the blocker and smallest useful next step, then stop
```

## Phase ownership and gates

1. `frame` owns `investigate`, `blueprint`, `plan`, and `redteam`. It returns the approved-plan
   candidate. Halt for human approval before `build`; complete here for `frame-approved`.
2. `build` owns implementation, self-review, and verification. It produces one reviewable change.
   Complete here for `pr-ready` only after the change exists and verification is green.
3. `land` owns checks, review, current verification, merge authorization, and configured release
   evidence. Complete only when every `done_when` condition is observably true.

Route `rewind_to: investigate | blueprint | plan | redteam` to `frame`; route
`rewind_to: build` to `build`.

In gated mode, plan approval before `build` and the between-child proceed gate are routine human
gates. In `mode: yolo`, those routine gates auto-advance. Surface a human decision only for a
meaningful scope diversion, safety or policy decision, unresolved red-team or code-review finding,
blocked or ambiguous execution, exhausted recovery budget, or a merge/release authorization that
the target policy does not permit the host to automate. A gate pauses the mission; it never shrinks
or rewrites it.

For `done_state: frame-approved`, ask the user to approve, refine, or reject the plan. Once they
approve it, return `outcome: advance` with `then: complete`; never enter or offer `build` for that
mission. Before approval, preserve the completed `frame` handoff (`outcome: advance`, `then: build`)
as the machine-readable phase result while the orchestrator holds the gate. Its `outputs` must name
the durable frame bundle from [`docs/frame-artifacts.md`](../../../docs/frame-artifacts.md); an
operating-system temporary directory, agent scratch area, or conversation-only result cannot open
the routine approval gate without an explicit user waiver.
