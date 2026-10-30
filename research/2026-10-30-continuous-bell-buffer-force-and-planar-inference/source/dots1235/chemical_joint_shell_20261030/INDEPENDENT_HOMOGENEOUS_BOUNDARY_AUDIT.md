# Independent audit: homogeneous factorial boundary limit

Reviewed 2026-10-30. Source: `HOMOGENEOUS_FAST_BOUNDARY_LIMIT.md`.

**Pass.** The claimed uniformity includes zero, bounded, and disabled minority coordinates; it does not assume all coordinates tend to infinity.

For p=(1-alpha)a+alpha b>0, the fixed-shift asymptotic gives |h_ab(m)-m^p|<=C m^(p-1) for sufficiently large m. If p>=1, its supremum up to N is O(N^(p-1)); if 0<p<1, it is O(1). The bounded-m remainder is O(1) in either case. Dividing by N^p gives exactly O(N^-min(p,1)). For m<a the source is disabled and the approximating term is O(N^-p). If a=b=0, the normalized factor is identically one and requires no limiting estimate.

Each normalized coordinate factor is uniformly bounded. Expanding a finite product therefore transfers the one-coordinate bounds uniformly to the complete gain. Conservation |y|=|y'|=D makes the sum of interpolated exponents exactly D. The corresponding loss estimate is the ordinary falling-factorial uniform limit. This proves uniform convergence of the entire normalized fast generator on the closed composition simplex.

At the pure-C endpoint of the cubic triangle, every source other than 3C has positive A exponent in both its loss and its interpolated gain, hence vanishes; every nontrivial outgoing gain from 3C also vanishes because its target has positive A exponent. The endpoint value is minus the pure-C outgoing rate sum. The analogous statement holds at pure A. For the doubled-edge v2 these values are -3 and -2, respectively. Continuity and uniform convergence yield fixed endpoint cones with a uniform negative order-N^3 fast drift.

Multiplying by (B)_4 and combining with the independently checked lower-than-cubic connector/return corrections proves the stated extreme-composition F inequality uniformly in B>=4. The balanced high-B region still uses the separate bulk theorem, as the source correctly states.

Reviewed hash:
35f2b30f25403a2a9a4854fa386215a468924b6fec5e5bd96831c4a91db5078d  chemical_joint_shell_20261030/HOMOGENEOUS_FAST_BOUNDARY_LIMIT.md
