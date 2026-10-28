# Reproduce the dark-control continuation

The archive contains this directory and the unchanged prior continuation at
`preserved/Astra_P1_Operational_Response_Continuation.zip`. The prior archive
also retains the original reciprocal receiver archive. No network, service
credentials or physical equipment are required for these checks.

Run from the extracted archive with Python 3.12, NumPy and SciPy:

```bash
python3 p1_dark_acquisition/run_reproduce.py
```

The executed environment used Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0.
The driver verifies the prior archive's SHA-256 and extracts its `p1_next/`
sources, which supply two retained check helpers. It refuses to overwrite a
different existing prior file. It then runs the nine listed programs, saves
their standard output and a receipt, and stops on any failing assertion.
Results within the new directory are regenerated. Timings are machine
dependent; floating proposals may vary by implementation. The mathematical
certificates and matrix checks use exact rational arithmetic.

## Executed scope

1. Lattice cardinality, transforms, degree elevation, exact source identities,
   positive Bernstein and spectral error enclosures, compliance transformation,
   and four indistinguishable dark path pairs.
2. Determinant truncation, positivity, relative and absolute bounds, projector
   sharpness examples, sparse twins and the false mean-matched Poisson guard.
3. Shifted-reference calibration/de-embedding on its small conditional example.
4. The corrected Poisson-tail display's counterexample and targeted hypograph
   hull/root/rounding checks.
5. Historical curvature failure probes against the preserved original code,
   followed by focused checks of the corrected implementation.
6. Five fresh calibrated noisy acquisitions and six later tasks per case.
7. Curvature refinement of exactly those saved records, with no new source
   readings, exact LDL certificates and independent derivative checks.
8. Complete recorded acquisition/use-cost and conventional-comparison summary.

`results/REPRODUCTION_RECEIPT.json` identifies the executed program hashes.
`MANIFEST.sha256` identifies the delivered files, excluding itself. A rerun
changes timing fields and reproduction logs, so the delivered manifest then
describes the archived version rather than the overwritten rerun outputs.

## Learner/checker boundary

The learner sees scalar response intervals, known commands, prices and
declared source bounds. `native_source.py` implements a fresh exact synthetic
affine-SPD source. Its microscopic vectors and determinant/cofactor response
are used only in post-decision checks. The curvature optimizer differentiates
the acquired polynomial; it never requests the source gradient. The raw files
retain checker vectors for reproduction, not as free learner input.

The two known calibration standards, raw measurement error, ADC/DAC precision,
source offset, stable source class and bounds are declared synthetic contracts.
These programs do not acquire or verify those physical contracts on a device.
Every proposed physical use would still require the recorded settings,
preparation, settling and reset. No measured settling time or energy is claimed.

The archive's proofs and finite checks have their stated scopes. The internal
reviews are hash-specific checks of selected arguments and code, not an
independent whole-proof audit.
