# Expanding-filter power has neither universal convexity nor concavity

26 October 2026. Exact actual-source scope guard for the anchored comparison. Independently received PASS in `qutrit_filtered_seed_equality_and_curvature_independent_audit.md`.

Let Omega=sum_i |ii>, S_a=|Omega><Omega|+a I9, a>=0, and
Z_u=diag(sqrt(u),1,1), u>=1. Define S_a(u)=(I tensor Z_u)S_a(I tensor Z_u).
The reference minimum filter eigenvalue is one, so subtraction of the fixed
unfiltered deficit does not change any u derivatives.

At u=1, direct BKM differentiation yields

 D_a''(1)=(14a+3)/9 + [4a(a+3)/27] log((a+3)/a)
                       -2a(a+1) log((a+1)/a).                 (1)

For a>0 this is an ordinary faithful derivative. To verify the factors,
replace the actual congruence by the isospectral affine Gram path
S_a^(1/2)[I+(u-1)(I tensor P0)]S_a^(1/2), separately for input,
reference and unscaled output. Write ell(x,y)=(log x-log y)/(x-y).
The three BKM contributions are respectively

 input: (23a+3)/9 + [4a(a+3)/9] ell(a+3,a),
 reference: 1+3a,
 output: 4a+1+4a(a+1) ell(2a+2,2a).

Input uses the rank-one maximally entangled projector P and
Tr[(P_perp (I tensor P0) P_perp)^2]=22/9, while
Tr[P (I tensor P0) P_perp (I tensor P0)]=2/9.
Output uses the antisymmetric projector P_minus and
Tr[(P_minus (I tensor P0) P_minus)^2]=1/2;
the cross trace is also 1/2 and the symmetric-block square trace is 3/2.
These give (1) with output coefficient ONE, as required for f(2NS).

At a=1,

 D_1''(1)=17/9-(76/27)log2 < -125/2187 <0,

because log2=2 sum_{n>=0}[(1/3)^(2n+1)/(2n+1)]>56/81.
Analytic continuity in u gives strictly negative curvature for u>1
sufficiently close to one, inside the actual expanding-filter domain.

At a=0, the pure-state Schmidt weights are (u,1,1). Direct pure-state
differentiation gives D_0''(1)=1/3>0. Alternatively (1) tends to 1/3 as
a decreases to zero, so faithful small positive a also have positive
curvature, again persisting at u>1.

Thus universal convexity AND universal concavity in expanding-filter power
are false even on white-reset commuting sources. This does not refute
monotonicity, the anchored finite-filter inequality, or whole source value:
these commuting sources are already paid. It only blocks an unsupported
shape argument from the nonnegative unfiltered score.
