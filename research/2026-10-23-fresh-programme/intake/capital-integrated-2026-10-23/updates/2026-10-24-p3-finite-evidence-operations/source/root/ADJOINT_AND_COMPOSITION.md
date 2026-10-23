# Finite acquired evidence for reusable operations

Private Astra P3, 23 October 2026. This extends `CORRELATION_CERTIFICATE.md`.
It preserves a conditional theorem and executable construction, including
its failed applicability cases and the equally informed retaining-program
tie. It does not establish a new architecture, a physical deployment, or a
general law of cumulative intelligence. Historical novelty and practical
advantage are UNKNOWN.

The governing Astra corpus revision remains
`0451552424b4679fa9a73faf5849ea5a4af21cf6`. N780 motivates distinguishing
acquisition within a promised class from recognition of that class. No N51
oracle or representation is used. Earlier circuit, network, finite-bit,
composition, repair, and retaining-comparison bundles are unchanged.

## 1. The operation and its external obstruction

The task is to predict the bounded endpoint correlation of a previously
unqueried, open-loop sequence of interventions on a partially observed
stochastic system. The learner need not identify the hidden state space.
It must acquire enough information to bound its own output error.

A concrete obstruction in stochastic residual DMD is that a single noisy
future gives a squared prediction error containing both a conditional-mean
residual and stochastic variance. Two independent futures from the same
initial state separate these quantities. See Colbrook, Li, Raut and Townsend,
*Beyond expectations: Residual Dynamic Mode Decomposition and Variance for
Stochastic Dynamical Systems*, arXiv:2308.10697v3, sections 3.2 and 4.2:
https://arxiv.org/html/2308.10697v3 .

The mechanism studied here acquires the needed bilinear residual information
through adjoint pulse sequences instead. This is a different access mechanism,
not an improvement over a baseline that is forbidden to use the same data.
It is useful only where the adjoint/preparation contract can be warranted
and its complete cost is acceptable. In a state-clonable simulator, the
batched-future alternative remains fully available.

## 2. Access contract with executable adjoints

Let the real Markov operators A_a preserve one probability law pi. Thus they
contract in L2(pi). A bounded readout satisfies |f|<=1. The ideal action
alphabet has an involution a -> a^dagger satisfying A_(a^dagger)=A_a^*.
Actions need not be self-adjoint or commute. Trials begin at pi and endpoint
readings do not change the stipulated process. Statistical confidence also
needs independent preparations or a valid dependence analysis.

For a chronological word w=(a_1,...,a_T), backward-operator convention gives
A_w=A_a1...A_aT. Write

    C(w)=<f,A_w f>_pi,
    w^dagger=(a_T^dagger,...,a_1^dagger).

Only C(w)=C(w^dagger) is generally valid. Plain word reversal is invalid for
non-self-adjoint actions.

Choose feature words b_0=empty,b_1,...,b_(d-1), and let V have columns
v_i=A_bi f. These columns are implicit functions on the unknown state space.
The following matrices are acquired by scalar endpoint protocols:

    G_ij       = C(b_i^dagger b_j),
    H_a,ij     = C(b_i^dagger a b_j),
    J_a^R,ij   = C(b_i^dagger a^dagger a b_j),
    J_a^L,ij   = C(b_i^dagger a a^dagger b_j).

H_a need not be symmetric. J_a^R and J_a^L need not be equal. For a closed
alphabet of k labels, the implementation requests at most (1+2k)d^2 words;
the J entry for the dagger label supplies J^L. Dictionary length at most L
gives query length at most 2L+2. Duplicate ideal protocols share their paid
evidence. If all dictionary words use forward labels only, a query contains
at most L+1 reverse operations. Otherwise count the actual reverse labels.

No hidden state count, normalizer, source equation, full Hankel rank, exact
closure promise, or state-space cloning is needed to evaluate the certificate.
None of those omissions makes common stationarity or the adjoint contract
free. In particular, visible stationarity is insufficient (section 7).

## 3. Exact two-sided theorem with distinct forward and adjoint fits

Choose any rational candidate matrices T_a for A_a and U_a for A_a^*. The
implementation uses U_a=T_(a^dagger), fitting both labels. Define

    E_a^R=A_a V-VT_a,             E_a^L=A_a^*V-VU_a,
    D_a=H_a-GT_a,
    R_a^R=J_a^R-H_a^T T_a-T_a^T H_a+T_a^T G T_a,
    R_a^L=J_a^L-H_a U_a-U_a^T H_a^T+U_a^T G U_a.

Thus R_a^R=(E_a^R)^*E_a^R and R_a^L=(E_a^L)^*E_a^L.
The candidate matrices need not be Galerkin, symmetric, accurate, or stable.
True G need not be invertible. Bad candidates can give uninformative bounds.

For target w=(a_1,...,a_T), form

    ell_0=e_0,       ell_j=U_aj ell_(j-1),
    r_T=e_0,         r_(j-1)=T_aj r_j.

The corrected prediction is

    Q_w(C)=e_0^T G r_0 + sum_j ell_(j-1)^T D_aj r_j.       (1)

For fixed candidates it is a linear functional of the finite acquired
correlation table. The exact output error obeys

    |C(w)-Q_w(C)|
      <= sum_(i<j)
          sqrt(ell_(i-1)^T R_ai^L ell_(i-1))
          sqrt(r_j^T R_aj^R r_j).                        (2)

### Proof

Let x_0=f and x_j=A_aj^*x_(j-1), so x_j=(A_a1...A_aj)^*f. Put
e_j^R=E_aj^R r_j and e_j^L=E_aj^L ell_(j-1). Right telescoping gives

    C(w)-<f,Vr_0>=sum_j <x_(j-1),e_j^R>.

Left approximation obeys

    x_j-Vell_j=A_aj^*(x_(j-1)-Vell_(j-1))+e_j^L.

Since each true adjoint contracts, the norm of this difference before j is
at most sum_(i<j)||e_i^L||. Its component in Vell_(j-1) is exactly the jth
correction in (1). Subtract those components and apply Cauchy-Schwarz to the
remaining inner products, proving (2). No full-system identification occurs.

This is a goal-oriented residual correction, with close established prior
in primal/dual reduced-basis output bounds. See Klindworth, Grepl and Vossen,
equation (32) and Proposition 2 (54)-(55):
https://www.igpm.rwth-aachen.de/Download/reports/grepl/KGV_CMAME_preprint_revised.pdf .
The missing interface being investigated is acquisition of these residual
quantities from scalar stochastic protocols; the product-error idea itself
is not claimed as new.

## 4. A finite certificate for every finite word

Suppose a proposed rational positive-definite coefficient metric M satisfies

    T_a^T M T_a <= r_R^2 M,      U_a^T M U_a <= r_L^2 M,
    R_a^R <= kappa_R M,          R_a^L <= kappa_L M,

with r_L,r_R<1. These are statements about the learned coordinates and their
acquired residuals. The true system may have invariant or arbitrarily slow
hidden modes.

Then (2) is bounded, for every T and every word, by

    M_00 sqrt(kappa_L kappa_R)/[(1-r_L)(1-r_R)].            (3)

To see this, set u=i-1 and v=T-j. The pair sum is over u,v>=0 with
u+v<=T-2 and is at most the full product of geometric sums.

Suppose the same finite confidence event bounds moment-center errors by

    |x^T(G-G_c)y| <= eta_G ||x||_M||y||_M,
    |x^T(D_a-D_a,c)y| <= eta_D ||x||_M||y||_M.

Their effect on (1) is at most

    M_00 [eta_G + eta_D min{1/(1-r_L),1/(1-r_R)}].         (4)

For the common maxima r and kappa used by the code, (3)+(4) becomes

    epsilon = M_00 [eta_G + eta_D/(1-r) + kappa/(1-r)^2]. (5)

One finite moment confidence event therefore implies

    sup_(all finite words w) |C(w)-Q_w(C_center)|<=epsilon.

No union bound over target words or model fits is needed. The implication is
deterministic for every candidate and target after the fixed finite pool is
acquired. Expanding the pool adaptively still requires valid confidence
allocations/stopping rules. Choosing future actions from observations within
the deployment run is not covered by this open-loop statement.

The implementation combines rational linear forms before taking intervals,
uses upward dyadic square roots, and checks matrix domination with exact
Schur complements including zero-pivot conditions. M is a numerical proposal;
it need not be the true Gram or prove true rank. Ill-conditioning is paid in
larger uncertainty and bit costs. A bounded sufficient search can return
UNKNOWN. It does not get an exact SDP, unlimited precision, or a hidden
matrix oracle for free.

### The retaining-program comparison is exact

Let

    M_a = [[U_a^T,D_a,c],[0,T_a]],
    left=[e_0^T,e_0^T G_c],       right=[0;e_0].

Then Q_w(C_center)=left M_a1...M_aT right. An ordinary 2d-state weighted
automaton or retaining program implements exactly the same acquired
operation and certificate. There is no architectural separation.

Stable weighted-language approximation and squared stability denominators
also have established precedents. Balle, Gourdeau and Panangaden,
*Bisimulation Metrics for Weighted Automata*, Lemma 25 and Theorem 22:
https://arxiv.org/pdf/1702.08017 . That spectral-learning theorem assumes a
complete finite Hankel block for a finite-dimensional irreducible target.
The result here instead uses acquired hidden-space residual bounds and
does not recognize full rank. The bounded prior review does not establish
historical novelty for this combination.

## 5. Approximate physical reverses affect finite acquisition, not target length

Suppose B_a is an executable reverse Markov kernel and an independently
justified bound gives ||B_a-A_a^*||_(L2(pi)->L2(pi))<=delta_a.
For |f|<=B and an ideal query q, replacing each reverse by its implementation
changes the observed endpoint correlation by at most

    B^2 sum_(reverse occurrences j in q) delta_(a_j).     (6)

Proof: telescope with ideal prefixes and actual suffixes. Ideal prefixes
contract in L2(pi), while actual Markov suffixes preserve the sup norm of f.
The latter have L2(pi) norm at most B even if B_a does not preserve pi.
Every replacement contributes at most B^2 delta_a.

Inflate each finite queried interval by (6) before fitting or verification.
The resulting intervals enclose ideal moments; equations (1)-(5) then apply
to true-forward target words of any length. No extra delta times the future
target horizon is necessary. A prediction containing ideal reverse labels
does not automatically describe future imperfect reverse pulses.

This is a conditional calibration result. The operator-error upper bound
is not inferred by checking a few moment inclusions. A finite-domain bound
can suffice only if it covers every actual suffix function used at a replaced
reverse position. Agreement on f and constants alone fails, as the exact
positive three-state example in `../external/APPROXIMATE_ADJOINT_CALIBRATION.md`
shows. A small per-step defect in forward stationarity can accumulate over
the target horizon; it cannot silently replace the true forward contract.

## 6. Composing the acquired operation into finite-schedule variance

For a fresh stationary run with n observations and open-loop actions
a_1,...,a_(n-1), let Y_n=n^(-1)sum_i f(X_i). Then

    E[Y_n^2] = [n C(empty)+2 sum_(i<j) C(a_(i+1)...a_j)]/n^2. (7)

The weights are nonnegative and sum to one. Thus (5) implies second-moment
error at most epsilon, independently of n. If a tighter empty-word error
delta_0 is retained, the bound improves to delta_0/n+(n-1)epsilon/n.

The retained weighted program evaluates the sum of all contiguous subwords
in O(n d^2) arithmetic, not O(n^2) separate protocol evaluations. With row u=0
and scalar s=0, perform u<-(u+left)M_a and s<-s+u right for each action.
Return [n left right+2s]/n^2. Bit growth still counts. `finite_variance.py`
implements this recurrence, interval subtraction of a paid squared-mean
interval, and a Chebyshev failure bound.

If U upper-bounds the target variance on an acquisition event of probability
at least 1-delta, a fresh run gives interval Y_n +/- sqrt(U/alpha) with joint
coverage at least 1-delta-alpha. The new run must be stationary conditionally
on the data and the chosen schedule; reusing a training endpoint to choose
its own action schedule can violate that condition. No mixing theorem, CLT,
or finite infinite-horizon integrated correlation time is asserted.

### Exact centering without a known mean

A strictly contractive predictor tends to zero, whereas a raw ergodic
correlation tends to mu^2. Merely subtracting a mean estimate after prediction
does not remove this invariant-component floor.

Under independent stationary reset access, use two independent copies and

    F(x,x')=(f(x)-f(x'))/2,       Atilde_a=A_a tensor A_a.

Then |F|<=1, its mean is exactly zero, and

    C_F(w)=[C_f(w)-mu^2]/2,
    Var(Y_(n,f))=2 E[Y_(n,F)^2].                          (8)

Each paired endpoint product is directly measured by multiplying initial
and final readout differences and dividing by four. It costs two independent
preparations and two executions of the pulse word. No same-hidden-state
cloning or prior mean is needed. The acquired correlation certificate on F
therefore produces finite-schedule variance error at most 2 epsilon_F.
This is ordinary covariance symmetrization, not a novelty claim. It fixes
centering, not nonstationary preparation or missing slow modes.

### Strong complete alternatives limit the application claim

* The independent stationary starts purchased during acquisition already
  provide IID samples for the same equilibrium mean. They must be retained
  by the baseline. A new claim of making that mean answerable is unjustified.
* Two independent target averages Y,Y' give Z=(Y-Y')^2/2 in [0,2] with
  E[Z]=Var(Y). Direct Hoeffding estimation is a valid gap-free comparator.
* A single-action moment method can optimize the finite variance polynomial
  directly. It can be tighter than adding separate uniform correlation
  bounds. Joint noncommutative moment constraints are a stronger, potentially
  expensive comparator for multiple actions.
* A conventional program learner can retain (7)-(8) and every acquired datum.

A fixed epsilon leaves a variance floor. With elementary O(epsilon^-2)
correlation acquisition, obtaining an O(h^2) variance allowance for mean
accuracy h can cost O(h^-4) preparations, whereas IID start averaging costs
O(h^-2). This is a sufficient-cost comparison, not a minimax lower bound.
The valid scientific operation is reusable finite-schedule variance
prediction; superiority for equilibrium-mean estimation has not been shown.

## 7. Applicability can fail while all visible short checks look stationary

The independently derived six-state witness in
`../partial/reverse_pulse/PREPARATION_OBSTRUCTION.md` is a reversible,
irreducible finite-rate CTMC with one common equilibrium. It stores an initial
hidden sign, first loses visible correlation, then recovers that sign through
a rare transition. Only the full stationary-preparation premise fails.

With leak d, return rho, and global equilibrium-reset rate gamma, its actual
prepared correlation is

    C_t^mu=e^(-gamma t){d/(d+rho)[1-e^(-(d+rho)t)]+2^(-t)e^(-dt)}.

The visible marginal is uniform at every time. The complete short visible
history through time L differs in total variation from a stationary binary
fast chain by at most L(d+gamma). Any adaptive independent-preparation
acquisition with bounded total pulse duration B has transcript TV at most
B(d+gamma). Yet rho=gamma=d^2 and T=ceil(1/d) give C_T^mu>3/5 while the
apparent fast predictor gives 2^(-T).

The failure is not an illicit change to the pulse dynamics. Self-adjointness
holds in L2(pi), while measurements start from mu. The two-pulse endpoint
correlation is not the asserted squared conditional-mean Gram entry under
mu. Symmetrizing independent copies does not change that inner-product error.

An independently warranted TV(mu,pi)<=zeta would suffice to add 2zeta to
each acquired moment interval. If future targets also begin from mu rather
than pi, add a separate 2zeta target allowance. Short visible checks alone
do not yield such a bound. The combined effect is not generally just 4zeta:
input uncertainty is amplified inside the certificate. For two independent
copies the product-preparation TV bound is at most 2zeta-zeta^2, and that
product bound must be used at both stages. A bound on the full state is
sufficient, but the
theorem does not assert it is necessary for every narrower scientific task.

## 8. Information sharpness, precision, and actual checks

For one positive self-adjoint action, unit f, and paid moments C_1=lambda,
C_2=lambda^2+v, the scalar model T=lambda has all-lag allowance
v/(1-lambda)^2. Exact Hausdorff moment optimization is stronger:

    x=lambda-v/(1-lambda), p=v/[(1-lambda)^2+v], y=lambda+v/lambda,
    lambda y^(N-1) <= C_N <= p+(1-p)x^N, N>=3.

Two-atom measures attain the bounds; quadratic Hermite interpolants certify
them. The residual allowance matches the first-order upper uncertainty in v,
but the tailored method improves constants. The same short information can
permit arbitrarily large integrated correlation even in fixed-dimension,
irreducible, reversible CTMCs. A useful pointwise operation is therefore
strictly weaker than full tail identification. The exact derivations and a
matched O(epsilon^-2) statistical order in the small-residual regime are in
`../partial/reverse_pulse/MOMENT_SHARPNESS.md`.

One charged sufficient example, with epsilon=10^-3 and delta=0.01, needs
19,172,686,551 independent short trials per required moment using elementary
Hoeffding bounds and data-fitted coefficients. Direct estimation of one
target needs 10,596,635 trials. The former count is not an executed experiment.
Two separately acquired moments cost 2m preparations and 3m elementary
pulses; a nondisturbing intermediate readout can reuse one two-pulse trial,
costing m preparations, 2m pulses, and 3m readouts. Preparation/calibration
work is additional. Long targets can favor the short procedure in pulse count
while preparations still dominate. No practical crossover is asserted.

The finite-bit root checks use already exposed exact sources:

* Self-adjoint check: 23 checks, no failures; 11 distinct exact fixture
  protocols; 482 exact PSD checks; largest recorded rational length 776 bits.
* Adjoint/composition check: 22 checks, no failures; 9 exact composite-pulse
  protocols, 21 composite pulses, two elementary stages per composite;
  largest recorded rational length 228 bits. Approximate-reverse query
  inflation produces a valid all-forward allowance about 1.7968e-6 in this
  authored calibration example.
* Independent arithmetic audits previously passed 27 per-word checks and
  42 uniform/metric checks. Their receipts identify the exact old byte
  versions they examined; they are not silently relabelled as post-repair.

Independent review then found a real implementation failure: the public
self-adjoint metric front door accepted an adjoint subclass and compiled
T_a^T instead of U_a^T. A deliberate coefficient perturbation in the same
exposed source gave true error 8.0474e-11 under a claimed 2.9626e-14 bound.
The intended adjoint wrapper was sound on that case. The old files and exact
counterexample remain preserved. Public interfaces now reject mixed semantics,
and a private shared metric routine is used by the validated adjoint wrapper.
Sixteen focused interface regressions passed; the 23- and 22-check root
constructions were then rerun successfully. No broad new benchmark was added.

These are proof and implementation checks, not acquired physical data or
unseen scientific transfer. Matrix truth was used only for exact fixture
checking; candidate fitting used the specified paid moment table. Timing
receipts are small-script execution times, not total research cost. Maximum
recorded rational sizes do not assert a complete peak-memory/bit-operation
profile. Search, physical preparation, calibration, failed proposals, and
verification are not omitted from any claimed end-to-end advantage; no such
advantage has been demonstrated.

### A strict all-word guarantee needs an appropriate protocol language

If A_a is unitary and A_(a^dagger)=A_a^(-1), every word
(a^dagger,a)^N has correlation ||f||^2. A corrected finite program whose
forward and left coefficients all strictly contract tends to zero on those
words: its terms are bounded by constants times r^(2N) and 2N r^(2N-1).
Any sound uniform allowance must therefore be at least ||f||^2. This
particular guarantee is uninformative for a nontrivial invertible deterministic
system whose inverse actions are included in the target language. More
authored permutation examples cannot repair that obstruction.

Likewise, a single-site Gibbs heat-bath operator P_i is an orthogonal
projection. Repeating just that site gives C(i^N)=||P_i f||^2 for N>=1.
An all-word strictly contractive predictor must allow at least this invariant
conditional component. If the scientific question concerns complete update
sweeps, the action alphabet should explicitly consist of complete sweeps
and their reverse-order adjoints, or a restricted schedule language should
be separately certified. The current implementation does not claim a
constrained-language stability solver. The domain restriction must come from
the task, not from silently excluding a difficult evaluation case.

## 9. Scoped conclusion and extension cost

The construction provides an explicit way to acquire task-sufficient
representation evidence, compose it to never-queried words, and then compose
those predictions into a different finite-run statistical operation.
It avoids a full hidden-model completeness claim. Its reach comes from the
measured residual information plus a warranted access contract.

The retaining-program tie is preserved. The theorem does not learn its own
physical class promise. The decisive unresolved scientific question is where
the required stationary/adjoint access can actually be obtained at a cost
that beats equally informed direct, cloning, coupling, and moment methods.
More authored matrices or larger target tables would not answer that question.

Reuse can also support further acquisition. For one newly available action
and its warranted adjoint, the old dictionary and G table remain usable;
new H_a, J_a^R and J_a^L tables suffice, at most 3d^2 scalar protocols before
duplicate sharing. H_(a^dagger)=H_a^T does not require an independent table.
Their physical durations, confidence allocation, calibration and new fit
are charged. The new action must preserve the same warranted law; old
observations cannot establish that fact. Adding a dictionary word requires
new cross correlations against the existing words for every retained action.
These are concrete acquisition operations, not a promise that every expansion
will find a compact or well-conditioned representation.

## 10. One access route is obtainable, with its competitors intact

`../structure/ACCESSIBLE_PREPARATION_ROUTE.md` closes the logical preparation
interface in a specified simulator class. On a finite bounded-degree graph,
take positive rational lattice-gas factors lambda_i and attractive rational
edge factors theta_ij>=1. The local conditional probabilities are computable
without the global normalizer. Enumerating the finite local conditional
tables, constructing exact common-integer thresholds, and using monotone
coupling from the past produces exact independent Gibbs starts. Every table,
random bit, failed lookback, replay and observable evaluation is charged.

For N sites, let b_i be the minimum probability of resetting site i to zero
over its local contexts. A prescribed ordered zeroing block has reference
random-scan probability beta=N^(-N) product_i b_i>0. Thus the minimal
coalescing lookback tau satisfies E[tau]<=N/beta. Doubling and replay of both
extremal paths use fewer than 8 tau single-configuration updates. This proves
termination, not affordability. Censoring slow completed calls can bias the
sample; use a prescribed number of independently completed calls or abort
the acquisition without pretending that fast selected calls are IID.

Every local heat-bath step is a conditional-expectation projection in the
same Gibbs measure. A complete sweep has an actual reverse-order adjoint,
so the new adjoint interface is available. This is known perfect sampling
and Gibbs algebra, with the source class explicitly supplied, not learned
local structure or recognition of an unknown physical source.

The same contract grants full simulated states and copying to the baseline.
It can use cloned futures, local conditional expectations, influence matrices,
coupling bounds, all paid starts, and direct paired-run variance estimation.
Where influence bounds cheaply prove rapid coupling, those direct bounds may
already be strong. Elsewhere preparation can be expensive. Thus the route
proves that the theorem's input contract is obtainable for a substantive
scientific computation class, while an end-to-end advantage is still UNKNOWN.

Primary algorithm verification used Fill's author-hosted paper, especially
sections 4-6 (the original Propp-Wilson full PDF timed out; its abstract and
metadata were retrieved): https://www.ams.jhu.edu/~fill/papers/algo1.pdf .
Scan order is an externally motivated scientific issue: He, De Sa, Mitliagkas
and Re show models with polynomial mixing-time differences between orders,
https://arxiv.org/pdf/1606.03432 . Neither source establishes this learned
certificate's advantage. A finite-sweep variance target is also distinct
from their global mixing-time question.
