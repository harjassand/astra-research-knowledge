# Fresh physical-qubit certificate for the complete noisy pipeline

28 October 2026. Fixed-policy simulation with fresh ordinary input/output records. Author result pending independent review. No prior ideal-logical holdout is reused.

## Fixed task and why there is no policy selection

The complete implemented pipeline is frozen from the separate continuous-inverse construction: five physical carriers, previously acquired local frames, actual bounded-speed three-layer inverse pulses, 32 mandatory native uses, flagged correction every second use, noisy encoder and noisy terminal syndrome measurements/conditional correction. The generator uses background integral .03 per201-unit EC window, eta=.001 and multiplicative pulse error .001. These are generator parameters, not learner-supplied noise knowledge or apparatus-selectable policies. The learner only receives ordinary experimental records and the fixed acceptance plan. This certificate does not discover or choose the noise scenario.

One fixed policy suffices to close the missing operational-test interface. No policy family, train/test optimization, reselection after failure or source-informed decoder choice is advertised. The target was selected from previous deterministic evidence and frozen before these fresh draws; this is an internal simulation experiment, not externally preregistered blind science.

## Ordinary six-state physical test

For each trial choose independently and uniformly one of the six eigenstates of X,Y,Z on a single physical input qubit. Run the complete noisy encoder, learned inverse pulses, native channels, flagged controller and measured terminal decoder. Measure the corresponding Pauli on the physical output. Record failure when the final sign disagrees with the intended input sign. No ideal logical preparation, ideal logical recovery or entangled-reference preparation is used.

If E is the full physical qubit-to-qubit channel with Pauli transfer matrix M, averaging the six ordinary tests gives

p_ideal = (3 − M11 − M22 − M33)/6 = 2(1−F_e(E))/3.

Translation terms cancel across opposite input signs, not because the channel is assumed unital. The uniform settings are independently chosen every trial; hence the marginal failures are iid Bernoulli with this averaged probability in the declared stationary model. A fixed balanced allocation would instead require handling a nonidentical Bernoulli sum, which is not the experiment used here.

## Explicit external tester budget

Internal encoding, inverse pulse, EC, measurement and correction errors are already in E. The external single-qubit preparation and measurement are not declared perfect: assume each intended input state is prepared within trace distance alpha=1/1000, and each intended output effect differs by operator norm at most beta=1/1000. For every trial,

|p_observed − p_ideal| <= alpha+beta = .002.

Proof: the measurement contribution is bounded by operator norm of the effect error, and the preparation contribution by trace-distance contraction under E followed by a binary measurement. This bound also holds after averaging settings. The simulated external preparation uses a Y rotation of angle .002 and measurement a preceding X rotation .002; both errors are bounded by sin(.001)<.001. Their small coherent errors are actually included in sampling probabilities, rather than only subtracted on paper.

These budgets require independent laboratory calibration if used on hardware. They are not inferred from the same endpoint outcomes. Unknown preparation/readout without any trusted bound can impersonate a good channel and does not support this fidelity certificate.

## Exact acceptance and interpretation

The fixed target is F_e>=4/5. If it is false, p_ideal>2/15 and therefore p_observed>2/15−1/500=197/1500. With N=32768 iid trials, accept only when the exact lower tail of Binomial(N,197/1500) at the observed failure count is at most1/1000. Monotonicity of the binomial lower tail in its probability proves false-acceptance probability at most .001. This is a repeated-experiment guarantee for the fixed pipeline, not a posterior probability or a diamond-norm claim.

The code evaluates the null tail as a ratio of arbitrary-size integers, without normal or floating-tail approximations. A diagnostic decimal is printed but does not decide acceptance. The random source uses52-bit floor-CDF thresholds, whose joint record-law deviation from supplied floating Born probabilities is at most N/2^52. Numerical channel coefficients remain ordinary floating values rather than rigorous interval enclosures; the physical interpretation is conditional on that declared numerical model and external tester budgets. Seeded pseudorandom simulation is reproducibility, not laboratory randomness or a demonstration against adversarial hidden memory.

## Paid acquisition

Each trial requires160 physical native channel exposures (five carriers times32 uses) and the full previously constructed pipeline elapsed time, including72 units for noisy encoding/terminal recovery. The external single-qubit preparation, basis control and readout add6 units per trial. Counts report the new aggregate reference-time sum across trials; parallel laboratory throughput would require additional hardware and is not assumed free.

The frame acquisition is inherited paid scientific capital, not repeated or erased. This new holdout is additional work, not part of the original learned-frame budget. No direct scheme comparison should omit these costs. A strong equally informed conventional method can run the identical code and test; this is a complete-interface certificate, not a new testing algorithm or claimed quantum-code superiority.
