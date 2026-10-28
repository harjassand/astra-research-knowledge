# Replay

Run at the workspace root with the existing read-only runtime:

    PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/verify_first_increment_fraction.py

This is the small, independent exact-rational consumer. Its expected result
is `PASS_EXACT_FRACTION_FIRST_CONNECTED_THERMAL_INCREMENT`. It reads only
the exact supplied/saved moment arrays, uses simple rational trial vectors,
and checks the conservative first connected increment without producer code,
an eigensolver, mpmath or Chebyshev.

The richer outward interval readout is:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/scalar_loop_certificate.py --betas 3/4 3/2 3 6

It preserves the precise first connected interval and broad failed next-rung
intervals. The raw producer, approximately432s for the two full six-cycle
arrays on this host, is:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/acquire_cycle_moments.py --n 6 --degree 192

The endpoint-spin acquisition is separate and is not needed for the
successful first increment:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/acquire_end_spin_moments.py --degree 192

Finite analytic/construction controls, separate from the completed independent
agent review, are replayed by:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/verify_source_controls.py

The A5 next-depth numerical diagnostic is:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/code/a5_preview.py

This last command is a feasibility preview, not a certified input acquisition.
Its beta3 count fails in one triplet list; no cyclotomic producer was run.

The source arrays and runtime pre-exist in the parent-authorized workspace.
`sources/ACCEPTED_INPUTS.json` freezes input provenance and local snapshots.
No files outside this owned lane were written. The input and output statuses
are scientific-scope claims, not a claim that replay or hashes prove novelty,
physical usefulness or the uniform gap.
