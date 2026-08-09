# Self-review findings record

Emit a structured, inspectable record of what the review found and how each finding was disposed
of. When the host provides a self-review artifact destination, write this shape there:

```json
{
  "outcome": "advance" | "rewind",
  "note": "<the prose summary already used as the routing reason>",
  "clean": true | false,
  "build_summary": "<one sentence describing what was implemented>",
  "findings": [
    {
      "severity": "high" | "medium" | "low",
      "category": "correctness" | "scope-creep" | "diff-hygiene" | "plan-gap" | "security" | "verification" | "other",
      "file": "<path the finding points at>",
      "line": <int> | null,
      "text": "<specific finding with a citation>",
      "disposition": "fixed" | "acknowledged-no-change" | "rewind",
      "what_changed": "<required fix description when disposition is fixed; otherwise null>"
    }
  ]
}
```

Apply these rules:

- Always write the record when the host supplies a destination. Never leave it missing or blank.
- Describe what was implemented in `build_summary`, not the review verdict. Keep it to one sentence
  because the host may use it as reviewed-change evidence.
- Set `clean: true` with `findings: []` for a clean review.
- Set `clean: false` and add one entry for every finding otherwise.
- Give every fixed finding a non-empty `what_changed`; include a commit or diff reference when one
  is available.
- Use `disposition: rewind` for a finding that requires `outcome: rewind`. Keep the prose reason in
  `note`; the finding record does not replace the routing outcome.
