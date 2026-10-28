# Whole intake of C's completed finite-exposure thermal receiver

**ACCEPTED at the two declared known-model/statistical-plan scopes.**
I whole-read the frozen PROOF, BLUR_PROOF, moment/active acquisition
code and outputs, compile_receiver.py / RECEIVER.json, receive.py,
RESULT, source notes and frozen receipt. I reconstructed the mathematics
and checked the implementation without rerunning a model, quadrature,
trajectory, source case or producer. This is substantive independent
whole intake; it is not a second interval numerical implementation.

The physical classification remains NOT_ACQUIRED. All advertised risks
are conditional on actual records, bath/metric/model, initialization,
electronics, geometry, timing and calibration admission. A Boolean or
file hash does not authenticate those scientific premises.

## 1. Moment and nonlinear exposure inputs

The directed scalar moments are already accepted separately in
MOMENT_REVIEW.md: exact beta=d^2/2 at theta1/Delta.5, 2048-panel
Simpson with per-panel fourth derivative suprema, infinite Gaussian
tails and outward Decimal arithmetic. K3/K2 contrast enclosures have
the correct physical normalization. MOMENTS and ACTIVE_INPUTS retain
the source/version bindings; no scalar input is treated as data.

RELATIVE_BLUR_RECONSTRUCTION.md independently derives the required
covariance positivity by reversible Dirichlet/semigroup calculus,
cooperative flow derivatives and stationary moments. Thus no unchecked
FKG limiting argument is necessary. The exact Duhamel comparison pays
relative, not merely absolute, motion blur. Connected access g>0 is
now explicit, and both assigned paths satisfy it.

A's accepted long-exposure interface is consumed at its actual
M-matrix/one-quartic/bath scope. The K3 numerical packet is unchanged.
K2 obtains its OWN continuant trace/second trace and R²_pp; it does
not copy K3 geometry across the changed shunt. Positive endpoint
resolvent ratios prove the travel survival and its two-moment
retention. The 64 finite known-spectrum modes are also paid and
outward qualified; no spectral oracle or simulated path is supplied.

The Machin remainder and the 50-term cosine remainder bound are valid
on the actual arguments. The endpoint weights are
[1-cos(2j*pi/33)]/33. The positive spectral expressions for harmonic
variance and adjacent covariance are correctly normalized. Correctly
rounded Decimal sqrt/exp with outward adjacent widening is the
declared backend premise, not a floating quadrature assertion.

## 2. Long-window statistics and cross-products

The nonlinear exposure is not Gaussian. Its pointwise product
Brascamp--Lieb/Wiener derivative form is bounded by harmonic V_delta,
using entrywise J<=exp(-Kt) and R>=0. Applying that form to a square
gives Var(F²)<=4V_delta²; electronics give Var(Z²)<=4S_delta².
Endpoint conditioning and the gap pay read correlations. The geometric
sum at spacing delta+1/kappa is bounded by 4+8/(e-1)<9.

For adjacent-product blocks, the Cantelli retention is correct:
delta=mu/4 puts all pair lags below mu/2 and gives the uniform factor
mu²/(mu²+4w). The product-form inequality

    Ecal(Z1Z2)<=2Z2² Ecal(Z1)+2Z1² Ecal(Z2)

gives Var(Z1Z2)<=4S_delta². The no-electronics product has variance
<=4V_delta², so the SAME geometric argument applies at block spacing
2delta+1/kappa. There are TWO actual readouts per block. Centered
independent electronics cancel from the product mean, not from its
variance or from its required PSD bound. Colored/offset noise can
invalidate this mean cancellation and is explicitly excluded.

## 3. Initialization, stopping count and consumer

The zero-start square/product coupling is correctly averaged over the
ACTUAL record. For qd=(1-exp(-kappa delta))/(kappa delta),
M=theta TrR, its per-block expectation is bounded by

    2sqrt(MS_delta)qd exp(-kappa t)
                      +M qd² exp(-2kappa t).

The geometric start-time sum divided by Q is exactly the compiler's
bound. It can qualify t0=0 at these huge Q: the initial transient is
bounded and diluted, not declared absent or stationary. For a general
initial law the separately warranted second-moment bound is necessary.

The Q rule uses 128V/(zeta sL²). At threshold sL/8, stationary
Chebyshev failure is at most zeta/2. The averaged coupling target
zeta sL/16 makes its Markov failure at most zeta/2. Combined score-
mean calibration error sL/8 leaves total error 3sL/8, below the
half-signal decision threshold for either hypothesis. This is uniform
over alpha>=Delta. It is an individual fixed-plan guarantee, not a
joint/adaptively selected guarantee across all listed plans.

The final raw-score/reference mismatch is resolved. Variance JSON
uses RAW Z² with reference V_delta+sigma²; the earlier debiased formula
has reference V_delta instead. Cross uses raw Z1Z2 and its harmonic
cross reference. The consumer follows the final explicit conventions.

receive.py computes interval-midpoint score/reference and charges
both interval half-widths plus the supplied calibration bound against
sL/8. Its sufficient count is in blocks for products and raw reads
for single-read mean/square plans. Extra observations are allowed
only under the same external timing/record contract. It returns no
qualified physical record without supplied aggregates, calibration
and externally warranted access; the admitted-decision branch is
explicitly CONDITIONAL and does not authenticate evidence itself.

## 4. Coarse electronics and calibration limits

The weaker-calibration square rule is sound at the population-mean
contract. With only 0<=sigma_j²<=sigma_max, the raw null mean is at
least V_delta, while the alternative is at most V_delta-s+sigma_max.
Subtracting sigma_max and the reference enclosure width from the
signal gives a conservative gap. It does not subtract an unknown
noise variance. PSD upper bounds still enter the score variance.

K2's positive gap qualifies 937983404 reads and native duration
4.61180307509e11. The K3 version declines this RULE because its gap
is negative. That is not a full-distribution or time-series no-go.
Equality of raw population variances by nuisance compensation is a
moment-contract ambiguity, not equality of all finite-record laws.

The externally supplied COMBINED score-error bound is load-bearing.
Displayed gain/reference sensitivities are one-source statements,
not a joint uncertainty rectangle for K, temperature, clock and
instrument. Changing those quantities can also change the contrast.
The coarse square's reference omits electronics, so its gain number
has the physical-exposure-before-additive-electronics interpretation
Z=G F+eta. A gain applied to the entire raw read would instead need
the noisy-reference upper V_delta+sigma_max in that sensitivity.
Neither interpretation grants an actual calibration certificate.

## 5. Strong actual comparators

ACTIVE_RECONSTRUCTION.md independently checks the finite-U Gibbs ratio,
the U1 sinhc/absolute-Gaussian-moment enclosure, high-force derivative
and shifted-tail bounds, and monotonicity against all alpha>=Delta.
No FDT derivative is silently substituted for finite force. Both
high-force scalar integrals are genuinely paid directed acquisitions.

The SAME-bath mean plan uses a CONTIGUOUS time average with variance
at most [2theta(R²)_pp+Sdet]/T, rather than artificial IID thinning.
The force changes neither the flow-derivative comparison nor the
Brascamp--Lieb covariance bound. Its stationary mean is entrywise
between zero and U R_.p, giving the actual forced second moment
theta TrR+U²(R²)_pp. The compiler uses that forced M, and its averaged
coupling bound, even at U1/g. It does not borrow the unforced burn-in.

The deterministic no-bath comparator receives the SAME one-quartic
promise. Its 100-step rational monotone root bracket, detector-only
averaging and uniform deterministic settling bound are correct. It
is a different bath interface, not T's more restrictive all-quartic
drive plan. Force peak, huge reference displacement and recoverable
loading energy are explicit. Stored bU²/2 is not irreversible work,
holding power or a universal full-cycle energy lower bound.

At K2 the ordinary SAME-bath U1 mean duration 3.56475100481e11 is
already slightly smaller than the calibrated passive variance plan's
3.68319247504e11. U33 reaches the much smaller sufficient duration
2.884301125e8 at its extra peak/range/calibration boundary. Thus no
passive winner over the strong ordinary alternatives is established.
K3 retains exponentially poor sufficient budgets despite the useful
long/short refinement. A's finite-Delta path lower and stationary
local Gaussian-likelihood conclusions keep their distinct starts and
scopes; no g^-4 full-path optimum or finite-Delta likelihood result
is imported from the stationary tangent.

## 6. Costs, wider theorem and final verdict

The actual costs .5826s moments, 1.6925s active inputs and all three
budget/compiler runs (.06487s,.06829s,.08522s) are retained. K2's 93
integer updates and 64 spectral modes are paid source computations.
A's old packet, backend startup, source reads/failures and proof work
do not disappear. No physical readout, calibration, trajectory or new
topology was generated by producer or reviewer.

The known K2 formulas imply delta=Theta(N²), constant retention,
signal Theta(N^-2), S_delta=O(N^-1), Q=O(N²) and duration O(N4), with
O(N² log(N/zeta)) burn-in when needed. The finite reference acquisition
is O(N), not a free all-dimension oracle. These are sufficient
qualified scalings; they do not prove optimality, economical physical
implementation or an unqualified negative-shift/hardware operation.

The completed positive operation is a mathematical finite-exposure,
correlated-record receiver and its calibration alternatives, with
actual scalar inputs and explicit ordinary competitors. All-alpha
here means the SINGLE hidden coefficient ranges over [Delta,infinity)
against reference zero; it is not multi-defect tomography. Bath,
geometry, other-quartic absence, mobility, initial energy, electronics,
gain/reference/clock and actual records remain physical gates. The
frozen packet's NOT_ACQUIRED physical decision and UNKNOWN priority/
practical advantage judgments are appropriate.
