# Replay and provenance

Run from the workspace root. The independent model, Markov construction,
fraction-free solver, structural controls and phase-type test use only the
Python standard library. The comparison/enclosure adapters additionally load
the archived producer code, which imports mpmath. No network or paid service is
required for replay.

The literal model and exact outputs were acquired independently before the
producer comparison. The two adapters are explicitly dependent checks; they
do not make the literal construction dependent on the producer.

## Independent literal acquisitions

```sh
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/literal_markov.py --n 2 --lambda 999/1000
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/literal_markov.py --n 4 --lambda 999/1000
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/literal_markov.py --n 4 --lambda 99999/100000
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/literal_markov.py --n 4 --lambda 1
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/structural_controls.py
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/phase_type_waiting.py
```

`results/chain_*.json` contains the exact sparse Q/R matrices, all transient
states, start index and source rewards. `results/literal_*.json` contains all
output probabilities and joint first moments as fractions. Each system is
checked by exact multiplication. The additional PGF query is z=lambda^2.
Replaying overwrites only this directory's output receipts and their timings.

## Comparison against the archived producer version

```sh
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python - <<'PY'
from pathlib import Path
from fractions import Fraction as F
import sys
root=Path('work/sol10_constructive_frontier_20261028/factory_independent')
sys.path.insert(0,str(root/'code'))
from compare_producer import run
for n,lam in ((2,F(999,1000)),(4,F(999,1000)),(4,F(99999,100000)),(4,F(1))):
    run(n,lam)
PY
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/factory_independent/code/interval_crosscheck.py
```

The adapters use `inputs/reviewed_producer/` rather than mutable sibling files.
Copies preserve the bytes reviewed from `independent_capability/`:

* waiting_loss_factory.py:
  bf36bd0477af36d11bcdafa0ccbf7f922c2d4d7410350fc45a473be9c64447b5
* dyadic_interval.py:
  00e7f9fb5ace2eab98b2d81b6c5fb24f32c2a02fc7648af634ff1dee7a275add
* certify_waiting_loss.py:
  4c6ea8a94f40db66d1f1211d6c1a0cf5d5b6b2fc94250ad1f2234df96a07810f
* WAITING_LOSS_PROOF.md:
  9584aac670fa0729f2088d5b0c56c2712b0a81f3ff9eaaafce7845ee7589726a

These hashes establish the reviewed version, not mathematical correctness.
That correctness is supplied at its stated scope by PROOF.md and the independent
exact comparisons. Larger sibling producer outputs are not copied or accepted
as independently checked results here.

`initial_timing_observations.json` preserves the first comparison receipts
underlying the cost table. The adapters were replayed once after redirecting
them to byte-identical archived inputs; all components still passed. Timing
differences do not change the exact numerical claims.

## Primary-source retrieval scope

The free web reader was used for primary 2019, 2021 and 2025 comparator sources
linked in COMPARATOR_AND_COSTS.md. No credit-billed Firecrawl call, paid compute,
physical acquisition, external outreach or integration was performed. No
thermal artifacts were changed by this continuation. Its final manifest covers
only this owned independent-factory directory and excludes the manifest itself.
