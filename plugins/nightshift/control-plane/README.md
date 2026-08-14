# Local Mission Control

This optional component is a small, read-only browser for AIDLC mission bundles. It discovers
missions from one or more local project roots, groups subtasks beneath their parent mission, and
renders the allowlisted Markdown artifacts in each bundle.

It does not run agents, create jobs, mutate mission files, start containers, or require access to
the private Nightshift runtime. The server uses only Python's standard library.

## Start it

From this repository:

```bash
python3 control-plane/server.py \
  --port 8091 \
  --mission-root "$PWD"
```

Add another local repository by repeating `--mission-root`:

```bash
python3 control-plane/server.py \
  --port 8091 \
  --mission-root "$PWD" \
  --mission-root "/path/to/another/repo"
```

Open <http://127.0.0.1:8091/missions>. The server looks for the v2 layout under
`nightshift/missions/*/.aidlc/mission.json` and the compatible legacy layout under
`nightshift/*/mission.json`.

For a shared or non-loopback bind, set an API token and pass `--host` explicitly:

```bash
AIDLC_INBOUND_TOKEN='choose-a-local-token' \
  python3 control-plane/server.py --host 127.0.0.1 --port 8091 --mission-root "$PWD"
```

The browser remembers the token locally when one is configured. Keep the server on loopback
unless you have separately secured the network path.
