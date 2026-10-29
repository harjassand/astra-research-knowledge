# Finite clock and sequential service: independent review

29 October 2026. Reviewed ACQUISITION_TO_PREPARATION.md, read version

    SHA256 2a71cfd2af99e2f6d59cee13163f7eb764823c64d6e9850d42d0814fe5ec7d91

Scope: the new load-bearing finite-clock construction and sequential
service composition, plus preservation of the warm-preparation theorem.
No optional numerical tests or further research extension were undertaken.

## Verdict

The dyadic clock, correlation timing bound, bit bias, censoring charge,
sampling-error reuse and conditional sequential hybrid argument check.
The work needs two explicit implementation/scope qualifications:

1. The actual mean execution-time upper bound must include **+delta_t**
   for the permitted timing error. The text states the ideal mean and
   probability-rounding increment but does not combine the jitter term.
2. Future experiments must be the SAME Markov kernel of the prepared
   state, including apparatus initialization. A retained burn-in transcript
   is not automatically covered by the prepared-state KL bound. State
   this explicitly if the apparatus can keep preparation history.

Neither qualification changes the mathematical preparation bound or the
finite-record error formulas under their stated independent-clock access.

## 1. Dyadic probability construction

For k=0,...,M-1, the probabilities p_k are nonnegative and sum to
1-exp(-gamma T_c); adding the censor probability gives total one. Taking
q_k<=p_k on a dyadic grid and assigning all leftover mass to q_* gives

    TV(q,p)=sum_k (p_k-q_k).

Interval-certified lower bounds on p_k can be rounded down to construct
these q_k without pretending to evaluate an irrational floor exactly.
The resulting interval upper bound on the displayed sum certifies
rho_clock. Every count 2^b q_k is an integer, so b fair bits and integer
threshold comparisons implement q exactly. The interval widths and b
must be chosen to achieve the requested bias; their bit costs remain real.

The zero-time outcome is legitimate: the same initial feature vector may
be reused. No second independent same-time physical sample is required.
Any extra sensor errors in a duplicate read remain part of the declared
sensor calibration, not new trial independence.

## 2. Timing bias and operator conversion

For deterministic s,t, path length and stationarity give

    E d(X_s,X_t) <= integral_s^t E|P_u|du
                   <=|s-t| sqrt(d tau).

Thus each symmetric correlation entry changes by at most
sqrt(d tau)|s-t|(B_i L_j+B_j L_i)/2. Conditioning on a clock outcome
preserves this estimate when the clock and timing error are independent
of the driver path. For a vector z, the absolute quadratic form is bounded
by the product (sum |z_i|B_i)(sum |z_i|L_i), hence by
||z||²||B||_2||L||_2. This proves the operator bound used in equation (7).

Compare continuous exponential lags with their ideal left endpoints,
then ideal probabilities p with actual probabilities q, then the executed
lags with their q-grid targets. These three comparisons give respectively
the Delta contribution, bit bias, and delta_t contribution. Therefore

    eta_time <=sqrt(d tau)(Delta+delta_t)||B||_2||L||_2/gamma

has the correct factor. No extra factor of two is needed under the
independent timing-error contract.

If that independence is relaxed, a mere pathwise |lag-t_k|<=delta_t is
not by itself the same conditional expected-displacement bound: adaptive
timing can select motion within its admissible interval. Any alternative
wording should explicitly supply the required conditional displacement
estimate, rather than only a conditional bound on timing error.

## 3. Bit bias, censoring and sampling

Every recorded ideal feature matrix has operator norm at most
||B||²/gamma. Thus probability TV at most rho_clock gives an expectation
change at most 2rho_clock||B||²/gamma, as in equation (8). The censor
matrix is zero and satisfies the same ceiling. The signed omitted
continuous tail has norm at most ||B||²exp(-gamma T_c)/gamma.

The actual finite-clock samples retain the same bounded ranges, so the
previous Hoeffding proof applies to their actual expectation. Adding the
deterministic timing, bit and tail biases then controls the target H.
Independence is across the physical preparations; entries and G/H samples
within a preparation may remain correlated.

## 4. Execution time correction

Assign ideal grid duration t_k to outcome k and a duration in [0,T_c]
to the censor outcome, with the convention fixed for both p and q.
The ideal mean is at most E[min(S,T_c)]
=(1-exp(-gamma T_c))/gamma. A change of outcome distribution by TV
rho_clock changes the expectation of a variable in [0,T_c] by at most
rho_clock T_c; this uses the range-times-TV bound, not twice that bound.
The actual positive timing excess is at most delta_t per executed trial.
Consequently a safe complete bound is

    E time_actual <= (1-exp(-gamma T_c))/gamma
                              +rho_clock T_c+delta_t.     (R1)

The stated worst-case T_c+delta_t is correct. Deciding the censor outcome
in advance and executing no driver evolution there only reduces these
bounds. If the burn-in clock also has bounded error, execute a certified
duration no shorter than the b required by Section 1; any extra duration
must be included in the preparation-time/work ceiling.

## 5. Warm preparation and future-kernel scope

Section 1 preserves the two-direction Gaussian-shift KL proof and the
uniform terminal-phase argument. The independent driver preparation gate
is retained. Adding a separately certified initial-product TV error by
propagating through the same warm-up dynamics is valid.

The future-experiment TV transfer is valid for a common kernel K from
the prepared full state: TV(rho_warm K,rho_stat K)
<=TV(rho_warm,rho_stat). This includes causal adaptive policies and their
complete transcripts when apparatus randomness and initial controller
memory have the same stipulated conditional law given that state.

A warm-up transcript correlated with the driver history is extra initial
information. Keeping it in the future experiment can require comparing
the joint prepared-state/transcript laws, which is not established by the
state-only Gaussian argument. Fresh common apparatus initialization, or
explicitly discarding preparation history, is one sufficient contract.
This is the precise scope of the common-kernel phrase, rather than a new
restriction on later causal policies.

## 6. Sequential reuse

Condition on a calibration record in the single simultaneous confidence
event. At each common prior service history, use the same selected force,
preparation target and future policy in the two experiments. The actual
fresh driver gate restores the stipulated initial driver law conditionally
on this history. The per-service kernel discrepancy is therefore bounded
by its uniform epsilon_j. Sequential kernel composition/induction gives

    TV(joint warm transcript,joint stationary transcript)
                                        <=sum_j epsilon_j.

Uniform deterministic budgets suffice as written. If budgets are
history-dependent, use corresponding uniform ceilings or explicitly take
the expectation in the chosen hybrid argument. Stops can be padded by
common dummy services up to a fixed maximum m.

Outside the calibration event, bound TV by one. Since acquisition has
the same law in the comparison, the unconditional joint bound is at most
delta_calibration+sum_j epsilon_j. The calibration failure is paid once,
even for adaptive coefficient selection on that same simultaneous event.
The root correctly rejects replacing fresh drivers by an unproved reset
obtained merely by waiting for receiver relaxation.
