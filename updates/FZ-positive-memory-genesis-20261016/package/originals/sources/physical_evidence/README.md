# Astra: pulse-controlled catalytic selectivity — evidence checkpoint

Date: 2026-10-16. Status: **bounded mechanism-acquisition lead, not a new demonstrated physical operation**.

## Result and attribution

The selected system is Pd/activated-carbon acetylene semihydrogenation under a time-dependent applied voltage. Xu and coauthors, not Astra, reported the experimentally demonstrated dynamic selectivity enhancement [S1–S3]. This checkpoint contributes calculations from published aggregates, a restricted causal null test, a metal-site-only purge bound, and an unperformed acquisition experiment. Historical originality of these deductions is not established. Generic dynamic selectivity and electrochemically triggered catalytic state transitions have prior art [S5–S6].

Independent screening preceded repository access. Candidates included support-polarized catalysts, mechanochemical ammonia, electrical heat-transport control, rapid Joule-heating recycling, and electron-beam atomic manipulation. Pd catalysis was selected because molecular products, a stimulus-duration scan, and mechanistic controls were reported in an actual operating system. This was an exploratory screen, not an exhaustive ranking of all technologies. The sources for alternatives are in `sources.json`.

Astra capital was subsequently inspected at Git revision `3dde9ce74d829a93388e64032d27351b36dd2221`, especially `technology/README.md` and `frontier/dossiers/N879.txt`. Its relevant lessons concern species-resolved outputs, hidden inventories, complete switching/reset costs, and prohibition of transferring a response between incompatible regimes. No archived mathematical theorem is treated here as a measured Pd response. No repository files were changed.

## What was actually acquired

Primary paper/preprint text, parsed supplementary text, and visual inspection of supplementary pages 5, 13–14, and 20–22 were available. Supplementary figures/current traces and carbon tables were inspected visually; figures were not numerically digitized. The final paper's Fig. 2 and Fig. 6 previews were also inspected.

Downloads of the Fig. 2 and Fig. 6 XLSX source workbooks were located but could not be acquired in this environment. The URLs are retained in `sources.json`. There are no raw chromatograms, instrument waveforms, original workbooks, new measurements, or validated kinetic simulations in this package. `observations.csv` is a manual transcription of published aggregate values, not the original dataset. File hashes establish the integrity of this checkpoint only, not that of original source files.

The quantitative endpoint calculation uses the **2025 preprint v1**; it does not silently relabel those numbers as a verified transcription of the final 2026 Fig. 2. The SI's separate 10-second/1-second example is kept separate from the preprint's 10-second/0.1-second optimum. Its inconsistencies are reported, not repaired by substitution.

## Reproduce

Run `python3 analysis.py` with Python 3.10 or later. No third-party package or network access is required. It writes `results.json` and `derived_fluxes.csv` and executes elementary numerical consistency checks. These checks are not experimental validation or an independent scientific review.

## Reaction contract and selectivity

Write A = acetylene, B = ethylene, C = ethane. The two-step idealization is A + H2 -> B, B + H2 -> C. Let a be A consumption and b be C generation in mol/s. The preprint uses S = a/(a+b), rather than the usual net ethylene gain divided by acetylene consumption. Under consistent molar-flow normalization and C2-only balance:

`b/A_in = X*(1/S - 1)`

`net B / A_consumed = 2 - 1/S`

`net B / A_in = X*(2 - 1/S)`.

From the preprint's values, the no-applied-voltage baseline has net B/A_in = -0.7590, the static +1.5 V state -0.07792, and the optimal dynamic state +0.61379. Negative values are possible because B is already abundant in the feed. These are conditional reconstructions, not directly measured net-flux traces.

The printed methods use concentration notation. Raw records are needed to establish flow normalization and detector calibration. A separate exact two-step gas-contraction sensitivity scenario is included: taking those concentrations literally as gas mole fractions moves the dynamic/static ethane ratio from 0.22148 to 0.22300. This does not account for oligomers, leaks, calibration bias, or unmeasured storage, and is not a confidence interval.

## Restricted causal null

The preprint's best waveform spends 10 s at +1.5 V and 0.1 s at -0.1 V. The negative duty is 0.9901%. Let b+ denote the static-positive ethane rate and let the negative-phase ethane rate be nonnegative. A memoryless mixture has

`b_average >= (10/10.1)*b+ = 0.990099*b+`.

The reconstructed ratio is 0.221477. Thus the instantaneous endpoint-mixture null is incompatible with the reported aggregate points, under the common-specimen/calibration/flow assumptions. More generally, the positive-phase mean ethane rate is at most 0.223692 times b+, assuming nonnegative ethane production during the negative phase.

The normalized integrated deficit during the positive phase is at least

`10 - 10.1*(b_average/b+) = 7.76308 seconds`.

This is **suppression-equivalent time, NOT a measured memory lifetime**. It does not locate the state in the catalyst or establish electronic memory. Reactor residence/composition, membrane hydration, interfacial potential lag, adsorbate coverage, hydrogen or other chemical inventory, thermal transients, and run-history/calibration problems remain possible explanations.

A decimal-rounding-only sensitivity gives ratios 0.21948–0.22349. That interval does not represent instrument or biological/physical replicate uncertainty.

## Single-purge capacity test

Ten milligrams of 1 wt% Pd/AC contains 0.1 mg Pd, or 0.93967 micromol of total Pd atoms. Using the reported 9.918 mol A/gPd/h activity to normalize the absolute flux scale, the avoided ethane production beyond even granting zero ethane production throughout the negative pulse is approximately 2.3392 micromol/cycle, or **2.4894 events per total Pd atom**.

A deliberately generous *metal-site-only single-purge model* permits at most one cleared ethylene molecule per total Pd atom, including buried atoms, and no persistent influence on later turnovers. That restricted model cannot account for the inferred deficit. A larger support reservoir, repeated release/replenishment during the pulse, altered subsequent adsorption/turnovers, or an electrical/reactor state escapes this bound. It is not a universal proof against desorption-based dynamic catalysis.

The absolute scale combines the preprint endpoint ratios with final-SI activity; source-version reconciliation remains required. The nominal 0.5 mL/min acetylene feed at 298 K supplies a close cross-check under an explicit volumetric-flow reference assumption. The exact two-step gas-contraction scenario gives 2.4369 events/Pd. Neither scenario is a validated uncertainty interval.

## Mechanism and data cautions

The SI excludes charging transients when forming its representative 4.41 mA current average. The plotted switching trace has ampere-scale transients, but their charge/energy cannot be inferred reliably from the preview alone. Even 4.41 mA sustained for 10 seconds corresponds to about 0.486 electron equivalents per total Pd atom. This is a charge scale, not measured hydrogen uptake or a whole-cycle integral. A small stoichiometric current/turnover ratio does not exclude rewriting a small catalytic inventory that influences many turnovers.

The SI's printed dynamic rates imply S = 1.65/(1.65+0.40) = 80.49%, not its stated 78.3%. Its printed absolute rate changes imply an equivalent current of 100.02 mA, rather than 95.04 mA. These are reconciliation items. They do not by themselves establish that the experimental effect is false.

The SI reports 98.6% carbon closure for its unspecified-duration oscillating row. At A:B = 1:20, the 1.4% total-carbon deficit is 0.294 acetylene-feed equivalents. A good-looking whole-feed closure can therefore be material on the desired minor-product scale. Closure is not a calibrated error bar and cannot bound compensating errors in different species.

The authors performed actual controls to distinguish desorption from hydrogenation; these should not be described as absent. However, time-resolved Pd-foil spectroscopy uses a different hydrogen supply, electrical contact/current scale, potential range, and time scale from the productive nanoparticle reactor. Those controls support their scoped interpretations but do not supply a measured 0.1-second response kernel for the productive mixed-feed electrode.

Any thermal transition-state model must use a barrier evaluated at the same instantaneous control, `G_TS(E)-G_i(E)`. Subtracting a ground-state energy at one voltage from a transition-state energy at another is not, on its own, an available activation barrier. Nonequilibrium excitation or retained populations require their own dynamics and switching-work accounting. This is a model-consistency constraint, not an argument that dynamic catalysis is impossible [S7].

## Technological assessment

The demonstrated effect acts on a useful chemical reaction, but is not a new energy source. With 1% incoming acetylene, 81% conversion leaves roughly 1,900 ppm before flow-contraction correction; a 1 ppm target would require approximately 99.99% conversion. No repeated identical-stage extrapolation is licensed because local composition and surface protection change as acetylene is depleted.

A relevant 2026 static Pd2/ND@G comparator reports 93.2% conventional net selectivity at full reported acetylene conversion and 100 C. It uses different hydrogen fraction and space velocity [S4]. Therefore it is neither a matched defeat of room-temperature dynamic catalysis nor evidence that the latter is best. 'Full conversion' is also not a substitute for a validated sub-ppm detection limit.

Complete switching energy, electrode/counterelectrode chemistry, hydrogen and membrane-conditioning requirements, operational durability, same-specification outlet purity, and area-specific productivity must be assessed together. The reported productivity corresponds to about 21 mg/h of net added ethylene for 0.1 mg Pd; on the preprint's 5 cm2 geometric area, about 42 g/m2/h. Net newly produced ethylene must not be confused with the much larger purified co-feed throughput. No industrial area or cost extrapolation is established.

## Next decisive acquisition

The next action is one common-initial-state, same-electrode pulse/hold experiment, not a new device architecture. See `EXPERIMENT.md`. Only if the measured hold response and accessible inventories survive that test should a full response library or additional synthesis targets be developed. Generic catalytic memory is already prior art, so a successful test would still require a specific new mechanism/control claim and a separate novelty audit.

This tranche advances from an assumed interface to a published molecular-output response and a narrower causal question. It does **not** demonstrate an increase in Astra's rate of discovering new physical capabilities or a civilisation-scale breakthrough.
