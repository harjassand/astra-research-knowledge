# Calibration-floor guard and strong comparator correction
2026-10-29. Supplements frozen GOVERNING_v1.md. New optional floor construction pending review.

## An observed artificial-failure floor
Suppose the actual SERVICE retains an EXACT genuine full-memory Pauli instrument and, for every current conditional memory state, a separately justified bound holds:
 e_h≤C q_observed,h+eta, eta≥0.
This is an all-memory effect bound, not merely a mean SPAM estimate. On an observed TEST pass, privately mark an artificial failure with independent probability theta=eta/(C+eta). Leave actual test failures marked. The augmented failure probability is
 f_h=q_observed,h+(1−q_observed,h)theta
    =(C q_observed,h+eta)/(C+eta),
so e_h≤(C+eta)f_h EXACTLY. The core negative-binomial proof applies unchanged with R=(C+eta)s/a and the augmented failure budget. This charges calibration uncertainty through actual deliberate failure marks and reduced yield, rather than silently subtracting a systematic floor.

Artificial failure randomization must occur after the source call; it can change the subsequent classical abort control but supplies no backward information to the source. Its branch does not need to reproduce a genuine TEST-failure bath update: the proof only compares conditional hazard probabilities. Imperfect logical pad wrappers, leaked keys and controls that destroy the exact Pauli refinement still require a complete-protocol implementation-error allowance. This trick does not repair those failures.

## Existing noise-tolerant authentication is a stronger comparator than abort-on-error traps
Primary source read: Dulek, Muguruza and Speelman, *An efficient combination of quantum error correction and authentication*, IACR Communications in Cryptology1(4),2024, https://cic.iacr.org/p/1/4/35/pdf , introduction and threshold-code description. It already combines quantum authentication with correction of probabilistic noise and analyzes a threshold trap construction. Therefore neither accepted quantum soundness against coherent attacks nor its coexistence with noise tolerance is new here. A baseline that authenticates logical data, uses the same learned DFS encoder and supplies conventional outer correction is mandatory when evaluating this architecture.

Barnum et al., https://arxiv.org/abs/quant-ph/0205128 , already gives private-key quantum authentication with exponentially decreasing failure as security overhead increases. Bouman–Fehr, https://arxiv.org/abs/0907.4246v5 , supplies general quantum sampling methods and explicitly corrected composability/abort scope. These are serious prior capabilities, not weak baselines.

Our surviving specific question is whether physically simple signed-singlet preparations and pair-readout tests give a useful control/interface tradeoff while discovering and guarding a high-rate encoded subsystem. The present derivation establishes no superior total gate count, source use, key cost, buffering, noise threshold, throughput, or historical novelty. Its O(n) test-to-service witness coefficient can be substantially worse statistically than full logical two-design/authentication tests. Corrected qubit Schur compilation can be efficient, so a loose polynomial compiler bound cannot justify an advantage claim.
