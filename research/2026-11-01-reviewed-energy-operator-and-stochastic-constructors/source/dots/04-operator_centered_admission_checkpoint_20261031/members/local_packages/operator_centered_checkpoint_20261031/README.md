# Raw-operator and centered-source admission checkpoint

31 October 2026. Local-only checkpoint; no upload is performed by its builder.

## Scientific scope

This bundle contains reviewed mathematical admission proofs, exact finite known-model certificate acquisition/checking, complete static schedule receiving, saved tests and resource rows. It includes the separate canonical source-creation activity result. It does NOT claim hardware calibration, quantum gate synthesis/execution, an experimentally attained loss ratio, a new threshold number, practical superiority or historical novelty.

Some immutable sources retain “candidate/unreviewed” in their original headers. Acceptance is determined by the exact source hashes and scoped independent receipts in REVIEW_BINDINGS.json, not by silently editing those original headers. The source-creation activity result counts the specified Markov loss/injection jumps, not heat or power.

## Reading order

1. `raw_local_operator_acquisition_20261031/RAW_OPERATOR_ACQUISITION_AND_RECEIVING.md` and its TWO receipts (core and schedule wrapper).
2. `local_injection_fault_admission_20261031/CLAMPED_WEIGHT_INJECTION_CANDIDATE.md` and final-source receipts.
3. `centered_source_acquisition_20261031/GENERAL_DRIFT_CLAMPED_RECEIVER.md`, `CENTERED_SOURCE_ACQUISITION_SPEC.md`, and whole receipt.
4. `local_injection_fault_admission_20261031/SOURCE_CREATION_ACTIVITY_CANDIDATE.md` and activity review.
5. `local_energy_fault_admission_20261031/PRIMARY_COMPARISON_AND_CONSEQUENCE_BOUNDARY.md` plus the comparison/cost sections of the new specifications.

The guarded mode requires BP=0 and can be much cheaper. The centered mode acquires projectors from bounded subsets of actual positive-rate one-cell source jumps, tests PBP=0, and checks ALL generator terms. Its fixed-diffusion disturbance does not vanish merely by increasing loss. Physical loss/injection/control acquisition remains a premise.

## Reproducibility

Core tools require Python and SymPy1.14.0. Floating diagnostic scripts additionally use NumPy/SciPy; they are diagnostics, not certified numerical proofs. All acquisition and verifier fixtures use exact rational arithmetic. No packages are installed by this bundle.

Directory structure is preserved because executable components hash-check and import their frozen relative-path dependencies. To run author suites without rewriting saved JSON, use their `run()` functions:

```
PYTHONPATH=raw_local_operator_acquisition_20261031 python -c 'import test_operator_certificate as t; print(len(t.run()[0]))'
PYTHONPATH=raw_local_operator_acquisition_20261031 python -c 'import test_operator_schedule as t; print(len(t.run()[0]))'
PYTHONPATH=centered_source_acquisition_20261031 python -c 'import test_centered_acquisition as t; print(len(t.run()[0]))'
```

Expected supplied counts:113,20,152. Running those test files directly intentionally regenerates their fixture/result JSON; do so only in a disposable copy. Independent checks are also included. The pre-complex-normalization raw implementation is HISTORICAL FAILURE EVIDENCE, not the accepted implementation. Its valid-complex-input false rejection/crash was repaired in the current code and is described in the source/receipt.

## Package integrity and exclusions

MANIFEST.json contains byte counts and SHA256 for every payload file except the manifest itself. REVIEW_BINDINGS.json records exact current proof/code and receipt dependencies. BUILD_ALLOWLIST.py lists every permitted source path literally, rejects symlinks and missing files, builds deterministic entries, then reads the ZIP back and checks its exact member set and all hashes. No glob directory capture, private conversation logs, credentials, caches, environments, or unrelated archives are included.

The package filename/hash identify transport bytes; they are not additional scientific reviews. No upload, publication or external transfer is performed.
