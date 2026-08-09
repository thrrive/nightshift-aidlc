---
description: "Run the full AI SDLC loop: frame, build with appropriate verification, then drive the reviewed change to its requested done state"
argument-hint: "<what to build> [--frame-only] [--pr-only] [--skip-frame] [--no-verify]"
---

# /aidlc

Load the `aidlc` skill via the active runtime's skill mechanism and follow it as the source of
truth for the lifecycle. Default goal is **stable production**; do not treat opening a PR as
completion unless `--pr-only` (or equivalent wording) was given.

Request:

```text
$ARGUMENTS
```

If the request is missing the target repo or is too vague to define "done", run `intake` first
(or ask for the smallest specific missing input). Do not reimplement lifecycle logic here —
delegate to the skill so per-repo/user overrides keep working.
