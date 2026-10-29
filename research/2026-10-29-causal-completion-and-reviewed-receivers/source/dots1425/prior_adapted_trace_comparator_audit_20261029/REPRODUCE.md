# Reproduce

From this directory:

```sh
(cd source_snapshot && sha256sum -c SHA256SUMS.txt && sha256sum -c ACTUAL_ENSEMBLE_SHA256SUMS.txt)
python rational_interval_check.py
python independent_checks.py
(cd author_replay && python certify_one_prior.py && cmp INTERVAL_CERTIFICATE.json ../source_snapshot/INTERVAL_CERTIFICATE.json)
(cd author_replay && python check_actual_ensemble.py && cmp ACTUAL_ENSEMBLE_CHECKS.json ../source_snapshot/ACTUAL_ENSEMBLE_CHECKS.json)
(cd author_replay && python explore.py && cmp CHECKS.json ../source_snapshot/CHECKS.json)
sha256sum -c SHA256SUMS.txt
```

Certified arithmetic uses Python 3.12.14's standard library only. Diagnostic and
author replays used numpy 2.3.5, scipy 1.17.0, mpmath 1.3.0. The exact rational
certificate should remain reproducible independently of numerical-library
versions. Floating diagnostic files can differ at harmless final digits across
versions; do not confuse that with failure of the rational certificate.

All writes are inside the audit directory, never the original source packet.
`source_snapshot/SHA256SUMS.txt` is the author's original manifest;
root `SHA256SUMS.txt` binds this independent audit including the receipt.
