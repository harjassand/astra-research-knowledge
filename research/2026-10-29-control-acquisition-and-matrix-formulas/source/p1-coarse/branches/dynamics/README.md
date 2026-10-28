# Dynamics research branch

Eight distinct pieces of work are retained.

1. `CLIFFORD.md`, `check_clifford.py`, `CLIFFORD_RESULTS.json`, and
   `CLIFFORD_TRANSCRIPTS.json` contain the exact passive frozen-law obstruction
   and an exact scalar-query acquisition. All frozen source laws coincide,
   while a five-operation response differs by 243/16384. The supplied
   16-word dictionary is exactly closed and supports later predictions.
2. `CONSTRUCTION.md`, `run_memory.py`, `RESULTS.json`, and `DATA.npz` contain
   the separate passive relaxation-memory acquisition. A synthetic run used
   404 step-time readings, one trajectory to T=10000, and one 256-grid LP,
   yielding a 44-mode positive model with analytic finite-horizon L1 error
   upper bound 0.0027473071. The requested bound was 0.01. Its source had 128
   hidden relaxation modes; no finite hidden mode count or lower rate is
   required by the theorem. This is not evidence for the switched compiler.
3. `BLOCK_EXPLORATION.md`, `check_block_geometry.py`, and
   `BLOCK_GEOMETRY_RESULTS.json` contain exact conservation subtraction,
   adaptive contracting-block construction, a polynomial-readout exact
   reachable-basis procedure, and fixed-rank slow-scale obstructions.
   Rational qubit examples show that O(n) readouts can still require
   Omega(4^n) primitive operations. The exact checker covers 630 primitive
   words and 150 macro words; it does not duplicate the parent's compiler.
4. `RELATIVE_DEFECT_CHALLENGE.md` independently checks the root's
   vanishing-relative-defect counterexample and embeds it into reciprocal
   four-level quantum channels with the same fixed preparation and receiver.
   It remains valid with identity as the only common conserved mode and
   with strictly positive primitive spectra. The independent
   `check_relative_quantum_embedding.py` passed 378 exact word checks;
   `RELATIVE_QUANTUM_EMBEDDING_RESULTS.json` records its results.
5. `DISSIPATION_CONSTANT_CHALLENGE.md` proves that the factor 2 in the
   dissipation-weighted theorem is sharp for realizable paired defects,
   including full-rank dictionaries. Its exact checker is
   `check_dissipation_sharpness.py`.
6. `RENEWAL_ACQUISITION.md` develops and executes the rank-one positive
   first-return comparator. `renewal_acquisition.py` generates receipts;
   `compare_renewal_flags.py` compares complete costs;
   `replay_renewal_exact.py` certifies all saved envelopes with rational
   arithmetic. Logical trials and optimized physical preparations are
   separately charged.
7. `MULTIBOUNDARY_ORDER_WITNESS.md` and
   `check_multiboundary_order.py` preserve the exact same-count return
   and transport witnesses and a direct endpoint comparator.
   `MULTIBOUNDARY_COMPILER_REVIEW.md` independently reviews the physical
   branch's new compiler; `replay_multiboundary_review.py` checks its saved
   confidence endpoints, matrix bounds, bilinear programs and cost ledger
   without generating new trajectories.
8. `ABSORBING_BOUNDARY_ACQUISITION_REVIEW.md` independently reviews the
   completed observed-absorption acquisition without a global source gap.
   `replay_absorbing_boundary_review.py` replays all 58 used confidence
   endpoints, finite matrix inequalities, and the acquisition cost ledger.
   It reproduces inference from only observable counts with hidden-source
   access disabled. No new trajectories are generated; the narrow direct
   comparator preparation-receipt limitation is explicitly recorded.

`COMPARATORS.md` records primary literature, including the March 2026
Trustworthy Koopman paper and its direct Gram-residual/multistep antecedent.
No historical priority or physical-device advantage is established.

Run the exact counterexample with `python check_clifford.py`. Run the memory
experiment with `python run_memory.py` after installing `requirements.txt`.
Run the independent block geometry checks with
`python check_block_geometry.py`.
Run the exact channel-embedding check with
`python check_relative_quantum_embedding.py`.
The newer replay scripts import shared exact arithmetic from the package's
`core` directory; preserve the complete successor package when moving them.
The local `_deps` directory, if present, is a temporary mpmath installation
and need not be packaged; the pinned dependency is recorded above.
