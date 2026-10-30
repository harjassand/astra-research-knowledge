# Whole mathematical challenge of the positive angular seed

30 October 2026. A's independent review. **ACCEPTED at the stated
mathematical scope**, after reconstructing the analytic argument and
running an independent exact supplied-data consumer. No correction to
the frozen seed is requested. There is no general Morrey, historical
priority, physical implementation or practical-discovery-speed claim.

The reviewed seed is exactly

    F*(A)=T²+12q²+4qX,
    A=(a,b,c,d) row-major, T=|A|², q=ad-bc,
    X=a²+c²-b²-d².

The review covers B's PROOF.md, EXACT_ALPHA.md, the literal certificate,
receive_literal.py and its saved replay; root's compact Hopf/Euler
representation, explicit full35 family and final ALIGNED_CONE. It does
not import or review B's separate INTRINSIC_REDUCTION as a premise.

## 1. The literal matrix is the actual compatible heat completion

For a smooth gradient A=Du,

    A_x=B1=(h0,h1,h3,h4), A_y=B2=(h1,h2,h4,h5).

Thus the six-dimensional jet is the actual common-mixed-partial space,
not two freely chosen four-vectors. Set alpha=sum P_i/T dA_i, with the
100 literal rational degree-five numerator terms in the certificate.
I independently differentiated it to obtain

    T² Omega_ij=T(partial_i P_j-partial_j P_i)
                          -2(A_i P_j-A_j P_i).

The convention Omega_ij=partial_i alpha_j-partial_j alpha_i gives
Omega(B1,B2)=sum_ij Omega_ij B1_i B2_j; there is NO extra factor 1/2 in
that evaluation. If D clears all P denominators, the receiver's integer
matrix is exactly 2D T² times the matrix of

    D²F*(A)[B1,B1]+D²F*(A)[B2,B2]+Omega(B1,B2).

The factor 2 pays symmetric-matrix polarization. Both my reconstruction
and the literal B receiver use that normalization. The resulting minor
factors are compared with the positive multiplier (2D)^k. D is exactly
633914087903460. This discharges a potentially consequential factor/sign
interface, not merely agreement of coefficient hashes.

## 2. The global symmetry cover is valid, including its orientation

The apparent column-swap danger is resolved by the actual literal sign.
The receiver's add(p,q) defaults to p+q, so its zero assertion proves
S*alpha=-alpha, NOT positive pullback invariance. For A'=AS,

    B1'=B2 S, B2'=B1 S,
    h'=(h2,h1,h0,h5,h4,h3).

Consequently the anti-pullback of Omega and the exchange of B1,B2 cancel.
For C=diag(1,-1), A'=CAC has
h'=(h0,-h1,h2,-h3,h4,-h5); its spatial reflection supplies the same
orientation cancellation. Output SO(2) has positive pullback invariance.
The polynomial Lie identity exponentiates along its complete rotation
flow. T is unchanged by these transformations.

I additionally checked the WHOLE polynomial-density congruences, rather
than relying only on the primitive's symmetry. My consumer verifies the
two discrete 6x6 congruences and the full rotation Lie matrix identity.

For every nonzero A choose a longest column, swap if needed, use an
output SO(2) rotation to make it (a,0) with a>0, then scale by a. This
gives (1,b,0,d) with b²+d²<=1. Homogeneity and the established congruences
preserve PSD. Thus this is an all-gradient cover. Zero is handled by
continuity, not by division by T. The canonical proof on all b and
-1<d<1 is stronger than the interior of the required disk; its continuous
limits include d=±1 and the legitimate conformal null directions.

## 3. Exact global positivity, not a grid or solver conclusion

I whole-read B's sparse differentiation, Bareiss exact-division and
integer Sturm algorithms. They are sound. The common positive scaling
in pseudo-division preserves Sturm signs; endpoint factors are removed
before counting, while positivity is tested on the ORIGINAL polynomial
at zero. Nonconstant final gcd/repeated roots cause no omission in the
standard p,p' Sturm count with nonroot endpoints.

My separate consume_exact.py imports no producer/CAS/optimizer code.
It rebuilds the full density from the literal P and F*. It computes the
six determinants by division-free subset expansion, not Bareiss, and
verifies every supplied factor coefficient and positive outer constant.
All factors have a nonzero constant-u slice, u=b². This matters: merely
nonnegative higher slices would not establish strict positivity at b=0.

Independent Fraction long-division/Sturm arithmetic proves all 67
nonexceptional nonzero slices strictly positive on (-1,1). The skipped
p1 slice of the last factor is genuinely NOT assumed positive. For it
the independently rebuilt 4p0p2-p1² has degree 52, endpoint multiplicities
4 and 4, and Sturm variations 22,22 after stripping those factors; its
original value at zero is positive. Therefore it is positive throughout
the open interval. Since p2>0,

    p0+p1u+p2u²=p2(u+p1/(2p2))²+(4p0p2-p1²)/(4p2)>0.

All higher slices are nonnegative for u>=0. Hence every leading minor is
strictly positive inside the certified strip. Sylvester's criterion,
continuity and the cover in section 2 prove the completed density is
PSD for EVERY compatible jet at EVERY matrix A.

The independent exact computation took 2.4561 seconds, of which 0.0693
seconds were determinant expansion. It checked supplied universal
polynomial identities and sign statements, not new point cases, a PDE,
source samples, optimizer output or an inference from finite diagnostics.

## 4. Origin, Euler/Hopf gauge and the QC implication

Each raw coefficient P_i/T is degree three and smooth on the sphere.
Its derivatives of order j<=2 are O(|A|^(3-j)); extending them by zero
at the origin proves alpha is globally C². Omega=dalpha is C¹ with
degree-two coefficients. This supplies classical chain rules and Stokes
even where Du=0. It does NOT supply an origin-C² two-form or a C³
primitive, and it does not contradict the earlier stricter obstruction.

Writing R=i_E alpha_raw, the Euler correction alpha_raw-dR/4 has the
SAME exterior derivative. It still has degree-three, sphere-smooth
coefficients. The root/B Hopf expressions agree because

    X²+Y²+Z²=T²,
    y dx-x dy=(Y dX-X dY)/T²,
    y dz-z dy=(Y dZ-Z dY)/T²,
    eta=(-c da-d db+a dc+b dd)/T.

Their four denominator-cleared identities are an ordinary exact gauge
change, not a new singular chart or different positivity certificate.

For a particularly clean boundary proof take a periodic smooth v and
u=Mx+v. With v_t=Delta v, A_t=Delta A, so

    d/dt integral F*(A)=-integral [F*''(A)[A_x,A_x]
                                         +F*''(A)[A_y,A_y]].

The pullback A*alpha is a global periodic C¹ one-form. Its exterior
derivative integrates to zero on the torus. Adding its density therefore
makes the right-hand side nonpositive by the proved completion. As
t tends to infinity, Dv tends uniformly to zero, yielding Jensen's
gradient inequality integral F*(M+Dv)>=volume F*(M).

For a compactly supported smooth test on any bounded domain, place it
inside a larger square, extend it by zero and periodize. Subtract the
unchanged outside-domain energy. This proves ordinary quasiconvexity
without an unpaid boundary limit at spatial infinity. Density in W1,4
and quartic growth give the corresponding Sobolev version where desired;
no false W1,infinity norm-density assertion is needed. This establishes
the actual global QC conclusion, not only pointwise heat-state algebra.

No uniform coercive margin is inferred for F* itself. The proof retains
its null orbits and does not infer strict Legendre--Hadamard positivity.

## 5. Full35 strongly-QC, non-PC export

I independently reconstructed root's entire 35-monomial line-coefficient
map at R+=(0,200,-1,0) and R-=(1,0,0,-2), all six row l1 norms, the seed
and T² coefficients, and the exact rational upper/lower support gap.
All match the supplied export without importing its compiler.

The non-PC support argument is valid for an ARBITRARY convex minors
lift: the convex hull of the minors graph is all R⁵, since (B,s) is the
midpoint of graph points B±Y with det Y=s-det B. A finite lift has an
affine support, and differentiability of F gives
F(I+V)-F(I)-DF(I):V-k det V>=0. Homogeneous polarization and minimizing
the resulting quadratic give k det R<=c2-c1²/(4c0). The two robust cuts
are therefore necessary without a polynomial/SOS assumption on the lift.
At epsilon=1/100000 and rho=1/84000000 their gap is the stated positive
Fraction, greater than 3/100. Both c0 are positive. This proves non-PC
for the ENTIRE independently varying coefficient box.

For the positive side, every Hessian entry of a quartic monomial is
bounded by 12T, so ||G''||<=1680rho T. Thus H=G+420rho T² is convex and
epsilon-420rho=epsilon/2. The decomposition

    F*+epsilon T²+G=F*+(epsilon/2)T²+H

retains the SAME angular correction and has a global coercive buffer.
The norm-four Bregman bound is indeed at least
(|M|²|V|²+|V|⁴)/4: after scaling |V|=1 its remainder is
(23/4)(s+8/23)²+(7/4)|W|²+5/92. Integrating linear terms to zero proves
the stated weighted strong-QC modulus 1/800000. The finite matrix and
support arithmetic independently passes exactly.

The old origin-regular exclusion radius remains UNEVALUATED. The named
explicit box is not thereby asserted inside it. The existential
sufficiently-small-epsilon intersection is valid separately. No old
accepted obstruction or ROC-extremality premise is reopened here.

## 6. Aligned cone and strongest predecessor reuse

I whole-read root's final ALIGNED_CONE. The endpoint
C=T²-2q²=Tr[(A^T A)²] is convex, since its Hessian is
2Tr(A^T H+H^T A)²+4Tr(A^T A H^T H)>=0. For any convex homogeneous
quartic its line second derivative is a nonnegative quadratic;
its discriminant gives Bregman>=C(H)/3. Here C(H)>=|H|⁴/2.
Consequently the initial chord r>=1/2+7|beta|/2 and its L4-only
modulus (1-|beta|)/6 are correct. The remaining q² term is QC by the
determinant null-Lagrangian identity and scalar Jensen, not an assumed
ordinary-heat dissipation law for q².

The stronger three-vertex envelope also checks. The already accepted
ROOT25 target has (beta,r)=(99/100,88/25) and L4 modulus 1/900000.
Affine interpolation with C and F* gives exactly

    U(b)=1/2+(302/99)b for b<=99/100,
    U(b)=48b-44          for 99/100<=b<=1.

The lower weight is lambda=100b/99 on the old target; the upper is
lambda=100(1-b) on it. The stated moduli add linearly and agree at the
middle vertex. Negative beta uses orthogonal sign transport. Extra
r adds a nonnegative determinant square. Thus all r>=U(|beta|) are QC.
The lower branch is admitted prior reuse; the new seed supplies the
high-beta segment and the endpoint, not a claim that the old target
had remained unresolved.

I also matched the old sol9 aligned-family definition. The direct
r=4 decomposition yields its stated stronger modulus
2/[3(m²+1)] on |Dphi|⁴. None of these arguments classifies the residual
curved ROC region or arbitrary nonlinear/nonpolynomial decompositions.

## Disposition and costs

The seed QC theorem and the stated root full35/envelope exports are
mathematically accepted at these scopes. The possible orientation
objection was independently resolved from the literal PLUS assertion;
it was not an actual certificate error or a changed primitive.

The independent code reads only literal JSON data and writes solely in
this review directory. No producer files were edited or imported, no
producer optimizer/source evolution was rerun, and no new scientific
grid was used. Discovery/search costs are B's separately retained costs,
not the 2.456-second verification figure. The prior ROC-extreme and
origin-regular exclusion results are retained at their accepted scope;
they are not newly validated by this scalar receiver. The separate
intrinsic-reduction note is outside this intake.
