# Measurement/dephasing bridge artifact manifest

2026-10-15. These are conditional mathematical results and original verification artifacts. They do not qualify noisy hardware, prove a practical threshold, or make novelty/priority claims. No canonical source-theorem files were edited.

## Completed results

- REPORT.md: exact endpoint-measurement replacement for private tracked stabilizer wrappers; formal CP instrument, finite-rate B-product transfer, shared bath, correction-first ordering, later reuse, support, and resource accounting.
- INDEPENDENT_MEASUREMENT_EFFECT_AUDIT.md: independent proof audit of that transfer.
- DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md: exact repeated-measurement budget p_i<=min{1,sum_l a_i,l^2}; equal weak cells give J_i^2 tau_i^2/M_i.
- UNREAD_MEASUREMENT_REFINEMENT.md: extra readout is unnecessary for exact nonselective boundary channels with fresh isolated reservoirs; labels become unobserved Kraus coordinates.
- PARTIAL_DEPHASING_BOUNDARY_THEOREM.md: qualified finite-strength unread boundaries, exact expected squared-block formula, cross-parent subset bounds, safe generator-specific remainder, partial endpoints, and finite-time/resource tradeoffs.
- PARTIAL_DEPHASING_INDEPENDENT_AUDIT.md: independent proof audit of the partial-boundary extension.
- FULL_DETECTOR_FOOTPRINT_CLOSURE_OBSTRUCTION.md: separate root-supplied rank proof that the unchanged zero-good-support certificate cannot cover every Pauli on a closed detector data region unless that region is a fixed stabilizer-state factor. It limits naive hardware closure, not the preceding conditional theorems.

## Original reproducible checks

- check_shared_bath.py and shared_bath_results.json: exact Lindblad matrix-exponential computation on the full joint input, with crossing intervals and later reuse; all 28 subset-effect inequalities at four rates pass.
- check_independent_phase_bridge.py and independent_phase_check.json: separately written branch/toggling/Fourier test for 64 records and eight mathematical seed tuples.
- check_partial_dephasing.py and partial_dephasing_results.json: exact rational CP/channel/endpoint and block-moment identities, plus 1,296 shared-bath Kraus branches and 48 conditional subset inequalities.

Replay the Python scripts directly in a workspace with NumPy, SciPy, and SymPy already installed; no external package installation or author-code execution was used. SHA256SUMS records current artifact hashes. Mathematical proofs, numerical checks, prior-art descriptions, and hardware assumptions are explicitly distinguished in the reports.
