# Independent marked-hole interval-cover audit and cyclic repair

Reviewed ising_marked_hole_cover_20261113/RESULT.md and reran certificate.py. The rooted activity, area/width estimate, and exact scalar certificate pass. The original one-direction greedy scan had a genuine cyclic-reuse defect, now repaired by fluid.

## Checked hypotheses and inequalities
This is conditional on actual embedded CONTRACTIBLE FILLED holes of area A<=R² and on the parent comparison having already earned activity exp(-8P+8A/R). It does not supply that field comparison or area cutoff.

A finite lift has inclusive bbox widths w,h, A<=min(R²,wh), P>=2(w+h), and w<=P/2-1. A filled disk covering a prescribed torus column cannot contain the entire essential vertical column. Some vertical physical edge in that column therefore crosses its outer boundary. Rooting/orienting there costs only O(L), not an uncharged ambient n or horizontal-origin factor. Fixed-triangulation physical-step encoding has at most3 continuations. The safe12L3^P count is sufficient.

The joint inequality8P-8A/R-12w>=(11/8)P follows from P>=2(w+h), A/R²<=min(1,WH), and (5/4)W+(53/4)H>=sqrt(265)/2 sqrt(WH)>=8min(1,WH). It does not combine incompatible independent extrema. The short-perimeter exponent -2P-12+P²/160 follows from w<=P/2-1, A<=P²/16 and R>=80. Exact positive Taylor receipts bound the finite sum and geometric tail in the correct direction; the total tilted kernel is below2/5 for all stated parameters.

## Defect and repair
On L10, target columns0,...,7, a wrapping projection A={6,7,8,9,0,1} and B={2,3,4,5} cover the target. A naive left-to-right scan selects A,B,A, charging A's activity twice although the actual contour appears once. Such a chain product can undercount physical configurations.

Maintain instead the remaining contiguous interval I. Choose a hole covering its left endpoint, and remove ALL of that projection's intersection with I: this can include both a prefix and a suffix. The remainder is one interval or empty. Once removed, the same hole has no point in the remaining interval and cannot be selected again. The removed cardinality p satisfies1<=p<=w. Whole-circle projections terminate immediately and also satisfy p<=w.

At each state, the sum of tilted child weights a_gamma exp(12p) is bounded by the same column-rooted S<1. With terminal mass1, induction on |I| bounds all first-passage tilted chains by1. Total removed cardinality is EXACTLY c, so untilting gives exp(-12c). This repair changes no constants, but is necessary for cyclic projections.

check.py exhaustively tests24766 covering families of up to3 cyclic arcs on a5-cycle and38113 peeling steps. Every remaining interval, no-reuse and progress invariant passes. It also records the explicit L10 failure of the old scan. These tests complement the interval proof; they are not a Gibbs simulation.

## Remaining dependencies
The marked-chain bound must still be multiplied by the paid unmarked-contour product. A deterministic chain plus the unmarked wall set reconstructs the original wall collection; this is why the corrected no-reuse property matters. Essential-wall multiplicities, erased-phase field cost, majority constraints and any source normalizer remain the parent's obligations. Actual source current is never replaced by a conditional Gibbs law.

With the repaired interval peeling, no further defect was found in this conditional lemma. It is not an unrestricted no-full-column theorem without those global assumptions.
