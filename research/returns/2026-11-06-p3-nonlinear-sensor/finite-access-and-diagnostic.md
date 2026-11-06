# Finite acquisition, metrology and the narrower implemented diagnostic

The [accessible prefix](P3_NONLINEAR_SENSOR_20261106_RETURN.txt) supplies a finite noisy-record construction for a narrower source family: a finite-rate piecewise-deterministic process **without Brownian noise**. Quantitative assumptions include between-jump velocity and rate bounds, lower small-jump intensity per direction, line-field separation/regularity, stationary neighborhood coverage, mixing and initialization bounds, calibrated finite-accuracy readings, clocks and simultaneous multichannel access. Full stationary support does not supply those constants or certify them from a short record.

Two-reading packets yield suitable small increments near spatial grid points. Multi-jump packets are allowed as outliers. A maximum-occupancy clustering argument recovers genuine direction clusters without event labels; it does not require every packet in the full campaign to have at most one event. Paid warm-up and separation handle dependence. Neighbor matching, finite differences, interval linear algebra, integration and finite residual-controlled inversion complete the proposed chain to an answer.

For fixed dimension and fixed positive conditioning/source constants, the displayed conservative packet count is `N=O(η^(−(2n+6)) log[K(m+1)/δ])`, with full constants retained in the report. An illustrative two-dimensional parameter choice gives approximately **`2.78×10²³` packets before readout averaging**. Those are illustrative inputs, not certified constants for the numerical diagnostic, and do not establish a useful engineering design.

Independent mean-zero electronics noise may be reduced by repeated noninvasive readings when that model is provided. Unknown fixed bias cannot be removed that way. ADC resolution/saturation, calibration residual, timing error and jumps during read bursts remain in the budget. Elapsed time includes warm-up, gaps and read bursts: `T≤W+N(Δ+G_gap)+reading allowances`, rather than only `NΔ`. No joule estimate or transfer of earlier quantum fault-tolerance guarantees is supplied.

## Implemented two-dimensional shear example

The declared sensor is `g(x₁,x₂)=(x₁,x₂+0.6x₁²)`, with native directions `e₁,e₂,(1,1)`. The learner receives ADC codes, range/resolution metadata and timing, without latent states, event labels, drift matrix or the shear coefficient. Its front end is a declared quadratic-shear fit using robust mixture regression. That parametric diagnostic feeds the general connection/compiler integration, without implementing the full nonparametric acquisition theorem.

| Saved source-reported diagnostic | Value |
|---|---:|
| Reading times / scalar readings | `1,000,001` / `2,000,002` |
| Estimated shear / absolute error | `0.5999521967` / `4.78×10^−5` |
| Maximum chart error on saved grid | `3.06×10^−5` |
| Multi-event intervals, scoring only | `13` |
| Saturated scalar readings | `0` |

For observed states `a=(−0.6,0.2)` and `b=(0.8,0.1)`, ordinary observation averaging gives `(0.1,0.15)`. The physical midpoint's sensor image is `(0.1,−0.144)`. The reconstructed operation reports `(0.1000000143,−0.1439765751)`, with error about `2.35×10^−5`. These are saved diagnostic claims, without newly run code, delivered raw records or an inference that the general conservative bound certifies this fit.

**The source capture ends at “Parallelogram completion relative to”.** Its continuation, any later comparisons/final qualifications and attachment contents are unavailable and have not been reconstructed. The PDF/ZIP names visible earlier in the prefix do not establish local artifact delivery. The complete source and any additional activity remain pending dispatcher collection after unlock, with existing transfer holds preserved.

[Exact-law classification and operation](geometry-and-affine-operation.md) · [Overview](README.md)
