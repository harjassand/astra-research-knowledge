# Reverse-pulse residual certificates: sharpness and a task-specific obstruction

Private Astra P3 adversarial derivation, 2026-10-23. This is a bounded
theoretical check of the parent's inverse-free reverse-pulse construction.
It adds no benchmark and makes no priority claim. Exact moment comparisons
below are established by explicit polynomial inequalities; they do not rely
on a hidden-rank or spectral-gap promise.

## 1. The claimed pair-residual identity is correct

Let A_a be self-adjoint contractions on a common Hilbert space. Let V map
coefficient vectors into acquired features, and include the readout vector
f=V c. Define

    B_a = A_a V - V T_a,
    G = V*V,
    H_a = V*A_a V,
    J_a = V*A_a^2 V,
    D_a = V*B_a = H_a-G T_a,
    R_a = B_a*B_a
        = J_a-H_a* T_a-T_a* H_a+T_a* G T_a.

The coefficient matrices T_a need not be G-self-adjoint, inverses are not
required, and R_a is positive semidefinite in exact arithmetic. The same
feature, stationary inner product and pulse operator must underlie all
correlations used to acquire G,H,J.

For a length-N target with ordered product A_1...A_N, put

    ell_0=c,       ell_j=T_j ell_(j-1),
    r_N=c,         r_(j-1)=T_j r_j,
    qhat=c*G r_0,
    qcorrected=qhat + sum_j ell_(j-1)* D_j r_j.

Right-side telescoping first gives

    q-qhat = sum_j <A_(j-1)...A_1 f, B_j r_j>.

The difference between the true left prefix and its coefficient lift is

    A_(j-1)...A_1 f-V ell_(j-1)
      = sum_{i<j} A_(j-1)...A_(i+1) B_i ell_(i-1).

Therefore the exact corrected error is

    q-qcorrected
      = sum_{i<j}
          <A_(j-1)...A_(i+1) B_i ell_(i-1), B_j r_j>.             (1)

Each intervening true operator is a contraction. Hence

    |q-qcorrected|
      <= sum_{i<j}
          sqrt(ell_(i-1)*R_i ell_(i-1))
          sqrt(r_j*R_j r_j).                                    (2)

In particular, arbitrary non-self-adjoint rational T_a do not invalidate the
correction: their asymmetry is accounted for by D_a. An omitted D correction
would require a separate argument.

## 2. A one-feature reduction makes the strongest moment baseline explicit

Take one positive self-adjoint contraction A, a unit readout f, and only the
feature f. The acquired data are

    C_0=1,   C_1=<f,Af>=lambda,
    C_2=<f,A^2 f>=lambda^2+v,

where 0<lambda<1 and 0<=v<=lambda(1-lambda). Choose the scalar coefficient
model T=lambda. Then D=0, R=v, and (2) becomes

    |C_N-lambda^N| <= v S_N(lambda),                              (3)

where, for N>=2,

    S_N(lambda)=sum_{k=0}^{N-2}(k+1)lambda^k
      =[1-N lambda^(N-1)+(N-1)lambda^N]/(1-lambda)^2.               (4)

The residual-pair count in (4) follows by fixing
k=(i-1)+(N-j); there are k+1 such pairs. In particular,

    S_N(lambda) <= (1-lambda)^(-2)                                (5)

for every horizon. This can be a nontrivial uniform pointwise prediction
contract even though the unrepresented dynamics has eigenvalues near one.

The spectral theorem represents C_N as the Nth moment of a probability
measure on [0,1]. Thus the strongest equally informed moment method solves

    min/max integral x^N dmu(x)
    subject to support(mu) subset [0,1],
               integral x dmu=lambda,
               integral x^2 dmu=lambda^2+v.                       (6)

For every integer N>=3, this problem has the explicit sharp solution below.
It requires no training, parameter search, hidden-state dimension, or matrix
inverse beyond ordinary rational scalar arithmetic.

Set

    x=lambda-v/(1-lambda),
    p=v/[(1-lambda)^2+v],
    y=lambda+v/lambda,
    q=lambda^2/(lambda^2+v).

Then

    L_N=q y^N=lambda y^(N-1),
    U_N=p+(1-p)x^N,                                                (7)

and every compatible positive contraction satisfies L_N<=C_N<=U_N.
Both endpoints are attained: use respectively

    mu_minus=(1-q)delta_0+q delta_y,
    mu_plus=p delta_1+(1-p)delta_x.                                (8)

They have the same zeroth, first and second moments. For v=0 both reduce
to delta_lambda; for maximal v both reduce to the same endpoint mixture.

### Polynomial proof and an explicit strong retaining baseline

Let g(t)=t^N. The quadratic Hermite interpolant U(t) that agrees with g
and g' at x and with g at 1 obeys

    g(t)-U(t) = g'''(xi)/6 * (t-x)^2(t-1) <=0

on [0,1]. This is the interpolation remainder, with its limiting meaning
at repeated nodes. Since g''' is nonnegative for N>=3, U majorizes g.
The quadratic interpolant L(t) that agrees with g at 0 and with g,g' at y
obeys

    g(t)-L(t) = g'''(xi)/6 * t(t-y)^2 >=0.

Its explicit expression is

    L(t)=(N-1)y^(N-2)t^2-(N-2)y^(N-1)t.

Expectations of either quadratic depend only on the retained three moments.
Equality holds on the two-node supports in (8), proving (7) exactly.

The upper polynomial can also be evaluated directly as

    U(t)=x^N+N x^(N-1)(t-x)+c(t-x)^2,
    c=[1-x^N-N x^(N-1)(1-x)]/(1-x)^2.

This is a complete same-information baseline, equivalent to a tiny univariate
moment optimization with explicit dual polynomial certificates. A generic
moment/semidefinite method is entitled to the same observations and cannot
be omitted from a claimed advantage comparison.

## 3. The residual-pair bound is first-order information-optimal

For fixed lambda in (0,1) and fixed integer N>=2, expand the sharp upper
endpoint in small v:

    U_N-lambda^N = v S_N(lambda)+O(v^2).                           (9)

Indeed p=v/(1-lambda)^2+O(v^2) and
x=lambda-v/(1-lambda). Substitution into (7) gives exactly (4) as the
linear coefficient. Consequently no uniformly sound certificate using only
C_0,C_1,C_2 can improve the leading coefficient in (3) for this class.
The moment baseline improves the higher-order slack, and supplies a sharp
one-sided interval rather than only a symmetric error bar.

There is also a uniform-horizon sharpness limit. As N tends to infinity,

    U_N -> p = v/[(1-lambda)^2+v],
    v S_N(lambda) -> v/(1-lambda)^2.

Their ratio tends to (1-lambda)^2/[(1-lambda)^2+v], which tends to one as
v tends to zero. A small persistent mode with small readout weight accounts
for the residual error. Requiring full identification would be unnecessary
for a pointwise absolute-error task, while pretending that the hidden mode
is absent would be invalid.

This lower bound already holds in a two-dimensional Hilbert space. For
example, the symmetric matrix

    A_plus = [[lambda, sqrt(v)],
              [sqrt(v), 1-v/(1-lambda)]]

has eigenvalues 1 and x, and f=(1,0). Its first two moments are the acquired
ones and its target is U_N. The lower extremizer is

    A_minus = [[lambda, sqrt(v)],
               [sqrt(v), v/lambda]],

with eigenvalues 0 and y. Both are positive contractions. These witnesses
are operator constructions; the next section supplies reversible Markov
realizations with bounded experimentally observable f.

## 4. Same moments and same short observation laws in reversible sources

For a concrete balanced choice lambda=1/2 and 0<v<1/4, put

    p=4v/(1+4v),    q=1/(1+4v),
    x=1/2-2v,      y=1/2+2v,
    pi=(p/2,p/2,q/2,q/2),
    f=(1,-1,1,-1).

Let

    K(theta) = (1/2) [[1+theta,1-theta],
                      [1-theta,1+theta]].

Use block-diagonal reversible Markov operators

    P_plus = diag(K(1), K(x)),
    P_minus = diag(K(0), K(y)).                                   (10)

Both share the same pi and the same bounded readout. The readout has
stationary mean zero and squared norm one. Their correlation measures are
exactly the two measures in (8), so their first two pulse correlations agree
and their longer correlations attain (7). All spectral values are
nonnegative. There is no hidden dimensionality explanation: four states
suffice.

The exact extremizers in (10) are not strictly mixing finite-time CTMC
propagators: one has a persistent contrast mode and the other a zero
eigenvalue. That distinction must not be hidden when comparing a physical
continuous-time subclass.

### Strictly positive irreducible finite-CTMC approximants

Choose a in (0,1) and r in (0,1). Replace each P by

    P^a = a I+(1-a)P,
    P'  = r P^a+(1-r)Pi,          Pi=1 pi^T.                      (11)

Every entry of P' is strictly positive, it is reversible with common pi,
and it has a finite continuous-time Markov generator. To see the last
claim, each two-state block K(theta), theta>0, is the unit-time exponential
of

    Q_theta=(-log theta)/2 * [[-1,1],[1,-1]].

Let Q be the block-diagonal generator of P^a. It commutes with Pi because
Q1=0 and pi^T Q=0. Then

    P'=exp[Q+(-log r)(Pi-I)].                                     (12)

The generator has positive inter-block rates and is irreducible. All rates
are finite. On mean-zero readouts, the pulse correlations become

    C_N^+ = r^N [p+q(a+(1-a)x)^N],
    C_N^- = r^N [p a^N+q(a+(1-a)y)^N].                            (13)

They still agree exactly at N=0,1,2, with

    C_1 = r(1+a)/2,
    C_2 = r^2 [((1+a)/2)^2+(1-a)^2 v].

For a small positive a and r sufficiently close to one relative to a chosen
horizon, the long-target ambiguity approaches that of the sharp extremizers.
Therefore merely promising finite irreducible reversible kinetics, without
a quantitative gap, does not eliminate the ambiguity. A supplied gap is
additional information that the strong physical baseline may exploit.

### Retaining all short raw observations does not distinguish these sources

The global sign flip within each block preserves the source law and changes
f to -f. Thus every odd product of stationary f observations has mean zero.
For a stationary observed sequence s_0,s_1,s_2 in {-1,1}, its full law is

    Pr(s_0,s_1,s_2)
      = (1/8)[1+C_1(s_0 s_1+s_1 s_2)+C_2 s_0 s_2].                (14)

This follows by the binary Fourier expansion: the means and triple moment
vanish, the adjacent pair correlations are C_1 by stationarity, and the
remaining pair correlation is C_2.

Consequently the matched pairs above have identical distributions for every
stationary observed trial of at most two actions, including every pulse-boundary
readout and outcome-dependent early stopping. Arbitrarily many independent
such trials do not distinguish them. The obstruction is not caused by
throwing away useful raw short-trial observations. Preparing particular
hidden states, measuring another observable, changing the pulse, or using
longer trials supplies different information and is outside this equality.
Continuously resolving the path inside each pulse is also stronger access;
only the declared boundary observations are covered by (14).

## 5. Small uniform pointwise error does not bound integrated response

Fix exact moments C_0=1, C_1=lambda, C_2=lambda^2+v with
0<v<lambda(1-lambda). For every sufficiently small epsilon>0, define

    b_epsilon=1-epsilon,
    x_epsilon=lambda-v/(b_epsilon-lambda),
    p_epsilon=v/[(b_epsilon-lambda)^2+v],
    mu_epsilon=p_epsilon delta_(b_epsilon)
                +(1-p_epsilon)delta_(x_epsilon).                  (15)

Both support points lie strictly between zero and one. Every member has
exactly the same retained moments, while

    sum_{N=0}^infinity C_N
      = p_epsilon/(1-b_epsilon)
          +(1-p_epsilon)/(1-x_epsilon)
      -> infinity                                                 (16)

as epsilon tends to zero. Subtracting the N=0 term or forming the customary
integrated autocorrelation 1+2 sum_{N>=1} C_N does not change this obstruction.
The analogous continuous-time integrated correlation also diverges because
the first decay rate is -log b_epsilon.

Each source can again be realized as a strictly positive irreducible
four-state finite-CTMC propagator with bounded f. Set stationary block
weights p_epsilon and 1-p_epsilon, choose r_epsilon strictly between
b_epsilon and one, use block eigenvalues b_epsilon/r_epsilon and
x_epsilon/r_epsilon, then add the mixing term in (11). On f, the resulting
eigenvalues are exactly those in (15). Formula (12) proves embeddability.
The stationary mean and one-point f distribution are the same for every
member, and (14) gives exactly the same complete two-action observation law.
The hidden equilibrium weights vary across this family; access to those
weights as separately resolved hidden-state information would be additional
evidence. Within each source, all pulses use its one common equilibrium.

### The obstruction also holds with a fixed known equilibrium

A six-state construction removes even that variation. Fix lambda=1/2,
0<v<=1/64, and

    p=v/[2(1/4+v)]=2v/(1+4v).

Use three two-state blocks with fixed equilibrium weights
p,(1-p)/2,(1-p)/2 and f=(1,-1,1,-1,1,-1). Let b range over [7/8,1), and
define

    m_b=(1/2-p b)/(1-p),
    s_b^2=[v-p((b-1/2)^2+v)]/(1-p)^2,
    x_b=m_b-s_b,    y_b=m_b+s_b.

The spectral measure with weights p,(1-p)/2,(1-p)/2 at b,x_b,y_b has
mean 1/2 and second moment 1/4+v exactly. Its rest variance is positive:
the numerator defining s_b^2 is at least v/2. Also p<=1/34,
m_b>=16/33 and s_b<=17/132. Consequently

    0 < 47/132 <= x_b <= y_b <= 83/132 < 7/8 <= b < 1.

Choose r_b=(1+b)/2 and form three blocks with eigenvalues
b/r_b,x_b/r_b,y_b/r_b, followed by the common equilibrium mixing in (11).
All are positive finite-rate CTMCs with the exact same six-state pi and the
same f, and their generators are irreducible by (12). The integrated
correlation is at least p/(1-b), hence unbounded. Their complete short
binary observation laws remain identical by (14). Even knowing the fixed
equilibrium distribution and the dimension six would not resolve this
particular short-access obstruction.

Thus short monitored experiments can warrant a uniformly small absolute
error for every individual future correlation through (3)-(5), while they
cannot warrant any finite upper bound on integrated correlation. This is a
task-specific insufficiency theorem, not a failure of the pointwise
construction. No full identification requirement is necessary for the first
task; some control of slow residual spectral mass is necessary for the
second.

## 6. Finite acquisition gives a simultaneous pointwise certificate

Exact input moments are not free. Suppose f is bounded by one, C_0=1 is
known (as for the binary readout above), and stationary reset/readout trials
give simultaneous intervals

    |C_1-Hhat|<=eta_H,    |C_2-Jhat|<=eta_J.

For any selected rational scalar t with |t|<1, let

    Dhat=Hhat-t,
    Rupper=max(0, Jhat-2t Hhat+t^2+eta_J+2|t|eta_H).

On that same confidence event, for all integer N>=1 simultaneously,

    |C_N - [t^N+N Dhat t^(N-1)]|
      <= Rupper S_N(|t|)+N eta_H |t|^(N-1),                       (17)

with S_1=0 and the usual 0^0 convention at N=1. This follows by applying
the exact corrected formula to t and bounding its single unknown D.
The parameter t may be selected from these observations because the
simultaneous moment event supports the algebra for every t. In particular,

    uniform error <= Rupper/(1-|t|)^2 + eta_H/(1-|t|),             (18)

where N r^(N-1)<=1/(1-r) follows by comparing each of N terms with the
geometric sum. No union bound over infinitely many prediction horizons is
needed: the uncertainty is in the finite acquired moments.

A simple acquisition scheme retains all three binary observations of each
independent stationary two-action trial. For m such trials the two sample
means of f_0 f_1 and f_0 f_2 obey simultaneous Hoeffding errors at most eta
with confidence 1-delta if

    m >= 2 log(4/delta)/eta^2.                                    (19)

This costs m stationary preparations and 2m actions, plus readout and
preparation time. Correlation between the two sample means is allowed by the
union bound. A stronger joint likelihood or variance-aware procedure should
retain it. Calibration, nondisturbing readout and stationarity are contracts,
not consequences of (19).

The eta^-2 scale is not automatically removed by small residual v. In the
balanced binary example lambda=1/2, the v=0 triple law has two probabilities
9/32, four probabilities 3/32 and two probabilities 1/32. Changing v from
zero changes every triple probability by magnitude v/8. Thus exactly

    chi-square(P_v || P_0)
      = sum_s [P_v(s)-P_0(s)]^2/P_0(s)
      = 16 v^2/9,
    KL(P_v || P_0) <= 16 v^2/9.                                  (20)

This yields a target-prediction lower bound, rather than merely a demand to
estimate an intermediate moment. Let 0<epsilon<=1/64, v=epsilon, and

    N=ceil(log_2(1/epsilon))+2 >=8,
    b=1-1/N^2,
    x=1/2-epsilon/(b-1/2),
    p=epsilon/[(b-1/2)^2+epsilon].

Compare the null correlation C_N^0=(1/2)^N with the alternative
C_N^1=p b^N+(1-p)x^N. They have the same C_1=1/2, and their C_2 values
differ by epsilon. The parameters satisfy

    p >= 4epsilon/(1+4epsilon),
    b^N >= 1-1/N >=7/8,
    (1/2)^N <=epsilon/4.

Therefore

    C_N^1-C_N^0 >= (207/68)epsilon >2epsilon.                     (21)

Both hypotheses have strictly positive irreducible finite-CTMC realizations
with exactly the SAME four-state equilibrium pi and the same bounded f.
Use weights p,1-p, r=(1+b)/2 and common Pi. For the alternative, take
within-block eigenvalues b/r and x/r. For the null, take eigenvalue
(1/2)/r in both blocks. Form r times the block operator plus (1-r)Pi.
All within-block eigenvalues lie strictly between zero and one; (12)
supplies the finite generators. The null has f as an eigenfunction with
eigenvalue 1/2; the alternative has the two prescribed readout modes.

For m adaptive independent stationary trials of at most two actions, the
transcript KL is at most 16m epsilon^2/9. Intermediate readout, retaining
the full histories, shorter queries and early stopping cannot increase it
beyond the full two-action trial. Any estimator accurate to epsilon with
probability 1-delta under both hypotheses would distinguish them by (21).
More usefully, the same reduction applies to a globally valid confidence
procedure allowed to return wide intervals elsewhere: suppose that under
the null, with probability at least 1-delta, it returns an interval containing
C_N^0 and of length at most 2epsilon. That event has probability at most
delta under the alternative, because an interval of that length cannot
contain both values. Data processing for the resulting binary test gives

    m >= [9/(16epsilon^2)]
          (1-2delta)log((1-delta)/delta),       delta<1/2.           (22)

Thus the epsilon^-2 short-trial sample order is necessary for informative
valid certification under the null, even for a target whose horizon is only
O(log(1/epsilon)). The squared-residual certificate achieves that order:
when v=0 and t=1/2, simultaneous errors eta_H=eta_J=eta imply
Rupper<=4eta on the confidence event, and (18) is at most 18eta. Set
eta=epsilon/18 in (19); then m>=648 log(4/delta)/epsilon^2 is a sufficient
explicit count for a valid uniform pointwise certificate of radius epsilon
under the null. The constant is deliberately conservative.

This is not a guarantee of precision epsilon for every positive v. Exact
short moments may leave an intrinsic interval wider than 2epsilon, as (7)
shows; more samples of the same experiment cannot remove that ambiguity.
Wide certificates or additional information are then necessary.

Insisting instead on
a first-order residual norm of order epsilon and estimating its square to
order epsilon^2 can create an epsilon^-4 sufficient count; that is a weaker
proof/estimation strategy, not an equally informed optimal baseline. The
exact moment method shares the epsilon^-2 information order.

Equations (19)-(22) concern bounded short-observation access. A different
coupled simulator or conditional sampling interface can have a different
cost. Direct long trials also have epsilon^-2 sample order at fixed
confidence, with N actions per trial; no reset-count separation follows.

Exact rational evaluation of (7), (17) or a forecast has bit costs that grow
with input precision and exponent length. Powers can use repeated squaring;
a finite-bit implementation must propagate outward error. Establishing small
Rupper may require correspondingly precise moments. None of these costs is
removed by avoiding a matrix inverse.

## 7. Multiple actions: a general uniform-length consequence

Suppose the acquired coefficient operators obey ||T_a||<=r<1 and their
true residual Gram matrices obey ||R_a||<=kappa for every allowed action.
For a target with left and right endpoint coefficient norms L and R, (2)
implies

    |q-qcorrected| <= L R kappa S_N(r)
                     <= L R kappa/(1-r)^2.                       (23)

The proof uses
||ell_(i-1)||<=L r^(i-1) and ||r_j||<=R r^(N-j), then the same pair count
as (4). When the readout is the included empty-word feature, its coefficient
vector is a coordinate unit vector and L=R=1.

This does not assert contraction of the full unobserved dynamics. Such
dynamics may retain arbitrarily slow modes with small acquired readout
couplings, as (15) already demonstrates. The norm conditions are themselves
acquired/verified representation conditions; finding stable T, bounding
R under noisy G,H,J, feature search, reverse-pulse feasibility and confidence
construction must all be charged. Coordinate conditioning can affect r,
kappa and the endpoint coefficient norms.

A finite simultaneous confidence set for the acquired matrices can certify
(23) for every future word covered by its action set. It does not identify
the system or certify integrated response. A retaining moment or program
learner with the same reverse-pulse tools is entitled to this same operation.

## 8. What this adversarial check resolves

The inverse-free correction is sound and its pair-residual bound can be
first-order sharp with only two observed moments. Finite acquired local
information can genuinely support new long-horizon pointwise predictions
without full model identification or a spectral gap. The construction does
not imply accurate integrated response, global hidden-dynamics contraction,
or a new architecture advantage. The exact moment baseline is stronger on
the one-action subproblem, and the four-state witnesses prevent that baseline
or any other equally informed procedure from inferring more than its data
permit.

## 9. Primary-source baseline check

The one-action moment baseline is classical. Golub and Meurant's
*Matrices, moments and quadrature*, Sections 2 and 3.1, represent symmetric
matrix functionals by spectral Stieltjes integrals and derive Gauss-Radau
bounds using a prescribed endpoint and a Hermite interpolation remainder.
The two-node formulas (7) are the corresponding elementary specialization,
with nonnegative third derivative for t^N. The primary author-hosted text
was read after deriving the explicit witness:

https://gerard-meurant.fr/mmq_1993.pdf

Bertsimas and Popescu's *Optimal Inequalities in Probability Theory: A
Convex Optimization Approach*, SIAM Journal on Optimization 15(3), 780-804
(2005), DOI 10.1137/S1052623401399903, develops tight moment bounds through
convex and semidefinite optimization. Its primary author-hosted text was
read for the incumbent comparison; the explicit polynomial proof above
establishes this note's particular bounds directly:

https://www.mit.edu/~dbertsim/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf

These sources do not establish novelty of the parent's switched multi-action
residual certificate. They do rule out presenting the one-action
moment-to-long-correlation capability or its endpoint quadrature baseline as
newly invented here. A targeted prior-art search for that broader certificate
remains a separate task.
