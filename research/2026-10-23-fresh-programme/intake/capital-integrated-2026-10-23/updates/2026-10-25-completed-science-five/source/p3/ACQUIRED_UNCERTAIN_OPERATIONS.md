# Acquired operations from uncertain response histories

New construction, 25 October 2026. This extends the retained exact relation work
in `ACQUIRED_INVERSE_RELATIONS.md`; it does not replace that proof or describe
unavailable historical scripts as recovered. The implementation is
`certified_response_instrument.py`, `acquired_uncertain_operations.py`,
`acquired_uncertainty_witnesses.py`, `acquired_uncertain_comparisons.py` and
`certified_precision_design.py`. Each has its corresponding retained JSON
calculation output. Prior proofs and working versions remain unchanged.

## 1. The operation being acquired

The learner receives full forward responses of a fixed linear scientific
software model, together with rigorously obtained numerical error enclosures.
It proposes an approximate inverse balance operator B, obtains a uniform
bound on its defect R = B H - I, and retains every response and its uncertainty.
A later task specifies a linear functional <W,H>, without providing its answer.
The retained object then constructs an answer interval, an executable linear
estimator using the history, and an unresolved task coefficient that proposes
further experiments. A floating optimizer can search for these procedures;
an independent rational calculation checks their error bounds.

This changes the interface of the preceding exact construction. Finite noisy
data do not establish exact missing couplings or exact learned identities.
Instead the acquired semantics are a set of compatible operators and a
task-specific executable certificate. The source's exact hidden matrix need
not be reconstructed to ask a new response question. Conversely, when its
source code is available to an incumbent, direct use of that code is legitimate
and can be much cheaper than acquisition.

The mathematical ingredients have substantial precedents in optimal recovery,
duality, matrix approximation, residual error estimation and active experiment
design. The candidate contribution is the obtaining and compilation chain, not
an invention of those fields, a general intelligence result, or an architecture
that conventional software cannot adopt.

## 2. Obtaining a bounded-error numerical response instrument

Assume supplied rational source coefficients define A with positive strict row
diagonal-dominance margin

    mu = min_i (|A_ii| - sum_{j != i}|A_ij|) > 0.

The executable checks this condition. Given a forcing f and a floating solver
proposal y, convert the finitely represented y to exact rational values and
compute the exact residual r = f - A y. The instrument returns

    ||H f - y||_infinity <= ||r||_infinity / mu,       H = A^{-1}.

Proof: for e = Hf-y, take an index attaining |e_i| = ||e||_infinity. Then
| (Ae)_i | >= (|A_ii| - sum_{j != i}|A_ij|)||e||_infinity.
Thus ||Ae||_infinity >= mu||e||_infinity. The same inequality proves A is
injective, hence invertible in the finite square case. This proof does not
depend on floating convergence or the correctness of a floating stopping test.

The current instrument uses Gauss-Seidel only to propose y. It includes all
exact residual arithmetic and solver sweeps in the cost. It checks whether a
requested tolerance was actually achieved, and returns its honest enclosure
even if the iteration or floating precision limit prevents that tolerance.

This is an obtained interface for auditable *software*. The checked source
coefficients are available to the instrument, although not to the forward-only
learner. No experiment here calibrates an unknown physical apparatus, discovers
linearity, or establishes that a real system is time invariant. An incumbent
with source-code access may use A directly, including its transpose. A different
physical or numerical source would need its own justified response contract.

## 3. Learning an approximate law and certifying it once

The retained support of an earlier source proposes which coefficients of B to
fit. Six new, bounded random full-vector responses give a least-squares proposal;
the fitted coefficients are rounded to explicit dyadic rationals. Neither
numerical rank nor a fitted zero is an exact structural certificate. B is
checked invertible by exact elimination.

Freeze B before drawing independent calibration inputs. For each calibration
response y_j with coordinate enclosure delta_j, the true defect action obeys

    ||(BH-I)f_j||_2
      <= ||B y_j-f_j||_2 + delta_j || |B| 1 ||_2.

Both norms on the right are enclosed upward using rational arithmetic. For
independent grid-uniform f_j in the cube [-1,1]^n, the previous cube-slicing
argument gives, for tau > 0,

    rho = max_j (certified defect-action norm)/tau,
    P(||BH-I||_2 > rho)
      <= min(1, (3/2)(tau + ceil(sqrt(n))/M))^t.

Here M is the number of equally spaced coordinates per axis and t the number
of fresh probes. The anti-concentration bound follows by projecting onto a
maximal right singular direction, coupling a continuous uniform cube to the
finite grid, and using Ball's cube-slicing density bound. The conservative
constant 3/2 exceeds sqrt(2). Numerical errors may be deterministic, correlated
or state-dependent; their individual enclosures, not independence, justify the
calibration. Linearity and a fixed underlying H remain substantive premises.

One event ||R||_2 <= rho covers all subsequently selected tasks, multipliers,
queries, stopping times and procedure searches on this same H. Reuse does not
consume a fresh probability allowance per task. Refitting B or changing H needs
a valid new calibration argument; selecting among separately calibrated models
needs the appropriate joint failure accounting. The two executed source cases
each have failure bound about 1.5384e-7; their joint bound is their sum.

## 4. A sharp error-versus-query result for one specified information class

Let R be an unknown real m by n matrix with ||R||_2 <= rho. A query chooses
||x||_2 <= 1 and observes the *whole vector*

    y = R x + e,                  ||e||_2 <= eta.

Errors are arbitrary bounded errors. They need not be independent, random or
unbiased. The target is the scalar <M,R>_F. Let sigma_1 >= sigma_2 >= ... be
the singular values of M, with zeros appended as needed. For a deterministic
algorithm allowed k adaptive queries, the exact minimax absolute error is

    E_k = rho sum_{i>k} sigma_i
              + min(eta,rho) sum_{i<=k} sigma_i.                 (1)

### Constructive upper bound

When eta < rho, write M = sum_i sigma_i u_i v_i^T. Query v_1,...,v_k and
return sum_{i<=k} sigma_i u_i^T y_i. The observed-direction error is bounded
by eta sum_{i<=k}sigma_i. The unobserved term is at most
rho ||sum_{i>k}sigma_i u_i v_i^T||_* = rho sum_{i>k}sigma_i, by duality
between spectral and nuclear norms. When eta >= rho, ignore the queries and
return zero; its worst-case error is rho||M||_*.

### Adaptive full-vector lower bound

Follow an arbitrary deterministic adaptive algorithm on the transcript in
which all reported vectors are zero. Let P be the orthogonal projector onto
the span of its at most k query vectors. Write M = U|M| with U a polar partial
isometry. For eta <= rho, define

    R_plus/minus = +/- U[eta P + rho(I-P)].

Both have spectral norm at most rho. On every queried x in range(P), their
response norm is at most eta, so bounded errors can produce precisely that
same entire zero transcript. Their target values are opposite, with magnitude

    rho tr|M| - (rho-eta)tr(|M| P)
      >= rho sum_{i>k}sigma_i + eta sum_{i<=k}sigma_i.

The last inequality follows because a rank-at-most-k orthogonal projector
captures at most the k largest eigenvalues of |M|. At least one of the two
indistinguishable operators therefore has error at least (1). If eta >= rho,
use R_plus/minus = +/- rho U; every unit query can again be masked. This
proves (1), including vector observations and adaptivity.

### What this theorem does and does not establish

Each useful direction is worth (rho-eta)sigma_i, and fixed instrumental error
creates a floor eta||M||_* even after all relevant directions have been queried.
Repeated measurements cannot remove that worst-case floor because their errors
may be systematic. If eta >= rho, additional measurements at that precision
cannot improve this worst-case guarantee. Better precision, a better acquired
model, or a stronger justified model class is then necessary.

The input-energy budget is essential. With unlimited input amplitude and a
fixed absolute error bound, querying a*x and dividing by a reduces the error
to eta/a. Equation (1) is not a lower bound for that unrestricted interface.
It is also not a randomized-query lower bound or a stochastic-noise theorem.
Prior historical constraints, positivity, locality and other legitimate
structural knowledge can reduce the operator class and invalidate an attempt
to use (1) as its exact minimax value. In the actual construction below, all
past observations are retained and used; (1) is a design principle for the
residual ball, not a claim that those observations are uninformative.

## 5. Compiling the complete uncertain history into a task evaluator

Let L = B^{-1}, R = BH-I, and H = L(I+R). Let F contain *all* previous input
columns, Y their response centers, and delta_j their coordinatewise error bounds.
Thus Y = H F + E, |E_ij| <= delta_j. Define

    C = B Y - F = R F + B E,
    M = B^{-T} W,
    nominal = <W,L> = tr(M).

For any matrix U with one column per past response, decompose

    <W,H> = nominal + <U,C> + <M-U F^T,R> - <B^T U,E>.

Consequently every U gives the rigorous upper certificate

    upper(W,U) = nominal + <U,C>
                 + rho ||M-U F^T||_*
                 + sum_j delta_j ||(B^T U)_j||_1.               (2)

A second application to -W gives a lower bound. This identity preserves the
coupling through the same unknown H and R; no history column is treated as an
independent unknown model. Correlated, adversarial errors remain allowed.

The compatible set is

    K = {H: ||BH-I||_2 <= rho,
                |(HF-Y)_ij| <= delta_j for every i,j}.

Taking the infimum of (2) over U is the convex dual of the support function
sup_{H in K}<W,H>. Under strict feasibility in the relative affine domain,
finite-dimensional convex duality gives equality. If this condition is not
established, every concrete U remains a valid upper bound; the implementation
does not claim that its finite optimizer run attained the support function.
The interval midpoint is a usable estimator even when optimization is incomplete.

### Search and proof have different roles

The implementation searches (2) with two-block ADMM. Its separable first block
contains X = M-UF^T and S = B^T U; singular-value thresholding updates X,
coordinate soft thresholding updates S, and a Sylvester equation updates U.
All of that numerical computation proposes a multiplier. The result is rounded
to explicit rational entries before verification. Failed optimization can
produce a weaker bound, but cannot turn an invalid inequality into a valid one.

The nuclear norm is certified without trusting floating singular values. A
floating SVD proposes dyadic P,Q; exact arithmetic checks

    ||A||_* <= (||P||_F^2+||Q||_F^2)/2
                   + sqrt(min(m,n)) ||A-PQ^T||_F.               (3)

Indeed ||PQ^T||_* <= ||P||_F||Q||_F <= (||P||_F^2+||Q||_F^2)/2, while
||A-PQ^T||_* <= sqrt(min(m,n))||A-PQ^T||_F. Every square root is enclosed
upward. The actual factors, residual bound, multipliers and rational answer
interval are retained, rather than only a numerical execution report.

### Generating new experiments and procedures

The unresolved coefficient M-UF^T is the part of the task that the chosen
historical estimator has not represented. Its dominant numerical right
singular vector proposes a new forcing. A dyadic rational approximation is
normalized with an exact upper norm enclosure, ensuring ||f||_2 <= 1. The
new response and its *actual* enclosure join the common history, and a new
estimator is searched and certified. Appending zero multipliers reproduces
any earlier certificate, so failed numerical search cannot make the retained
interval worse.

This residual-directed experiment selector is a heuristic for the full set K.
The exact minimax theorem for the unrestricted ball is not silently promoted
to a theorem of optimal adaptive design under arbitrary previous boxes. What
is guaranteed is correctness of each acquired procedure's resulting interval,
not global optimality of the search or experiment choice.

## 6. Comparators and claim boundary

Ettehad and Foucart's computational optimal recovery explicitly handles
bounded inaccurate data, compatible model sets, locally optimal recovery and
computable convex programs. The historical support-function calculation here
belongs to that tradition. Foucart and Hengartner also study worst-case
learning under multiple fidelities. It would be incorrect to present noisy
set-valued inference or error/cost tradeoffs as new principles in themselves.

Hutchinson and Hutch++ provide important stochastic trace-estimation alternatives.
Hutch++ uses a low-rank approximation to reduce variance and has strong query
guarantees, primarily for PSD matrices, with extensions for general matrices.
Those algorithms may use the same retained B, all historical responses and a
control-variate residual. The present source is not assumed reciprocal or PSD.
Deterministic bounded-error intervals and high-probability randomized trace
estimates answer different information contracts; neither is an automatic
dominance claim over the other.

XTrace is an especially pertinent stronger comparator: it uses variance
reduction and exchangeability to reuse its samples. It is not legitimate to
define our advantage as retaining information that these methods must discard.
No Hutch++, XTrace or randomized dynamic-trace runtime experiment was performed
in this continuation, so there is no empirical superiority claim over them.
Plaskota and Siedlecki explicitly study noisy linear information whose cost
depends on chosen precision; precision allocation itself is established
information-based complexity. The full-vector, spectral-ball calculation in
section 8 is the particular theorem proved here, without a claim that every
aspect of that specialization is new in the literature.

Strong structured algebra and retained-model methods can use the same B and
exact elimination. A conventional optimal-recovery program can adopt (2),
including all correlations and all saved certificates, and tie this compiler.
A full-source method can use A, solve the task directly, and avoid acquisition.
AlphaEvolve and other program-search systems may use the resulting evaluator,
but the search mechanism here is not an LLM evolutionary program search and no
universal procedure-invention or physical-discovery claim follows.

The surviving capability is narrower and operational: available forward
software interactions can acquire reusable approximate semantics, an obtained
error contract and a compiler that turns a later scientific linear query into
a certified estimator and further experiments. Exact hidden matrix recovery,
exact identity testing and a supplied task answer are not prerequisites.

## Primary sources

- M. Ettehad and S. Foucart, *Instances of Computational Optimal Recovery:
  Dealing with Observation Errors*, SIAM/ASA J. Uncertainty Quantification
  9(4), 1438-1456 (2021), authors' full text:
  https://foucart.github.io/publi/OR_Uncertainty_v2.pdf
- S. Foucart and N. Hengartner, *Worst-case learning under a multi-fidelity
  model*, SIAM/ASA J. Uncertainty Quantification 13(1), 171-194 (2025):
  https://foucart.github.io/publi/Multifidelity_v3.pdf
- R. A. Meyer, C. Musco, C. Musco and D. P. Woodruff, *Hutch++: Optimal
  Stochastic Trace Estimation* (SOSA 2021):
  https://arxiv.org/html/2010.09649v5
- J. Melbourne and C. Roberto, *Quantitative form of Ball's cube slicing in R^n*
  (2021), a primary source restating the cube-section bound used above:
  https://arxiv.org/pdf/2109.03946
- AlphaEvolve technical report, supplied comparison source:
  https://arxiv.org/html/2506.13131v1
- E. N. Epperly, J. A. Tropp and R. J. Webber, *XTrace: Making the Most of Every
  Sample in Stochastic Trace Estimation*, SIAM J. Matrix Analysis and
  Applications 45(1), 1-23 (2024):
  https://tropp.caltech.edu/papers/ETW24-XTrace-Making-SIMAX.pdf
- L. Plaskota and P. Siedlecki, *Worst case tractability of linear problems in
  the presence of noise: linear information*, J. Complexity 79, 101782 (2023):
  https://arxiv.org/abs/2303.16328
  The primary abstract and publisher introduction were accessible. Direct
  publisher, arXiv PDF and HTML full-text fetches were blocked in this session;
  the comparison does not claim a complete theorem-by-theorem novelty audit.
- A. Carpentier, J. Eisert, D. Gross and R. Nickl, *Uncertainty Quantification
  for Matrix Compressed Sensing and Quantum Tomography Problems*:
  https://arxiv.org/abs/1504.03234
  This is an additional antecedent for adaptive sampling driven by confidence
  sets, not evidence that such a general strategy originated here.

## 7. Acquiring negative answers: explicit information obstructions

An optimizer's failure to achieve a requested radius does not by itself prove
that the evidence is insufficient. It could simply be a poor optimization
run. The second constructor therefore builds *two concrete compatible
operators* with distinguishable task answers.

First propose R0 = C F^dagger numerically, round its entries to rationals, and
check the following facts exactly:

1. r0 >= ||R0||_F and r0 < rho;
2. H0 = B^{-1}(I+R0) lies within every retained observation box.

Next obtain an exact right nullspace basis of F^T. From this basis construct a
rational frame V with V^T F = 0 exactly. Numerical QR and SVD propose a
well-conditioned frame and a left factor J aligned with the unresolved task.
No numerical zero is accepted as an exact annihilation claim.

For an r-column frame X, an exact operator-norm upper bound is

    q_X = sqrt_up(1 + ||X^T X-I_r||_F,up).

Indeed lambda_max(X^T X) <= 1 + ||X^T X-I||_2 <= 1 + ||X^T X-I||_F.
Set d = q_J q_V and a = (rho-r0)/d. Then

    R_plus/minus = R0 +/- a J V^T,
    H_plus/minus = B^{-1}(I+R_plus/minus)                         (4)

both obey ||R_plus/minus||_2 <= rho and produce the same full response H0 F
on every historical forcing. They therefore fit all of the same boxes. Their
task half-separation

    a |<M,J V^T>|

is a lower bound on the best absolute error any estimator can guarantee from
this retained information. This is a negative certificate obtained without
the true H, without a task answer oracle, and without restricting an incumbent
to a particular algorithm or compute budget.

The scope is exactly K from section 5. An additional sign constraint, known
conservation law, source-code access, or a known physical model family can
exclude these alternatives. No lower bound against those stronger classes is
claimed. The constructor can also fail: a proposed center may be infeasible,
the spectral ball may have no certified slack, or F may have no nullspace.
It reports that failure rather than treating absence of a witness as uniqueness.
In particular, full input rank leaves bounded-noise ambiguity that this
nullspace-based witness constructor does not exhaust.

In particular, the alternatives were not shown to retain the synthetic
source's path topology, nonnegative transport interpretation, or exact
diagonal-dominance/contraction constants. The impossibility statement is for
the retained norm-and-box description, not for every fact an informed scientist
could legitimately extract from the supplied source.

### A witness can obtain an experiment

For a proposed new unit forcing x, compute the two predicted full responses
under (4). If their infinity-norm separation is d_x, any new reporting box
with coordinate error strictly below d_x/2 cannot admit both alternatives.
The executor proposes x using a leading right singular vector of
B^{-1} J V^T and rationally normalizes it. This operation requires no native
transpose or hidden physical projection. It may exclude one or both exhibited
alternatives; it does not guarantee a fixed reduction of the entire set K.

The ability to produce such witnesses is useful to a search process: it
distinguishes improving an algorithm on existing information from needing a
new information intervention. Counterexample-guided refinement and optimal
recovery are antecedents; the object here is acquired from the supplied
forward interface and retained uncertainty, rather than a supplied exact
target answer.

## 8. Precision-dependent information widths

The fixed-eta theorem in section 4 extends to queries with individually chosen
precision. Suppose a query with accuracy eta has a declared cost c(eta), and
still returns Rx+e with ||x||_2 <= 1 and ||e||_2 <= eta. For a fixed multiset of
k accuracies, cap each at rho and sort:

    0 <= eta_(1) <= ... <= eta_(k) <= rho.

The sharp deterministic minimax error is

    E(M; eta_1,...,eta_k)
       = sum_{i=1}^k eta_(i) sigma_i(M)
                           + rho sum_{i>k} sigma_i(M).          (5)

The most accurate measurements should be paired with the largest singular
directions. The constructive upper bound queries those directions and uses
the truncated singular expansion. The error estimate is the same calculation
as section 4 with a separate eta_i for each direction.

For the lower bound, follow the zero transcript and sort its actual queries by
their chosen accuracies. Let P_i project onto the span of the first i queries
in that sorted order, with P_0=0 and eta_(k+1)=rho. Define the positive operator

    D = sum_{i=1}^k eta_(i)(P_i-P_{i-1}) + rho(I-P_k)
      = rho I - sum_{i=1}^k (eta_(i+1)-eta_(i))P_i.

Its norm is at most rho. On query i, which belongs to range(P_i), ||D x_i||
is at most eta_(i)||x_i||. The alternatives R_plus/minus = +/- U D, where
M=U|M|, are therefore indistinguishable under the stated error budgets. Their
task half-separation is

    rho tr|M| - sum_i (eta_(i+1)-eta_(i)) tr(|M| P_i)
      >= rho tr|M| - sum_i (eta_(i+1)-eta_(i))sum_{j<=i}sigma_j,

which telescopes to (5). This argument handles adaptively chosen directions
and precisions: the zero transcript determines one admissible choice under
the algorithm's worst-case budget. Minimizing (5) over admissible menus gives
the optimal worst-case error for this *declared contract*.

The actual source may have further exploitable numerical structure, and K
also includes historical constraints. Thus (5) is not automatically the
globally optimal policy for the complete experimental situation. It supplies
an exact organizing result for the residual-ball information class; the
executable below uses a verified finite family of procedures on the whole
history, with its own stated optimization objective.

## 9. Obtaining the accuracy/cost interface instead of assuming it

The original floating solver supplied honest error enclosures after execution,
but its observed convergence times did not justify a uniform cost promise
for a new forcing. A second instrument now obtains such a promise directly
from the checked source software.

Let

    alpha = max_i sum_{j != i}|A_ij|/|A_ii| < 1.

Run Jacobi iteration from zero, rounding every new state coordinate to the
nearest multiple of 2^{-p} with exact rational/integer arithmetic. Let
epsilon_round = 2^{-p-1}. For every ||f||_infinity <= 1,

    ||H f-y_t||_infinity
      <= alpha^t/mu + epsilon_round/(1-alpha) = E_t.             (6)

Proof: the Jacobi update contracts infinity-norm error by at most alpha, while
the checked rounding adds at most epsilon_round. Iterate this recurrence from
||Hf||_infinity <= 1/mu. The bound retains a real rounding floor and therefore
does not promise arbitrary accuracy at fixed p. The code encloses alpha^t
upward by fixed-denominator dyadic exponentiation, avoiding denominator growth
in the bound calculation. It also computes an exact final residual and returns
the smaller of the two justified error enclosures.

For the acquired residual action R x, set g = || |B|1 ||_2, enclosed upward.
Then eta(t)=g E_t is a uniform residual-response error bound. Binary search
obtains the smallest t in this bound that meets each predeclared accuracy ratio
of rho. This search uses checked source coefficients through the instrument's
contract, not favorable response samples or hidden task answers.

Each source here has n=32 and 62 off-diagonal entries. The implemented sweep
uses 188 Fraction arithmetic calls plus 32 integer quantizations. A nonzero
final response uses at most 221 Fraction calls for the residual certificate;
power-bound arithmetic is additional and counted by the executor. State
precision is fixed at p=40, and actual intermediate bit lengths are retained.
The optimization objective is source sweeps. This is not an optimal wall-time
claim, and integer, rational, query overhead and local synthesis costs are not
silently counted as free.

### A checked finite procedure search

Start with the same inexpensive retained projection that performed almost as
well as ADMM. Its historical estimator leaves a rational task remainder A.
A floating SVD proposes a rational rank-one decomposition

    A = sum_i a_i q_i^T + E,            ||q_i||_2 <= 1.

Its actual reconstruction residual is enclosed exactly. For a chosen subset
of terms and a precision menu assignment t_i, the procedure adds a_i^T times
the newly measured R q_i to the historical estimator. Its certified error is

    historical_noise + rho ||E||_*
       + sum_queried eta(t_i)||a_i||_2
       + sum_unqueried rho||a_i||_2.                            (7)

This formula is valid even if the numerical SVD was poor or its factors are
not orthogonal. All returned factors, query vectors and coefficients are
explicit rationals. Dynamic programming optimizes the positive bound (7)
exactly over the supplied discrete menu and a stated sweep budget. It selects
the least sweep cost reaching the predeclared target, or the largest bound
improvement within budget when the target cannot be reached. This finite
family's optimum is distinct from the ideal minimax theorem (5), and both are
distinct from global optimality under arbitrary historical correlations.

Eight independent exhaustive enumerations on a diagonal known-answer control
matched the dynamic program's exact optimum. The scientific-source execution
uses the same acquired history, including the separating experiment, rather
than restarting from an empty model to exaggerate its gain.

## 10. Executed scientific-software workload and findings

The supplied sources are two 32-channel nonreciprocal transport/balance
operators with damping mu=1 and mu=1/100, chosen before the outcomes. They
share the previously acquired support but have new fitted coefficients. Both
retain all vector outputs and signed software inputs. Their construction has
A=mu I-Q for a finite-state Markov generator Q, so

    H = (mu I-Q)^{-1} = integral_0^infinity exp(-mu t)exp(Qt) dt.

Thus tr(H)/n is the mean discounted return response, and also the derivative
with respect to uniform damping of log(det(A))/n. A signed diagonal weighted
trace measures a contrast in local response sensitivities. The determinant
identity is a mathematical consequence of the supplied linear source, not an
inferred physical intervention law. The exact matrix coefficients, damping,
linearity and software actuation are supplied assumptions. There is no
physical parameter acquisition or biological evidence in these controls.

### Acquisition

Both cases use six approximate fitting queries followed by sixteen fresh
calibration queries: 22 full responses of width 32, or 704 returned scalars.
The earlier support acquisition is prior exposure, not a free discovery: its
retained source reports nine forward calls and a substantial combinatorial
support search. An equally informed retaining learner receives that support
and history too.

| Quantity | mu=1 | mu=1/100 |
|---|---:|---:|
| Acquired rho | 0.00368360258 | 0.00231891632 |
| Initial solver sweeps over 22 calls | 169 | 6,885 |
| Maximum observed local fit condition | 14.992 | 193.686 |
| Maximum true response error, separate exact control | 3.043e-5 | 8.770e-6 |
| Calibration failure bound, each fixed source | 1.538313e-7 | 1.538313e-7 |

All requested initial enclosures were achieved and separately checked against
the exact source. The weakly damped case costs roughly 41 times as many sweeps,
despite its smaller acquired residual norm. The sensitivity of a task also
depends on B^{-T}W; rho alone does not measure its difficulty.
Exact source identity was also checked between the retained calibration rows
and both numerical instruments. After all operation phases, every coordinate
of the ten new response vectors per source was separately checked against the
exact supplied operator; all ten enclosures held in each case.

### The first search fails its target for an identifiable reason

The initial task policy allows four new unit-energy experiments per task, with
requested response accuracy 1e-8 and an absolute task target 1e-4. The second
task receives the first task's four new full responses. Every reported interval
contains the separately computed reference, but none initially meets target.

| Source and task | Achieved certified radius | Compatible-pair lower radius |
|---|---:|---:|
| mu=1, mean local response | 3.997047e-4 | 3.371816e-4 |
| mu=1, response contrast | 1.710256e-4 | 1.187861e-4 |
| mu=1/100, mean local response | 1.012316e-3 | 9.233595e-4 |
| mu=1/100, response contrast | 4.698882e-4 | 3.815370e-4 |

Every lower radius exceeds 1e-4. Within K, unlimited additional computation on
that same record cannot meet the requested guarantee. The result does not
depend on assuming an incumbent forgets any vector coordinate or correlation.
The witness constructors used about 135,000-140,000 rational arithmetic calls
per case/task, with exact nullspace entries reaching 565 bits and perturbation
entries reaching 652 bits. These are finite executable objects, not compact
constant-width or dimension-independent representations.

### Search itself was not the advance

A conventional retained projection with one pseudoinverse gives almost the
same certified answer. Its radii differ from ADMM by only about 6.24e-8 and
5.77e-8 on the two mean-response tasks, and are exactly equal on both contrasts.
The original search performed 32,000 ADMM iterations and 32,820 floating SVDs
per source case. Its endpoint verification across the ten stages uses about
2.71 million Fraction arithmetic calls per source. This is a substantial cost
for negligible benefit in these examples. Later construction therefore uses
the cheaper projection. Optimization is useful as a valid search interface,
but this particular expensive optimizer does not establish useful algorithm
invention or a practical advantage.

A stronger-access source-code incumbent obtains the path ordering from A and
computes its exact inverse diagonal by conventional selected inversion in 249
Fraction arithmetic calls, then answers both diagonal-weight tasks without a
forward response query. This source-aware calculation is explicitly allowed.
It prevents any claim that hiding supplied source code creates a real scientific
advantage.

### Acquired ambiguity produces a real information intervention

One witness-generated unit-energy experiment per source separates the final
contrast alternatives by 0.00218578 and 0.01087868 in output infinity norm.
The achieved coordinate enclosures are respectively 2.608e-9 and 4.800e-9.
Both exhibited alternatives are excluded in both executions. The full-set
radii shrink to 1.120511e-4 and 2.312198e-4, which still miss target. Eliminating
two explanations is not silently treated as identifying the source or shrinking
the full uncertainty set enough.

### An obtained precision plan completes the requested operation

The checked Jacobi contraction constants are 365/596 and 36500/36731. The
same relative-accuracy menu leads to sweep counts

    mu=1:     18, 21, 23, 26;
    mu=1/100: 2126, 2300, 2520, 2740.

These are certified uniform costs from (6), not fitted times. The generated
plan uses one new response in each source, at 18 and 2520 sweeps respectively.
Its pre-execution guarantees are 9.080815e-5 and 9.679562e-5, both below 1e-4.
After execution, the tighter actual residual certificates give radii
4.645193e-5 and 8.786572e-5. Exact-source checks give actual center errors
1.668e-7 and 2.017e-7, but those reference values were not supplied to planning
or certification.

The new exact quantized executions cost 3,616 and 474,003 Fraction arithmetic
calls, plus 576 and 80,640 integer quantizations. State entries reach 41 and
43 bits; intermediate rational values reach 112 and 117 bits. The exact menu
allocation performs 900 transitions in each case. The weak case's much larger
cost is retained as a limitation. The uniform Jacobi cost promise is also
conservative relative to the observed floating Gauss-Seidel executor; it is
not an assertion that Jacobi is the best available solver.

### Actual transfer, and the retaining-method tie

After completion there are 32 retained full-response columns. A genuinely new
off-diagonal task asks for the mean response between channels paired by the
previously unused permutation j=(i+7) mod 32. It is evaluated with zero new
source queries, giving certified radii 4.642727e-5 and 8.786570e-5.

At this point ordinary retaining tomography can tie the operation. The full
forcing matrix F is checked invertible, and V F^T=W gives

    <W,H> = <V,Y> - <V,E>,
    radius = sum_j delta_j ||V_j||_1.

The exact data-only implementation obtains radii 4.642691e-5 and 8.786547e-5,
without using B or rho, in 155,568 Fraction operations per source. Thus the
last zero-query transfer is real procedure reuse but not an exclusive or
sample-saving capability. The final broad workload reaches the full input
span; it is not evidence of asymptotically cheaper general tomography.
The data-only interval also avoids the random calibration event altogether:
its guarantee follows just from the deterministic response enclosures and
the checked invertibility of the forcing frame. This is a reason to prefer
that certificate once this additional information has actually been acquired.

### Lifetime accounting, failed controls and scope

The retained current-source evidence comprises 22 acquisition/calibration,
eight initial task, one witness and one costed-precision response per source:
32 native calls and 1,024 returned coordinates, plus the earlier support
acquisition on its earlier source. One development run completed the witness
experiments before failing on nested cProfile; its two native calls were
repeated and are explicitly recorded as additional spent work, not omitted
from lifetime accounting. Detailed timings from that failed process were not
retained. All substantive prior scripts, proofs and counterexamples remain.

Other controls cover the exact diagonal minimax values, a systematic error
that survives 100 repeated reports, an indistinguishable zero versus nonzero
coupling, rejection of a nonpositive dominance margin, and a deliberately
insufficient solver iteration budget that reports its missed requested
accuracy honestly. The latter does not get relabeled as a certified success.

The construction now supplies three reusable outputs: a verified estimator,
an explicit information obstruction when one is found, and a costed experiment
program whose reporting conditions are obtained for an actual software class.
It removes the exact-response restriction and an assumed numerical precision
interface. It does not establish general physical calibration, nonlinear
mechanism discovery, new source-level program-search heuristics, a practical
speed advantage here, or novelty over the entirety of optimal recovery.

The executor currently forms dense task and certificate matrices and retains
all histories. No fixed-width repeated-update or source-size-independent
compactness theorem is asserted. The informative next boundary is acquiring
structural or computational information that avoids reaching the complete
input span on a substantial class of new operations, while preserving these
positive and negative guarantees. Better orchestration alone would not remove
that information requirement.

## Reproduction from the retained scientific files

The scripts use Python's standard library and NumPy. Their retained helper
modules are `acquired_inverse_relations.py` and `acquired_relational_semantics.py`;
the first instrument reads the prior `acquired_inverse_relations_results.json`
for the already acquired support. These are actual available files. None of
the scripts imports the unavailable historical `quotient_actions` or
`source_warrants.py`.

Run the five new scripts in the order listed at the top of this note to
recompute everything. Their JSON outputs already preserve the actual records,
learned rows, elimination tapes, multipliers, norm factors, alternatives,
precision menus, selected procedures, error bounds and cost observations.
Recomputation is not needed to inspect or reuse those objects.
