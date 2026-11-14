# Major partial: original-current occupation of short actual phase walls

## What is new
This construction bounds the original Ising voltage-weighted occupation of every non-target state with a noncontractible **actual physical-plus-resolution phase wall** of physical length p<=2L-8. Other spins are arbitrary. The source core, soft-source clock, physical Hamiltonian, native heatbath clock and majority target are unchanged.

It uses a visible actual wall to reconstruct path labels, a deterministic native hole-first growth order, and a pointwise thermal partition bound with a paid ONE-versus-THREE-or-more winding-loop decomposition. A low path barrier alone is NOT used as a substitute for thermal congestion control.

At theta4, phi4/R, L8R and the inherited original source parameters:

|R|r|Occupation N_H/ZA upper|
|---|---|---|
|80|5|exp(-94)|
|200|5|exp(-567)|
|1000|6|exp(-3858)|
|10000|7|exp(-41368)|

These are finite analytic certificates, not billion-spin simulations or estimates of the full committor.

## A genuinely added, nonrare sector
The new stepped-annulus family has no full plus row or column, no diagonal winding, and every plus winding path has length at least approximately4L/3. It therefore escapes the earlier full-line, regular diagonal-anchor and short/low-roughness plus-seed routes. Nonetheless one actual wall has length approximately5L/3 and is covered here.

Its n distinct translations have Gibbs mass normalized by the CORE partition ZA greater than .022,.14,32million/3,3.2billion/3 at the four instances. These are core-normalized masses, not probabilities under the full Gibbs distribution; values above one are legitimate. The occupation upper already includes the entire family without an extra orbit charge. This supplies a strong same-new-sector comparison rather than merely bounding a Gibbs-rare set.

## Exact limits
This is NOT the full exit/residence theorem, complete actual-current coverage, or a civilisation-changing breakthrough. It does not cover every longer wall, original diagonal-only connectivity, all diagonal phase interfaces, no-winding-wall phases, or large contractible defects. Literature-wide novelty is not established. The wider p<2.45L completion was considered and explicitly rejected as unproved; it is not claimed here.

## Read in order
1. `research_notes/n1722_actual_wall_collar_20261113/THEOREM.md`.
2. `CONNECTED_PIN_PARTITION.md` in that directory, including cancellation and limits.
3. `research_notes/ising_physical_phase_boundary_20261113/SHORT_SPAN_COMPLETION.md` and `PIN_CANCELLATION.md`.
4. `research_notes/ising_right_only_bootstrap_20261113/HOLE_FIRST_AUDIT.md`.
5. `research_notes/n1722_actual_wall_collar_20261113/NEW_SECTOR_BASELINE.md` and `BRIDGE_INDEPENDENT_REVIEW.md`.
6. `DEPENDENCIES_AND_SCOPE.md`.

## Reproduce
Python3 standard library only, no network or external solver:

    python verify_manifest.py
    python run_checks.py
    python verify_manifest.py

The runner first executes the complete prior dependency package, then the new geometry, actual-label, original-clock scalar, baseline and exact mincut checks. The new scalar receipt READS the freshly generated local optimized-capacity certificate. The new baseline checks its conservative pressure against the freshly generated local core-pressure certificate. No hidden external files are required.

`CHECK_OUTPUT.txt` records the run. `SHA256SUMS.txt` covers every other file. Checks support the mathematical proof; they do not constitute independent reconstruction of the entire inherited Astra archive or external peer review. No delivered prior archive has been modified.
