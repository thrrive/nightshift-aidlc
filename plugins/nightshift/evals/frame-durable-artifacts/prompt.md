Use the Nightshift `frame` skill for this interactive mission:

> Critique an existing reference architecture and plan a new, more general-purpose repository from
> selected source files. Stop for approval before creating the repository or copying product code.

The user started the agent in `/work/general-agent`, which is an authorized durable invocation root.
The target repository does not exist yet and therefore has no feature-docs convention. A host helper
offers `/tmp/agent-session/frame-42` for intermediate files, but that directory disappears when the
session ends.

Complete the frame and present it for approval. Explain where every review artifact is stored and
return the canonical handoff. Do not implement the repository.
