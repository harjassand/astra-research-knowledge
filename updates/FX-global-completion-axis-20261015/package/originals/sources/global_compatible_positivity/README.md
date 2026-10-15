# Astra: global compatible-positivity completion

Start with **RESEARCH_REPORT.md**.

The principal result is an exact characterization of which coefficients in the full four-dimensional shear-contact face admit quasiconvexity after adding a finite multiple of the Cauchy–Riemann distortion fourth power H. It is an equality of projected rank-one-convex and quasiconvex cones, not equality at each fixed H coefficient.

A universal isotropic-heat certificate covers r<-2 and r>0, using a 6+4 quotient repair followed by an eight-dimensional convex completion. An explicit compatible Fourier example independently shows that constant linear heat misses even the polyconvex determinant square.

## Exact verification

With Python 3.10+ and SymPy installed:

```sh
python verify_global_structure.py
python replay_previous.py
```

The first program reads only the portable new JSON certificate. It checks universal identities, closedness, positive pivot formulas, projection identities, acoustic obstructions, exact Fourier dissipation, and rational completions. The second hash-checks and replays the unchanged supplied package in a temporary directory.

## Compile a new rational member

```sh
python compile_completion.py --r=-11/4 --alpha=27 --output=my_certificate.json
python compile_completion.py --r=1/2 --method=trace --output=trace_certificate.json
```

The compiler certifies P_(alpha,r)-H. With no alpha argument it selects the ceiling of its sufficient bound. Rejection below this bound is not a proof of impossibility. `EXAMPLE_27_COMPLETE.json` is a complete rational instance already checked in this run.

## Main files

- `GLOBAL_COMPLETION_CERTIFICATE.json`: universal rational matrices, forms, and orderings.
- `GLOBAL_VERIFICATION.json`: executed exact-algebra receipt.
- `RESEARCH_REPORT.md`: analytic proof, global scope, and limitations.
- `FAILED_CASES_AND_NEXT_OBLIGATION.md`: separates three negative results and fixes the next mathematical obligation.
- `SOURCES_AND_REVIEW.md`: inherited mathematics and actual source-reading/review scope.
- `inputs/previous_moving_kernel_package.zip`: unchanged incoming mathematical capital.

`MANIFEST.json` records hashes of final package files. Independent external mathematical review, formal verification, and historical priority are unresolved. No repository or user Library content was modified.
