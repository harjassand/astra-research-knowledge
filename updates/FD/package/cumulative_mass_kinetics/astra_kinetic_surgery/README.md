# ASTRA cumulative-mass transport checkpoint

Read `RESEARCH_NOTE.md` for derivations, scope, failures, resource accounting and references.

Run diagnostics with:

```bash
python -m pip install sympy==1.14.0
python verify.py
```

`results.json` is the complete recorded diagnostic output. `run_log.json` is the console summary from the execution. Tests are finite exact algebra or manufactured symbolic checks, not a molecular performance benchmark. The 1D logarithmic enclosure comparison is explicitly numerical; no complete certified high-dimensional integration engine is provided.

`RESTART.md` preserves the consequential objective and exact unresolved acquisition problem. `MANIFEST.json` records file hashes for this generated checkpoint. Hash checks establish file integrity, not scientific truth.
