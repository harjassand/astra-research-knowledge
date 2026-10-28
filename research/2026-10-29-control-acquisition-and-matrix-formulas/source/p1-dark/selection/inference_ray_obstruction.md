# A full-law obstruction to too few scalar rays

28 October 2026. A simple exact adaptive-query bound, independent of noise,
hidden rank, rational interpolation, or pole-identification algorithms.

Fix n controls, total dose delta>0, coupling cap G>0, and known c0>0. Restrict
the legal source class to B=0, so

    R_w(u)=r0+c0+sum_i w_i u_i, 0<=w_i<=G^2.

This is a valid rank-one affine-SPD source already in one microscopic
dimension: Q0=c0, e=1, and actuator matrix V_i=w_i. A factor v_i=sqrt(w_i)
exists; rational V_i and rational raw reactions do not require v_i itself
to have rational entries.

Consider a deterministic adaptive algorithm making at most m<n nontrivial
scalar source queries before claiming a uniform full-law prediction. Run
it on the center source w0=(G^2/2)1, and retain its actual query vectors
u^(1),...,u^(m). Their m-by-n matrix has a nonzero null vector h. Normalize
it so ||h||_infinity=1 and define

    w_plus=w0+(G^2/2)h,
    w_minus=w0-(G^2/2)h.

Both source vectors belong to [0,G^2]^n. At every recorded query they give
exactly the center source's raw reaction. Hence, by induction on the
algorithm's decisions, both produce the same adaptive queries and the same
complete transcript. Select an index i with |h_i|=1. At the legal command
u*=delta e_i,

    |R_plus(u*)-R_minus(u*)|=delta G^2.

Any common point prediction has absolute error at least delta G^2/2 on one
of these sources. Any uniformly valid interval must have width at least
delta G^2 at that command. Thus fewer than n native scalar queries cannot
give a uniform full-law guarantee stronger than this in the worst case,
even with exact readout and unlimited computation. Known baseline readings
do not constrain w and do not count among the m informative rows.

The same argument applies if the information obtained on each selected ray
is its entire exact curve R(s w_direction): on this linear subclass the
curve supplies only the one inner product with w_direction. Consequently
arbitrarily accurate Stieltjes reconstruction along fewer than n such rays
does not determine the angular dependence of the full law.

Fixing a randomized algorithm's seed gives the corresponding deterministic
witness. No minimax expected-risk or distributional lower bound is claimed.

## Exact rational four-control illustration

Take G=1, delta=1/5, c0=1 and

    w_plus=(1,0,1,0), w_minus=(0,1,0,1).

Use three ray directions

    (1/2,1/2,0,0), (0,1/2,1/2,0), (0,0,1/2,1/2).

Every entire ray has the same response `R(s w_direction)=r0+1+s/2`
for the two sources, for all 0<=s<=1/5. Yet their responses differ by
exactly 1/5 at `(1/5,0,0,0)`. Here even the actuator vectors can be taken
rational: their scalar values are zero or one.

This is a modest but unconditional acquisition boundary within the stated
source class. It does not claim an n^2 lower bound from parameter counting,
and does not prevent the n singleton queries that exactly learn this
linear subclass. Its role is to block transferring a one-ray result to an
entire many-control law without paying for directional information.
