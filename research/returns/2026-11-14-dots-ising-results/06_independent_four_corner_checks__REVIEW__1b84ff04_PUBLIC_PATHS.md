# Independent review: high-area four-Ferrers-corner family

## Executed geometry check
`check.py/json` enumerates all1296 four-corner shapes for R=2: begin with an8-by8 square and remove an independent Ferrers order ideal in each2-by2 corner. All shapes have unique corner-partition encodings, connected interiors, full8-by8 bounding rectangle, area48–64 (=12–16R²) and physical perimeter32 (=16R). A single shape-independent order, filling each corner in descending distance from that corner, supplies exactly two plus neighbors for every actual missing-site fill. All10368 executed single-spin additions preserve physical perimeter and finish at the square.

This is a finite **solid geometry** test. R2 is not within the main thermal theorem's R>=80 range. It does not validate thermal transport or source coverage by simulation.

## General geometric argument
The four R-by-R corner boxes are disjoint and leave connecting full strips of width at least2R. A Ferrers cut removes only the two exterior-adjacent sides of a corner and replaces them with a monotone staircase of the same total length. Hence each cut preserves perimeter, independent of its area. Full central rows and columns remain, fixing the bounding rectangle. The shape uniquely determines its corner cuts. Descending x+y exposes the two inward neighbors before each removed site is filled. None of these properties depends on the small test size.

## FKG and source normalization
The proposed positive-interior reduction is legitimate only in the scope already stated in `POSITIVE_INTERIOR_HOLE_REDUCTION.md`: fixed actual plus boundary, independent exterior small-domain constraints, interior conditioned solely on M_D>0, nonnegative field. Large interior minus-domain occurrence is decreasing; M_D>0 is increasing. FKG and field monotonicity therefore permit a zero-field Peierls upper bound on that event. Full-domain spin reversal of the good interior sends it to M1, retaining thermal bits. No claim about FKG for the current-conditioned process, reflection, or globally imposed M<0 is justified. Including target states in the source envelope and letting v=0 there avoids the latter conditioning.

For a corner deficit k and P=16R,V=16R²-k, the inherited normalization gives
Z_D <= [Z_A/((1-alpha)(1-u1))] exp(-2phi k),
since the square's wall/field exponent cancels exactly. This is an upper bound relative to the normalizer, not an equality or proof that a pure-square state has order-one Gibbs probability.

## Partition and aggregate-energy bookkeeping
Let P(q)=product_(j>=1)(1-q^j)^(-1). Finite R-by-R corner partitions form a subset of unrestricted partitions. Thus
sum_D sqrt(Z_D/Z_A) <= n/ sqrt((1-alpha)(1-u1)) * P(exp(-phi))^4.
The factor n safely pays translated bounding squares; it is not a thermal-label count. Since logP(exp(-phi))<=pi²/(6phi), squaring this source sum yields exp(4pi²/(3phi)). With inherited per-contour flow E_D<=2n exp(4theta) Z_D, triangle inequality gives
E(F)/Z_A <= [2n³ exp(4theta)/((1-alpha)(1-u1))] exp(4pi²/(3phi)).
At theta4, the exponential coefficient is pi²/3≈3.28987 timesR. Pairing with an independently valid SAME-clock capacity bound exp(-cR) produces an occupation exponent -(c-pi²/3)R/2, plus explicit finite prefactors. I have not independently re-certified that capacity constant here.

The fixed source geometries can collide along the paths; the energy triangle explicitly pays those collisions. No independence, label recoverability at merged intermediate states, or uncharged interior multiplicity is needed.

## Physical-path limitation
The two-plus-neighbor geometry check applies to solid corner filling. With thermal holes/companions, the actual construction toggles exterior sites by XOR and may also turn a plus spin minus. Its energy estimate must come from the existing thermal companion prefix-moment theorem, not from a mistaken assertion that every thermal step is an energetically favorable fill. Retained D-boundary and M_D>0 ensure the full outside-XOR sequence eventually reaches the actual majority target. Stopping at first target is required. No whole-strip or cluster update may replace these native spin flips.

## Fair baseline and actual limit
The direct full-domain Gibbs upper bound for this family is
Z_G/Z_A <= [n/((1-alpha)(1-u1))] P(exp(-2phi))^4
<= [n/((1-alpha)(1-u1))] exp(pi²/(3phi)).
This bound grows rather than yielding rare occupation. Thus the aggregate-flow/capacity bound can improve the existing direct-mass bound in this high-area family; unlike the former5–6R² result it is not automatically baseline-dominated by that estimate. This comparison does **not** prove that every possible sharper equilibrium estimate fails or that actual Z_G/Z_A is large.

Coverage remains narrow: four corner monotone defects in a fixed-scale square; positive interior magnetization; embedded geometry; small separated exterior companions. Arbitrary rough contour defects, large companions, negative interiors and winding domains remain outside. No bound on the fraction of actual source current or full residence denominator follows. This is a potentially useful scoped occupation construction, not the full Ising mean or a civilization-scale result.
