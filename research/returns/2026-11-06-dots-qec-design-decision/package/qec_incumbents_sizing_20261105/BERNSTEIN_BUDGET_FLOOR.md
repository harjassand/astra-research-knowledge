# A scope-limited sample floor for an existing certified baseline

Source inspected as inert text: ScaLERQEC commit 0babdb7a7171009e8079f68f80ae9ae8eb4c259b, uniformized.py lines 407–416 and confidence.py. No upstream code executed.

For the uniformized defensive-mixture method, the source divides observations by the number J of mixture components. For one requested target and a per-design error budget alpha, every checkpoint allocates at most alpha/4 to each of the two bounds (checkpoint allocation starts alpha/2; then splits between KL and empirical Bernstein). Therefore its KL upper endpoint, minimized over every possible nonnegative observation sequence, is at least

    J [1 - exp(-log(8/alpha)/N)]

unless capped at 1. This follows because the inverted Bernoulli-KL upper endpoint is increasing in the observed mean; the smallest is the all-zero mean. The empirical-Bernstein upper endpoint has nonnegative mean and variance, and its additive 7 log(4/delta)/(3(N-1)) term is larger than this KL minimum. Taking the minimum of the two, or intersecting checkpoints having at most N observations, cannot defeat the lower bound. Later checkpoints use still smaller error allocations.

Consequently, to ever report an upper endpoint no greater than 1e-12 at alpha=.001/3 requires at least log(8/alpha)/[-log(1-1e-12/J)] shots. With J=1 this exceeds 1.0085e13; J=2 exceeds 2.0171e13. This is independent of decoder speed or the observed estimate.

This is a limitation of the published uniformized controller's global bounded-observation certificate, not an impossibility theorem for rare-event estimation, a critique of the polynomial identity, or a lower bound for ScaLER's separately implemented conditional-stratified method. The latter may use smaller per-stratum bounds, and other structure-aware proposals may sharply reduce their weight bound. This analysis establishes why executing the global-bound controller for a practical number of shots cannot certify the present 1e-12 pass decision. A tiny point estimate would not change the conclusion.
