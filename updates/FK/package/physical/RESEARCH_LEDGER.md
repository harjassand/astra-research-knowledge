# Astra physical-operation investigation — 14 October 2026

## Status

No new practically consequential physical operation is established by this investigation. The strongest retained opportunity is **carrier-gated selection of dislocation reactions**, rather than generic electrical or optical dislocation motion. The constituent responses have experimental precedents. The proposed reaction-selectivity advantage, historical novelty, implementation in a consequential material, and throughput remain unestablished. No experiment or calibrated material simulation was performed here.

Repository consulted selectively at revision `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`: `00_START_HERE.txt` and `technology/README.md`. No repository theorem was used as a physical premise. No repository mutation was performed.

## Proposed operational contract

Input: an experimentally mapped defect network in a specified crystal and strain state, with known slip geometry and Burgers vectors, subject to measured illumination, thermal and mechanical constraints.

Desired output: a changed reaction outcome that removes specified harmful defect content, remains improved after controls return to operating conditions, and does not substitute a hidden fault, junction, surface defect or unacceptable plastic distortion for the original defect.

Critical distinction: changing the relative velocities of defect populations can change encounter geometry. Merely multiplying every velocity by the same positive scalar changes the clock in an autonomous deterministic drift model, not its paths. This is a mathematical observation, not a claim of new historical theory.

For two glide coordinates, a candidate independent control requires, at the same configuration and mechanical conditions,

`D = v1(Ia)*v2(Ib) - v2(Ia)*v1(Ib) != 0`.

A nonzero determinant is not sufficient for a useful annihilation route: compatible topology, permitted reactions, pinning, noise, and retention still have to be demonstrated. The published different core responses motivate this test; they do not supply a measured network-control matrix.

## Preserved negative results

### N1 — Mobility does not imply annihilation

In lattice-constant units, the two coplanar partial Burgers vectors `[1,-2,1]/6` and `[2,-1,-1]/6` sum to `[1,-1,0]/2`, not zero. Both make a 30-degree angle with line direction `[1,-1,0]`. Bringing them together can restore a perfect screw dislocation rather than remove the topological defect. The exact rational check is in `checks.py`.

For an opposite-Burgers pair on a common slip plane, with line length L and initial separation d, annihilation by glide can still produce plastic shear of magnitude `b*L*d/V` in a simple volume-averaged geometry. Zero final net Burgers content is not zero accumulated plastic distortion.

### N2 — Do not assemble incompatible material regimes

Electrical partial-dislocation motion and optical suppression of strain-driven threading-dislocation motion are separate experiments and defect geometries. The optical-gating ZnS thin-film methods include 350-degree-C anneals. A joint room-temperature electrical drive / optical lock operation is not established by juxtaposing the papers.

The high-field atomistic illustration in the electrical-motion paper is not a quantitative barrier measurement at the lower estimated experimental fields. Observed motion itself is not disputed.

### N3 — Population processing cannot be inferred from a selected maximum

A maximum segment speed is not a sustained velocity, a travel-range demonstration, a removable population fraction, or qualified area per hour. Pinning and reaction accessibility must be measured across the relevant distribution. The travel and voltage calculations in `checks.json` are explicitly hypothetical extrapolations, not a performance forecast.

### N4 — Spectral notching is not an established autonomous alignment operation

Consider a deliberately simplified reset model: each reset lands within the desired frequency window with probability q; reset attempt rates are ro outside the window and ri inside it. Its target occupancy p obeys

`dp/dt = q*ro*(1-p) - (1-q)*ri*p`,

so `p_stationary = q*ro / (q*ro + (1-q)*ri)`.

Concentrating q=0.01 to p=0.99 requires ro/ri=9801. This is a conditional arithmetic requirement, not a measured property. In the assessed silicon T-center experiment, off-resonant perturbation still produces spectral diffusion. Making the emitter itself optically dark therefore does not establish a protected frequency window. The rejection is scoped to this proposed mechanism in the measured regime; it is not a universal prohibition on feedback, optical cooling, or other materials.

### N5 — Existing physics is not Astra novelty

Carrier-assisted room-temperature glide and dislocation interactions in GaAs/Si, and strain-engineered dislocation reduction, predate this investigation. Demonstrated nonreciprocal thermal emission is also prior work; an emissivity/absorptivity contrast is not by itself a net conversion-efficiency advantage. No useful-work advantage for a new radiation-based architecture was established here.

## Smallest decisive experimental sequence

1. Use the demonstrated ZnS optical-gating platform and its actual thermal regime. Map a real small network containing a compatible removal route and a competing unfavorable reaction. Do not assign arbitrary charges, slip planes or Burgers vectors to convenient abstract particles. Sample selection and preparation costs count.
2. Establish reproducible non-proportional mobility control in that network's relevant defect classes. Measure temperature, carrier-sensitive response, specimen drift and readout-beam effects. Stop if illumination only changes total displacement or creates irreversible damage.
3. Compare reaction outcomes under a selected illumination schedule, an optimized dark control, constant illumination and a dose-matched timing control. Account for irreversible specimen history; repeated cycles are not independent replays of the same initial state.
4. Identify final Burgers content and fault structure with multiple suitable imaging/diffraction conditions. Report detection limits. Distinguish true annihilation, boundary export, out-of-view motion, junction formation and contrast loss. Check retention after controls are removed and under the intended operating conditions.
5. A positive mechanism result is not scaling validation. Later compare qualified material area per time, full wall-plug energy per qualified area, electrical/optical performance and damage against appropriate growth/filtering/annealing comparators in the same target material.

## Physical accounting requirements

Any model must couple dislocation geometry and pinning to carrier occupancy, internal electric fields, applied/thermal/piezoelectric stress, and the probabilities of junction formation, annihilation, climb, and new defect nucleation. Optical injection may change both force and mobility; those parameters are not independent free controls. A thermal-equilibrium noise law must not be assigned to an illuminated driven system without justification.

Measure net electrical input, optical-source wall power, heating, mechanical work, control/readout cost and any actually recovered energy. Stored strain energy released during a one-off repair is not a renewable energy source. Capacitive stored energy is not automatically identical to cycle dissipation.

## Primary-source ledger

These are source identifiers, not an exhaustive priority search. Reports are credited to their authors; preprint claims retain preprint status.

- Li et al., *Harnessing dislocation motion using an electric field*, Nature Materials (2023), DOI `10.1038/s41563-023-01572-7`; author manuscript `arXiv:2211.14933`. Main text and supplementary displacement/current/voltage figures inspected.
- Fonseca Montenegro et al., *A common origin of photoplastic and electroplastic effects in ZnS*, Physical Review Materials, DOI `10.1103/c2hc-lyp2`; detailed methods in `arXiv:2506.07908v2`, especially Sections III and VI.3.
- Callahan et al., *Direct observation of recombination-enhanced dislocation glide in heteroepitaxial GaAs on silicon*, Physical Review Materials 2, 081601(R) (2018), DOI `10.1103/PhysRevMaterials.2.081601`. Publisher abstract inspected; no uninspected full-text reaction details used as established evidence.
- *Asymmetric Dislocation Densities in Forward-Graded ZnS_ySe_(1-y)/GaAs (001) Heterostructures*, Journal of Electronic Materials (2010), DOI `10.1007/s11664-010-1101-z`. Publisher abstract reports overshoot-interface reduction through annihilation/coalescence.
- Frisch et al., *Dislocation response to electric fields in strontium titanate: A mesoscale indentation study*, Journal of the American Ceramic Society, DOI `10.1111/jace.70383`. First online 22 November 2025; 2026 volume. Null dislocation-response result is specific to the tested 2 kV/mm indentation conditions; it is not a universal impossibility.
- Xueyue Zhang et al., *Laser-induced spectral diffusion of T centers in silicon nanophotonic devices*, PRX Quantum 6, 030351 (2025), DOI `10.1103/x2cv-2gcw`; full author manuscript `arXiv:2504.08898v2`, especially the off-resonant perturbation comparison.
- Chaoshen Zhang et al., *Resolving and resetting the charge environment of single T-centers in silicon p-i-n waveguides*, `arXiv:2608.15993` (2026 preprint). A credited existing reset operation, not an Astra invention. Dark retention, readout-driven recovery, narrowing, screening and tuning must not be conflated.
- Zhenong Zhang et al., *Observation of Strong Nonreciprocal Thermal Emission*, Physical Review Letters 135, 016901 (2025), DOI `10.1103/PhysRevLett.135.016901`. Experimental directional emission/absorption contrast; no new whole-system efficiency result produced here.

## Reproduction

Run `python checks.py` to regenerate `checks.json`. Only Python's standard library is required. Exact rational checks cover the Burgers-vector example; floating-point arithmetic covers explicitly labeled scale and rate calculations. The binomial example assumes independent, identically distributed trials and must not be used to certify one evolving sample.
