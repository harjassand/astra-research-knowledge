# Paid intermediate-diagonal thermal partition

Status: integrated construction independently reviewed by fluid and GKP on geometry, and fluid on the paid partition; compute's final independent construction/partition review also passed (shadow-envelope RESULT Section6). Exact scalar receipts are linked to the original capacity JSON. No global exit theorem is asserted.

## Precise geometry interface
Use the actual deterministic physical-plus encoding, original A/B/voltage/capacity, and original rate-one-per-site heat-bath clock. Select an actual primitive diagonal wall gamma with p<5L/2. The independently reviewed native reference construction supplies:
- its NN-connected essential plus collar D and exactly one essential unavailable pin band in the right strip;
- initial bounded D-complement pockets retained with their ACTUAL bits, never filled natively;
- a deterministic two-neighbor growth order in the essential right complement, maintaining that complement essential-connected by hole-first repair;
- all actual visited-plaquette pins unchanged, and actual first-majority stopping;
- every reference prefix determined by gamma and its scheduled site, independently of source extra plus bits (which are skipped).

The authoritative CONSTRUCTION.md, supported by SINGLE_PIN_BAND, CONNECTED_MINUS_REPAIR and compute's ising_shadow_envelope/RESULT provide these interfaces. The exact lattice hull residual bound is Lb+6L, b=(p-2L)/2<L/4, which is below n/2 at all original finite instances. Frozen initial pockets lie in the SAME projected hull, so are not a separate lost-area term.

## Actual fixed-edge fiber
At a native edge, only the previously scheduled source bits are erased. Their weights must all be summed. Initial frozen pockets have no physical edge to the growing component and cancel exactly from the source/reference ratio; fill them plus on both sides of the auxiliary comparison. Other outside plus bits, including adjacent fourth-corner pins, are lowered to minus by termwise ferromagnetic ratio monotonicity, not falsely canceled. Keep mandatory D plus and freeze an auxiliary triangulation preserving gamma's crossed triangles. The extra fourth corner is outside those triangles, so the comparison preserves gamma. Positive field contributes exp(-2phi times erased minus count)<=1 and is discarded.

The resulting mandatory-plus set is essential-connected. The remaining mandatory-minus set is essential-connected by the hole-first invariant and can be connected by the per-prefix minus-biased auxiliary diagonals without changing gamma's fixed local choices. Hence no contractible contour can enclose a mandatory pin: such an essential-connected pin set cannot fit in a disk without crossing that contour. Contractible loops can be removed while preserving all prefix constraints.

Let the reference moving perimeter, after removing fixed gamma, be m. Collar P(D)<=2p and every two-neighbor birth is perimeter-nonincreasing, so m<=p. Replay the reference birth order from ANY compatible initial erased-bit assignment, skipping existing plus sites. Each remaining addition still has at least two plus neighbors. It follows that every compatible assignment has total perimeter at least the reference perimeter. Apply this argument AFTER removing all contractible loops. Thus the total moving ESSENTIAL perimeter is at least m. This step is why connected pins and frozen initial pockets matter; a low peak barrier alone would not suffice.

## One or at least three parallel moving walls
All essential contours disjoint from gamma are parallel primitive diagonal cycles. The number of other essential contours is odd. Each has physical length at least2L. Put

 rho=13/3, z=rho exp(-8), q=3exp(-8),
 A=100n q^4/(1-q),
 b0=200n 2^(-2L) z^(2L)/(1-z).

The independently certified diagonal nonbacktracking witness bounds the activity of a marked moving wall of length at least M by200n 2^(-2L)z^M/(1-z). Separate ONE from at leastTHREE moving essential loops, paying every contractible/unmarked contour with ordinary pressure:

 J <= exp(A+8m) [200n 2^(-2L) z^max(2L,ceil(m))/(1-z) + b0^3 exp(b0)/6].

For m>=2L, exp(8m)z^m=rho^m<=rho^p. For m<2L, exp(8m)z^(2L)<=rho^(2L)<=rho^p. The three-loop term is negligible uniformly at m<=2.5L: three other diagonal loops cost at least6L of physical perimeter and three displacement tilts, rather than three times merely L. Exact rational log witnesses log rho<1.467 and log2>.693 certify the bound in paid_scalar.py. A conservative common result is

 J <=402n rho^p 2^(-2L) exp(A).

There are at most L visible actual diagonal labels at an edge. Both endpoint ratios and the original n coordinate-current cuts give

 N <=804 n^2 L rho^(2.5L) 2^(-2L) exp(A) C_kappa.

The original capacity receipts then give exact conservative occupation/Z_A exponents48,441,3197,34696 at R80,200,1000,10000, conditional only on the stated reviewed geometry interface, not on any new source distribution.

## Relation to the full diagonal sector
The independent actual two-diagonal-wall tail at total essential perimeter>=4.5L has exponents62,220,1303,13568, with arbitrary contractible defects. Below that threshold both diagonal walls are shorter than2.5L. With the reviewed geometry, tail plus transport covers exactly-two-diagonal-wall sources at exponents47,219,1302,13567 (paying2<e). The exact union receipt reads both fresh branch certificates; geometry and partition have passed independent reviews by fluid, GKP and compute. Zero-essential-wall sources would remain untouched even after such a closure.

## Stronger existential union (final)
Transport requires only ONE eligible actual diagonal wall. If exactly two diagonal walls have total perimeter<5L, their shorter wall is<2.5L. Otherwise the explicitly extended adaptive global winding tail applies. Its exponents1117/2797/13997/139997 and transport48/441/3197/34696 yield the stronger final diagonal exponents47/440/3196/34695, paying2<e. The earlier4.5L union above remains valid but is not the final receipt.
