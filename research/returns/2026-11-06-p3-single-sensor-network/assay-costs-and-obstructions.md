# The reported assay, paid acquisition and visible limits

This page preserves what is visible in the [truncated response](P3_SINGLE_SENSOR_NETWORK_20261106_RETURN.txt), rather than claiming a complete package or newly verified simulation.

The fixed comparison is a reciprocal three-node chain and a triangle. The matrices are related by a rotation of the two hidden coordinates that fixes the measured port. Their entire linear port responses agree, as do scalar autocovariances under isotropic driving and the full observed laws under Gaussian driving. The comparator is therefore stronger than a poorly estimated spectrum: even exact covariance or Gaussian-law information cannot distinguish this pair.

Independent local symmetric unit jumps at rate `0.05` per coordinate break that Gaussian equivalence. The assay also has Gaussian drive covariance `0.005I` and independent sensor noise with standard deviation `0.05`. It uses only `cos(12Z)`:

| Hypothesis | Source-reported certified stationary mean interval | Simulated empirical mean |
|---|---|---|
| Chain | `[0.1074986560, 0.1075723515]` | `0.109618` |
| Triangle | `[0.0749928475, 0.0750442588]` | `0.077560` |

Threshold `0.091` has a reported margin above `0.0159`. Directed Decimal arithmetic, analytic quadrature-error and infinite-tail bounds certify the intervals according to the source. The simulation is a diagnostic; the reported success guarantee comes from the analytic campaign budget.

| Resource | Stated assay contract |
|---|---|
| Start | Unknown, `E‖X₀‖≤1`; no equilibrium requirement |
| Scalar readings | `100,000`, nominal spacing `80` model time units |
| Timing error | At most `±1`, deterministic or independent and exogenous |
| Read noise | Fixed standard deviation `0.05` |
| ADC | 21 bits on `[-17,17]`, digitization error below `10^−5` |
| Feature evaluation | Degree-16 cosine polynomial, 80-bit fixed-point integer arithmetic and eight angle doublings; reported error below `10^−9` |
| Decision | At least `0.95` correctness under either of the two specified hypotheses |
| Duration and raw storage | At most `8,000,001` model time units; `2.1×10^6` bits before metadata |
| Hidden access | No states, event times or source labels passed to inference; classifier receives ADC integers |

Both reported simulated records classified correctly without clipping. Neither their arrays, the interval certificate nor the classifier has been delivered or executed here. The implemented binary assay is distinct from a general drift reconstruction run. The long physical campaign is not an engineering resource advantage, and model time units are not converted into laboratory seconds.

The learned drift supports deterministic response deductions: for symmetric `A,B≤−αI` with `‖A−B‖≤ε`, the source gives `‖exp(At)−exp(Bt)‖≤εt exp(−αt)` and a bounded-input zero-start response discrepancy at most `εU/α²`. One matrix-confidence event supports those fixed-drift deductions even for bounded waveforms selected afterwards. Physical inputs must still be registered, delivered and calibrated. Gaussian drive covariance need not be identifiable, so this does not give every stochastic prediction after changing the network or acquire a complete hidden generator.

The visible rare-source lower bound uses the same two fixed networks **started at zero**. Gaussian and measured-port forcing can be coupled identically, even with adaptive linear forcing at that port. Only a hidden-coordinate jump can separate their records. With rate `ρ` on each hidden coordinate, error at most `δ<1/2` under both hypotheses requires

`T ≥ (1/(2ρ)) log(1/(2δ))`.

This permits unlimited computation. Taking `ρ=2^−b` forces exponential physical waiting in the bit length of the rate specification, while the matrices stay fixed, three-dimensional and well conditioned. A stationary specimen carrying informative past disturbances is a different, paid preparation contract; this campaign-start bound does not silently charge it as free or cover every possible intervention model.

The available prefix also exhibits a connected stable reciprocal positive family with invisible mode `(0,1,−1)ᵀ` and a sensor impulse-response row independent of its parameter. It uses this to show why connectivity does not establish observability, even with local non-Gaussian sources. **The captured text ends mid-sentence in this discussion.** Its remaining argument, comparisons, final limitations and any later sections have not been reconstructed.

[Exact-law versus finite access](identifiability-and-finite-access.md) · [Overview](README.md)
