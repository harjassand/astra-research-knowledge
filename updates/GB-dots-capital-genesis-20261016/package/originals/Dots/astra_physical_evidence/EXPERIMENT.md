# Decisive acquisition: single-pulse selectivity response

**Status: proposed, not performed.** This is an adaptation of established transient/isotopic catalytic measurements, not a claim to invention of those techniques. It requires a qualified catalysis/electrochemistry laboratory with appropriate hydrogen/acetylene gas controls.

## Exact question

After a brief negative pulse, does the same productive Pd/AC electrode suppress ethane production during a common +1.5 V hold, while retaining acetylene consumption, beyond what electrical/reactor transients and a one-shot accessible product purge explain?

The candidate operation is retained control of reaction branching after a short intervention. A simple observation of memory would not establish historical novelty; electrochemically triggered catalytic states and dynamic selectivity have prior art.

## First experiment; do not build a device first

Use the published mixed-feed specimen class and initial operating conditions: 10 mg of 1 wt% Pd/AC, the same membrane/electrode geometry, ambient temperature and pressure, 1:20:60:19 acetylene:ethylene:hydrogen:nitrogen, 50 mL/min total flow. Resolve actual flow reference conditions and all impurities before analysis. Do not substitute the foil desorption cell or a pure-gas kinetic test.

Establish a repeatable static +1.5 V reference. Randomize paired trials between a sham hold and a -0.1 V, 0.1-second pulse followed by the common +1.5 V read hold. Measure the complete subsequent response and recovery, not just the periodic GC average. Establish a return protocol experimentally; do not assume a reverse pulse erases all relevant states. Failed recovery or drift invalidates a common-initial-state comparison.

Measure actual working/reference and terminal potentials, the full signed current including switching transients, temperature, pressure, and calibrated species-resolved molar outputs. Verify the electrical transfer function and current-range saturation. The published SI peak plot must not be integrated as if it were a raw waveform.

Calibrate reactor and detector residence-time response separately under matched flow/pressure. Use sufficiently fast product detection or reproducible phase-resolved collection. Ordinary mass-28 detection is insufficient because the original feed contains both nitrogen and ethylene; ethane fragments and isotope overlaps also require validated chromatographic or high-resolution/fragmentation separation. Set the temporal resolution from the measured response and transfer function. Do not assert that a nominal sampling frequency alone resolves the catalyst kinetics.

## Minimal go/no-go analysis

Let b_ref(t) be the matched reference ethane rate and b_pulse(t) the post-pulse rate after correcting or jointly modelling the measured transport response. Define the hold-only deficit:

`D = integral_hold [b_ref(t) - b_pulse(t)] dt`.

Also measure hold-only acetylene consumption, net ethylene gain, carbon-bearing side products, and all uncertainty correlations. A useful engineering screen could demand at least 50% reduction of the undesired rate while retaining at least 90% of reference acetylene conversion; these are **proposed selection thresholds**, not scientific constants or claimed results.

For the one-shot purge hypothesis, acquire a conservative bound B_purge on the total product inventory that the pulse can directly release, including support, membrane, pore gas and Pd. Reject that restricted explanation only if the simultaneous lower confidence bound on D exceeds B_purge with all relevant stoichiometry and transport corrections. Total Pd atom count alone is not a bound on all accessible inventories.

Power the repetition count from pilot measurement variance. Use independent electrode preparations as well as within-electrode paired trials. Do not treat many sampled time points or repeated cycles on one electrode as independent specimens. Freeze calibration, uncertainty treatment and model comparisons before held-out pulse histories are tested.

## Identify what the control actually acts on

If the first hold effect survives, compare models based on interfacial potential lag, hydrocarbon coverage, hydrogen/other chemical inventory, and thermal response against held-out pulse widths and spacings. A narrow fit to the original periodic grid is insufficient. Acquire same-regime state measurements only as needed to discriminate the surviving models; lack of a bulk XAS change does not set a sufficiently small bound on a catalytically active minority phase.

A phase-resolved carbon-label experiment can distinguish ethane derived from feed ethylene from ethane derived from acetylene. For example, supply labelled acetylene and unlabelled ethylene while preserving total composition and verifying isotope effects and detector separation. Label-switch kinetic analysis is established prior art [S8], not the proposed technological operation. Avoid relying solely on H2/D2 switching, which also changes reaction kinetics and exchanges with membrane/support inventories.

## Advancement and stop rules

Advance to a response library only after independent molecular-output confirmation of the hold response and a physical state/transfer model that predicts new histories. A genuine new elementary control claim must specify which branch rates or populations become independently controllable beyond prior dynamic-catalysis and electrochemical-promotion operations.

Redirect if the apparent benefit is detector/flow aliasing, irreproducible conditioning, a single depleted reservoir, or an already-known mechanism without a consequential useful-output advantage. Preserve any accurate negative result. Do not infer an energy-efficient or scalable process from a small current fraction.

A subsequent technological test must compare the same outlet acetylene specification, net ethylene recovery, throughput, feed, full electrical/chemical/conditioning work, and durability with a strong static catalyst. Changes in composition toward the low-acetylene outlet require requalification; the original waveform cannot be cascaded by arithmetic alone.
