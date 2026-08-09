# Extending the skill kit

Extend the kit at its explicit seams instead of forking lifecycle semantics into a host.

## Override a skill

A host may resolve a repository, user, or organization-specific skill in place of a packaged one.
Keep the same mission and outcome contract, transition ownership, and human gates. A major phase may
compose its own subskills but must return to `aidlc` before another major phase begins.

## Implement a host capability

Bind the purpose-level ports in `docs/host-capabilities.md` to your own workspace, verification,
reviewed-change, release, context-read, or lesson-proposal service. Return structured evidence and
one of the documented availability states. Do not expose provider SDK objects or credentials to the
skills, and never convert unavailable execution into a passing result.

## Add a skill

Create `skills/<name>/SKILL.md` with YAML frontmatter whose `name` equals the directory. Use a
one-line description that says when the skill applies. Keep decisions and routing in `SKILL.md`;
put detailed templates or variants in `skills/<name>/references/` and link each required reference
explicitly.

Add a thin command wrapper only when users need to invoke the skill directly. Update the lifecycle
documentation and add contract tests for its handoff. Prefer extending an existing subskill over
adding another lifecycle stage.

## Keep extensions portable

Describe required behavior and capability purpose rather than hardcoding a runtime command, file
layout, model vendor, source-control provider, verification runner, or release platform. Put those
details in the host adapter and test the skill with the adapter absent.
