# Reproduce the retained-memory decoder pilot

Start with [FINDINGS.md](FINDINGS.md). This is a local Astra numerical diagnostic, not exact rational/hardware execution. Requires Python 3.12, NumPy and SciPy; the recorded stack is NumPy 2.3.5 / SciPy 1.17.0. No network or source oracle is needed by the learner.

From this directory:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# Source-disabled replay of preserved public records (zero new source calls):
python replay.py runs
python replay.py runs_independent_comparator
# Deterministic math and instrument tests (zero new stochastic source calls):
python test_pilot.py
# Privileged post-hoc scoring only; does not influence acquisition:
python score.py runs
python score.py runs_independent_comparator
python analyze.py
```

`score.py` rewrites derived score/summary files. To keep the delivered byte manifest intact, run in a copied directory. Acquisition will refuse to overwrite an existing run:

```bash
# Fresh diagnostic acquisition with exactly the original seed layout:
python pilot.py --out reproduced_initial --n 128 512 --seeds 17 31 47 73
# Primary ordinary comparator uses independent offset streams:
python pilot.py --out reproduced_independent --n 128 512 \
  --seeds 10017 10031 10047 10073 --algorithms ordinary
```

`learner.py` imports only the known matrix operations and receives `act(i,z)` / `observe(y)`. It cannot access the plant through its interface. `ordinary_comparator.py` receives only actual random-Pauli integers. The driver writes private source state/probability records to separate files solely for later scoring; do not feed those files to a learner.

Source calls are not made by `replay.py`, `score.py`, `analyze.py`, or `test_pilot.py`. Source sampling is done only by `pilot.py`. Timing fields are not expected to reproduce bit-for-bit across runs; recorded actions, outcomes, and numerical iterates should reproduce on the stated stack with the same seeds. The public-record prefix at N128 repeats the N512 prefix within a seed; do not treat those as independent experiments.
