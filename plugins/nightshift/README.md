# Nightshift AIDLC

Turn a product request into a reviewed, verified, deploy-ready change—without handing over the
decisions that need a human.

Nightshift is a portable skill kit for Claude Code and Codex. It gives an agent one durable mission
and a simple lifecycle:

```mermaid
flowchart LR
    subgraph I["Intake"]
        I1[Investigate] --> I2[Design + plan] --> I3[Red-team]
        I3 -. gap found .-> I1
    end
    subgraph B["Build"]
        B1[Implement] --> B2[Self-review] --> B3[Prove]
        B3 -. defect found .-> B1
    end
    subgraph L["Land"]
        L1[PR + delivery checks] --> L2[Evidence + feedback]
        L2 -. retry check .-> L1
    end
    I3 -->|you approve plan| B1
    B3 --> L1
    L2 -->|requested outcome proven| D[Done]
    B3 -. design gap .-> I1
    L2 -. code fix .-> B1
```

The plan is the last thing shown in Intake. You approve, refine, or reject it before any product
code is written. Each phase first works through its own bounded evidence loop; only a finding that
belongs to an earlier phase crosses the boundary.

## Start here

Install the plugin, then describe the change in plain language:

```text
/nightshift:aidlc Add CSV export to the holdings table. Include the active filters and verify it in the browser.
```

Nightshift will:

1. investigate the target and turn your request into an approval-ready plan;
2. stop and show that plan—nothing is implemented yet;
3. after approval, build in an isolated workspace, review its own work, and run the relevant proof;
4. drive the pull request and delivery checks to the outcome you requested.

Use `--frame-only` when you want a plan only, `--pr-only` when a reviewable PR is the finish line,
and `--no-verify` only when the target cannot be exercised in this run.

## Choose your path

| I want to… | Use | What happens |
| --- | --- | --- |
| Deliver a complete change | `/nightshift:aidlc <request>` | Runs Intake, waits for your plan approval, then Build and Land. |
| Get a plan before committing | `/nightshift:intake <request> --frame-only` | Investigates and presents an approval-ready plan. |
| Implement an already-approved plan | `/nightshift:build` | Makes one focused, verified reviewable change. |
| Finish a ready pull request | `/nightshift:land` | Drives checks, feedback, merge and configured delivery gates. |
| See where work stands | `/nightshift:missions` | Reads durable missions and identifies the next eligible action. |

`aidlc` is the lifecycle entrypoint; `intake`, `build`, `land`, and `missions` are the public
phase and status skills. The specialist skills that power them
(`investigate`, `blueprint`, `plan`, `redteam`, `implement`, `self-review`, `verify`,
`pr-drive`, and `release-gate`) are there when you need to customize a host or inspect the
workflow—not steps you need to memorize. `frame` remains a compatibility alias for existing
installations; new work should start with `intake`. `workflow` is an optional host dispatcher.

## Optional workflows

Use a workflow when your host supports named workflows and you want a stable, shareable name for
the lifecycle—not because it unlocks extra autonomy. The default `/nightshift:aidlc` command and
the `nightshift-aidlc` workflow use the same Intake → Build → Land gates. Workflows are especially
useful for team runbooks, a host-managed runner, or a paused mission that needs an explicit next
action.

Start a complete mission by workflow name:

```text
/nightshift:workflow nightshift-aidlc Add CSV export to the holdings table.
```

For a gated mission with approved child work, explicitly start one eligible child:

```text
/nightshift:workflow nightshift-missions-next <mission-id>
```

The first command announces the workflow and mission, then shows the same plan-approval gate as
the direct entrypoint. To see its durable output at any time, inspect the mission:

```text
/nightshift:missions
/nightshift:missions <mission-id>
```

The mission view reports the current phase and gate, child status, evidence location, observed
attempts and retry counts, and available model/cost metrics. Use the optional local Mission Control
browser below when a visual view of the same durable mission bundle is more useful. Workflows never
bypass plan approval, verification, review, merge, or release authorization.

## How it keeps you in control

| Moment | Nightshift does | You decide |
| --- | --- | --- |
| Before code | Investigates, designs, pressure-tests, and saves the plan. | Approve, refine, or reject the plan. |
| During delivery | Works in an isolated workspace, reviews the diff, and gathers evidence. | Scope changes and meaningful trade-offs. |
| At the finish line | Reads PR checks and configured delivery signals. | Merge and release authority, unless your policy delegates it. |

The mission and its evidence survive the chat in a durable bundle, so a resumed session can pick
up the real state instead of reconstructing it from conversation history. Read the
[complete lifecycle and skill reference](docs/lifecycle.md), the
[evidence-backed review contract](docs/review-contract.md), the
[durable frame-artifact contract](docs/frame-artifacts.md), and the
[human-first mission-bundle contract](docs/mission-bundles.md) when you need the full protocol.

## Install

**Latest release candidate:** [`v1.0.0-rc.14`](https://github.com/thrrive/nightshift-aidlc/releases/tag/v1.0.0-rc.14).
Use it when you want the Intake-first lifecycle and the simplified developer experience.

### Claude Code

```bash
claude plugin marketplace add thrrive/nightshift-aidlc
claude plugin install nightshift@nightshift-aidlc
```

### Codex

```bash
codex plugin marketplace add thrrive/nightshift-aidlc
codex plugin add nightshift@nightshift-aidlc
```

For a local checkout:

```bash
git clone https://github.com/thrrive/nightshift-aidlc.git
cd nightshift-aidlc
codex --plugin-dir plugins/nightshift
```

See [INSTALL.md](INSTALL.md) for host-specific setup and [COMPATIBILITY.md](COMPATIBILITY.md) for
the capability contract.

### Update to the latest release candidate

After the marketplace is installed, update and restart your agent host so it loads the new skills:

```bash
# Claude Code
claude plugin update nightshift@nightshift-aidlc

# Codex
codex plugin marketplace upgrade nightshift-aidlc
codex plugin remove nightshift@nightshift-aidlc
codex plugin add nightshift@nightshift-aidlc
```

For a reproducible Codex install pinned to this candidate, use
`codex plugin marketplace add thrrive/nightshift-aidlc --ref v1.0.0-rc.14`. See
[INSTALL.md](INSTALL.md) for the complete upgrade and local-checkout paths.

## Optional Mission Control

Mission Control is a local, read-only browser for durable mission state. It is never started
silently: when a host can launch it, Nightshift should ask whether you want it for this run. Most
terminal workflows do not need it; use it when a visual status view would help.

```bash
python3 control-plane/server.py --port 8091 --mission-root "$PWD"
```

Then open `http://127.0.0.1:8091/missions`. The dashboard reads local mission bundles; it does not execute
code or grant merge authority.

![Nightshift Mission Control: a local visual view of a mission and its evidence](https://github.com/user-attachments/assets/24ee2768-4df7-4da3-b84e-7914fc7d773f)

## What this package is—and is not

This repository contains the portable lifecycle skills, durable contracts, and optional local
mission browser. It works against many repositories and does not require a hosted control plane.
The full execution runtime—job orchestration, sandbox provisioning, target registry, and provider
integrations—belongs in a separately operated environment.

For the design thinking behind moving from one-off prompts to durable harnesses, see
[From Prompts to Harnesses](https://mihirsambhus.substack.com/p/from-prompts-to-harnesses).

## Contributing

Run the package checks before proposing a change:

```bash
python3 scripts/check_package.py
python3 scripts/check_schemas.py
python3 scripts/check_mission_bundles.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the [MIT License](LICENSE).
