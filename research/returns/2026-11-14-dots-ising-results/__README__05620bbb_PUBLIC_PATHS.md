# Major partial: unrestricted-defect actual two-axis sector

## Main result
For the ORIGINAL Ising source, voltage, majority target and native per-site heatbath clock, this package bounds the voltage-weighted occupation of EVERY non-target state with exactly TWO actual axial noncontractible physical phase walls. Other contractible defects are unrestricted.

At theta=4, phi=4/R, L=8R, with the inherited original core and soft clock:

|R|r|Occupation N_K/ZA upper|
|---|---|---|
|1000|6|exp(-138)|
|10000|7|exp(-4356)|

There is NO full-sector claim at R80 or R200. The relevant wider transport constants are vacuous there.

The proof is an exhaustive SIX-way positive decomposition: full lines; short actual walls; a nonbacktracking essential-perimeter tail; a marked large-contractible-hole tail; canonical native transport for area-admissible success; and corrected marked-hole pruning for both conservative completion failures. All branches refer to the same actual weight and voltage. No Gibbs entrance law replaces the actual source current.

A separate topological addendum controls higher essential-wall multiplicities and higher primitive homologies. Including that seventh branch preserves the displayed bounds because7<e². The remaining uncontrolled actual-wall topologies are zero essential walls and exactly two diagonal walls. Those sectors are NOT claimed negligible.

## Why this is substantive but partial
The prior short-wall theorem already demonstrated a substantial NEW-sector Gibbs mass against tiny occupation, with a stepped-annulus family escaping earlier full-line/short-seed results. This package removes both the short-wall restriction and the contractible-defect-area restriction for the entire actual two-axis class at the two large instances.

It is NOT the full residence/exit theorem, a simulation of the enormous systems, or a civilisation-changing breakthrough. Literature-wide novelty is not established. The source/core/clock imports and finite-volume limits are explicit.

## Important corrected argument
The original naive cyclic hole scan could select one wrapping hole twice. The included proof uses corrected FULL-INTERSECTION peeling: remove all of a selected projection's intersection with the remaining cyclic interval, so no hole is reused. Independent counterexample, repaired proof, exhaustive tests and reviews are included. The enlarged cutoff4R²/3 uses new kernel and pressure receipts; the old small-area activity is not silently reused. Its complementary marked-large-hole tail uses a global field cap exactly once.

## Read in order
1. `research_notes/n1722_axis_nonbacktracking_tail_20261113/TWO_AXIS_SECTOR.md`.
2. `GOOD_CLASS_PARTITION.md` and `RESULT.md` in that directory.
3. `research_notes/ising_physical_phase_boundary_20261113/AREA_ADMISSIBLE_COMPLETION.md`.
4. `research_notes/ising_marked_hole_cover_20261113/{RESULT,ENLARGED_AREA}.md`.
5. `research_notes/n1722_failed_completion_pruning_20261113/COMBINED_THERMAL_PRUNING.md`, including its explicit raised-cutoff appendix.
6. `research_notes/north_compute_20261113/ising_enlarged_hole_tail/RESULT.md`.
7. The independent reviews and `DEPENDENCIES_AND_SCOPE.md`.

Component notes preserve their original narrower hypotheses. The sector theorem explicitly explains which enlarged receipts extend them; it does not silently relabel an old small-defect theorem unrestricted.

## Reproduce
Python3 standard library only, no network or external solvers:

    python verify_manifest.py
    python run_checks.py
    python verify_manifest.py

The runner regenerates all inherited source/capacity receipts, the complete reviewed short-wall dependency, corrected cyclic cover checks, raised kernel/pressure, independent marked-large-hole tail, and every branch of the final sector receipt. Final scripts read fresh local dependency JSON rather than disconnected hardcoded exponents.

`CHECK_OUTPUT.txt` records execution; `SHA256SUMS.txt` covers every other file. No previously delivered archive was altered. This worker prepares the package but does not deliver it directly.
