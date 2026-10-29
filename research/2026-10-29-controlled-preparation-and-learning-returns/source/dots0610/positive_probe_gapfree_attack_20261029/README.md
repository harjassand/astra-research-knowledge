# Positive physical feedback and a gap-free small-loss controller
2026-10-29. Independently accepted mathematics at the scope identified by the two receipts in sibling `positive_probe_gapfree_audit_20261029`.

## What changed
A physical Bell-sign-change test produces a genuine nonnegative bit whose failure probability is a positive quadratic form in a candidate local frame. A common correct algebra gives zero failure pathwise, even without excitation. This avoids the constant shot variance of a signed estimator when the source is harmless.

Lifting rotations into35-dimensional quadratic features allows established small-loss linear-bandit machinery to exploit this physical feedback. The new derivation checks the bounded stochastic-feedback extension, supplies a full-dimensional radial action body, and replaces continuous sampler/covariance oracles by a terminating finite rational quadrature construction using the ACTUAL discrete law's exact covariance. For a horizon-refined rotation net, expected cumulative probe loss has a polylogarithmic-in-horizon bound, without an excitation gap. The construction is finite but may be computationally astronomical.

**Not supplied:** polynomial classical runtime, a35-dimensional end-to-end learner execution, manageable constants, hardware calibration, complete new readiness/guard integration, or practical superiority. The previous executed finite signed-feedback algorithm remains the concrete fallback. Conventional controllers with the same information and controls can use the same positive probes and learning construction.

## Governing arguments and review
- `BERNOULLI_SMALL_LOSS_BRIDGE_DRAFT.md`: retained physical probe derivation and initial reasoning. Its physical interface remains a dependency; its unthickened/oracle treatment is superseded by v2/v3. Despite the draft filename it is hash-bound in the v2 review: do not omit it.
- `RADIAL_ORACLE_THEOREM_v2.md`: accepted exact-oracle bridge, rational rotation net, universal rank35 argument and one-edge masked feedback accounting.
- `FINITE_RATIONAL_KERNEL_v3.md`: accepted finite-computability closure. Exact finite-law covariance removes estimator bias; certified moment/mean/leverage bounds replace impossible discrete-versus-continuous TV approximation. All candidate decompositions are precomputed before fresh private sampling. A flattened rational joint sampler gives an explicit capped-randomness abort allowance. Zero responses permit kernel caching.
- `FINITE_RATIONAL_KERNEL_v3_DRAFT.md`: superseded working copy, not governing.
- Independent `ORACLE_REVIEW_RECEIPT_v2.json` and `FINITE_KERNEL_REVIEW_RECEIPT_v3.json` govern acceptance and exclusions. Their hashes and governing files have not been changed after acceptance.

For one edge, v3 gives expected physical loss at most
`6 T epsilon² + 128 d² gamma² log(T) +16`,
with d=35 and integer gamma=4 ceil(log2(10dT)). Taking epsilon<=T^-1/2 gives O(log³T), but the explicit constants are large. A fixed net instead has a nonzero risk floor. One-edge-per-round masking carries the stated m²/p cost across m star controllers; it is not simultaneous access to every edge.

## Executed evidence and its scope
- `check_positive_probe.py`:300 direct Bell-sign/commutator/quadratic checks, including identity, a nonunital common-swap channel and arbitrary CPTP noise. Floating mathematical checks, not laboratory shots.
- `check_rational_geometry.py`: exact rational feature rank35 and radial affine dimension35 from125 rational rotations and explicit nonzero minors. Universal upper-bound identities are separately checked by the reviewer.
- `check_finite_quadrature.py`: a2D finite rational-law diagnostic. Its covariance inverse and estimator unbiasedness are exact Fraction calculations; continuous moment comparison uses floating high-order quadrature, not interval certification.
- `check_exact_initial_kernel.py`: exact2D uniform-potential mean/covariance/leverage certificates.
- `check_certified_exponential_kernel.py`: rigorous1D nonuniform exp(-4x) kernel certificate using exact rational Taylor remainders and integral enclosures. This verifies finite integration and moment-inversion logic on a small case, not the35D learner.
- `check_flat_sampler.py`: exact demonstration that hierarchical caps can bias action selection, while the preflattened joint sampler preserves current-outcome probabilities with a declared abort allowance.
- The reviewer independently supplies another certified scalar exponential kernel plus physical, rank and radial/masking checks.

Run programs with Python, NumPy and SymPy as used here; no network, account data or raw conversations are needed. The directory contains no hardware data. The scientific primary dependency is Ito–Hirahara–Soma–Yoshida's2020 adversarial linear-bandit potential argument, linked in the governing notes; its small-loss algorithm is not claimed as an Astra invention.

## Important unresolved obligations
The adaptive interval quadrature has a finite termination proof, not a useful complexity bound. Candidate-private timing, genuine common conditional source maps, trusted or separately budgeted probe controls and the common-algebra promise remain load-bearing. A positive comparator loss from drift or calibration error introduces a loss floor. No frame can be identified without informative noise merely because protection loss can be kept small. The construction should not be presented as a completed civilisation-scale or practical unknown-noise recovery system.
