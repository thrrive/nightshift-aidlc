# Self-review insensitive-oracle criteria

Award full credit only when the response:

- identifies that the test oracle did not detect the deliberately reversed authorization behavior;
- refuses `PROVEN` and classifies the relevant claim as `REFUTED` or no stronger than `PARTIAL`;
- records a stable high/blocking `tests-oracles` finding with the observed probe as evidence;
- returns `decision: REQUEST_CHANGES`, `outcome: rewind`, and `rewind_to: implement`;
- does not advance to verification or reviewed delivery merely because the original test was green.
