# Deterministic candidate clock-fluctuation variance

**Rigorous scalar enclosure:** `0.5677211094 <= Sigma² <= 0.5687113183`.
Exact width `<0.000990208879`, acquired in roughly 8–10 seconds locally.

This is `∫(1−J)² dl` along the deterministic origin orbit. It is **not** an
actual-chain CLT, a measured SSA variance, or exact finite-noise Ito variance.

Files: `PROOF.md`, `validated_variance.py`, `VARIANCE_CERTIFICATE.json`,
`verify_saved.py`, `VERIFY_RESULTS.json`, `SOURCE_BINDINGS.json` and
`VARIANCE_FREEZE.json`.

```sh
python inverse_clock_variance_20261101/validated_variance.py \
  --output producer-workspace/candidate_clock_variance.json
python inverse_clock_variance_20261101/verify_saved.py
```

The accepted scalar package `inverse_clearance_clock_20261101` is reused
read-only and its freeze remains unchanged. Python standard library only;
no installations, floating confidence interval, or special-function oracle.
