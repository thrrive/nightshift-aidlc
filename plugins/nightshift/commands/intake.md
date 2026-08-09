---
description: "Turn a freeform change request into a structured mission (ask, done_state, done_when, halts)"
argument-hint: "<freeform request> [--frame-only] [--pr-only] [--no-verify]"
---

# /intake

Load the `intake` skill and follow it. Produce a `mission` from the request below, grounding
`done_when` in resolved target metadata. If the request is too vague to define done, return
2–3 sharp clarifying questions instead of guessing.

```text
$ARGUMENTS
```
