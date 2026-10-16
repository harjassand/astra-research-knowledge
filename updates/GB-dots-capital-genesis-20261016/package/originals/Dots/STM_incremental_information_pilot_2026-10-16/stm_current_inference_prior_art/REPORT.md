# Current-trace inference: bounded prior-art and identifiability check

## Result

**The proposed information source and broad operation are not new.** Primary experiments already infer lattice-site occupancy and hopping from tunneling current, and reconstruct Ag/Ag(111) atom pathways from manipulation signals. The defensible candidate is narrower: calibrated prediction of an image-confirmed endpoint or target attainment at an already-triggered scan boundary in the Chen archive, using measured-state/action/history plus current, with demonstrated incremental information over action-only baselines and honest uncertainty across chronological changes. No such result has been established in this check.

**Universal physical inversion is not justified by this archive.** That is not a proof that useful statistical endpoint prediction is impossible. The archived observables can support a conditional predictive distribution without uniquely identifying the entire atom trajectory.

## Strongest primary precedents

### Direct current-to-lattice-site readout: Stroscio and Celotta, 2004

*Controlling the Dynamics of a Single Atom in Lateral Atom Manipulation*, Science 306, 242–247, DOI https://doi.org/10.1126/science.1102370 . Full primary paper: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=620561 .

Figure 3 and pp. 243–244 are decisive. For Co/Cu(111), the raster is paused at known lateral positions and the height servo disabled. Two current levels identify occupation of an hcp site and its nearest fcc neighbor. Closer to the hcp center, four levels identify the hcp and three adjacent fcc sites. Transition ordering and residence-time distributions are inferred, not merely the occurrence of motion. The known lattice registration and controlled fixed tip position are essential context. This is restricted-state current-to-position inference, not a benchmark for arbitrary moving-tip endpoint estimation. Note 19 explicitly relates current to bias and exponentially to height.

### Closest same-material pathway precedent: Hla, Braun and Rieder, 2003

*Single-atom manipulation mechanisms during a quantum corral construction*, Phys. Rev. B 67, 201402(R), DOI https://doi.org/10.1103/PhysRevB.67.201402 . Primary PDF: https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.67.201402/fulltext .

Ag on Ag(111), constant-current manipulation, known lattice-relative paths and tip speed. Figures 3–4 reconstruct 2.89 Å same-sublattice hops, shorter fcc/hcp visits, row-crossing move/rest/jump cycles, and sliding paths from tip-height signals. Importantly, p. 201402-3 explains a semicircular detour through adjacent sites that leaves no apparent manipulation-signal signature. This is substantial prior art against a general claim of discovering displacement/path information in manipulation traces, and concrete caution against identifying every hop from spikes. It is **not current-only experimental inversion**: the signal analyzed is the height response of constant-current feedback.

### Model-based current/height pathway interpretation: Kühnle et al., 2002

*Understanding atom movement during lateral manipulation with the STM tip using a simple simulation method*, Surface Science 499, 15–23. DOI https://doi.org/10.1016/S0039-6028(01)01848-9 . Primary abstract/introduction: https://www.sciencedirect.com/science/article/abs/pii/S0039602801018489 .

The work models atom pathways and manipulation curves from tip-plus-surface potentials, and compares iodine/Cu(111) experimental height curves to simulated constant-height currents. It explicitly distinguishes experimental constant-current height signals from computed constant-height currents, explaining their analogous information content. Thus a physically constrained hop/path decoder is also an established methodological class; a universal decoder without the constraints is not established.

### Adjacent prior work, without conflating observables

- Moresco et al., *Recording intramolecular mechanics during the manipulation of a large molecule*, PRL 87, 088302 (2001), https://doi.org/10.1103/PhysRevLett.87.088302 ; primary abstract https://pubmed.ncbi.nlm.nih.gov/11497988/ . Constant-height experimental current plus theory reveals intramolecular motion. This broadens the earlier signal-to-configuration precedent, but is a molecule experiment, not Ag endpoint prediction.
- Scheidt et al., *Concept for the Real-Time Monitoring of Molecular Configurations during Manipulation with a Scanning Probe Microscope*, J. Phys. Chem. C 127, 13817–13836 (2023), https://doi.org/10.1021/acs.jpcc.3c02072 . Primary text https://pmc.ncbi.nlm.nih.gov/articles/PMC10364088/ and author repository https://juser.fz-juelich.de/record/1009369/files/acs.jpcc.3c02072.pdf?version=1 . POMDP/particle-filter configuration monitoring with precomputed atomistic models and force-gradient evidence is an experimental non-image state-estimation precedent. It is not current-only Ag localization.
- Bao, Archibald and Maksymovych, *Lévy Backward SDE Filter for Jump Diffusion Processes and Its Applications in Material Sciences*, Commun. Comput. Phys. 27, 589–618 (2020), https://doi.org/10.4208/cicp.OA-2018-0238 ; primary PDF https://global-sci.com/index.php/cicp/article/download/6793/13522/14752 . Although motivated by current/force jump observations, the atom-tracking demonstrations are simulations and explicitly assume noisy observed atom coordinates (p. 612), not experimental current inversion. Do not treat this as a matched physical baseline.

## What Chen actually supplies

Chen et al. 2022, https://doi.org/10.1038/s41467-022-35149-w , uses a current CNN plus empirical jump rule to choose scans, then localizes from images. Unscanned positions are carried forward. Its own Methods cite Hla for distance/direction information in manipulation signals. This rules out calling current-based movement information itself new, while leaving endpoint prediction unevaluated.

Static source inspected from the companion qualification, pinned commit ace9ca3f9be401bb9c8146d0bfc2882e87141f7e:
- https://github.com/SINGROUP/Atom_manipulation_with_RL/blob/ace9ca3f9be401bb9c8146d0bfc2882e87141f7e/AMRL/Environment/createc_control.py#L134-L176
- https://github.com/SINGROUP/Atom_manipulation_with_RL/blob/ace9ca3f9be401bb9c8146d0bfc2882e87141f7e/AMRL/Environment/Env_new.py#L303-L348

The controller acquires time, X, Y, current and topography; the environment retains current and d = sqrt((x-x0)^2+(y-y0)^2). **d is radial distance from the initial tip sample, not cumulative path length in general.** Neither snippet specifies the feedback mode; setting current/conductance does not establish whether the servo remains enabled during lateral manipulation. Do not assert that Chen is constant-height or constant-current without instrument-setting evidence.

## Identifiability analysis (our deductions)

1. A scalar current depends on atom-to-tip geometry, tip electronic structure, local density of states, bias, and height. Unknown height/tip changes can imitate amplitude changes attributed to lateral displacement. Even with known height, symmetric lateral configurations can give equivalent currents. The inverse is therefore not generally one-to-one without additional restrictions/calibration.
2. Under ideal constant-current feedback, very different atom paths can share the same setpoint current while information appears in Z. Finite-bandwidth current transients retain useful event information, but interpreting them requires the feedback response. Omitting Z and mode leaves this ambiguity unresolved. Under confirmed constant height, it would still require calibrated geometry/electronics and a restricted state space.
3. Omitted time prevents inference of physical dwell times, rates or velocities from sample index alone. It does not automatically prevent endpoint inference: d provides a spatial parameter when monotonic and properly aligned, and initial/action geometry adds constraints. Radial d loses angular/sign information; commanded endpoints are not an exact substitute for the measured XY trace after clipping/pixel mapping.
4. A hop count is not a 2-D displacement. Backtracking, alternate lattice directions, fcc/hcp alternation, invisible sliding, and motion during approach/retraction can break naive spike-count-to-endpoint maps. Last-observed state can also be stale after skipped scans.
5. The next scan measures the relaxed post-manipulation configuration. A trace ending before tip withdrawal does not by itself establish that this configuration equals the last in-trace configuration.

These are reasons not to claim unique inversion, not quantitative bounds on obtainable accuracy. No empirical collision pairs or impossibility theorem have been established here.

## Minimum differentiated capability and comparator contract

A credible result would demonstrate all of the following:

- Forecast the next measured displacement/target-attainment distribution from the exact pre-image information boundary, conditional on the already-existing scan decision. No next coordinates, rewards, done flags, images, future actions or freshness IDs as features.
- Include all action/current history since the last confirmed fresh image, or restrict to a verified fresh predecessor. Restrict labels to source-qualified fresh scans. Do not label carried-forward states as no-motion truth.
- Compare persistence; executed-command geometry; action/history-only strong nonlinear model; and action/history+simple trace statistics/hop-change-point features, then a strong sequence model. The published CNN is a motion-gating incumbent, not sufficient endpoint comparator. A constrained lattice-aware decoder is useful only where lattice orientation/registration and mode justify it.
- Show current adds held-out predictive information beyond geometry, policy progress and episode/tip correlations. Fix chronological episode-disjoint splits before new outcome access, guard reused images, burn the three previously inspected diagnostic episodes, calibrate uncertainty on development data, and evaluate changes of tip condition separately where identifiable.
- Use positional error and calibrated success probability/coverage, including near-threshold ambiguity from localization uncertainty. Avoid claiming exact lattice site identity from a 0.166 nm success radius.
- State scope: selected scan boundaries under this historical behavior policy. This is not a validated scan-skipping policy, throughput gain, counterfactual policy comparison, or physical trajectory reconstruction.

For stronger physical reconstruction, acquire/retain mode and feedback settings, synchronized measured XYZ/current/time, calibration and lattice registration, tip-change metadata, and validation of the atom state after release. Those are requirements for a future claim, not experiments authorized or performed here.

## Scope and stopping

Bounded primary-source search completed 2026-10-16 UTC. It found decisive older prior art; it is not an exhaustive novelty clearance and no absence claim is made. Read primary articles and existing static control sources; no episode downloads, unsafe deserialization, author-code execution, model fitting, hardware work, outreach, or new experiments. Companion source/data audit is in the STM qualification report.
