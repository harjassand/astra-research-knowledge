# Evidence audit and the strongest existing constructions

The [selection](README.md) rests on acquired primary numerical sources and scoped reanalyses. The [final report](package/output/selection/reactive_interface_selection.pdf) and [materials audit](package/opportunity_materials/materials_evidence_audit.md) retain the governing source versions, uncertainty and reservations.

## First-product ranking: a bounded residual failure

The Szymanski study supplies a 37-reaction comparison and a phase-fraction workbook with 26 experiments and 1,318 temperature rows. The [recorded reanalysis](package/opportunity_root/thermodynamic_audit.json) finds 23/37 correct first-product predictions for the largest compositionally unconstrained thermodynamic driving force.

| Cohort | Matches |
|---|---:|
| All published cases | 23/37 |
| Energy margin at least 60 meV/atom | 14/14 |
| Margin below 60 meV/atom | 9/23 |
| Comparable cases after four exclusions | 23/33 |
| Comparable cases below 60 meV/atom | 9/19 |

Three mismatches have observed products absent from the ranked stable-phase inventory; another has conflicting energy labels between table and main text. Excluding all four leaves ten disagreements. The 60 meV threshold is selected in-sample, not an independently validated universal boundary. Energies are evaluated at observed onset, so the calculation does not predict onset time. Close rankings remain sensitive to free-energy error.

Requiring two consecutive observations above 1%, 2% or 5% fitted fraction recovers the published first-phase identity in all 26 sheets; 10% recovers 24/26. This is a sensitivity diagnostic, not replicate-based uncertainty or proof of a unique kinetic explanation. Onset temperatures are less stable than phase identity. See [onset results](package/opportunity_root/onset_sensitivity_by_reaction.json) and [original workbook](package/opportunity_root/phase_data/adp3309_data_s1.xlsx).

## Stronger precursor selection and temperature dependence

The Chen study reports 224 syntheses targeting 35 compounds. The package recovers 202 numerical route-temperature rows and 100 matched target/temperature comparisons; it does not pretend those reconcile all 224 runs. The [matched summary](package/opportunity_materials/chen_reanalysis_summary.json) has 40 improvements above ten percentage points, 44 within plus/minus ten and 16 worse by more than ten; mean selected-route advantage is 10.51 percentage points.

For LiMgPO4, eight-hour measurements give selected/traditional diffraction target scores `.70/.29` at 800 C and `.60/.75` at 900 C. The advantage changes from `+.41` to `-.15`. These are diffraction scores, not mass purity or independent randomized replicates. The four cells have no matched synthesis replicates, so no invented significance interval is attached. The stronger method's real aggregate improvement remains credited.

The source article's prose and figure caption use different improvement thresholds. Deposited data reproduce the familiar 15/16/4 classification at an absolute ten-point cutoff, not the prose's twenty-point criterion. Other headline/supplement differences remain recorded rather than silently repaired. See [matched rows](package/opportunity_materials/chen_matched_temperatures.csv) and the [audit](package/opportunity_materials/materials_evidence_audit.md).

## Existing kinetics already rule out the easy contribution

The 2026 correlated-ion-transport construction couples microscopic Onsager transport, chemical-potential forces, diffusion-limited growth and spatial ReactCA reactions. Adding those ingredients or drawing contact/reaction graphs is not a missing invention. ARROWS3 already reuses learned pairwise intermediates through feedback; reaction-diffusion and phase-field theory already couple constitutive inputs.

The source's macroscopic trajectories are indexed by reaction steps and use a chemical-system scale `s` to place onset. Its sensitivity table gives maximum timewise BaTiO3 mole fractions `.392,.534,.932,.482` at `s=1e13,2e13,5e13,1e14`, respectively. These are separate temporal maxima, not final yields. The scale changes pathway competition, not merely axis labels. This motivates the unitful assembly question while preserving the transport explanation's earned selectivity result.

The [local shell diagnostic](package/opportunity_root/clock_diagnostic.json) uses `dh/dt=K_D/h`, hence `h^2=2K_D t` and `t_shell=r_0^2/(2K_D)`. At assumed radius `.1 micrometre` and the reported 1000 K coefficients, conditional times range from about 30 microseconds to `.95 milliseconds`; BaTiO3 is about 41 microseconds. This is an exact calculation **conditional on an already active homogeneous layer and uninterrupted supply**, not an observed bulk conversion time or a complete simulator prediction. It locates a missing interface/geometry/nucleation clock rather than demonstrating anomalous new physics.

## Collection size and rejected anomalies do not establish closure

The [Precursor Genome summary](package/opportunity_materials/precursor_genome_summary.json) covers all 1,035 unordered pairs of 46 precursors, 1,351 scans and 1,950 candidate refinements. There are 981 actual temperature profiles, 54 missing hold time/temperature entries, 750 one-hour and 231 four-hour holds, and no duplicate unordered pairs. Different pairs used different temperatures. Rescans/refinements are not independent repeated syntheses. This is valuable pair-outcome coverage, not 1,035 kinetic trajectories or higher-order composition tests. Missing/negative metadata records remain unchanged in the raw ledger.

An apparently indefinite mean Onsager matrix was counterchecked against its archived uncertainty: a physically admissible matrix lies within all componentwise one-standard-deviation intervals. That is not a joint confidence claim, but removes the proposed basis for a new-physics anomaly. [Countercheck note](package/opportunity_dynamics/onsager_outlier_note.md) and [result](package/opportunity_dynamics/onsager_outlier_countercheck.json) are preserved.

The granular-memory and dense-electrolyte leads were rejected because strong existing explanations already describe their main phenomena. Electronic/redox coupling is established irreversible-thermodynamics machinery, not a new principle merely because one recent simulator excludes changing oxidation states. The archived notes retain these useful failures and their conditions.
