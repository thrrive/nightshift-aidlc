# Human-first mission bundles

An AIDLC mission has two audiences with different needs. A person needs one readable account of
what the agent understood, attempted, spent, proved, and still needs. A host needs validated state
it can route, resume, rebuild, and audit without parsing prose. The `aidlc-mission-bundle/v2` format
serves both without making either representation pretend to be the other.

## Layout

```text
nightshift/missions/<mission-slug>--<mission-id>/
  MISSION.md
  .aidlc/
    bundle.json
    mission.json
    events.jsonl
    latest-outcome.json
    reviews/
      <stage>--attempt-<n>.json
```

`MISSION.md` is the only normal human entry point. It is a generated projection, not routing state.
The hidden `.aidlc/` directory is machine truth:

- `bundle.json` fixes the immutable mission identity, canonical mission digest, format, and paths;
- `mission.json` contains the unchanged v1 mission;
- `events.jsonl` is the append-only execution and evidence ledger;
- `latest-outcome.json` contains the current v1 routing handoff;
- `reviews/` retains each pinned review attempt instead of overwriting its history.

Hosts should render the projection using [`MISSION.template.md`](MISSION.template.md) or an
equivalent presentation containing every required section. They may change styling, but not omit
uncertainty, rewinds, gates, or the separation between LLM and tool activity.

JSON is used for bounded snapshots because hosts can validate it deterministically. JSON Lines is
used for events because a host can append and recover one record at a time. The v2 bundle does not
use YAML. Markdown remains the presentation format because it is the best review and sharing
surface, but a host never recovers routing state by scraping it.

## Fresh mission versus resume

A slug is a label, not an identity. Every fresh invocation receives a new opaque `mission_id` and
the host creates `<mission-slug>--<mission-id>` exclusively. It never searches for a same-slug
directory to reuse. Two identical asks in one worktree therefore produce two independent bundles.

A rewind or cross-session resume supplies the exact `bundle_ref` or `mission_id`. Before appending,
the host verifies the stored identity and SHA-256 digest of `.aidlc/mission.json`. The digest is the
lowercase hexadecimal SHA-256 of the exact immutable UTF-8 file bytes written at bundle creation;
hosts do not reserialize the JSON before hashing. A missing,
ambiguous, or mismatched reference is rejected; it never degrades to "use the latest slug."

One host-owned writer serializes each bundle's appends, assigns a strictly increasing `sequence`,
and enforces unique `event_id` values. Retrying delivery of the same event is idempotent and cannot
double-count tokens or cost. A new physical LLM attempt receives a new event ID even when it is a
retry of the same logical step.

## Event provenance

Every event records mission, sequence, phase, step, phase attempt, step attempt, status, timestamp,
and safe evidence references. `llm_call` and `tool_call` are separate event types:

- an LLM call records requested/resolved model provenance, token usage, cost, cost source, duration,
  and explicit availability;
- a tool call records tool identity, operation, status, duration, and safe evidence references, but
  never raw arguments or results in the portable record;
- a transition records its source, destination, reason, and optional rewind target;
- reviews, verification, artifacts, gates, and phase boundaries retain their own evidence.

Provider-reported cost uses `provider-reported`. A host calculation uses `host-calculated` and must
name the versioned pricing reference. A known numeric zero is different from missing data. When a
runner does not expose a value, its object says `availability: unavailable` and explains why; it
must not carry a numeric value. A partial usage report names the token fields it actually observed.

Human totals sum only known cost events and show the count of LLM calls whose cost is unavailable.
They never present a known subtotal as a complete mission total.

## `MISSION.md` projection

The host rebuilds `MISSION.md` atomically after a material transition, artifact, review,
verification result, or gate. It contains, in this order:

1. mission identity, status, verbatim ask, and observable done-when conditions;
2. current decisions, approved plan, rollout, and verification shape;
3. the allowed lifecycle diagram and the chronological route actually taken;
4. every phase/step attempt with rewinds and remediation retained;
5. an LLM ledger with model, tokens, cost source, cost, and duration;
6. a separate tool-activity summary;
7. review findings, verification evidence, current blockers, and human gates;
8. known cost subtotal, unknown-cost call count, and the latest outcome.

The projection is rebuildable from `.aidlc/`. Manual edits to `MISSION.md` are not inputs and may be
replaced on the next refresh. User decisions enter through a host gate and become ledger events.

## Redaction and retention

The host applies its authorization, minimization, data-classification, and redaction policy before
anything reaches the ledger or projection. Do not persist credentials, environment values, raw
prompts, raw model responses, tool arguments/results, or secret-bearing logs in portable events.
Evidence references must themselves be safe to share with the bundle's audience.

Projection failure does not rewrite machine routing state. It does prevent a phase from claiming
that the required human document is current. The host records the failure and retries safely.

## Format negotiation and v1 compatibility

The durable-artifact capability advertises supported formats. A host selecting
`aidlc-mission-bundle/v2` follows this document and the `bundle` and `event` schemas. A v1-only host
continues to use the peer-file frame bundle in `frame-artifacts.md`; the v1 `mission` and `outcome`
wire schemas do not change.

A v2 host reads old bundles without rewriting them. If a known v1 consumer still needs peer files,
the host may produce an explicit legacy export. It must not dual-write two canonical stores or
silently treat a legacy projection as current machine truth.
