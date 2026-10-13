# CRAY GENESIS: response-cell acquisition

Research packet dated **13 October 2026**. Read `REPORT.md` for proofs, assumptions, prior art, scientific limits, and resource accounting.

## Status

This is a candidate acquisition interface with internally derived mathematics and executed synthetic tests. It is not an independently validated or historically novel breakthrough, and it does not establish a real-material or ab initio speedup.

## Contents

- `experiment.py`, `results.json`: 65,536-vertex float64 synthetic comparison against matched Hoeffding acquisition and a full sparse solve; includes a failed strong-mismatch case.
- `exact_checks.py`, `exact_results.json`: 3,223 counted exact-rational assertions over 32 small connected graphs plus a zero-reference-work test.
- `finite_bit_demo.py`, `finite_bit_results.json`: lazy rational coefficient acquisition, integer/rational confidence arithmetic, full sampled-index stream and exact interval endpoints. No NumPy or SciPy dependency for this script.
- `cell_probe.py`, `cell_results.json`: full-data local-cell coarsening experiment. This experiment acquires ALL target coefficients; it is not an acquisition-saving result.
- `requirements.txt`: dependency versions used.
- `manifest.json`: SHA-256 hashes for the packet files except the manifest itself.

## Reproduce

Python 3.11 or newer is appropriate. Install the supplied scientific-package versions in a separate environment when needed.

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py
python exact_checks.py
python finite_bit_demo.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python cell_probe.py
```

The scripts overwrite their corresponding result JSON files. Timings are environment dependent. Seeded statistical results are reproducible subject to library behaviour; the statistical theorem presumes independent random bits, not a formally verified PRNG.

An optional non-seeded OS-backed acquisition run is:

```bash
python finite_bit_demo.py --system-random
```

The finite-bit demonstration uses an analytically available reference field. Its finite-bit confidence arithmetic does not imply a generic verified reference solver. Synthetic oracle arithmetic stands in for expensive microscopic acquisition; no physical rate calculations were performed.
