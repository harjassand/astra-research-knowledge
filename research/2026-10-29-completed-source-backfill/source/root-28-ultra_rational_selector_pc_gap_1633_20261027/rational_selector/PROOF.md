# A polyconvex planar quartic with no polynomial global minor-support map

This is a complete internally constructed mathematical result. A separate
preserved peer is independently reviewing the new positive half and the
combined argument. The earlier polynomial-selector obstruction is already
independently accepted. World priority, a physical technology and a
civilisation-level operational breakthrough are separate claims, not made
here.

For A=[[a,b],[c,d]], put

    u=a²+c², v=b²+d², w=ab+cd, q=ad−bc,
    T=u+v=|A|², x=u−v, y=2w, z=2q.

The exact quartic is

    F=p0(u²+v²)+p2 uv+p3 w²+L q(u−v),

    p0=55220381/10000000000,
    p2=114430029/625000000,
    p3=−801761987/5000000000,
    L=118849817/4000000000.

**Theorem.** F has a finite real-valued convex lift in its five minors and
is uniformly strictly quasiconvex in the bound below. There is nevertheless
no polynomial global minor-affine support map of any degree, even if its
remainder is required merely to be nonnegative instead of SOS. Both
properties persist when every one of the 35 ordinary homogeneous quartic
coefficients is perturbed by at most 1/4928000000. These conclusions need
no symmetry assumption on a perturbed energy.

## 1. The acquired rational homogeneous support

Let B_F(A,X)=F(A+X)−F(A)−DF(A):X and define

    p6 = (6222019/200000000) x³
       +(1686519911/10000000000) x²z
       +(81172813/2000000000) xz²
       +(1726116771/10000000000) z³
       +(128626163/5000000000) xy²
       +(373321239/2000000000) y²z.

Set k(A)=p6(A)/T² for A≠0 and k(0)=0. The numerator is degree six in
matrix entries, so this selector is degree-two homogeneous and continuous
at zero. It is not assumed polynomial or differentiable at zero.

`EXACT_RATIONAL_SUPPORT.json` supplies the exact identity

    |A|⁴ B_F(A,X)−p6(A)detX = Z180(A,X)^T R Z180(A,X),   (1)

where Z180 consists of every A^alpha X_i with |alpha|=3, followed by
every A^alpha X^beta with |alpha|=|beta|=2. These are 80 and 100 features.
Entries of A and X are row-major, indexed0,1,2,3. In the first block,
enumerate index triples0≤i≤j≤k≤3 lexicographically, with the single X
index0,1,2,3 inside each triple. In the second block enumerate A index
pairs lexicographically, with X index pairs lexicographically inside each
A pair. Gram and dyadic-factor rows and columns use this exact order.
Products span all 3,185 possible monomials of bidegrees (A6,X2), (A5,X3)
and (A4,X4); 998 coefficients of this particular identity are nonzero.
The identity is reconstructed from literal differentiation of F, without
trusting a numerical coefficient residual.

The rational Gram has common denominator 80000000000 and satisfies

    R ≥ I/400000.                                        (2)

For clarity, its positivity proof is entirely exact. A floating Cholesky
only proposed a factor; that factor was rounded to a rational dyadic L
with denominator 2^44. Exact integer multiplication gives

    R = LL^T + I/200000 + E,
    ||E||2 ≤ max_i sum_j |E_ij|
       =4305014904500628945243/
        3022314549036572936765440000000000
       <1/400000.

Symmetry of E makes the displayed row-sum operator bound valid. Since
LL^T is PSD for any exact L, this proves (2) independently of the accuracy
or success status of the floating Cholesky or SDP. No unused matrix entries,
unmeasured eigenvalues or floating positivity premise enters (2).

Certificate SHA256:
`ecbd2bd7d333abe79810625c7be6e1d218d4411095cc28c049fa731958059191`.
The literal construction/positivity/full35 replay took 0.704 seconds.

## 2. Global support, including the zero base point

Let S_j(A)=sum_(|alpha|=j) A^(2alpha). The multinomial identity implies
S3(A)≥|A|⁶/6 and S2(A)≥|A|⁴/2. Hence

    |Z180(A,X)|²
       =S3(A)|X|²+S2(A)S2(X)
       ≥ |A|⁶|X|²/6+|A|⁴|X|⁴/4.

For A≠0, divide (1) and (2) by |A|⁴ to obtain

    B_F(A,X)−k(A)detX
       ≥ |A|²|X|²/2400000+|X|⁴/1600000.                  (3)

Because k is continuous at zero, the same assertion holds there by taking
A→0. In particular F(X)≥|X|⁴/1600000. The vanishing multiplier at A=0
is not cancelled there or treated as a positive denominator.

## 3. A finite convex lift and a compatible-gradient bound

For each base point A, define the affine function in five minor variables

    ell_A(B,s)=F(A)+(DF(A)−k(A)cofA):(B−A)
                         +k(A)(s−detA).

The planar determinant identity
det(A+X)=detA+cofA:X+detX and (3) imply ell_A(B,detB)≤F(B), with equality
at B=A. Therefore g(B,s)=sup_A ell_A(B,s) is convex and equals F on the
minors graph. It is finite everywhere: choose Y with detY=s−detB; then
(B,s) is the average of (B+Y,det(B+Y)) and (B−Y,det(B−Y)), and every
ell_A(B,s) is bounded above by [F(B+Y)+F(B−Y)]/2. A fixed ell_A also gives
a finite lower bound. Thus g:R5→R is a finite real-valued convex lift.

At any fixed affine background A, substitute X=Dphi into (3) and integrate.
The mean gradient and mean determinant of a zero-boundary or periodic
gradient vanish. The selector k(A) is fixed at that affine background;
no cancellation of a spatially varying selector is being assumed. Hence

    integral [F(A+Dphi)−F(A)]
       ≥ |A|²/2400000 integral |Dphi|²
                           +1/1600000 integral |Dphi|⁴.   (4)

The statement extends from smooth tests by strong W1,4 density on bounded
Lipschitz planar domains. It proves QC and the stated quantitative margin.

## 4. Why no polynomial support can do the same job

The separate exact source is
`../quartic_boundary_alternative/EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json`,
SHA256 `e51d9be90ba977c34f5daab4a75901eb6acc377dc53c0004d479425fed945d22`.
Its 24 actual rational evaluation points have strictly positive weights.
Their functional L satisfies

    L(A_i A_j detX)=0 for all ten i≤j,
    L(B_F)<−1/100000.

Root independently reconstructed these facts and the complete argument in
`../common_cone_review/ATOMIC_REVIEW.md`; no pseudo-moment positivity is
assumed. If a polynomial selector k had B_F−k detX≥0 globally, simultaneous
scaling (A,X)→(tA,tX) with either determinant sign would bound k(tA)/t² at
both t→0 and t→infinity. Every polynomial component except degree two
would vanish. The ten remaining quadratic directions are annihilated by L,
contradicting positivity on all 24 actual evaluations.

For a general polynomial minor-affine support map, touching at B=A forces
its entry component to DF(A)−k(A)cofA by differentiation. Its remainder
is exactly B_F−k detX, so that formulation is excluded as well. In
particular F is not SOS polyconvex under the polynomial-selector definition,
and no finite increment-norm SOS level with a polynomial selector repairs
it. The rational selector in (1) is the acquired escape from that class.

The target is now positively resolved as PC/QC and should be removed from
unresolved-QC candidate searches. This does not resolve the broader
six-parameter or nine-parameter ROC/QC cones or Morrey's problem.

## 5. An open gap in the full 35-dimensional coefficient space

For each ordinary homogeneous quartic monomial m(A), the coefficient l1
norm of |A|⁴ B_m(A,X) is exactly 176. Root checked all 35 identities.
Products of Z180 span all relevant monomials, so every coefficient
perturbation polynomial can be placed in a symmetric Gram correction:
use one diagonal entry or half the coefficient in each of a symmetric
off-diagonal pair. The correction operator norm is at most its entry l1
norm, hence at most 35*176*epsilon=6160 epsilon.

At epsilon=1/4928000000, the corrected Gram is at least I/800000.
The same rational selector therefore remains a valid global support for
every such perturbation, with (3)–(4) constants halved. For irrational
perturbed coefficients the Gram is real; exact rational reconstruction is
claimed only when its data are rational.

The accepted atomic obstruction already persists throughout the larger
full35 box of radius 1/336000000, so it persists on this smaller box too.
Every energy in the displayed neighborhood is PC/QC but has no polynomial
global minor-support selector. Exact target symmetries were useful for
acquisition, but are not hypotheses of this neighborhood theorem.

This also closes the original nearly symmetric target from the combined
search. Its difference from F is q|A|²/20000000000, which has exactly eight
ordinary quartic monomials, each of coefficient magnitude1/20000000000.
That is smaller than the proved full35 radius. Hence both the original
and exactly symmetric targets are PC/QC and have no polynomial global
minor-support map. Neither remains an unresolved-QC candidate.

## 6. Acquisition, comparison and limits

Polynomial-selector norm levels could never succeed here, as the exact
atomic theorem proves. Symmetry also makes degree-four numerators over
|A|² collapse to polynomial selectors. The degree-six numerator over
|A|⁴ was the first genuinely nonlinear rational interface for this target.
Its full 180-feature acquisition was implemented. An expensive unstructured
numerical control was terminated without a result, then replaced by an
exact ordinary-control construction. A bounded 60-second SCS target run
provided a positive suggestion. Rational affine projection, literal
coefficient matching and the exact dyadic residual turned that suggestion
into (1)–(2). The solver's optimal_inaccurate status itself proves nothing.

The general rational-selector/sphere-matrix completeness proof in the
peer's `RATIONAL_SELECTOR_COMPLETENESS.md` uses established compact
approximation and Scherer–Hol machinery. The acquired finite certificate
here does not establish a universal degree or efficient algorithm.
The primary comparison for SOS polyconvexity remains Fantuzzi et al.,
arXiv:2604.11124v1, Definition 2.5 and Remark 2.1. External priority has
not been established by the bounded literature search.
