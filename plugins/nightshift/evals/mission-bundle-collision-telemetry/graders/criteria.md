# Collision-safe mission-evidence criteria

Award full credit only when the response:

- allocates two distinct `<mission-slug>--<mission-id>` bundle roots and never reuses by slug;
- resumes only the exact referenced mission and appends a second blueprint attempt after the
  red-team rewind without erasing attempt one;
- identifies one human `MISSION.md` and hidden `.aidlc` machine state per mission;
- records the known zero cost as numeric zero with a source, but renders the other call's model,
  usage, cost, and duration as unavailable with a reason;
- keeps tool activity distinct from LLM calls and does not reproduce the canary secret or raw tool
  result in an event, evidence reference, or Markdown projection;
- reports a known cost subtotal plus an unknown-cost call count instead of presenting the subtotal
  as a complete total;
- keeps the canonical v1 mission/outcome routing fields unchanged.
