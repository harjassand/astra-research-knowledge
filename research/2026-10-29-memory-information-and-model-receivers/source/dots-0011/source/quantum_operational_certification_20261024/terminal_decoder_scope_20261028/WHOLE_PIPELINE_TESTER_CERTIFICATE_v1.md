# Whole-pipeline certificate with imperfect calibrated testers

28 October2026. Author proposition; independent review pending. This is a standard six-state channel test with explicit tester-error accounting, supplied to close the new physical-boundary interface. No novel test, SPAM-free guarantee, or environment-reconstruction advantage over an equally informed conventional tester is claimed.

## Physical object and data

Freeze a selected physical implementation after its training phase. Let Lambda be its complete qubit-input to qubit-output CPTP channel, INCLUDING actual unknown-input injection, all native uses, noisy EC, physical terminal syndrome measurement/correction/decode, and boundary waiting. No ideal encoder, recovery or decoder is substituted inside Lambda. Fresh tester trials begin at the actual input port and end at the actual output port.

For uniformly random j in{X,Y,Z} and s in{+1,−1}, intended input rho_js=(I+s sigma_j)/2 and failure effect E_js=(I−s sigma_j)/2 yield binary failure. The ideal tester failure mean obeys

    p_ideal = (2/3)[1−F_e(Lambda)].

This follows immediately by summing the affine Bloch expressions over s, then over j. It does not assume Lambda is unital, Pauli, close to identity, or known microscopically.

Actual prepared states tilde_rho_js and actual failure effects tilde_E_js satisfy calibrated bounds

    (1/2)||tilde_rho_js−rho_js||_1 <= a_js,
    ||tilde_E_js−E_js||_infinity <= b_js,

with actual effects between0 andI. Contractivity of trace distance and the variational characterization against an effect give

    |p_actual−p_ideal| <= delta,
    delta = (1/6) sum_js (a_js+b_js).

No dimension of the channel's environment enters. The calibration bounds must be justified independently; the operational construction does not grant them for free.

## Finite acceptance and composition

For independent stationary trials of the frozen implementation and fixed randomized tester, let p_U be any valid one-sided binomial upper confidence bound on p_actual at failure level beta. Then on that confidence event,

    1−F_e(Lambda) <= min(1,(3/2)(p_U+delta)).

Training-selected circuit/cadence is allowed when this validation bank is fresh and the selected implementation is frozen. If a family of validations is used, pay its actual selection/union budget. Future arbitrarily drifting channels are not certified by old counts. With independent or contractually reset deployments of the SAME complete channel, the normalized Choi trace-distance bound and input dimension2 give

    (1/2)||Lambda−id||_diamond <= min(1,2 sqrt(epsilon)),

where epsilon is the fidelity-error bound. Hence J uses in an arbitrary surrounding circuit have half-diamond discrepancy at most min(1,2 J sqrt(epsilon)) by telescoping. This is a conservative composable bound, not a hardware threshold or retained-environment theorem. A channel observed only after averaging correlated persistent memory cannot be substituted into this composition.

If a genuinely private fresh Pauli twirl is physically performed at the two USER ports and its key is retired before output, the ideal twirled qubit channel has half-diamond distance exactly1−F_e(Lambda). Approximate port Pauli gates require a separate physical error allowance for their complete channels. This optional strengthening must not be inferred from merely relabeling measurements or from a key retained by the assessed adversary. The earlier received logical-twirl source governs that additional operation; it is not executed in this note.

An exact acceptance test for target epsilon0 can directly test the rational null p0=(2/3)epsilon0−delta when p0>0. It is impossible for this guard to certify epsilon0 if the tester allowance delta is already at least2epsilon0/3, even with zero observed failures. This identifies an actual calibration floor rather than hiding it in an ideal logical endpoint.

## Why an uncalibrated tester is not sufficient

A concrete false-pass model has a qubit channel that completely dephases in Z. For every purported axis j, let the uncalibrated preparation device actually prepare |s_Z> and let its purported j readout actually measure Z. Every matched trial passes, for all j and s, yet the user's qubit channel has F_e=1/2 and destroys X/Y coherence. This model uses only a qubit at the tested port; it requires no hidden quantum bypass. Thus perfect-looking matched counts cannot certify arbitrary quantum preservation without a directional tester-calibration assumption. The explicit a_js,b_js bounds exclude exactly this defect.

## Scope and immediate use

This proposition applies to the actual physical_output_PTM from the noisy-boundary implementation only after that physical operation is frozen and directly tested. Prior ideal-decoder probabilities or cadence holdout counts are not interchangeable with new whole-pipeline counts. It permits testing the consequential operation without learning its full process matrix or environment; an ordinary experimental six-state benchmark has the same capability with the same tester assumptions.
