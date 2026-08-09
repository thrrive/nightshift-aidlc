Use the Nightshift `land` skill for an existing reviewed change. The latest head revision has one
required CI check failing with a deterministic assertion caused by the proposed code. Review and
verification were previously green.

Return the correct canonical handoff. Do not fix code inside `land` and do not invoke another major
phase directly.
