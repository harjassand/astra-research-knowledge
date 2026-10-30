# One angular certificate for a full 35-dimensional non-polyconvex family

30 October 2026. Root construction. The implication below is conditional
on the literal seed theorem in `../b_angular_repair` until its full
mathematical intake is recorded. The non-polyconvex separation and
convexity-buffer estimates do not depend on that seed theorem.

For a real matrix A=[[a,b],[c,d]], put T=|A|², q=ad−bc,
X=a²+c²−b²−d² and

    F*(A)=T²+12q²+4qX.

Assume the seed theorem supplies a homogeneous degree-three one-form
alpha, C² at zero and smooth elsewhere, such that Omega=d alpha and

    D²F*(A)[B1,B1]+D²F*(A)[B2,B2]+Omega_A(B1,B2) >= 0,
    B1=(h0,h1,h3,h4), B2=(h1,h2,h4,h5),

for EVERY A and h. That premise implies quasiconvexity by the ordinary
componentwise heat flow and the exact-form Stokes identity. It is a
specific seed premise; no general rank-one-convexity implication is used.

## The explicit family

Let G be ANY real homogeneous quartic in all four matrix entries. Its
35 ordinary monomial coefficients are independently allowed to vary.
If

    epsilon = 1/100000,
    rho = 1/84000000,
    ||coeff(G)||_infinity <= rho,
    F = F* + epsilon T² + G,

then F is non-polyconvex. If the seed premise is qualified, F is strongly
quasiconvex and the SAME alpha certifies it without an additional
coefficient search. In particular, for every bounded domain Omega,
constant A and smooth compactly supported phi:Omega->R²,

    integral_Omega [F(A+Dphi)-F(A)]
      >= (1/800000) integral_Omega
           [|A|² |Dphi|² + |Dphi|⁴].                    (1)

Here quasiconvexity is the all-gradient variational inequality, not
positivity on a finite sample or an acoustic test. The radius is small
but explicit, and the family has nonempty interior in the full
35-dimensional space, with no retained rotational symmetry.

## A universal convexity buffer

Each second derivative of a degree-four monomial has absolute value at
most 12|A|². Summing 35 coefficients and using the four-dimensional
matrix norm estimate gives

    ||D²G(A)||_operator <= 1680 rho |A|².

Since D²(T²)=8 A A^T+4|A|² I, the quartic

    H=G+420 rho T²

is convex on all R⁴. Consequently

    F=F*+(epsilon−420rho)T²+H
     =F*+(epsilon/2)T²+H.                              (2)

The seed's completed heat density, plus the positive Hessian densities
of the last two summands, proves the same-certificate assertion.
Its density is bounded below by

    2 epsilon |A|² (|B1|²+|B2|²).

The convex H has nonnegative Bregman remainder. The seed's integrated
remainder is nonnegative by QC; the linear term integrates to zero.
For any Euclidean vectors A,V,

    |A+V|⁴−|A|⁴−4|A|² A:V
      >= (1/4)(|A|²|V|²+|V|⁴).                         (3)

For V!=0 scale |V|=1 and write A=sV+W with W perpendicular to V.
The left side minus the right side equals

    (23/4)(s+8/23)²+(7/4)|W|²+5/92 > 0.

The V=0 case is equality. Equations (2) and (3) prove (1).
They also imply a uniform strict rank-one-convexity margin.

## Robust non-polyconvexity, with unrestricted convex minor lifts

For a differentiable finite polyconvex F, a convex lift on the minors
has a supporting hyperplane at the graph point (A,det A). It is finite
throughout R⁵: every (B,s) is the mean of graph points B±Y with
det Y=s−det B. Thus at A=I some real k must satisfy

    F(I+V)−F(I)−DF(I):V−k det V >= 0 for every V.

For a homogeneous quartic, write F(R+tI)=c0+c1 t+c2 t²+... .
Substitute V=sR into this support inequality, divide by s², use quartic
polarization and minimize its quadratic in s. Whenever c0>0 it requires

    k det R <= c2−c1²/(4c0).                           (4)

The two fixed test directions are

    R+=[[0,200],[-1,0]], det R+=200,
    R−=diag(1,−2),       det R−=−2.

For F* their (c0,c1,c2) are respectively

    (1568560801,0,4808), (97,−8,−48).

For T² they are respectively

    (1600080001,0,160004), (25,−20,24).

The exact l1 norms of the coefficient-to-(c0,c1,c2) rows for G are

    R+: (1608040201,16080402,120603),
    R−: (31,49,42).

They are computed over all 35 monomials, without symmetry reduction, in
`export_family.py` and recorded with the literal rows in
`EXPLICIT_FAMILY.json`. Both c0 are positive: F*>0 off zero and
|G(A)|<=35rho T² while epsilon>35rho. Dropping the nonpositive square
term for R+ in (4) gives the necessary upper bound

    k <= U=(4808+160004epsilon+120603rho)/200.

For R−, c0<=97+25epsilon+31rho and
|c1|>=8+20epsilon−49rho>0. Thus (4) gives the necessary lower bound

    k >= L=[48−24epsilon−42rho
          +(8+20epsilon−49rho)²/(4(97+25epsilon+31rho))]/2.

At the stated rational epsilon,rho,

    U=19238405903/800000000,
    L=18837461610901303279/782210018976000000,
    L−U=167933142714235999/4888812618600000000 > 3/100.

No k exists. This excludes an arbitrary convex representative on all
minors, not just a polynomial lift or a semidefinite parametrization.

## What the origin-regular obstruction means after a positive seed

The ROOT28 closed-cone proof established that some neighborhood of F*
is excluded from finite sums of polyconvex quartics and constant-flow
certificates whose two-form coefficients are C² at the origin. Its
radius delta0 is positive but UNEVALUATED. The named explicit ball
above is NOT asserted to lie in that unknown-radius neighborhood.

For every sufficiently small epsilon>0, the same construction with
rho<=epsilon/840 proves strong QC of a full-dimensional neighborhood
of F*+epsilon T². Choose epsilon also small relative to delta0 and that
neighborhood lies inside the old exclusion region. Thus a qualified
angular seed would demonstrate an actual separation in certificate
expressiveness, not merely failure of one polynomial ansatz. The repair
uses Omega with C¹, generally not C², coefficients at zero; it does not
contradict the earlier obstruction.

## Acquisition, comparison and scope

The root constructed the full35 buffer, the Bregman constant and both
robust support cuts, and executed `export_family.py` using ordinary
integer/Fraction arithmetic in about 0.00026 seconds. The complete
monomial row data is retained. The seed search, exact literal replay,
global cover and heat argument have their own costs and reviews in
`../b_angular_repair`; they are not hidden behind this small export cost.

`compact_hopf.py` independently gives a 14-coefficient Hopf/Euler gauge
for the same candidate (232 coefficient equations, rank14). It changes
alpha by an exact differential and does not change Omega. Its first
ungauged linear system was inconsistent; subtracting
d[(i_A alpha)/4] resolves that representation issue. This was not a
negative mathematical certificate or a new positivity computation.

`check_global_cover.py` records a finite exact principal-minor diagnostic
at eleven rational matrices. Those checks are NOT a universal proof;
the seed's analytic symmetry cover and exact univariate positivity are
the governing evidence. A sign concern raised during root intake was
resolved: the consumer's `add(p,q)` tests p+q, so its reflection tests
enforce ANTI-pullback, as required by domain orientation.

Ordinary convexity and the existing polynomial/PC methods are admitted
at full strength. The seed is anisotropic and invariant under left row
rotations; it is not assumed to fall in the left-and-right rotational
class already covered by Bruno–Pasqualotto2608.06367v1 AppendixA.
Historical priority and general Morrey implications remain UNKNOWN.
There is no physical material, measured computational advantage,
laboratory operation or civilisation-level capability claim here.
