# Acquired policy certificate, value forecasting and executed evidence

The [productive-control theorem](README.md) settles action inequalities across a model set rather than accurately learning the resulting absolute mean work. The complete [acquisition code](package/code/acquire_and_certify.py), [saved counts](package/results/calibration_counts.json), [rational certificate](package/results/policy_certificate.json), [separate verifier](package/code/verify_certificate.py), and [independent verification receipt](package/results/independent_certificate_verification.json) are preserved as supplied. Capital did not rerun them.

## Actual supplied acquisition

The synthetic source generated multinomial sufficient statistics representing 371,368 complete one-cycle trials per mode, 742,736 total. The corresponding physical protocol must also pay 742,736 resets, outcome reads, and aggregate exposure; no ordered physical trial trace or laboratory experiment is claimed.

The statistical radius is 0.003, systematic allowance 0.001, total probability half-width 0.004 and joint concentration failure below 0.01. The compiler receives counts, rewards and uncertainty budgets, not the simulator's true probabilities. Its implemented form certifies one prefix state plus a constant tail and abstains when exact inequalities fail.

The standard certificate gives `L0 approximately 28.92163622`, `D_box approximately 16.61965488`, and `rho_B^- approximately 3.42582955`, leaving a strict tail margin. Swapping the kinetic profiles while preserving reward labels reverses the learned rule to B at zero, A thereafter. Both certificates passed the separate verifier reconstructed from saved counts. These are actual source-side computations, not proposed tests.

The [verification record](package/results/verification_receipt.json) also includes exact rational comparisons of all 252 stationary policies for N=2 through 7 at every safe start, and 18 fixed state-dependent probability-box corner models. The main all-depth and arbitrary-policy quantifiers come from proofs, not finite enumeration. Independent working constructions and [targeted final audit](package/results/final_audit_receipt.json) are retained at their stated scope.

## Same-access absolute-value lower bound

Keep A, p_B=0.2 and rewards fixed, while `q_B=theta` varies near 0.7. The exact optimal policy remains stable while its absolute expected work is exponentially sensitive to theta. A forecaster required to estimate log V within epsilon with confidence 1-delta, uniformly for theta in [0.69,0.71], needs the following expected aggregate cycle evidence on at least one allowed model (N>=32, 0<epsilon<=0.1, 0<delta<1/2)

```text
E K >= N^2/(208 epsilon^2) * kl(1-delta,delta).
```

The access grants arbitrary safe-state preparation, adaptive action choice, complete transitions, parallel specimens and unrestricted computation. For N>=100 and `0<epsilon<=0.1`, the hard pair `theta0=0.698`, `theta1=theta0+4epsilon/N` lies inside the same [0.698,0.702] acquisition-success family. Its target log values differ by at least4epsilon while one cycle carries only order epsilon^2/N^2 information. Adaptive likelihood chain rule covers stopping and parallel acquisition.

Ordinary parameter estimation followed by the recursion attains order `N^2 epsilon^-2 log(1/delta)` on a regular neighborhood. At fixed positive action margins, exact policy acquisition's dependence on N is constant, with confidence dependence order log(1/delta), under homogeneous or justified-transfer sampling. Unrestricted state-specific rows need additional coverage.

This separates two requested statistical outputs. Ordinary direct policy identification can exploit the same action stability, so it is not a superiority claim against every equally informed method. Existing structure-aware policy identification and change-of-measure sources are credited; their discounted assumptions are not silently equated with this undiscounted all-depth theorem.

The saved intervals illustrate unresolved value uncertainty:

| Failure depth N | Certified policy | Permitted upper/lower value ratio |
| --- | --- | --- |
| 16 | A at zero; B otherwise | 2.27 |
| 64 | Same | 27.0 |
| 128 | Same | 733 |
| 256 | Same | 540,455 |

That widening interval describes these particular data. The separate information theorem establishes the general lower bound. The supplied [figure](package/figures/policy_vs_value.png) illustrates this distinction rather than a physical endurance measurement.

## Full operational bill

Uniform physical envelopes, complete transition support and transfer to the deployed population are premises that finite local counts alone cannot establish against arbitrary alternatives. Positive margins must include systematic classification, output/reward and energy errors. Deployment needs a paid verified safe state, reserve for a low-risk mission, reliable damage sensing and actual cycle actuation. A short digital counter does not manufacture N levels of physical damage buffer.

The compiler has finite-state/prefix and rational bit-complexity costs; exact arithmetic does not make the long operation, memory protection or actuator precision free. Output, energy, consumables, support reliability and future maintenance remain charged. Calibration reuse lasts only while the operating envelopes and transition support remain valid; changed equipment, aging or new conditions need a renewed earned contract. The [mission/rare-hazard page](missions-and-rare-hazards.md) shows how omitted support can invalidate an otherwise valid local certificate.
