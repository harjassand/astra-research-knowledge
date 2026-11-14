# Confined magnetic-walk envelope for the critical-width strip

Status: explicit positive transfer bound, using the raw outer-face walk encoding for connected unions of closed square faces. It bounds static marked and unmarked shape masses uniformly, including overhangs and all perimeters. It is not a reduction of native dynamics to one dimension: the tridiagonal matrix is a CONTOUR-COUNTING operator, not a physical jump generator.

## Word weight and confined operator
For a positively oriented closed boundary word in a width-W strip, a horizontal step receives weight exp(-8), and a vertical step at coordinate x receives exp[-8 ± .04(x-W/2)]. Since the word closes vertically, the centering term cancels, and the product is exactly exp[-8P+.04A], with A its signed enclosed area. The physical contour is a subset of the counted words.

Ignore vertical closure, simplicity and nonbacktracking. Track only x=0,...,W. The resulting nonnegative symmetric matrix T has off-diagonal b=lambda exp(-8) and diagonal

 d_x=lambda exp(-8)[exp(.02(2x-W))+exp(-.02(2x-W))].

At W400 this becomes lambda[exp(-.04x)+exp(-.04(400-x))]. Each matrix step represents one physical boundary step; the diagonal sums the two possible vertical directions, not a zero-length holding event. The factor lambda discounts length, not physical time.

Use lambda=1 for W<=399, where diagonal dominance suffices for spectral radius<1. Use lambda=9999/10000 for W400. `strip_walk_bound.py` computes outward lower LDL pivots of I-T, all strictly positive, which proves I-T positive definite. Perron–Frobenius then implies the nonnegative T has spectral radius<1. Consequently R=(I-T)^(-1)=sum T^k exists with nonnegative entries.

The total weight of x-closed walks rooted at0 that visit W is

 H_W=R_(0,W)^2/R_(W,W).

Proof: the weight of first hitting W is R_(0,W)/R_(W,W); append an arbitrary return from W to0. Equivalently H_W=R_00(full strip)-R_00(strip avoiding W). This identity includes every visit multiplicity once through the first-hit decomposition.

For LDL pivots p_i and constant off-diagonal b,

 H_W=b^(2W)/(p_W product_(i=0)^(W-1) p_i^2).

This positive product permits a directed upper bound without subtracting nearly equal resolvents. Lower log sums and discount products are accumulated downward; numerator logs upward. The source researcher identified and helped repair these rounding directions before the current certificate.

## No illicit initial-perimeter restriction
For W400 and P<=12000, multiply H_400 by lambda^(-12000). For longer actual outer boundaries inside a400-by1600 rectangle, A<=640000, so the complete per-root tail is bounded independently by

 exp25600 * (4exp(-8))^12001 / [1-4exp(-8)].

Its log is below -53771.08. Add it to the discounted bound. Thus the result is UNIFORM over all initial shapes; it does not use a low-perimeter occupation estimate to narrow a canonical-path sum. W<=399 uses lambda1 and already sums all lengths.

## Marked component and all thermal companions
A marked connected union of closed plus squares spanning all400 columns has a canonical raw outer-face boundary walk rooted on the leftmost boundary and visiting the right boundary. Vertex-touching lobes are allowed; the outer-face walk may revisit vertices but uses each outer boundary edge once. Filling bounded square-face holes preserves its width and gives the signed area used above. Internal negative boundary cycles restore the original shape and cost exp(-8P-.04A), bounded by exp(-8P). This raw face convention must be used consistently; it must not be silently replaced by an unrelated graph-fill convention.

For a fixed width400 rectangle with height<=1600, at most1601 vertical root records suffice. Since every full400-by-h rectangle has energy6400, the certificate gives

 sum_marked outer weights / exp(-6400) < exp(190.556),

including that vertical record and the full high-perimeter tail. The per-fixed-root relative log is183.177399.

All unmarked positive outer-face loops contained in a width<=400 strip can be summed by width w=1,...,400 and a canonical root among n=2560000 lattice vertices. Discarding all compatibility gives an exponential loop gas with logarithm

 Gamma_outer <= n sum_w H_w(corrected) < .288671.

The looseness mainly comes from unphysical two-step backtracking words at width1, which are deliberately retained as overcount. All negative/internal cycles have length>=4, at most n4^P codes, and field contribution nonpositive, so their independent gas has logarithm

 Gamma_holes <= n sum_(P>=4)(4exp(-8))^P < .000008311.

Counting positive and negative loops independently overcounts nesting and incompatibility; their exact oriented-area factorization preserves the original Gibbs weight. An initial subset containing the explored width-spanning prefix has at least one marked component. Mark it, sum its mass above, and sum all remaining loops by these gases. There is no assumption that the entire initial intersection with the overwrite region is connected.

## Scope for path reconstruction
This supplies the previously missing marked mass for contractible pre-wrap overwrite rectangles, including the final seam row when compared to the OPEN reference: periodic plus bonds only reduce the relative deletion weight. Earlier erased ORIGINAL components are a separate Gibbs factor, not split across the overwrite boundary. Records identifying the overwrite region, native rate factors, the actual path length, and cross-phase sums must still be included in the complete congestion certificate. Post-wrap cylinders use a separate transfer bound; they are not treated as contractible contours.
