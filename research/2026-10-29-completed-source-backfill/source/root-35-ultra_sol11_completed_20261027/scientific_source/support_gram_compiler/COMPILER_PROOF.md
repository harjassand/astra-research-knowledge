# Constructive support and leading Grams for the calibrated-jet operation

These are new enabling certificates for the old accepted PC/QC quartic F
and rational selector p6/T^2. They do not concern the newer ROC/non-PC
quartic. No source proof is rewritten. Global70-conic padding, value-function
evaluation, and calibrated-jet local exactness are separate worker tasks.

The literal input, in row-major A=(a,b,c,d), is

    u=a^2+c^2, v=b^2+d^2, w=ab+cd, q=ad-bc, T=u+v,
    F=p0(u^2+v^2)+p2 uv+p3 w^2+L q(u-v),
    p0=55220381/10000000000,
    p2=114430029/625000000,
    p3=-801761987/5000000000,
    L=118849817/4000000000.

p6 is exactly the six-term degree-six Hopf polynomial in the accepted
`sol8_opportunity_selection_20261027/rational_selector/PROOF.md`, reproduced
literally in both new scripts. B_F(A,X)=F(A+X)-F(A)-DF(A):X.

## 1. A small useful constructive support correction

Let Z26 consist of the16 features A_i X_j in row-major i,j order, followed
by the10 X_iX_j with0<=i<=j<=3 in lexicographic pair order.

**Exact theorem:** there is a rational symmetric Gram G26 such that

    B_F(A,X)+(33/400)T(A)|X|^2=Z26(A,X)^T G26 Z26(A,X),
    G26>I/25000.                                         (1)

The complete matrix is in `EXACT26_SUPPORT_GRAM.json`, with denominator
160000000000. Its26-feature identity was reconstructed from literal
differentiation of F. The independent consumer reconstructs B_F instead
by expanding every monomial F(A+X) with binomial coefficients and dropping
the X-degrees0 and1; the resulting exact coefficients agree.

A small26 by26 SDP was used ONLY to propose a Gram and C. It suggested
C approximately.08245831566, with status `optimal_inaccurate`. We rounded
UP to the convenient rational C=33/400=.0825, adjusted the16 AX diagonal
entries by that increase, rounded matrix entries to a rational grid, and
corrected the215 possible target monomials exactly. The largest affine
correction was only2 numerator units. No solver success, residual, floating
eigenvalue, or alleged optimum is a proof premise.

The delivered matrix originally had a conservative exact margin1/20000000.
The SAME matrix, without another solver call, was then proved strictly
above I/25000 by BOTH integer Bareiss Sylvester minors and a separate exact
Fraction LDL calculation. The weaker intermediate proof is retained in
the metadata. The current certificate and consumer use the stronger bound.
Optimality or minimality of C is not claimed.

A stronger useful corollary is free from the same matrix. Write
mu=1/25000. Since |Z26|^2=T|X|^2+S2(X), with
S2(X)=sum_(i<=j) X_i^2X_j^2, subtracting mu I from G26 and adding the
explicit SOS mu[S2(X)-|X|^4/2]=(mu/2)sum_i X_i^4 proves

    B_F+(4123/50000)T|X|^2-|X|^4/50000 is SOS.             (1a)

In particular F(X)-|X|^4/50000 is SOS by setting A=0. This is an algebraic
consequence of the delivered matrix, with no additional solver acquisition.
The convenient C=33/400 is retained below to keep sigma=1/33 simple.

## 2. The denominator shift is now jointly SOS with useful sigma

Let R(A,X)=T^2 B_F(A,X)-p6(A)q(X), the accepted R180 SOS certificate.
For epsilon>0, sigma>0 put D_sigma=(T+sigma)^2. Then EXACTLY

    D_sigma B_F-p6 q(X)+epsilon D_sigma|X|^2
      =R+(2sigma T+sigma^2)[B_F+C T|X|^2]
       +[(epsilon-2C sigma)T^2
             +sigma(2epsilon-C sigma)T+epsilon sigma^2]|X|^2.   (2)

Every term on the right is SOS whenever

    0<sigma<=epsilon/(2C)=200epsilon/33.                  (3)

This is a joint polynomial SOS in A,X; division by D_sigma at a FIXED A
therefore gives a valid increment SOS support for the shifted selector
k_sigma=p6/(T+sigma)^2. Positive scalar division at fixed A is explicit.
The zero base point needs no cancellation by T because D_sigma>0 there.

More strongly, subtract(epsilon/2)D_sigma|X|^2 from the left side of(2).
The same decomposition has residual coefficients

    epsilon/2-2C sigma,
    sigma(epsilon-C sigma),
    (epsilon/2)sigma^2.

They are nonnegative for

    0<sigma<=epsilon/(4C)=100epsilon/33.                  (4)

Thus the shifted selector retains an ACTUAL uniform epsilon/2 quadratic
SOS margin. This avoids the much smaller coefficient-l1 smoothing scale;
it is stronger information than a nonnegative scalar support inequality.

For the concrete epsilon=1/100, the boundary choice sigma=2/33 gives the
nonnegative support identity. The interior choice sigma=1/33 gives the
uniform epsilon/2 margin; after that margin is removed, the remaining
coefficients of(T^2,T,1)|X|^2 are exactly

    (0,1/4400,1/217800).

The consumer checks BOTH versions of(2), including all polynomial
coefficients and these exact rational parameters. No Hessian grid enters.

In fact BOTH original strict margins also survive at the larger scale(4).
Put gamma=1/400000 and mu=1/25000. In the SOS order the accepted and new
Gram bounds give

    R >=_SOS gamma[S3(A)|X|^2+S2(A)S2(X)],
    S26:=B_F+C T|X|^2 >=_SOS mu[T|X|^2+S2(X)].

Use S3(A)>=_SOS T^3/6 and S2(A)>=_SOS T^2/2. The two resulting coefficients
are gamma*T^2/6+mu(2sigmaT+sigma^2), multiplying T|X|^2, and
gamma*T^2/2+mu(2sigmaT+sigma^2), multiplying S2(X). Since mu>=gamma/2,
they dominate gamma*D_sigma/6 and gamma*D_sigma/2 respectively. Finally
S2(X)>=_SOS |X|^4/2. Thus, for ALL sigma satisfying(4),

    D_sigma[B_F+epsilon|X|^2-k_sigma q(X)
       -(epsilon/2+T/2400000)|X|^2-|X|^4/1600000] is SOS.  (4a)

This is a quantitative strong joint-SOS support theorem, rather than a
pointwise Hessian lower bound. The full constructive decomposition can be
read explicitly by writing f=2sigmaT+sigma^2, D=D_sigma,
R0=R-gamma[S3(A)|X|^2+S2(A)S2(X)],
S0=S26-mu[T|X|^2+S2(X)], and
h=(epsilon/2-2C sigma)T^2+sigma(epsilon-C sigma)T
+(epsilon/2)sigma^2. The polynomial in(4a) equals

    R0+gamma[S3(A)-T^3/6]|X|^2
      +gamma[S2(A)-T^2/2]S2(X)+f S0
      +(mu-gamma/6)f T|X|^2+(mu-gamma/2)f S2(X)
      +(gamma/2)D[S2(X)-|X|^4/2]+h|X|^2.

Each displayed term is SOS with nonnegative rational coefficients for the
declared parameters. The independent consumer reconstructs this complete
identity coefficient by coefficient, including its diagonal SOS differences.

## 3. A positive-definite35 Gram directly from the accepted180 Gram

The accepted identity is

    R(A,X)=Z180(A,X)^T R180 Z180(A,X),
    R180>=gamma I, gamma=1/400000.

Its features are the80 A^alpha X_j with |alpha|=3, followed by the100
A^alpha X^beta with |alpha|=|beta|=2, in the original exact order. Set
X=-A. Euler's homogeneous quartic identity and q(-A)=q(A) give

    R(A,-A)=3T(A)^2 F(A)-p6(A)q(A)=:P8(A).                (5)

Let Z4 contain all35 ordinary quartic monomials in A. Every substituted
feature is PLUS or MINUS exactly one member of Z4, so there is an explicit
180 by35 signed0/1 matrix M with Z180(A,-A)=M Z4(A). Consequently

    G35=M^T R180 M,
    P8=Z4^T G35 Z4.                                     (6)

All35 monomials occur. Because each row of M has exactly one nonzero
entry, M^TM is diagonal. Its multiplicities for exponent patterns
(4),(3,1),(2,2),(2,1,1),(1,1,1,1) are respectively

    2,4,5,7,10.

It follows constructively that

    G35>=gamma M^TM>=I/200000.                           (7)

`EXACT35_LEADING_GRAM.json` contains M, all multiplicities, the resulting
35 by35 rational Gram (denominator80000000000) and its basis. The scripts
reconstruct every coefficient of P8 literally. Both integer Bareiss and
independent Fraction LDL also verify G35-I/200000 is strictly positive
definite, so positivity of this delivered matrix can be checked directly
without assuming any unexamined floating part of the old certificate.

There is a useful stronger scalar leading floor. In the expansion of T^4,
the respective multinomial coefficients are1,4,6,12,24. The minimum ratio
of multiplicity to multinomial coefficient is10/24=5/12. Therefore

    P8-T^4/960000 is SOS.                               (8)

For the actual delivered Gram the consumer additionally proves a POSITIVE
DEFINITE Gram for(8): subtract from G35 the diagonal Gram with entries
binom(4,alpha)/960000. No new SDP or scalar polynomial fit is needed.

## 4. General constructive compiler lemma

The first construction does not require the target's symmetry or ROC.
Let F be ANY rational homogeneous quartic in n variables with a GIVEN
rational positive-definite Gram G_F in the full n(n+1)/2 quadratic-monomial
basis, and a supplied rational bound G_F>=gI, g>0.

Use features consisting of all n^2 A_iX_j and all n(n+1)/2 X_iX_j.
The bidegree(A2,X2) terms of B_F have a rational symmetric Gram H in the
first block. Every bidegree(A1,X3) monomial is a product of a first-block
feature and a second-block feature, so it has a rational cross block J.
The bidegree(A0,X4) block is the supplied G_F. Thus exactly

    B_F=Z^T [[H,J],[J^T,G_F]] Z.

Adding C|A|^2|X|^2 adds C I to the first block. Define rational bounds

    h=max_i sum_j |H_ij|,
    j2=sum_ij J_ij^2.

The Schur complement is positive definite for any rational

    C>h+j2/g,                                         (9)

because ||H||2<=h and J G_F^-1 J^T<=(j2/g)I. This is an actual finite
rational algorithm, not an unevaluated search. It explicitly charges the
supplied Gram and conditioning bound g; it does not assume that mere
coercivity or positivity implies an interior SOS Gram. The small SDP in
this target improves that generic loose C to the useful33/400, and the
result is then certified exactly.

For any planar homogeneous quartic and degree-six p6 with the same full
R180 feature certificate and bound R180>=gamma I, the X=-A compiler
likewise always yields G35>=2gamma I and the SOS floor
P8>=(5gamma/12)T^4. These follow from the fixed feature map, independently
of the target coefficients. Strict PD of the residual floor requires the
corresponding strict Gram slack or a separate check, as supplied here.

These elementary Gram/Schur and substitution tools are not claimed as
new general SOS algorithms. The consequential new interface here is the
literal small-C certificate, the direct leading Gram and the usable shifted
SOS scale for the actual calibrated-jet construction.

## 5. Acquisition, independent replay, and scope

`acquire_compiler_grams.py` contains all literal definitions and basis
orders, the sole small SDP proposal, exact affine correction, Bareiss
proof and direct180-to35 extraction. The26-feature setup took0.018201s,
the CLARABEL solve0.107277s (9 iterations), and its first exact Bareiss
proof0.000802s. The35-feature extraction and literal proof took0.029589s,
including0.004666s in its Bareiss calculation. Scientific imports, literal
symbolic construction, the small SDP and both certificate constructions
together took0.956390s from the module timer. Interpreter startup and the
initial stdlib imports before that timer are excluded and not silently
claimed as free in an efficiency comparison. There is no such advantage
claim. The old180 certificate is an accepted, charged prior input; its
historical acquisition costs remain in its original files.

The separate `verify_grams_independently.py` imports no producer code,
solver, NumPy or SymPy. It uses binomial literal translation, Fraction
polynomials and Fraction LDL, independently rebuilding both identities,
the signed congruence, the stronger leading floor, and both shifted-support
algebras. Its first replay took0.136401s; after strengthening the SAME Gram
margin and adding the strong-shift identity, its second replay took0.146487s.
A third replay after adding the full preserved-margin decomposition took
0.141286s. All three are charged. The extra exact margin proofs took
0.007020s without another solver call. The sum of these measured numerical
phases and the original module run is1.387584s. Source reading, writing this
proof and interpreter startup are not folded into a claimed end-to-end
speed result. Complete measured phases and intermediate scope are
preserved in `ACQUISITION.json` and `INDEPENDENT_COMPILER_REPLAY.json`.

This is independent-code-path verification within one worker, not yet a
separate peer acceptance. Global fixed70-SOS feasibility, smooth local
exactness of its value, practical solver conditioning, and ordinary-method
advantage remain outside these certificate claims. No physical, paid,
public, Capital, goal, automation, protected-chat or new-worker action ran.
