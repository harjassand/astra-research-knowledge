# Certified physical response design without a hidden-state model

29 October 2026. Continuation6, existing physical-mechanism role. This is an
independently selected inverse-design construction, not another preparation
theorem. The strongest ordinary score estimator changes its scientific
disposition: the construction supplies a useful physical design and global
certificate, but does not establish a new exclusive physical operation or a
general speedup over model-free stochastic optimization.

## 1. Concrete task and actual interface

A stationary physical sensor has hidden microscopic state X and a bounded
noninvasive visible readout f(X), |f|<=1. There are m ACTUAL operations P_j,
each a Markov kernel reversible for the same probability law mu. State space
and hidden predictive rank may be infinite. No hidden coordinate, transition
matrix, microscopic clone, or conditional future from a copied state is
available. The common invariant law and reversal property are supplied
physical premises, not inferred from a short readout record.

Each native operation is a complete round of the same actual duration tau.
If sensing or switching occupies time, its actual action and latency must be
included in that round. Equal call count is not equal elapsed time for a menu
with different durations; free padding or holding is not supplied by this
theorem. The fixed-kernel interface needs no hidden jump-rate ceiling.

The designer chooses w in the probability simplex and, at every round, draws
an independent operation label j with probability w_j. The implemented kernel
is P_w=sum_j w_j P_j. This is ordinary actual switching, not an arithmetic
mixture used only in a prediction. The native operation and selector record
may be retained. Calibration can prepare independent copies of mu, conditional
on the complete previous calibration record and the fixed device model.
Every such preparation has its real cost. Without that resource, a separate
serial-dependence or conditional-start theorem is needed.

The objective is the stationary noise of a prescribed exponentially smoothed
readout at the fixed round clock. Let 0<rho<1, q=1-rho, and

    Z_k = q sum_(r>=0) rho^r f(X_(k-r)).                (1)

The DC mean mu(f) is unchanged by every admissible w. The task is to choose w
to reduce Var(Z_k), retaining this same readout filter. It concerns stationary
sensing of a fixed parameter. Equality of DC means does not establish equal
gain or latency for a time-dependent external signal; that additional tracking
task would need its response constraint and calibration.

The dynamics are not accelerated by an uncharged global rate multiplier.
One native round is executed at each tau. Extra control-energy differences can
be represented by actual constraints on w, but are not numerically compared
here. The initial theorem uses the whole simplex.

## 2. Exact physical noise objective, without a mixing assumption

Define

    R_w=(I-rho P_w)^(-1),   S_w=q R_w,
    F(w)=q <f,R_w f>_mu=<f,S_w f>_mu.                 (2)

Self-adjoint contraction of P_w gives I-rho P_w>=q I. Therefore R_w exists
as a bounded operator even if microscopic memory never mixes. Since S_w is
the mixture sum_(n>=0) q rho^n P_w^n, it is an actual geometrically stopped
operation and a Markov contraction. In particular 0<=F(w)<=||f||_2^2<=1.

The stationary autocorrelation C_n=<f,P_w^n f> obeys |C_n|<=||f||_2^2.
Absolute summability of the filter weights justifies the double sum in (1):

    E Z_k^2 = [2 F(w)-q ||f||_2^2]/(1+rho),
    Var(Z_k) = [2 F(w)-q ||f||_2^2]/(1+rho)-mu(f)^2.  (3)

For a centered readout replace ||f||_2^2 by Var_mu(f), and replace F by the
centered response. The constant mu(f)^2 in the uncentered F has no effect on
the optimizing w. Thus an unknown mean need not first be estimated merely
to select the optimal design.

Equation (3) makes the discounted objective an exact finite-filter noise
consumer, not an assumed approximation to infinite-time autocorrelation.
There is no spectral-gap hypothesis. It does not imply that a finite-TV warm
start controls an infinite-time integral, or that a zero-frequency estimate
has been acquired. A common frozen sector can retain a nonzero noise floor.

## 3. Convexity and a global certificate

For a tangent direction d with sum_j d_j=0, put D=sum_j d_j P_j. Let the
perturbed weights remain in the simplex. Differentiating the bounded inverse,

    F'(w;d)=q rho <f,R_w D R_w f>,
    F''(w;d)=2q rho^2 <D R_w f,R_w D R_w f> >=0.       (4)

Hence F is convex on the entire simplex, including its boundary. This is the
ordinary convexity of an inverse positive affine operator. It is closely
related to convex effective-resistance and reversible mixing design; no
novelty is claimed for this operator fact.

One valid ambient gradient, from an open neighborhood where the inverse
remains positive, is

    g_j = q rho <f,R_w P_j R_w f>
        = c <f,S_w P_j S_w f>,    c=rho/q.             (5)

Only its tangent differences matter on the simplex. For any feasible w,

    0<=F(w)-min_v F(v)<=G(w),
    G(w)=sum_j w_j g_j-min_j g_j.                     (6)

This is the standard first-order convex / Frank-Wolfe gap: convexity gives
F(v)>=F(w)+g dot(v-w), then minimize that affine expression over v. Once
acquired with a confidence interval, G is an actual global design certificate
for this family, despite the absence of a microscopic model.

There is a simple dimension-free curvature bound. Since ||R_w||<=1/q,
||D||<=||d||_1, and ||f||_2<=1,

    F''(w;d)<=2 rho^2 ||d||_1^2/q^2.

Every simplex chord has ||d||_1<=2, so along it

    F(w+gamma d)<=F(w)+gamma g dot d+(C/2)gamma^2,
    C=8 rho^2/q^2.                                   (7)

Hidden dimension and native mixing gaps are absent from these constants.
The filter horizon is not absent: c and C diverge as rho tends to one.

## 4. A chronological intervention experiment acquires each derivative

At a currently chosen w:

1. Prepare a fresh warranted mu specimen and read f_0.
2. Draw independent N_1,N_2 with Pr(N_i=n)=q rho^n, n>=0.
3. Execute N_1 native rounds with independent selectors distributed as w.
4. Execute one actual P_j round.
5. Execute N_2 further native rounds with independent selectors as w.
6. Read f_end and return c f_0 f_end.

The expected endpoint product is exactly <f,S_w P_j S_w f>, so the returned
value is unbiased for g_j. Its magnitude is at most c, and the expected
native call count is

    E(N_1+1+N_2)=2c+1.                               (8)

There is one specimen moving chronologically through the whole experiment.
The two random word lengths are independent controller variables, not two
futures spawned from the same hidden state. Reversibility is what turns the
operator derivative into the positive quadratic form and convexity; the
chronological expectation in (5) itself is an ordinary kernel-product identity.
No microscopic adjoint operation or reversal of a realized path is invoked.

N_i=0 means no prefix rounds; it does not assume an available physical hold or
identity intervention of duration tau. The forced middle round is always
executed. Exact geometric sampling is almost surely finite but has no hard
deadline. Its expected duration and random-bit cost remain paid. A bounded
clock implementation would need to debit its tail/truncation bias.

Unlike an on-policy score estimate, this experiment is defined at w_j=0.
It intentionally tests a feasible intervention absent from the current design.
This is ordinary weak-derivative / intervention sampling. Section 7 and the
separate comparator note show why it is not generally statistically superior.

## 5. A finite acquired global certificate and terminating design algorithm

Suppose n independent trials are taken for each j at a data-selected w, with
fresh conditional baseline preparation as in Section 1. Conditional Hoeffding
and a union bound give

    Pr(max_j |g_hat_j-g_j|>xi) <= beta

whenever

    n >= 2 c^2 log(2m/beta)/xi^2.                     (9)

Consequently, with that confidence,

    F(w)-F_* <= G_hat(w)+2xi,
    G_hat(w)=sum_j w_j g_hat_j-min_j g_hat_j.          (10)

The interval bounds a fixed underlying response objective on the good
calibration event. It is not a posterior claim for every observed transcript,
and conditioning on a rare selected transcript is not justified by beta.

For completeness, a conservative terminating optimizer can use xi=epsilon/8,
per-round beta_r=6 beta/[pi^2(r+1)^2], and fresh data each round. If
G_hat+2xi<=epsilon, stop. Otherwise choose s=e_argmin(g_hat) and update

    w <- (1-gamma)w+gamma s,
    gamma=min(1,epsilon/(4C)).                        (11)

On the simultaneous confidence event, a nonstopping round has G>epsilon/2.
The selected direction has true descent at least G-2xi>epsilon/4. Equation
(7) then gives decrease at least epsilon^2/(32C) when gamma<1, or epsilon/8
when gamma=1. Since 0<=F<=1, there can be fewer than

    max(32C/epsilon^2,8/epsilon)+1                    (12)

nonstopping rounds. The union confidence is at least 1-beta. Its final
stationary filtered-noise regret is at most 2epsilon/(1+rho), by (3).

The bounds are deliberately conservative existence budgets. A practical
optimizer can use ordinary stochastic gradients, bisection for two controls,
or line searches, and then acquire an independent certificate (10). The
validation guarantee does not require trusting the pilot optimizer.

The explicit per-round costs are m n baseline preparations, 2m n endpoint
readings, expected m n(2c+1) native calls, the same number of selector/control
rounds up to the forced interventions, and their clocks, bits and storage.
Physical output precision, source drift, baseline error and actuator mismatch
need actual budgets. For example a uniform conditional baseline TV error zeta
can bias each gradient observation mean by at most 2c zeta, which must be added
to xi before applying (10). Assumed population preparation is not a measured
end-to-end precision certificate.

## 6. Retained records and deployment

The experiment retains calibration data, controller selectors, random lengths,
and the chosen w. This poses no erased-key issue: their action probabilities
are part of the likelihood and experiment, not hidden to create an averaged
deployment channel. The mathematical objective is the actual randomly
scheduled physical system, averaged over the future selectors.

The fresh baseline premise is conditional on the complete old record D.
Thus data-selected w is fixed conditional on D, and the next experiment has
the stated expectation. After selecting w, deployment starts from the same
actual conditional baseline if the stationary consumer (3) is requested.
Leaving the old physical specimen in an uncharacterized conditional state
does not supply that stationarity. It can instead be deployed with a separately
proved preparation/mixing budget, but no such budget is imported automatically.

The statement controls a stationary second moment / response. It does not
compare complete future records to a different kernel, does not certify every
record-conditioned fluctuation, and does not provide target tracking under an
arbitrary time-dependent environment. The complete decision/measurement clock
and equilibrium law remain part of the physical specification.

## 7. Strong ordinary route: selector scores already give exact derivatives

Run a single geometric word of length N with mean c under P_w, record action
counts N_j, and read Y=f_0 f_end. For w_j>0 define

    S_j=N_j/w_j-N.

The ordinary likelihood-ratio identity gives

    E[Y S_j] = g_j-sum_k w_k g_k.                    (13)

To prove it, differentiate the probability of each controller word in tangent
direction e_j-w. The unknown physical conditional law given that word is
independent of w. Its score is exactly N_j/w_j-N. Termwise differentiation is
valid because the geometric word has finite mean and second moment and Y is
bounded. No hidden transition probabilities are evaluated or estimated.

The action count noise has the exact covariance

    E[S_j S_k]=c[1_(j=k)/w_j-1].                      (14)

Given N, selector indicators are iid and the scores have mean zero; (14)
follows from their multinomial covariance and E N=c. In particular the
variance of Y S_j is at most c(1/w_j-1), while one trajectory costs c expected
native calls and estimates all tangent coordinates simultaneously.

For two controls use S=N_1/w-N_2/(1-w). Then

    E[Y S]=dF/dw,   E[S^2]=c/[w(1-w)].                (15)

An independently acquired reward baseline b gives the unbiased estimator
(Y-b)S. These are familiar REINFORCE / likelihood-ratio methods. In the
interior they can beat the forced-sandwich estimator by a horizon factor;
the numerical comparison includes this stronger baseline-corrected route.
The sandwich's bounded observations and defined boundary behavior are real
advantages, but do not create exclusive access to a gradient. An ordinary
optimizer may combine score sampling with forced exploration at the boundary.

## 8. Failures that change the claim

**Nonreversible menus lose the convex global certificate.** Let P_1 be a
deterministic rotation on a three-cycle, P_2 its inverse, and let f be a real
mean-zero unit vector in their two-dimensional rotation sector. Both preserve
uniform mu. Direct inversion gives

    F(w)=q(1+rho/2) /
       [(1+rho/2)^2+3rho^2(2w-1)^2/4].                (16)

It has a strict maximum at w=1/2, not a minimum. Stationary common law alone
does not make inverse-response design convex. Score identities remain true,
but a small first-order gap no longer certifies a global optimum.

**Different native durations change the physical problem.** A call-level
stationary law and response do not automatically describe fixed physical-time
occupation or fixed-clock readout when durations depend on the action. The
equal-duration premise or an actual accounted physical compiler is essential.

**No uniform zero-frequency conclusion follows.** A rare hidden sector of
mass delta carrying visible decay rate epsilon contributes at most delta to
a normalized discounted response, but order delta/epsilon to the undiscounted
integrated response. Finite discounted-data accuracy does not bound that
quantity without a spectral-tail/integrability contract. Optimizing a filter
of successively larger horizon has real acquisition and execution costs.

**One frozen specimen cannot reveal an ensemble of frozen specimens.** If the
hidden class never changes and preparation only redraws the visible bit within
that same class, repeated trials estimate the class-conditional objective.
They do not acquire an unknown mixture over classes. An ensemble-level design
requires its actual baseline/replacement supplier or separately supplied
class weights. The theorem never pays for that resource with retained bits.

**Uniform sampling is a strong comparator.** A hidden gate can make either
individual operation poor while their mixture is good. That observation alone
does not demonstrate a benefit from optimizing the mixture; uniform random
scan can already capture most of the improvement. The checks retain this
baseline alongside the optimized design and the score route.

## 9. Scientific disposition

The constructive result is an acquired global design certificate for an exact
stationary sensing-noise objective, using only visible endpoints and actual
operation selectors on an unknown reversible physical source. No hidden-state
model or finite predictive closure is necessary. This is a useful capability
at the declared information interface.

However, convex inverse design, effective-resistance optimization, random-scan
adaptation and score/weak-derivative gradient acquisition are substantial
predecessors. The strongest ordinary route already has the needed derivative
access. The scoped combination here is not established as a new physical
principle, and no generic computational or experimental advantage is claimed.
The remaining opportunity would have to improve the actual actuator, sensing,
variance, baseline, or task class beyond these ordinary methods; an operator
identity alone does not do so.

Primary sources, exact score comparisons, executable acquisition and their
limits are preserved in the adjacent files. No older continuation is amended.
