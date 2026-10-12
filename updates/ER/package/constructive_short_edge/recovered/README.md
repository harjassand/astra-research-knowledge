# Constructive Short-Edge Geometry

Read `constructive_short_edge_geometry.md` for the theorem, input/oracle model, proof, provenance, and limitations.

## Executable scope

`cell_repair.py` implements exact enclosing-cell repair for an explicitly described rational polytope and fixed affine slice. It returns a bounded-encoding rational vertex of the clipped slice using exact boundary pushes. It discards temporary grid facets when reporting the original face. It is not a full discrepancy-rounding implementation.

Run the diagnostics with:

```sh
python exact_audit.py
OPENBLAS_NUM_THREADS=1 python spectral_audit.py
```

Dependencies: Python, SymPy; NumPy and SciPy for the floating-point local spectral audit. No network access is needed to run the scripts.

The JSON files contain the executed results. `audit_history.md` records the unsuccessful preliminary runs and scope limitations.

`sources/` contains the user's earlier constructive manuscript. It is historical research capital; its claims of earlier audits are not new independent verification in this run. The current note replaces its affine-anchor repair, explicitly allowing descent to a smaller original face.

No complete spectral rounder, sampling backend, or runtime benchmark is included. The complete mathematical construction has not been independently reviewed or formally verified. Novelty is unverified.
