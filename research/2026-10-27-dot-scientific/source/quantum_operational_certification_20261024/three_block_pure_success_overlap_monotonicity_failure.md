# Coordinate overlap monotonicity fails for an actual three-block reset

Actual source: success sigma=|1><1| on a logical qubit; reset tau=sum_i w_i |i><i| tensor P_vi, with vi=(sqrt(1-ri),sqrt(ri)). Take rational

p=1/4, w=(1/2,1/4,1/4), r=(3/4,99/100,3/40).

Its WH3 deficit is positive, approximately .05215075055947849. However

partial Delta/partial r3 = -.002382242889515570870778523441132899388105036978609.

Thus increasing an individual reset block's overlap with the pure logical success direction can DECREASE the deficit. Coordinate overlap monotonicity cannot receive the full three-block class by moving all blocks away from success.

This is a reproducible high-precision mechanism obstruction, not a negative whole value. Script three_block_pure_success_overlap_exact_failure.py integrates the exact rational derivative. With a=p/3, bi=q wi/3, P_x(s)=x/(x+s), that derivative integrand is

[P_(3a) P_b3/3]/[1-P_(3a)sum_i ri P_bi/3]
 +[P_a P_(3b3)]/[1-r3 P_a P_(3b3)]
 -sum_(i=1,2) [P_a P_b3]/[1-P_a(ri P_bi+r3 P_b3)/2].

All denominators are positive for s>=0 in this witness. This follows directly from the actual scalar success/noise Gram determinants (one success direction, three orthogonal physical reset labels). No phase relation between the vi enters these determinants. The source-level finite-difference replay agrees to its expected precision; the exact resolvent integrand avoids entropy finite-difference cancellation.

## Stronger failure: coordinate endpoint minimization

With the same p,w and r1=3/4,r2=99/100, vary only r3. Exact Gram-entropy evaluation at60 digits gives

Delta(0)=0.0523371123110629105052860704062055952194168591269,
Delta(1/2)=0.051554274660093843888441013425638082995205131352781,
Delta(1)=0.058056123794585622685805756752583741103983823202753.

The interior is strictly below both endpoints. Thus even the weaker strategy 'minimize each reset overlap at0 or1, without assuming monotonicity' fails. The reproducer includes the exact scalar Gram spectral formula, independently of the rational derivative quadrature. These remain positive values and do not refute WH3.

## Full affine coherent-star convexity also fails

In the exact dual source, hold d=p/3=1/12 and x=(3/8,3/16,3/16) fixed and vary the actual affine cross amplitudes c_i. Set c1=sqrt(6)/16, c2=3sqrt(11)/80, c3=0; these encode r1=3/4,r2=99/100,r3=0. The matrices are strictly positive on their six-dimensional supported source algebra, and c3 admits two-sided small variations.

Since r3=c3^2/(d x3), the exact rational overlap derivative gives

partial_r3 Delta at0 = -.00258095850388202995493809920790667794004570318,
partial_c3^2 Delta at0 =128 partial_r3 Delta
 =-.330362688496899834232076698612054776325850008.

Thus the full deficit is not convex even in the affine source variable c3 at fixed x and d. A generic joint shared-Gram convexity theorem on (x,c) cannot be used. Simultaneous permutation balancing remains a strictly weaker separate question; this local counterexample does not refute it.
