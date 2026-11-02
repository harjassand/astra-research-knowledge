# Reproduce the ordinary proof/calculation package

Read `RESULT.md` first. The governing implementation is the untouched-source K15 certificate; the K13 encoding is optional.

## Required inputs

Python3, NumPy (only the full Gibbs regression needs NumPy), and the existing source fixture:

`producer-workspace/example_6_8_polygon_data.json`

The source geometry and exact recursive port convention are in the already declared `explicit_cochain_fibers_20261102/ATLAS_NORMALIZATION.md` and the source Section6.2. They are mathematical premises for the all-level closure, not replaced by finite tests. This package does not claim a new full global integer-coordinate source generator.

## Governing regressions

Run from any working directory:

```
python producer-workspace/boxed_link_geometry_certificate.py
python producer-workspace/audit_k13_regression.py
python producer-workspace/direct_clifford_gibbs_regression.py
python producer-workspace/thermal_reduction_regression.py
python producer-workspace/audit_hpl_regression.py
```

The first produces252 complete boxed-star records. The independent audit checks all252, the named coordinate inventories and172,816 exact Clifford action identities. The full Gibbs regression checks672 finite-temperature states. The last two test the separately retained abstract thermal-contraction/parity theory.

Additional link/halo/octahedron scripts and JSON files are exploratory diagnostics, not premises of the K15 certificate. In particular the stronger simple-octahedron and optimized-vertex-basis routes are not being silently used. Primary-source HTML/text and figure images are retained only for provenance; ordinary derivations and executable matrices are the substantive deliverable.

`SHA256.txt` hashes all package files except itself and transient Python bytecode. Re-running deterministic scripts should preserve their listed JSON hashes.
