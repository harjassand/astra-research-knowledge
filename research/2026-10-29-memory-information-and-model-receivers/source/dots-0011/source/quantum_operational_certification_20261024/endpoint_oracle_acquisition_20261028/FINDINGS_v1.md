# Endpoint baseline findings v1

28 October2026. Author-completed, independent review pending. Full-CPTP oracle is source-informed; sampled-fit values below are true simulator scores, not confidence certificates.

## Correction to a weak comparator

AtT32, the original fixed-per-round-control unencoded baseline has infidelity0.382–0.910. Allowing its optimal terminal CPTP qubit decoder reduces this to0.14308–0.21171. The oracle must be retained in any superiority comparison.

## Standalone direct endpoint learning, no inherited inverse

Each experiment separately allocates its stated TOTAL native-calibration budget across all5sites. AtT32,20480uses gives128endpointshots/site;102400gives640/site. No per-round learned inverse or prior inverse-training data is granted.

| Background integral per EC window | Native-use budget | T32 scored fit infidelity range across5sites | T32 source-informed oracle range |
|---:|---:|---:|---:|
| 0 | 20480 | 0.166688–0.254676 | 0.143835–0.212081 |
| 0 | 102400 | 0.169597–0.220353 | 0.143835–0.212081 |
| 0.01 | 20480 | 0.263605–0.327918 | 0.260283–0.315697 |
| 0.01 | 102400 | 0.270541–0.317377 | 0.260283–0.315697 |
| 0.1 | 20480 | 0.707227–0.766047 | 0.668469–0.685581 |
| 0.1 | 102400 | 0.681764–0.764280 | 0.668469–0.685581 |

The ranges are descriptive, not an operational best-site selection. Finite sampling need not improve monotonically between two independent budget experiments; no best-seed selection was used. At stronger background the endpoint signal is weak, and a fitted rotation can perform poorly even when the source-informed oracle remains better.

The first endpoint pilot retained an inherited per-round inverse; its endpointbudget is ADDITIONAL, not a standalone total-budget comparison. Those files are preserved verbatim and their correction is documented in ORACLE_AND_BUDGET_SCOPE_v2.md and endpoint_clock_costs_v1.json.

Clock charges: each new endpointshot atT32 uses32 native calls and32×203=6496reference time units before endpoint prep/readout and terminalpulse. With5sites parallel, the20480use calibration experiment takes128×6496=831488reference units for channel evolution; the102400use experiment takes4157440. Aggregate channel-time is five times those figures. Prior local calibration probes used the native channel ONCE, withoutEC or acquiredinverse; their elapsed perprobe is separate, not203units.
