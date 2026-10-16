# Held-out stages: prepared, not executed

No real test inputs or outcomes were read during preparation. All tests used temporary synthetic fixtures. This code does not change the frozen models, features, targets, baselines, selection, or protocol. Mode 0400 is a procedural seal and is not OS-level isolation from the file owner.

## Review and code hashes

- prediction_stage.py: bfe669ec3f72b947f35c6052264dbbcddcbe499132814274f096273e24e7e1bf
- evaluate_once.py: cac323867bccb5e01aeee170662aeea7a054cbd0414e2239f2d1788d17a0c369
- test_heldout_stages.py: 62b800b69ca65e99ca624b0ad8cfb28da45956599369dd89d4e77ddccb26a5ed
- seal_labels.py: 3e1f052911f72dba872178bad80366af465a83ce462fb4cb98d5802c0ba1255c
- Synthetic test log: heldout_synthetic_tests.txt (11 tests pass)

Independent review and root authorization must precede real execution. The literal approval flags are procedural guardrails, not an authentication mechanism.

## 0. Hash-only label seal, only when root separately authorizes

The initial submitted scripts omitted a prebound test-label digest. Those versions and their hashes are preserved in pre_label_digest_fix/. This correction precedes any real held-out operation and changes no modeling choice.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python seal_labels.py \
  --sanitized /workspace/shared/stm_prediction_run/sanitized \
  --output /workspace/shared/stm_prediction_run/test_label_seal.json \
  --approval ROOT_LABEL_HASH_ONLY_APPROVED
```

This separate module reads raw sealed bytes only, computes SHA-256, and writes a digest artifact. It never decodes labels, parses JSON, counts outcomes, or reports outcome summaries. Record the returned seal-artifact SHA-256. This stage is NOT authorized merely by preparation or by prediction authorization.

## 1. Freeze, only when root authorizes

Run from /workspace/shared/stm_prediction_run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python prediction_stage.py freeze \
  --fitdir /workspace/shared/stm_prediction_run/fits \
  --sanitized /workspace/shared/stm_prediction_run/sanitized \
  --protocol /workspace/shared/stm_prediction_protocol/PROTOCOL_v1.1.md \
  --manifest /workspace/shared/stm_prediction_protocol/split_manifest.json \
  --audit /workspace/shared/stm_prediction_run/audit_report.json \
  --label-seal /workspace/shared/stm_prediction_run/test_label_seal.json \
  --expected-label-seal-sha256 SEAL_ARTIFACT_SHA256 \
  --lock /workspace/shared/stm_prediction_run/heldout_lock.json \
  --approval ROOT_FREEZE_APPROVED
```

Replace SEAL_ARTIFACT_SHA256 with the approved digest from step 0. This verifies and hashes all nine numeric model snapshots, fit lock and hash sidecar, parameters, selected models and q, feature schema, training/development inputs/routing/labels, test inputs/routing, protocol, manifest, audit, frozen feature/training/audit code, safe reader, and prediction/evaluation/synthetic-test code. The expected label digest is bound separately in the lock and never placed in the generic file-hash map. Freeze and verify_lock only read the seal artifact and never open test labels. Record the returned lock SHA-256 and have root review that exact lock before prediction.

## 2. Predict, only after separate root authorization

Replace LOCK_SHA256 with the actual approved digest from step 1:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python prediction_stage.py predict \
  --lock /workspace/shared/stm_prediction_run/heldout_lock.json \
  --expected-lock-sha256 LOCK_SHA256 \
  --output /workspace/shared/stm_prediction_run/test_predictions.json \
  --approval ROOT_PREDICTION_APPROVED
```

All eleven models are predicted, including the two baselines. All nine learned candidates use frozen train.predict_frozen numeric inference. Input/routing hashes and code/model hashes are rechecked. Predictor arrays strip routing keys. The canonical fits/TEST_PREDICTION_STARTED.json marker prevents repeating inference with a changed output path. No test outcome is opened. Record the returned prediction SHA-256. Do not run evaluation until root separately authorizes that exact prediction artifact and lock.

## 3. Evaluate once, only after separate root authorization

Replace LOCK_SHA256 and PREDICTIONS_SHA256 with the root-approved values:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python evaluate_once.py \
  --lock /workspace/shared/stm_prediction_run/heldout_lock.json \
  --expected-lock LOCK_SHA256 \
  --predictions /workspace/shared/stm_prediction_run/test_predictions.json \
  --expected-predictions PREDICTIONS_SHA256 \
  --output /workspace/shared/stm_prediction_run/test_result_once.json \
  --approval ROOT_ONE_SHOT_EVALUATION_APPROVED
```

After preflight integrity checks, the evaluator exclusively creates sealed/TEST_EVALUATION_STARTED.json before opening the single fixed sealed/test_labels.jsonl. Changing the result output path cannot evade that marker. The evaluator compares the raw label bytes with the lock-bound expected digest before parsing or scoring. A mismatch, including valid-but-changed JSON labels, consumes the attempt and aborts. The marker remains present if digest comparison, parsing, validation, metrics, or result writing fails. The result is exclusively created once. Never delete either stage marker or silently retry a failed evaluation: explicit invalidation/amendment is required. An integrity failure before any label access is a preflight refusal, not a consumed evaluation.

The result includes primary and secondary metrics, both baselines, all selected-arm comparisons, all three same-hyperparameter comparison sets, planned blocks that retain excluded episode membership, block errors and paired improvements, q envelopes, support-gated classification, disagreement strata, exact GO/NO-GO criteria, and recorded-scan proxy/conditional physical-interpretation caveats. No confidence intervals, statistical significance, scan-savings or physical-safety claims.

## Synthetic tests (safe before authorization)

```sh
cd /workspace/shared/stm_prediction_run
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest -v test_heldout_stages
```

Tests create temporary synthetic data only. Additional tests verify hash-seal authorization, raw hashing of non-UTF-8/non-JSON bytes without decoding, no evaluator label reads before the marker, and rejection of valid-but-changed labels before scoring. They cover label-free prediction, numeric inference, full metric flow, class gates, hashing/tamper failures, authorization checks, persistent one-shot markers after evaluation failure, fixed chronology membership, and macro-episode weighting.
