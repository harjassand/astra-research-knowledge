# Finite-horizon transfer and its service obstruction
2026-10-30. New research after the 00:38:48 UTC package freeze.

- CONNECTED_COMMUTATOR_TRANSFER.md: independently reviewed exact, volume-uniform short-time local-noise conjugation estimate. It is a conditional technical tool, not a native controller theorem.
- FIXED_HORIZON_SERVICE_OBSTRUCTION.md: independently reviewed counterexample to deriving the needed uniform service from locality, raw monotonicity and finite reset paths. It defeats both initial-W and integrated-W fixed-horizon proposals in a simple two-stage controller.
- SHORT_TIME_CP_AVERAGE.md: original working route, preserved to show what was attempted. Its finite-window service premise is NOT earned and is false generically. Do not present that premise as a result.
- check_transfer.py / transfer_checks.json and check_startup_obstruction.py / startup_obstruction_checks.json: reproducible finite regressions. The asymptotic obstruction is proved analytically, not extrapolated from the tests.

Independent review: producer-workspace/REVIEW.md with exact reviewed-source hashes. This failure does not affect the separately accepted phase-dependent multiplicative CP construction in producer-workspace/simple_compiler_whole_audit_20261030.

The next native attack needs phase-dependent local service credit or another construction. Whole-window CP averaging alone is insufficient. No native two-site continuous-noise memory, practical threshold, physical retrieval, publication, or novelty claim is made here.
