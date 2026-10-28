# Independent constructive review of the calibrated70 theorem

Reviewed source: `../smooth_conic_interface/PROOF.md`, whole-read after the
definition and local exactness proof were saved. The exact conventions are
epsilon=1/100, kappa=1/20000000, e=epsilon-kappa, H=F-kappa q^2,
pH=p6-2kappa qT^2, sigma=1/34, D=(T+sigma)^2, f=H+eT. The frozen26/180
inputs concern the old PC/QC quartic, not the newer non-PC example.

**Core analytic theorem: ACCEPTED at this stated scope.** V is the globally
finite fixed70-SOS value in the source, V agrees with f on the entire
minors graph, and G=V+kappa|z|^2 agrees there with F+epsilon T. G is globally
2kappa-strongly convex and real analytic on an open neighborhood of the
entire graph. Smoothness elsewhere is not established. The support matrix
and off-axis characteristic receiver below are constructive independent
challenges, rather than treating an IFT invocation as a numerical oracle.

## Exact source stability and69-feature positivity

The correction from F to H is explicit in the old180 features:
R_H=R_F-kappa vv^T, where v represents T(cofA:X+q(X)). It has24 entries
equal to+/-1, hence ||v||^2=24. Thus R_H>=(13/10000000)I.

In26 features, B_(q^2)=L^2+2q(A)q(X), where L=cofA:X+q(X) has coefficient
vector norm squared6. The second polynomial has a Gram consisting of four
disjoint symmetric2 by2 blocks with eigenvalues+/-1. Its norm is1, so
the canonical correction has operator norm at most7. Therefore the same
C=33/400 works for H, with G26H>=(793/20000000)I. These quantitative
bounds independently strengthen the source's conservative row bound44.

At z0=m(B), t0=f(B), the cleared polynomial t0D-N is exactly the shifted
support polynomial with X=B-A. Its Gram is a sum of the R_H congruence,
sigma^2 G26H, four2sigma A_i^2 G26H congruences, and the three positive
diagonal residuals in source equation(2). Under A=B+U,X=-U they all vanish
at U=0. The feature span contains every degree1–4 monomial: X supplies
linears, X_iX_j quadratics, A_i X_jX_k (or A_iA_jX_k) cubics, and
A_iA_jX_kX_l quartics. Leading-degree triangularity proves rank69.
Positive source Grams and positive residual weights therefore prove a
POSITIVE DEFINITE69 Gram, with no SDP feasibility inference.

## Why the finite cone has the claimed local value

At graph contact, the negative A-Hessian of ell_A(m(B)) is

    M_B=D^2 f(B)-k(B)D^2q,

which is positive definite by the strict support. The ordinary implicit
function theorem gives a local stationary branch a(z) near B. It is real
analytic because ell is rational with D>0. Put t(z)=ell_(a(z))(z).
The centered polynomial D(a(z)+U)t(z)-N(a(z)+U,z) has no constant or
linear terms, exactly; differentiation of D introduces no residual because
both t-ell and its A-gradient vanish at contact.

The symmetric69-Gram map onto polynomials of degrees2–8 is surjective.
There is an especially simple quantitative right inverse: split each
monomial U^alpha into two nonconstant factors of degrees at most4, assign
its coefficient c to a diagonal Gram entry or c/2 to each symmetric
off-diagonal entry. Distinct monomials occupy disjoint pair groups. Hence

    ||right_inverse(p)||_2<=||right_inverse(p)||_(entry,l1)
                            <=||coeff(p)||_1.

The fixed right inverse therefore preserves the PD graph Gram whenever
the nearby centered coefficient error is sufficiently small. This proves
SOS feasibility at t(z). Evaluation at A=a(z), divided by positive D,
gives the reverse bound for EVERY feasible t. Thus V(z)=t(z) locally.
The PD Gram and its included linear features also give strict inequality
away from a(z), hence a unique GLOBAL CONTACT MAXIMIZER. This does not
assert uniqueness of every stationary point elsewhere in A-space.

## Global feasibility, closure and compensation

The epigraph feasibility condition is affine in(z,t), so convex. Each
graph value f(B) has its actual SOS certificate above. For arbitrary(B,s),
take rational Y=diag(1,s-det B) when the query is rational. The average of
m(B+Y),m(B-Y) is(B,s). Averaging their graph SOS certificates supplies a
finite feasible t. Evaluation at A=0 gives t>=ell_0=0. No noncompact
global Gram-padding theorem or infinite support oracle is needed.

Attainment does need closure of the fixed-degree SOS cone; it must not be
inferred from an arbitrary PSD-image closure assertion. A direct proof is
available: integrate each Gram polynomial on a fixed full-dimensional
compact box. The monomial moment matrix of that box is PD, so bounded
polynomial coefficients bound the trace of every PSD Gram representing
it. A convergent polynomial sequence therefore has a bounded Gram
subsequence and a PSD limit. The SOS cone is closed; minimizing t in its
closed nonempty lower-bounded affine slice attains the value.

On the graph f+kappa|m|^2=F+epsilon T exactly. Convexity of V plus the
quadratic compensation gives global2kappa strong convexity. At z=m(B), if
J=D_A(Df-k cofA,k), then

    D^2 V=J M_B^-1 J^T,
    D^2 G=J M_B^-1 J^T+2kappa I.

J has rank4 because J^T Dm=M_B. Thus V has local Hessian rank exactly4;
the compensation supplies the missing positive curvature. All statements
refer to the finite70-SOS value, not a convex envelope substituted for it.
Off graph, the inverse in this Hessian formula is instead
M(z)^-1=[-ell_(AA)(a(z),z)]^-1; it generally depends on the query. It
remains positive definite in the local neighborhood. J(a(z)) still has
rank4 because J(a)^T Dm(a)=D^2f(a)-k(a)D^2q is positive definite.

## Constructive nonzero-base receiver

At the rational off-axis base B=(1/3,-1/5,1/7,2/5), let r=grad k(B),
c=cofB, h=M_B^-1 r, and define

    n=(-h,1-c^T h).

Then J^T n=0 and n_s-c^T n_B=1. Hence B remains EXACTLY stationary for
every z(lambda)=m(B)+lambda n, with t(lambda)=f(B)+lambda j(B)^T n.
A quantitative69-Gram perturbation certifies a nonzero rational interval
of lambda. On that interval V is exactly affine and G exactly quadratic.
This is distinct from the source's small-origin open box and root's
origin normal strip. It uses no new SDP or numerical critical-point solve.
The receiver is now acquired: `receiver.py` proves a baseline69 Gram lower
bound7137/1150525184000, a certified two-sided lambda radius approximately
1.2076843197e-10, and evaluates lambda=1/10000000000 exactly. See
`RECEIVER_PROOF.md`, `RECEIVER.json` and both complete69 Gram files.
The code checks every polynomial coefficient, exact J^Tn=0, transversality,
and graph compensation. Parent independently whole-read the theorem spine
and receiver code and accepted their substance; this is not a separate
parent numerical replay of the69 matrices.

The updated source `PROOF.md` and `EXPLICIT_BOX.md` were also whole-read.
The explicit full5D box is ACCEPTED: independent direct weighted-binomial
coefficient bounds reproduce its exactrho=.4448325631397352 and Hessian
deviation2.662348473e-6<e. The coordinate cube/Euclidean ball distinction,
inward boundary root argument, square completion and both strict Slater
constructions check. `check_box_bounds.py` imports no producer evaluator
functions and does not rerun the two finite70 query certificates already
independently consumed by parent. Detailed scope is in `BOX_REVIEW.md`.

Finally, `conjugate_receiver.py` supplies an exact global Fenchel pair from
the nonzero contact point: w=j(B)+2kappa z, G*(w)=w:z-G(z), with exact
Fenchel gap0 and unique inverse gradG*(w)=z. This uses the supporting affine
jet and strong convexity directly, with no conjugate optimization or
numerical derivative. Standard convex duality receives its ordinary credit.

Ordinary parametric optimization, SOS Gram representations and IFT retain
their prior credit. Priority of this specialized fixed-degree composition
remains UNKNOWN. No global C-infinity claim outside the graph neighborhood,
physical model, practical speed advantage or civilisation-level result is
inferred from the theorem or receiver.
