# Durable frame-artifact criteria

Award full credit only when the response:

- stays in `frame`, does not initialize or implement the target repository, and stops at the human
  plan-approval gate;
- selects the visible collision-safe bundle
  `/work/general-agent/nightshift/missions/<mission-slug>--mission-frame-42/`;
- persists or explicitly directs persistence of `MISSION.md`, `.aidlc/bundle.json`,
  `.aidlc/mission.json`, `.aidlc/events.jsonl`, `.aidlc/latest-outcome.json`, and the immutable
  red-team review attempt before requesting approval;
- lists the human document and hidden machine root in the canonical handoff's `outputs` field;
- may use `/tmp/agent-session/frame-42` for scratch work but never treats it as the sole copy or a
  durable output;
- returns `needs_human` with inline recovery content if durable writes unexpectedly fail, rather
  than claiming the frame was persisted;
- ends with a fenced YAML handoff using canonical routing fields and does not invoke `build` or
  `land`.
