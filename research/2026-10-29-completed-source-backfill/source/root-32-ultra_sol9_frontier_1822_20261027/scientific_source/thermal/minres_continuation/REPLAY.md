# Replay

From the workspace root, using the existing read-only runtime:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/minres_continuation/code/minimize_residual.py

This runs only the bounded numerical preview and writes only this continuation.
It regenerates G/H/M2, scans the same prescribed-shift interval and preserves
all candidates and conditioning diagnostics. It does not acquire exact A5 data.

The exact finite-form check is:

    PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol9_frontier_20261028/thermal/minres_continuation/code/verify_dyadic_span.py

Its expected status is
`PASS_EXACT_RESTRICTION_FOR_STORED_NUMERICAL_FORMS_ONLY`.
This is not a physical-source certificate. Its input hash freezes the precise
NPZ matrices treated as dyadic forms.
