# Reproduction

```sh
python independent_checks.py
```

Python3 and NumPy suffice. This writes `INDEPENDENT_CHECKS.json` and does not edit the received source. Pauli and classical-grouping optimum values are derived analytically in `REVIEW.md`; random decoder tests are competitor-witness tests only. No SDP or unknown-channel adjoint/inverse oracle is used.
