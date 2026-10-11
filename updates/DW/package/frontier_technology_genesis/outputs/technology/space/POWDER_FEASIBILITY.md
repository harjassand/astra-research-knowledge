# Acquisition feasibility for a conditional closed-void powder certificate

Status: analytic engineering constraints and a falsifiable prototype protocol. No instrument, accuracy, throughput, tail bound, cost advantage, or working device has been demonstrated here. The model is reproducible with `python3 work/genesis_space/powder_model.py`; it writes `powder_results.json` beside the script. Source literature was checked on 2026-10-12. All numerical instrument parameters below are design assumptions.

**Decision:** the polarization force is large enough to measure on a single 30 µm aluminum grain. The combined claim “0.2% per-particle response, 1 kg/h, useful one-sided 1% closed-void certificate” is not established and has several independent missing interfaces. The statistical confidence specification alone tightens the useful random precision to 0.115% in the ideal material model, or 0.046% under the threshold supplied by the root/materials analysis. Optical centroid accuracy, rotational dynamics, trace acquisition, charge cancellation, parallel feeding and sorting remain unclosed. A milligram-scale controlled experiment is warranted only after a realizable response observable replaces or restricts the analytically blocked universal passive force ensemble.

The root/materials workers report an internal counterexample: a positive field ensemble centered at the center of mass cannot universally deliver the proposed force trace for conductors with off-center closed spherical cavities. This report does not independently re-prove that result or assume it away. It budgets a *conditional interface that actually returns* `R = Tr(alpha)/m`, whether obtained by a different observable, active orientation reconstruction, or an explicitly restricted particle class. The engineering estimates cannot establish that interface.

## 1. Operational target and demonstrated comparators

Assuming the trace lower bound and its hypotheses are valid,

`Tr(alpha) >= 9 epsilon_0 V_filled`, `m = rho (1-phi) V_filled`,

give `R >= R0/(1-phi)`, where `R0 = 9 epsilon_0/rho`. A conservative **upper** measurement bound `R_U` would certify

`phi <= 1 - R0/R_U`.

Low measured response is useful only if an upper bound covers trace acquisition, finite particle size, charge, field calibration, optical tracking, material density/composition, particle interactions, and statistical error. A response higher than the cutoff returns UNKNOWN; it does not identify porosity, because nonsphericity or other admitted effects can raise the trace.

The closest source anchors found in this focused search are:

| Source-reported operation | Source-reported evidence | Scope of comparison |
|---|---|---|
| Rose/MIT, vacuum free-fall dielectrophoretic separation | A separator was designed and constructed; the report explicitly discusses alternating fields to suppress charge forces. | Vacuum DEP and field-sign charge suppression are established principles; they are not the proposed novelty. No 0.2% precision or industrial particle count is reported in the accessed record. [NASA report, 1986](https://ntrs.nasa.gov/citations/19890004301) |
| Blakemore et al., individual levitated silica sphere mass/density | About 4.7 µm diameter; 1.8% systematic mass uncertainty; three recovered spheres imaged by electron microscopy; inferred density 1.55 ± 0.08 g/cm³. | A serious individual-particle force/mass experiment, with substantially different material, trapping and throughput. [Phys. Rev. Applied 12, 024037, 2019](https://doi.org/10.1103/PhysRevApplied.12.024037) |
| Metal powder digital radiography | Numerical and experimental pore detection around 3–4.4 µm for the selected X-ray setup. | Direct internal-pore detection; no matched kilogram-per-hour certificate established here. [Metals 10, 1634, 2020](https://www.mdpi.com/2075-4701/10/12/1634) |
| Calibrated XCT of metal powder | Approximately 2 µm voxels and 10–30 µm pores in particles up to 100 µm; four powder sample types. | Offline internal-pore metrology; reported bulk porosity and an indirect volume-accuracy analysis, not a per-particle 0.2% response comparator. [Measurement: Sensors, 2021](https://doi.org/10.1016/j.measen.2021.100110) |
| Bjerregaard et al., segmentation of powder radiographs | Fastest reported processing 0.014 s/particle with F1 0.78; most accurate 0.291 s with F1 0.87. | This is image segmentation of acquired radiographs, not complete acquisition or a physical certificate. [2024 primary preprint](https://arxiv.org/abs/2408.02427) |

This is a focused set of primary anchors, not an exhaustive priority search. No measured competitor in this set supplies the proposed universal trace certificate. Conversely, lack of a matched comparator is not evidence that its acquisition is feasible.

## 2. Single-grain signal and position metrology

Take diameter 30 µm, homogeneous aluminum matrix density `rho=2700 kg/m³`, `E_rms=10^6 V/m`, transverse gradient `g_rms=10^9 V/m²`, and effective field scale `L=E/g=1 mm`. For a conducting sphere:

`V=4 pi a³/3 = 1.4137e-14 m³`, `m=3.8170e-11 kg`,

`alpha_axis=4 pi epsilon_0 a³ = 3.7551e-25 SI`,

`F=alpha_axis E g = 3.7551e-10 N`, `A=F/m=9.8380 m/s²`.

The quoted field strength is RMS for a sinusoidal carrier, so the time-average DEP force matches the DC-equivalent value. A trace protocol must charge its duty cycle and actual geometry; three independent axis measurements are not automatically a common scalar force.

For a 1 ms kick followed by a 10 ms free drift,

`D = A tau_k (T + tau_k/2) = 103.30 µm`.

Holding the exterior sphere fixed while introducing 1% closed void changes mass and response by `1/0.99 - 1 = 1.0101%`, hence changes this displacement by 1.043 µm. A 0.2% response error corresponds to 0.207 µm displacement error. A simple three-screen second-difference trajectory estimator has position-noise factor `sqrt(6)` when the pre/post time intervals are comparable: its necessary single-screen precision scale is **84 nm**. More efficient many-frame estimators may improve random noise, but field reversal and several tensor components consume measurements and introduce correlated calibration errors.

The more useful 0.046% random response target derived below corresponds to approximately **19 nm** single-screen precision in that estimator. These values are noise scales, not achieved accuracy specifications.

For an ideal uniformly bright disk, each detected photon has coordinate standard deviation `a/2=7.5 µm`. Shot-noise centroid precision 84 nm needs approximately 7,900 photons per position. With ten observations per particle and two views at 7.28 million particles/s, the detected photon rate is 1.15e12/s: only 0.43 µW at 532 nm. **Photon energy is not the primary obstruction.** Collection efficiency, speckle, sensor noise, optical shape, timing and stable centroid definition are the metrology problems.

At 2 µm object pixels a particle occupies a 15×15 ROI. The same ten observations and two views create a minimum **65.5 GB/s** of 16-bit ROI values, excluding background, track association and metadata. An 86 mm square beam imaged at that pitch needs 1.86 billion pixels/frame; 10 kframes/s would be 18.6 trillion pixels/s. Ordinary full-frame imaging is therefore a poor architecture. Tiled line-scan/light-sheet/event processing must be designed and costed. Freezing axial blur below 0.1 µm at 10 m/s requires 10 ns illumination, although a transverse estimator may tolerate and model axial streaking. A nominal `lambda/NA²` depth-of-field scale at NA 0.1 is 53 µm: light-sheet thickness, depth localization and electrode visibility cannot be left unspecified.

## 3. Optical center, center of mass and rotation

A centroid can have excellent repeatability while following the wrong mechanical point. For a spherical exterior with a closed cavity volume fraction `phi`, displacement between geometric center and center of mass satisfies the coarse bound

`d_CM <= phi a/(1-phi)`.

At `phi=1%`, this is 0.152 µm, already comparable to the 0.207 µm response-error budget. A grain spinning at 1000 rad/s can give a geometric-center acceleration `d_CM omega² ≈ 0.152 m/s²`, approximately 1.54% of the DEP signal. Irregular opaque grains can also move their shadow/scattering centroid as they rotate. A measurement of optical centroid precision alone does not bound these errors.

There is a possible conservative restriction for spherical exteriors, not a general solution: the worst three-screen second difference from a rotating bounded offset is at most `4 d_CM`. Here `4a/D=0.581`; combining this with the mass response gives a worst normalized response lower bound

`[1 - (4a/D)phi]/(1-phi)`.

That remains increasing in `phi` in this particular geometry, but weakens the ideal void sensitivity by roughly 2.4 times. It requires a justified bounded tracking point and the correct actual estimator. General silhouettes, field-induced rotation, spin, nonuniform force application, and the internally reported passive-force counterexample are not closed by this inequality. Short-time force-at-offset rotational mobility can increase measured response, but long drift and pre-spin do not provide a universal sign guarantee.

Electrostatic alignment is also fast enough to matter. With only 1% polarizability anisotropy,

`I ≈ 0.4 m a² = 3.44e-21 kg m²`,

`torque_scale ≈ (delta alpha) E²/2 = 1.88e-15 N m`.

If treated as constant for a scale estimate, rotation from rest during 1 ms is 0.273 rad. For 10% anisotropy it is 2.73 rad; the constant-torque approximation then ceases to describe the trajectory but correctly warns of a large effect. Thus slow sequential axis kicks generally do not measure three diagonal entries of one fixed tensor. Balanced rapid cycling could suppress alignment torque in an ideal geometry, but a realizable covariance, mechanical point and finite-size force still need proof. This report assumes no such proof.

## 4. Residual charge and field calibration

One electron gives a `qE` force scale equal to 0.0427% of the DEP force. A DC residual charge of only five electrons would already consume the nominal 0.2% budget. The following are **stress cases**, not an assertion about a powder's typical charge distribution:

| Charge | `qE/F_DEP` | DC displacement during 1 ms kick | DC displacement including drift |
|---|---:|---:|---:|
| 10,000 electrons | 4.27 | 21.0 µm | 441 µm |
| 100,000 electrons | 42.7 | 210 µm | 4.41 mm |

A 100 kHz sinusoidal carrier reduces the peak charge micromotion to approximately 0.150 nm and 1.50 nm, respectively, for the stated RMS field. In the ideal high-frequency expansion the charge ponderomotive force relative to DEP is of order

`q²/(m omega² alpha_axis)`:

4.5e-7 and 4.5e-5 in those cases. Alternating fields are therefore an important feasible mitigation, already present in the 1986 vacuum DEP proposal. They do not automatically remove static Coulomb interactions, image forces, patch fields, charge-dependent trajectories or finite switching envelopes. Pure sign subtraction in two spatially different trajectories samples different field gains; a charged grain's 21 µm in-kick displacement is 2.1% of the field scale. The root's demodulation calculation must supply a quantitative residual bound.

At a wall distance 0.5 mm, the ideal image-charge force has scale `q²/(16 pi epsilon_0 h²)`: 0.0061% of DEP for 10,000 electrons and 0.614% for 100,000. At the same pair separation, direct Coulomb force is four times those fractions. AC field reversal does not remove direct static particle-particle charge forces. Baseline subtraction is only valid to the accuracy of the trajectory and force model.

For a geometrically similar electrode cell, `G=E g ∝ V²/L³`, so

`delta G/G ≈ 2 delta V/V - 3 delta L/L`.

A 0.1% gain budget by itself requires voltage stability 5e-4 or gap stability 0.33 µm at a 1 mm gap, before sharing the budget with other errors. This is plausible in a clean isolated cell, but scales poorly with contamination and thousands of independent maps. Deposition of just one part per million of a 1 kg/h feed is 1 mg/h. Uniformly distributed over 10 cm² it adds 0.37 µm/h of aluminum thickness, giving roughly 0.11%/h geometric gain drift; local deposits and charge patches can be worse. This is a sensitivity calculation, not a measured deposition fraction. Cleaning/calibration uptime and rejected dust must be charged.

The symmetric-sphere finite-size scale `(a/L)²` is 2.25e-4, or 0.0225%, already significant for a 0.046% random target. General shapes need not enjoy the same leading cancellation. No finite-size correction is treated as solved here.

## 5. Particle occupancy and interactions

At 1 kg/h, monodisperse 30 µm aluminum means **7.277 million particles/s** and 2.620e10 particles/hour. Approximately 80,000 particles occupy an 11 ms measurement flight at once. Size dispersion changes count strongly; finer tails make the optical/channel burden larger.

For induced dipole `p=alpha_axis E`, the worst collinear aligned pair force is

`F_dd = 3 p²/(2 pi epsilon_0 r⁴)`.

It reaches 0.2% of the intended force near `r=317 µm`. At 500 µm it is 0.0324%, and the single-neighbor field perturbation scale is 0.0054%. Several neighbors, charge and nonidentical polarizabilities need separate budgets.

**Important cancellation caveat:** for equal spheres in a uniform applied field, ideal equal orthogonal averaging makes the leading pair energy vanish, because `sum_i [p_i·p_i - 3(p_i·rhat)²]=0`. The single-axis force calculation is consequently a conservative stress test, not a universal throughput impossibility proof. Actual gradient fields vary over 1 mm, and particle anisotropy and feedback break that ideal model. An optimistic 150 µm exclusion radius is listed only to show sensitivity to a future justified cancellation result; it is not an established bound. At 150 µm, the raw worst single-axis pair force is 4% of the intended force.

For a random spatial Poisson beam, the probability of no neighbor within radius `r` is `exp[-(4pi/3) n r³]`. At 10 m/s and 95% geometrically isolated particles:

| Exclusion radius | Density limit (particles/m³) | Beam area for 1 kg/h | Square side | Independent Poisson lane count from axial neighbor veto |
|---|---:|---:|---:|---:|
| 500 µm, conservative stress envelope | 9.80e7 | 7.43e-3 m² | 86 mm | 14,188 |
| 150 µm, optimistic conditional residual | 3.63e9 | 2.01e-4 m² | 14 mm | 4,257 |

The lane calculation uses `P_clean=exp[-2 lambda r/u]` and treats interlane interactions as separately shielded/separated. A 1 mm lane pitch at 14,188 lanes occupies approximately a 119 mm square grid. The 3D beam and lane counts are alternative geometries, not quantities to multiply. Neither a single millimetre-scale gradient field nor a single camera covers this without a deliberately constructed field/optics array.

Hard-clocked injection changes the result substantially: 500 µm exact axial spacing at 10 m/s allows 20,000 particles/s per lane and a minimum 364 lanes. That is a **supplied singulation interface**, not a property of random powder flow. Deterministic spacing, agglomerate rejection, lane routing and longitudinal velocity dispersion must be demonstrated. Neighbor veto lowers accepted throughput, so “1 kg/h feed” is not “1 kg/h certified output.”

## 6. Gas drag and the vacuum feed

For a free-molecular gas, the Epstein linear-drag model gives

`b = delta (4pi/3) a² rho_g cbar`,

`tau_drag=m/b = rho a/(delta rho_g cbar)`.

The dependence on gas/surface accommodation is real; `delta=1–1.4` is an assumed envelope, not measured for this powder. The underlying gas-kinetic regimes and surface-scattering dependence are derived in [Epstein, Phys. Rev. 23, 710, 1924](https://doi.org/10.1103/PhysRev.23.710) and [Li and Wang, Phys. Rev. E 68, 061206, 2003](https://doi.org/10.1103/PhysRevE.68.061206).

For nitrogen at 300 K, `cbar=476 m/s`, `tau_drag≈7.57/(delta P[Pa]) s`. The exact damped kick/drift displacement used in the model is

`D_drag = A tau [tau_k - tau(1-exp(-tau_k/tau))]`

`         + A tau²(1-exp(-tau_k/tau))(1-exp(-T/tau))`.

At 0.1 Pa the signal reduction is 0.0069–0.0097%; Brownian displacement over 10 ms is about 1 nm. At 1 Pa the reduction is 0.069–0.097%. Thus **quiescent background gas is manageable** near 0.1 Pa. A local 10 m/s relative gas stream at 0.1 Pa nevertheless gives drag acceleration 0.13–0.18 m/s², larger than a 0.2% signal error. Pressure alone does not specify local gas velocity or nozzle transients.

One standard litre/min of carrier gas loads the chamber by roughly `Q=1.69 Pa m³/s`. Holding 0.1 Pa needs `S=Q/P≈16,900 L/s` pumping speed before conductance losses. A gas-entrained feed therefore carries large hidden pumping capital. A dry mechanical airlock is more promising: 1 kg/h solid aluminum occupies only 0.370 L/h; with 50% volumetric fill, entrained atmospheric void air of similar volume requires an ideal pumping scale around 104 L/s at 0.1 Pa. Real seals, differential pumping, outgassing, powder capture and charge/agglomeration still require design and measurement.

## 7. One-sided confidence changes the precision target

“0.2% uncertainty” must distinguish a hard bound, systematic budget, single-particle standard deviation and an ensemble standard error. Only the first two, or a validated confidence construction, can support a certificate on a new grain. Averaging many grains does not certify each grain.

For illustration only, assume normalized additive Gaussian measurement noise with known standard deviation `s=sigma_R/R0`, a known one-sided systematic budget `b`, and use `R_U/R0 = R_hat/R0 + b + z s`. To keep the probability of **any** upper-bound coverage failure in one hour below 1%, the union bound requires a per-grain failure probability at most

`0.01/(2.620e10) = 3.817e-13`, hence `z=7.1676`.

The union bound does not require independent particles. The Gaussian tail model does require validation and cannot be established to 1e-13 probability by a small prototype. At `s=0.2%`, the guard alone is 1.4335%. Five sigma would still give about 7,510 upper-bound coverage failures/hour in this model; this is not automatically the count of false classifications, which also depends on true response margins.

To certify a 1% void ceiling, the ideal material threshold is `R_U/R0 <= 1/0.99 = 1.010101`. Requiring 95% dense-sphere acceptance means

`s <= (0.010101 - b)/(7.1676 + 1.64485)`.

This is **0.1146%** for zero systematic budget, or 0.1033% with a 0.1% systematic budget. At `s=0.2%`, dense-sphere acceptance is only 1.71% before systematic errors. A 2% void ceiling is much less demanding in the ideal model: approximately 99.88% dense acceptance at 0.2% random noise and the same confidence rule.

The root/materials analysis supplies a tighter illustrative normalized threshold **1.004056** after its material budget. This report does not rederive that material threshold. At the same confidence and yield:

`s <= 0.004056/(7.1676 + 1.64485) = 0.0460%`,

before any additional systematic budget. That is approximately a 19 nm three-screen position-noise scale. Neither 0.046% response acquisition nor an appropriate tail bound has been achieved here. A true validated hard 0.2% error bound would be a different specification from 0.2% RMS and must not be dismissed by the Gaussian calculation, but repeatability does not supply such a bound.

## 8. Sorting is a separate interface

A 1%-void response difference gives only a 1 µm differential displacement. A passive knife-edge collection scheme therefore needs submicrometre incoming phase-space control or a measured larger separation stage. Active classification can trigger a much larger kick, but must address one grain without significantly kicking its neighbors.

At 10 m/s, a 1 ms actuator spans 10 mm along the trajectory. At the conservative 513 particles/s lane rate above, the probability of no other particle arriving within ±1 ms is only **35.8%**. Thus 500 µm spacing sufficient for one interaction budget is insufficient for independent 10 mm sorting pulses. Under the conservative rule that no neighbor may overlap the full pulse, 95% actuator isolation allows 25.6/s per lane and needs **283,754 lanes**. This is a sufficient stress constraint, not a theorem: rare-defect grouped rejection, metered injection, shielded segmented traveling waveforms, or carefully bounded partial kicks can alter it.

For a 100 µm sorting shift and 10 ms drift:

| Sorting pulse | Active length at 10 m/s | Required acceleration | RMS field if `G∝E²` at fixed transverse scale | 95% isolated Poisson lanes |
|---|---:|---:|---:|---:|
| 1 ms | 10 mm | 9.52 m/s² | 0.98 MV/m | 283,754 |
| 0.1 ms | 1 mm | 99.5 m/s² | 3.18 MV/m | 28,376 |
| 10 µs | 0.1 mm | 1000 m/s² | 10.1 MV/m | 2,838 |

The short-pulse estimates do not establish compatible electrode geometry. Electrostatic fringing links axial localization to aperture size, and dirty high-field operation, switching envelopes and neighboring-lane coupling remain unclosed. A two-particle sorting experiment is necessary; a single isolated grain deflection cannot validate addressability.

At 14,188 reference lanes a 1×10 mm electrode face over a 1 mm gap has ideal capacitance only 0.089 pF/lane, but an assumed 10 pF/lane wiring load dominates. At 100 kHz and 1 kV RMS this is approximately 89 kVAR per axis. Reactive power is not dissipation; a resonant energy-recovery design could reduce losses. Naively charging/discharging that load gives a `CV²f` loss scale of 14 kW/axis. An isolated binary half-`CV²` kick of every particle would be only about 36 W at 10 pF, illustrating why carrier drive and independently addressable switching must be designed separately.

Radiation pressure is not a free replacement: ideal reflection at the DEP force requires about 56 mW focused onto one grain. A 1 ms pulse carries 56 µJ. With an assumed `cp=900 J/(kg K)`, absorption of 10% of that incident energy gives about 164 K temperature rise before thermal losses; absorption also changes the force efficiency and therefore the required incident power. A real partially reflecting aluminum grain needs absorption and torque characterization. Gas jets conflict with the low-flow vacuum design. Charging grains for a Coulomb kicker can be powerful, but supplies another charge-control and contamination interface rather than eliminating one.

No bill of materials or supplier pricing was obtained. Real capital remains UNKNOWN. Minimum charged subsystems are dry feed/airlocks and recovery, vacuum vessel and conductance-sized pumps, singulation and neighbor detection, electrode/field-map arrays, high-voltage carrier and switching, pulsed illumination and calibrated imaging, real-time association/classification, particle collection, calibration artifacts, cleaning and downtime. Quoting launch mass, photon power or ideal electrode capacitance alone would hide the main costs.

## 9. Falsifiable prototype and next milestone

Do not start by claiming 1 kg/h. First require a realizable observable and its uncertainty mapping from actual fields and optical trajectories to `Tr(alpha)/m`. The team's internal passive-force counterexample rules out treating a generic positive three-field ensemble as that mapping. Any restriction to concentric cavities, nearly spherical exterior, bounded spin, known composition or measured shape/orientation must appear in the certificate's admission test. Outside that admitted domain the output is UNKNOWN.

**Gate A: one-particle acquisition.** Use a dry-fed or individually launched grain, approximately 1 mm electrode gap, nominal 1 kV RMS carrier near 100 kHz, background pressure ≤0.1 Pa, a calibrated 1 ms force region and 10 ms downstream flight. Begin at 1 m/s for geometric access, then verify 10 m/s; the interaction length must change accordingly. Use calibrated pulse-shadow images from two views and retain complete raw trajectories. Measure charge by a separate sign-odd diagnostic, field waveform and geometry before blind testing. A stable dense sphere controls field gain but cannot alone calibrate shape-dependent errors on unknown grains.

Blind controls should include dense and known-void metal spheres at nominal 0%, 1%, 2% and 5% cavity fraction, deliberately off-center cavities, exterior-shape variations, charge sweeps up to the stated stress envelope, and measured spin. For a 30 µm sphere, a central 1% spherical cavity has diameter 6.46 µm. Acquire and capture each test particle in an indexed well, then determine ground truth by destructive serial sectioning/FIB-SEM or another independently bounded method. X-rays are absent from the operating certificate; destructive validation is allowed. Manufacturing accurate closed aluminum cavity standards and validating their ground-truth fraction are explicit work items, not assumed solved. Larger standards can debug forces but do not establish 30 µm performance.

Predeclare the response estimator, admission domain, upper-bound construction and bias budget. Sweep carrier frequency, voltage, gradient sign, orientation, pressure and velocity; fit allowed parameters only on calibration data and freeze before blind evaluation. The immediate falsifiers are: failure to recover the same trace across admitted orientations, negative bias larger than its bound on off-center cavities, unresolved charge-even or rotation terms, optical center shifts exceeding the budget, or held-out error incompatible with the claimed model. Repeatability below 0.2% is insufficient if an admitted systematic effect can lower response enough to pass a voided grain. A successful small test does not establish industrial Gaussian tails or universal validity.

**Gate B: neighboring particles and sorting.** Introduce known pairs at 150, 317 and 500 µm separation, multiple alignments and charge signs. Compare each response with its isolated reference under the *actual* trace waveform. Vary separation and check the predicted distance scaling; measure whether orthogonal cancellation survives gradients and nonidentical grains. In the same apparatus, classify one grain and pulse the sorter while a second good grain passes at controlled time offsets. The sorter must demonstrate the declared target displacement and a bounded non-target disturbance/collection loss. Failure cannot be repaired by silently excluding close neighbors without reducing accepted throughput.

**Gate C: one-lane acquisition/production accounting.** Only after Gates A/B, run a realistic dry aluminum powder lane near 500–1000 particles/s, retain feed and accepted/rejected mass, neighbor statistics, charge/spin distributions, deposition, calibration drift and collection yield. At 1000 particles/s the monodisperse mass rate is only **0.137 g/h**. This is an engineering milestone, not a kilogram-per-hour demonstration. Demonstrate stable uncertainty and useful one-sided yield over a fixed period with the calibration frozen; recovery time, cleaning and rejected material count against production.

The next milestone after that is a costed, mechanically realizable 16–64-lane tile with measured optical association, driver losses, field cross-talk, singulation, vacuum conductance and independent sorting. Multiplication by the required thousands of lanes is justified only after those interfaces are measured. At present the valid conclusion is a conditional static inequality plus a demanding, structurally incomplete acquisition proposal. There is no supported claim of a new practical powder-sorting capability.
