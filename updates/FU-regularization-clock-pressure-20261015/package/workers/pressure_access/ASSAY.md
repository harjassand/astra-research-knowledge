# Decisive release-and-transport assay

This is a proposed laboratory protocol, **not an acquired apparatus, authorized external experiment, or predicted successful result**. It needs an appropriate high-pressure superconductivity laboratory. No external messages were sent. Start from the published preparation and extraction procedures, rather than an invented conductor architecture.

## First screen: recoverable conducting enhancement

Question: after actual removal from the anvils and gasket, does the same pressure-treated specimen carry a reproducible low-dissipation current above its matched pristine transition?

1. Use characterized sibling pieces from a batch, assigning permanent IDs before treatment. Measure pristine transport and magnetization without conflating onset, midpoint and zero-voltage criteria. Save raw measured current, each voltage polarity, thermometer readings, field vector, timestamps, geometry and contact images. Include rapid-release, slow-release and no-pressure thermal-history controls; randomize measurement order. A few pieces can identify a hard failure, but cannot estimate industrial yield.
2. On each treatment piece, record `P(t), T(t)` and the quench trajectory. A recorded screw motion is not a measured quench rate. Track the same sample through initial DAC measurement, nominal pressure release, physical separation from anvils/gasket and low-traction mounting. Bound mounting/contact loads where they matter. Do not assert an exactly traction-free mounted conductor.
3. First use the ordinary warm extraction route already demonstrated for magnetic measurement. Record its actual peak temperature, dwell and contact-making history. Re-establish four contacts using established micromanipulation methods with independently checked contact heating; the practicability and survival of those contacts must themselves be recorded. Do not count FIB implantation or annealing as harmless by assumption.
4. Screen at `T_screen=T_pristine,onset+2 K` with an uncertainty interval entirely above the matched pristine transition, beginning at small bias and self-field. For an illustrative pristine onset of 133 K this is 135 K. This is a proposed discriminator, not a measured operating point. Acquire bipolar I–V curves, independent voltage-pair/current-path permutations, thermal stabilization and zero-current offset records. If the specimen remains in Van der Pauw geometry, report the actual four-terminal transfer resistances; postpone a uniform-bar `E` or `J` claim until the geometry/current distribution is qualified.
5. Require a connected low-voltage interval, correct current/voltage polarity behavior, repeatability, intact contacts and calibrated temperature. Compare with matched history controls and normal-state readings. A mere onset shift or a current-dependent temperature shift does not pass.

Failure scope: no enhanced conducting path in the tested recovered specimen/history/precision window. It neither disproves its in-cell transition nor excludes a different preparation. If the in-cell response survives but the extracted transport screen fails, **stop current/pinning optimization**. The material premise needed for a conductor is missing.

## Separating mechanical release from thermal relaxation

If this screen fails but a strong in-cell response persists, the next causal test is a factorial comparison of mechanical status and temperature history. Use (a) the released specimen still in the DAC, subjected to the recorded warm extraction temperature history without extraction; (b) warm extracted specimens; and, only if a cold transfer method is actually demonstrated, (c) cold extracted specimens and (d) corresponding cold in-cell controls. Record failed transfer attempts and the contact/mounting histories.

This distinguishes thermal erasure from loss of residual confinement or handling damage. It does not assume that cold extraction is available. A cold-only success establishes a cold-conditioned extracted state and must carry its cold handling/reset cost.

Local diffraction strain mapping and magnetic measurements before/after the transport sequence can test storage hypotheses. Their acquisition and potential disturbance of the state must be included. Correlating a diffraction width with onset is not yet a causal barrier measurement; isolate thermal history, oxygen configuration, mechanical support and aging sufficiently to test competing explanations.

## Qualification only after the screen passes

Prepare a geometrically measured bridge and acquire the joint surface `I-V(T,B,orientation,age)` on that same state. Begin below its actual observed current and temperature limits. Do not import pinning or relaxation coefficients from an irradiated crystal or a differently doped film.

The pasted ambitious decision threshold can then be tested: `140 K`, external `0.1 T` in the less favorable measured orientation, gross specimen `J>=1000 A/mm^2`, `E<=1 microvolt/cm`, with a `24 h` current hold. These are chosen research thresholds, not a universal industry specification or expected performance. Include self-field and all specified operating tolerances in the actual test.

For the illustrative `60 by 20 micrometre` cross-section and `50 micrometre` voltage spacing, the current is `1.2 A` and allowed voltage is `5 nV`. Bound acceptance with measured uncertainties, for example

`E_upper=(|V_odd|+bounded_offset+statistical_allowance)/L_lower`,

`J_lower=I_lower/(width_upper*thickness_upper)`.

Here `V_odd=(V(+I)-V(-I))/2` removes only an additive even-in-current offset. Use calibrated reversal settling, reference channels, injected known signals and drift records. For independent noise of standard deviation `sigma_pair`, averaging reduces the stochastic term as `sigma_pair/sqrt(N)`; unknown systematic drift does not decrease that way. An assumed 50 nV pair noise would require 2,500 independent pairs to bring a five-sigma stochastic allowance to 5 nV, before any offset/geometry allowance. This example is not an instrument specification.

A constant-direction DC hold and a rapidly alternating-current experiment are different operations. Specify current-direction, downtime and reversal/calibration periods in advance, log the actual waveform and integrate delivered current. If uninterrupted DC is the task, validate offsets with independent reference channels during the hold and use bipolar I–V checks before and after; do not silently replace it with a low-duty pulsed test. Thermometry must establish specimen temperature under the actual load, not merely the bath setting. Measure contact/lead losses and refrigerator input as well as the voltage segment.

Log all specimens and all failures. A single successful hold establishes only that specimen and interval. Under independent identical trials, zero failures in 59 trials gives a one-sided 95% upper failure-probability bound of about 4.95%; 299 trials is needed for about 1%. Neither infers longer service life. Multi-temperature aging can test an activation model; one storage temperature cannot identify an activation barrier or attempt time.

## Obtainable information versus unacquired operation

Available now: published main text, published SI figures, methods, journal metadata, primary film transport and REBCO system baselines, and conditional arithmetic. The official archive supplies no numerical raw traces.

Potentially obtainable with access, but not acquired here: original V+/V-/I/T/time logs; exact temperature history during extraction; cold pressure traces and release rate; specimen dimensions/contact map; raw XRD frames and instrument calibration; failed-sample/yield records. These would audit the published precursor but cannot manufacture a missing post-extraction current test.

Required new physical observation: the same liberated specimen delivering the specified current, field, voltage and duration simultaneously, with measured control/heat/reset costs. A lab, material, cold transfer capability and successful response remain unacquired. No current public dataset located in this audit already supplies that observation.
