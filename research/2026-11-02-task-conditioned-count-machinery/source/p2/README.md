# Cumulative scientific computation: reproducible conditional pilot

Read `RESEARCH_REPORT.md` for the theorem, strong-baseline context, qualified claims, source assumptions, full results, errors, computational accounting and references.

```bash
python -m pip install -r requirements.txt
python experiments.py
python validation.py
python failure_acquisition.py
python feedback_test.py
python verified_uniformization.py
```

The scripts write `results.json`, `validation_results.json`, `failure_acquisition_results.json`, `feedback_results.json` and `verified_results.json`. No physical observations or unaccounted external oracles are used. The benchmark supplies complete native local rate arrays to the learner and ordinary comparator; network group labels are withheld from the learner.

**Verdict:** A valid conditional task-relevant state reduction, failure-based refinement and rationally certified heterogeneous intervention decision are demonstrated. The generic algorithm itself was researcher-written, not learned autonomously, and best-of-field superiority/historical novelty are not established.
