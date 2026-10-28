# Cost, source scope and replay

Every numerical physical trace retains all states. The six-site angular
calculation uses15625 states at each angle, largest magnetization block1751.
Exact integer/sqrt6 spin-inversion checks justify the factor2 for M>0. The
largest complex block alone occupies49.05MB; several arrays and LAPACK work
coexist. Peak process RSS was not instrumented.

Measured wall times, with BLAS/OMP threads1:

| Work | Seconds |
| --- | ---: |
|64-angle grid,33 distinct full six-site spectra|49.943|
|Exact scalar alias-constant replay|.014|
|Exact physical +/-M component control|.087|
|Uniform P0/equal-time two-vector source, beta1.5 and3|12.139|
|Initial three-fugacity projected preview|9.719|
|Independent odd-sign/triangle control|.220|
|One wider matched P0/equal-time preview,75 trace pairs|33.771|
|Same-information ordinary scalar26-vector comparison|3.990|
|New two-atom signed-moment feasibility test|.188|

Some jobs overlapped; these are their measured wall costs, not a claim about
CPU-seconds. Source reading, proof, failed debug runs, readout and prior
acquisition are additional costs. Kubo source evaluation uses full physical
eigenvectors and operator matrix products; the equal-time comparator could
be cheaper when run alone. Shared eigensystems control information and
accuracy, but do not establish a runtime advantage for P0.

No exact/cyclotomic trace acquisition or certified angle grid was launched.
The separately owned validated-Kubo interface is not claimed as acquiring
the missing ratio. Existing Galerkin, symmetry projection, Kubo response,
MED, BS-CMI and thermal-MPO methods remain ordinary comparators entitled to
the same source information and connected objective. No world-priority,
physical capability or practical matched-advantage claim is made.

Run from the workspace root with the existing read-only runtime, setting
OPENBLAS_NUM_THREADS=1,OMP_NUM_THREADS=1,PYTHONDONTWRITEBYTECODE=1:

    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/angular_spin_projection.py --grid 64
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/verify_alias_constants.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/verify_sector_symmetry.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/audit_odd_moments.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/static_time_message.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/projected_fugacity_preview.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/wider_time_projection.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/scalar_reference_preview.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/nonzero_mode_readout.py
    work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/thermal_spin_projection/code/two_atom_moment_preview.py

The main source/output receipts are in each JSON and MANIFEST.json. Replay
and hashes do not certify the unvalidated physical trace or ratio intervals.
