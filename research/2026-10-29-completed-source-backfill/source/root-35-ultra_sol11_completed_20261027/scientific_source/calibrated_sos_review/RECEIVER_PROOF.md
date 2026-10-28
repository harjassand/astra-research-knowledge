# Exact characteristic and conjugate receivers at a nonzero graph base

The reviewed fixed70-SOS primitive and frozen constants are those in
`REVIEW.md`. This receiver uses B=(1/3,-1/5,1/7,2/5), with q(B)=17/105,
well outside the source evaluator's small origin box. It supplies an exact
family of off-graph values and a corresponding exact Fenchel pair. No SDP,
Newton iteration, numerical critical-point solve or derivative fit runs.

## The characteristic direction is rational and exactly stationary

Let f=H+eT, k=pH/(T+sigma)^2 and define the jet gradient
j(A)=(Df(A)-k(A)cofA,k(A)). At the selected B put

    M=D^2f(B)-k(B)D^2q, r=grad k(B), c=cofB, h=M^-1 r,
    n=(-h,1-c^T h), z0=m(B).

M is positive definite; the code also checks this with exact rational LDL.
All quantities are rational. The Jacobian of j at B is

    J=[M-c r^T; r^T].

Direct multiplication gives J^T n=0 and n_s-c^T n_B=1. Since ell_A is
affine in z, B is EXACTLY stationary for every point

    z(lambda)=z0+lambda n,
    t(lambda)=f(B)+lambda j(B)^T n.                        (1)

There is no nonlinear equation hidden in this receiver. M is a supplied
explicit4 by4 rational matrix and its inverse is computed exactly.
The normal direction and scalar slope are in `RECEIVER.json`.

## A quantitatively positive69 graph Gram

`receiver.py` constructs the base Gram directly from the frozen input
Grams. The old180 Gram loses the rank-one square T(cofA:X+q(X)), whose
feature coefficient norm squared is24; its remaining margin is

    gamma_H=13/10000000.

The26 correction for B_(q^2) is a rank-one square with coefficient norm
squared6 plus four disjoint symmetric2 by2 blocks of norm1. Its total
operator norm is at most7. Thus the H-support26 Gram has margin

    mu_H=793/20000000.

The shifted-support decomposition from the reviewed theorem is evaluated
at A=B+U,X=-U. Every feature is expanded exactly as a polynomial in U.
Integer congruences combine R_H, sigma^2 G26H, the four2sigma A_i^2 G26H
copies and the positive diagonal residuals. The resulting69 by69 Gram Q0
is saved in `BASE69_GRAM.json`. Its polynomial is checked coefficient by
coefficient against the independently formed literal D(A)f(B)-N(A,m(B)).

A quantitative PD bound does not rely on a floating eigenvalue. Select
69 rows of the source features, ordered by degree:

- U_i, all four linears;
- U_iU_j, all ten quadratics;
- (B_i+U_i)U_jU_k, one leading representative for each of20 cubics;
- (B_i+U_i)(B_j+U_j)U_kU_l, one representative for each of35 quartics.

The selected coefficient matrix K in the standard centered monomial basis
is unit lower triangular. These rows have Gram weights at least

    m0=min(e sigma^2,mu_H sigma^2,2sigma mu_H,gamma_H)
      =793/23120000000.

The exact inverse has

    ||K^-1||_1=31102/11025, ||K^-1||_infinity=49/25.

Consequently

    Q0>=m I,    m=7137/1150525184000.                     (2)

The code reconstructs K and its inverse and verifies their product exactly.
The lower bound follows from Q0>=m0 K^T K and the standard matrix-norm
bound. Every input and conditioning factor is explicit.

## Exact polynomial correction gives a nonzero interval

With U=A-B, the cleared contact polynomial at(1) is affine in lambda:

    P_lambda(U)=P0(U)+lambda P1(U).

P1 has zero constant and linear coefficients, because value and stationarity
remain exact at B. It has degree at most8. The code constructs it from the
literal D,N definition and checks those zero coefficients directly.

For each monomial U^alpha of degree2–8, choose two nonconstant degree<=4
factors. A diagonal Gram entry gets its coefficient, or two symmetric
off-diagonal entries get half. This is a fixed finite right inverse of the
69-Gram coefficient map. Distinct monomials have disjoint pair groups, so
the resulting Q1 satisfies

    ||Q1||_2<=||Q1||_(entry,l1)<=L=||coeff(P1)||_1.

`DELTA69_GRAM.json` contains Q1 and its exact rational L. The identity
v69^T Q1 v69=P1 is checked for every coefficient. Define

    rho=min(m/(2L),1/[2(1+|q(n_B)|)],1).

For every |lambda|<=rho, Q0+lambda Q1>=m I/2. Thus P_lambda is globally
SOS in A. Evaluation at A=B proves the matching dual bound t>=ell_B(z).
We have therefore acquired EXACTLY

    V(z0+lambda n)=f(B)+lambda j(B)^T n,
    G(z0+lambda n)=V(z0+lambda n)+kappa|z0+lambda n|^2.      (3)

The certified radius has display rho approximately1.2076843197e-10; its
full rational is in JSON. The chosen rational lambda=1/10000000000 is
inside it. Its query is off graph since

    s(lambda)-q(B+lambda n_B)=lambda-lambda^2 q(n_B),

whose absolute value is at least |lambda|/2 for lambda!=0 in this segment.
The executed gap is approximately9.999999999624596e-11. The exact
compensated value has display

    G approximately0.008103535145998592.

Exact rationals, not these rounded displays, are the certificate. This is
a quantitative receiver of an entire-graph local theorem at a substantial
nonzero base. It does not claim an explicit full5D neighborhood there.
The separate source box provides that kind of domain around the origin.

## A global Fenchel pair and exact inverse at the constructed input

Dirac evaluation at B gives the GLOBAL affine lower support ell_B for V.
At the certified point it touches, so j(B) belongs to the subgradient of V.
Put

    w=j(B)+2kappa z(lambda).

Then w belongs to the subgradient of G at z(lambda). Global2kappa strong
convexity makes z(lambda) the UNIQUE conjugate maximizer, hence

    G*(w)=w:z(lambda)-G(z(lambda))
         =kappa|z(lambda)|^2-f(B)+j(B):m(B),
    grad G*(w)=z(lambda).                                (4)

`conjugate_receiver.py` is a separate stdlib-only Fraction evaluation of
this pair. It reconstructs the jet from the literal quartic, not a numerical
gradient. It obtains exact Fenchel gap0 and the display

    w approximately(.01590785805,-.004881923426,.006962965860,
                                            .01000603420,.04480296874),
    G*(w) approximately.010426405965219815.

All exact entries are in `CONJUGATE_RECEIVER.json`. This is a constructed
one-parameter family of exact inverse inputs, not an implemented solver
for arbitrary entropy-variable queries. Standard convex duality retains
its prior credit. Since G>=kappa|z|^2 and is globally strongly convex, G*
is finite and C1 globally with gradient Lipschitz constant1/(2kappa)=10^7;
that ordinary regularity statement supplies no generic computational rate.

## Cost, acceptance, and limits

The receiver run took0.746241s, including scientific imports, literal input,
symbolic exact derivatives, source reading,69 congruences, all polynomial
identities, triangular inverse bound and the rational point. The standalone
conjugate Fraction receiver took0.006405s. Interpreter startup/initial
stdlib imports before the timers are excluded; no efficiency advantage is
claimed. R180 and26/35 acquisition remain charged prior inputs. No new
26 or70 SDP ran. Peak memory and global arbitrary-query solver cost were
not measured.

Parent whole-read `REVIEW.md` and the complete receiver code and accepted
the construction in substance: feature congruence, K bound, right inverse,
stationarity/transversality and matching contact dual. This is a substantive
independent code/proof review, not a second parent numerical replay of the
69 matrices. Our own exact execution and that review have those distinct
scopes. No priority, global off-neighborhood smoothness, physical entropy
device, general performance advantage or mission-completion claim is made.
