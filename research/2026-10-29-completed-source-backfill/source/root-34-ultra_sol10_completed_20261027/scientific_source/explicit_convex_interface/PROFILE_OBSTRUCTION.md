# A concrete determinant-dependent rational profile is impossible

The larger architecture excluded in `NORMAL_POLYNOMIAL_OBSTRUCTION.md`
requires a rational lift to use its determinant coordinate s inside the
denominator. We therefore constructed and tested the following actual
two-parameter alternative, not a catalogue of future candidates.

For the old accepted rational-selector F and its degree-six numerator p6,
write T=|B|^2, q=det B, d=s-q and H=T+sigma. For sigma>0 consider

    g(B,s)=epsilon T
       +[F(B)H^2+p6(B)d+alpha T^2d^2+c d^2(s^2+H^2)]
                                               /(H^2+d^2).       (1)

The denominator is everywhere positive, so (1) is globally C-infinity and
rational. It has the required graph values F+epsilon T, and its normal
derivative on the graph is exactly p6/(T+sigma)^2, the smoothed selector
of the structural-opening theorem. The last numerator term was chosen
so that its large-|s| behavior is c s^2+O(1/s), avoiding a spurious
negative B-curvature from an uncancelled H^2 term.

**Theorem.** Formula(1) is not globally convex for ANY real alpha,c, ANY
sigma>0 and ANY epsilon>=0. The failure is certified by three rational
directional Hessian evaluations and positive rational weights. It does
not exclude other rational lifts with s-dependent denominators.

## 1. A necessary homogeneous limit

If g were convex, so would be g(tB,t^2s)/t^4 for each t>0. Their pointwise
limit is

    g_infinity(B,s)=[N0+alpha Nalpha+c Nc]/D,
    D=T^2+(s-q)^2,
    N0=F(B)T^2+p6(B)(s-q),
    Nalpha=T^2(s-q)^2,
    Nc=(s-q)^2(s^2+T^2).                                  (2)

At the sole zero denominator B=0,s=0 define this limit as0, as follows
directly from (1). The limit is finite everywhere and hence convex if g
is convex. The proof only uses its Hessian at points with B!=0, where
(2) is a smooth rational function.

## 2. Three exact rational curvature cuts

For a point P and direction v let H_j(P,v)=D_v^2(N_j/D)(P). Convexity of
(2) requires

    H_0(P,v)+alpha H_alpha(P,v)+c H_c(P,v)>=0.               (3)

Take these three pairs; every displayed decimal is an exact terminating
rational, not an approximate location or direction.

| i | P=(a,b,c,d,s) | v |
| --- | --- | --- |
| 1 | (-.57,.29,.28,.72,-1.18) | (.90,.01,-.41,.07,-.13) |
| 2 | (1,0,0,0,-2) | (1,0,0,.04,.04) |
| 3 | (.89,-.04,-.39,-.25,-1.74) | (.92,-.03,-.39,.05,.04) |

`verify_profile_obstruction.py` reconstructs F and p6 literally with
standard-library Fraction polynomial arithmetic. It evaluates each
curvature by the exact quotient identity

    D^3 D_v^2(N/D)
      =D^2 D_v^2N-D[2(D_vN)(D_vD)+N D_v^2D]+2N(D_vD)^2.

It then solves the EXACT rational three-by-three system

    sum w_i=1,
    sum w_i H_alpha(P_i,v_i)=0,
    sum w_i H_c(P_i,v_i)=0.

All three rational weights are strictly positive. Their decimal displays
are approximately(.5992326436,.2816384623,.1191288941). The exact weighted
constant is strictly smaller than-3/20, with display-0.1552361958582027.
Thus the weighted sum of(3) is strictly negative independently of BOTH
parameters. This proves the theorem, including parameters of either sign.
`EXACT_PROFILE_OBSTRUCTION.json` contains all rational curvatures and
weights; exact arithmetic, not the decimal displays, supplies the proof.

## 3. Acquisition and boundaries

The proposed formula was tested before extracting this obstruction.
`rational_profile_search.py` evaluated513 Hessian constraints and acquired
a negative best sampled margin. This took1.65454s after imports, including
0.97463s symbolic compilation and0.53787s in the small-parameter conic
solve. That finite diagnosis alone was not an impossibility certificate.
The three rational evaluations above were rounded from the dominant
dual suggestions and then reconstructed from scratch. The standalone
exact replay took0.02917s after literal polynomial setup. Startup/import
costs are not included in these measurements; no efficiency advantage is
claimed. All acquisition work, including the failed profile, is retained.

The finite order-two moment operation in `FINITE_OPERATION.md` succeeds
as a global convex evaluator and is independently accepted. It has
corners at every graph point and is therefore outside the global smooth
target. This rational profile supplies an exact additional obstruction;
it does not close that target. A directly evaluable globally convex
smooth representative remains NOT_ACQUIRED.
