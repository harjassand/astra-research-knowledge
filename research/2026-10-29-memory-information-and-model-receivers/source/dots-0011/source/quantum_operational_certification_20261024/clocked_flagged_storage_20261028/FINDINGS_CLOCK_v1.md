# Clocked storage survival and failure regimes

28 October2026. Deterministic numerical comparison, independent review pending. These are dimensionless closed-model cases, not hardware lifetime claims. All T=32; same elapsed time within each comparison. Coherent control angle eta=.001 throughout.

| Case | EC time | Background integral | Encoded infidelity | Best single-site full-CPTP final-decoder oracle infidelity | Lower encoded infidelity? |
|---|---:|---:|---:|---:|:---:|
| measure_1.0_v1.json | 165 | 0.0165 | 0.1028175 | 0.3132361 | True |
| measure_16.0_v1.json | 345 | 0.0345 | 0.2373262 | 0.4277565 | True |
| measure_4.0_v1.json | 201 | 0.0201 | 0.1276736 | 0.3411017 | True |
| rate_0.001_v1.json | 201 | 0.001 | 0.0197766 | 0.1557633 | True |
| rate_0.003_v1.json | 201 | 0.003 | 0.0274105 | 0.1800909 | True |
| rate_0.01_v1.json | 201 | 0.01 | 0.0617897 | 0.2553199 | True |
| rate_0.03_v1.json | 201 | 0.03 | 0.2033554 | 0.4048167 | True |
| rate_0.1_v1.json | 201 | 0.1 | 0.6316649 | 0.5562844 | False |
| rate_0.3_v1.json | 201 | 0.3 | 0.7498598 | 0.5617054 | False |
| rate_1.0_v1.json | 201 | 1 | 0.7500000 | 0.5493609 | False |
| zero_clock_v1.json | 201 | 0 | 0.0163654 | 0.1430801 | True |

The comparator is the optimum **terminal qubit CPTP decoder for each specified unencoded endpoint dynamics**, allowed source information as a diagnostic ceiling. It does not optimize all intermediate unencoded controls or extra quantum resources. The code spends five source calls/seven physical qubits rather than one, and the synchronous fixed-window schedule is not optimized. Ordinary redundancy is expected to help; this is not a novel-code superiority claim.

At default timing, the code beats even this source-informed endpoint-decoder comparison for background integrals up to .03 in the tested grid, but loses at .1 and above. This is a tested-regime boundary, not a proved sharp threshold. Measurement-duration cases1,4,16 hold the background RATE fixed at.0001/unit while time increases165→201→345; they must not be mistaken for a fixed-total-noise comparison.

The zero-background whole-operator check and all source files are preserved separately. See GOVERNING_CLOCK_MODEL_v1.md for interval ordering, live ancillas, rates and unpaid interfaces; endpoint learning budgets are governed by the separate endpoint-oracle acquisition source, not by this oracle table.
