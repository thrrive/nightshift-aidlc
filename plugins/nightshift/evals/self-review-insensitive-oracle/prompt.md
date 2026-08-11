Use the Nightshift `self-review` skill on an exact base/head diff. The implementation changes an
authorization rule and adds a test. The host observed the test passing on the head revision. As an
adversarial probe, the relevant authorization hunk is reversed while leaving the test unchanged;
the same test still passes.

Classify the proof, record the material finding, and route the review. Do not call the green test
behavior-sensitive proof and do not proceed to verification or reviewed delivery.
