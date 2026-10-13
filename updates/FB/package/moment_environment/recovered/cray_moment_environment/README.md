# CRAY finite-moment environment research

Start with `RESEARCH_NOTE.md`. It states the exact assumptions, proofs, acquisition costs, prior-art comparison, and failures. This package does not contain a real adsorption calculation or a demonstrated solver speedup.

## Reproduce

Python 3 with NumPy, SciPy, and SymPy is used for numerical diagnostics. The exact principal certificate uses only the Python standard library.

```bash
python certify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python additional_tests.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python acquisition_test.py
```

`exact_certificate.json` contains rational spectral root intervals and the resulting exact uncertainty enclosure. `additional_results.json` includes the rational non-Gaussian counterexample witness. Numerical interacting and lattice controls are in `numerical_results.json`; the sampling diagnostic is in `acquisition_results.json`.

The signed-band theorem uses coupling weights and first **absolute-energy moments**. The symmetric-bath theorem and its certificate use coupling weights and **squared-energy moments**. They are distinct input contracts.

Floating-point routines drop very small numerical eigenvalues and use ordinary eigensolvers; they are diagnostic implementations, not validated matrix-input certification software. The main scalar certificate instead isolates all required roots in rational arithmetic. Historical priority of the proposed characterizations remains unestablished.
