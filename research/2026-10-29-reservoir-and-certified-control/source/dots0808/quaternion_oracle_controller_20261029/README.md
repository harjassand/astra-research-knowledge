# Certified quaternion controller — 2026-10-29

## What changed
The acquired star-loss bank reduces exactly to35 homogeneous-quartic coefficients in a unit quaternion. A small executable global optimizer now returns an ACTUAL rational rotation and an exact rational lower certificate, rather than assuming an SO3 optimization/SDP-rounding oracle. On six real acquired banks the certified global mean-loss gaps were below1.8e−10 with about0.09–0.30s solver/verification time each. This is a promising controller-component improvement, not a uniform speed or hardware claim.

## Governing accepted scope
`QUARTIC_ORACLE_v1.md` gives exact bank compression, rational Gram/LDL certificates, the genuine non-SOS limitation and complete finite grid fallback. `FINITE_FTPL_DRAFT.md` derives fresh finite-bit perturbed-leader regret with a proved approximate-oracle bias allowance, same physical probe feedback and actual-history comparison. Despite its filename, its exact mathematical scope is accepted by `producer-workspace/REVIEW_RECEIPT.json`; read that receipt for dependencies/exclusions. `CORE_SHA256SUMS.txt` freezes those proofs and governing code. Existing net/tracking controllers remain completed fallbacks; this is not yet a reviewed replacement for unknown-budget drift tracking.

The oracle's fallback is complete when actually run without a point cap, but can be astronomical. A point limit reports failure, not success. Current-candidate-dependent runtime must be padded to a deterministic schedule or genuinely isolated from the source clock; that can erase apparent speed gains. Trusted control synthesis, source privacy, buffering and outer codes remain paid.

## Executed evidence
- `capture_one_axis.py`, `capture_drift.py` and `bank_*.json`: replayed60k-call retained-bath fixtures,29,916 actual sampled probes each, three exact coefficient banks. No new physical measurement is claimed.
- `oracle_*_edge*.json` and `check_certificates.py`: six independent exact bank/rotation/Gram/LDL checks. `CONCRETE_BANK_CERTIFICATES_SHA256SUMS.txt` freezes these inputs/results.
- `check_nonsos_limit.py/json`: nonnegative Choi–Lam quartic; low-degree SOS fastpath does not attain its true minimum. The proof of non-SOS is algebraic, not inferred from solver failure.
- `certified_oracle.py` and its checks: actual-bank success, zero polynomial,4913-point exact fallback, and an honest non-SOS resource-cap failure. Five malformed exponent inputs are rejected; the review-found normalization bug is corrected.
- `check_perturbed_queries.py` and24 saved query certificates: actual-bank FTPL-style finite perturbations all met the requested absolute gap~2.93e−6; these are offline queries, not a controller trajectory.
- `check_online_ftpl.py` and `online_ftpl_result.json`: a120-call three-role retained-bath diagnostic actually completed38 probes,59 matching validations and23 averaged-orbit services. All360 edge calls returned exact certificates; independent Fraction-only verification passes. Solver time72s. Performance is NOT good protection:25 validation failures and mean service bad weight0.336. No outer code, unknown payload or laboratory latency model is executed; capped-oracle failure would have stopped this diagnostic, not counted as neutral.
- `critical_chart_attempt.py/log`: separate bounded exploratory algebraic critical-point attack. Not part of accepted oracle success unless a later complete certificate is supplied.

Programs require Python, NumPy, SciPy and SymPy. Exact verifiers do not trust numerical optimality flags. Rational Gram identities and candidate objective values are the evidence. `PRIMARY_OPTIMIZATION_SOURCES.md` records actually-read prior SOS/FTPL machinery; those methods are not claimed as inventions here. No historical novelty or superiority to the equally informed conventional full-path baseline has been established.

## Important corrections and unresolved obligations
The wrapper initially silently discarded malformed monomial keys; it now rejects them before canonicalization. A preliminary perturbed-query harness encountered a missing zero coefficient and stopped before its last edge; it was corrected and all24 queries rerun. SLSQP is bounded to the unit cube to prevent irrelevant off-sphere overflow; exact verification, not floating success, governs every returned certificate. No accepted proof depended on those failed preliminary runs.

The main remaining barrier is dependable small total control latency/cost, not only a fast successful average solve. Global mean empirical-loss optimality also does not itself certify future service protection; the actual matching/outer-code guard remains necessary. Stronger solver families, better statistical constants and controller timing/privacy interfaces remain worthwhile research, with the accepted finite net fallback retained.
