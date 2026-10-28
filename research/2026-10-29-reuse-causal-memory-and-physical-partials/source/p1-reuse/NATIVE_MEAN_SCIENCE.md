# From hidden values to a reusable, certified probability law

Scientific continuation for Capital. 29 October 2026, Brisbane.

## Current result after the next construction and comparison

The strongest completed object is now an acquired candidate law together
with two measured quantities: a conditional mean residual R and a conditional
noise energy S. They support both direct reuse of the learned law and an
executable source correction at a stricter requested accuracy. Source values,
training, validation, preparation and correction are all charged. The current
result is conditional on a strictly contractive source and a useful constructed
candidate; it is not a general solution of dense native Gaussian-law sampling.

The first large validation below cost 1187841 values. Continuing past that
failure against the ordinary comparator produced two stronger constructions.
First, a 4096-query pilot acquired S<=.4796733159537619, replacing the
worst-case 54.21027964847543. A new U-statistic validation then certified
W2<=.4525404119140231 using 192513 complete original vector values. The old
worst-case bound on these same data gives .7407286944170575 and fails.

A simpler conventional paired-energy certificate is stronger on this fixture.
At a shared center take independent residuals D1,D2 and use

    Y+=(D1+D2)/sqrt(2),  Y-=(D1-D2)/sqrt(2),
    E||Y+||^2=2R^2+S,   E||Y-||^2=S.

One-sided Gaussian norm concentration bounds their population energy
difference. Its complete learned workflow costs 24577 original vectors
(8193 training plus 16384 fresh validation) and 2359392 scalar answers,
certifies per-output stationary W2<=.48980753486931167 with false-release
probability <=1/1024, and produces 8192 fresh candidate samples with no further
source values. The current ordinary global Gaussian-convolution sampler for
the same .5 target costs 393217 original vectors. The paired rule is adopted;
ordinary concentration and paired-moment identities are not novelty claims.

### Greater requested accuracy requires actual source correction

For a new .1 target, the candidate's .49 certificate is insufficient. A fresh
experiment acquires R and S simultaneously with three one-sided tail budgets
summing to 1/1024, then executes

    mhat_q(x)=q^-1 sum_j g(x+G_j)-A q^-1 sum_j G_j,
    next=mhat_q(x)+sigma Z.

The acquired affine A cancels observation noise without changing the drift
mean. For fixed inner noises the correction is independent of x, preserving
the source's L-contraction. The conditional noise RMS s(x) is L-Lipschitz,
so its measured average under the candidate transfers to the target law:

    A0=R_bar/(1-L),
    sqrt(E_pi_g s^2)<=sqrt(S_bar)+L A0,
    e_0<=A0,   e_t<=L e_(t-1)+c/q_t,
    c=sqrt(log(2))(L+||A||)[sqrt(S_bar)+L A0]/sigma.

The convolution step uses the same current Paulin--Whalley primary result
as the strongest ordinary comparator. The acquired information makes its
noise-dependent bound executable without a uniform covariance promise.
The simultaneous event supports every deterministic accuracy schedule chosen
from the acquired record, with actual new execution calls paid. It does not
justify sampling allocations or stopping chosen from production outcomes.

The fresh execution acquired A0=.4943461674646958, S_bar=.3897671667254895,
and c=.5452285285907604, then used [5,7,9,13,18] source values per output:

| Executed route, target W2 .1 and 8192 outputs | Complete native vectors | Scalar answers | Per-output bound |
|---|---:|---:|---:|
| Global Gaussian-convolution sampler from zero | 1949697 | 187170912 | .0998763231 |
| Same ordinary sampler, initialized from the acquired candidate | 1589249 | 152567904 | .0997957710 |
| Acquired candidate and integrated-noise source correction | 450561 | 43253856 | .0984059368 |

Both acquired-record routes include the same 24577-query preparation and
inherit its 1/1024 false-certificate budget. Their optimized finite schedules
use respectively 191 and 52 source values per output. The source-corrected
route saves 1138688 original values against the stronger acquired-start
comparator, a factor 3.527. The standalone route instead has a deterministic
bound under its ideal premises. This compares the declared executable policies,
not all possible methods. Conventional control-variate sampling can adopt
the acquired interface and receives its benefit.

The new acquired-noise, paired-energy and stricter correction proofs received
independent scoped reviews. Saved-array audits reconstructed confidence
constants, schedules, counts and output hashes without source reruns. Every
full-vector query still pays d scalar answers and the fixture's O(d^2) source
arithmetic. Counts do not acquire Gaussian or instrument precision. Conditional
production independence and false-release scope are as detailed below.

### New ordinary theorem beyond a Gaussian candidate invariant law

NONLINEAR_CANDIDATE_ACCURACY_THEOREM.md separates a direct beta-contractive
candidate drift b from an affine noise-control matrix A. A finite T-step
candidate chain is an actual Lipschitz function of Gaussian seeds, with
squared constant C_T=sigma^2 sum_(j<T) beta^(2j), and its finite burn-in
error e_b is paid. Native residuals g(x+G)-b(x)-A G acquire R_T and S_T
under that actual finite law. Its initial target-law error obeys

    A0=[R_bar+(1+beta)e_b]/(1-L).

Focused review supplied a stronger direct finite-law comparison: if kappa
justifiably bounds W2(nu,nu K_b), then A0=(R_bar+kappa)/(1-L). For the
specified T-step candidate preparation, kappa<=beta^T sqrt(||b(0)||^2+sigma^2 d),
constructed without additional source calls. This sharper form is adopted;
it need not compare through a candidate invariant law. The same
source-correction recurrence applies. This removes the requirement
of an exactly Gaussian candidate invariant law while retaining all candidate
preparation, matrix and source costs. The extension is an ordinary theorem,
not a newly executed nonlinear fixture or a universal model-discovery result.

The scientific gap remains finding compact useful representations for hard
sources, particularly beyond strict contraction. The following sections retain
the construction, early comparisons and useful failures that led to this
current interface. Their initial cost crossovers are superseded by the
completed refinements above.

## Question reopened and provisional choice tested

The completed coarse-composition tranche is retained. Its absolute survival
guarantees do not control a mean lifetime, and its lower bound concerns its
declared observation interface. Neither fact is a ceiling on discovery.

The strongest continuation of that direction would acquire a representation
that controls consequential long-run quantities despite unobserved states.
A materially different opportunity is distribution-valued computation:
produce the probability law centered at an inaccessible expectation, then
compose or reuse it without first identifying the underlying function.
Success could turn expensive averaged models into executable scientific
objects with a guarantee on the consequences they are meant to preserve.

I provisionally chose the latter. Astra's existing native heat actions and
Gaussian-law work, together with current positive Poisson/FORS constructions,
provided an approachable bridge. Serious construction changed that choice
internally: a general path-clock approach exposed a paid dimension problem;
exact local sampling succeeded; supplied locality was then replaced, for a
stationary consequence, by an acquired residual certificate. The final
prototype also learns its candidate instead of receiving one for free.

A separate rare-event opening was constructed rather than only surveyed.
Its general unknown-kernel Doob implementation was correct under a certified
strict superharmonic potential, but a native reversed-drift comparator was
dramatically cheaper on the proposed example. That branch did not earn an
operational advantage. Its failure and exact conditioning construction remain
reusable under branches/rare_event_bridge.

## 1. A positive local interface for the Gaussian mean law

The primitive target is

    N(E g(x+G),sigma^2 I_d),       G~N(0,I_d),

using original whole-vector values of globally L-Lipschitz g. In the first
successful construction, supplied supports S_i satisfy |S_i|<=s and specify
which inputs each output coordinate uses. Their intersection graph admits
chi colors of disjoint supports. These are supplied structural warranties;
they were not inferred from finitely many source readings.

For a scalar k-input L-Lipschitz f, let m_k=E||G_k||, U be uniform on the
unit sphere, and R~chi_(k+1), independently. Radial size bias gives

    X=m_k[f(RU)-f(0)]/R,
    E X=E f(G_k)-f(0),       |X|<=L m_k.

Disjoint input supports let one native vector query supply independent X
observations for every active coordinate in a color. This independence is
the substantive interface obligation; separate correct marginals are not
enough for the desired joint Gaussian.

A conventional one-observation positive Poisson rule then samples the scalar
Gaussian exactly in the ideal model. For |X|<=a, theta=EX and r=a/sigma,
propose Y~N(0,2sigma^2), let

    K(Y)=r^2+Y^2/(4sigma^2)+a|Y|/sigma^2,
    lambda(Y,X)=r^2+Y^2/(4sigma^2)-YX/sigma^2,

and accept a Poisson(K) proposal when every fresh mark passes with probability
1-lambda/K. The acceptance normalization depends on theta but has a known
positive lower bound; it need not be estimated. This removes the unnecessary
paired X1 X2 term in the first valid construction.

An exponential tail for all latent marks gives an every-execution cap. A
fresh Gaussian fallback, its correlation-aware Gaussian tail moment bound,
and independent packing supply full joint TV and W2 guarantees. For fixed
s,chi,L/sigma the native query cap is O(chi log(d/epsilon)). Every query
still returns d scalars and pays its source evaluation, preparation,
arithmetic and precision requirements. The exact Poisson version's constants
are exponential in the squared bounded-observation radius; ordinary FORS is
a stronger large-radius alternative and was implemented with the same access.

### Executed comparison, same native interface

All rows have 16 output vectors, sigma=2, a=1.6, three colors, and targets
TV<=.01 and W2<=.2 per output.

| Dimension | First paired factory | Adopted one-observation rule | Clipped FORS |
|---:|---:|---:|---:|
| 96 | 4143 | 608 | 23286 |
| 384 | 5349 | 827 | 25940 |
| 1536 | 7397 | 953 | 28053 |

Entries are original full-vector queries, including the shared anchor.
Early rejection also contributes to the adopted rule's lower executed cost;
the table is not an optimization lower bound for the paired formula. At
d=1536, the adopted run returns 1463808 scalar answers. No cap aborted in
these runs; their small failure bounds come from proofs, not observed absence
of failures. The interface, factory code, cap and receipt identities received
separate scoped internal reviews.

The actual addition is the explicit radial/native observation and independent
packing interface, with its conditional law and complete costs. Positive
rejection, bounded-mean FORS and Gaussian sampling are established machinery.
Priority for the combined interface is not established. General dense N687
remains open.

## 2. A consequence that controls unbounded observables

For a fixed rho-contractive g, define the precise target kernel

    K_g(x,.)=N(m_g(x),sigma^2 I),   m_g(x)=E g(x+G).

It has a unique invariant law pi_g. This is the target declared by the
construction; it is not identified with an unsmoothed Gibbs measure or a
deterministic mean fixed point.

A per-step W2 error eta gives after T steps from zero

    W2(Law(X_T),pi_g)<=rho^T B+eta(1-rho^T)/(1-rho),

where B is acquired from g(0) and supplied constants. An error e controls
linear/unit-Lipschitz observables and the squared norm through

    |E||X_T||^2-E_pi_g||X||^2|<=e(2B+e).

This explicitly controls the chosen scientific consequence. Relative rare
probabilities, hitting-time means and arbitrary unbounded costs are outside
that guarantee.

The local one-observation implementation executed 256 independent 96-variable
chains for 10 steps, using 100267 native values and 9625632 scalar answers.
Its proved ideal per-chain stationary W2 bound is .0639181257892 against
target .1. The valid paired implementation used 676422 native values. These
are conditional-law and moment bounds; they do not assert independence from
the sampler's own acquisition transcript.

## 3. Replace exact locality by an acquired consequence certificate

The next attack did not try to infer exact absent dependencies from finite
data. It proposed an explicit cheap surrogate h and acquired the residual
that controls its stationary consequence:

    r(x)=m_g(x)-m_h(x),
    R^2=E_(X~pi_h)||r(X)||^2,
    W2(pi_h,pi_g)<=R/(1-rho_g).                     (1)

The contraction argument in (1) is conventional. The new operational task is
to acquire R without an oracle for either hidden averaged drift and without
confusing a small raw variance with a small conditional mean error.

At an independently prepared candidate state X, acquire m independent native
residuals D_j=g(X+G_j)-h(X+G_j). Use the standard all-pairs U-statistic

    V=[||sum_j D_j||^2-sum_j||D_j||^2]/[m(m-1)].

Its conditional expectation is ||r(X)||^2. Gaussian Poincare and a known
Poincare constant C for the candidate population give, for v>=Lip(g-h),

    Var V <= v^2(4C+4/m)R^2+2d v^4/[m(m-1)].       (2)

Independent groups and an explicit one-sided median inversion turn (2) into
a finite confidence upper bound for R. Fresh validation after freezing h
allows data-dependent candidate learning without a candidate-class union
bound. Every validation center must actually be prepared independently.
Exact finite candidate chains have a proved Poincare constant; a capped
approximation does not automatically inherit it. An observable abort can
instead make validation inconclusive, using the exact-law coupling.

The construction also handles bounded vector-value errors by a pathwise
upper correction to each statistic. That error warranty remains supplied;
the count of calls does not acquire it.

### Complete learned workflow executed on a dense source

The hidden source is a 96-variable conservative globally .5-Lipschitz field
with a dense orthogonal mixture of nonlinear coordinates. The learner
receives only original values and the declared contraction warranty. Its
candidate class is diagonal affine, proposed without claiming that the
original system is diagonal.

One anchor and 4096 symmetric probe pairs acquire a clipped least-squares
candidate. Its actual rho_h=.25145885649511934 follows from its constructed
coefficients. Its invariant Gaussian has explicit mean and diagonal
covariance, so the conventional direct Gaussian sampler is used. A fresh
holdout has 9216 independent candidate states and 128 native inner values
per state, arranged into nine independent confidence groups.

| Resource or consequence | Executed value |
|---|---:|
| Candidate acquisition, original vectors | 8193 |
| Independent validation, original vectors | 1179648 |
| Complete original vector values | 1187841 |
| Complete scalar answers | 114032736 |
| Certified stationary W2 per output | .45735537758574524 |
| False-certificate probability bound | 1/512 |
| Squared-norm expectation error bound | 9.46545546973607 |
| Fresh production outputs | 8192 |
| Further original values for production | 0 |

Outputs are independent conditional on the acquired model. Before conditioning,
sharing a random learned model can correlate them. The stated confidence is
an unconditional false-release bound over training/validation, not posterior
coverage conditional on release. The per-output W2 bound grows by at most
sqrt(M) for a conditional M-output product. Monte Carlo estimation error is
separate.

The direct raw-RMS certificate on exactly the same data gives stationary
bound 1.212224450946256, missing the .5 target. The conditional mean-energy
statistic resolves cancellation that a raw residual norm cannot. An equally
informed existing method can adopt this statistic and receives the same
guarantee; the estimator itself is conventional.

The proof, candidate acquisition and fresh-validation bridge were independently
reviewed. The saved prototype is floating execution of an ideal-value/random
primitive theorem, not a finite-bit continuous-TV certification or physical
instrument experiment.

## 4. The strong conventional route wins the initial first-batch comparison

Ordinary Gaussian-smoothed empirical drift is a much stronger baseline than
the elementary sample-mean RMS bound suggests. Current Paulin--Whalley
(July 2026) convolution theory gives, using only the same global L,

    eta(q)<=sqrt(d log(2)) L^2/(q sigma)

for q fresh native values in a step. A finite deterministic allocation of
accuracy across contracted steps chooses

    (q_1,...,q_11)=(1,1,1,1,2,3,3,5,7,10,14).

This ordinary sampler was executed on the identical dense source with the
same access, target W2 .5, and 8192 independent outputs.

| Complete route | Original vectors | Scalar answers | Per-output W2 bound |
|---|---:|---:|---:|
| Current conventional Gaussian-convolution route | 393217 | 37748832 | .4953566680 |
| Acquired candidate plus independent validation | 1187841 | 114032736 | .4573553776 |

The conventional guarantee is deterministic given its ideal premises; the
learned certificate also has its stated statistical failure budget. At this
batch size, conventional sampling uses about one third of the original
queries. It should be preferred for that task.

For these explicit implementations the conventional original-query cost is
1+48M, while the learned route pays 1187841 once and then no original values.
The latter first becomes cheaper at M=24747. This is an accounting crossover,
not a lower bound on any method, a universal economic threshold, or an excuse
to ignore validation and training. Both still pay random preparation, source
arithmetic, model computation, reading/output and precision costs. A correlated
long trajectory is a distinct comparison when independent samples are not
required.

## 5. Useful failures and retained capital

The path-clock attack has a sharp new warning. In one dimension an actual
martingale clock Q completes g(B_1) to the desired Gaussian. Replacing it by
E[Q|B_1] preserves covariance but changes the fourth centered moment to

3 sigma^4-3 E Var(Q|B_1).

The deficit is strictly positive for g(z)=max(z,0), the gradient of a C1,1
potential. Better estimation of the wrong averaged object cannot repair the
joint-law failure. The ordinary proof is preserved separately.

Other scoped results remain reusable: independent affine replicas retain a
positive fourth cumulant; small off-support pick-freeze variance can coexist
with an order-one Gaussian mean error even for a conservative Lorentz-cone
projection; exact mean agreement does not license bounded local packing.

The coarse lower-bound branch now also covers entrywise nonnegative PSD
contractions and finite-time killed reversible semigroups, using a padded
reversible clock. It needs a growing alphabet q=2d+5 and charges informative
preparations. At constant prediction accuracy and polynomial witness length,
it forces exponentially many such preparations. It does not establish a
fixed-alphabet PSD theorem, cheap preparation of its large common state,
or a universal ceiling under stronger access. This new scope received a
substantive independent review.

## Current scientific position

The construction has progressed from supplied local structure to an actual
proposal--validation--reuse pipeline and stricter source correction for a
dense source. It provides an acquired consequence and noise interface beyond
exact locality, while keeping
conventional positive factories, regression, U-statistics, perturbation
theory and Gaussian convolution where they are strongest.

The central unclosed obligation is stronger than making this particular
example cheaper: discover compact executable drift representations for
difficult sources, with complete acquisition and reuse costs that remove a
major scientific bottleneck. A direct explicit drift candidate b(x) already
has a proved validation variant with no nested surrogate-mean oracle. General
dense N687, efficient nonlinear recursive closure, finite-bit law guarantees,
and guarantees for critical/rare-event observables remain open. This tranche
does not claim the civilisation-scale mission is solved.

## Proof and execution map

- branches/gaussian_completion/LOCAL_GAUSSIAN_MEAN_THEOREM.md
- branches/passive_bridge/ONE_OBSERVATION_EXACT_COMPARATOR.md
- branches/passive_bridge/ONE_OBSERVATION_CONTRACTIVE_CONSEQUENCE.md
- branches/gaussian_completion/ACQUIRED_STATIONARY_RESIDUAL.md
- branches/gaussian_completion/STATIONARY_RESIDUAL_USTAT_REFINEMENT.md
- branches/gaussian_completion/LEARNED_STATIONARY_SURROGATE.md
- branches/gaussian_completion/ACQUIRED_NOISE_ENERGY.md
- branches/passive_bridge/PAIRED_ENERGY_AND_CONTROL_VARIATE_CHALLENGE.md
- branches/gaussian_completion/ACQUIRED_ACCURACY_INTERFACE.md
- branches/gaussian_completion/NONLINEAR_CANDIDATE_ACCURACY_THEOREM.md
- branches/passive_bridge/STRICT_PW_COMPARISON.md
- branches/gaussian_completion/GAUSSIAN_CONVOLUTION_BASELINE.md
- branches/passive_bridge/PW_GAUSSIAN_SAMPLE_AVERAGE_COMPARATOR.md
- branches/gaussian_completion/PATH_CLOCK_CONDITIONAL_MEAN_FAILURE.md
- branches/passive_bridge/PASSIVE_PADDED_CLOCK_LOWER_BOUND.md

Executable Python, frozen JSON receipts and output arrays sit beside the
proofs. Scoped reviews are under branches/different_opening and
branches/rare_event_bridge. SOURCE_NOTES.md records current Astra and primary
literature retrieval. Earlier composition proofs and receipts are retained.
