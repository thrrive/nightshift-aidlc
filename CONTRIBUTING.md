# Contributing

Open an issue before changing the canonical mission, outcome, routing, or capability contracts.
Keep each change focused and include evidence that the portable package works without Nightshift's
private runtime.

For skill changes:

- keep `SKILL.md` concise, imperative, and decision-dense;
- put detailed templates and variants one level below the owning skill in `references/`;
- never let a major phase invoke a sibling major phase;
- preserve the canonical field names and human gates;
- add or update contract and conformance tests.

Every contribution must pass the clean-room scrub, manifest and frontmatter validation, local-link
checks, schema fixtures, representative lifecycle tests, and package build. Do not submit private,
employer-owned, credential-bearing, or generated execution-plane material.
