# Actual two-diagonal-wall tail and residual length reduction

This is a direct original-source Gibbs-mass/occupation tail, not a native-growth theorem. It treats the SAME deterministic physical-plus contour encoding as the two-axis work.

## Rational directional witness
For directions north,east,south,west give step weights (2,2,1/2,1/2). Let rho=13/3 and h_i=rho−w_opposite(i). The nonbacktracking transition T_ij=w_j except immediate reversal satisfies T h<=rho h, with exact polynomial slack rho²−5rho+3=1/9. Also (sum_i w_i h_i)/min h<=2rho.

Therefore the total weighted count of length m physical nonbacktracking walks is at most2rho^m. Any walk of displacement(L,L) has weight2^(2L), so the safe physical-root count gives

 count_diagonal(m)<=200n rho^m 2^(-2L).

Reflections handle the other diagonal slope. All resolved simple essential walls in a disjoint pair have parallel primitive homology; the scope here is primitive norm2, not arbitrary larger windings.

## Source-compatible global tail
For non-target states the unchanged global field cap is exp(phi n)=exp(32L). Put q=3exp(-8), z=rho exp(-8), A0=100n q^4/(1−q). Exactly two actual diagonal walls with total perimeter P>=P0=9L/2 obey

 Z_tail/ZA, N_tail/ZA <=320000 n²(P0+2)
       exp(32L+A0) 2^(-4L) z^P0.

The factor includes two diagonal slopes, global spin reversal, both rooted wall counts and the geometric length-composition sum. Every contractible wall is allowed, with its ordinary pressure retained. ZA>=wminus and0<=v<=1 suffice; no source equilibrium law or altered clock enters.

Exact rational receipts verify log rho<1.467, log2>.693, q<1/900 and z<1/600. The principal exponent is at most−.1705L. After all displayed prefactors and pressure:

 R80: exp(-62), R200: exp(-220),
 R1000: exp(-1303), R10000: exp(-13568).

`check.py/json` verifies the positive transfer-matrix witness, forty weighted-walk recurrences, exponential inequalities and finite bounds. Floating point is used only to propose an integer upper bound for a prefactor logarithm; a positive rational Taylor lower bound independently certifies each choice.

## Remaining actual-source sector
Below the tail threshold, each of the two actual diagonal walls has physical length<2.5L, because the other has minimum length2L. This is a useful scope reduction for the native diagonal construction and its thermal-prefix partition. It does NOT establish such a construction or count an abstract plus-seed family as the whole actual-wall source.

No-essential-wall states and the near-geodesic two-diagonal sector remain open. A union with existing axis bounds must explicitly pay its additional branch count or use an appropriately stronger scalar absorption argument.
