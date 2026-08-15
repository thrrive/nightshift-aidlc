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
codex plugin marketplace add thrrive/nightshift-aidlc --ref v1.0.0-rc.4
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

For stable-v1 qualification, pin `v1.0.0-rc.4` exactly. Promotion to `v1.0.0` changes release
metadata and evidence only; it does not change the canonical v1 contract tested by the candidate.
