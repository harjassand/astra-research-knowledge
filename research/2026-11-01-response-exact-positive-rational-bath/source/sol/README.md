# Single Sol scientific work, first turn

Start with [REPORT.md](REPORT.md). Full construction and proofs: [DERIVATION.md](DERIVATION.md). Exact failed-thermal-promotion discriminator: [TWO_QUANTUM_OBSTRUCTION.md](TWO_QUANTUM_OBSTRUCTION.md). Sources and version-bound acceptance: [SOURCES.md](SOURCES.md), `source_receipts.json`. Preserved alternatives: [ALTERNATIVES.md](ALTERNATIVES.md).

Status: a derived and executable candidate primitive for one explicit gapless Gaussian bath family. No independent audit of the new proof, historical-priority conclusion, hardware validation, practical advantage or revolutionary outcome is claimed. Programme sources retain their actual accepted/unreviewed scopes.

Reproduce using Python3 with numpy, mpmath, sympy, matplotlib (versions used: numpy 2.5.3, mpmath 1.3.0, sympy 1.14.0, matplotlib 3.11.2):

```sh
python3 response_exact_bath.py --check
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 noncommuting_check.py
python3 two_quantum_check.py
python3 extra_synthesis_check.py
python3 make_figure.py
```

The scripts write numerical results and explicit physical matrices under `results/`. They do not contact an external service, fit supplied bath data, or modify programme checkouts. The scientific figure is `results/construction_checks.png` (PDF also included).

The task-first Astra fallback uses pinned raw corpus bytes, reference content-posting scoring and verified projection hashes. `sources/astra/SEARCH.json` preserves its results. An existing shared local checkout rejected retrieval as stale; it was not rebuilt or edited. No scientific publisher or programme chat was contacted.
