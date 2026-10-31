# Independent review: bounded-innovation calibration receiver

## Verdict and source binding

PASS as a mathematical calibration-to-CQ-simulation receiving theorem, conditional on its known-mechanism and iid observation promises. I read the complete `BOUNDED_INNOVATION_CALIBRATION_RECEIVER.md`, 14,390 bytes, SHA-256 `546c90eb5e3efc087e4dc90d559017623772c6f426bdf58c20ccdbddba3172bf`. No correction is required. This receipt is separate from the executable exact affine learner: no new estimator implementation or quantum execution was reviewed here.

The received complete-CQ perturbation source is SHA `467b02dac2c0b5326ce2de8356b4255c49ad1d68f081e840c11bdd024b99ac01`, independently reviewed in receipt SHA `13b1a285ee3865775760308ee808652d98c29c224d7d45d4f318e43e694b1610`. Its common-stationary, centered and uniform-error premises remain essential.

## 1. Structural model certificate

Every fixed innovation gives a permutation of the label space because F is invertible. Thus uniform pi is stationary for every p, including distributions with zero probabilities. This is exact model structure, not a stationary distribution estimated from data. The reference m-step law is uniform independently of the initial x because the controllability matrix maps uniform innovation strings onto all of GF(2)^n. The affine offset is deterministic and does not change uniformity. The displayed expansion of x_m and P0^m=Pi are correct.

For each fixed x, full-column-rank G makes the innovation-to-output map injective. Therefore the absolute column-sum difference equals ||p-u||_1, identically for every x, and the full induced matrix norm is exactly this quantity. This eliminates a 2^n transition-table estimation problem only because the mechanism and innovation coordinates are known. For redundant coin columns the same equality need not hold for the original coin law; the source explicitly excludes that unearned identification.

## 2. Observation and statistical event

A computed left inverse recovers r from v=y+Fx+beta after separately checking v belongs to im G. The consistency check cannot certify the affine/iid mechanism. Under the explicit premise, successive recovered innovations are iid even from a dependent source trajectory. The requirement to observe every actual clock event, including self-loops, is load-bearing. Change-only records and missed events do not satisfy this observation model.

For D=2^k, the identity ||v||_1=max_s sum s_r v_r and the one-sided Hoeffding bound for variables in [-1,1] give 2^D exp(-N t^2/2). Substituting the stated r_N gives probability at most delta. Unknown support and zero probabilities cause no issue. The calculation is a proof bound; it does not require executing a loop over all 2^D sign vectors.

On E, eta<=eta_hat+r_N and eta<=2, so capping the upper confidence bound at two is safe. An upward certified radius is also safe. The radius and its sample-size condition can be checked with directed rational arithmetic as stated; there is no exact-logarithm equality oracle. eta_hat is rational and exactly computable from counts.

## 3. PASS semantics and complete controlled-process receiving

The threshold simultaneously enforces eta<=1/(4m), which is needed for the perturbation theorem, and eta C<=epsilon_model, with C=72(p_slots+1)m+4096 b^2m^2T. On E and PASS both requirements hold. Safe upper bounds for C and lower thresholds preserve this implication.

The resulting deterministic channel bound is uniform over all specified CQ inputs, finite references and outcome-retaining prescribed instruments in the envelope. Thus a consumer selected from the public calibration transcript is allowed. It must still obey the common centering, norm, time, instrument and CQ-algebra constraints. Unknown coupling/backaction and arbitrary source-coherent controls are not acquired by this estimator. Microscopic clock-path disclosure is also not silently included in the fast compiler's output task.

A separately acquired ideal-reference simulator is received only with its actual same-task uniform numerical error and paid input operations. The reference's classical forgetting horizon m and its synthesized quantum pure-return horizon are not identified without proof; taking n conservatively for both is legitimate. The existing affine realization preserves the classical diagonal process, not the private old coins or an arbitrary old quantum dilation.

## 4. Correct statistical confidence, including public reuse

False PASS while eta exceeds the target is contained in E-complement, so its unconditional training probability is at most delta. This is not posterior truth of an individual transcript. Acceptance may be rare; a conditional bound must divide by its actual probability unless a separate lower bound is earned.

For the joint transcript/output comparison, draw the same training transcript under the true model in both experiments. On ABORT both outputs agree. On accepted good transcripts the deterministic process discrepancy is at most epsilon_model+epsilon_exec, uniformly in the transcript-dependent consumer. Bad training mass contributes at most 2 delta in trace norm. The displayed joint bound therefore follows. It is not a comparison between two different training distributions generated by Pp and P0; the source correctly uses the same calibration record for both downstream experiments.

If eta<=eta_target-2 r_bar, then on E one has eta_hat+r_bar<=eta_target, so PASS probability is at least 1-delta. The claimed conditional bound delta/(1-delta) and the convenient eta<=eta_target/2, r_bar<=eta_target/4 case are valid. Increasing N does not force a genuinely biased law to pass.

One global parameter event certifies all subsequent finite uses, so there is no statistical union bound over later experiments. Nevertheless deterministic model error and numerical simulation error accumulate. A whole-lifetime envelope must count all physical time and all segments/instruments, including separate experiment preparations where appropriate, or sum the individual deterministic bounds. The text explicitly retains this cost. Rare future postselection can magnify conditional error and is excluded.

## 5. Centering and implementation cost

Uniform source means of diagonal Pauli strings are exact: nonidentity Z strings average to zero, while the identity contributes the system mean. Rational aggregation and a safe accessible LCU normalization supply a valid b. The common nontrivial mean can enter H0 in the robustness proof because that proof does not pay ||H0||, but its sqrt(lambda) physical evolution must still be implemented. Thus rate-independent model discrepancy does not imply rate-independent gate cost for an unremoved mean. Scalar identities are the stated trivial exception.

Ordinary uniform-state compression supplies a block encoding of a mean when the required input encoding is available; it is not numerical evaluation or free simulation of that mean. The source distinguishes these tasks correctly.

The sufficient record count scales as (2^k+log(1/delta))/eta_target^2. This is exponential in k and generally quadratic in inverse model-error tolerance, with the full lifetime envelope entering eta_target. No factor of 2^n is needed for the innovation histogram, but per-record label access, O(N n) possible transcript storage, resets, all-tick monitoring and elapsed time are separately charged. Consequently calibration can dominate a logarithmic-precision execution algorithm. There is no free data-acquisition or practical-speedup conclusion.

## 6. Strongest ordinary comparator and final boundary

The same residual extraction and empirical distribution estimate are available to an ordinary classical estimator with the same observations. The concentration argument is elementary finite-alphabet statistics, and the received CQ theorem uses ordinary structured semigroup perturbation machinery. The already inspected primary comparisons are [Mitrophanov 2005](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/26A9854BCB8D103B3A63A9B272616EC0/S0021900200001066a.pdf/sensitivity_and_convergence_of_uniformly_ergodic_markov_chains.pdf) and [Szehr–Wolf 2013](https://arxiv.org/html/1210.1171); this review adds no claim of statistical novelty.

The separate `ORDINARY_AFFINE_INNOVATION_COMPARATOR.md` explains that dense finite-dimensional CQ propagation already removes switching-rate dependence at full-dimension cost, and that source-only approximate Fourier closure can be cheap even when the exact closure is exponential. Thus the receiver earns a useful known-mechanism near-model parameter certificate, not superiority over all ordinary simulators. The remaining succinct controlled integration question is separate.

Accepted scope: known invertible controllable affine mechanism, injective bounded-width iid innovations, complete correct observations with known event interpretation and clock, supplied centered coupling, fixed finite CQ resource envelope, and an independently acquired ideal simulator. Excluded: arbitrary unknown kernels, dependent innovations, latent/noisy labels, change-only event records, posterior-per-transcript certainty, unlimited accuracy-preserving reuse, arbitrary quantum source coherences, and a completed numerical/quantum implementation. No frozen source was edited.
