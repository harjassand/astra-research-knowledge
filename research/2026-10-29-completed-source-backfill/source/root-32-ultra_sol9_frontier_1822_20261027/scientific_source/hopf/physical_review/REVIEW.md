# Independent substantive review: orientation-preserving elastic completion

**Disposition: ACCEPTED at the mathematical scope below.**

The completion of the accepted Hopf quartic is a smooth objective stored
energy on GL+(2), nonnegative with exactly the stated stress-free well,
quartically coercive, divergent at determinant zero from above, and strictly
rank-one convex. It remains genuinely non-polyconvex on GL+(2). Right
normalization moves the zero set to SO(2), and the resulting material remains
anisotropic. The infinite aligned family retains its contradictory minor
supports wholly inside GL+(2), away from the barrier.

This is an exact constitutive construction, not a material identification,
physical measurement, experimental validation, proof of global QC, or
existence theorem for minimizers. The claim does not place a non-PC failure
at a zero-energy stress-free minimum.

## Independence and accepted premises

I whole-read inversion/prior_challenge/PHYSICAL_DOMAIN.md, verify_completion.py,
and outputs/COMPLETION_REPLAY.json. I did not execute or import the producer's
verifier. The companion verify_independently.py reconstructs the finite
witness directly with Fraction arithmetic and separately checks the critical
symbolic identities. Its REPLAY.json contains the exact outputs.

The original strict-ROC theorem and its explicit margin are accepted from
the completed independent Hopf audit. The aligned family support gaps are
also accepted mathematical inputs; here their minimizing scale and the
physical-domain admissibility are independently reconstructed. Barrier
smoothness, convexity, divergence and domain arguments are proved below,
rather than inferred from numerical integration or finitely many derivatives.

## 1. The complete main witness already belongs to GL+(2)

At A=diag(36,35), I independently reconstructed all three matrices B_i and
their positive weights. They have exact matrix mean A and determinant mean
detA. Their determinants, including the base, are

    1260,
    3622910039/2874500,
    630011/500,
    28992/25.

Every one exceeds1/2. Literal quartic evaluation gives the same strict gap

    sum_i lambda_i F(B_i)−F(A)
       =−13534664264487807/296890944920312500.

Consequently non-PC already holds for the restriction of F to GL+(2).
Jensen for any convex minor lift only uses these positive-determinant graph
points. It does not require extending that lift to orientation-reversing
matrices, differentiating it, or assigning it finite values everywhere.

## 2. Square completion, zero set and stress-free property

For the aligned family the exact identity is

    F=x²+y²+4beta qx+4r q²
      =(x+2beta q)²+y²+4c q², c=r−beta²>0.

Hence

    W_flat=F−8c q+4c
          =(x+2beta q)²+y²+4c(q−1)².

Both identities were independently expanded. This proves nonnegativity
and identifies all zeros: q=1, y=0 and x=−2beta. The column Gram identity
uv=w²+q² then gives u v=1 and u−v=−2beta, so

    u=sqrt(1+beta²)−beta,
    v=sqrt(1+beta²)+beta.

Both are positive. The columns are orthogonal and their determinant is
positive, so the zero set is exactly SO(2)A0 with
A0=diag(s,1/s), s²=sqrt(1+beta²)−beta. Conversely every such matrix
annuls all three squares. The gradient is zero there because each square
has zero factor. The independent symbolic replay also checks the gradient
by substituting beta=(s^−2−s²)/2 directly, without trusting simplification
of nested square roots.

The main coefficients give c=25399/10000, exactly as stated. The addition
−8c detA+4c is affine in the minors, and therefore preserves PC equivalence
on the SAME domain. It is a null Lagrangian for compatible zero-boundary
variations, preserving QC equivalence on that same admissible domain.
Along rank-one lines detA is affine, so it also preserves ROC. This step
does not conflate a GL+ restriction with an unrestricted-domain QC claim.
The resulting W_flat is nonhomogeneous of degrees4,2,0 and no longer
has the original even-Hopf symmetry; the producer explicitly states this.

## 3. Smooth convex determinant barrier

For delta=1/2 define

    k(q)=e^(−1/(delta−q))/q⁴ on0<q<delta, zero above;
    b(q)=integral_q^delta (t−q)k(t)dt below delta, zero above.

For every q>0 below delta the integral is finite. Differentiating by
Leibniz gives

    b'(q)=−integral_q^delta k(t)dt<=0,
    b''(q)=k(q)>=0.

Thus b is nonnegative, nonincreasing and convex. Its flat gluing is valid:
put z=delta−q. Every derivative of k near delta is e^(−1/z) times a
rational expression bounded by some power of1/z. For every integer N,
e^(−1/z)z^(−N) tends to zero; one elementary proof uses
e^(1/z)>=(1/z)^(N+1)/(N+1)!. Therefore every derivative of k tends to
zero. The integrals defining b and b' also tend to zero, while all higher
derivatives are derivatives of k. Hence b is C-infinity across delta,
with every derivative zero there. This proves the whole smoothness claim,
not just a finite symbolic derivative check.

For0<q<delta/4, restrict integration to2q<=t<=delta/2. On that interval,
t−q>=t/2 and e^(−1/(delta−t))>=e^(−2/delta). The exact integral is

    integral_(2q)^(delta/2) 1/(2t³)dt
       =1/(16q²)−1/delta².

This is positive in the stated range and diverges as q decreases to zero.
It proves the claimed lower bound and actual determinant blowup. Extending
b by positive infinity for q<=0 is convex because its finite domain is
the convex interval(0,infinity), and is lower semicontinuous because the
one-sided boundary limit is positive infinity.

No exact closed form for the original exponential integral, quadrature
error, or floating extrapolation is needed.

## 4. Completed energy: coercivity, compact sublevels and rank-one domain

Define W=W_flat+b(detA) for detA>0 and positive infinity otherwise.
It is C-infinity on GL+(2), and objective under left SO(2), because
x,y,q and the barrier are invariant under those proper row rotations.
The barrier vanishes on the natural well q=1, so the exact zero and
stress-free statements above remain unchanged.

If lambda_min(K)=lambda>0 and t=|A|², then

    W(A)>=lambda t²−4c t+4c
         >=(lambda/2)t²−8c²/lambda+4c.

The first inequality uses |detA|<=|A|²/2 and b>=0. This gives quartic
coercivity with explicit positive leading constant. On a fixed finite
sublevel, |A| is bounded. Because W_flat>=0 and b(q) diverges at zero,
the determinant is bounded away from zero there. Continuity on GL+
then makes each such sublevel closed in ambient R4 as well as bounded,
hence compact and contained in GL+. Connectedness is not claimed.

For a rank-one direction R, D²det(A)[R,R]=2detR=0. Thus

    D²[b(detA)][R,R]=b''(detA)(cofA:R)²>=0.

The accepted half-Hessian margin7/35200 for F survives unchanged for
W on GL+. The positivity domain of det(A+tR) is an interval because
that determinant is affine in t. On the interval W is convex along the
rank-one line; extending by infinity outside preserves extended convexity.
There is no use of a segment whose finite endpoints pass through a forbidden
determinant region.

All four main Jensen determinants exceed delta. The barrier is therefore
EXACTLY zero at all of them, and the determinant-affine shift cancels by
the exact determinant mean. The strict Jensen gap is unchanged. Adding
a convex function of det generally need not preserve non-PC, but here
the actual flat-witness calculation proves that it does.

## 5. Normalization and the location of the obstruction

Set V(A)=W(A A0). Right multiplication by the invertible det-one A0
preserves GL+, rank-one directions, and the determinant. It also preserves
PC by an invertible linear change of the matrix minor coordinates, and
preserves QC by the standard corresponding invertible change of independent
variables. Norm equivalence supplies quartic coercivity and a positive
weighted strict-ROC constant after this right multiplication.

The zero set of V is exactly SO(2); V(I)=0 and DV(I)=0. The main witness
is transported to C_i=B_i A0^−1, with mean A A0^−1. Both determinant
mean and gap are unchanged, as independently verified algebraically.
This mean has determinant1260 and so cannot be I or any member of SO(2).

The distinction is essential: V>=0=V(I), so the constant-zero minor-affine
function supports V at I, and V is QC at I by nonnegativity. The producer
does NOT claim non-PC at the stress-free well, a local instability there,
or a compatible-gradient violation.

I also independently derive the material-anisotropy test. For
D=diag(2,1) and a right quarter-turn Q,

    V(D)−V(DQ)=−12beta sqrt(1+beta²),

which is nonzero at the main beta and every stated family beta. Both
determinants equal2; barrier and determinant-affine terms cancel. The
normalization has not created right rotational isotropy.

## 6. Infinite family: both incompatible cuts are admissible in GL+

For beta=(m²−1)/(m²+1), r=4, m>=197, the accepted original cut base
is I. With Rplus=[[0,m],[-1,0]],

    det(I+tRplus)=1+m t²>=1.

Thus every nonzero sufficiently small t used for the limiting local upper
support cut lies in GL+ and the barrier-flat region. At Rminus=diag(1,−2),
independent expansion of F(Rminus+tI) gives the minimizing scale

    tstar=(18beta−14)/(24beta+73).

It is positive for beta>7/9. Its derivative in beta is
1650/(24beta+73)²>0, and beta_m<1, so tstar<4/97. The function
(1+t)(1−2t)=1−t−2t² is strictly decreasing for t>=0. Consequently

    det(I+tstar Rminus)>8989/9409>1/2.

The replay independently verifies these inequalities as positive
polynomial coefficients after m=197+z, z>=0. Therefore the finite lower
cut also lies wholly in GL+, beyond the barrier threshold. At the base
the barrier and its first derivative are zero.

For W=F−8c det+4c on these points, its support coefficient k_W would
produce the original F support coefficient k_F=k_W+8c. Thus the accepted
strict incompatibility between the upper and lower F cuts persists for W
on the positive-determinant domain. The domain restriction does not silently
reuse a minimizer outside GL+.

For the normalized family V, this obstruction is transported from I to
A0^−1, which is distinct from its stress-free well SO(2) for beta>0.
The pre-normalization base I is not a minimum: W(I)=4beta²>0.

## 7. Convex representatives on the GL+ graph

The support argument remains valid when a convex representative is specified
only to agree on positive-determinant graph points. The claimed convex hull
is indeed R4 times(0,infinity).

Here is a direct independent construction for every invertible matrix B
and target determinant d>0. Put alpha=d/detB−1 and

    u=(1−alpha)/2, v=(1+alpha)/2,
    Z=[[u,v],[-v,−u]], Y=BZ.

Then trZ=0, detZ=alpha and det(I+Z)=det(I−Z)=1+alpha.
Thus det(B+Y)=det(B−Y)=d, and their average is B. This works for
both signs of detB. For singular B, a signed-diagonal reduction by proper
left/right rotations puts B into diag(s,0) or0. Taking an off-diagonal
Y of determinant d gives cofB:Y=0 and the same two positive-determinant
points. This confirms the producer's construction, including rank-zero
and rank-one B.

Conversely a convex combination of positive determinant graph points has
positive final minor coordinate, proving exact equality of the hull.
A convex representative finite at every GL+ graph point is therefore
finite throughout this open halfspace. It has a subgradient at the graph
point(I,1). Differentiating the touching minor-affine function along the
open GL+ graph fixes the entry coefficient in the usual way and gives the
scalar support used above. No finiteness on q<=0 is required.

## Scope and ordinary comparator

I checked the supplied primary Voss–Ghiba–Martin–Neff arXiv2009.09690v1
text at Proposition3.5. It already gives an objective isotropic non-PC
ROC energy on GL+(2) with compact connected sublevels, using a nonpolynomial
volumetric-isochoric formula with determinant blowup. Thus the broad elastic
phenotype is established prior science. The present result transfers this
particular positive polynomial family's exact separation through an explicit
stress-free normalization and smooth barrier; the completed function itself
is nonpolynomial, nonhomogeneous and no longer even Hopf.

No material is specified or measured. Global QC, global energy-minimizer
existence, and historical priority remain UNKNOWN. The completed independent
review accepts the exact constitutive/domain statements and their finite
non-PC witnesses at their actual scope.
