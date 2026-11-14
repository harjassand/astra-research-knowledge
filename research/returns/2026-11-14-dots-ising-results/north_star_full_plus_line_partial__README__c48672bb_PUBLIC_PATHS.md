# Major partial result: actual occupation of every full-plus-line configuration

## Result
This package bounds the original Ising voltage-weighted occupation of **every non-target configuration containing a full plus row or column**. Unlike the previous restricted square/annulus result, there is no initial minus collar, no core-gas restriction on the exterior, no interior phase-purity requirement, and no restriction on other macroscopic or winding structures.

The method is stronger than the earlier global energy Cauchy bound: decreasing original voltage gives nonnegative upward native currents and a capacity budget for each coordinate cut. A pointwise preimage partition bound then gives a bound linear in the ORIGINAL capacity. All overwritten spin patterns and full nested domain walls are paid.

For theta=4, phi=4/R, L=8R, n=L², epsilon=.01, with the inherited original r and soft clock:

|R|r|Occupation N_H/Z_A at most|Same non-target Gibbs mass/Z_A at least|
|---|---|---|---|
|80|5|exp(-596)|.99711925|
|200|5|exp(-1836)|.99279925|
|1000|6|exp(-10234)|.96399925|
|10000|7|exp(-105199)|.63999925|

These are finite analytic certificates, not simulations of the large systems or computations of their full committors. The non-target Gibbs lower bounds come from the previous core-image annulus subfamily, which is contained in this larger set. Thus the result is not a relabeling of a small-Gibbs-mass bound.

## Important unresolved sector
A diagonal winding band can have no full plus row or column. The included explicit example is outside the majority target, winds in both directions, and has exact weight exp(-64) times the all-minus weight. At the four finite instances, its Gibbs weight relative to Z_A is bounded below using LOCAL inherited pressure certificates. This does not lower-bound its actual occupation, but prevents treating the complementary geometry as automatically negligible.

The theorem therefore does NOT close full native residence, mean exit time, actual-current coverage or the North Star. Literature-wide novelty is not established. It is a source-faithful reusable partial construction using established potential-theory and contour tools.

## Read in this order
1. `01_full_plus_line/ONE_LINE.md`: full construction, constants and limitations.
2. `02_monotone_current/`: original-clock monotonicity and coordinate-current budget; exact small-network diagnostic.
3. `03_wall_topology/TOPOLOGY_AUDIT.md`: fixed triangulation, fixed/moving winding walls, and full-wall encoding.
4. `04_independent_review_and_gap/`: independent review and the diagonal countercoverage example.
5. `DEPENDENCIES_AND_SCOPE.md`: imports, reproducibility and what was not independently acquired.

`00_previous_high_mass_dependency/` is the complete previously verified high-mass package. It supplies the unchanged original source/core snapshot, finite optimized capacity certificate and same-set mass lower bound. Its earlier results are dependencies, not additional new claims. This new archive is separate from that prior ZIP.

## Reproduce
Python3 standard library only:

    python run_checks.py

The runner first regenerates the previous dependency package, then the current/contour/coverage diagnostics and headline scalar certificates. Headline capacity inputs are READ from the freshly generated dependency receipt, not silently hardcoded. The diagonal baseline is checked against the local pressure receipt. `CHECK_OUTPUT.txt` records the run; `SHA256SUMS.txt` covers every other file.

Checks are finite exact-rational/integer diagnostics and analytic scalar certificates, not external peer review or independent reconstruction of the full inherited Astra archive. No held source was accessed.
