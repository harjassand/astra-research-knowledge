# Astra PRO3 Cycle6 source return

Read REPORT.md for the result and decision; GLOBAL_BOUNDARY_THEOREM.md for
the complete arguments; STATUS.md for exact source-bound acceptance; then
CONTINUATION_SEED.md for the next expressly unproved question. SOURCES.md
gives precise attribution and closest primary comparisons. EXPERIMENT_CONTRACT.md,
NUMERICS.md and FAILED_APPROACHES.md preserve the inputs, limits and decisions.

The new native theorem is the exact global-dominant critical amplitude at
r0>=1, including equality. A reusable boundary-weighted first-hit estimate
and a constant three-state full-law lower are proved. The pure-IMH comparison
is adverse to the hybrid; no practical speedup is claimed.

## Replay

Python 3, standard library only:

    python replay.py --output /absolute/path/cycle6_replay_receipt.json

This verifies MANIFEST.json, checks every payload byte/hash, and runs only
`code/weighted_boundary_checks.py` in a temporary output directory. Deterministic
input/results must match the delivered files exactly. Resource measurements
can vary. No package install, network, paid compute or old campaign is used.

To run the new diagnostic directly:

    python code/weighted_boundary_checks.py --output-dir /absolute/path/checks

Do not overwrite delivered evidence while testing. The current source archive
contains the unchanged Cycle5 ZIP and its complete historical source chain.
It also includes the original contributor proofs and focused reviews.

## Source identity and receipt

The produced ZIP's exact bytes/hash and native private identities are recorded
in a separate immutable delivery receipt. This avoids a circular archive hash.
The receipt can also record a portable replay after packaging without mutating
the source ZIP. Authorized Page readback of ordered base64 parts provides an
exact-byte receiving route when binary materialization is unavailable.

Max owns integration. Delivery does not assert recipient reading, independent
acceptance or integration. The same private source is available to the evaluator.
