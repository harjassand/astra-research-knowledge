# Pressure-written Hg-1223: a concrete circulating-current test, with the memory claim kept identifiable

Status: `CONCRETE_EXPERIMENT_DERIVED; NOT_PHYSICALLY_DEMONSTRATED; MICROSCOPIC_MEMORY_CARRIER_UNRESOLVED; MISSION_NOT_ACHIEVED`.

The best operation I can substantiate is an **electrodeless, mechanically released annulus test**. It can measure the net current passing around an entire Hg-1223 specimen at the same temperature, field and age, without reconstructing high-current contacts after extraction. A second, independently controlled time variable distinguishes loss of material capacity from decay of an already circulating current. Neither pressure retention nor contactless ring-current measurement is a new invention. No acquired experiment establishes the proposed Hg-1223 performance.

## 1. What the primary evidence actually admits

Deng et al., PNAS 123, e2536178123 (2026), DOI [10.1073/pnas.2536178123](https://doi.org/10.1073/pnas.2536178123), reports onset temperatures up to 151 K after pressure release, measured inside the DAC. Its extracted S2 has magnetic onset around 140 K. The reported 78% shielding estimate is evaluated at 70 K. The published supplement S5 follows resistance after storage and temperature cycles to 160–170 K; curves drift. It does not establish 24-hour current capacity at 140 K. S6 explicitly shows the extracted magnetic trace multiplied by ten. The material's microscopic history carrier is unresolved.

The original specimen dimensions are square diagonals about 80–120 micrometres and thickness about 20 micrometres; the chamber is about 100–130 micrometres. These admit an 80-micrometre outer-diameter annulus in a sufficiently large starting specimen. Fabrication, pressure cycling and cold recovery of such an annulus have **not** been demonstrated in the acquired record.

The main article and the published nine-page SI were independently acquired from Europe PMC, rather than from another worker or an arXiv copy. See `ACQUISITION_RECEIPTS.json`; S5 and S6 were visually inspected.

An immediate physical restriction matters: if the recovered phase really has a maximum superconducting transition of only about 140 K, substantial current **at** 140 K is not supported by that observation. Test 135 and 138 K first, and retain 140 K as the demanding original acceptance point. Reaching it requires the cold-recovered specimen itself to retain adequate capacity above 140 K. It cannot be inferred from another specimen's 151 K onset.

## 2. The measurement: link the entire current path

Machine a closed annulus **before** the pressure-writing treatment, qualify its untreated response, and perform the published pressure–temperature treatment. Recover it without warming above its experimentally measured stability limit. Remove anvils and pressure-medium bridges, including material spanning the aperture. Mount it in a perforated, nonmagnetic cradle with weak, measured support forces and access to both faces.

Inductively charge a circulating current using a controlled magnetic-field history. Hold the final external field and specimen temperature fixed. A vector magnetic microscope measures a closed contour Gamma lying entirely outside the specimen, threading the central aperture and enclosing one complete radial cross-section of the annulus. In the quasistatic limit,

\[
I_{\rm wind}=\frac{1}{\mu_0}\oint_\Gamma \mathbf B\cdot d\boldsymbol\ell.
\]

This is ordinary Maxwell–Ampere physics, applied to an experimentally useful geometry. It is not a new theorem. Its advantages over a center-field or Bean-model estimate are specific:

1. The contour encloses the **whole** cross-section. A nonzero result measures net current around the hole, independently of how that current is distributed through the cross-section.
2. By current continuity, the same net current crosses every radial cut when the ring has no electrical branches and charge accumulation is negligible.
3. Local screening loops in disconnected grains have zero algebraic intersection with this full cut. Local bound magnetization contributes zero because the contour lies outside magnetized matter: the integral of its curl reduces to a boundary magnetization term that vanishes there.
4. A uniform background field has exactly zero closed-contour integral. External gradients also have zero integral if their source currents do not thread the chosen surface. Spatially varying calibration errors and temporal drift still require measurement.
5. A current can be concentrated in a small connected fraction; the measured **gross** capacity already charges that disadvantage. No superconducting volume fraction is substituted for current capacity.

For a nonuniform specimen, conservatively report

\[
J_{\rm gross,LB}(t)=\frac{|\widehat I_{\rm wind}(t)|-u_I(t)}{A_{\max,\rm UB}},
\]

where the denominator is an upper bound on the largest complete cross-section around the usable ring. This avoids turning an unknown thin active filament into an inflated current density. Also report the absolute current and all measured cross-sections.

A slit control is essential. A ring cut completely across its radial width cannot support net steady winding current, even though it can retain local superconducting shielding. Prepare slit controls before pressure treatment; a sacrificial post-measurement cut provides an additional control but can damage the material and must not be the sole comparison.

Two nested linked contours, multiple angular cuts, reversed loading polarity, and a known-current calibration loop test the integral. Hall-probe bias wires and other conductors must not introduce an unaccounted current threading Gamma. A reference sensor follows drift while the contour is scanned. An inaccessible part of the contour must not be filled in by an unvalidated current model.

## 3. Quantitative design within the reported specimen scale

All values in this table are proposed geometry, acceptance criteria or electromagnetic calculations. None is a measured Hg-1223 current.

| Quantity | Value or requirement |
|---|---:|
| Inner / outer radius | 20 / 40 micrometres |
| Thickness | 20 micrometres |
| Gross cross-section | 400 square micrometres = 0.0004 square millimetres |
| Specimen volume | 0.0754 nanolitres |
| Current corresponding to 1,000 A/mm2 | 0.400 A |
| Required current if area upper bound is 10% larger | 0.440 A, before current uncertainty |
| Proposed meridional contour | radial coordinate 10–50 micrometres; height -20 to +20 micrometres |
| Contour length | 160 micrometres |
| Average tangential self-field on that contour at 0.4 A | 3.14 mT |
| Field-error budget of 10 microtesla everywhere on contour | at most 1.27 mA current error, before geometry and quadrature errors |
| Field-error budget of 50 microtesla | at most 6.37 mA current error, before other errors |
| Illustrative center field, assuming uniform current density | 8.18 mT |
| Illustrative field 5 micrometres above the top face | 5.97 mT |

The field error follows directly from

\[
|\delta I|\leq \ell_\Gamma\epsilon_B/\mu_0.
\]

It is a design budget, not a claimed instrument accuracy. Finite sensor area, position errors, field gradients, angular calibration, scan duration and temperature-dependent gain must be included. Repeat at larger contour distances and finer sampling to bound finite-aperture and integration effects.

Published vector Hall instrumentation has already demonstrated approximately 5 × 5 micrometre active area and operation over 10–300 K; the 2004 instrument report gives about 1 microtesla/√Hz resolution. This establishes a relevant sensor regime, not an assembled cold-extraction apparatus. [Cambel et al., JMMM (2004)](https://doi.org/10.1016/j.jmmm.2003.12.865). A later primary method reconstructs three-dimensional fields with 700 nm spatial resolution from height-resolved Hall maps and was demonstrated at 77 K: [Dede et al., APL 109, 182407 (2016)](https://doi.org/10.1063/1.4966896).

The script `annulus_calculation.py` performs a finite-filament Biot–Savart calculation. The Ampere integral reconstructs an imposed 0.400 A as 0.400003645 A, a numerical discrepancy of 9.1 × 10^-6 relative. Adding a uniform 0.1 T background does not change it. A second construction with +0.4 A at radius 25 micrometres and -0.4 A at 35 micrometres produces a 2.87 mT center field but essentially zero net winding current. This is the explicit reason a center-field signal alone is insufficient. These are electromagnetic sanity checks, not evidence that Hg-1223 supplies either current distribution.

The instrument must qualify the **joint** target, for example T = 140 K, external B = 0.1 T in the worse measured orientation, and current lower bound above the chosen threshold throughout 24 hours. Measure both principal field orientations and the local total field including self-field. A lower-temperature positive control separates specimen or instrumentation failure from absence of enhanced-temperature current.

## 4. Separate material age from current decay

One decaying magnetic signal cannot identify the loss of a pressure-written material state. A fixed material can show vortex creep, while a changing material can reduce its current capacity. In a lumped representation,

\[
L(q)\dot I+I\dot L(q)+V_{\rm creep}(I,q,T,B)=-\dot\Phi_{\rm ext},
\qquad \dot q=F(q,T,B,I).
\]

One measured I(t) does not identify both q(t) and the voltage law. A time-dependent current trace can always be fitted by either changing the state variable or changing an effective creep law along that trajectory. This is an identifiability obstruction, not a reason to stop.

Use two explicit clocks: material age a under a specified temperature/field exposure, and dwell time tau since a standardized current-loading procedure. Measure I(a,tau), including first-load current capacity at different ages.

The minimum discriminating comparison is a matched pair of identically written, recovered rings:

- Ring A is loaded at the start of the service-temperature hold and then monitored.
- Ring B follows the same temperature and field schedule with measured net current held near zero, and receives its first standardized load only at the late age, such as 24 hours.

Replicate matched pairs to estimate preparation variability; two specimens are an identifiability design, not a statistical replication claim. Compare early and late first-load curves at equal dwell times and equal loading histories. A smaller current in A with unchanged late first-load capacity in B points to decay of the loaded state. Reduced capacity in B establishes loss during unloaded aging, independent of that loaded-current decay. Current-induced material damage remains a separate possibility if only loaded specimens lose reload capacity.

Where possible, reset and reload A at the late age. A thermal flux reset is admissible only after demonstrating that it preserves material capacity within the required uncertainty. The Hg SI's cycles to 160–170 K motivate investigating such a window but do not certify it. Do not assume that warming above the superconducting transition leaves the pressure-written state intact. If no harmless reset exists, use independent first-load cohorts instead. All loading-field losses and transient heating enter the recorded history.

This design identifies **operational material memory** and its effect on current capacity. It does not identify whether the slow variable is oxygen ordering, defect topology, internal strain, or electronic order.

## 5. A bounded mechanism intervention

Add a pressure–temperature-order experiment only after the ring measurement works. Compare warm loading followed by cooling and cold release with loading performed only after cooling, followed by the same cold release. Match final pressure, final temperature, subsequent storage and current readout. Measure actual trajectories and heat deposited during loading; cold compression cannot be assumed isothermal during plastic events.

A successful cold-only write would reject the narrow hypothesis that **warm, thermally activated oxygen ordering during pressure application is indispensable**. A warm-only success would show that a thermally activated preparation step matters, while still allowing both oxygen and defect mechanisms. Neither outcome alone names the atomic memory carrier. This is a useful falsification test with an explicit limited conclusion.

The released specimen can also be mapped by cryogenic microdiffraction before and after the same aging/erasure sequence. Resolve multiple noncoplanar reciprocal-lattice vectors and line profiles; one broadened peak cannot uniquely separate strain, disorder and coherent-domain size. Include unilluminated controls because the probe itself may alter defects. A correlation between diffraction broadening and current capacity is evidence about a state, not a selective causal proof of its carrier.

For the proposed volume V and maximum distance R, measured support forces give an average-stress bound of scale R sum|F|/V. For total support force at most 3 micronewtons this is about 1.59 kPa, far below the writing pressure. This is a proposed metrology bound, not an achieved mount. It addresses support confinement. It does **not** exclude self-equilibrated internal strain, dislocations, changed atomic arrangements or a structural metastable phase.

## 6. Current persistence is stronger than onset, but retain the voltage boundary

A 188.5-micrometre mean circumference corresponds to 18.85 nV total loop voltage at 1 microvolt/cm. A persistent-current measurement integrates very small voltages over time and avoids that lead-voltage measurement. Nevertheless, the Ampere integral alone certifies current, not a local electric field or terminal-delivered power.

Under an independently calibrated, time-independent inductance, fixed external flux, and absence of coupled-current or material-energy sources, average loop voltage follows from L Delta I / Delta t. Even the deliberately loose conditional bound L <= 1 nH and at most 1% loss of 0.4 A over 24 hours would yield mean loop voltage <= 4.63 × 10^-17 V. This is an illustration of the integrator's sensitivity, **not** an experimental resistance bound. Near the transition, kinetic inductance and material evolution must be checked. A loop-average voltage bound also cannot be silently promoted to a pointwise electric-field bound at every weak section.

Therefore report two separate outcomes: (i) measured net circulating current sustained at specified T, B and time, and (ii) any voltage/resistance inference with its extra assumptions. A cable or lead still requires actual terminal transport, contacts, stabilisation, protection and full packaging qualification.

## 7. Strong prior art prevents an inflated operation claim

Tomita et al., [PRL 96, 077001 (2006)](https://doi.org/10.1103/PhysRevLett.96.077001), already measured pressure-written current enhancement in YBCO bicrystalline rings and its thermal relaxation. Their 0.6 GPa treatment increased Jc at 9 K from 1.291 to 1.447 kA/cm2; cold pressure release removed 0.125 kA/cm2, retaining only 0.031 kA/cm2. Thus about 2.4% of baseline current density, or 20% of the pressure-induced gain, survived. The relaxed quantity was current capacity itself. The authors linked it to oxygen ordering using temperature and oxygenation dependence. Their result is far stronger coupled evidence than an onset-plus-low-temperature-shielding combination, but it is not a consequential conductor improvement relative to modern textured conductors.

For the same useful-output class, Ali et al. demonstrated a 90 mm ring magnet made from 200 REBCO loops, with peak trapped field 4.6 T at 25 K and relaxation measured for 16.5 hours; the split tape had measured critical current 490 A at 77 K. [SST 33, 04LT01 (2020)](https://doi.org/10.1088/1361-6668/ab794a). A proposed micrometre Hg ring generating millitesla does not compete with that magnet merely because it operates hotter. It is a diagnostic sample. Manufacturing yield, pressure tooling, cold retrieval, mercury handling, refrigeration, usable field volume, field stability and service life all remain charged.

For a strictly matched millitesla field at this microscopic geometry, an externally driven normal-metal loop and a permanent micromagnet are also necessary comparators. The normal loop's conductor-only loss would be

\[
P_{\rm loop}=I^2\rho\ell/A
=0.754\ {\rm mW}\,[\rho/(10^{-8}\ {\rm ohm\,m})]
\]

at 0.4 A. Here rho must be measured for the actual fabricated conductor; the reference value merely sets units and is not an assumed copper material property. Leads, cooling and field programmability must be matched. This illustrates why a millitesla demonstration alone would not establish a consequential technological advantage.

## 8. Decision

The physically specific next step is now sharper than “measure Jc”: fabricate and qualify a ring, recover it cold, measure its net winding current with a linked magnetic contour, then compare loaded and unloaded aging at the same temperature and field. This removes a real contact and identifiability obstacle **if executed successfully**. It does not make the atomic memory carrier known, demonstrate the target current, or establish technological superiority.

No exceptional physical operation has been established in this tranche. The useful contribution is an independently derived experimental design, its electromagnetic calculation, a concrete counterexample to center-field inference, and an unusually close piece of prior art that limits novelty and expected retained benefit.

Artifacts: `DESIGN_CALCULATION.json`, `annulus_calculation.py`, `ACQUISITION_RECEIPTS.json`, `CLAIM_LEDGER.json`, and primary sources under `sources/`. No GitHub writes or external messages were made; no other worker's scientific results were read.
