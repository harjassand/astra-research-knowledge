# Independent mechanism/novelty review

Date: 2026-10-10. Target: Ito et al. 2021 pulse-driven stator remodeling. This is a targeted primary-literature review and identifiability assessment, not an exhaustive priority search. No raw trajectories were downloaded or analyzed here.

## Bottom line

The defensible opportunity is an intervention-resolved kinetic result, not yet an identified molecular mechanism. Test whether a pulse commits the motor to a later torque-onset while it is stationary, and whether CW's larger success fraction arises from more first appearances or better retention. Hidden intermediates, catch-bond maturation, and multistep contact are already established prior art. A genuinely different molecular alternative worth excluding is **mechanical masking by the flagellar bearing**: an existing stator could be torque-capable but unable to move the rotor until external drive unpins or mechanically reorganizes the bearing. New 2026 bearing measurements make this more concrete than generic glass sticking, but do not establish it in the Ito assay.

## 1. What could be learned from the pulse traces

### A. Pulse-induced commitment before the first detectable torque

Proposed kinetic hypothesis: rotation populates a metastable precursor P; P persists after the drive ceases and matures into a torque-producing state A. This is meaningfully narrower than saying stators have hidden states: its defining feature is **externally induced, pre-first-torque memory** and completion without continuing rotation.

Null: after pulse termination, for motors demonstrably still at zero torque-output, the first-event hazard immediately returns to that motor's ordinary stationary baseline. In a simple memoryless model, accumulated first-event survival depends only on integrated time at each imposed condition, with no extra pulse-history term.

Test: locate first sustained positive-speed onset within each OFF interval, keeping motors at risk until that onset. Compare post-pulse OFF hazard against the pre-first-pulse stationary interval and suitable unstimulated remodeling data, with cell-level effects and time since the stripping intervention. A reproducible delayed OFF onset excess beyond edge/transient uncertainty rejects the strict instantaneous gate. Fit a decaying pulse-history term only as a kinetic description; it does not locate the memory in MotA, MotB, FliL, the rotor, or bearing.

Critical endpoint issue: the published procedure attributes a binding to ON when the mean speed in the next 1-s OFF exceeds a threshold. Under an ideal one-stator step and a threshold near half its speed, an event occurring in approximately the first half of OFF is also classified as ON. Re-localizing these events is therefore a direct assumption check rather than another fit to published endpoint probabilities. [Ito 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8163892/)

Controls: use causal or explicitly modeled filtering; exclude enough pulse-edge samples to remove filtering/electrorotation recoil; vary the exclusion window; preserve cell/run clustering and right censoring; account for cell frailty, changing risk sets, and stripping recovery. Frailty mixtures can create declining pooled hazards without molecular memory. A delay exceeding a filtering window alone is not proof of chemistry. A negative finding only bounds memory within the resolved timescale and 1-s OFF window; it cannot exclude a faster or much slower precursor.

### B. Direction-dependent survival versus attachment

Hypothesis: CW and CCW have comparable encounter/activation frequency but different loss rates for newly engaged units during the forced phase. This is a new question for this intervention, not a new catch-bond mechanism.

The identifiability problem is explicit. A two-state U <-> A process with forward rate a, reverse rate d, initially U, gives

    P(A at tau) = a/(a+d) * (1 - exp(-(a+d)*tau)).

A single endpoint at fixed tau cannot determine a and d separately. An OFF-average threshold makes the ambiguity larger. Ito's binding-rate conversion assumes negligible within-ON loss. Stable OFF survival does not independently establish negligible ON loss, because switching off changes load.

Best test: resolve first functional appearances and reversals during ON using a calibrated electrorotation baseline, then compare direction effects on first-appearance hazard and retention through the pulse boundary. If ON events cannot be resolved, describe results as probability of detectable post-pulse torque, not an elementary association rate. Direction-specific short OFF losses can constrain persistent stabilization differences but cannot fully recover direction-specific ON loss.

Prior art is particularly strong: torque-dependent lifetimes were established in Nord et al.; Wadhwa et al. already report direction-sensitive dissociation under positive versus negative motor torque. [Nord 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5724282/), [Wadhwa 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6576217/)

## 2. Distinct molecular alternative: a history-dependent bearing gate

Candidate, not a claimed discovery: rotor/rod–LP-ring contact states mechanically arrest a weakly powered rotor; imposed motion depins it or changes the barrier landscape, revealing pre-existing torque production. Subsequent rotation could then permit genuine recruitment. This shifts the initial causal bottleneck from activation/anchoring of an incoming stator to the rotor's internal mechanical bearing.

Motivation: Rieu et al. measured stator-independent passive bearing dynamics with roughly 26–28 preferred angles, broad relaxation times, and changing energy landscapes. Their equivalent barrier torque is about 200 pN nm, comparable to a single stator's torque. Those experiments are in E. coli with different probes; transfer to tethered Salmonella is an unverified inference. [Rieu 2026](https://www.nature.com/articles/s41467-026-74079-9)

Falsifiable consequences, if angular data and resolution permit:

- Restart probability or latency depends on pulse-end angular registry, not only speed/duration/direction. Separate high-order molecular periodicity from 1–2-fold body/glass geometry.
- Alleged zero-stator OFF intervals can show bounded, biased angular excursions and nonstationary dwell wells.
- A nonzero endogenous torque offset exists during external driving before the apparent first OFF appearance. Reliable measurement requires torque/drag calibration and adequate controls; imposing motion also changes stator kinetics.
- Simultaneous stator occupancy fluorescence and rotation would show some restart events without added occupancy. This is the cleanest distinguishing new experiment.

A simple static barrier alone may be inadequate: a rotor that has crossed one periodic well may pin at the next. The proposed version therefore requires landscape change/hysteresis or an already sufficient torque near the barrier, with thermal escape completing restart. Do not claim that a peak in angular occupancy proves this mechanism. Nor does failure to resolve 26–28 wells in a noisy tethered-cell assay refute it.

## 3. What is already known, and what not to relabel as new

- **Hidden states:** Shi et al. inferred a short-lived non-torque state from turnover kinetics. Wadhwa et al. later modeled diffusing D, loosely bound L, tightly bound T, and hidden H states, with load-dependent L/T transitions. A generic “primed stator” is insufficiently novel. [Shi 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6426456/), [Wadhwa 2022](https://www.nature.com/articles/s41467-022-33075-5)
- **Two-stage contact:** diffusion-limited collision followed by speed-dependent successful engagement was explicitly proposed in 2019. Merely adding “search” and “capture” stages repeats that framework. [Wadhwa 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6576217/)
- **Force-matured binding:** a two-state catch-bond model already explains asymmetric relaxation from high and low initial occupancy. Those authors tested, and found inadequate for that dataset, simple neighbor cooperativity and finite-pool explanations. [Perez-Carrasco et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8942351/)
- **Stator-stator interactions:** a 2025 fluctuation analysis specifically infers cooperative interactions from occupancy statistics. Any new statistical-cooperativity claim must distinguish this work and the rotational feedback already demonstrated by Ito. [Franco-Oñate et al. 2025](https://www.nature.com/articles/s41598-025-14570-3)
- **Pool-size effects:** a July 2026 primary preprint predicts and experimentally tests abundance-dependent on-rates and shifts in mechanosensitivity. Do not claim expression/pool dependence itself as new. [Wise et al. 2026, preprint](https://pubmed.ncbi.nlm.nih.gov/42619747/)
- **Direction-specific ion gating:** a 2026 preprint proposes contact-dependent MotA–FliG control of MotB ion release, aimed at physiological torque-speed asymmetry. It is relevant molecular prior art, not proof of assembly gating. [Zhu et al. 2026, v2 preprint](https://arxiv.org/abs/2604.00470v2)

## 4. Direction and interpretation cautions

The starting strain lacks cheY. Externally forced CW motion does **not by itself** establish the physiological CW switch conformation. Structural comparisons of active CW versus CCW motors therefore cannot simply be assigned to the two pulse directions. Nonetheless, Wadhwa 2019 observed occasional native CW rotation after electrorotation even in a cheY deletion and proposed force-induced switching. Check the sign of OFF motion rather than assuming a perfectly fixed switch state. [Wadhwa 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6576217/), [Johnson et al. 2024](https://pubmed.ncbi.nlm.nih.gov/38459206/)

The observables are functional torque/speed, not molecular occupancy. A zero-speed state can mix zero stators, nonconducting stators, mechanically disengaged stators, and pinning. Conversely, stepwise speed recovery is consistent with incorporation but does not uniquely identify it. With fixed pulse duration and OFF duration, many microscopic rate sets are observationally equivalent. Positive intervention memory would be a valuable falsification of a narrow model; molecular identification needs an orthogonal readout or a specifically discriminating perturbation.

## Recommended priority

1. Audit event timing within OFF and the robustness of first onset to pulse-edge filtering.
2. Quantify how much reported direction asymmetry survives a first-appearance versus survival decomposition, where identifiable.
3. If angle is retained, screen for mechanical masking/registry dependence as a competing explanation.
4. State any result as a new kinetic constraint unless molecular alternatives have actually been distinguished.
