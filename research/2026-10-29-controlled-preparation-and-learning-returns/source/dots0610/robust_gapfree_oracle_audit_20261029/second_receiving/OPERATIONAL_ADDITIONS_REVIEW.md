# Receiving review of finite sampler scheduling and fixed-port robust corollary
2026-10-29. Reviewer sharpen_noreset_acquisition_certificate.

This review supplements, rather than overwrites, the first v4 receiving receipt. The core commutator triangle, deterministic-comparator actual-history oracle inequality, perturbation budgets and finite threshold agree with my independent derivation and operator checks. No second independent novelty claim or duplicate canonical theorem is created.

## Genuine implementation-order obligation
The frozen v4 argument for capped INTEGER-WEIGHT candidate sampling is correct: conditional on current integer weights, accepted index and rejection count are independent. Candidate caps can be neutral pre-role stopping events. This fact alone does not cover keys sampled only after selecting a role.

An exact counterexample is retained in `independent_checks.json`: learning probability1/3 with no key abort, other roles totaling2/3 with abort probability1/2, and constant candidate loss1. If abort rounds are assigned zero loss, expected physical stopped loss is2/3 but the probe importance estimator expectation is1. Thus role-specific post-role abort is not a literal unbiased stopped-history process. This does not refute the core uncapped theorem or its candidate-only cap argument; it limits a broader implementation interpretation.

`FINITE_SAMPLER_SCHEDULING_CLARIFICATION.md` fixes the problem constructively by prefetching every potential role's classical keys/settings and treating any cap exhaustion as a pre-role stop. Exact rejection-sampling counts are independent of accepted values; different private sampler streams are independent conditional on history. The role coin's accepted value is likewise independent of its rejection count. Therefore neutral cap events preserve the requisite conditional candidate, role and setting distributions. Unused keys remain private and retired. The total cap budget includes every prefetched sampler, not only the selected role's keys. This adds classical randomness/work but no source exposures. It is a necessary paid implementation choice for the literal actual-history Gamma statement.

## Fixed-port composition
The referenced fixed-port compiler is independently accepted. Its exact parameters give b+1>N/1024 and T=9N. Since a*alpha4=(4/9)*8=32/9,

 (32/9)G/(b+1) <32768 G/T.

The aggregate G already includes all three edges; no extra factor3 should be applied. For a fixed deterministic comparator budget Gamma<=gT, the net/learning remainder vanishes relative to T. This proves positive limiting readiness for g<1/32768, not readiness tending to one at nonzero g. With three edges, contamination and coherent-joint budgets give g<=6 times the appropriate expected actual-history average, hence sufficient threshold1/196608. These are conservative sufficient interface constants, not observed noise estimates or hardware thresholds.

Code-generation failure is charged once before deployment. Conditional-on-verified-code Gamma may be averaged over that conditional code-generation law, with the comparator fixed independently of realized records as required. Multiplying conditional readiness by code-success probability and union bounding yields the displayed additional beta_code. The source port remains four spins; the outer code length and trusted buffers grow. Source-exposure ratio1/1152 is preserved, not a total-time or unassisted-capacity claim. The full-path testing alternative shares the same fixed-port learner/code order.

## Additional independent diagnostics
Fifty random joint CPTP fixtures checked the positive memory effect against the direct adjoint loss, operator-level gamma inequality, mixture linearity and quadratic coherent perturbation bound. Largest equality residual4.5e-16. Exact rational rejection-sampler counting verifies independent accepted-index/count behavior and the neutral-prefetch repair. These executable checks are diagnostics of the supplied proof, not proof by random examples or a quantum hardware experiment.

No previously accepted proofs or first-review files were modified. Source hashes are bound in the accompanying receipt after author freeze.
