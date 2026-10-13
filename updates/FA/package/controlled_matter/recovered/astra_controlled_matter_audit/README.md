# ASTRA controlled-matter audit

This packet preserves the 13 October 2026 continuation of the lattice-loop ionic-transport hypothesis.

Start with `REPORT.md`. `SOURCES.json` contains primary-source provenance and scope. `check_audit.py` and `checks.json` reproduce algebraic diagnostics only.

Run from this directory:

```sh
python check_audit.py --output checks.json
```

Dependencies: Python 3.10 or later, NumPy, SciPy. No network access is required to run the checks.

No DFT/MD or experimental data were generated. No material-control matrix was acquired. No exceptional manufacturing capability or historical novelty is claimed. No repository update was performed.
