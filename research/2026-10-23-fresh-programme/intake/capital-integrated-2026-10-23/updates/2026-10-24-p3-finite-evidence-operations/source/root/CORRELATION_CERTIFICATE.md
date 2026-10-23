# Acquiring a composable prediction certificate from reversible correlations

Private Astra P3, 23 October 2026. This is a conditional mathematical
construction and executable certificate, not a demonstrated physical
application or an architectural separation. The old circuit, retained-program,
network and renewal results remain unchanged. The source corpus stays pinned
at `0451552424b4679fa9a73faf5849ea5a4af21cf6`; this continuation does not use N51.

The subsequent non-self-adjoint extension, finite reverse-calibration proof,
variance composition, preparation obstruction, and exposed implementation
repair are recorded in `ADJOINT_AND_COMPOSITION.md`. The original arithmetic
versions and their audit receipts remain preserved under explicit backup names.

## 1. Scientific question and the information that is actually acquired

Can a learner certify the correlation of a **new sequence of interventions**
on a partially observed system, without recovering its microscopic state space
or assuming that its fitted low-dimensional model is complete?

The proposed input contract is stronger than ordinary endpoint observations:

* The unknown dynamics have one stationary probability measure pi.
* Each available action has a real self-adjoint contraction A_a on L2(pi).
  Common equilibrium and detailed balance of the full future-relevant system
  warrant this. A visible marginal at equilibrium is insufficient.
* A bounded, calibrated observable f, |f|<=1, can be read at the start and end
  of a trial without changing the claimed transition law.
* Each trial can begin with the stationary law, or a quantified preparation
  error is included. Independent trials or justified dependent-data bounds
  are required for statistical confidence.

For backward Markov operators, physical chronological word w=(a1,...,aT)
means A_w=A_a1...A_aT. The observed correlation is

    C(w) = <f,A_w f>_pi = E_pi[f(X_0) f(X_T)].

No state cloning, hidden-state readout, generator matrix, state count,
normalizer, spectral gap, or exact finite-rank promise is an inference input.
The physical/algorithmic contract above is NOT recognized by finitely many
correlations. Its cost and warrant cannot be discarded.

## 2. An implicit acquired representation

Choose a finite dictionary of action words b_0=empty,b_1,...,b_(d-1), and put
v_i=A_bi f. These vectors need not be evaluated on hidden states. Let V map a
coefficient vector z to sum_i z_i v_i. Reversibility makes their inner
products and action residuals experimentally accessible:

    G_ij    = <v_i,v_j>       = C(reverse(b_i)+b_j),
    H_a,ij  = <v_i,A_a v_j>   = C(reverse(b_i)+a+b_j),
    J_a,ij  = <A_a v_i,A_a v_j>
            = C(reverse(b_i)+a+a+b_j).

Thus a finite pool of at most (1+2k)d² protocol types, each of length at most
2L+2 when |b_i|<=L, exposes the required bilinear quantities. Shared and
reversed words are measured once and retained. This is acquired information,
not free preprocessing.

Choose **any rational matrices** T_a as candidate reduced actions. They can
come from a Galerkin fit, a regularized fit, an old retained program, or another
search. For validity, no inverse, positive minimum eigenvalue, exact rank,
small fitting error, or stability of T_a is assumed. Bad fits can simply
produce useless bounds.

Define

    D_a = H_a-G T_a,
    R_a = J_a-H_a^T T_a-T_a^T H_a+T_a^T G T_a.

For every coefficient vector z,

    z^T R_a z = ||A_a Vz-V T_a z||² >= 0.             (1)

Equation (1) is a known residual construction, not a novelty claim. Its
access through reversed pulse correlations is the interface being studied.
See Colbrook, Li, Raut and Townsend, *Beyond expectations: Residual Dynamic
Mode Decomposition and Variance for Stochastic Dynamical Systems*,
[arXiv:2308.10697v3](https://arxiv.org/html/2308.10697v3), section 3.2,
equations 24–26 and section 4.2, equations 29–30. Their batched-snapshot
construction uses two independent futures from a shared initial state for
the corresponding squared-mean matrix. Ordinary unbatched squared snapshots
also contain stochastic variance. A same-information retaining implementation
can use the pulse access here and reproduce the entire construction.

## 3. Inverse-free, two-sided composition theorem

For a target word w=(a_1,...,a_T), form

    l_0=e_0,       l_j=T_aj l_(j-1),
    r_T=e_0,       r_(j-1)=T_aj r_j.

Define the corrected finite-dimensional prediction

    Q_T(C) = e_0^T G r_0
             + sum_(j=1)^T l_(j-1)^T D_aj r_j.       (2)

After T and its coefficient paths are fixed, (2) is one **linear functional**
of the finite acquired correlations. Define

    (rho_j^L)^2 = l_(j-1)^T R_aj l_(j-1),
    (rho_j^R)^2 = r_j^T R_aj r_j.

Then, without any injectivity assumption on V,

    |C(w)-Q_T(C)| <= sum_(i<j) rho_i^L rho_j^R.        (3)

### Proof

Let x_0=f and x_j=A_aj x_(j-1). Set

    e_j^L=A_aj V l_(j-1)-V l_j,
    e_j^R=A_aj V r_j-V r_(j-1).

Telescoping the right approximation gives

    C(w)-<f,Vr_0> = sum_j <x_(j-1),e_j^R>.

Indeed the successive exact prefixes cancel, with self-adjointness moving
the prefix to the left argument. Now x_j-Vl_j=A_aj(x_(j-1)-Vl_(j-1))+e_j^L.
Since A_aj is contractive and x_0=Vl_0,

    ||x_(j-1)-Vl_(j-1)|| <= sum_(i<j) ||e_i^L||.

The component <Vl_(j-1),e_j^R> is precisely
l_(j-1)^T D_aj r_j. Subtract all these terms from the telescoping identity,
apply Cauchy–Schwarz to each remaining inner product, and use (1).
This proves (3). No projection or Gram inverse was used.

The first-order defect terms should be combined before an absolute value or
interval is taken. They can also correct the prediction as in (2). This is
ordinary dual/residual correction reasoning; historical novelty is UNKNOWN.

### Exact Galerkin special case

If the candidate actions are exact Galerkin projections, D_a=0 on the feature
span, and (3) is a leave-and-return error bound. The output error needs both
an excursion out of the span and a later coupling back to it. If each squared
residual on a unit projected state is <=kappa, then ||f||<=1 and the projected
actions contract, giving

    |C(w)-e_0^T G T_a1...T_aT e_0| <= binomial(T,2) kappa.

A generic one-sided state error gives only T sqrt(kappa). The two bounds
answer different questions: (3) is for a scalar endpoint correlation and
does not establish an approximation of the complete hidden state or all
future observables.

## 4. Exact finite-noise and finite-bit implementation

Suppose simultaneous intervals I_v for the acquired correlations contain the
truth. `correlation_certificate.py` represents each scalar in (1) and (2) as
a dictionary of **combined rational coefficients** of C(v). Since
C(v)=C(reverse(v)), reversed protocols share one entry. This avoids treating
one paid measurement as several independent uncertain numbers and preserves
identities such as A_a f being an already present feature.

For every squared residual form, evaluate an interval and use its upper end
as a bound on the true nonnegative square. A negative upper end is rejected:
it contradicts the asserted source/data event. No square is silently clipped
from a negative upper bound. Square roots are rounded **up** to an exact
dyadic rational using integer square root. Evaluate the combined functional
Q_T(C) as an exact rational interval, and enlarge it by the upper bound in
(3). Intersect with [-1,1] and with the separately valid one-sided residual
certificate when this improves the result.

The certificate accepts integers and Fractions only; floats and booleans
are refused. Matrix fitting can be numerical, but its output must be fixed
as a rational candidate. The certificate can be checked independently of
the optimizer. Singular or redundant feature spaces are allowed.

All finite-noise certificates hold on the same event that the measured
correlations lie in their intervals. Thus candidates, targets and policies
for choosing a *fixed target sequence* can be selected after seeing that
finite pool, without a fresh union bound over candidate fits or target
words. This does not cover a policy that changes the physical action based
on unmodelled intermediate observations. If the acquisition pool itself is
adaptively expanded, use fresh conditional confidence allocations or a valid
confidence sequence; reusing a nominal fixed-sample interval after arbitrary
stopping is not justified.

There is no claim of a dimension-free bit cost. The recurrence can amplify
coefficient magnitudes; rational numerator/denominator sizes, construction
of linear forms, model search, and failed fits all count. Exact-rank fitting
can still be ill-conditioned even though certificate validity does not
require an inverse. A conservative dense implementation uses polynomial
work in target length T, dictionary size d, pool size M, and the bit length
of its intermediate rationals; it never enumerates hidden states.

## 5. Acquisition and the strongest fair comparisons

With independent stationary trials, every product f(X_0)f(X_T) lies in
[-1,1]. For M distinct protocol types, m trials per type and common radius
eta, the elementary sufficient bound is

    m >= (2/eta²) log(2M/delta).

This charges M*m preparations, 2*M*m endpoint readouts (one squared readout
can suffice at the empty word), and m*sum_v |v| elementary pulses. Actual
equilibration, failed trials, readout calibration, protocol switching,
dependent-data correction, fitting, search and exact verification are extra.
An initial-law total-variation error eps adds up to 2eps to each bounded
correlation interval. A uniform readout error |f_tilde-f|<=e adds up to 2e+e²
before clipping to the physical range. These errors cannot be made small
merely by increasing trial count.

For a near-invariant, bounded-coefficient representation, squared residual
uncertainty is O(eta). The two-sided output error can then be O(T² eta),
where a one-sided state bound is O(T sqrt(eta)). This removes an artificial
fourth-root convergence rate for this output task. It is not a universal
sample-complexity separation: a strong moment/correlation estimator can
use exactly the same second-order argument.

Directly sampling one target of length T to accuracy eps also needs only
O(eps^(-2) log(1/delta)) independent trials and O(T eps^(-2)) pulses. In
contrast, the displayed uniform library certificate can require
O(M T^4 eps^(-2)) short trials before conditioning/coefficient factors.
This can be much worse for one target. A meaningful advantage must come
from a legitimate protocol-length limit, many changed targets, a useful
low-dimensional residual structure, or lower acquisition cost under a
specific source contract. None is established by an authored table alone.

The strongest equally informed alternatives are:

1. Direct endpoint estimation, if target protocols are available.
2. Retaining ResDMD/variational kinetic models with the SAME pulse correlations
   and physical warrants. They can implement (1)–(3) and tie the mechanism.
3. Positive moment/semidefinite completion using all the same correlations
   and contraction relations. This can tighten our inexpensive certificate;
   exact global optimization cost is not silently treated as free.
4. State-cloned batched simulation, if the actual simulator permits it. The
   pulse construction must not be given an advantage by withholding cloning
   or a supplied explicit model from this baseline.

## 6. What is reusable and what remains unknown

The acquired object consists of a paid correlation table, an implicit feature
dictionary, candidate reduced actions and checkable error functionals. It can
certify previously unqueried action words. Adding one new action while reusing
the dictionary requires its H/J correlations and a new candidate fit; G and
all old evidence remain useful. Adding a feature requires new cross data,
not a gratuitous new coordinate. Exact rank or full class membership need
never be declared merely to make a task-specific prediction.

This is a mechanism for accumulating warranted predictive operations under
a strong access contract. It is not yet a foundational law of intelligence.
Historical novelty, a physical deployment with an obtained full-equilibrium
warrant, and practical advantage over the best same-information method are
UNKNOWN. Physical adjoints, shared equilibrium, initial preparation and
noninvasive readout are the next interface questions; an arbitrary waveform
reversal is not automatically a Markov adjoint.

## 7. A finite certificate can warrant every future word, without certifying mixing

The target-specific theorem has a useful stronger specialization. Suppose
the *candidate coefficient matrices* satisfy ||T_a||_2<=r<1, and the acquired
residuals satisfy R_a<=kappa I. Neither statement asserts a contraction gap
for the full unknown dynamics. Since ||e_0||_2=1,

    rho_i^L <= sqrt(kappa) r^(i-1),
    rho_j^R <= sqrt(kappa) r^(T-j).

Consequently, for every word of length T>=2,

    |C(w)-Q_T(C)| <= kappa S_T(r),
    S_T(r)=sum_(k=0)^(T-2) (k+1)r^k <= 1/(1-r)^2.    (4)

Let G_c,D_a,c be the centers of the acquired linear forms and suppose the
same confidence event gives ||G-G_c||_2<=eta_G and
||D_a-D_a,c||_2<=eta_D. Then

    |Q_T(C)-Q_T(C_center)|
       <= eta_G r^T + T eta_D r^(T-1)
       <= eta_G + eta_D/(1-r).                       (5)

The final inequality follows from T r^(T-1)<=sum_(j=0)^(T-1)r^j. Handle
T=0 directly; T=1 has no residual-pair term. Combining (4) and (5) gives
a **single finite certificate for all finite action words at once**:

    |C(w)-Q_w(C_center)|
       <= eta_G + eta_D/(1-r) + kappa/(1-r)^2.         (6)

No union over words or horizons is necessary. The finite-data event for the
acquired moment pool implies the deterministic statement for its entire
composed language. A large bound remains valid but uninformative.

The corrected predictor itself is a reusable finite linear program. Define
the 2d-by-2d block matrices and readout vectors

    M_a = [[T_a^T, D_a,c], [0,T_a]],
    left = [e_0^T, e_0^T G_c],    right = [0,e_0]^T.

Then left M_a1...M_aT right equals Q_w(C_center) exactly. This is a weighted
automaton representation with a correction channel; a conventional retaining
program learner can store and execute it. No new physical oracle is created.

`uniform_correlation.py` implements a sufficient finite-bit certificate:
||T||_2<=sqrt(||T||_1||T||_infinity), outward rational square roots,
interval evaluation of residual Gram entries, and a Gershgorin upper bound
on R. It reports UNKNOWN if its sufficient norm bound cannot establish
r<1. That failure need not mean the representation or source is unstable;
another metric or a sharper norm calculation may work. No such optimization
is silently provided. The root's per-word certificate remains available.

This distinction is scientifically substantive. For one action and one
feature with C(0)=1, C(1)=lambda and C(2)=lambda²+v, a candidate T=lambda gives

    |C(N)-lambda^N| <= v/(1-lambda)^2 for every N.

Yet the same two moments can coexist with arbitrarily large integrated
correlation time: a small spectral weight can approach eigenvalue one while
other weights compensate the two fixed moments. Thus a useful uniform
absolute-error prediction does **not** certify a finite mixing time, spectral
gap, hidden-state rank, or integral response. Those stronger questions
require additional information. Ordinary sharp Hausdorff moment bounds are
the equally informed baseline for this one-action subclass; they can improve
the constants and match the order of this certificate. A larger authored
table would not establish an architectural advantage.

### The word basis needs an acquired numerical metric

The unweighted norm check has a predictable failure: if both f and A_a f
are feature columns, the natural exact transition sends e_0 to e_a and
has Euclidean norm at least one, even when all observable dynamics decay.
This coordinate artifact must not be described as a scientific obstruction.

`metric_correlation.py` handles a proposed rational positive-definite matrix
M. Often the center of the paid Gram table is a useful proposal; it is a
numerical metric, not a claim that the true Gram is invertible. The exact
conditions are

    T_a^T M T_a <= r² M,       R_a <= kappa M,
    |x^T(G-G_c)y| <= eta_G ||x||_M ||y||_M,
    |x^T(D_a-D_a,c)y| <= eta_D ||x||_M ||y||_M.

The same proof gives the uniform error

    M_00 [eta_G + eta_D/(1-r) + kappa/(1-r)^2].

For a symmetric uncertain matrix with entry radii E_ij, its error is bounded
above and below by diag(sum_j E_ij). For a nonsymmetric defect error, row
and column diagonal majorants both dominated by eta_D M imply the displayed
bilinear bound: apply 2|x_i y_j|<=x_i²+y_j², then rescale x and y to equal
M-norm. Residual centers plus their row-radius diagonal give an upper matrix
bound on the true residual Gram.

The implementation searches dyadic domination constants and **verifies**
each M-based matrix inequality with rational Schur complements, including
the zero-pivot condition. It records the exact PSD-check count. Search is
bounded and can return UNKNOWN; no unbounded SDP or real-number oracle is
assumed. A badly conditioned metric makes the uncertainty constants large
and may require expensive acquisition precision. It changes the inference
coordinates, not the available information.
