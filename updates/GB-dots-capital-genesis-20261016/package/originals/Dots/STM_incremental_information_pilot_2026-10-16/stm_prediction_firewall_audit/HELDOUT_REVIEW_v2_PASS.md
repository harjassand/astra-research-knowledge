# Corrected held-out-stage review: PASS

2026-10-16 UTC. This addendum resolves the specific blocker in HELDOUT_REVIEW_v1.md; both that original review and phase-one REPORT.md are preserved.

## Decision

PASS for the corrected freeze, label-blind prediction and one-shot evaluation implementation, subject to root's separate authorization for actual operations. No real test features, labels, outcomes, predictions or episodes were accessed by this reviewer, including no hash-only access to actual labels. No actual stage was executed by this reviewer.

Audited and preserved in heldout_corrected/:

- prediction_stage.py: bfe669ec3f72b947f35c6052264dbbcddcbe499132814274f096273e24e7e1bf
- evaluate_once.py: cac323867bccb5e01aeee170662aeea7a054cbd0414e2239f2d1788d17a0c369
- test_heldout_stages.py: 62b800b69ca65e99ca624b0ad8cfb28da45956599369dd89d4e77ddccb26a5ed
- seal_labels.py: 3e1f052911f72dba872178bad80366af465a83ce462fb4cb98d5802c0ba1255c

## Blocker resolution

1. seal_labels.py requires ROOT_LABEL_HASH_ONLY_APPROVED before access and checks mode0400. It reads raw bytes only, computes SHA-256 and writes a new seal artifact with canonical path and digest. It never decodes, parses, counts or summarizes outcomes.
2. Freeze requires the expected seal-artifact hash, verifies target path and digest syntax, and binds the expected label digest into the held-out-v2-label-digest lock. The seal artifact and seal script join the regular code/dependency provenance. Raw labels do not join the generic hash list.
3. verify_lock explicitly rejects the sealed-label path in generic dependency hashes. It verifies only the seal artifact and its agreement with the bound expected digest, without opening labels.
4. Evaluator still requires separate ROOT_ONE_SHOT_EVALUATION_APPROVED, verifies all ordinary dependencies and prediction hashes, then exclusively creates the canonical TEST_EVALUATION_STARTED.json marker before its first label read. It compares the exact bytes' SHA-256 with the frozen expected label digest before JSON decoding or scoring.
5. Any mismatch consumes the attempt and creates no result. The marker is retained and prevents retry even with another output filename. A valid but changed label payload is now tested explicitly, in addition to malformed JSON and generic hash mutations.

The initial stage versions remain preserved; no feature map, candidate, fitted model, development choice, metric or GO rule changed. This is an integrity correction before actual held-out use, not test-informed tuning.

## Verification

The corrected sources' exact hashes match the implementation worker's handoff. All19 synthetic tests pass:11 submitted stage tests plus8 independent tests originally authored for this audit. Results: heldout_corrected_results.txt. Independent test source: test_heldout_independent_v2.py. Tests use synthetic temporary files only.

Coverage includes label-blind prediction, explicit approvals, seal without JSON/text decoding, no pre-marker label read, one actual evaluator label read, exact marker-before-read ordering, valid label tamper rejection, failure burn, no alternate-output retry, all six screening gates, selection fixed despite better unselected test candidate, macro episode weighting, support-only unavailable classification, preserved chronological blocks, model/prediction hash integrity and descriptive metrics.

Root should authorize and retain the returned seal-artifact hash, then frozen lock hash, then prediction-artifact hash in that order before separately authorizing the one-shot evaluator. The reviewed code enforces those supplied hash bindings, but approval strings and mode0400 remain procedural controls rather than security isolation from the same operating-system owner. A future failure after the marker must not be retried without explicit invalidation/amendment.

All passing substantive metric/protocol findings from HELDOUT_REVIEW_v1.md remain applicable. Any eventual numerical result is for the recorded-scan proxy subset; physical pre-scan timing/freshness interpretation remains conditional on documented logger semantics, with no claim of verified physical freshness, actual scan savings, safety or prospective deployment authorization.
