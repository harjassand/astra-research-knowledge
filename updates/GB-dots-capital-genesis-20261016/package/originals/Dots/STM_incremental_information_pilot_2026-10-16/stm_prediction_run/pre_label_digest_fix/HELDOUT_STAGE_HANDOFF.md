# Held-out stages: prepared, not executed

No real test inputs or outcomes were read during preparation. All tests used temporary synthetic fixtures. This code does not change the frozen models, features, targets, baselines, selection, or protocol. Mode 0400 is a procedural seal and is not OS-level isolation from the file owner.

## Review and code hashes

- prediction_stage.py: 979dbb1f121f2beca664d75d6aa915feeeab6a95154169fd6f081bb7babf4767
- evaluate_once.py: 8418bff40c0df70463875e002acfb6032c5b7b7770388355d2ab226b558b7857
- test_heldout_stages.py: 3245475db7cbcf8630c26fc51ec23e06007db6fdcce5ffd3fbc300be80078404
- Synthetic test log: heldout_synthetic_tests.txt (8 tests pass)

Independent review and root authorization must precede real execution. The literal approval flags are procedural guardrails, not an authentication mechanism.

## 1. Freeze, only when root authorizes

Run from /workspace/shared/stm_prediction_run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python prediction_stage.py freeze \
  --fitdir /workspace/shared/stm_prediction_run/fits \
  --sanitized /workspace/shared/stm_prediction_run/sanitized \
  --protocol /workspace/shared/stm_prediction_protocol/PROTOCOL_v1.1.md \
  --manifest /workspace/shared/stm_prediction_protocol/split_manifest.json \
  --audit /workspace/shared/stm_prediction_run/audit_report.json \
  --lock /workspace/shared/stm_prediction_run/heldout_lock.json \
  --approval ROOT_FREEZE_APPROVED
```

This verifies and hashes all nine numeric model snapshots, fit lock and hash sidecar, parameters, selected models and q, feature schema, training/development inputs/routing/labels, test inputs/routing, protocol, manifest, audit, frozen feature/training/audit code, safe reader, and prediction/evaluation/synthetic-test code. It never opens test labels. Record the returned lock SHA-256 and have root review that exact lock before prediction.

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

After preflight integrity checks, the evaluator exclusively creates sealed/TEST_EVALUATION_STARTED.json before opening the single fixed sealed/test_labels.jsonl. Changing the result output path cannot evade that marker. It remains present if parsing, validation, metrics, or result writing fails. The result is exclusively created once. Never delete either stage marker or silently retry a failed evaluation: explicit invalidation/amendment is required. An integrity failure before any label access is a preflight refusal, not a consumed evaluation.

The result includes primary and secondary metrics, both baselines, all selected-arm comparisons, all three same-hyperparameter comparison sets, planned blocks that retain excluded episode membership, block errors and paired improvements, q envelopes, support-gated classification, disagreement strata, exact GO/NO-GO criteria, and recorded-scan proxy/conditional physical-interpretation caveats. No confidence intervals, statistical significance, scan-savings or physical-safety claims.

## Synthetic tests (safe before authorization)

```sh
cd /workspace/shared/stm_prediction_run
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest -v test_heldout_stages
```

Tests create temporary synthetic data only. They cover label-free prediction, numeric inference, full metric flow, class gates, hashing/tamper failures, authorization checks, persistent one-shot markers after evaluation failure, fixed chronology membership, and macro-episode weighting.
