# A sharper forward metrology bound at positive noise rates

5 November 2026. This is an optional improvement to the conservative linear
coupling bound in the operation notes. It does not alter the source, quantum
factory, selector, or preparation theorem. Near a noise-simplex boundary the
earlier bound remains the uniformly applicable fallback.

## 1. Compare independent noise histories, holding the source fixed

Fix a calibration record and compute a positive preparation/program law for
the estimated parameter theta_hat. Use this SAME law under the actual and
estimated apparatus. Replace the actual classical export by its independent
reference roots using the already paid prefix/history-erasure discrepancy.

Suppose the quantum schedule has F independent native stochastic locations
with law P(theta), and K independent reference roots with BSC probability
q_h(theta). All noisy selection, native gates, reset, transport and delivery
are included. Conditional on the common sampled source and programs, the
rest of the protocol is one fixed CPTP processing of its classical fault
history. Consequently, data processing and Pinsker give

    D(rho_actual, rho_estimated)
      <= TV(fault_history_actual, fault_history_estimated)
      <= sqrt{[F KL(P(theta)||P(theta_hat))
               + K KL(Bern(q_h(theta))||Bern(q_h(theta_hat)))]/2}.

Different fixed root heights or a finite number of location types simply
replace each product term by its corresponding sum. The same bound controls
an arbitrary referenced input to the fixed process: conditional fault maps
are identical in the two comparisons. No global inverse norm is used.

This comparison is legitimate although the source depends on theta_hat:
once the calibration record is fixed, that positive source is held fixed on
both sides. On the estimated side its output is the desired target up to
the separately budgeted finite-source and compilation errors.

## 2. Explicit positive-rate constants

For probability vectors P,Q with Q_a>=kappa>0,

    KL(P||Q) <= sum_a (P_a-Q_a)^2/Q_a
              <= ||P-Q||_2^2/kappa.

For a binary law,

    KL(Bern(q)||Bern(q_hat))
       <= (q-q_hat)^2/[q_hat(1-q_hat)].

The root Lipschitz constant is uniform in height:

    |q_h(theta)-q_h(theta_hat)| <= L_root ||theta-theta_hat||.

If the estimated root probabilities stay in a fixed interval separated from
0 and 1, parameter error of order epsilon/sqrt(F+K), with these explicit
constants, suffices. The actual noisy contrast assays then need

    O((F+K) epsilon^-2 log(1/delta_acq))

shots, at fixed parameter-domain and visibility constants. For the general
factory F and K are O(N) at fixed B, eta. This improves the sufficient N^2
shot count to N in this interior-noise regime. It does not remove the other
source, numerical, protected-classical, tree, routing or energy costs.

Uniform positivity of Pauli error probabilities is an additional domain
condition, not a consequence of small total Pauli error. A law supported only
on selected Paulis need not satisfy it. One may instead use the conservative
TV coupling bound in the main theorem. No observed zero count proves a zero
error probability.

## 3. Explicit two-rate cluster specialization

Let the six quantum data layers have depolarizing total rate p_Q and let
classical outgoing basis wires have flip probability p_C. Both are fixed
positive rates in certified ranges, with p_C <= p_Q, p_Q <= 1/3000, and p_C
below the derived classical protection threshold. The reference root is
computed from the actual seven-location classical voter and three links.
For height h>=1 its final independent output flip implies q_h>=p_C; also
q_h<=10p_C and its sensitivity is at most L_q=10/(1-.029).

Because the three nonidentity depolarizing probabilities change together,

    KL(P_dep(p_Q)||P_dep(pQ_hat))
      = KL(Bern(p_Q)||Bern(pQ_hat)).

Therefore

    D <= sqrt{N/2 [
      6 (p_Q-pQ_hat)^2/[pQ_hat(1-pQ_hat)]
      + L_q^2 (p_C-pC_hat)^2/[qhat_h(1-qhat_h)] ]}.

Different root heights can be bounded by the worst admitted denominator.
This is a forward bound, despite the correlated input-label preimage.

The two rates have actual compatible assays. Quantum idle contrasts acquire
p_Q, with classical capture in the unknown stable amplitude. Classical
opposite-sign preparations, zero/one classical idle, and the same protected
capture give m_t=A_C(1-2p_C)^t. Their ratio acquires p_C while cancelling
capture and preparation visibility. All templates, resets, storage and
capture are the declared noisy operations. This is a finite-type bridge,
not an identification theorem for arbitrary component heterogeneity.

If no positive lower bound is initially supplied, geometrically increasing
confidence-calibrated batches can establish one for every fixed nonzero
rate. Allocate failure probability summably across batches and stop when
the confidence interval excludes zero. With high probability the stopping
cost is finite, of order inverse squared rate up to confidence/log factors
under conservative bounded-output estimation; this commissioning cost must
be paid. A hard finite budget may instead retain the quadratic fallback.
At exact zero or unidentified support boundaries do not invoke the interior
bound without its conditions.

This gives a concrete resource improvement in the achieved explicit family,
but still no matched total-resource advantage over a method allowed to use
the same forward statistical comparison and state-specific preparation.
