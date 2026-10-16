# Reproduce the bounded result

Read HANDOFF.md first, including the distinct >1/4 common-scalar extension, then OVERWRITTEN_PRODUCT_OBSTRUCTION.md (PROOF.md gives the intermediate native-boundary result). Use Python 3.10 or later; run:

    python replay.py

This verifies payload hashes and runs the both exact static-product proofs and the common-scalar certificate conditions, prior exact product/coupled checks, and conditional absorbing-diffusion algebra using the Python standard library only. No network or upstream Julia execution is used. For numerical operator/gate smoke tests, install NumPy and SciPy in your own environment, then run:

    python replay.py --numerical

Recorded verification environment: Python 3.12, NumPy 2.3.5 and SciPy 1.17.0. Numerical smoke tests are not interval certificates. Runtime and floating outputs may differ across systems. Each check is run as a subprocess; a failed assertion or nonzero exit fails replay. Exact results do not depend on the earlier numerical searches. Discovery/optimization scratch and copyrighted paper PDFs are intentionally absent.

MANIFEST.json covers all payload files except itself and REPLAY_RESULTS.json; that result file reports replay of this manifest after clean ZIP extraction. The ZIP's externally reported SHA-256 pins every byte, including those two files.
