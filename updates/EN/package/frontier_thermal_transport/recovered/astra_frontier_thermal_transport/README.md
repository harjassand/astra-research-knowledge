# Reproducibility packet

The scientific result, proofs, hypotheses, resource accounting, prior-art attribution, and exact remaining obstruction are in **research_note.md**.

**checks.py** reproduces small floating-point checks and the exact rational three-spin localization certificate. **checks.json** contains executed results. **research_state.json** records scoped status and a precise continuation gate.

Run from this directory:

```bash
OPENBLAS_NUM_THREADS=1 python checks.py --output checks.json
```

The executed environment used Python with NumPy 2.3.5 and SciPy 1.17.0. The script uses standard NumPy/SciPy interfaces and Python fractions; no external data, credentials, or network calls are needed. Runtime and floating residuals may differ across installations.

Most diagnostics use floating-point linear algebra and numerical quadrature. They are not interval proofs. The exact rational certificate is separately identified and bounds **ideal-filter localization error**, not the numerical solver or a physical device. Its input coefficient arithmetic uses Python fractions. The complete mathematical argument is in Section 5 of the note.

Nothing here was committed to either research repository. No reference equilibrium preparation, quantum circuit, hardware calibration, or large-system benchmark was performed. Historical novelty and independent mathematical validation remain unresolved.
