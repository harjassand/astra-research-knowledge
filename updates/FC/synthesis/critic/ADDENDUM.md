# Adversarial review of the FC integration deductions

13 October 2026. Same-team independent reconstruction and countertests;
external correctness, scientific priority and real-system usefulness remain
UNKNOWN. This addendum supplements the frozen source review in `REPORT.md`.
Exact reviewed versions and ranges are in `ADDENDUM_INPUTS.json`.

## Sequential certificates and rare-overlap lower bounds

The root proof's uniform-Beta factorial formula and uniform-Dirichlet formula
are likelihood mixtures with the stated normalization. They give nonnegative
martingales at interior true probabilities and supermartingale boundary
interpretations. The stopped first-crossing argument is valid. Inverting them
gives an event simultaneous over all observation times. This event can be used
for every later diagonal design without a design-count multiplicity penalty.

The source histogram operation needs a confidence *set*, so the derivation
applies to either the nonlinear Dirichlet region or per-label intervals plus
the simplex. Only the latter keeps the source's linear-program form. The
binary feasible latent range is correctly
`[max(0,l-(1-1/C)), min(1/C,h)]`. Actual fixed-reference Gibbs sampling,
independence and a jointly valid coherence/calibration budget remain premises.
Changing gate settings changes the law; a fixed-N kinetic bound is not made
anytime-valid by applying the label confidence sequence.

The rare family is consistent in the same charge-one sector of two fermion
modes and has T=0, C=1. Its common intervention has energy scale B, growing
like m. The two free-energy signs are opposite with margin at least
`log(10/7)/(2 beta)`, although the reference rare probabilities differ by only
`theta=2^-m`. These are observation-interface lower bounds, not a hard
Hamiltonian-solver example: the complete reference Hamiltonian is excluded
from the supplied inputs.

The first-mismatch coupling remains valid with random stopping. The event
that draw j is requested is predictable from preceding data. Along the p0
run the expected disagreement count is `theta E0 N`; without a disagreement
before that stop both transcripts and outputs are identical. This proves
the stated TV bound, including infinite expectation as a trivial case.
The UNKNOWN allowance and error constants follow from the event "decide
positive". Unlimited abstention correctly evades the bound.

The tilted-label separation is exactly `1/[(3-2theta)(2-theta)]>=1/6`.
An exact or TV-approximate target-label sampler therefore obeys the stated
reference-shot lower bound. This prevents treating a Bernoulli factory as a
free amplifier of unsampled rare weight. It does not contradict the collision
sampler, whose input/envelope/cost contract differs.

Independent exact checks cover 264 Beta martingale recurrences, finite-horizon
crossing probabilities, 84 Dirichlet recurrences, 504 binary latent
optimizations, 19 rare families and their stopped-transcript examples. Infinite
horizon and arbitrary-procedure conclusions rely on the written proof.

## Activity entropy budget and common-latent contrasts

The exact entropy identity in `ACTIVITY_COHERENCE_BOUND.md` checks algebraically.
Pinching makes `Tr rho log sigma=Tr sigma log sigma`; Gibbs entropy then gives
`log(ZH/ZD)=beta*a-D(rho||sigma)-D(sigma||rho_D)`. Measuring the mathematical
POVM `(I±T/K)/2` compares probabilities `(1±a/K)/2` with the fair coin and
lower-bounds the first relative entropy by f(a/K). The POVM is a proof witness;
it does not require a newly implemented measurement beyond the supplied
kinetic expectation.

The Fenchel maximum of `beta*a-f(a/K)` is `log cosh(beta*K)`. The observed
activity bound can be smaller than both original budgets. For uncertain
activity, the maximizer is the interior `K*tanh(beta*K)` clipped to the feasible
interval. Using only its largest endpoint would be unsafe. K=0, norm/temperature
uncertainty and inconsistent negative upper bounds are correctly separated.
This restricted scalar improvement uses established relative-entropy and
data-processing ingredients, with priority unresolved.

`SHARED_LATENT_CONTRAST.md` correctly distinguishes the reference budget from
both target budgets. Reference kinetic information does not automatically bound
the counterfactual target activities. The unchanged microscopic norm graph
can supply both target budgets. Scaling the true weights down to mass
`1/C_ref` is safe because the scale factor is at most one and preserves ratios.
The ratio bounds and both Charnes--Cooper transformations follow with the
stated confidence region. Only the outer-polytope optimization is sharp;
sharpness over physically compatible quantum systems is unproved.

The four-label control has correct symmetry, norm budget and sign. An
independent rational argument proves its shared lower contrast endpoint is
positive using `exp(16)>10^6`, `exp(1/2)<2`, and
`(101/100)(100/103+8/10^6)<1`. Independent interval subtraction straddles zero.
This establishes an information improvement within the declared supplied
contract, not an acquired material or strongest-method advantage.

The critic independently checks 80 complex block Hamiltonians for the entropy
identity and activity inequalities and the resonant two-level equality.
Floating checks are diagnostics. The strict shared-control sign is separately
supported by rational comparisons, rather than only by LP eigenvalue output.

## Binary population-conditioned compression

The later root proof `BINARY_COHERENCE_COMPRESSION.md` survives an independent
complete reconstruction. Its Heisenberg map has the stated positive Choi block
on `|0> tensor H0` plus `|1> tensor H1`, because B/K is a contraction, and is
zero on the complement. It is unital, so its adjoint is a legal CPTP map.
The compressed qubit preserves the measured diagonal and has off-diagonal
real part `-a/(2K)`. Positivity supplies the necessary feasibility condition
`a/K<=2 sqrt(p(1-p))`. The compressed pinched state is the diagonal qubit.

Relative-entropy data processing and the qubit entropy formula therefore give
the claimed d_p(a/K) penalty. The construction needs no physical implementation
of the analytic channel and no new state tomography. The entropy lower bound
is sharp for abstract real-coherence qubits; the full partition bound discards
another relative entropy and is correctly not called minimax sharp.

The x derivative proves d_p(x)>=f(x), and its bias derivative has the right
sign because atanh(r)/r increases on [0,1). Within a rectangular uncertainty
set, the p nearest 1/2 has the weakest penalty and widest feasible activity
range. Maximizing the remaining concave activity exponent is sound. Endpoint
limits, K=0, empty feasibility, coefficient precision and more general correlated
uncertainty still require the stated explicit handling. This is a bounded
certificate improvement of at most log2 in the entropy subtraction, not removal
of a rare-weight, equilibrium or large-coherence obstruction.

Independent critic fixtures reconstruct 48 complex binary Choi witnesses,
compressed Gibbs/pinched states and partition inequalities, plus 102 bias-order
cases. They import no root or producer code and passed. These finite floating
tests support the implementation; the written universal proof is the authority
being internally reviewed. Known coherence compression and UCP/data-processing
tools remain credited; no novelty or physical capability gate is closed.

## Preparation obstruction

The fixed pair-charge four-mode construction in
`PREPARATION_OBSTRUCTION.md` has the stated reference partition functions and
target ratios. The elementary exponential bounds prove opposite free-energy
signs with margins exceeding 1/4. A-only controls cannot leave s=0, where the
two Hamiltonians coincide exactly; arbitrary local data there are identical.
Both T=0 and knowledge of the intended total charge can therefore coexist
with a completely unacquired hidden Gibbs sector weight.

The common number-conserving bath tunnelling has norm epsilon. Operator-norm
free-energy continuity preserves the signs for epsilon<1/16. Duhamel bounds
and a hybrid over A-only instruments give the conservative `4 epsilon t`
distinguishability bound between the two perturbed models. The resulting
Omega(1/epsilon) time lower bound charges total Hamiltonian interaction time
under that access. It does not prohibit bath control, extra preparation
ensembles or complete Hamiltonian information; those change the interface.

This construction uses two-body density terms and differs from N786's
growing-order vacuum construction. It supports the acquisition gate, while
refuting no theorem that assumes actual coupled Gibbs observations.

## Collision information, acquired late-time approximation and converter gate

The Gaussian overlap integral in `TRANSIENT_INFORMATION.md` is correct under
the positivity condition D<mu. Its power series has positive coefficients;
mean conservation cancels the first term and the second-moment decay bounds
all remaining terms by `B exp(-2t/3)`. The product chi-square and testing
argument then gives the stated fixed-N raw-velocity observation lower bound.
This is neither an adaptive expected-shot theorem nor a lower bound on a
model-aware solver. The quartic statistic supplies the matching exponent
under the separately known mean/variance premises.

The median-of-means acquisition and late-time Gaussian approximation have
correct constants. They validate only a conditional one-output law given a
shared calibration event. The proof explicitly charges the M-output product
error and unconditional dependence introduced by shared calibration. It does
not obtain a latent mixture sampler, validate the collision model, or replace
the source's exact transient operation under the same guarantee.

The reusable signed-density converter contract is sufficient. Bounded unbiased
operator actions from N687 do not supply a bounded density ratio, positive
pointwise lower envelope or finite weighted integral. The expected/every-run
query distinction also remains. The finite-word boundary obstruction is sound
for the stated coin-only access. The candidate bridge should remain a candidate.

Four additional critic quadratures independently compare the t=0 mixture
chi-square with its closed Gaussian overlap formula and the claimed bound.
An exact Gaussian polynomial-moment calculation verifies the quartic variance
constant. These are finite diagnostics, not proof of all t or of a new solver.

## Phonon geometry, Gaussian selection and adaptive global writing

The closest-convex-hull-point proof supplies the exact max-min linear velocity
margin inside a supplied mass-weighted control ball. The optimal Te A1 azimuth,
collinear zero-momentum relaxation and sqrt(2) energy-efficiency difference
follow. A ball or mode subspace does not acquire a physical actuator, mode
phases or a retained-event law.

The final finite-angle Eq.(2) correctly uses linearized D^(1) and baseline
S^(0), with dominated smoothness and explicit odd/even remainders. This scope
is essential. For example `g(T)=T^3` gives the exact half opposite-shift
difference `3T^2 a+a^3`, not only `3T^2 a`; the independent rational fixture
records that falsifier of an unqualified nonlinear equality. The corrected
coefficient identity and the cubic total-yield signature survive. An axial
beam's average null still requires angular/symmetry conditions; it is not an
axial impulse at every angle.

The Gaussian ROC inequality is the correct sharp Neyman--Pearson frontier
for the *entire retained-response state* with a common kernel. Applying it to
one projected velocity when the reaction depends on omitted neighbours or
electronic state would be invalid. The source correctly excludes that transfer.
The thermal scalar example and tail-rate ceilings are conditional controls;
neither a Gaussian Te covariance nor a retained cross section was acquired.
Sixteen critic logistic-response quadratures satisfy the same frontier.

The adaptive global-write bound has the correct Bellman/supermartingale
residual. Per-remaining-site intensities and `rt<=R ru` give
`L V(k)=km V(k-1)(rt-Rru)/(kR+m)<=0`. Constant saturating rates attain the
product formula in its optimistic irreversible model. It allows instantaneous
event-conditioned stopping, so the one-target R>=99 criterion has a different
contract from the source's fixed-dose 458.2106 requirement. This is an
interface distinction, not a correction to the source arithmetic.

The global fidelity, harmonic-dose and latency statements retain their model
premises. They do not apply automatically when healing, site removal, evolving
reaction branches or correlated events alter the full configuration kernel.
The critic independently checked 432 exact rational generator residuals,
including saturation. No measured Te rate or technology-readiness gate follows.

## Disposition

Retain the positive restricted interface improvements, precise negative
transfers and candidate bridges together. None provides cheap universal
preparation, a physical retained-write mechanism, a full-law N687 compiler,
finite-bit exact collision sampling or demonstrated material advantage.
Internal proof agreement and tests must remain distinct from independent
external validation and historical novelty.
