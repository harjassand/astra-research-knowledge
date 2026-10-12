# CRAY conditional-resonance research packet

Start with `RESEARCH_NOTE.md`. This is a derivation-and-falsification packet, not a claimed sign-problem breakthrough.

## Main result and decision

An acquired intermediate-field reference provides an independent Gaussian estimator with explicit ideal-arithmetic phase, variance, and approximation bounds for strongly gapped onsite-quartic actions. It is practical on the test inputs, but specialised transfer and two-order Wick calculations outperform it. Its useful certificate selects an effectively weak-interaction regime.

The stronger surviving opening is exact conditional integration across local determinant resonances. The heat/Fourier identity, finite-order error, block extension, and genuine logarithmic-variance cancellation are derived. An affordable global decomposition and remaining-phase theorem are not established. Historical priority and independent correctness remain unresolved.

## Reproduction

Use Python 3 with NumPy, SciPy, SymPy, and mpmath. Versions used are recorded in `environment.json`. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_benchmarks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python exact_algebra_checks.py
python spectral_heat_continuation.py
python true_resonance_check.py
```

The commands regenerate result JSON files and the seeded grid inputs. Timings vary by hardware and libraries. The complete benchmark makes tens of thousands of dense matrix factorisations; the small algebra/heat scripts can be run separately. No network, API key, external model, or repository checkout is required.

## Files

- `resonance_compiler.py`: model generation, branch-safe determinant, acquired proposal, ideal-arithmetic bounds, independent sampling, and Wick comparator.
- `run_benchmarks.py`, `benchmark_results.json`, `grid_*.npz`: matched chain and independently seeded square-grid tests; gate sweep and under-resolved transfer output retained.
- `exact_algebra_checks.py`, `exact_algebra_results.json`: 200 exact finite matrix assertions on 20 rational fixtures.
- `spectral_heat_continuation.py`, `spectral_heat_results.json`: local identity, explicitly acquired remainder majorants, 12 high-precision-reference diagnostics.
- `true_resonance_check.py`, `true_resonance_results.json`: genuine determinant-zero fixture and logarithmic second-moment asymptotic.
- `CLAIMS.json`, `SOURCES.json`, `RESTART.md`, `IMPLEMENTATION_LOG.md`: scope, priority, failures, and exact open gates.
- `MANIFEST.json`: SHA-256 hashes of the delivered files other than the manifest itself.

## Numerical limitations

The prototype is floating-point and uses pseudorandom Gaussian numbers. Mathematical probability bounds are not interval-certified executable guarantees. The special-function references use high internal precision but return doubles for reported differences. The transfer comparator has convergence checks, not certified interval enclosures. Wick truncation has no general remainder bound here. Larger-grid ground truth is not independently known.

## Repository status

No GitHub files were modified. This is a local downloadable handoff. The prior analytic-anchoring family is retained, not assumed to prove these results.
