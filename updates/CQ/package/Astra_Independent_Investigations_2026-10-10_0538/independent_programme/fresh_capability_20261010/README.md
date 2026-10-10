# Fresh capability screen

Outcome: no qualifying transformative computational invention.

- `RESULT.md`: selection, constructions, proofs, native-cost audit, and rejection
- `PRIMARY_SOURCES.md`: verified prior-art boundary
- `test_attention_edit_gate.py`: first-layer identity, group-radius gate, and
  nonzero-margin moment-summary collision
- `attention_edit_gate_results.json`: nine complete seeded 12-layer runs
- `test_correlated_edit_transport.py`: rank-one edit transport and mixed-product
  identity checks
- `correlated_edit_transport_results.json`: five complete seeded runs

Reproduce with Python 3 and NumPy:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_attention_edit_gate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python test_correlated_edit_transport.py
```

Only modest native CPU was used (a few seconds). These synthetic numerical
checks are mechanism gates, not trained-model benchmarks or formally rounded
certificates. See the report's exact limits before using any result.

A subsequent qualitative-measurement candidate is preserved in `phase_pair/`:
paired phase encoding cancels unknown periodic detector response under exact
actuation symmetry. Its exact theorem, finite BV certificate, twelve small
synthetic checks, and decisive 1984/2015 prior-art boundary are recorded there.
It too is closed as a transformative-invention candidate.
