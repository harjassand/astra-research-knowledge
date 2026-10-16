# Warning diagnosis addendum

This is a bounded follow-up to the frozen identity/replay package in the sibling `gd_identity_replay` directory. Its `FROZEN_HASHES.sha256` file remained unchanged during this work (SHA256: `421414a2f4667a400ce77e0581b72c0937cc6cbab7be1316635a025cf230fb15`). This addendum does not alter any supplied source or the earlier frozen payload.

## Scope and method

I reran only exact byte-for-byte temporary copies of the two bounded checkers that had produced `RuntimeWarning` in the earlier replay:

- `originals/joint/independent_checks.py`, SHA256 `e4cd836b7170ce65e2a9ade126fd80603c805d254595ac62aba22743bd0cb146`
- `originals/compiler/check_compiler.py`, SHA256 `0706185b6513f321f5d9d07552ac44a0fc9061d93fedfeb83719b1300ee86fef`

The interpreter was `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13` (Python 3.13.2, NumPy 1.26.4, SciPy 1.17.1). For each checker, I ran warning-enabled copies with all recorded BLAS-related thread variables set to 1, 2, and 4. I also ran copies with `PYTHONWARNINGS=error::RuntimeWarning` at thread settings 1 and 4. Each run used a fresh temporary directory, a 60-second CPU limit, a 16 MiB output-file limit, a 90-second timeout, and disabled core dumps. No warning was suppressed. The exact source hashes were verified before execution.

For each successful warning-enabled run, stdout was parsed as strict JSON (rejecting non-standard NaN/Infinity constants), then every numeric leaf was recursively checked. The joint checker’s generated `independent_results.json` was separately parsed and checked against stdout. A structural and numeric-path comparison was made across thread settings.

## Results

| Checker | Warning-enabled runs | Emitted JSON audit | Warnings-as-errors runs |
|---|---|---|---|
| Joint independent checks | Threads 1, 2, 4 each exited 0 with 12 `RuntimeWarning` records: four each for divide-by-zero, overflow, and invalid value in `matmul`. | 90 numeric leaves (71 floats, 19 integers); all finite. Generated JSON and stdout agreed. Stdout SHA256 and every numeric value were identical across the three thread settings (maximum absolute delta 0). | Threads 1 and 4 each exited 1 on the first warning, at checker line 143; no result JSON was emitted. |
| Structured compiler check | Threads 1, 2, 4 each exited 0 with 30 `RuntimeWarning` records: ten each for divide-by-zero, overflow, and invalid value in `matmul`. | 68 numeric leaves (41 floats, 27 integers); all finite. Stdout SHA256 and every numeric value were identical across the three thread settings (maximum absolute delta 0). | Threads 1 and 4 each exited 1 on the first warning, through `check_compiler.py:97 → compiler:48 → numpy.linalg.pinv:2030`; no result JSON was emitted. |

The joint warnings are reported at the authored tensor-sink matrix products on lines 143, 146, 147, and 148. The compiler warnings are reported in `numpy.linalg.pinv` line 2030 and checker matrix-product paths at lines 26, 32, 34, 35, 49, 51, 54, 56, and 61. The unmodified warning-enabled runs reached their ends with default CPython assertion behavior: the source contains bare `assert` statements, invocation used no `-O` flag, and `PYTHONOPTIMIZE` was removed from the child environment. The warning-as-error runs fail closed at the first promoted warning rather than producing a result payload.

## Attribution and limits

The warning pattern is reproducible under all three tested thread settings on the recorded Python/NumPy/SciPy installation, with byte-identical outputs. No non-finite numeric value was found in either emitted JSON payload. That establishes only output finiteness for these runs. It does not establish that the intermediate arithmetic is valid or that the warnings are harmless.

Whether the warnings arise from the installed NumPy/BLAS implementation or indicate an arithmetic issue in the checker computations remains **UNKNOWN**. The warning-as-error result is a checker failure under strict warning policy, not a pass. This evidence does not establish the scientific claim or universal mathematical/physical correctness.

## Workspace and source boundary

A fresh read-only hash check found all 48 R source inputs still match the prior before-hashes, and every file in the earlier frozen package still matches its original hash manifest. The earlier source-integrity receipt recorded W at the requested task pin. At this follow-up’s final check, W was clean at `1ddf2056b596214023bf0cf8ae865b6a443ef2d1`; the parent confirmed this is its source-preservation commit after scientific investigation. This worker made no writes to W or to the R source inputs. The commit provenance is captured in `BOUNDARY_RECEIPT.json`.

## Execution accounting

- **Executed:** six warning-enabled checker runs (two checkers × thread settings 1, 2, 4) and four warnings-as-errors runs (two checkers × thread settings 1, 4).
- **Blocked:** none by timeout or resource limits. The four strict-policy runs terminated at the first promoted `RuntimeWarning`, as expected.
- **Not run:** warnings-as-errors at thread setting 2; all other programs, acquired/legacy programs, and the old replay wrapper.

Machine details and raw stdout/stderr for all ten runs are in `WARNING_REPLAY_RECEIPTS.json` and `raw_logs/`. The package-level `FROZEN_HASHES.sha256` records the final bytes.
