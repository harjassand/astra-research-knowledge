#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
python exact_verify.py
python exact_failure.py
python exact_weak_cut.py
python experiment.py
python lp_enclosure.py
