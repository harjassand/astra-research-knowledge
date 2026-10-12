# ASTRA FRONTIER: balanced transport continuation

Start with `research_note.md`. The mathematical result is a nonperturbative bound on a specified infinite-chain **second-moment** transport coefficient, together with a local-intervention decision certificate. It is not a Gaussian hydrodynamic theorem, a general matter solver, or independently validated novelty.

## Main result

For a translation-invariant nearest-hop spin chain with arbitrary bounded finite-range diagonal density interactions and calibrated on-site dephasing, let hopping be t, two-site coherence damping d=4 gamma, and Xi the uniform mean squared allowed-hop energy detuning. The note derives

    2 t^2 d / (d^2 + Xi) <= D <= 2 t^2 / d.

Section 7 supplies the infinite-volume and long-time argument, rather than extrapolating a finite ring. Sections 3–4 give balanced primal–dual witnesses and their exact classical-exclusion pressure solve. Section 10 supplies a conditional-confidence local Ramsey decision rule.

## Reproduce

Use Python with NumPy, SciPy and SymPy; versions used are in `environment.json`.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments.py
OPENBLAS_NUM_THREADS=1 python noise_response.py
OPENBLAS_NUM_THREADS=1 python block_checks.py
python ramsey_certificate.py
OPENBLAS_NUM_THREADS=1 python larger_checks.py
```

These commands overwrite the corresponding JSON outputs. Recorded timings depend on the execution environment. Rational fields are exact mathematical certificate values; floating comparisons and synthetic Ramsey samples are separately labeled. Synthetic samples are not physical measurements.

## Evidence boundaries

All five scripts were executed. No formal proof assistant, external proof reviewer, device experiment, full model calibration, or strongest-method performance comparison was supplied. No original repository was modified. `sources.json` records targeted primary sources and exact repository revisions. `manifest.json` records file hashes, not scientific validation.

## Unresolved capability

G1 in the note asks for a polynomial-cost construction of high-precision balanced witnesses, charging representation growth and the exact pressure solve. G2 asks for quantitative Gaussian hydrodynamics. Neither is established. The passive-Gibbs rare-information lower bound from the preceding investigation remains intact.
