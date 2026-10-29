# Calibrated physical programs with uniform-in-time observable accuracy

29 October 2026. Root construction. This is a narrower finite-data objective,
not a replacement for the previous full-record TV theorem.

## 1. The objective changed by the failed long-record certificate

Small errors in stochastic transitions can eventually be detected in a long
record without destroying the accuracy of a stable physical program. Here
the intended outputs are deterministic-time bulk observables and approximate
equilibrium preparation in a declared metric. We combine an actual calibrated
operation with an established contractive Gibbs receiver. An equally informed
ordinary solver can use this construction. Concentration, Gibbs dynamics,
and Dobrushin-type coupling are not claimed new.

## 2. Restricted receiver and proof

There are d binary sites. A fixed target program chooses a site uniformly,
independently of state/history, and replaces its bit according to

    new bit ~ Bernoulli((1-s)x_i+s p_i(x_-i)),  0<s<=1.

All other sites actually remain unchanged. Suppose changing x_j changes p_i
by at most c_ij, with c_ii=0 and

    max_j sum_i c_ij <= alpha < 1.                    (1)

The column sum is the one used here. The target specification is frozen;
arbitrary record-selected schedules, online target changes, and data-selected
stopping times are outside this receiver. Site randomization is an actual
resource. At every actual update, assume conditional endpoint-row TV from
the target row is <=delta_i, uniformly in current state, hidden state, and
all actual past information. This is a POINTWISE row premise. An equilibrium
L2 defect alone does not supply it.

Let W_norm be Wasserstein distance with cost Hamming distance divided by d.
Set rho=1-s(1-alpha)/d and delta_bar=(sum_i delta_i)/d. Then

    W_norm(Law(X_t),Law(Y_t))
      <= rho^t W_norm(Law(X_0),Law(Y_0))
         + delta_bar/[s(1-alpha)] (1-rho^t).          (2)

Cap the right side at1. This controls distributions at every deterministic
macrostep t, not one simultaneous sample-path accuracy event.

Proof: choose the same update site in both chains. Between ideal updates
started at x,y, use the same keep/refresh coin and a maximal Bernoulli
coupling on refresh. The disagreement at i is at most

    (1-s)1_{x_i!=y_i}+s sum_j c_ij 1_{x_j!=y_j}.

Glue to a coupling of the actual row at x and its ideal row, adding delta_i.
The resulting expected unnormalized Hamming distance after one update is
at most rho*d_H(x,y)+delta_bar. This remains valid conditional on the full
actual hidden history. Iterate and divide by d to prove(2). A function f
with Lipschitz constant L_f in normalized Hamming distance has expectation
error at most L_f times(2).

As a receiving statement this allows evolving hidden memory when the uniform
row premise is independently warranted. Section5 supplies it only under
the stronger static-disorder experimental interface stated there.

## 3. The constructed Ising consumer

Use Section10 of SIGNED_CONTINUATION_CONTROL_THEOREM.md. Its conditional
refresh probabilities are3/8,1/2,5/8 according to the two neighbours, with
s=9/20. Each neighbour has influence1/8, so alpha=1/4. Hence

    rho=1-27/(80d),    error floor=(80/27)delta_bar.   (3)

The exact source-A compiler supplies delta_i=0 for every frozen hidden vector.
It uses one native call and five fresh private fair bits per local update,
plus actual site selection and boundary control. The formal model has
instantaneous boundary reads/switching. Any implementation must include
decision-time evolution in the actual kernel or supply an actual protected
hold; a finite selector-bit count is not a hardware timing proof.

Write S_i=2X_i-1. The ideal refresh mean is(S_{i-1}+S_{i+1})/8. The exact
mean-spin equation is therefore

    m_i(t+1)=(1-s/d)m_i(t)+[s/(8d)](m_{i-1}(t)+m_{i+1}(t)), (4)

with Fourier eigenvalues

    lambda_k=1-(s/d)[1-(1/4)cos(2 pi k/d)].           (5)

This is familiar Glauber/heat-bath solvability. The new physical supplier
changes the dynamics that this ordinary solver describes: the raw modes have
the preserved infinite-rank frozen-disorder correlations, while the compiled
network follows the specified finite-state process exactly. No new solution
of the Ising model or computational speedup is asserted.

Normalized magnetization M=d^-1 sum_i S_i has L_M=2. Normalized bond
correlation C=d^-1 sum_i S_i S_{i+1} has L_C<=4. Starting at the same state
with uniform row error delta, at every deterministic t,

    |E M_actual(t)-E M_ideal(t)| <= (160/27)delta,
    |E C_actual(t)-E C_ideal(t)| <= (320/27)delta.     (6)

The bounds do not grow with run length. Strongly coupled targets with
alpha approaching1 lose this guarantee; no critical-dynamics solution follows.

## 4. Preparation, calibration records, and what is not bounded

The ideal ring preserves the Ising target pi. Comparing arbitrary actual
initial state to an ideal pi start gives

    W_norm(Law(X_t),pi) <= rho^t+(80/27)delta_bar.     (7)

The stationary actual endpoint law, when it exists, has discrepancy at most
the same floor. This does not equilibrate the hidden variables.

Keep the same pre-service record Z and full calibration D in both laws and
apply the row bound conditional on(H,D,Z). For this general joint extension,
replace the initial distance in(2) by the average CONDITIONAL initial
Wasserstein distance, conditioning on all variables kept identical in the
coupling. Equal unconditional visible marginals are not sufficient. The
intended same-start initial distance0 and preparation upper bound1 remain
valid. Tests f(D,Z,x) uniformly Lipschitz
in x receive the same coupling guarantee. If the simultaneous calibration
event fails with probability beta, add beta in W_norm, whose diameter is1.
For an L-Lipschitz observable multiply by L, or use its actual oscillation
for the failure part. This is a joint frequentist statement, not conditional
coverage for every rare realized D.

No bound is asserted for arbitrary functions of the complete subsequent
service record or of new exposed primitive keys jointly with the output.
Those keys, clocks and sensor logs may remain present and are paid; this
program's guarantee concerns the actual endpoint state. They must not be
used to change the declared update rule/site-selection law. Different word
durations also mean that a randomly chosen wall time samples a different
distribution from macrostep completion.

## 5. Actual finite calibration on the source-B network

Supply d addressed source-B sites, with other sites actually isolated during
an update. Each H_i remains fixed; their joint law and old-record correlations
are arbitrary. Conditional on that vector, the native flip increments of
each selected mode are fresh independent Bernoulli(p_ij) variables. There
is no unmodelled returning bath, drift, invasive sensor or crosstalk. These
are substantive model/control premises, not consequences of equilibrium.

On EACH deployment site take N mode0 calls and N mode3 calls and retain the
entire calibration history. Clip their estimates to

    p_i0_hat in[1/20,3/20],  p_i3_hat in[1/4,9/20].

For beta in(0,1), let

    eta=sqrt[log(4d/beta)/(2N)].                       (8)

For every fixed hidden vector and admissible old record, all2d estimates
have error<=eta with probability at least1-beta. This uses conditional
independence and a union bound; no hidden prior, baseline ensemble or
conditional density ceiling is required. Calibration and deployment use
the SAME unchanged specimens. The bound is not posterior coverage for
every observed D.

The actual words low=T0 and high=T3 T3 have flip probabilities p_i0 and
r_i3=2p_i3(1-p_i3). The high estimate lies in[3/8,99/200], and its error
is at most eta because |d(2p(1-p))/dp|<=1 on[1/4,9/20]. Every target
alpha_target in{27/160,9/40,9/32} lies between the low and high intervals.
Choose low with fitted probability

    w=(r_i3_hat-alpha_target)/(r_i3_hat-p_i0_hat).

The denominator is>=9/40, and convexity makes actual flip error<=eta.
Round w to a dyadic multiple of2^-b. A fixed b fresh fair bits then implements
the selector literally. Conservatively,

    delta_i <= eta+2^-b+delta_impl,i.                 (9)

The last term is separately warranted physical endpoint error from clocks,
actuation, sensing and execution. It is zero only in the ideal model here;
no apparatus value is acquired. Exact integer arithmetic can compute the
dyadic numerator from the finite counts without a floating-point ambiguity.

The controller learns actual bracketing operations, not H or its distribution.
The intended ring specification stays fixed. Its state-dependent fitted
mixtures are part of the specified Gibbs program; the ordinary solver is
allowed the same information and resources.

Calibration costs exactly2dN native calls and d(2N+1) endpoint reads when
adjacent calls share their boundary readout. It does not require2dN new
specimens, but all d persistent devices and their initial preparation must
exist. Each deployment macro costs one or two native calls, b fresh fair
bits, site selection, word duration, and any retained intermediate sensing.
State isolation, arithmetic, memory and other apparatus costs are additional.
No invisible selector or common-time padding is required for this endpoint
observable objective.

## 6. Executed check and limits

check_robust_program.py uses d=4, N=100000, beta=0.01, b=16. It generates
all800000 synthetic flip increments and saves the packed readout arrays.
The estimator receives observations and clipping intervals; the simulation
parameters are used separately to verify the model and confidence event.
No physical experiment is performed. Hardware error is set to zero only
inside that idealized model.

The finite certificate does not grow with service horizon. The actual
16-state fitted kernel and its stationary law are checked by exact rational
arithmetic, alongside numerical transient curves. Counts and results are in
ROBUST_PROGRAM_CHECKS.json. Floating random generation and displayed
Hoeffding logarithms are not an outward-rounded metrology certificate.

This ring is a standard tractable statistical-physics program. Its role is
to complete an explicit physical-control/learning/consumer chain with a
nonvacuous finite-data objective. General strongly coupled targets, large
hidden-dependent costs, drift, crosstalk and bounds known only on average
remain live limitations. Full-record exact results and the positive-flux
comparison theorem keep their original scopes.
