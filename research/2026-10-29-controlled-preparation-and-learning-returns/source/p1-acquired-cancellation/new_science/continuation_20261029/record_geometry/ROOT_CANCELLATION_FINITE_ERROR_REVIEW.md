# Focused review: acquired hidden-response cancellation

29 October 2026. Actual internal review by the complementary record-geometry
researcher. Not external peer review, formal verification, apparatus validation
or historical-priority determination.

Reviewed input: ACQUIRED_HIDDEN_RESPONSE_CANCELLATION.md, SHA256
`17507118b24da8848620b3d5c753b93d56846bc6f9e7bb8e8e3752619f667bcd`.
The exact reviewed bytes are preserved as REVIEWED_ROOT_17507118b24d.md.

## Verdict

The core acquisition identity, convex cancellation theorem, fixed-library
static-H KL bound, reference-preparation composition and infinite-rank example
are sound at the written mathematical interface. Sections5--6 require one
explicit qualification before a general data-selected deployment claim:
conditioning on calibration/design data can change deployment H's density.
A simultaneous Gram confidence event does not remove that selection effect.
The root was notified with the precise correction below. No other mathematical
error was found in this focused review.

## 1. Finite confidence

If every entry of the true H is within d of Hhat, then for every simplex p,
|p^T(H-Hhat)p|<=d because sum_ij p_i p_j=1. This is simultaneous for ALL p,
including a data-selected p on the same event. Since p^T H p>=0, the true upper
bound p^T Hhat p+d cannot be negative on that event; max(0,.) is harmless.
An indefinite empirical matrix does not make the design optimization convex,
so the PSD regularization/confidence-set qualification is necessary and given.

For known mu_a, raw-frequency errors eta imply L error eta/mu_a and individual
clipped conditional-mean error eta/mu_a. The k product means therefore incur
at most2k eta/mu_a, giving d=(1+2k)eta/mu_a. Weighted return loops need their
actual bounded report range in eta. Estimated masses need a genuine floor
and ratio interval, as stated. Nothing here establishes generic exact zero.

The n*zeta/2 selector-implementation error is valid when l1 probability error
is uniformly <=zeta at every label/history and actual selection/native calls
satisfy the fresh-randomness interface. It is ordinary TV telescoping.

## 2. Static-H complete-record KL

Fix the compiled library and reference matrices. For a row r=(ell,a), write
P_r(h) for the real outcome law and Ctilde_r for its positive reference.
Comparing laws of (H,Z,Y0,record) with identical initial joint distributions
cancels initial KL. The conditional transition KL at each stage is
D(P_r(H)||Ctilde_r), even when the outer policy depends on arbitrary Z and the
entire prior record. Conditional native Markov evolution and fresh discarded
selectors are essential here.

Use D(p||q)<=sum_b(p_b-q_b)^2/q_b and q_b>=tau. Since row costs are
nonnegative, the chosen cost is bounded by the sum over all fixed ell,a.
H never changes; its unconditional marginal therefore stays the initial one,
even while its posterior given the record changes drastically. A genuine
marginal ceiling d rho_H/dnu<=B controls the expectation of that sum. Finally
E_nu(P-Ctilde)^2=E_nu(P-C)^2+(C-Ctilde)^2 for C=E_nu P.
Pinsker supplies exactly the factor1/2 under the square root in equation(7).
The result is valid for arbitrary Z, including Z=H and infinite-valued Z.
No conditional density of H given Z is needed for a FIXED library.

If H evolves, stationary H marginals of individual uncontrolled operations do
not suffice for this argument under feedback. The draft correctly excludes
that extension. Positive Ctilde support, or actual exact matched zero support,
is essential. Small measured mean-square error does not warrant zero columns.

## 3. Required calibration/design qualification

If the compiled probabilities, reference matrices or chosen library depend on
calibration data D correlated with deployment H, the proof must be applied
conditional on that configuration. The prior unconditional density ceiling
need not survive this conditioning. Uniform Gram confidence only bounds
integrals of each fixed design's residual with respect to nu. It does NOT
bound the residual of a hidden-correlated selected design at its selected H.

Valid sufficient options are:

* Treat the library and reference as fixed before choosing the deployment
  source, with the stated actual H marginal ceiling.
* Use an independent deployment specimen/source relative to the data-dependent
  configuration, retaining its warranted H ceiling.
* Require dLaw(H|D)/dnu<=B almost surely for the calibration/configuration data,
  then allow arbitrary further Z correlated with H. The theorem can be applied
  conditional on D; confidence failures are still charged separately.
* Include every selectable configuration in a finite predeclared action library
  and pay the corresponding sum over that whole library. A separate valid
  uniform pointwise envelope is another possible route.

Exact finite counterexample to dropping this distinction is saved in
CALIBRATION_SELECTION_COUNTEREXAMPLE.json. H is uniform on100 values, D=H,
and design c uses symmetric binary flip probability

    p_c(h)=1/2+(1/4)(1_{h=c}-1/100).

Each fixed design has row mean1/2 and row residual energy99/80000. Choose c=D.
The initial unconditional density ceiling is B=1, but the deployed flip
probability is always299/400. For one stage the joint-record TV from the
mean reference is99/400=0.2475, whereas an incorrectly unconditioned application
of(7) has squared bound99/40000 and bound about0.04975. Conditioning on D
correctly requires B=100. Including all100 designs in the certified menu also
repairs the bound. This is a selection-interface counterexample, not a
counterexample to the fixed-library theorem.

## 4. Preparation and reference identity

For a fixed positive reference reset Ctilde_R with coefficient theta, the
coarse process starting at arbitrary Y0|Z contracts to its stationary visible
law by theta^m. This supplies the independent-of-Z target. Comparing the real
m+n-call process to that coarse process by(7), discarding reset records, and
then applying data processing proves(8). The reference is a positive Markov
law and is not automatically the original physical system at mu. The draft
states this distinction correctly. Two physical preparations can each be
compared to the SAME reference and their two errors added.

At exact cancellation, label-independent mixtures preserve mu; an ergodic
compiled reset therefore targets mu_Y. Arbitrary old microscopic information
is harmless because the compiled output kernels ignore it exactly. For
row-dependent mixtures, separate target-stationarity checks are required and
are explicitly retained. Retained reset histories or private selector keys
would change the observation interface; they must actually be unavailable.

## 5. Source/calibration and example checks

The independent baseline ensemble premise is necessary: a single forever-
frozen H specimen cannot provide iid nu calibration data merely by waiting.
The draft explicitly uses an independently prepared ensemble or another
justified source protocol and disclaims the single-device shortcut.

All four flip probabilities lie in[1/20,9/20]. The generator formula yields
symmetric continuous-time flips over the common duration t with exit rate
at most log(10)/(2t). The coefficients cancel exactly for A and B. Their
centered factors are7/10 and2/5. Eight B calls from an arbitrary binary
initial distribution give TV at most(1/2)(2/5)^8=0.00032768 to uniform, and
all later compiled records contract that discrepancy.

The autocorrelation moments of lambda(h)=4/5-h/10 form Gram matrices of
polynomials under a continuous full-support measure. Every finite such Gram
is positive definite, proving unbounded Hankel rank for the raw operation.
No finite linear predictive model reproduces its complete raw records.
The compiled language differs physically, so its rank2 does not contradict
that statement or the connected-source smoothing obstruction.

Replacing slopes by absolute values preserves each isolated raw operation's
whole baseline continuous-time law via h->-h, while cross-control inner
products change. The stated mixed return probability difference1/100 and
positive-slope mixture floor1/600 are correct. This excludes convex one-call
mixtures, not sequential control words.

The selector exposure example is also correct: even when averaged next labels
agree for H=+1 and H=-1, revealing J gives joint(J,next label) TV3/20 for A.
Thus literal selector disposal and exposed-duration padding are substantive
parts of the mechanism, with their real costs retained.

## 6. Scope of acceptance

Accept after the calibration/design density qualification is made explicit.
This review did not independently run the root executable, certify finite-
sample acquisition end to end, prove historical novelty, or identify a
practical device. Established covariance, convex separation, controlled
lumpability, chain-rule KL and finite-state mixing remain credited tools.
