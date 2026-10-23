# U continuous diffusion: ordered-limit existence and fixed-cycle numerics — 24 October 2026

This selected unit combines two distinct results for one stipulated overdamped diffusion: a producer-derived ordered-limit existence argument and floating finite-volume evidence at a separately fixed waveform. The [selected-source manifest](source_manifest.json) preserves the proof, governing model and solver code, complete cycle report, all six resolution records, the earlier unchanged specification and its source-authored primary gate. No scientific code, proof checker or numerical replay was run during this integration.

## Model and work ports

The medium is one overdamped Brownian coordinate on a circle of length 3, with mobility, temperature and diffusivity set to 1, a maintained nonconservative force `F = ln(3/64)/3`, and potential `U_H(x,h)=H V(x)+v(x)−h f(x)`. The lifted offset satisfies `w(x+3)=w(x)−3F`; the model's full continuous `f(x)` is used in the field work, including in barrier regions. Work on the medium is separated into

- field port: `W_h = −∫ ḣ(t) ∫ f(x)ρ(x,t) dx dt`;
- maintained-force port: `W_F = F ∫ j(x,t) dx dt`, with winding counted on the circle.

Thus a negative field-port work value is force-to-field conversion inside the model. It does not by itself mean net work extraction from both controls.

## Ordered-limit existence result

The newer [static Poisson proof](source/continuum/STATIC_POISSON_EXISTENCE_PROOF.txt) uses exact one-dimensional stationary and Poisson formulas, a Laplace limit with signed-mass domination, and the intended three-state kinetic action. Its reported limiting coefficient is

`κ_H ζ_H → −29239948720000/54023012580627 ≈ −0.5412498734`.

The source concludes that `ζ_H < 0` for all sufficiently large but finite `H`; after fixing such an `H`, sufficiently small finite frequency and amplitude can give negative field-port work while retaining the full continuous field, including barrier work. The choices may depend on `H`; no fixed-`H` parameter window or uniform-in-`H` remainder is supplied. This ordered-limit result does **not** establish the selected `H=12`, amplitude `0.3`, slow frequency `0.01` cycle.

The source also retains the cost of the maintained circulation. In the existence scaling, frequency relative to `κ_H` and amplitude may shrink; the per-cycle force-fuel input grows while field output shrinks. Physical output power and the output/fuel ratio therefore vanish along the stated limiting choices. This is not an efficient-engine or useful-power result.

## Separately fixed H=12 full-cycle report

The [full-cycle report](source/fixed_H12_full_cycle/FULL_CYCLE_RESULTS.md) fixes `H=12` and `h(t)=0.3 cos(0.01 κ_H t)` with period `2,712,579.85698` model time units. It reports six floating finite-volume resolutions, with no parameter search. Across the six records, trapezoidal field work is negative, from `−0.000742762` to `−0.000744608` per cycle. At the finest listed grid, field work is `−0.000744608`, while the maintained-force port supplies `+3.739017`; the combined control work is still a net input of about `+3.738272` per cycle. The replay therefore does not show net work extraction from the two controls.

The report includes the full force, field, heat and entropy ledger. At the finest resolution it records a trapezoid first-law residual of `+5.31×10⁻⁶`, an entropy gap of `7.19×10⁻⁶`, maximum raw mass drift of `6.87×10⁻⁹`, and periodic-start L1 residual below `2.5×10⁻¹¹`; mass renormalization and residuals are retained rather than silently corrected away. Four numerical warm-up cycles from a uniform numerical start were used at each listed resolution. That is not a free physical preparation protocol.

Spatial convergence remains visible in the force/heat ledger: at 4,800 steps the force work changes by about `1.75×10⁻³` between 600 and 1,200 cells, while the reported field-work change is about `4.1×10⁻⁸`. These comparisons do not provide a certified PDE mesh-error enclosure. All six records remain together in [the resolution directory](source/fixed_H12_full_cycle/resolution/) and are individually pinned in the manifest.

## Physical and comparison boundaries

This is a force-to-field conversion result within a specified overdamped model, with no physical observation, device, practical advantage or novelty established. The construction does not build or cost a force source, field controller, phase reference, sensor, or preparation system. Barrier height and maximum restoring force grow with `H`; at high barriers a real fixed-mass, finite-memory bath may not remain overdamped and white as the intrawell time shrinks. A finite-`H` physical claim would need measured friction/bath behavior and a full apparatus/resource ledger.

This is a continuous-diffusion companion to the earlier [discrete kinetic triangle/star construction](../2026-10-24-u-kinetic-binary-port/README.md), not a transfer of its atomic-return test. A continuum well with `f=1` contains many microscopic states; a basin visit is not an exact single-state herald at a protocol boundary. Point-hitting with synchronization and monitoring would be a different continuous stopping protocol. The broader source-clock closed-cycle Gibbs-tilt derivation noted in that prior unit remains unresolved; neither the existence proof nor the H=12 replay supplies it. N713 and its independent-review gate are unchanged.

## Review provenance and status

The supplied review read the model, existence argument and numerical report with prior exposure to the finite construction. It did not replay code or independently certify the proof. This is source-exposed review, not blind proof review. The existence argument, limiting calculation and H=12 numerical results remain producer-reported; independent verification, physical experiment, practical advantage and novelty remain `UNKNOWN`.
