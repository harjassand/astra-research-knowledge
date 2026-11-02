# Astra independent rare-event intervention research bundle

Starting fixed Astra corpus: `5489b118101275c81500d823361592c670ec77bb`.

Read **`RESEARCH_NOTE.md`** for the exact theorem, assumptions, math proofs,
predecessors, numerical evidence, strongest conventional comparator, source
readback and unpaid physical/novelty obligations. No peer drafts were used.

## Executable parts

- `exact_binary_twist.py` + `_results.json`: Python standard-library only; exact rational full enumeration of 4096 paths; no randomness or numerical approximation.
- `dominated_twist.py` + `_results.json`: adaptive conditional Gaussian noise, passive and constant Gaussian shift baselines; 200-step, 50k-trajectory tests (NumPy/SciPy).
- `decision_test.py` + `decision_results.json`: two scientific intervention candidates under the same partial-physics upper bound; familywise 95% risk and task-threshold decisions (NumPy/SciPy).
- `rare_event_bridge.py` + `rare_event_results.json`: conventional bounded Gaussian-shift likelihood as a simpler first-passage baseline (NumPy/SciPy).
- `run_experiment.py` + `results.json` + `diagnostics.npz`: earlier unrestricted log-partition optimality upper bound and matched-data model-based DP controls; a strong conventional fit/DP controller wins here.

## Minimal replay

```sh
python exact_binary_twist.py
python dominated_twist.py
python decision_test.py
```

All test systems are numerical; no physical experiments have been carried out.
Running the code does not independently validate a real noise port, global drift
bound, unchanged hidden response, or finite precision of the actual hardware.
