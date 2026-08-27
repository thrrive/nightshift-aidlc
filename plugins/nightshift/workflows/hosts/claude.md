# Claude host mapping

When Claude provides a native named-workflow facility, register the files in this directory as
the workflow definitions and expose their `entry_skill` as the portable skill fallback. The native
workflow is responsible for invoking the same skills and recording the same `execution_state`;
it must not replace the mission, handoff, review, or host-capability contracts.

When using the portable plugin dispatcher, invoke `/nightshift:workflow nightshift-aidlc <request>`
or `/nightshift:workflow nightshift-missions-next <mission-id>`. If native workflow support and
the dispatcher are unavailable, invoke `/nightshift:aidlc` or `/nightshift:missions <mission-id>
--next` and follow the referenced workflow file directly.

For live progress and intervention, bind the workflow to Claude's streaming NDJSON session. Forward
mission boundary events to the active session and inject operator replies through its open input
stream. If no streaming bridge is available, the skill must print progress and the exact human
question in the current session and provide the command/reference needed to resume.
