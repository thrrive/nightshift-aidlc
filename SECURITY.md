# Security policy

Do not report security vulnerabilities in a public issue. Until a dedicated public security contact
is published, use GitHub private vulnerability reporting on the eventual
`thrrive/nightshift-aidlc` repository.

The skill kit contains behavior and contracts, not credentials or a privileged execution runtime.
Hosts remain responsible for workspace isolation, tool authorization, secret handling, reviewed
change permissions, release credentials, and audit retention. A missing required capability must
stop the relevant phase; it must never trigger an unsafe fallback.

Human-first mission bundles are shareable evidence, so their portable event records intentionally
exclude raw prompts, model responses, tool arguments/results, environment values, credentials, and
secret-bearing logs. Hosts must minimize and redact content before persistence, including evidence
references. Never assume that hiding `.aidlc/` from a normal directory listing is an access-control
boundary.

Supported security fixes target the latest preview or stable release. A disclosure will state the
affected versions, mitigation, and fixed version.
