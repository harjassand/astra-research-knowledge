# Finite acquisition, metrology and the narrower implemented diagnostic

The [complete visible response](P3_NONLINEAR_SENSOR_20261106_COMPLETE_RETURN.txt) supplies a finite noisy-record construction for a narrower source family: a finite-rate piecewise-deterministic process **without Brownian noise**. Quantitative assumptions include between-jump velocity and rate bounds, lower small-jump intensity per direction, line-field separation/regularity, stationary neighborhood coverage, mixing and initialization bounds, calibrated finite-accuracy readings, clocks and simultaneous multichannel access. Full stationary support does not supply those constants or certify them from a short record.

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

The recovered ending reports parallelogram completion relative to the origin with true output `(0.2,−0.276)` and reconstructed error about `4.59×10^−5`. The inverse solver issued an insufficient-progress warning after reaching residual about `2.78×10^−17`; the warning is retained, and acceptance uses an explicit residual criterion rather than an unqualified solver-success flag. A separate four-dimensional analytic diagnostic recovers all 40 connection coefficients for two disjoint paired blocks; coordinate directions alone lower the rank to 36, exposing four scalar freedoms. Floating numerical errors are not statistical confidence bounds, and these checks are not physical preparation. Their original code/records remain uncollected in the held ZIP and were not replayed here.

## Strong existing methods and priority boundaries

These are the source's comparisons, not a new Capital literature audit. [Belliart Theorem 1.4.3](https://www.numdam.org/item/10.24033/bsmf.2523.pdf) already gives planar three-direction affine rigidity. An equally informed method with the recovered line fields can use that classical web geometry; no computational separation is claimed.

| Existing route | Conditions and consequence retained |
|---|---|
| Geometry-based blind source separation, including [Levin](https://arxiv.org/pdf/cs/0612096) | Statistical-geometry coordinate reconstruction is prior work, not a new idea merely by renaming it |
| Hasan and coauthors' latent-SDE identification | Specified generative assumptions, including the displayed Euler–Maruyama transition model, must be retained. A promised constant nondegenerate latent diffusion metric offers a strong affine-chart route that can make extra jump directions unnecessary |
| [LEAP](https://arxiv.org/pdf/2110.05428) and Schell–Oberhauser nonlinear ICA | Parametric/nonparametric innovation, variability, transition or independent-component-process conditions differ from arbitrary interacting state-dependent jumps; neither silent transfer nor universal superiority is claimed |
| [Sokol–Hansen generator-to-intervention identification](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2891/2565.pdf) | Their Lévy-driven SDE contract already earns the generator-to-intervention step. The new proposed interface identifies the physical affine update as a function of observed coordinates; ordinary kernel composition then supplies the protocol-law deduction |
| Ordinary parametric fitting | Used by the declared numerical front end; no advantage over that incumbent is claimed |

The recent [diffusion-shift paper](https://arxiv.org/abs/2606.28228) was credited, but its full governing text was not retrievable in the source run. No theorem transfer, exclusion or historical-priority claim rests on its metadata. These are bounded source comparisons; no global originality determination is made here.

The complete source retains a broad mathematical conclusion at its declared mechanics contract while leaving a practical total-resource advantage and mission-scale payoff unearned. General acquisition may be enormous, full-state access is substantive, and predicting an operation does not supply an executing actuator or guarantee that an unmodelled environment resumes unchanged. The older corrected known-actuator receiver, scalar-sensor theorem and quantum/preparation/control results keep separate scopes; no physical reduction is inferred.

[Exact-law classification and operation](geometry-and-affine-operation.md) · [Overview](README.md)
