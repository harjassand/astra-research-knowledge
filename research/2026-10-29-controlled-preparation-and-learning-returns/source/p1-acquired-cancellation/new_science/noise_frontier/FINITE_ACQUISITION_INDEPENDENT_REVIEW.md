# Finite acquisition and execution: independent targeted review

29 October 2026. Read the complete new ordinary acquisition note and the new
actual-menu/interval executable. No physical experiment was performed. Exact
inputs and executable receipts are preserved under reviewed_finite_acquisition/.

Ordinary note reviewed SHA256:

    fbdbbc1f30de571116be707ef4082b6fd40505e9f8d7d2363cec5d64a7f0d8dd

New executable reviewed SHA256:

    e170741e395d2495e4858d7d142bb94acf4a1ca914a4a566c9d2592fbc57f7fb

Its fixture dependency, not independently re-audited here, has SHA256:

    bd8e28189e1a634864c08d5a4ab2b26d497f358eceb600c8b2349d27e6b7f961

## Finding and two explicit clarifications

The finite confidence, matrix perturbation, initial-functional and clock-word
bounds are valid at their stated independently prepared, finite report-word
interface. They do not establish the physical source/operation premises.

1. Normalize each known reversible weight so min w_j=1. This is allowed because
   multiplying a reversible measure by a constant does not change its operation.
   With max sqrt(w_j)/min sqrt(w_j)<=R, the center weight is then at most R^2
   and each adjoint endpoint ratio at most R^2, proving W=R^(2L+2). Without
   specifying a normalization, ratios alone do not bound an absolute center
   weight. The intended construction is unaffected by making this explicit.
2. The phrase "exit-rate-difference calibration" must mean a valid ratewise
   coupling discrepancy, not merely a difference of TOTAL exit rates. Equal
   total exit rates can have different jump destinations and different observed
   laws. A sufficient quantity is

       sup_x sum_(y!=x) |q_xy-qtilde_xy|,

   or an independently supplied path-coupling intensity. Integrating this
   over the capped duration gives a valid stage mismatch bound. A scalar
   difference between the two total exit rates does not.

These are physical-interface/normalization clarifications, not changes to the
correct inverse or statistical formulas. Include the baseline among the s
operations when using the printed 3s entry count; otherwise count its G entries
separately or explicitly reconstruct them using label locality.

## 1. Independent trials and Hoeffding

A fixed pair/operation setting produces a bounded scalar in [-W,W]. For N
genuinely independent baseline stationary preparations, Hoeffding gives

    P(|mean-E report|>eta_stat)
                      <=2 exp[-N eta_stat^2/(2W^2)].

Union over the declared M_entries yields the printed schedule. Entries from
one trial may be correlated; the union bound does not require independence
between entries. Independent trials at each setting ARE required. A long
visible record or a good fit does not supply independent hidden preparations.
For an adaptively selected dictionary, fresh validation data or conditional
failure-budget allocation is necessary; the note correctly retains it.

The schedule controls deviation from the physically implemented trial's mean.
Clock, sensor, actuator and arithmetic biases must then be added, as in (5).
Finite sample confidence does not make the true residual small, guarantee Gram
conditioning, or certify exact population closure.

## 2. Finite independent clocks and endpoint-word bias

Rounding an exponential duration upward by at most Delta and recording an
overflow at T_c yields the stated finite categorical law. Integer CDF thresholds
rounded with b fair bits have TV at most M 2^-b; the printed (M+1)2^-b is safe.
Certified exponential evaluation/threshold uncertainty requires its own allowance,
which the note explicitly retains. Independent stages require fresh bit draws.

For bounded-rate CTMCs, coupling along a common path makes an endpoint mismatch
over extra duration d at most Lambda d; equivalently the bounded-test semigroup
norm difference is at most2Lambda d. The printed time term is conservative.
A calibrated two-sided timing error delta_t can be handled by the possible
jump window around the intended endpoint; the stated factor2Lambda suffices.

Conditional on matching earlier endpoints, run the next stage from the same
hidden state with the same fresh command/clock coupling. Union over at most A
stages and use report range [-W,W]. Tail flags, bit-law differences, and timing
rounding then give the stated conservative

    2 W A [exp(-alpha_min T_c)+(M+1)2^-b
                                  +2Lambda(Delta+delta_t)].

Setting the ENTIRE report to zero on overflow is valid and charges tail bias.
Discarding such trials and dividing by the retained trial count would change
the estimand. Reusing one clock twice does not produce S_j^2.

This argument applies to a word of endpoint label reports and known weights.
It does not give TV approximation of a continuous clock-time transcript by a
digital one, or control an arbitrary discontinuous statistic of exact elapsed
times. The source note correctly retains this distinction. Ordinary time records
remain acquisition resources even when the moment estimator ignores them.

Conditional sensor errors and per-stage actuator TV errors give the stated
2W times union bounds. Actuator rate calibration needs the ratewise qualification
above. Actual weight evaluation/calibration errors are additional arithmetic
or metrology errors, not supplied by a nominal dynamic range.

## 3. Deterministic residual error formula

Let ||G-Ghat||<=eG, ||K-Khat||<=eK, ||D-Dhat||<=eD, and Ghat>=gI with
g0=g-eG>0. Then G>=g0I and

    ||G^-1-Ghat^-1||<=eG/(g g0).

Decompose KG^-1K-Khat Ghat^-1 Khat into the K perturbation using G^-1,
plus Khat(G^-1-Ghat^-1)Khat. This proves exactly

    eR=eD+eK(2||Khat||+eK)/g0+||Khat||^2 eG/(g g0).

Since the true residual is PSD,

    ||G^-1/2 R G^-1/2||
           <=max(0,lambda_max(Rhat)+eR)/g0.

If the asserted upper bound is negative, the confidence/calibration event is
inconsistent with the model. The note correctly says to report that failure,
not silently treat it as exact zero leakage. Eigenvalue and matrix arithmetic
must be outward certified as stated.

## 4. Resolvent, inversion, weighted norms and initialization

Using C=G^-1K and Chat=Ghat^-1Khat,

    C-Chat=(G^-1-Ghat^-1)K+Ghat^-1(K-Khat)

gives the printed

    eC=eK/g+eG(||Khat||+eK)/(g g0).

If sigma_min(Chat)>=c>eC, then sigma_min(C)>=c-eC, and the inverse identity
gives alpha eC/[c(c-eC)]. Converting Euclidean matrix error to the TRUE weighted
coordinate norm costs at most sqrt((||Ghat||+eG)/g0). Add the separate physical
compression bias: successful numerical inversion does not eliminate omitted
generator directions.

For the baseline initial functional ell^T=c1^T G, the true dual-norm error is

    ||(ellhat-ell)^T G^-1/2||
                          <=||c1|| eG/sqrt(g0).

This uses the BASELINE G and its own confidence bounds. Known label-indicator
columns give an exact coefficient vector c1 even when other predictive features
are nontrivial. Projectors are exact because the dictionary is label-local;
conditioning and feature selection still require validation.

## 5. Full task cost and limits

The stated number of genuine stationary preparations, pulse stages, readings,
random bits, capped exposure and ideal mean exposure are correctly attached to
acquisition. Reset time/work and calibration remain independent physical costs.
For explicit total computational cost, add sample aggregation/record processing
to the O(s r^3) dense matrix preparation (at least proportional to the number
of acquired scalar reports). The note's O(s r^3) is properly restricted to
matrix arithmetic and is not a bit-complexity claim.

The raw Gram diagnostic 217298716624.47653 appears in the saved source receipt,
matching the stated approximately2.17e11. The omitted exact entry is
128/7358694984207. Reporting this conditioning is scientifically necessary:
post-acquisition orthogonal coordinates do not recover lost instrument or
sampling precision. No physical or practical sample-efficiency result follows.

Actual source rate bounds, microscopic reversibility, operation weights,
switching maps and independent preparation remain warranted physical premises.
The finite confidence theorem measures moments under that contract; it does
not prove the contract from those same moments.

## 6. Executable check, and a retracted reviewer concern

Ran the UNMODIFIED copied check_actual_menu_and_confidence.py, with its copied
fixture dependency. It passed. The generator/rate reconstruction, residual-error
intervals and inverse error are exact Fraction calculations. The PSD routine
updates the FULL trailing matrix and correctly implements symmetric Schur
elimination, including its zero-pivot row condition.

An initial reviewer message incorrectly alleged a stale-lower-triangle bug.
That was a misreading of the inner loop. Isolated execution of the ORIGINAL
routine correctly rejects [[1,1,1],[1,2,0],[1,0,1]], whose determinant is -1,
and accepts the rank-deficient PSD matrix [[1,1,1],[1,2,2],[1,2,2]]. No author
code correction was required. An equivalent proposed variant and its run were
preserved as review history, explicitly superseded by this correction.

The original executable returned normalized-defect upper bound approximately
1.0550273150055306e-16 for imposed entry error1e-50, and a separate clock-word
error upper bound8.940696720471931e-08. These are SEPARATE component checks.
The clock error is vastly larger than the imposed matrix-entry radius, so they
cannot be combined into an end-to-end acquisition certificate at1e-50. No actual
observations, clocks, actuator calibration or source preparations were executed.
Root has explicitly acknowledged this distinction.

The rho/Gram matrix errors imposed in the fixture are deterministic synthetic
perturbations, not empirically acquired confidence intervals. The executable
checks the algebraic certification machinery; physical statistical certification
would additionally require the actual trials and premises described above.
