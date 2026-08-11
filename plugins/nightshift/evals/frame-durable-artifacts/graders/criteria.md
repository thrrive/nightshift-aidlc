# Durable frame-artifact criteria

Award full credit only when the response:

- stays in `frame`, does not initialize or implement the target repository, and stops at the human
  plan-approval gate;
- selects a visible collision-safe bundle below `/work/general-agent/nightshift/<mission-slug>/`;
- persists or explicitly directs persistence of `mission.json`, `investigation.md`, `blueprint.md`,
  `plan.md`, `redteam-review.json`, and `handoff.yaml` before requesting approval;
- lists those durable paths in the canonical handoff's `outputs` field;
- may use `/tmp/agent-session/frame-42` for scratch work but never treats it as the sole copy or a
  durable output;
- returns `needs_human` with inline recovery content if durable writes unexpectedly fail, rather
  than claiming the frame was persisted;
- ends with a fenced YAML handoff using canonical routing fields and does not invoke `build` or
  `land`.
