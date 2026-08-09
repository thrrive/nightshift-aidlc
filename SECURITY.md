# Security policy

Do not report security vulnerabilities in a public issue. Until a dedicated public security contact
is published, use GitHub private vulnerability reporting on the eventual
`thrrive/nightshift-aidlc` repository.

The skill kit contains behavior and contracts, not credentials or a privileged execution runtime.
Hosts remain responsible for workspace isolation, tool authorization, secret handling, reviewed
change permissions, release credentials, and audit retention. A missing required capability must
stop the relevant phase; it must never trigger an unsafe fallback.

Supported security fixes target the latest preview or stable release. A disclosure will state the
affected versions, mitigation, and fixed version.
