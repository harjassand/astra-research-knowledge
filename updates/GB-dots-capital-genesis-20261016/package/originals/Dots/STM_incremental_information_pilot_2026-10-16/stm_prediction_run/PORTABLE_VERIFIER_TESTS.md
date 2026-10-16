# Portable verifier tests

Verifier: `verify_portable.py` (SHA-256 `12458daafa5a85b3d712398ae7f107956c30314db288ecc12331a368a01f8e82`).

## Scope

Independent arithmetic reconstruction on the **same released held-out records**. No production-module imports, fitting, prediction/evaluation stage calls, model execution, downloads, or new experimental validation. The original independent verifier and frozen production artifacts were not changed.

## Executed tests

All replay and rejection tests ran with `python -O`, so they do not depend on Python assertions. Separate isolated bundle copies were tested under `/tmp` and `/workspace/shared`; shared delivery staging was not modified by these tests.

- Clean relocated bundle: PASS, 3,892 equality checks, 100 rows, 60 episodes, original NO-GO decision reproduced. This is the original 3,910 equality checks minus 18 unavailable model-byte hash comparisons (nine models referenced by two locks). Additional explicit array identity, manifest completeness, size/hash, path, and omission checks also passed.
- Appending a byte to sanitized training labels: rejected on manifest size mismatch before arithmetic; no result file created.
- Removing an original-path mapping for a locked dependency: rejected as a missing unexpected original dependency.
- Reusing an existing output path: rejected; output is created exclusively and must reside outside the bundle.

The final source resolves bundle-local descendants before mapping original absolute paths, allowing relocation beneath `/workspace/shared` as well as elsewhere. Marker output-path checks still assert the original production paths.

## Omissions and limits

Nine numeric model snapshots are intentionally absent. Their declared hashes are cross-checked against both original locks, but their bytes are explicitly reported as **NOT VERIFIED**. The manifest also lists intentionally omitted raw/source artifacts. Included file bytes and included locked dependencies are hash-verified before arithmetic. Hash manifests do not authenticate coordinated malicious replacement of the verifier and manifest.

These tests used isolated staging copies. The parent packaging task will independently test the final ZIP after fresh extraction.
