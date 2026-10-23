# EB-on-resin PFOS: dose, site occupancy, and reuse challenge

**Status:** quantitative stress test of the second candidate in `OPERATION_AUDIT.md`. This is a source-based calculation and a proposed falsification experiment, not an EB-on-resin result.

## The source dose is a clean-water parent-loss benchmark

Trojanowicz et al. report a dose-normalized pseudo-first-order coefficient of `k_D = 0.0184 kGy^-1` for electron-beam treatment of `0.1 mg/L` PFOS in neutral, deaerated solution. Interpreting that coefficient as `C(D)/C(0) = exp(-k_D D)` gives

```text
D90 = ln(10)/k_D = 125.14 kGy.
```

This is an extrapolated 90% **parent disappearance** dose from the reported coefficient, not a separately reported D90, not 90% defluorination, and not a dose measured on resin. At water density `1 kg/L`, it corresponds to `125.14 kJ/kg water = 34.76 Wh/kg = 34.76 kWh/m^3` absorbed. Accelerator wall-plug electricity is higher and is not specified by this absorbed-dose calculation.

At the paper's `0.1 mg/L` feed, taking PFOS molar mass as `500.1 g/mol`, a litre contains `1.204e17` parent molecules. A 90% parent-loss extrapolation therefore represents `1.084e17` molecules lost per litre, or `8.66e11` parent molecules lost per absorbed joule (`7.21 MeV` absorbed per parent molecule lost). The energy denominator matters:

```text
per kg PFOS fed:     34.76 kWh/m^3 / 0.000100 kg/m^3 = 347,600 kWh/kg
per kg PFOS lost:    34.76 kWh/m^3 / 0.000090 kg/m^3 = 386,200 kWh/kg
```

The latter is the appropriate value when the denominator is PFOS actually removed. Neither quantity is total system energy or a mineralization efficiency.

There is no defensible thermodynamic or reaction-stoichiometric minimum dose in the cited result: it does not provide a product-specific electron count or a verified yield linking absorbed energy to fluoride release. The clean-water D90 above is the real source-based reference. Any “one productive hydrated electron per PFOS” ideal would require extra assumptions and should not be presented as a measured or universal lower bound.

## What the resin uptake data imply per exchange group

Wahman et al. tested single-use strong-base anion-exchange gel resins. For PSR2 Plus Cl, their 42-day PFOS kinetic run used `0.2 mg/L` PFOS, `5 mM` chloride and `25 mg` dry resin, reporting 99.995% liquid removal and maximum occupancy of `1.4%` of resin equivalents. Their PFOS isotherm dataset separately reached `3.4%` maximum occupancy for PSR2 Plus Cl. These are measured test occupancies, not saturation capacities and not evidence that the same load is attainable from a competitive real-water bed.

For a monovalent PFOS anion, occupancy `theta` is the number of PFOS molecules initially captured per exchange group. If (only as a transfer scenario) 90% of those parent molecules disappear at the clean-water D90, then

| PSR2 Plus Cl scenario | Initial PFOS/site | PFOS parent loss/site at 90% | Sites per parent lost |
|---|---:|---:|---:|
| Kinetic-run occupancy, `theta=0.014` | 0.014 | 0.0126 | 79.4 |
| Higher observed isotherm occupancy, `theta=0.034` | 0.034 | 0.0306 | 32.7 |

Thus 90% PFOS parent loss corresponds to transforming only 1.26% or 3.06% of the total site-equivalent count. This does **not** mean that 96.9–98.7% of resin sites survive: radiation can destroy exchange groups that never held PFOS.

Using PSR2 Plus Cl's independently measured dry anion-exchange capacity `Q=1.59 meq/g` (monovalent sites, hence `1.59 mmol/g`) converts these occupancies into an inferred loading ledger:

| Scenario | Inferred PFOS captured | Molecules/g dry resin | Molecules lost/g at 90% |
|---|---:|---:|---:|
| `theta=0.014` | 11.13 mg/g | `1.341e19` | `1.206e19` |
| `theta=0.034` | 27.04 mg/g | `3.256e19` | `2.930e19` |

The mg/g values are calculated as `Q theta M_PFOS`; they were not directly reported as uptake capacities in the kinetic paper. They describe the stated occupancy scenario, not a guaranteed column loading.

## Conditional energy advantage and the unmeasured penalty

For mass normalization, a mixture at `125.14 kGy` with one gram dry resin and `W` grams water per gram dry resin corresponds to `125.14(1+W) J` absorbed. The PFOS-loss entries below are conditional on resin-bound PFOS reaching the clean-water D90 response; that transfer is unmeasured for any wet resin fixture. The `W=0` column is only a dry-mass arithmetic endpoint, with no water-phase efficacy implied.

| Scenario | Lost PFOS molecules/J, dry-mass arithmetic (`W=0`) | Absorbed energy per kg PFOS lost (`W=0`, arithmetic only) | At illustrative `W=1` |
|---|---:|---:|---:|
| `theta=0.014` | `9.64e16` | 3.47 kWh/kg | 6.94 kWh/kg |
| `theta=0.034` | `2.34e17` | 1.43 kWh/kg | 2.86 kWh/kg |

The `W=0` column cannot represent water-mediated radiolysis efficacy. The `W=1` column is an illustrative wet-mass scenario, not a performance prediction. Smith et al. report resin water-retention capacity and bed-structure data, but those do not determine the water mass in an EB cassette. For any wet scenario, the calculation still assumes away the central unknown: that radiolysis in/around the exchanger directs the same fraction of absorbed energy to productive PFOS conversion despite resin, counterions, co-captured anions/NOM, oxygen, and any added donor. Cassette mass, fluid circulation, capture/regeneration, accelerator efficiency, and dose nonuniformity are also omitted.

The existence of an EB-on-resin dose-response, the required dose to achieve a specified fluoride yield, and the wall-plug energy per kg of PFOS destroyed are all **unknown**. The calculation above is only what a favorable unchanged-dose transfer would buy. If matrix scavenging or resin attack raises dose or lowers PFOS conversion, that concentration advantage can disappear.

## The resin is a competing target and a cycle-life risk

The quaternary-ammonium gel resin cannot be assumed to be an inert scaffold. At the two measured occupancies, there are about 71 and 29 exchange groups per PFOS molecule, respectively. A simple conditional competition bound makes the risk concrete: if every equivalent site is accessible and its effective hydrated-electron scavenging rate coefficient per site were `k_R`, while PFOS had coefficient `k_P`, then the site sink would be at least as fast as PFOS capture when

```text
k_R / k_P >= theta.
```

So PFOS would need `k_R/k_P < 1.4%` in the kinetic-run loading or `<3.4%` in the higher-occupancy scenario merely for PFOS to outcompete exchange sites as an electron sink, before counting polystyrene/DVB backbone, water, counterions, dissolved oxygen, nitrate, NOM, or other PFAS. This is a deliberately simplified well-mixed bound; actual radiation spur chemistry and local partitioning require measurement. It shows why bulk water rate constants alone cannot validate the interface.

A 2026 gamma-irradiation study of closely matched strong-base PS-DVB/quaternary-ammonium resins (gel Tulsion A-33 and macroporous Indion 810) reports dose-dependent NH4+ leaching, amine/organic-acid release, and exchange-capacity loss; the gel resin showed the largest exchange-capacity loss and related pH/conductivity changes. This establishes a real resin-damage pathway at class level. It does not give a transferable capacity-loss fraction for PSR2 at `125 kGy` EB, nor does it establish repeated-cycle selectivity. No capacity-retention claim is supported.

The candidate must currently be treated as **single-use loaded-resin irradiation with unknown spent-solid handling**, not as a regenerative cycle. Reuse becomes a testable claim only if after each EB cycle the same resin lot retains both (a) measured strong-base exchange capacity and (b) PFOS/co-PFAS breakthrough/selectivity under a defined feed matrix. Resin mass remaining is not an adequate proxy for either.

## Decisive matched control and stop rule

Run a small, sealed, dose-mapped factorial at identical initial total F and total PFOS, matched liquid/resin mass and gas condition:

1. PFOS-loaded PSR2 Plus Cl-like resin, EB on/off.
2. PFOS in solution without resin, same PFOS concentration and EB dose.
3. Unloaded resin plus PFOS-free matrix, EB on/off (resin-only damage blank).
4. PFOS spiked into the external liquid with unloaded resin, at the same total PFOS and same EB dose (a preparation-order control). It separates initially bound from initially free PFOS only if resin/liquid partitioning at beam-on and transfer during irradiation are independently measured; otherwise the PFOS may adsorb before or during EB.
5. A non-ionic PS-DVB bead control if available, to separate quaternary-ammonium damage from backbone/water effects.

Use source-matched neutral deaerated conditions first; test the aerated plus 10 mM 2-propanol condition only as a separate factor, because the source result is solution chemistry. At every cycle measure parent PFOS and short-chain PFAS, inorganic fluoride, total/extractable organic fluorine across liquid/resin/rinses/filters/headspace, and sulfur products. Before and after each cycle measure strong-base exchange capacity (chloride-form titration or validated equivalent), PFOS/co-PFAS uptake and breakthrough, resin-derived NH4+, amines, TOC/COD, swelling and visible cracking. Include dosimetry at the liquid and resin locations.

Interpretation:

- **Evidence consistent with encounter-enabled cleavage:** preloaded resin gives more fluoride per absorbed joule and closes a larger fraction of initial F to inorganic fluoride than matched controls, with the initial PFOS partitioning established. This supports a process benefit; it does not alone prove the molecular attack pathway.
- **Resin damage:** substantial AEC loss or NH4+/amine/TOC release means the resin is not an inert or demonstrably reusable scaffold. Resin damage can coexist with direct PFOS reaction, so these measurements determine the material/reuse burden rather than refute interfacial PFOS attack.
- **No demonstrated process advantage:** if loaded resin performs no better than the solution-only condition, the capture step has not shown a treatment benefit under that fixture. That result does not by itself disprove an interfacial reaction mechanism.
- **No cleavage evidence:** parent loss without inorganic-fluoride/total-F closure remains transformation or unaccounted F, not destruction.
- **Reuse failure:** capacity/selectivity degrades after one or more cycles even if the bead mass remains. In that case, include fresh-resin consumption and spent-resin disposal in the process burden; do not claim regeneration.

**Stop rule:** stop the capture-plus-EB process lead if the loaded resin does not improve closed fluoride production per absorbed joule over the matched solution-only condition, or if measured exchange-capacity loss prevents a useful second capture cycle and the single-use material/energy balance fails the intended application. These are process-value criteria, not mechanism-disproof criteria.

## References used in this quantitative follow-up

1. Trojanowicz et al. (2020), “Application of ionizing radiation in decomposition of perfluorooctane sulfonate (PFOS) in aqueous solutions,” *Chemical Engineering Journal* 379, 122303. [DOI: 10.1016/j.cej.2019.122303](https://doi.org/10.1016/j.cej.2019.122303). Source for solution EB coefficient and chemical conditions; no resin-bound result.
2. Wahman et al. (2023), “Strong Base Anion Exchange Selectivity of Nine Perfluoroalkyl Chemicals Relevant to Drinking Water,” *ACS ES&T Water* 3, 3967–3979. [DOI: 10.1021/acsestwater.3c00396](https://doi.org/10.1021/acsestwater.3c00396). Source for PSR2 Plus Cl PFOS test occupancies/removal; no EB data.
3. Smith et al. (2023), “Anion Exchange Resin and Inorganic Anion Parameter Determination for Model Validation and Evaluation of Unintended Consequences during PFAS Treatment,” *ACS ES&T Water*. [PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC10078613/). Source for PSR2 Plus Cl `Q_m=1.59 meq/g`; used only to convert occupancy into inferred mg/g.
4. “Influence of microstructure on the radiolytic stability of anionic resins,” *Radiation Physics and Chemistry* 241 (2026), 113558. [DOI: 10.1016/j.radphyschem.2025.113558](https://doi.org/10.1016/j.radphyschem.2025.113558). One decisive, class-level gamma-resin-damage source; not an EB/PSR2 dose-response.
