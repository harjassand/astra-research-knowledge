# Evidence audit: precursor choice and transferable synthesis kinetics

Audit date: 2026-11-05. Scope: Chen et al. 224-reaction study, the Precursor Genome ledger, ReactCA, and the 2026 Onsager-transport extension. This is an opportunity-selection audit, not a claim of an achieved synthesis theory.

## Decision

**Reject the broad claim that solid-state synthesis lacks a representation of contacts, reaction networks, or kinetic selectivity.** Those operations already exist in substantial form. The 2026 work explicitly combines ionic cross-correlations, chemical-potential gradients, diffusion-limited growth and spatial reaction simulation.

**The data support a narrower unresolved target: transfer of experimentally measurable interface kinetics into phase fractions on an independently calibrated physical clock across composition, particle geometry and thermal history. They do not establish that pairwise interface laws compose into such a predictor.** The Chen endpoints discriminate route rankings; they do not identify which mechanism causes ranking reversals. The Precursor Genome is a large first-contact endpoint collection, not a multicomponent kinetic closure experiment. Accordingly, these data alone do not justify choosing compositional closure as an already-evidenced discovery opportunity. A scientific contribution must construct and test the missing operation, not rename this residual gap.

## 1. Chen et al.: independent matched-condition reanalysis

Primary article: [Navigating phase diagram complexity to guide robotic inorganic materials synthesis](https://www.nature.com/articles/s44160-024-00502-y), Nature Synthesis 3, 606–614 (2024), DOI [10.1038/s44160-024-00502-y](https://doi.org/10.1038/s44160-024-00502-y). Theory code: [synthesis_planning_algorithm](https://github.com/dd-debug/synthesis_planning_algorithm). Data archive: [Figshare](https://doi.org/10.6084/m9.figshare.22671571).

The method ranks precursor sets by the target's depth in the reaction convex hull, using competing reactions within the precursor-composition region. It favors precursors with few or no competitive outcomes and substantial inverse-hull energy, including preformed ternary precursors. This is considerably stronger than merely asking whether the final target is thermodynamically stable.

### Generation conditions and selection

The reported campaign comprises 224 syntheses of 35 quaternary oxide targets using 28 precursors and covering 27 elements. Targets emphasize alkali-containing materials, including battery-relevant phosphates, borates and transition-metal oxides. It is a selected target set, not a random sample of inorganic chemistry.

The automated protocol uses powder dosing, 1 mL ethanol, ball milling for 15 h at 100 rpm, drying at 80°C for 2 h under vacuum, and an 8 h air anneal in alumina crucibles at selected temperatures between 600°C and 1000°C. There is no repeated grinding and annealing. Temperature is explored separately for each precursor route. The headline Figure 4C therefore compares each route's best observed result across its tested temperatures; it is not itself a matched-temperature route comparison.

### What the endpoint measures

Supplement SI2.2.3 defines the score as target-only fitted integrated XRD intensity divided by target intensity plus residual intensity. It is **not a full multiphase Rietveld mass fraction**. Only the target's crystal structure enters the automated fit. The best residual among 16 empty-holder background patterns is retained. Scattering-factor differences, model misfit and coincident peaks can affect the score. The authors advise mainly quantitative interpretation above 0.2 and use target integrated intensity 0.2 million counts as a detection cutoff.

A validation set of 255 independently collected, fully refined patterns is reported. The supplement describes a 22.9% average underestimation and a 4.6% root mean squared difference. These summaries cannot be converted into a universal per-sample mass-fraction standard error without the underlying normalization and calibration details. In particular, the endpoints should not be relabeled as exact weight purity.

A separate reproducibility campaign has 153 replicate experiments covering 20 target compositions in eight chemical systems at 600–1200°C. Paired score differences have reported mean -0.6 percentage points and standard deviation 7.6 points; 79.7% lie within 10 points. Crucibles were not required to be identical. This is useful reproducibility evidence, but there is no per-cell replicate count or confidence interval for the main route-temperature table. It does not license assigning independent Gaussian errors to every main-study score.

### Independently recomputed results

`analyze_chen.py` parses the numbered target tables in the supplement and joins routes on exact target identity and annealing temperature. Data and outputs are retained locally as `chen_extracted_temperature_rows.csv`, `chen_matched_temperatures.csv`, and `chen_reanalysis_summary.json`.

| Comparison | Predicted better by >10 points | Difference within 10 points | Traditional better by >10 points | Mean predicted-minus-traditional |
|---|---:|---:|---:|---:|
| Figure 4C, best temperature for each route, 35 targets | 15 | 16 | 4 | +15.04 points |
| Supplement, 100 matched target-temperature pairs | 40 | 44 | 16 | +10.51 points |

Figure 4C median improvement is only 3.62 points. The method offers useful aggregate improvement; it does not supply uniform dominance across the tested temperatures. The matched comparisons are correlated within targets and use rounded semi-quantitative scores. These counts are descriptive, not 100 independent statistical trials.

The supplement contains six target identities with score differences exceeding +10 points at one temperature and -10 at another: K3Al2(PO4)3, K3LiP2O7, KBaPO4, Li2CuP2O7, Li2TiGeO5 and LiMgPO4. Some cells have low target intensity or score, so the most interpretable example is:

| Target | Temperature | Traditional score | Predicted score | Difference |
|---|---:|---:|---:|---:|
| LiMgPO4 | 800°C | 0.29 | 0.70 | +0.41 |
| LiMgPO4 | 900°C | 0.75 | 0.60 | -0.15 |
| Li2TiSiO5 | 1000°C | 0.75 | 0.51 | -0.24 |

For LiMgPO4 the proposed precursor set is MgO + LiPO3; the traditional set is Li2CO3 + MgO + NH4H2PO4. All four highlighted LiMgPO4 scores exceed 0.2. Target integrated intensities at 800°C are 0.32 and 1.33 million counts; at 900°C, 1.61 and 1.37 million, respectively. Thus the reversal survives the authors' stated low-score and detection cautions. Its two-temperature difference in route advantage is 0.56. With no cell-specific replicates, this remains an observed reversal, not a calibrated significance result.

For Li2TiSiO5 the proposed Li2TiO3 + SiO2 route has zero computed competitors, reaction energy -0.026 eV/atom and inverse-hull energy -0.026 eV/atom in the supplement, yet loses the matched 1000°C endpoint comparison to Li2CO3 + TiO2 + SiO2. Target integrated intensities are 0.84 and 0.34 million counts, both above detection. This is a clear limitation of using the selector alone as an endpoint predictor. It does not by itself distinguish kinetic delay from a changing phase inventory, transient melting, nucleation, volatility or geometry.

### Data coverage and version reconciliation

The supplementary tables yield 202 numeric route-temperature rows, 35 targets and 100 matched pairs. KLi(PO3)2 contributes two additional traditional-only temperature rows. The raw-XRD workbook has 36 sheets and 219 paired angle-intensity patterns, rather than an unambiguous 224-pattern ledger. Filenames and table coverage are not perfectly aligned: some sheets have additional patterns or precursor-order duplicates, and one extra sheet is titled Li2Fe3(PO4)3. They cannot be assumed to be independent synthesis replicates.

There are also differences between raw supplementary scores and Figure 4C. For example, BaLiBO3 and KLi(PO3)2 have nonzero supplementary traditional maxima but zero plotted headline values, plausibly reflecting the stated intensity detection correction. K3LiP2O7 has supplementary predicted maximum 0.66 but Figure 4C value approximately 0.77209; LiSi2BO6 has traditional maximum 0.46 versus approximately 0.41246. These are larger than simple rounding. This audit preserves each source and does not claim complete reproduction of all 224 reported reactions or silently combine their versions.

## 2. Precursor Genome: actual ledger content

Sources: [repository](https://github.com/lauren-walters/precursor-genome), [raw ledger](https://raw.githubusercontent.com/lauren-walters/precursor-genome/main/ledger_precursor_genome.json), [Zenodo DOI](https://doi.org/10.5281/zenodo.21285545). The downloaded ledger is 31,165,664 bytes; its Git blob identifier was a8ef03cee29670b22ed04b9cebb1686fe26e1acd. The README calls its associated manuscript in preparation and states that the production refinement pipeline is not public. The ledger is an exact computational collection; peer-reviewed validation should not be inferred from its release.

`analyze_precursor_genome.py` independently counted:

| Quantity | Count |
|---|---:|
| Samples / unordered precursor pairs | 1,035 |
| Distinct precursors | 46 |
| Duplicate unordered pairs | 0 |
| XRD scans | 1,351 |
| Candidate refinements | 1,950 |
| Samples with actual temperature profiles | 981 |
| Null synthesis records | 40 |
| Records lacking hold temperature/time | 54 |
| Recorded 60 min holds | 750 |
| Recorded 240 min holds | 231 |
| Accepted / rejected / unreviewed candidate refinements | 1,161 / 55 / 734 |

The 1,035 pairs equal all unordered pairs of 46 precursors. Outcome categories are transformed 384, unreacted 369, completely reacted 143, partially reacted 113, and unspecified 26. Scans per sample are one for 798 samples, two for 171, three for 57, four for five, and five for four. **Repeated scans and alternative refinements are not repeated syntheses.**

The global workflow describes nominal 2 g dosing, a 60 min hold, manual recovery and 150 mg XRD sampling, but the per-sample fields include 231 four-hour holds. Recorded temperatures vary across pairs: 200°C 399, 300°C 56, 400°C 117, 500°C 171, 700°C 20, 800°C 18, 900°C 53, 1000°C 73, 1100°C 74; 54 are missing. One cannot compare pair identities as if they received a common thermal intervention.

The reported result must be resolved through the sample's `active_scan_index`, then that scan's `active_case_index`. It must not be selected by the first scan, lowest Rwp, rank one, or `is_active` alone: 237 samples have multiple scans flagged active. Quality scores across all candidate refinements are 1 for 769, 2 for 392, 3 for 53 and absent for 736. Rwp ranges from 0.94 to 55.86. These are candidate-fit diagnostics, not calibrated uncertainty intervals for the final phase fractions.

Quality flags that require resolving before mechanistic fitting include 19 negative XRD mass entries and two negative recovered-mass entries. For PG_0102 (Ag2O + Al(OH)3), the per-sample hold field is 240 min while a scan filename indicates 200°C and 60 min, and XRD sample mass is -49 mg. Such conflicts cannot be repaired by choosing whichever value suits an inference.

The collection is promising for prediction of first-contact endpoints and precursor-transformations under recorded conditions. It has no repeated-pair time series, no ternary or higher-order mixture test, and no varied geometry intervention for a fixed reaction. Therefore it does not independently establish pairwise kinetic composability or identify a physical rate operator. Manufacturer purity, melting points, thermal profiles, masses, and microscopy links are valuable inputs, but are not a substitute for measured evolving contact geometry.

## 3. Strong existing kinetic and spatial methods

### ReactCA (2025)

[Cellular automaton simulation of inorganic solid-state synthesis](https://doi.org/10.1021/acs.chemmater.4c02301); [author PDF](https://perssongroup.lbl.gov/papers/gallant_cellular-automaton-simulation_2024.pdf); [code](https://github.com/mcgalcode/rxn-ca).

ReactCA already implements three-dimensional local contacts, reactions between neighboring cells, melting-associated swaps and volume bookkeeping. It uses reaction free energies and a softplus onset based on Tammann's rule. It is thus incorrect to propose spatial contact evolution or a local reaction network as an absent organizing concept.

Its original demonstrations involve five recipes in BaTiO3, CaZrN2 and YMnO3 systems. Simulation steps are not independently calibrated physical time. Temperature-stage durations are adjusted in demonstrations. The phase list combines Materials Project entries with observed phases, excludes high-above-hull entries, and removes theoretical structures unless experimentally observed. This is a target-informed candidate inventory rather than blind prediction over all computed structures. Ordered intermediates may be overpredicted; amorphous and nonstoichiometric intermediates remain a limitation.

### Onsager transport extension (Nature Materials 2026)

[Ion correlations explain kinetic selectivity in diffusion-limited solid-state synthesis reactions](https://doi.org/10.1038/s41563-026-02596-5); [full primary XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13421335/fullTextXML); [data](https://doi.org/10.6084/m9.figshare.28207292.v3); [py-OATS](https://github.com/vir-k01/py-OATS).

This work is the essential comparator. It calculates multicomponent Onsager transport coefficients using molecular dynamics, includes ionic cross-correlations, combines them with chemical-potential gradients, derives an effective diffusion-growth coefficient, and inserts this information into ReactCA. The comparison spans four Ba–Ti–O precursor stoichiometries and improves phase-pathway agreement over self-diffusion-only and thermodynamic alternatives. The assumed growing interface is a liquidlike or amorphous composition corresponding to the product. Five MD trajectories per transport condition supply transport error bars, and substantial atomistic model preparation is explicitly incurred. This is a real mechanistic advance, not another generic fitted classifier.

However, its demonstrated macroscopic trajectories remain indexed by reaction steps. The Figure 4/5 source workbooks have 250 output points with x = 0, 2, 4, …, 498 and separately specified thermal-stage coordinates. They do not establish a seconds-valued macroscopic reaction clock. The model assumes a fixed particle radius 0.1 µm for all recipes, uses BaO to represent decomposed BaCO3, retains a thermodynamic/Tammann scoring heuristic, and introduces a scale factor s = 5 × 10^13 selected to place onset near 1000 K. The supplement says s need only be tuned once per chemical system, but this is calibration, not a parameter-free prediction of absolute onset.

**Additional decisive numerical limitation:** supplementary Table S3 reports maximum timewise mole fractions for Reaction 1 as s varies:

| s | Maximum BaTiO3 | Maximum Ba2TiO4 | Maximum BaTi2O5 | Maximum Ba4Ti13O30 |
|---:|---:|---:|---:|---:|
| 1 × 10^13 | 0.392 | 0.323 | 0.283 | 0.250 |
| 2 × 10^13 | 0.534 | 0.209 | 0.256 | 0.044 |
| 5 × 10^13 | 0.932 | 0.202 | 0.192 | 0.034 |
| 1 × 10^14 | 0.482 | 0.232 | 0.283 | 0.314 |

These columns are separate temporal maxima and should not be summed as one composition. A factor-two increase from the chosen s reduces peak BaTiO3 from 0.932 to 0.482 and substantially increases Ba4Ti13O30. The same change shifts reaction onset by about -100 K; decreasing s to 2 × 10^13 shifts it by about +100 K. Thus the scale factor changes pathway competition as well as clock placement. A remaining constructive target cannot merely fit another value of s.

The supplement also reports exclusion of poorly determined transport slopes and inability to reliably determine some 750 K cross-coefficients. The fixed oxidation-state treatment does not directly cover variable-valence or substantial-charge-transfer systems. These are explicit scope limits, not grounds for dismissing the demonstrated improvement.

## 4. What has and has not been selected

The Chen matched data establish that a useful thermodynamic precursor selector does not uniformly predict the better measured endpoint under a fixed protocol, and that route rankings can reverse with temperature. The new transport study establishes that correlated transport already explains meaningful kinetic selectivity. Together they rule out a simplistic proposed breakthrough of “add kinetics” or “track contacts.”

A stringent remaining target would predict complete phase-fraction trajectories in physical time using independently measured or calculated interface laws and measured geometry, with no recipe-specific rescaling when changing composition, heating profile or particle-size distribution. It would have to preserve stoichiometry, charge constraints and thermodynamic consistency, account for new interfaces created by reactions, and state when an inventory is incomplete. Phase-field and reaction-diffusion theory already address these constraints when their constitutive laws and inputs are supplied; simply recasting them is insufficient novelty. Relevant explicit predecessors include Huang et al., *Phase-field modeling of solid-state metathesis reactions with the charge neutrality constraint*, Computational Materials Science 221, 112080 (2023), as well as classical BaCO3–TiO2 kinetic studies and the new Onsager extension.

The present collections cannot decide whether a closed pairwise interface operator is sufficient. They lack interventions separating chemical constitutive kinetics from contact geometry, nucleation, transient melts, volatilization and inventory error. No achieved transferable operator or new route has been constructed in this audit. My recommendation is to retain physical-time transfer as a sharply defined unmet capability, but **reject a discovery claim or strong opportunity selection based on these endpoint data alone**.

## Reproduction

Run `python3 analyze_chen.py` and `python3 analyze_precursor_genome.py` from this directory or using their absolute paths. Both consume the retained downloaded sources. The Chen script uses the retained text extraction of the published supplement and Figure 4C source workbook. The Genome script reads the entire exact JSON ledger and counts records without silently collapsing alternative refinements. Raw originals, text extractions, matched tables and JSON summaries remain in this directory. `audit_manifest.json` records SHA-256 hashes and file sizes.


## Final source consistency note: comparison thresholds

The article main text says “at least 20% higher phase purity” for the 15 improved targets, while its Figure 4 caption explicitly defines green as >10% better purity, light green as within ±10%, and red as traditional >10% better. The deposited Figure 4C numerical data reproduce the caption’s absolute 10 percentage point classification (15 improved, 16 similar, 4 worse). A 20 percentage point cutoff instead gives 11 improved, 23 similar, and 1 worse. Thus cite the caption and deposited-data definition when reporting 15/16/4, and do not describe those counts as a verified 20 percentage point criterion. Strict signs give 19 wins, 13 losses, 3 ties. Mean predicted and traditional maximum scores are 0.5187996762 and 0.3683917373.
