# Finite acquisition, preparation, and execution costs

29 October 2026. Root ordinary construction for the actual-operation theorem.
No physical observations were collected. A supplied source contract and an
actually acquired confidence interval are different things throughout.

## 1. Fixed dictionary and finite experimental menu

Take s actual reversible operations INCLUDING BASELINE, with known visible
square-root weight ratios at most R. Normalize each weight by min_a w_j(a)=1;
this changes no reversible measure or operator, and bounds its center weight
by R^2. Use
source exit ceilings at most Lambda, and calibrated exponential-clock rates at
least alpha_min. Select r label-local future-word features, containing the label
indicators and at most L pulse stages each. Their values f_i are in[0,1], but
their conditional values are hidden. The actual adjoint experiment supplies
their products. A complete moment trial uses at most A=2L+2 pulse stages and
a known finite number n_read of visible label readings. Its recorded scalar
has magnitude at most

    W=R^(2L+2).                                               (1)

The center weight is included. This dynamic range and its calibration are paid;
a small r or a retained output bit does not pay for the acquisition history.

For every test pair i<=j, a no-central-pulse trial supplies G and the center
label, hence every G_j. One- and two-stage central trials supply K_j,D_j for
each operation. A conservative number of distinct settings is

    M_settings <= (1+2s) r(r+1)/2,
    M_entries <= 3s r(r+1)/2.                                 (2)

Use N genuinely independent baseline stationary preparations PER setting.
No hidden same-state copy is needed within a trial, but independent stationary
trials are not created by observed mixing. Test clocks and random bits are fresh.
Shared coefficients can be acquired from one trial; independence between entries
is unnecessary for the confidence union bound.

If scalar statistical error is at most eta_stat, the conservative Hoeffding
schedule

    N >= (2W^2/eta_stat^2) log(2M_entries/delta)              (3)

makes all scalar errors <=eta_stat with probability >=1-delta. This bound even
allows signed reports in[-W,W]; purely indicator words permit a better factor.
It is sufficient, not optimal. Actual data may produce a large defect or an
ill-conditioned Gram matrix; (3) does not guarantee a successful small model.

## 2. Finite clock construction and physical errors

An ideal exponential clock E with rate alpha is rounded UP to a grid Delta
and censored after T_c=M Delta. Its ideal grid probabilities are
exp[-alpha(j-1)Delta]-exp[-alpha j Delta], j=1,...,M, plus the tail flag.
Use b independent fair bits and monotone integer CDF thresholds to implement
a rational categorical law. Outward exponential intervals give certified
thresholds; residual threshold uncertainty is included in the bit-error budget.
CDF floor rounding yields TV <=(M+1)2^(-b). An overflow flag sets the recorded
trial value to0; it must not be silently discarded or resampled as if ordinary.

For one pulse, ideal-to-grid rounding changes a bounded state transition by at
most 2Lambda Delta in the bounded-test norm. Conditional on no earlier mismatch,
couple the endpoints and their labels. Successive independent stages therefore
give the conservative expectation error

    eta_clock <=2W A[exp(-alpha_min T_c)
                 +(M+1)2^(-b)+2Lambda(Delta+delta_t)].       (4)

delta_t is a uniform calibrated timing error. Use each operation's own cap/rate
for a tighter sum. This proof concerns the finite endpoint word actually used
in acquisition; it does not license deletion of an additional observed clock
transcript in a different service task. Gamma-two pulses use TWO independent
clocks, not twice one draw. The recorded elapsed times, bits, and overflow
flags remain part of the acquisition resource record.

If each label report has a conditional error probability <=eta_sensor, its
contribution is <=2W n_read eta_sensor by a coupling/union bound. A supplied
uniform TV error eta_act per physical stage contributes <=2W A eta_act.
If a RATEWISE discrepancy sup_x sum_(y!=x)|q_xy-qtilde_xy| is supplied,
integrate that path-coupling intensity over the capped duration to obtain
eta_act. A difference of total exit rates alone is insufficient: equal total
rates can have different destinations. A claim about
visible energy alone is not that calibration. Arithmetic/report-weight errors
are separately bounded by eta_arith. Thus an entrywise error budget is

    eta=eta_stat+eta_clock+eta_sensor_total+eta_act_total+eta_arith. (5)

All constants refer to actual qualified clocks, sensor, actuator, and source
contracts. Neither a full rate ceiling nor microscopic detailed balance is
inferred from a finite fitted record.

## 3. Turning noisy moments into an honest defect upper bound

Symmetrize the acquired Ghat,Khat,Dhat. Let their certified operator errors be
eG,eK,eD; entrywise eta gives each <=r eta (with weighted reconstruction
factors included if entries are reused). Suppose lambda_min(Ghat)>=g>eG,
and put g0=g-eG. Then G>=g0 I and

    ||G^-1-Ghat^-1|| <=eG/(g g0).

For Rhat=Dhat-Khat Ghat^-1 Khat, a deterministic true-residual error is

    eR=eD+eK(2||Khat||+eK)/g0
                +||Khat||^2 eG/(g g0).                      (6)

Insert KG^-1Khat between the products to prove the bound. Therefore

    epsilon^2 <= max(0,lambda_max(Rhat)+eR)/g0.               (7)

Numerical eigenvalue/inverse intervals must also be outward-certified. A negative
empirical eigenvalue is not negative physical leakage. If an asserted certified
interval is inconsistent with PSD, report the failed model/calibration premise;
do not turn it into an exact zero by clipping. The safe spectral floor a from
the source rate ceiling supplies d=alpha epsilon/a^2 and compression bias
alpha epsilon^2/a^3. The stronger acquired c_min formulas may be used only with
their own certified lower bound.

The label-local dictionary makes the coordinate label projectors known block
matrices exactly. G is block diagonal across labels, and constant1 is the known
sum of the retained label-indicator columns. This avoids treating an approximate
label-invariance test as exact. Near-dependent features may be omitted before
validation, but their discarded physical effects are then tested by the residual.

## 4. Inverse and execution errors

The true compressed resolvent is C=G^-1K; set Chat=Ghat^-1Khat. A Euclidean
matrix error bound is

    eC=eK/g+eG(||Khat||+eK)/(g g0).                          (8)

If sigma_min(Chat)>=c>eC, its generator inversion error is at most

    alpha eC/[c(c-eC)].                                     (9)

Convert this to the true weighted norm by multiplying by
sqrt((||Ghat||+eG)/g0), and add the true compression bias above. Arithmetic
errors in every inverse and product are included. Ordinary certified linear
algebra supplies the bound; floating success alone is not certification.

Initial functional ell^T=c_1^T G has NUMERICAL error in the baseline dual norm at most
||c_1|| eG/sqrt(g0). Propagate generator, initial, and numerical killed/jump
block errors by ACTUAL_OPERATION_ALGEBRA.md equation(5). Weight conversions
between operations use their known R_j. Apply a consistent label block
representation; a signed predictor is not silently declared a positive model.
This functional error does not certify physical service preparation. Matching
only retained moments of another initial law is insufficient. Retain baseline
pi preparation, a warranted full-state TV error, or the appropriate joint
calibration/service bound. Solver propagation errors are separate from generator
errors unless a valid effective-generator perturbation theorem is supplied.

For fixed segment controls and a specified snapshot word, ordinary r by r
matrix exponentials/products suffice. Whole feedback payoffs need the actual
policy description, its observation interface, and an appropriate controlled
solver. General Borel policies need not be computable. Jump-series truncation
has an explicit tail from the same bound sum_m k(k-1)^m J^m T^m/m!;
time integration and payoff discontinuities still need certified handling.
No universal favorable runtime is claimed. For a bounded payoff, a uniform
certified scalar error also supports control selection: within a computable
searched policy family, selection regret is at most twice that error plus
the optimization tolerance. This does not search every mathematical policy.

## 5. Full costs and strongest equally informed route

Acquisition needs N M_settings baseline preparations, at most A stages and
n_read sensor readings per trial, and A b random bits. Ideal mean pulse
exposure is <=A/alpha_min per trial, capped exposure <=A T_c. Preparation and
reset time/work, switching, sensor precision, report dynamic range, storage,
arithmetic bit lengths, and calibrated source ceilings are separate costs.
Sample acquisition and aggregation require their own O(N M_entries) scalar
accumulations in this conservative protocol. Ordinary matrix preparation uses
O(s r^3) arithmetic operations plus the cost
of certified precision; this is not a bit-complexity or physical-cost claim.

The same acquired matrices are reusable for new policies without new source
identification, conditional on unchanged physical operations and fresh qualified
service preparation. They do not prepare a hidden physical equilibrium state.
For adaptive feature selection use a pilot/validation split or allocate a
summable failure budget over stages. Reusing one selected fit requires joint
confidence, not multiplying marginal successes. No iid source is fabricated.

An equally informed conventional residual-DMD/observable-operator estimator and
reduced solver should use these same acquired matrices. The proposed gain is
the physical access to hidden conditional inner products and closure, not a
claimed faster inverse or superiority to all conventional system identification.

## 6. Executed fixture and candid limitation

check_pulse_closure.py verifies exact rational identities and a rigorously
enclosed finite-time intervention gap. It is NOT a sampling experiment.
Its eight-state/four-coordinate fixture has a raw Gram condition number of
about 2.17e11 (floating diagnostic), and its first omitted pulse defect includes
128/7358694984207. These are warnings against calling the fixture a practical
sample-efficiency result. Feature depth/conditioning and the conservative
horizon error can make (3)--(9) very expensive. Orthogonalizing the printed
coordinates does not erase the acquisition precision needed to learn them.
The separate interval-code fixture imposes matrix radius 1e-50, while its
illustrative clock component bounds about 8.94e-8. These are independent
component checks, NOT one combined acquisition certificate. No physical
process supplied either precision in this work.

The established consequence is a scoped acquisition/completeness principle and
an honest finite error construction, not a demonstrated operational speedup.
