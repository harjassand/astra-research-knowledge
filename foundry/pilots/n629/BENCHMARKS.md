# Measured benchmarks

Final run: `results/run-20261010-v4/`. Apple M4, 16 GiB, macOS, Python 3.14.3.

Median algorithm milliseconds, including setup plus 16 draws, across three replicates. Module loading is excluded from these timers and included in the per-process receipts. The RSS columns are median process high-water MiB, including the interpreter. Skipped brute force has no algorithm timing.

| Input | m,w | Matrix bits / JSON bytes | Exact count | FPT ms | Brute ms | Rejection ms | FPT / brute / rejection RSS MiB |
|---|---|---|---:|---:|---:|---:|---|
| disjoint_m6_w2 | 6,2 | 36 / 44 | 1,849 | 3.986 | 8.594 | 0.135 | 20.42 / 20.08 / 19.92 |
| disjoint_m8_w2 | 8,2 | 64 / 53 | 44,521 | 7.917 | 241.378 | 0.118 | 20.48 / 23.20 / 19.97 |
| disjoint_m10_w2 | 10,2 | 100 / 64 | 866,761 | 8.863 | 4500.105 | 0.168 | 20.50 / 58.28 / 19.95 |
| coordinate_m5_w5 | 5,5 | 25 / 46 | 1 | 530.214 | 1.398 | 25.337 | 21.17 / 19.83 / 19.88 |
| common_kernel_m8_w4 | 8,4 | 32 / 40 | 256 | 183.930 | 77.116 | 6.832 | 20.50 / 19.88 / 19.83 |
| large_m30_w3 | 30,3 | 900 / 234 | 1,142,827,901,003,938,843 | 321.202 | skipped | 0.192 | 20.53 / 19.92 / 19.88 |
| repeated_m4_w1 | 4,1 | 16 / 34 | 211 | 0.540 | 0.384 | 0.072 | 20.47 / 19.86 / 20.00 |
| repeated_m4_w3 | 4,3 | 48 / 62 | 211 | 1.329 | 1.990 | 0.115 | 20.48 / 19.86 / 19.94 |
| repeated_m4_w5 | 4,5 | 80 / 90 | 211 | 14.327 | 1.496 | 0.157 | 20.48 / 19.91 / 19.88 |
| repeated_m4_w7 | 4,7 | 112 / 118 | 211 | 429.515 | 1.969 | 0.197 | 20.45 / 19.91 / 19.94 |

Final execution: 94 child processes; 26.965 CPU seconds; 32.958 summed child wall seconds; 97.45 MiB maximum child RSS. There were zero failed or timed-out final children, and three deliberately skipped brute-force replicates at m=30.

The earlier complete run is also retained: 58.557 CPU seconds and 75.005 summed child wall seconds. Combined complete runs consumed 85.522 measured child CPU seconds and 107.963 child wall seconds. Preliminary checks, failed preflights, preparation, monitoring and interactive work were not fully resource-metered; their usage is unknown, not zero.

Rejection proposal counts and exact input/draw records are in `benchmarks.json`. All requested rejection outputs completed before the one-million-proposal limit. Every method validates outputs with the same independent predicate. FPT and brute force additionally provide exact counts; rejection supplies draws only.

FPT improves substantially over the admitted pair enumeration for large m at fixed w. Rejection is faster on these sampling workloads. Width-sensitive cancellation and duplicate-block expansion remain visible. These are three local replicates on a shared machine, with no system-isolation or universal complexity inference. The brute predicate is deliberately simple Python, so these timings are not comparisons with an optimized exhaustive engine.
