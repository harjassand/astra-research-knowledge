# Offline replay

Run with the provisioned read-only scientific runtime:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 producer-workspace/python -B producer-workspace/replay_all.py
```

The completed seven-check replay passed on October28. It took 1.91545 seconds
inside the script, 2.17 seconds wall time under `/usr/bin/time -l`, with
maximum resident set size 141950976 bytes and peak memory footprint 125108824
bytes. BLAS used one thread. The replay needs no network or solver license
and writes only the owned `gibbs_transfer_bridge/results/` files.

The checks, in dependency order, are:

1. Exact source-unitary/Marshall gauge and source generator-word span.
2. Symbolic nine-term quadratic-gate reconstruction and finite rank replay.
3. Positive periodic transfer, source-Q comparison, independent physical gates.
4. Actual-cut support proposals and explicitly noncertified scaled SVD data.
5. Complete exact rational support replay, fooling sets, inverse-minor bounds.
6. Separate exact-exponential 25-factor formula and physical trace orientation.
7. Exact AKLT finite-ring transfer/projectors, independent physical vector,
   rational logarithm bound, cold Gibbs physical-product-frame exclusion.

`results/REPLAY.json` records each completed check. The peer source module and
NPZ are frozen snapshots with checked SHA256, so replay does not depend on a
later edit in the peer's active directory. The inspected public SSE magnet
implementation is pinned to commit 0ee4bb3e78ad90306d594978e0ad405edebe8961;
its exact Git blob is also checked offline. That Julia implementation was
not executed here.

The replay regenerates result files, including timings and the diagnostic
proposal's hash. `MANIFEST.json` records the final supplied bytes; a replay
will naturally alter timing fields. Hashes establish provenance, not the
correctness or novelty of the mathematics. This is an internal construction
replay, not an independent full audit or a cold trace/purity certificate.

All 78 entries in the earlier frozen corpus-first manifest, totaling 14591755
bytes, were checked against their original hashes after this extension and
remain unchanged. The new extension has its own manifest.
