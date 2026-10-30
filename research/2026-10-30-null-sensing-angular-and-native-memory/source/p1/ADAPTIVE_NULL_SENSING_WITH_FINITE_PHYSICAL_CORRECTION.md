# Adaptive null sensing with a finite physical correction mechanism

30 October 2026. Root construction, continuation 13. Earlier scientific files are unchanged. This is a derived mathematical result at the operations stated below, not a claim of a built apparatus, priority, or superiority to an equally informed ordinary controller. Independent checks and any subsequent corrections are recorded separately.

## 1. Consequence selected, and the comparison that changed it

The intended capability is global estimation of a constant physical frequency to error epsilon, with total coherent interrogation time proportional to inverse epsilon, while the correction mechanism has a fixed finite response rate and the hidden error environment persists across trials. The estimator should not identify the error kinetics, their effective scale factor, or a full hidden initial law.

The previous reachable-ensemble construction answers a stronger, different question: agreement under arbitrary future receiving interventions. That assurance is unnecessary for this specified sensing task. Here the acquired information consists only of bounded terminal outcomes that locate the zero of a controlled response.

The independent ordinary construction in physical_mechanism/ already regulates occupation and makes a measured servo residual decay as inverse time. It also proves why that alone is insufficient for metrology: for dR = g(theta-u)dt + sigma dW, the full feedback record is equivalent to an ordinary noisy drift observation and has KL g^2 delta^2 T/(2 sigma^2). Additive measurement noise remains. This rules out promoting in-loop noise squashing to improved physical parameter accuracy.

The present mechanism instead protects a coherent coordinate exactly at the physical null. Away from that null, the remaining signal couples through an uncertain internal clock. Correction need only guarantee positive average clock exposure. The unknown clock speed can change between trials and with the complete history; the estimator locates its common zero rather than dividing by an unlearned gain.

Subsystem encoding, gauge reset, adaptive Hamiltonian cancellation, and robust multiscale phase inference have direct predecessors. In particular Liu and Zhou's 2026 subsystem construction uses the same basic two-qubit encoding, and Kimmel--Low--Yoder's corrected robust phase inference already has inverse-precision scaling. The candidate addition developed here is the explicit combination of a finite auxiliary Hamiltonian, a uniform occupation certificate, persistent conditional hidden states, and a global finite-sample time budget. The literature search does not establish priority even for that combination.

## 2. Conditional physical interface

Work in units hbar = 1. There is a logical qubit L and an internal system K, which includes the clock, the hidden environment, and every unobserved apparatus degree of freedom relevant to later service. An entire old classical record H is retained. Conditional on each possible H, one actual trial provides:

1. A fresh logical state |+><+|, tensor an arbitrary state tau_H on K. No prescribed law, mixing or reset of K is required. An imperfect preparation must satisfy the joint input error bound in Section 6; a good marginal confusion matrix is insufficient.
2. A real reference command u. During interrogation for time T, the generator is

   L_delta,t = I_L tensor A_t - i delta [Z_L tensor S/2, .],

   where delta = theta-u, S = S^dagger on K and ||S|| <= 1. A_t generates completely positive trace-preserving propagation on K. All clock/environment evolution is logical identity at delta = 0.
3. A binary terminal measurement of Y_L, or the bounded-error receiver of Section 6.

The nuisance evolution may depend on H, the selected command, time, and the actual unknown parameter. For a given physical trial the proof freezes that actual nuisance evolution and varies only the displayed signal term as a mathematical comparison. It does not assume that experiments at different commanded frequencies have the same hidden kinetics. The required occupation inequality must hold uniformly for every such conditional nuisance evolution and initial state.

Non-Markovian observed noise is allowed by putting its memory in K. The proof requires a well-defined enlarged CPTP propagator and the stated logical-identity property, not a Markov approximation for the visible sensor. Bounded finite-dimensional generators suffice for all proofs below. Unbounded bath extensions need their own domain/propagator justification. A signal-dependent hidden observation that directly measures the logical amplitude does not satisfy this interface.

Let rho_0(t) denote the comparison evolution with only the signal coefficient set to zero. The one indispensable response premise is

\[
s_T:=\int_0^T\operatorname{tr}[S\rho_{0,K}(t)]\,dt\ge vT,
\qquad v>1/24.                                      \tag{1}
\]

The finite physical supplier in the companion proof gives v >= 1/2 for every T >= 1/W, using a correction rate fixed by the initial dynamic range W and the noise bound, independently of final precision. It allows arbitrary warm initial clock states and a finite-temperature reset port.

## 3. Signed response without a classical clock-path assumption

Write b(delta) = E_delta[Y_L]. Then

\[
|b(\delta)-\delta s_T|\le |\delta|^3T^3/6,
\qquad |b(\delta)|\le |\delta|T.                       \tag{2}
\]

This is useful for the finite coherent auxiliary, whose internal clock is quantum and need not have the classical telegraph-path representation of the complementary role's effective recovery model.

**Proof.** Put B = -i[Z_L tensor S/2, .]. On Hermitian trace-class operators, ||B X||_1 <= ||X||_1. Interleave B with the zero-signal CPTP propagators in the Duhamel expansion. The first derivative of the terminal Y expectation is s_T: in the adjoint picture B^*(Y_L) = X_L tensor S, and the unperturbed logical state is |+>.

Conjugation by X_L changes delta to -delta, fixes the initial logical state, commutes with every nuisance propagator and changes the sign of the terminal Y. Thus b is odd for this frozen nuisance propagator. Its zeroth and second Taylor terms vanish. The exact third-order Duhamel remainder is a threefold ordered integral with three B factors and CPTP propagators, including the true delta propagator in the innermost segment. Hermitian trace-norm contraction bounds it by |delta|^3 T^3/6, with no exponential prefactor. The first-order Duhamel formula similarly gives |b(delta)-b(0)| <= |delta|T. This proves (2).

If |delta|T <= 1/2, (1)--(2) imply

\[
\operatorname{sign}(\delta)b(\delta)
 \ge g_0 |\delta|T,
\qquad g_0:=v-1/24>0.                                \tag{3}
\]

The response has the correct sign, although its unknown gain need not be constant, symmetric in u, reproducible across trials, or learned. At v = 1/2 one may take g_0 = 11/24. A constant-sign mean alone is not enough to justify a constant-gain averaged servo command; the ordinary role supplies an explicit asymmetric-gain bias example. The bracket construction below avoids that error.

## 4. Global finite-sample receiver on one persistent environment

Take 0 < alpha < 1 and 0 < epsilon < W/2. Initially theta belongs to a warranted deterministic interval I_0 of width W > 2 epsilon. Its origin, confidence if itself calibrated, and cost belong to the complete experiment. Let

\[
K=\lceil\log_2(W/(2\epsilon))\rceil,
\qquad w_j=W2^{-j},\qquad T_j=1/w_j,
\quad j=0,\ldots,K-1.                               \tag{4}
\]

Every level uses the centre u_j of its current interval, kept fixed during that level. The true residual, provided earlier levels have succeeded, satisfies |delta|T_j <= 1/2.

Suppose the actual bounded outcome has conditional mean differing from b(delta) by at most beta, where beta <= g_0/32. Set

\[
\eta=g_0/16,\quad s=\eta+\beta,\quad
\alpha_j=\alpha 2^{j-K},\quad
m_j=\left\lceil {2\over\eta^2}\log{2\over\alpha_j}\right\rceil . \tag{5}
\]

Run m_j actual logical preparations/interrogations/readouts at the frozen command. Retain all outcomes and apparatus records. Let bar Y_j be the mean outcome.

* If bar Y_j > s, retain the upper half of the current interval.
* If bar Y_j < -s, retain the lower half.
* Otherwise retain its central half, centred at u_j.

All three updates halve the width. Endpoints may be included in both adjacent intervals.

**Theorem.** If the conditional physical interface and error bound hold after every actual record, this procedure returns the centre of an interval of width at most 2 epsilon containing theta, with probability at least 1-alpha. No trials need be independent, and the hidden system need never be initialized to a reference law.

**Proof.** Within a level subtract each outcome's mean conditional on the full preceding history. These bounded martingale differences satisfy

\[
\Pr\left(\left|\bar Y_j-{1\over m_j}\sum_i E[Y_{ji}\mid H_{ji}]\right|>\eta
 \mid H_{j0}\right)\le 2e^{-m_j\eta^2/2}\le\alpha_j. \tag{6}
\]

The bound uses conditional ranges of length two. It is unaffected by selection of u_j from prior data. On the good event, if delta <= 0 every ideal conditional mean is <= 0, so bar Y_j <= beta+eta=s; an upper-half update cannot discard theta. The lower-half case is symmetric. If the central update occurs, (3) and the receiver bias give

\[
g_0 |\delta|T_j\le |\bar Y_j|+\eta+\beta
\le 2s\le 3g_0/16.
\]

Therefore |delta| <= 3w_j/16 < w_j/4, and theta is in the central half. Induction and sum_j alpha_j = alpha(1-2^{-K}) < alpha prove the claim. The concentration statement itself remains valid on histories where an earlier bracket failed; only the containment induction uses the successful earlier events.

## 5. The complete interrogation budget

Put C = 2/eta^2 and A = log(2/alpha). Since alpha_j = alpha 2^{j-K},

\[
\begin{aligned}
\mathcal T=\sum_{j<K}m_jT_j
&\le {1\over W}\{(CA+1)(2^K-1)
   +C\log 2\,[2^{K+1}-K-2]\}\\
&< {C[A+2\log 2]+1\over\epsilon}.                  \tag{7}
\end{aligned}
\]

The last inequality uses 2^K < W/epsilon. No extra logarithm of inverse precision is needed in total interrogation time. Early, cheaper levels carry smaller failure probabilities. The total number of preparations and measurements obeys

\[
N\le K(CA+1)+C\log 2\,K(K+1)/2.                    \tag{8}
\]

If each preparation/readout/command cycle takes at most t_op, total wall time is at most mathcal T + N t_op, plus stated coarse initialization and controller costs. A fixed nonzero standby power is paid during this entire duration. The conservative constants in (5) are large; this theorem is not a practical speedup demonstration.

For comparison, a permitted noiseless subfamily already requires order inverse epsilon total signal exposure: for two hypotheses separated by Delta, a hybrid/Duhamel argument bounds the final full-record TV under any common adaptive protocol by |Delta| mathcal T/2. When W >= 4 epsilon, two values in the initial interval separated by 4 epsilon with success at least 1-alpha therefore require mathcal T >= (1-2alpha)/(2epsilon). The extra range condition applies only to this displayed lower bound, not to the upper receiver. This only matches the precision exponent. It does not establish a matching logarithmic confidence lower bound. The lower-bound subfamily uses common initial records and parameter-independent nuisance operations; already informative calibration records must be charged separately.

## 6. Actual preparation, reference, sensing and error floors

The mathematical initialization map resets only L:

\[
\mathcal P(\rho_{LK})=|+\rangle\langle+|_L\otimes\operatorname{tr}_L\rho_{LK}. \tag{9}
\]

It is not a reset of K. In the explicit sensor coordinates the logical observables are X_L = X_s X_a, Y_L = X_s Y_a and Z_L = Z_a. A supplied projective measurement of X_L followed, on the minus outcome, by Z_a implements a pure logical preparation, conditional on the retained outcome, with an arbitrary conditional clock/environment state. Separate physical X_s and X_a measurements plus the same sign correction also prepare the + eigenspace while retaining the extra records. The extra information can disturb K; that is permitted by the warm-state certificate. These are real measurement/actuation operations, not inferred from access to a terminal scalar report.

Finite endpoint operations must come with a warranted *joint conditional* error bound. If the actual input is within trace distance d_p of some |+><+| tensor tau_H, its contribution to a norm-one output mean is at most 2d_p. A terminal receiver with uniform mean error d_m contributes d_m. A reference error |u_actual-u| <= e_u contributes at most e_u T by Duhamel, provided the other evolution remains in the stated nuisance class. A residual logical generator with Hermitian trace-norm bound ell contributes at most ell T. A timing mismatch Delta T relative to an ideal permitted continued evolution contributes at most |delta| |Delta T| to the logical mean, because nuisance evolution is identity on L. Any corresponding change in the promised apparatus behavior must also remain inside the class.

One sufficient budget is

\[
2d_p+d_m+e_uT+\ell T+|\delta|\,|\Delta T|\le\beta. \tag{10}
\]

The constant beta budget allows endpoint preparation and readout precision independent of epsilon. The reference error must decrease to order epsilon at the last level. Fixed absolute reference bias produces an accuracy floor; it cannot be learned away from these observations because it shifts the physical null. Fixed nonzero logical dephasing also creates a finite useful interrogation window. Neither is removed by the theorem.

All reset-bath emissions, discarded syndrome readings, timing devices and controller seeds are part of the actual source. Only the displayed terminal measurements and their conditional means are needed for inference. The theorem does not say that the full apparatus record is close to an ideal record, nor that the native material path is preserved. It changes the actual composite operation. Quantum trajectories may be used to simulate it, but the proof never copies a hidden state or assumes simultaneous hypothetical futures.

Here a trial's conditional mean is conditioned on the complete history *before that trial*. Records generated during the trial may be retained for later conditioning. No signed-response bound is claimed after postselecting on that same trial's future bath or measurement record.

If an earlier calibration supplies the initial interval and service bounds with failure probability alpha_cal, then an unconditional error bound alpha_cal + alpha is justified only when its good event warrants the displayed uniform conditional service contract for the calibration-selected operation and every subsequent history. An observed data-dependent radius is not itself an unconditional deployment guarantee. A population rate fit or a marginal preparation certificate does not supply that contract. The calibration trials, assumptions about stability through reuse, and the initial old-record information all retain their costs; this theorem constructs no cheaper acquisition procedure for an unknown physical error algebra.

## 7. What the ordinary alternative can already do

An ordinary robust phase-estimation or stochastic-bracketing controller given these exact preparation, correction, reference and measurement operations can run this procedure. There is no information-processing separation from that controller. Fast or discrete QEC with a sufficiently positive exposure per finite cycle may supply the same general interface. The autonomous finite Hamiltonian below is one explicit supplier, not the only possible supplier or a lower-cost universal replacement.

Finite-strength QEC changes the phase scale factor and causes fixed-nonzero-residual decoherence; Rojkov et al. already identify this bias. Estimating that gain per device is an ordinary alternative. Adaptively controlling the residual makes gain identification unnecessary for locating its common zero, under (1)--(3), but it requires the actual cancellation port and its increasing precision. If the underlying parameter drifts during the experiment, an additional tracking model is needed.

The protected coordinate is a substantial supplied resource. Logical identity at the null is an exact algebraic property, not a consequence of a small measured average noise rate. Generic signal-parallel noise breaks it. The result therefore does not say that arbitrary unknown materials can become inverse-time sensors.

## 8. Primary comparison and preserved scope

* Q. Liu and S. Zhou, *Subsystem Quantum Error Correction for Noisy Quantum Metrology*, arXiv:2606.19628 (2026). The complementary role read the primary PDF: same CNOT, Bell input, gauge/logical separation and syndrome-free gauge reset. Root separately retrieved the primary indexed abstract. The basic architecture is directly preempted.
* I. Rojkov et al., *Bias in Error-Corrected Quantum Sensing*, Phys. Rev. Lett. 128, 140503 (2022), DOI 10.1103/PhysRevLett.128.140503. Finite correction delay changes signal response; postprocessing/calibration is a direct ordinary remedy.
* S. Kimmel, G. H. Low and T. J. Yoder, *Robust calibration of a universal single-qubit gate set via robust phase estimation*, PRA 92, 062315 (2015), with Erratum PRA 104, 069901 (2021), DOI 10.1103/PhysRevA.104.069901. The corrected primary result retains Heisenberg scaling with bounded additive inference error and constant overhead. Generic robust multiscale inference is established.
* S. Pang and A. N. Jordan, *Optimal adaptive control for quantum metrology with time-dependent Hamiltonians*, Nature Communications 8, 14695 (2017). Only previously retrieved primary indexed text is used; Hamiltonian cancellation and iterative adaptation are established. The non-retryable publisher boundary was not bypassed.
* Z. Mann, N. Cao, R. Laflamme and S. Zhou, *Quantum Error-Corrected Non-Markovian Metrology*, PRX Quantum 6, 030321 (2025), arXiv:2503.07745. The complementary role's primary read identifies perfect arbitrarily fast QEC in the relevant general construction. That source is not evidence against a finite-rate result elsewhere.
* The independent effective-recovery construction, detailed prior scope and executed population checks are preserved in record_geometry/FINITE_RATE_SIGNAL_TRANSDUCTION.md. The constructive ordinary nulling and additive-noise counterexample are preserved in physical_mechanism/NULL_SERVO_MEASUREMENT_AND_ITS_NOISE_BILL.md.

No exhaustive novelty conclusion or experimentally acquired error certificate is claimed. Biology and operational chemistry were not used. Prior accepted Astra results, N675, and the previous fixed-gate deployment correction remain untouched.

## 9. Executed work, received corrections and scope

The runnable check_adaptive_null_sensor.py keeps the finite reset qubit explicitly. It checks the physical coordinate/Hamiltonian identities, the positive storage equality at four finite rate ratios, eighteen warm time-varying response cases, fixed-residual coherence loss, and the separate logical-dephasing failure. It then executes the actual adaptive interval rule using reported binary outcomes, with fixed preparation/readout errors inside the stated bias budget. The full conditional clock/hidden state is propagated after each report; the hidden state is never replaced by an independent draw.

Four numerical specimens each used 89,426 reported trials and 769,192 units of interrogation time to target epsilon = 1/128 with theorem-level alpha = 0.05. Their final errors were 0.0033125, 0.0004375, 0 and 0.0068125, all below 0.0078125. These four outcomes do not empirically establish the 95% guarantee; that guarantee comes from the model assumptions and proof. The maximal storage-identity residual was 8.89e-16 and the maximal adaptive instrument trace residual was 1.43e-13. ADAPTIVE_NULL_SENSOR_CHECK_RESULTS.json and the retained binary records contain the actual results and source hash.

The next root construction, COHERENT_MEMORY_AND_PHYSICAL_NULL.md, extends the operation to a coherent persistent bath, proves strict fixed-residual coherence loss in the finite supplier, and gives a restricted KL lower bound when the logical null leaks. Its checker propagates the complete conditional quantum clock/bath state through another 89,426 binary trials, with no bath reset or iid replacement. The final error was 0.0023125 at epsilon = 1/128. The initial clock/bath input was entangled; its hidden marginal was maximally mixed, so this run is not advertised as an experimentally observed bath-memory signature. Numerical population checks are distinct from acquired hardware confidence throughout.

The record-geometry receiving review independently reconstructed the Hamiltonian algebra, storage equality, thermal/warm-state bound and signed Duhamel response. Its exact reviewed versions and receipt are preserved under record_geometry/receiving_review/. A second review reconstructed the coherent-bath and peripheral-spectrum arguments, and required the confidence domain 0 < alpha < 1/2 for the dephasing lower bound. That qualification is now in the receiving theorem; the pre-correction version remains preserved. The physical-mechanism role identified the additional W >= 4 epsilon condition for the displayed two-point precision lower bound; it is now stated explicitly. No review of an analytic theorem is presented as independent execution of the numerical checkers.

The same physical-mechanism role also constructs a finite cooling/damped-transfer alternative under physical_mechanism/finite_cycle_qec/. It uses the same exchange and reservoir together with a separately declared coupling gate and fixed pulse timing. Its final proof retains a further necessary qualification: a terminal transfer-effect certificate alone does not bound within-pulse occupation; the actual pulse/ramp preserves excitation-conserving exchange or needs an additional excitation-growth bound. Its existence reinforces the intended comparison: an ordinary controller can consume this physical response principle. The conservative sample counts and continuing reservoir/control operation do not establish a practical advantage or a total-work saving.
