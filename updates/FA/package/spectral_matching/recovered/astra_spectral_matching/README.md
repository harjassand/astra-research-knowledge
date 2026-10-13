# ASTRA Frontier: Hamiltonian-referenced spectral matching

Read `RESEARCH_NOTE.md` first. This is a candidate research packet, **not an established scientific breakthrough**.

## Files

- `RESEARCH_NOTE.md`: construction, exact proofs, scope, prior art, physical costs and failed unrestricted-control claim.
- `checks.py`: exact rational assertions and finite interacting-ring quantum/kinetic diagnostics.
- `additional_checks.py`: finite-pulse cutoff and product-dimer nonuniformity diagnostics.
- `results.json`, `additional_results.json`: executed outputs.
- `run.log`, `additional_run.log`: execution logs.
- `SCOPE.json`: machine-readable evidence and unresolved requirements.
- `MANIFEST.json`: SHA-256 hashes of packet contents.

## Reproduce

Python 3 with NumPy and SciPy is required. From this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python checks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python additional_checks.py
```

The rational assertions use Python's standard-library `fractions.Fraction`. Other numerical results use floating point and are not interval-certified. The scripts do not access the internet or quantum hardware. The product-dimer calculation evaluates an exact scalar formula; it does not simulate a million-dimer Hilbert space.

## Scope

The 97% theorem concerns the weak-hopping kinetic model with fixed coherent detunings, common baseline linewidth, and a specified physical diagonal-operator access contract. A volume-uniform finite-hopping current theorem is open. Coherent cancellation, when physically available and allowed, defeats an unrestricted advantage claim. Historical novelty and independent correctness have not been established. No repository update or experimental run was performed.
