# Audit: local rate admission, unknown stationary law, and rare means

Parent `/root` owns the rate-admission construction and synthesis. This
note independently checks its algebra, supplies a symmetric flow-error
sharpening, and records an ordinary hypercontractive improvement. It is
not a claim that these ingredients, or their conjunction, are historically
new. Prior Astra premises remain pinned to revision
51ce47ce39f976517d60e2f87bbe280b651f6056.

## 1. Contract and finite-time positive comparison

Let Q0 be an irreducible finite-state generator, with invariant law pi0,
additive symmetric-part gap at least g>0, and exit rates at most Lambda.
Let Q be any generator on the same allowed off-diagonal support satisfying

    (1-eta) q0(x,y) <= q(x,y) <= (1+eta) q0(x,y),  0<=eta<1.

No stationarity, Gibbs representation, cycle decomposition, or reversibility
of Q is assumed. Finite-state irreducibility follows from shared support.
The support and local contexts must be supplied structural information;
finite passive data alone cannot exclude arbitrary hidden transitions or
global-state dependence.

Entrywise comparison of Metzler generators gives

    (1-eta)Q0-2eta Lambda I <= Q <= (1+eta)Q0+2eta Lambda I.

Therefore, by positivity of matrix exponentials,

    exp(-2eta Lambda t) P0((1-eta)t)
       <= P(t) <=
    exp(2eta Lambda t) P0((1+eta)t).                 (1)

The factor2 is sufficient: the diagonal difference between Q and
(1-eta)Q0 can be as negative as -2eta times the reference exit rate.

Suppose the reference admits a certified relative mixing time r_beta:

    |P0(s;x,y)/pi0(y)-1| <= beta  for all s>=r_beta,  0<beta<1.

It suffices to establish this at r_beta, since subsequent Markov averaging
preserves both entrywise bounds. Set

    t_beta = r_beta/(1-eta),
    u = 2eta Lambda t_beta - log(1-beta).

Multiplying (1) by the unknown invariant row law pi and summing over the
initial state proves the pointwise stationary certificate

    exp(-u) pi0(x) <= pi(x) <= exp(u) pi0(x).         (2)

The upper bound uses log(1+beta)<=-log(1-beta). This step requires no
computation or sampling from the true pi. A gap-only reference certificate
is r_beta=log[1/(beta pi0_min)]/g. Section4 greatly improves it for the cube.

## 2. All-target mean comparison by balanced flows

Use L=-Q, D=diag(pi)L and D0=diag(pi0)L0. Both D and D0 have zero row
and column sums. Their off-diagonal positive flows are

    F(x,y)=pi(x)q(x,y), F0(x,y)=pi0(x)q0(x,y).

From the rate box and (2), the flow ratio lies in exp(+/-v), with

    v=u-log(1-eta).

For every positive a,b with a/b in exp(+/-v),

    |a-b| <= 2sinh(v/2) sqrt(ab).

Let E0(f)=f^T D0 f and E(f)=f^T D f. Balanced-flow identities give
E(f)=0.5 sum_xy F(x,y)(f(x)-f(y))^2, including nonreversible D.
For the bilinear difference, center f in pi0; column balance makes this
centering leave f^T(D-D0)h unchanged. Edgewise Cauchy--Schwarz yields

    |f^T(D-D0)h|
      <= 2sinh(v/2)
           sqrt(sum_xy F0(x,y) f(x)^2)
           sqrt(sum_xy F(x,y)(h(x)-h(y))^2)
      <= kappa sqrt(E0(f) E(h)),

    kappa=2sqrt(2Lambda/g) sinh(v/2).                (3)

This mixed-energy estimate avoids an artificial requirement that a
one-sided relative flow error be less than1.

Here is the scalar comparison behind its use. Fix any probability weight
w with full support and any proper nonempty target A; put B=A^c. A
balanced irreducible D defines a generator -diag(w)^(-1)D with invariant w.
Its stationary-conditional mean hitting time is

    M(w,D) = [w_B^T D_B^(-1) w_B]/w(B).             (4)

The killed inverse D_B^(-1) is entrywise nonnegative. Define
mu=w_B^T D_B^(-1)w_B and C=1/mu. Extending t=D_B^(-1)w_B by0 on A,
the equilibrium h=1-t/mu satisfies h|A=1, w(h)=0,

    z^T D h=0 for every z|A=0, w(z)=0,
    h^T D h=C.

The adjoint equilibrium h* has the analogous properties. Taking
w=pi0 for both D0 and D, their capacities satisfy the exact identity

    C-C0 = (h0*)^T(D-D0)h.

Indeed h0*-h and h-h0 lie in the common homogeneous constraint space,
so the forward and adjoint weak equations remove the cross terms.
Equation(3) now gives |C-C0|<=kappa sqrt(C C0). Consequently both the
capacity ratio and its inverse are at most

    F_miss = exp{2asinh[sqrt(2Lambda/g) sinh(v/2)]}.  (5)

The mean ratio at the fixed weight pi0 has the same two-sided factor.
To change the weight from pi0 to the actual pi while holding D fixed,
apply the positive inverse formula(4). Its numerator changes by at most
exp(+/-2u), and its denominator by at most exp(+/-u). Thus, simultaneously
for every proper nonempty target A,

    exp(-3u)/F_miss <= M(pi,D)/M(pi0,D0)
                         <= exp(3u) F_miss.          (6)

Since g<=2Lambda, a=sqrt(2Lambda/g)>=1. The elementary inequality
asinh(a sinh z)<=az for z>=0 gives the simpler sufficient log bound

    |log[M/M0]| <= 3u+sqrt(2Lambda/g)v.              (7)

### Rare-target sharpening

The weight step before bounding its denominator is sharper:

    exp(-2u) b0/b <= M(pi,D)/M(pi0,D)
                       <= exp(2u) b0/b,

where p0=pi0(A), b0=1-p0, and b=pi(B). If exp(u)p0<1, define

    b_min=1-exp(u)p0, b_max=1-exp(-u)p0.

Then

    exp(-2u)b0/[b_max F_miss] <= M/M0
                    <= exp(2u)b0 F_miss/b_min.       (8)

For a rare target this saves almost u in the log error. Formula(6)
remains simpler and applies without checking exp(u)p0<1.

## 3. The actual gap and passive completion are also earned

The true energy satisfies E>= (1-eta)exp(-u) E0. Also
Var_pi(f)<=exp(u)Var_pi0(f), by minimizing over constants. Hence

    g_actual >= (1-eta)exp(-2u)g.                    (9)

Likewise pi_min>=exp(-u)pi0_min, and every local context has actual
stationary mass at least exp(-u) times its reference mass. Thus the
fixed-exposure passive confidence scheme in PASSIVE_BASELINE.md is valid
without knowing pi, and this admitted near-reference class has an explicit
completion-time bound. Confidence validity and completion complexity must
not be conflated: the martingale confidence set is valid even for a source
that fails admission; completion is guaranteed for sources in the stated
structural and quantitative class.

The mean bound can feed the parent's nonreversible screened-lifetime
certificate. With an actual mean interval[M_-,M_+], actual gap lower bound
g_-, and actual target-mass upper bound p_+<1, set

    delta_+=1/[g_-(1-p_+)M_-].

When delta_+<=1/4, the previously proved lifetime error D(delta) applies.
For conditional initial law pi(.|B), comparison with Exp(mean M) costs at
most [D(delta_+)+p_+]/(1-p_+)+p_+. Therefore the deadline CDF is enclosed
using 1-exp(-t/M_+) and 1-exp(-t/M_-) plus this additive error. There is no
pathwise error factor proportional to the possibly exponential mean M.

## 4. Hypercontractivity with arbitrary invariant driven channels

For the concrete uniform cube Omega={0,1}^n, n>=2, suppose

    Q0=H+K,
    H f(x)=c sum_i [f(x^i)-f(x)], c>0,

and K itself is a Markov generator preserving uniform pi0. Arbitrary
noncommuting directed channels are permitted if their aggregate K is
Markov and pi0-preserving. The same conditions hold for K*, because the
stationary adjoint of a Markov generator is Markov.

The ordinary cube hypercontractive inequality is

    ||exp(tH)||_(p->q) <=1,
    q-1=(p-1)exp(4ct), p>1.                         (10)

Normalization check: on one bit the positive projection B=I-Pi has
eigenvalues0,1. The negative generator is -H=2cB. Gross1975 Theorem3
gives q-1=(p-1)exp(2s) for exp(-sB), so s=2ct gives(10).
Tensorization gives the same exponent independently of n. Equivalently
Ent(f^2)<=E_H(f)/c=(2/rho)E_H(f), with rho=2c.

Jensen's inequality and invariance show that exp(tK) contracts every
Lp(pi0),1<=p<=infinity. Fix m and d=t/m. In the Trotter product

    [exp(dH)exp(dK)]^m,

apply exp(dK) at the current exponent p_j and exp(dH) from p_j to
p_(j+1), where p_j-1=(p-1)exp(4cjd). Every factor has norm<=1 between
the designated spaces. The finite-dimensional Trotter limit therefore
proves(10) for P0(t)=exp(tQ0). Apply the same argument to H+K* to prove
it for P0(t)*. No reversibility of Q0 is used.

Set

    t0=log(n-1)/(4c).

Then P0(t0) maps L2 to Ln with norm<=1. Finite uniform-space embedding
has ||f||infinity<=2^(n/n)||f||n=2||f||n, so

    ||P0(t0)||_(2->infinity)<=2.

Adjoint hypercontractivity and duality give

    ||P0(t0)||_(1->2)<=2.

The symmetric-part gap of Q0 is at least2c because K has nonnegative
Dirichlet energy. Hence ||P0(tau)-Pi||_(2->2)<=exp(-2c tau). Factor

    P0(2t0+tau)-Pi=P0(t0)[P0(tau)-Pi]P0(t0)

to obtain

    ||P0(2t0+tau)-Pi||_(1->infinity)<=4exp(-2c tau).

For any signed matrix R acting on Lp(pi0),

    ||R||_(1->infinity)=max_(x,y) |R(x,y)|/pi0(y).

The upper bound follows by the triangle inequality, and a signed unit
point mass f=+/-1_y/pi0(y) attains the maximizing entry. Thus the bound
is valid for the signed kernel P0-Pi, not just positive kernels.
Choosing tau=log(4/beta)/(2c) gives the simple certified relative horizon

    r_beta=log[4(n-1)/beta]/(2c).                   (11)

Its dimension dependence is log n. In the actual-source sandwich use
t_beta=r_beta/(1-eta), as in Section1. This is an application of ordinary
hypercontractivity and Trotter theory; it should be credited accordingly.

For a general finite pi0 and a hypercontractive floor with exponent2rho,
one may instead choose q*=max{2,log(1/pi0_min)},
t0=log(q*-1)/(2rho). Then both endpoint operator norms are<=e, yielding
r_beta=log(q*-1)/rho+[2+log(1/beta)]/g. The cube choice q=n replaces e
by2 and has a simpler exact formula.

## 5. Comparison boundaries

The strongest ordinary passive CTMC likelihood already learns the local
rate table in this model from unmarked timestamped trajectories; a naive
reversible rate-ratio failure is not an inference impossibility.

Ordinary known-model potential theory, splitting, and positive short
excursions already supply rare-event tools. The proposed incremental
operation is the explicit bridge from a simultaneous local rate confidence
box to all-target relative mean and lifetime conclusions for an actual
source whose stationary law is unknown and need not equal the reference.

This note does not establish historical priority. Thiede--Van Koten--Weare
2015 gives sharp stationary relative-perturbation bounds and explicitly
allows analytical bounds from a simple dominated reference. Its generic
O(|Omega|^3) evaluation cost is not an unconditional exponential lower bound
for compact chains. Its raw edge-sum bound using only Q_xy(S)>=S_xy is
pessimistic here, but a better analytical evaluation must remain an open
comparator. Solan--Vieille2003, Hunter's perturbation formulas, nonreversible
variational capacity theory, and uniformly ergodic perturbation bounds are
also serious comparators. Do not claim that all prior perturbation bounds
accumulate error linearly to time M: many are uniform over infinite time.

## 6. Ordinary stationary-resolvent refinement

This section independently audits the parent's refinement. It replaces the
small-beta mixing sandwich when a useful deviation-operator estimate is
available. No historical novelty is claimed for stationary perturbation
identities, Neumann-series arguments, or integration of mixing envelopes.

Let W0=diag(pi0), E=Q-Q0, and use the stationary reference adjoint

    E*=W0^(-1) E^T W0, Q0*=W0^(-1) Q0^T W0.

The actual density h=pi/pi0 obeys pi0(h)=1 and

    (Q0*+E*)h=0.

The reference deviation operator is

    R0*=integral_0^infinity [P0*(t)-Pi0] dt.

On the pi0-mean-zero subspace, it is the inverse of L0*=-Q0*. Since
E1=0, pi0(E*f)=0 for every f. Since Q0*1=0, stationarity therefore gives
the exact identity

    h-1=R0* E*h.                                  (12)

This is a finite-state Poisson equation; no true stationary samples,
unknown inverse, or actual-source mixing constant is inserted as an input.
Only a bound on the reference inverse will be used.

The relative rate box gives a useful absolute-row bound on E*. For each x,

    sum_y |E*(x,y)|
      <= eta q0_out(x)
         + eta sum_(y!=x) pi0(y)q0(y,x)/pi0(x)
      = 2eta q0_out(x) <= 2eta Lambda.              (13)

The equality is reference stationary flow balance. It does not require
reversibility or uniform pi0. The diagonal E*(x,x)=E(x,x) contributes at
most eta q0_out(x); the other term is the weighted incoming flow sum.

Let T_infinity bound the L-infinity norm of R0* on the pi0-mean-zero
subspace, and put a=2eta Lambda T_infinity. With z=||h-1||infinity,
(12)--(13) give z<=a(1+z). Thus, if a<1/2,

    z <= a/(1-a) <1,
    u_res=log[(1-a)/(1-2a)]                         (14)

is a valid symmetric log-density certificate exp(-u_res)<=h<=exp(u_res).
The upper density bound follows because 1+z<=1/(1-z). The condition
a<1/2 is sufficient for the positive lower bound; the algebraic bootstrap
only requires a<1. Use the minimum of u_res and every independently valid
Metzler bound from Section1.

### Acquired imbalance or forcing

If an acquired bound d satisfies ||E*1||infinity<=d, splitting h=1+f in
(12) gives

    f=R0*E*1+R0*E*f,
    z <= T_infinity d/(1-a),                       (15)

provided a<1. Whenever this z<1, u=-log(1-z) is valid. More generally,
replace T_infinity d by any earned bound b_forcing on ||R0*E*1||infinity.
If E*1=0 is established exactly, pi0 is invariant for Q and uniqueness
gives h=1 without a smallness assumption.

For supplied finite-range kinetic contexts, d can be earned from the local
rate confidence intervals. Under uniform pi0 the imbalance is

    E*1(x)=sum_y [E(y,x)-E(x,y)].

It is a sum of local functions. A safe interval bound combines each rate
cell's incoming and outgoing coefficients before taking interval extrema.
For path contexts of bounded range, maximizing the resulting local
potential over x uses ordinary finite-width dynamic programming. A local
Gibbs reference also permits this operation because pi0(y)/pi0(x) for a
local move depends only on the factors touching that move. This procedure
requires the supplied kinetic-context structure; finite observations
alone do not establish it. A triangle sum over all local interval widths
is a looser but immediately valid alternative.

### One smoothing is sufficient for the inverse norm

In the cube setting of Section4, P0*(t0) has 2-to-infinity norm at most2,
with t0=log(n-1)/(4c). On the mean-zero subspace, for t>=t0,

    ||P0*(t)f||infinity
      <=2 exp[-2c(t-t0)] ||f||2
      <=2 exp[-2c(t-t0)] ||f||infinity.

For every t>=0, Markov contraction also gives norm at most1. The two
bounds cross at

    t_star=t0+log(2)/(2c)=log[4(n-1)]/(4c).

Integrating the resulting envelope proves

    T_infinity <= [log(4(n-1))+2]/(4c).             (16)

The cap1 here is the norm of P0* restricted to mean-zero functions. The
unrestricted norm of P0*-Pi0 can be2, so replacing it by1 without the
restriction would be an error. Both arguments in (12) and (15) are
mean-zero, as shown above, so the restricted bound is sufficient.

The earlier two-smoothing argument also gives the valid but weaker
T_infinity<=[log(4(n-1))+1]/(2c). Both remove the artificial log(1/eta)
from the optimized small-beta sandwich. With Lambda=O(n), (14) is
u=O(eta n log n) when eta n log n is small. The general mean comparison
then has log error O(eta n^(3/2) log n), without a factor equal to the
rare-event waiting time.

### Product reference: forcing decays before global mixing

Suppose more specifically that Q0 flips bit i at rate c_i>0, and Q has
only single-bit moves with rates q_i(x) satisfying

    |delta q_i(x)|=|q_i(x)-c_i|<=eta c_i.

No locality assumption on the state dependence is needed for this
mathematical implication. Locality is still needed to acquire all rates
using a polynomial-size passive rate table.

Under the uniform reference,

    E*1=sum_i f_i,
    f_i(x)=delta q_i(x^i)-delta q_i(x),
    f_i(x^i)=-f_i(x), ||f_i||infinity<=2eta c_i.

The product semigroup commutes with each bit-flip projection. Its i-th
factor acts on f_i by multiplication with exp(-2c_i t), and its other
factors contract L-infinity. Therefore

    ||P0*(t)f_i||infinity<=2eta c_i exp(-2c_i t),
    ||R0*E*1||infinity<=sum_i eta=n eta.            (17)

Apply (15) with b_forcing=n eta, not T_infinity d:

    z<=n eta/(1-a), u_product=-log[1-n eta/(1-a)].  (18)

These expressions are valid when a<1 and n eta/(1-a)<1. For equal c_i=c,
use (16) and Lambda=nc. For unequal c_i, the same sufficient envelope
uses c=min_i c_i and Lambda=sum_i c_i. The forcing argument is an ordinary
tensor-product semigroup calculation. It is valid even though the true
source can be nonreversible and have a nonproduct stationary law.

Stronger ordinary baseline found subsequently: relabeled coordinatewise
coupling proves (1-eta)^n<=pi/pi0<=(1+eta)^n for this pure product
reference, with no bootstrap smallness condition. See
CYLINDER_COUPLING_BASELINE.md Eq(5). Thus(18) is correct but unnecessary
for this subclass. Combining that ordinary pointwise bound with Section7
also covers nonmonotone targets; the pure-product case alone cannot
establish a missing consequence of the general reference-transfer method.

## 7. Sharper all-target comparison for a reversible reference

Assume D0 is symmetric. The true balanced matrix D need not be symmetric.
Write S=(D+D^T)/2 and A_skew=(D-D^T)/2. Since the reference flows are
symmetric and true flows lie in exp(+/-v) times the reference flows,

    exp(-v) D0 <= S <= exp(v) D0                    (19)

as quadratic forms. Let K0=sqrt(2Lambda/g). The mixed estimate (3),
followed by antisymmetrization and (19), gives

    |f^T A_skew h|
       <=2K0 sinh(v/2) exp(v/2) sqrt(E_S(f)E_S(h))
       =kappa_skew sqrt(E_S(f)E_S(h)),
    kappa_skew=K0[exp(v)-1].                       (20)

To see the antisymmetrization explicitly, write
f^T A_skew h=[f^T(D-D0)h-h^T(D-D0)f]/2. Bound each term by (3),
and use E0<=exp(v)E_S. Centering either vector causes no problem because
all these matrices have zero row and column sums.

For any target A_target, extend killed-space vectors by0 on A_target.
The killed symmetric matrix S_B is positive definite. Equation(20) implies

    J=S_B^(-1/2) (A_skew)_B S_B^(-1/2),
    J^T=-J, ||J||2<=kappa_skew.

For any real vector b, put y=S_B^(-1/2)b. Elementary inverse algebra gives

    b^T D_B^(-1)b=y^T(I+J)^(-1)y
                 =y^T(I-J^2)^(-1)y.

The second equality concerns the quadratic form: the symmetric part of
(I+J)^(-1) is (I-J^2)^(-1). It is not an equality of those two matrices.
Since -J^2 is positive semidefinite with norm at most kappa_skew^2,

    b^T S_B^(-1)b/(1+kappa_skew^2)
          <=b^T D_B^(-1)b<=b^T S_B^(-1)b.          (21)

Use b=pi0_B and (19), then the positive-inverse weight step from Section2:

    exp(-v)/(1+kappa_skew^2)
          <=M(pi0,D)/M(pi0,D0)<=exp(v),            (22)

    exp(-2u-v) b0/[b(1+kappa_skew^2)]
          <=M/M0<=exp(2u+v) b0/b.                 (23)

One can substitute b_min and b_max from(8) for the unknown b; or replace
its ratio by exp(+/-u) for a simpler all-target factor. Nonreversibility
now costs quadratically in the sector perturbation. This is the standard
symmetric/skew inverse mechanism, already explicit for nonreversible
variance calculations in Duncan--Lelievre--Pavliotis2016, Lemma3 Eq(29)
and Eq(31). The finite killed-matrix application above is proved here so
its target-boundary and weight conventions are unambiguous.

Together with (18), the equal-rate independent-bit reference has leading
log mean error O(n eta), plus O(n^3 eta^2) from the skew correction, in
the sufficient bootstrap regime eta n log n small. This is a conditional
performance bound, not a claim of optimal dimension dependence.
