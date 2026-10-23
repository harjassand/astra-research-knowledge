# Bounded precision assessment: screen error and target error are different

Contributor: /root/cycle10_precision. Scientific date: 23 October 2026,
Australia/Brisbane. This is a bounded alternative assessment for the PRO3
principal, not a replacement of the selected endpoint investigation.

## Decision

There is a clean implementation distinction worth preserving, but the elementary
results below do not justify redirecting the current allocation into a new
precision campaign. They adapt established delayed-acceptance and perturbation
ideas. No historical novelty or efficient implementation claim is made.

The distinction is exact:

1. A reciprocal-consistent error in the first screen preserves the true target
   when the correction uses the exact target Hastings ratio. It can affect
   transport and mixing, but it does not by itself create stationary bias.
2. Coherent errors in target evaluations define a different target. Even the
   easy null pi=q then admits a sharp, nonzero stationary error. An existing
   exact-real screen theorem cannot remove that error.

This is a useful computational contract boundary. A serious further question
would need a specified arithmetic/evaluation algorithm and paid accuracy cost;
an abstract per-edge error allowance is not an IEEE floating-point model.

## Sources actually read

The exact Cycle9 original was read at
cycle10_pro3/incoming/Astra_Amplification_Cycle9_PRO3_20261022/:
SHARP_DISTORTION_RATE.md, INFORMATION_AND_COST_CONTRACT.md, and the copied
Cycle8 ASYMMETRY_BUDGET_THEOREM.md finite energy proof.

Primary literature opened and relevant passages read:

- Sherlock and Lee, *Variance bounding of delayed-acceptance kernels*,
  arXiv:1706.02142v4, especially the exact correction mechanism and bounded
  surrogate-discrepancy discussion: https://arxiv.org/html/1706.02142v4 .
  This establishes the prior target-preserving delayed-acceptance setting
  and qualitative robustness context. It is not the owner’s moving-KL rate.
- Alquier, Friel, Everitt and Boland, *Noisy Monte Carlo: Convergence of
  Markov chains with approximate transition kernels*, arXiv:1403.5496v3,
  Theorems 2.1 and 2.2: https://arxiv.org/pdf/1403.5496 . Their perturbation
  discussion uses uniform/geometric ergodicity assumptions and distinguishes
  the ideal invariant target from the approximate kernel. It does not supply
  a support-uniform mixing constant from the owner’s sole KL promise.

These sources make a claim of a new generic perturbation principle unwarranted.
The precise elementary statements below are proved here for reuse; no broad
novelty search or external mathematical acceptance is asserted.

## 1. Reciprocal-consistent first-screen error

Fix one finite native instance and its true target Hastings ratios
t_xy=(pi_y Q_yx)/(pi_x Q_xy). Write s_xy=log S_xy. Suppose a computed screen
has

    shat_xy=s_xy+e_xy,   e_yx=-e_xy,   |e_xy|<=E.

The error field and proposal remain fixed within the run. Define the actual
computed local off-diagonal probability as

    Lhat_xy=Q_xy min(1,exp(shat_xy)) min(1,t_xy exp(-shat_xy)),

and retain its actual completing rejection diagonal. This model assumes the
second factor uses the EXACT t_xy. It does not grant that operation at zero
precision or target-evaluation cost.

### Lemma 1 (exact invariant target and edge comparison)

Lhat is pi-reversible. If L is the ideal local factorization, then on every
positive proposal edge

    exp(-E) L_xy <= Lhat_xy <= exp(E) L_xy.

Proof. Both shat and log t change sign when the edge is reversed. The ratio
of the two forward acceptance factors to their reverse factors is t_xy,
so pi_x Lhat_xy=pi_y Lhat_yx. For the comparison put

    f_t(s)=log[min(1,exp(s)) min(1,exp(t-s))]
          =min(0,s)+min(0,t-s),

where t now denotes log t_xy. This piecewise-linear function has slopes
in {-1,0,1}; hence it is globally 1-Lipschitz. Apply this to s and s+e,
then exponentiate. Diagonal equality is not asserted or needed. QED.

If Chat=(I+alpha G+beta Lhat)/2 with exact G, the actual target remains pi.
The Dirichlet forms obey

    E_Chat(f,f) >= exp(-E) E_C(f,f),

because every off-diagonal coefficient, including the unchanged G component,
has that lower comparison. This does NOT imply finite-time TV ordering.

A simple finite-horizon perturbation bound is

    sup_x TV(Chat(x,.),C(x,.)) <= beta (exp(E)-1)/2,
    TV(mu Chat^n,mu C^n) <= min(1,n beta (exp(E)-1)/2).

The first inequality follows by summing absolute off-diagonal changes and
paying the completing diagonal; the second is kernel telescoping plus TV
contraction. Its n factor generally makes it uninformative at the scientific
logarithmic scale. It is recorded as a standard bound, not offered as a new
sharp rate theorem.

### Lemma 2 (honest reduction of the accepted upper interface)

For the owner’s original public discrepancy D=|kappa-eta|A, the finite
Cycle8 energy and full-return upper certificate applies to Chat with D
replaced by D+E.

Proof. With r_xy=(q_y/q_x)(Q_yx/Q_xy), the perturbed screen satisfies

    Shat_xy = r_xy^eta exp(xi_xy+e_xy),
    |xi_xy+e_xy| <= D+E.

The finite energy proof uses precisely this upper screen envelope, reciprocal
support, exact pi-reversibility, the true accepted-outflow subtraction and
the unchanged G component. Its equations (11)-(16) do not otherwise use
xi_xy=(kappa-eta)log(Q_yx/Q_xy). Lemma 1 supplies reversibility and the actual
diagonal is retained. All smoothing and post-hit propagation hypotheses
therefore continue to hold. This proves an UPPER transfer only; it does not
prove sharpness for a restricted arithmetic-error generator. QED.

An arbitrary antisymmetric edge-error allowance can be much larger than the
errors generated by cached scalar evaluations. For example, if a cached
log q value is log q_x+h_x with |h_x|<=epsilon and the rest is exact, the
first-screen log error is eta(h_y-h_x), bounded by 2 eta epsilon; its sum
along a path is eta(h_endpoint-h_start). Treating that error as freely
adversarial on every edge discards real consistency information. Rounding
of subsequent multiplication/exponentiation requires additional assumptions.

Conversely, on an oriented symmetric tree one may assign e_xy=E on forward
edges and -E on reverse edges. With forward degree M and Q_edge=1/(M+1),
level masses q_i=b z^i and z=M exp(-(E+a)/eta) give actual first acceptance
exp(-a). Thus even A(Q)=0 cannot protect against an independently admitted
screen-error field. This is an algebraic realization of the envelope; a
complete asymptotic arithmetic-error theorem would still have to specify
the error generator and retain the owner’s admission/return obligations.
It must not be labelled an actual roundoff counterexample.

## 2. Coherent target-evaluation error

Suppose instead every unnormalized target evaluation is coherently replaced by

    pi_unnormalized(x) exp(h_x),    osc(h):=max h-min h <= B.

Every target Hastings ratio, including the ratio used by the global IMH
component, is formed consistently from those values. A common additive
constant in h is irrelevant. Exact proposals and reciprocal screen factors
are retained. Then the actual target is

    pi_h(x)=pi(x) exp(h_x) / sum_z pi(z) exp(h_z).

This is an explicitly CHANGED target-oracle contract. It is outside the
exact-pi native theorem, not a defect in that theorem. It may model a certified
deterministic approximation to log target values, but certifying B over the
whole relevant support is a substantive input assumption.

### Theorem 3 (sharp stationary bias for bounded coherent log error)

For every finite positive pi and every such h,

    TV(pi_h,pi) <= tanh(B/4).

The constant is attained on two positive states. Thus no uniform smaller
stationary-bias bound follows from osc(h)<=B alone, even with pi=q and
D(pi||q)=0 under the same supplied positive K.

Proof. Let Y=exp(h), m=min Y, M=max Y and mu=E_pi Y. Then

    TV(pi_h,pi)=E_pi[(Y-mu)_+]/mu.

For y in [m,M], convexity of (y-mu)_+ gives the chord bound
(y-mu)_+ <= (y-m)(M-mu)/(M-m). Taking expectation gives

    TV <= (mu-m)(M-mu)/(mu(M-m)).

The right side is maximized over mu in [m,M] at mu=sqrt(mM), with maximum
(sqrt(M)-sqrt(m))/(sqrt(M)+sqrt(m))=tanh(log(M/m)/4)<=tanh(B/4).
The case m=M is zero directly.

For equality let t=exp(B/2), take

    pi=q=(t/(1+t), 1/(1+t)),   h=(0,B).

Then pi_h=(1/(1+t),t/(1+t)) and TV=(t-1)/(t+1)=tanh(B/4).
Every mass is strictly positive. The population KL is exactly zero. QED.

If a numerical contract instead certifies |h_x|<=epsilon after one common
centering, then B<=2epsilon and the sharp worst-case bound becomes
tanh(epsilon/2). Confusing an edge log-ratio tolerance with a scalar
log-density tolerance loses a factor and possibly a consistency condition.

### Theorem 4 (exact proposal-start obstruction, all returns retained)

Use the two-state equality construction, let Q=I and let G_h be independence
MH using proposal q and target pi_h. All local attempts hold, so

    Chat=(1-alpha/2) I+(alpha/2) G_h.

Starting at q=pi, for every integer n>=0,

    TV(q Chat^n,pi)
      = tanh(B/4) [1-(1-alpha exp(-B/2)/2)^n].

Proof. Write states 0,1 in the order above. The off-diagonal probabilities
of G_h are G_h(0,1)=1/(1+t), G_h(1,0)=1/[t(1+t)]. Their sum is 1/t.
Thus Chat has nontrivial eigenvalue lambda=1-alpha/(2t). Its invariant
distribution is pi_h. The two-state law is exactly

    q Chat^n=pi_h+lambda^n(q-pi_h).

Subtract q=pi and take TV. This is the full transition law, including
every hold and return. QED.

For any fixed B>0 the proposal-start error tends to tanh(B/4), despite the
true pi=q null. If B_n->0, n->infinity, the bracket tends to one and the
error is asymptotic to B_n/4. Hence B_n much larger than 1/log n defeats
critical-scale O(1/log n) accuracy in this changed oracle model. To make
this bias o(1/log n), B_n=o(1/log n) is necessary in the worst case.
This is a bias requirement, not a sufficient full mixing theorem.

Ordinary exact IMH starts at stationarity on the same true pi=q pair, and
direct q sampling is also legitimate for the disclosed analytic null. An
ordinary sampler given the SAME coherently corrupted target ratios suffers
the same target substitution. The construction is not an advantage for the
hybrid and does not hide a legitimate ordinary control.

## 3. Limits and resources

No off-candidate target table, normalizer, KL estimator, precision oracle or
free exact correction is introduced. The bounded error certificates are
explicit assumptions. Obtaining them, evaluating exponentials, sampling q
and Q, evaluating reverse Q and storing cached values retain actual costs.

No general target-ratio error theorem for arbitrary non-gradient edge fields
is proved here. Such fields need not define a perturbed probability density,
so Theorem 3 cannot be applied to them. Likewise, stationary bias is not a
proposal-start mixing upper. The standard perturbation literature requires
additional stability information for stronger conclusions.

The two-state rational diagnostic accompanying this note takes t=2,
B=log 4, alpha=1/2 and n=64, fixed before execution. It verifies the exact
matrix identity and the true null KL without changing any old fixture.
Its small execution cost is recorded separately, not treated as discovery.
No old suite, evaluator experiment, protected programme or private handoff
was run. Inference, token, design and total research costs remain unknown.
