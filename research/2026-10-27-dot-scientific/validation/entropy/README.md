# Entropy replay at intake

Twenty-four selected supplied symbolic, rational or finite-matrix checkers
passed in a disposable copy. Their regenerated frozen JSON outputs matched
exactly. Original scientific bytes were not edited or executed in place.
The detailed commands' script names, source/output hashes and per-check scope
are in `report.json`; individual logs are retained beside it.

The producer's frozen `nonflat_two_mode_white_reset_independent_replay.py`
wrapper could not run unchanged here because it hardcodes a producer scratch
directory. This is recorded as `WRAPPER_PATH_GAP`, not a scientific PASS. Its
two underlying checkers were run directly from the disposable copy: the exact
coefficient certificate passed, as did the actual complex6x6 clock/output and
2x2 marginal ratio checker. No historical path or source hash was silently
rewritten.

The portable replay helper runs those twenty-four underlying checks directly:

```sh
python3 research/2026-10-27-dot-scientific/validation/replay_entropy.py \
  --output /tmp/dot-entropy-replay-new
```

The output directory must be new. Dependencies are the retained source files
and the Python packages imported by those exact programs, principally SymPy
and NumPy. The helper fixes `OPENBLAS_NUM_THREADS=1`; it copies sources before
running any checker that writes its adjacent report.

Finite identity/certificate replay is separate from the full analytic proof
and its named completed independent audit. It does not acquire a physical
channel, operational receiver, practical advantage or priority. In particular,
the source-weighted cubic and global-bound variance-payment checks remain
independently unreceived at the frozen cutoff despite their exact PASS outputs.
