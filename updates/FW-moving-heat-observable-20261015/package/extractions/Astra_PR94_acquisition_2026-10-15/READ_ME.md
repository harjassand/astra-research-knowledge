# Astra: finite-noise control acquisition and scalar positivity

Research handoff, 15 October 2026. Source checkpoint: astra-research-knowledge PR94, commit 6fde70a4668f877bc9988bc8f20c570ef4513d08. These are mathematical constructions and primary-source comparisons, not externally validated technologies. No canonical research records have been changed.

## 1. A missing resource in exact scalar-control recovery

**Capability under examination.** Predict or optimize the response of an unknown linear network using scalar readings under diagonal controls, following N854.

**Evidence.** An explicit m-control, m+2-state accretive network family realizes hidden product responses with polynomially bounded conditioning and calibrated port sizes. With fixed bounded adversarial noise, or independent Gaussian noise of fixed variance, exponentially many queries can be necessary even for a constant-quality control decision. The proofs include adaptive queries, generic perturbations, and a precision-budget version. Exact noiseless recovery is unaffected: one carefully chosen rational query identifies the unperturbed family, but its absolute precision requirement is severe. This is not an exponential bit-length lower bound.

**Closest results.** Passive product realizations, rational-pencil realization, exact read-once determinant learning, and exponential system-identification lower bounds are reviewed in noisy_control_obstruction/PRIOR_ART.md. The generic hidden-needle information argument is established machinery. Priority for this particular resource-accounted realization is unestablished.

**Missing operation.** A physically obtainable conditioning/separation certificate or additional measurements that avoid the small scalar-response distinctions.

**Consequence.** Polynomial exact query counts and favorable plant conditioning alone cannot justify cheap experimental acquisition.

**Decisive next test.** On an actual calibrated apparatus, establish measurement noise, drift and model mismatch, then measure full acquisition cost against a fitted-model baseline. No qualifying public raw dataset was acquired; see MEASURED_RESPONSE_GATE.md.

## 2. Constructive escape when the measurements support it

**Capability.** A data-dependent interval reconstruction and diagonal-stability certificate bounds prediction error uniformly over the entire control cube, including zero controls. Reciprocal ambiguities can sometimes be retained in a conservative hull rather than individually resolved.

**Evidence.** Exact-rational worked scripts give uniform error below 0.011827 from 14 settings in one synthetic nonreciprocal case, and below 0.027424 from 13 settings in a reciprocal case. A separate proof check and replay are included. Under known independent Gaussian noise sigma=1e-7, 1,588 repetitions per setting give a 14-setting coverage-failure bound below 1%, for 22,232 readings. This bounds the probability of passing with an incorrect certificate; it does not prove 99% correctness conditional on passing, or that random calibration will pass. Bias does not average away.

**Closest result.** Verified feasible-set identification with the same data may produce tighter bounds. No superiority over that baseline is established.

**Missing operation and next test.** Obtain calibrated measured responses and compare complete cost. The theorem assumes the model class and actuator calibration; scalar readings do not certify those assumptions.

## 3. Stronger scalar prior-art overlap for N853

**Evidence.** The inspected Katkova–Vishnyakova 2001 theorem supplies a positive lattice multiplier in its admitted scalar function class. A new explicit postprocessing proof makes the symmetrized multiplier smooth, strictly positive, even, strictly log-concave and endowed with all absolute exponential moments, while preserving positivity. A second proof checks the global curvature bound. Gaussian smoothing alone fails for the nontrivial Skellam multiplier.

**Consequence.** The complete requested kernel properties follow from the older theorem plus this new deduction in that scalar input class. Those properties are not claimed to have been stated in the 2001 paper. General compact distributions, matrix/cone cases and multidimensional radial scope remain unresolved.

**Next test.** Determine exactly which broader hypotheses require genuinely new machinery; obtain the original Diamond–Essén text before making historical priority claims.

## Reproduction

Python scripts use exact rational arithmetic where stated; see each proof for assumptions and limitations. Run certified_control_escape/worked_example.py and reciprocal_example.py, then audit_control_prediction_certificate/audit.py. The noisy-control check scripts test finite examples, not the asymptotic theorem by themselves. Full proof text and source links accompany every result. AI-generated review labels alone are not independent scientific validation.
