# Reproduce

From this audit directory:

```sh
(cd source_snapshot && sha256sum -c SHA256SUMS.txt)
python independent_checks.py
(cd author_replay && python check_uniform.py && cmp UNIFORM_CHECKS.json ../source_snapshot/UNIFORM_CHECKS.json)
sha256sum -c SHA256SUMS.txt
```

Environment: Python 3.12.14, numpy 2.3.5. All source copies and audit files are
hash-bound. The independent script imports no author code. Exact Fraction checks
and explicit boundary witnesses accompany numerical diagnostics. The theorem is
received analytically; sampled tests alone would not prove the uniform claims.

Original files are never overwritten. Cross-version floating output can differ
at final digits; inspect analytic assertions and tolerances instead of interpreting
such differences as a theorem failure.
