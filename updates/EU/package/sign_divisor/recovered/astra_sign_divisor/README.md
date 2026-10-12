# ASTRA sign-divisor research packet

Date: 13 October 2026.

- `RESEARCH_NOTE.md`: complete statements, proofs, failure examples, limitations, provenance, and the initial quantum-gluing appendix.
- `verify.py`: deterministic finite algebraic diagnostics and clearly labelled floating-point diagnostics.
- `checks.json`: actual diagnostic output from this investigation.
- `MANIFEST.json`: SHA-256 hashes of the three files above and this README.

Run with Python 3.10 or later and the `numpy` and `sympy` packages:

```sh
python verify.py --output rerun_checks.json
```

The script is a finite diagnostic, not a formal proof or an independent validation. Historical novelty and external mathematical correctness remain unestablished. No unrestricted computational-complexity separation or general quantum-marginal solution is claimed.
