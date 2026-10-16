# Measured-memory endpoint transfer: portable audit packet

Start with AUDIT.md. It distinguishes the old history-event certificate from the new endpoint-event certificate, proves their scheduled lifecycle mapping, and states narrowly qualified improvements.

## Main conclusions

- Directly substituting the endpoint F_K into the old ANY-block-mismatch bound is false.
- The exact counterexample has old history effect (19/32)I and endpoint effect (18/32)I. Thus the failure already holds on the entire input space, not merely a selected state.
- Complete retained cuts permit the improved Q constant for the unchanged history event.
- A scalar full-syndrome node permits F_K for an explicitly changed endpoint-good CP decomposition.
- One actual general-Schur node permits F_C; independent-generator kernels are translation invariant in the entering syndrome, while a general kernel needs a uniform max over entering labels.
- Actual endpoint channels, full-footprint support, chronological bath coefficients, fixed reservations/schedules, independent inaccessible node environments, and old decoder/contour assumptions remain essential.
- This is a conditional mathematical interface, not a device qualification, finite-width noisy-measurement theorem, threshold calculation, or claimed physical memory lifetime.

## Reproduce the exact check

Run `python check_counterexample.py` with Python 3 and SymPy installed. The script performs exact 2-by-2 matrix arithmetic, resolves every actual entering/node/final Kraus branch, verifies trace preservation, and checks both full-input effects. It writes counterexample_results.json. No network or downloaded code is used.

## Contents and provenance

AUDIT.md is the transfer argument. The counterexample script and JSON are its executable check. The sources/ directory contains unchanged prerequisite proof snapshots. These snapshots may refer to ancillary files from their original research packages; the core theorem texts used by this audit are included here. In particular:

- sources/measurement_randomizer_bridge: actual-channel, boundary, support, and CP-refinement interface.
- sources/causal_refresh_product and sources/joint_refresh_bernstein: causal tensorization, unchanged-action simulation, and analytic input.
- sources/imperfect_refresh_product and sources/multisector_refresh_audit: partial-node singleton and label embedding.
- sources/general_schur_refresh_audit: full Schur singleton optimization and label embedding.

SHA256SUMS covers every other file in this packet. It verifies frozen file integrity, not mathematical validity. Existing source bibliographies identify their external mathematical imports; this packet does not reproduce copyrighted external papers or claim independent verification of those papers.
