#!/bin/bash
set -euo pipefail
task_root=$(cd -- "$(dirname -- "$0")/.." && pwd)
cd "$task_root"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
export NUMBA_CACHE_DIR="$task_root/tmp/numba" XDG_CACHE_HOME="$task_root/tmp/cache" MPLCONFIGDIR="$task_root/tmp/matplotlib"
task_py="$task_root/../../empirical_operation_invention/.venv/bin/python"
"$task_py" analysis/probe_calibration.py
"$task_py" analysis/rotated_multislice.py --kind oblique --prefix oblique_768_analytic_finite_dz1
"$task_py" analysis/rotated_multislice.py --kind onaxis --prefix onaxis_768_analytic_finite_dz1
"$task_py" analysis/rotated_multislice.py --kind oblique --prefix oblique_768_vacuum_dz1 --vacuum
"$task_py" analysis/rotated_multislice.py --kind oblique --prefix oblique_896_large_finite_dz1 --gpts 896 --box 112 --halfwidth 32 --fixed-target-depth 69.39539494934884
"$task_py" analysis/rotated_multislice.py --kind oblique --prefix oblique_1024_finite_dz05 --gpts 1024 --dz .5 --fixed-target-depth 69.39539494934884
"$task_py" analysis/analytic_checks.py
"$task_py" analysis/kernel_checks.py
"$task_py" analysis/summarize_fields.py
