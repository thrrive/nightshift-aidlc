---
description: "Start a named Nightshift workflow through its portable workflow definition"
argument-hint: "<workflow-name> <request or mission-id>"
---

# /workflow

Load the `workflow` skill and follow it. Resolve the requested workflow from
`workflows/manifest.json`, load its definition, and delegate to the declared entry skill.

```text
$ARGUMENTS
```

Supported workflow names include `nightshift-aidlc` for a complete lifecycle mission and
`nightshift-missions-next` for one explicit next-subtask transition.
