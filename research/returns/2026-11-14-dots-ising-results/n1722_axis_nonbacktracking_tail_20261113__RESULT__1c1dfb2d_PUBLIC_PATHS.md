# Rational nonbacktracking tilt: two-axis-wall tail

This is a direct Gibbs-mass estimate that tightens the remaining source sector. It is not a new transport theorem. All contractible walls are permitted; no small-defect-area assumption is imposed.

## Exact walk certificate
After contracting zero dual edges, a physical resolved contour is a nonbacktracking square-lattice walk. Use direction weights w=(3/2,1,2/3,1) for (north,east,south,west), rho=13/4, and h_i=rho-w_opposite(i)>0. The transition matrix is T_ij=w_j unless j is opposite i, in which case zero. Direct rational algebra gives

    rho^2-(2+3/2+2/3)rho+3=1/48>0,
    T h <= rho h,
    (sum_i w_i h_i)/min_i h_i <= 2rho.

Thus the sum of weights of all length-m nonbacktracking walks is at most2rho^m. Every walk of axial displacement L has weight (3/2)^L (orient upward). The safe rooted physical-wall counting factor therefore gives

    count_axis(m) <= 200 n rho^m (3/2)^(-L).

A horizontal axis uses the rotated tilt. This is a standard positive transfer-matrix/Chernoff argument with an exact witness, not a claim of a new general counting method. The code checks the matrix inequalities and forty exact weighted-walk recurrences.

The bound also applies to the deterministic adaptive physical-plus contour encoding: a configuration determines its collection of resolved physical walk sequences. That collection determines the physical disagreement edges, hence the spins up to global reversal. Counting all walk sequences may overcount but cannot miss configurations. Auxiliary diagonal choices do not create an extra independent2^n label factor.

## Exactly two actual axis winding walls
Let H_tail consist of non-target configurations with exactly two noncontractible axis walls, both in the same axial homology, whose TOTAL physical length is at least P0=(23/5)L=4.6L. Other contractible walls are arbitrary. With theta4, phi4/R, L8R, nL^2, non-target volume gives the global field cap exp(phi n)=exp(32L).

Let q=3exp(-8), z=rho exp(-8). The ordinary contractible-loop pressure is

    A=100n q^4/(1-q).

Count two wall lengths by their total P, use at most P+1 compositions, and pay both global spin choices and both coordinate axes. Since z<1/800,

    sum_(P>=P0) (P+1) z^P <= 2(P0+2) z^P0.

Consequently

    Z_Htail/ZA <= 320000 n^2(P0+2)
        *exp[A+32L] *(3/2)^(-2L) *[rho exp(-8)]^P0.

ZA>=w_minus is sufficient; no capacity or additional source oracle is used. Since0<=v<=1, the same bound holds for original voltage-weighted occupation N_Htail/ZA.

Exact receipts verify log(rho)<1.179, log(3/2)>.405, q<1/900. Therefore the principal exponential is at most exp[-.1866L]. The complete finite negative exponents, including roots, axes, length sum and pressure, are

    R80:72, R200:246, R1000:1432, R10000:14856.

## Consequence and limits
Combined with the reviewed short-wall result, a remaining two-AXIS-wall state below this tail threshold has each wall shorter than2.6L+8, provided neither wall already meets p<=2L-8. This narrows a potential area-admissible large-span transport problem; it does NOT supply that transport.

Diagonal actual walls, arbitrary wall multiplicities and no-winding sectors are not included in this two-axis statement. The earlier global winding-perimeter tail and the short-wall theorem may separately cover portions of them. Do not silently replace actual wall homology by plus-seed homology.

No delivered ZIP has been modified; this construction was developed after the frozen short-wall package.
