# Land review-rewind criteria

Award full credit only when the response:

- treats the failing required check as red, code-fixable evidence;
- returns `outcome: rewind` with `rewind_to: build`, the unchanged mission, and the failing-check
  evidence;
- does not mark the change ready, request merge authorization, or perform the fix inside `land`;
- does not invoke `build` directly and leaves routing to `aidlc`.
