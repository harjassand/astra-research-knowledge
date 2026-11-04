# What the blind-tomography result enables

4 November 2026. This assessment accompanies PROOF.md and its independent AUDIT.md.

## Actual operation

Measure a baseline stationary histogram and the stationary histogram after each of several local changes. The controls have experiment identifiers, but their affected transition pairs and strengths are unknown. Under the stated promises, the reconstruction identifies which pair each control changed, aligns the recovered graph with the named measured states, and recovers every directed transition rate up to one common time scale. Rates on additional unperturbed transitions are included.

No time-resolved trajectory, relaxation rate, calibrated control amplitude, pre-labelled transition target, or prior full transition graph is supplied. Those are genuine omissions from the input contract. They are not supplied implicitly by choosing a numerical rate normalization.

The decisive steps are: finite response vectors reveal a transformed incidence geometry; established graphic-matroid reconstruction obtains the abstract target graph; cycle rigidity determines the linear generator map; and each column's unique negative diagonal identifies its physical state label. The last step works even with a uniform stationary distribution.

## Sufficient assumptions, not a complete minimal classification

- All states are fully observed and retain their correct names across experiments. Their evolution follows one finite irreducible continuous-time Markov generator before each control.
- Each control changes only one pair of opposite rates by a common positive nonunit factor. Both rates on that pair are positive. The experiment does not create hidden states or alter other transitions.
- Distinct active target pairs form a spanning 3-vertex-connected graph. The full generator can contain other unperturbed, including one-way, transitions. A complete target graph is not required.
- Every selected pair carries nonzero baseline current, so every response is nonzero. The three-state complete triangle is a separately proved small case.
- Exact identification uses exact probabilities. Finite-data recovery needs sufficient response amplitude, conditioning and sign margins, with iid samples or a justified effective-sample analysis. These margins can fail near equilibrium or nearly trivial interventions.

These are sufficient assumptions of the proved theorem, not asserted necessary conditions for every blind experiment. In particular, the work does not classify all graphs below three-connectivity or certify locality from a successful numerical fit.

## Strongest existing comparisons

The graph-reconstruction operation is classical: Bixby–Cunningham network-matrix recognition, Seymour graphic-matroid reconstruction and Whitney uniqueness. Existing inverse problems already use matroid reconstruction from unlabelled data. Markov static-response and finite-edge mutual-linearity formulas are also established. The assembled contract must therefore not be advertised as a new general graph-reconstruction principle or as the first blind network identification method.

Known blind dynamic-network methods infer unknown inputs and network structure from time-series or other structured perturbations. Direct trajectories recover absolute rates and do not need local barrier controls. Calibrated global reset experiments give generator inversion from stationary histograms, including at equilibrium. The present result exchanges these stronger observations or calibrations for a restrictive local-control coverage promise and retains an unknown common clock.

The independent audit documents these comparisons and their input differences. No established method was shown to be impossible or slower under a fully matched physical resource budget. An existing network-matrix algorithm coupled to the same response identities can implement the essential reconstruction.

## What has and has not been earned

Earned: an exact polynomial-time inverse theorem, a fully explicit complete-graph reconstruction including the three- and four-state ambiguities, finite-control consistency equations, a conditional noisy reconstruction bound, and independent exact checks on dense and sparse examples with extra unperturbed transitions.

Not earned: an experimentally available family of selective controls, a method for proving an apparatus obeys locality, a uniform finite-sample guarantee, absolute time, hidden-state or hidden-channel recovery, novelty clearance, a demonstrated acquisition-cost advantage, or a civilisation-scale consequence.

A meaningful next test would use a system with visible states but genuinely uncalibrated selective transition controls, measure the required rank and sign margins, and compare total acquisition cost with trajectory and reset-based identification. Until that gate is crossed, this is a scoped mathematical acquisition result rather than a deployed scientific instrument.
