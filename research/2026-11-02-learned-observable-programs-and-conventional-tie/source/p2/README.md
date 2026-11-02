# Learned observable calculus: complete construction and adverse comparator

**See `RESEARCH_REPORT.md` for definitions, acquisition, proofs, tests, full source/compute bills and the strong-baseline negative result.** This package contains real executable research, not just an outline. Models/experiments are synthetic; learned code is not a novel confirmed scientific algorithm.

## Core files

- `source_device.py`: hidden physical experiment simulator for the first two modes. **Never imported by `synthesize.py` or `independent_verify.py`.**
- `synthesize.py`: finite Poisson-count acquisition, restricted observable code search, local rewrite discovery and exact-rational local uncertainty calculation.
- `train.py`: first freezing operation; outputs `frozen_programs.json` and `frozen_measurements.json`.
- `execute.py`: deploys frozen original-mode programs on new lattice sizes/open-loop controls; never reads hidden source rates.
- `reference.py`: small-system full native CTMC reference, evaluation only.
- `evaluate.py`: six frozen first-stage heldouts, recorded in `heldout_results.json`.
- `signed_extension.py`: learns a signed additional rule from eight additional physical-mode experiments while retaining old programs.
- `signed_execute.py`: bounded signed/cemetery trajectory interpreter.
- `signed_reference.py`: field-mode exact small-system truth; evaluation only.
- `signed_evaluate.py`: six separately predeclared field-mode heldouts.
- `independent_verify.py`: independent rational residual, kill-rate, and drift checks with no hidden-rate inspection.
- `strong_baseline.py` and `matched_comparison.py`: equally informed conventional Fourier–Walsh baseline; **this baseline matches or improves the error and is computationally cheaper to compile**.
- `assumption_attack.py`: identical-admitted-data fourth-neighbour counterexample against unwarranted generalization.

## Reproduce

```
python train.py
python signed_extension.py
python independent_verify.py
python evaluate.py
python signed_evaluate.py
python matched_comparison.py
python assumption_attack.py
```

The experiment fixes thresholds and heldouts in `heldout_contract.json` and `signed_heldout_contract.json`; the program hashes are pinned inside the evaluator scripts and signed extension. The previous study remains separately at `producer-workspace/cumulative_machinery`.

## Scientific status

1. Acquired observable rule programs and finite-data local/global conditional error guarantees: **completed**.
2. Exact-rational recheck of stored source uncertainty and rule identity: **completed**.
3. Frozen heldout interventions and larger task executions: **completed on simulated sources**.
4. Best-of-applicable ordinary comparator: **full-table symbolic Fourier–Walsh matches/improves**.
5. Novel, general, civilisation-scale cumulative-learning mechanism: **not established**.
