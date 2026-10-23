# Reproduction and receiving instructions

## Default integrity and scientific status check

From the extracted archive root, run:

    python3 replay.py

This verifies every listed delivered payload hash, the exact unchanged Cycle9
ZIP, both preserved fixture statuses and the source-bound principal review.
It does not run old simulations or reinterpret a failed admission. To inspect
the full predecessor, safely extract the ZIP under sources/ into a separate
directory. Its native verifier belongs to that full original, not to a selected
source directory.

## New exact diagnostic only

    python3 replay.py --new-precision

This replays the separate rational two-state changed-target-oracle calculation.
Read PRECISION_BOUNDARY.md before interpreting it. It is not a test of the
native critical theorem or a new floating-point implementation model. The
recorded producer output and resource receipt are already supplied. The replay
copies the unchanged diagnostic code to a fresh temporary directory, because
the diagnostic correctly refuses to overwrite an existing result.

## Proved-formula visualization

    python3 code/critical_profile.py --out /tmp/astra_pro3_cycle10_profile

This requires matplotlib and Pillow. It evaluates the proved scalar control
cost and phase formulas, writes VALUES.json, a PNG/PDF and a resource receipt.
No native Markov chain is simulated. Floating evaluations are not exact
certificates for the theorem. The default output is the included evidence
directory; use the external output path above to preserve original evidence.

## Mathematical reproduction

Read Theorems 1–3 and the explicit remaining gap in CRITICAL_TRANSPORT_THEOREM.md.
Trace (8)–(9) to the delivered unchanged finite dependency, then check the new
endpoint multiplier, three-cell KL allocation, clipped weight, native full-law
sandwich, phase subsequences and control-model super-solution. Contributor
notes contain additional finite estimates. The proof does not require a huge
graph, finite matrix-power extrapolation or the old failed coalescence fixture.

The external transport manifest identifies ordered base64 UTF-8 parts if the
receiver can read Page source but cannot materialize binary ZIPs. The provided
code/decode_transport.py validates each part and final byte identity. The same
archive is also available as a private Library/file and Page attachment. None
of these routes changes access permissions or requires user relay.
