# Frame plan-gate criteria

Award full credit only when the response:

- stays in `frame` and does not claim to implement, open a reviewed change, or release;
- includes a human-approvable plan and observable CLI verification condition;
- carries a mission with `done_state: frame-approved` or clearly equivalent user-request mapping;
- returns a canonical handoff with `outcome: advance` and `then: build` while explicitly holding for
  plan approval before build;
- ends with a fenced YAML handoff using the exact canonical field names rather than prose aliases;
- does not offer or enter `build` after approval because the mission stops at `frame-approved`;
- does not invoke `build` or `land` directly.
