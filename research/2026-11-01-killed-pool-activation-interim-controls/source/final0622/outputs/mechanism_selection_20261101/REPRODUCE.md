# Reproduce the constructive controls

Run from the existing task directory. No installation, network, worker, hardware
or outside output directory is needed. The existing interpreter contains NumPy,
SciPy and mpmath; all newly generated outputs stay under this task's `outputs/`.
The exact MPS code uses Python big integers inside NumPy object arrays.

```zsh
cd producer-workspace/continue-astra-s-civilisation-changing-discovery
astra_math_python=producer-workspace/python

env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 "$astra_math_python" work/mechanism_selection_20261101/cooperative_pool_controls.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 "$astra_math_python" work/mechanism_selection_20261101/cooperative_exit_controls.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 "$astra_math_python" work/mechanism_selection_20261101/cooperative_higher_order_pool_controls.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 "$astra_math_python" work/mechanism_selection_20261101/cooperative_higher_order_exit_controls.py
env PYTHONDONTWRITEBYTECODE=1 python3 work/mechanism_selection_20261101/cooperative_scope_controls.py
env PYTHONDONTWRITEBYTECODE=1 python3 work/mechanism_selection_20261101/cooperative_higher_order_scope_controls.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 "$astra_math_python" work/mechanism_selection_20261101/exact_stabilizer_controls.py
env PYTHONDONTWRITEBYTECODE=1 python3 work/mechanism_selection_20261101/verify_artifacts.py
```

The first two scripts retain the degree-four overlap and degree-five two-A
comparisons, including the minimum-three-A failed uniform-ratio control. The
next two test the further degree-six/three-A witness. Full return scripts keep
overflow separate and use mixed-precision refinement only as a numerical solver;
the actual final residuals use exact integer rates and outward intervals. A
positive embedded-step potential supplies an a posteriori solution-error bound.
They never close or reflect the truncated B boundary.

The exact stabilizer controls include independent dense Pauli action, the
displayed-prefix counterexample, 16/32/64-qubit bond-two cases, fixed-width-input
promotion, zero-state rejection and the extremely rare exact-support case.
`exact_stabilizer.py` also exposes `ExactPauliMPS(tensors).extract()` and
`ZMatrix.make(real_integer_matrix, imaginary_integer_matrix)` for supplied inputs.
Clear one common rational denominator per site before constructing the tensors;
the common scaling leaves the stabilizers unchanged.

The archived `cooperative_exit_float_only_failed.py` is intentionally NOT part
of the passing entry points. It documents the failed double-precision attempt.
The original `killed_pool_controls.py` and `residual_exit_controls.py` reproduce
the SUBSUMED pure-family reconstruction; their earlier bound results remain.

Scientific proofs are the Markdown arguments, not the finite test matrices or
hash check. A successful verification reports implementation/transport scope
only, while keeping novelty, independent review and mission status separate.
