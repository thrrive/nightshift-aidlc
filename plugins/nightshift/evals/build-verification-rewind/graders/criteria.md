# Build verification-rewind criteria

Award full credit only when the response:

- classifies the observable mismatch as failed verification rather than passed or unproven;
- returns `outcome: rewind` with `rewind_to: build` and preserves the mission;
- carries the specific wrong-field evidence into the handoff;
- does not open a second reviewed change, waive verification, or invoke `land` directly.
