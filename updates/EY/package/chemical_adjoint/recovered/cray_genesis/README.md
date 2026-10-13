# CRAY GENESIS research packet

Start with `research_note.md` for the mathematical contract, proofs, prior-art boundaries, resource accounting and proposed falsification experiment.

`verify.py` reproduces the checks and writes `results.json`:

```sh
python -m pip install numpy scipy sympy
python verify.py --output results.json
```

`run_log.txt` is the output from the executed run. The numeric examples are synthetic and are not evidence of a real-world speedup. No physical experiment, historical-priority clearance or independent proof review was performed.

Executed environment: Python 3, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0.
