# Exact path exterior-square endpoint certificate

Read `EXTERIOR_CERTIFIER_REPORT.md` first. This is a research prototype for fixed symmetric nearest-neighbor exchange on a path. It is not an arbitrary graph solver or a physical dataset.

Dependencies: Python 3, NumPy, SciPy, and mpmath, already installed in the reported environment. No installation is performed by these scripts. Only NumPy and the Python standard library are needed for the main certificate; SciPy/mpmath are used for separate checks.

From this extracted directory:

- `python exterior_certificate.py --n 20 --output reproduced_certificate.json`
- `python verify_exterior.py`
- `python check_incumbent_residuals.py`
- `python check_sampler.py`
- `python cycle_extension/check_cycle.py`

To repeat the single expensive baseline comparison: `python run_dense_bounded.py`. It stops the original dense certifier at 240 seconds if no result has been produced. It can consume hundreds of MiB. This comparison is optional for reproducing the successful certificate.

The original dependency files are copied byte-for-byte under `original_dependencies/`. `PAIR_CERTIFICATE_BASE` can override that directory. The historical measured receipts are retained; subsequent executions replace a script's corresponding receipt unless an output option is provided. Use a fresh extracted copy to preserve the reported receipts.

`tested_source_snapshot/` preserves the exact source versions used for the original timed runs. Their absolute paths reflect the original environment; use the top-level portable versions to rerun. The sole main-script semantic change after its timed run is a guard rejecting the unsupported averaging wrapper case n<4. Portable replay reproduced the exact rational result.

`MANIFEST.json` records file hashes and dependency provenance. The compact cycle proof is algebraically checked, but an end-to-end cycle averaging certificate was not run. The report distinguishes exact certificates from diagnostics throughout.
