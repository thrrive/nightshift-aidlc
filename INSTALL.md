# Install and upgrade

The release artifact is a marketplace repository containing the `nightshift` plugin under
`plugins/nightshift`. Pin a release tag in environments that require reproducible behavior.

## Claude Code

For a local source checkout:

```bash
claude --plugin-dir ./plugins/nightshift
```

When the target repository is outside that checkout, pass the same plugin directory through
`--add-dir` so skills can read their packaged one-level references:

```bash
claude --plugin-dir /path/to/nightshift-aidlc/plugins/nightshift \
  --add-dir /path/to/nightshift-aidlc/plugins/nightshift
```

After the public repository exists:

```bash
claude plugin marketplace add thrrive/nightshift-aidlc
claude plugin install nightshift@nightshift-aidlc
```

Upgrade an installed public plugin and restart Claude Code:

```bash
claude plugin update nightshift@nightshift-aidlc
```

## Codex

For a local source checkout:

```bash
codex plugin marketplace add .
codex plugin add nightshift@nightshift-aidlc
```

After the public repository exists, replace the local marketplace with the Git source or add it in
a separate environment:

```bash
codex plugin marketplace add thrrive/nightshift-aidlc --ref v1.0.0-rc.10
codex plugin add nightshift@nightshift-aidlc
```

To upgrade a Git marketplace and reinstall the plugin from its refreshed snapshot:

```bash
codex plugin marketplace upgrade nightshift-aidlc
codex plugin remove nightshift@nightshift-aidlc
codex plugin add nightshift@nightshift-aidlc
```

Restart the host after installation or upgrade so the new skill definitions are loaded in a fresh
session.

## Compatibility

Read `COMPATIBILITY.md` before changing pinned major versions. The package has no runtime service,
credential, or database migration; hosts supply capabilities independently.

For stable-v1 qualification, pin `v1.0.0-rc.10` exactly. Promotion to `v1.0.0` changes release
metadata and evidence only; it does not change the canonical v1 contract tested by the candidate.

## Local Mission Control

The public checkout includes a read-only mission browser. It requires Python 3.11+ and does not
run agents or mutate mission files:

```bash
python3 control-plane/server.py \
  --host 127.0.0.1 \
  --port 8091 \
  --mission-root "/path/to/your/mission-root"
```

Open <http://127.0.0.1:8091/missions>. Repeat `--mission-root` for additional project roots. Keep
the server on loopback; for a shared bind, set `AIDLC_INBOUND_TOKEN`. The browser discovers v2
`nightshift/missions/*/.aidlc/mission.json` and legacy v1 `nightshift/*/mission.json` bundles.

## Full execution runtime

The public skill kit is not the full execution service. For streamed jobs, isolated workspaces,
approvals, retries, verification, and merge/release gates, use the companion `sdlc_harness`:

```bash
python3 runtime/control-plane/server.py --host 127.0.0.1 --port 8080 --simulate
python3 cli/psdlc run --server http://127.0.0.1:8080 \
  --target net-worth-tracker --watch "Describe the change here"
```

Use `psdlc status`, `psdlc logs <job-id> --follow`, and `psdlc approve <job-id> --watch` to follow
the SSE event stream and human gates. Direct interactive workflows require a host bridge for live
updates: Codex uses `codex app-server`/`turn/steer`, and Claude Code uses streaming NDJSON with an
open input stream.
