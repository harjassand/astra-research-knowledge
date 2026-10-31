# Observed exact executions

Standard-library Python, raw dictionaries already in memory. Chain coupling 20; all are nonconvex sufficient models. Unit beta,d_min,kappa. No controlled hardware benchmark. Exact results.json is authoritative.

| Full dimension | Raw terms | Exact points | Grid N | Tail T | Largest power bits | Seconds | Full-rate display interval |
|---:|---:|---:|---:|---:|---:|---:|---|
| 3 | 9 | 1793 | 128 | 4096 | 97 | 0.031 | [0.353944347, 0.448585301] |
| 4 | 15 | 2049 | 256 | 64 | 111 | 0.042 | [0.442022507, 0.558245787] |
| 5 | 21 | 1537 | 256 | 16 | 148 | 0.029 | [0.453596963, 0.573333915] |
| 17 | 93 | 1537 | 512 | 2 | 656 | 0.030 | [0.136084571, 0.17218422] |
| 65 | 381 | 3073 | 1024 | 2 | 2880 | 0.150 | [0.000119095808, 0.000150866386] |
| 129 | 765 | 6145 | 2048 | 2 | 6272 | 0.568 | [3.69591944e-09, 4.6707027e-09] |
| 257 | 1533 | 6145 | 2048 | 2 | 12544 | 1.385 | [1.73513954e-18, 2.19850233e-18] |

Every factor is exactly 157/125, with at most 1% further quadrature width. Largest power bits is an explicit proxy, not whole-program peak arithmetic. Producer timings exclude fixture generation/module loading/file output; verifier reruns all math.

The dense graph fixture has physical m=12, 234 expanded terms, acquired axis 5, and all 66 couplings equal 1,000,000. The coupling graph and weights are checked from raw coefficients, not supplied as an oracle.

Author tests pass 2,550 assertions. No independent executable audit is claimed by this table.
