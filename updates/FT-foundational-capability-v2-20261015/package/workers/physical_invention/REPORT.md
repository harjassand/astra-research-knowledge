# Transient isotope separation: a real operation, but no new qualified capability

Status: **NOT_ACHIEVED**. Independent physical-operation investigation, 15 October 2026. No laboratory experiment, new material simulation, purchase, or outside communication was performed. Both supplied pasted-text attachments were read completely. Their missing packages were not used as premises or treated as a research task. No sibling research output was consulted during selection.

The selected operation was a sequence of **load, close, selectively purge, and harvest** in one hydrogen-isotope adsorbent. It attacks molecular separation rather than passive mechanical de-trapping. Stable-isotope supply supports scientific experiments, chemical analysis, and semiconductor processing. It would not itself establish energy abundance: useful deuterium separation and an economical fusion energy system are different capabilities.

The selection had an experimental reason. Real frameworks already combine temperature-dependent access, isotope discrimination, storage, and release. This avoids inventing a favorable response matrix. The investigation nevertheless found two decisive limits: the broad sequence is established prior art, and the proposed extra purification pulse lacks the mixed-feed escape contrast needed for useful recovery. A short room-temperature graphene alternative also failed qualification.

## One obtainable apparatus and the proposed operation

The concrete substrate is a packed **Cu-ZIF-gis** bed with temperature control, inlet isolation, pressure control, and separately collected outlet fractions. The candidate sequence was:

1. Admit a declared H2/D2 mixture while pores are accessible.
2. Cool and isolate the bed to trap the loaded molecules.
3. Open a selected release window and discard an H-rich fraction.
4. Release the retained D-rich fraction into a product receiver and restore the initial state.

The apparatus does not require an arbitrary atom clamp, an assumed hidden actuator, or a material assembled from different papers. But the useful properties must hold **for this sequence and this feed**. Storage and release alone do not establish selective purification.

The primary Cu-ZIF-gis paper reports 1:1 H2/D2 loading for 60 minutes, evacuation, cooling to 18 K, and a 6 K/min release ramp to 240 K. At 120 K and 2 bar its TDS selectivity is approximately 1.7; Fig. 3d gives roughly 0.45 mmol D2/g by visual reading. Separate breakthrough measurements used 1.832 g of pellets and Ne/H2/D2 = 95.11/2.45/2.45 vol%, 3.68 cc/min: dynamic selectivities were 1.5 at 115 K and 1.3 at 159 K. Room-temperature dosing followed by cold trapping and thermal release was already demonstrated. These are published measurements, not Astra results. [Jung et al., 2025](https://www.nature.com/articles/s41467-025-56649-5)

**Novelty decision:** warm loading, temporary gate closure, and later release cannot be claimed as a new invention. The only remaining proposal was whether a separately harvested purification window improves the complete recovery/energy frontier. The available measurements do not establish this. No additional hypothetical waveform should be optimized without measuring that gate.

## The coupled requirement that an extra purge must satisfy

Let `n_H(0)` and `n_D(0)` be the amounts retained immediately before a purge. Count molecules of the same declared species; this two-species treatment excludes chemical conversion and isotope exchange. During a one-way, feed-free purge with no re-adsorption, define cumulative effective escape exposures

\[
\Lambda_i=-\log[n_i(t)/n_i(0)],\qquad i\in\{H,D\}.
\]

The odds gain and desired-isotope retention are then exactly

\[
A=\frac{n_D(t)/n_H(t)}{n_D(0)/n_H(0)}
 =e^{\Lambda_H-\Lambda_D},
\qquad R_D=e^{-\Lambda_D}.
\]

For a target gain `A > 1`, positive desired-isotope loss, and retention at least `0 < R < 1`, a necessary condition is

\[
\boxed{\frac{\Lambda_H}{\Lambda_D}
\ge 1+\frac{\log A}{-\log R}.}
\]

This is a screening identity, not a new fundamental theorem or a fitted material model. If every allowed interval has an effective unwanted/desired escape ratio at most `r_max`, splitting the purge into multiple windows cannot evade

\[
A\le R_D^{-(r_{\max}-1)}.
\]

Zero desired-isotope loss with positive unwanted-isotope escape is the ideal infinite-ratio limit; no finite ratio is assigned to it.

| Retain captured D | Escape-exposure ratio required to double odds | Required for tenfold odds |
|---|---:|---:|
| 99% | 69.97 | 230.11 |
| 95% | 14.51 | 45.89 |
| 90% | 7.58 | 22.85 |
| 80% | 4.11 | 11.32 |

For the 1.7-odds starting example, doubling odds yields only `3.4/(1+3.4) = 77.3%` D2 in the retained two-species fraction. Ninety-percent retention here concerns **already captured D2**, not 90% recovery from the inlet. Total feed recovery additionally includes loading, dead-volume removal, harvesting, and any recycle losses.

In a reversible dilute-site kinetic model, detailed balance additionally couples entry and escape:

\[
K_i=k_{\mathrm{in},i}/k_{\mathrm{out},i},
\qquad
\frac{k_{\mathrm{out},H}}{k_{\mathrm{out},D}}
=\frac{K_D/K_H}{k_{\mathrm{in},D}/k_{\mathrm{in},H}}.
\]

Thus faster desired-species entry and stronger desired-species binding are not independent multiplicative gifts. This simple model is **not** assigned to the hysteretic Cu framework, and no source-derived rate is inferred from it. It explains why the actual mixed-feed release trace is indispensable. Localized single-gas mobility, an equilibrium affinity, or an entry selectivity does not supply the required escape exposures.

If HD forms or molecules re-adsorb, the simple purge calculation is inapplicable. The experiment must then track atomic isotope balances and the actual product fractions directly. Adding an unobserved exchange reaction to restore a favorable answer is not permitted.

## Strong existing comparators

The competitors already demonstrate temporary-state operations. Published numbers below have different feeds and conditions; they are evidence of competing capabilities, **not** a matched ranking.

| Comparator | Primary evidence | Consequence for the candidate |
|---|---|---|
| Isotope-triggered framework opening | DUT-8(Ni): mixed-feed selectivity 11.6 and D2 uptake 9.44 mmol/g at 23.3 K; D2 opens the framework while H2 and HD do not. [Bondorf et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9007508/) | Selective temporary pore states and narrow thermal release are prior art. Its cold duty must still be charged. |
| A more selective flexible framework | Mn-triazolate: reported selectivity 32.5 for 1:1 H2/D2 at 60 K, with a 10-minute exposure. A 5:95 D2:H2 experiment also showed enrichment. [Primary 2025 paper](https://d-nb.info/1370824327/34) | High selectivity is already measured elsewhere. A 5% molecular D2 feed is far above natural isotope abundance. |
| Coupled pressure/temperature cycling | An experimental dual-column process reports enrichment factor 19.7, recovery above 99%, and 560 standard L/day for a 3.63 at.% D feed. [Experimental verification, 2021](https://doi.org/10.1016/j.fusengdes.2021.112726) | A comparator must charge complete recovery and treatment capacity; isolated uptake selectivity is insufficient. |
| Palladium thermal-cycling absorption | A 12 m experimental column operated for over 200 cycles and separated a 25% D feed into streams each above 99.7% purity. [Heung et al., 2009](https://doi.org/10.13182/FST09-29) | Recoverable purified streams are an established capability. Avoid comparing a single proposed pulse against an untreated vessel. |
| Room-temperature hydron membranes | A graphene/Nafion electrolyzer showed improved isotope separation but a 12% cell-efficiency decrease at 75°C. [Park et al., 2024](https://doi.org/10.1016/j.cej.2024.155328) | Avoid assuming that refrigeration is unavoidable. Membrane resistance, electrolysis work, and product form must be included. |

A recent theory also explicitly studies mass-selective transport through fluctuating nanopores, including proposed external modulation. It is not a laboratory demonstration of a new pulsed separator. It removes a broad priority claim for deliberately exploiting a molecular gate's timescale. [Tang et al., 2026](https://www.nature.com/articles/s41467-026-75540-5)

## Full-cycle cost and scale

Use a common contract: the same declared H2/HD/D2 composition, feed pressure and temperature, impurities, final purity, isotope recovery, output pressure, and delivered amount. For the first comparison, a prepared 1:1 H2/D2 gas feed is legitimate **only if every method receives that feed and its preparation cost is stated separately**. A natural-water capability requires a different experiment.

For an atomic D fraction `x` after randomized molecular pairing,

\[
y_{H_2}=(1-x)^2,\quad y_{HD}=2x(1-x),\quad y_{D_2}=x^2.
\]

At the explicitly illustrative `x = 1.5\times10^{-4}`, HD is about `3\times10^{-4}` and D2 only `2.25\times10^{-8}` of molecules. A binary equimolar H2/D2 experiment does not identify the dominant natural-feed carrier. These are combinatorial calculations, not a statement that a particular feed is equilibrated.

The required accounting is

\[
e_D=\frac{W_{\rm feed\ prep}+W_{\rm refrigeration}
+W_{\rm pumping}+W_{\rm compression}+W_{\rm heating}
+W_{\rm controls}+W_{\rm analysis}-W_{\rm recovered}}
{n_{D,\rm delivered}}.
\]

Capital amortization, adsorbent synthesis and replacement, solvent recovery, activation, vessel mass, insulation, heat exchangers, downtime, carrier-gas recovery, calibration, and losses enter cost per delivered isotope as well. A useful annualized comparison cannot be calculated from the acquired evidence: measured cycle energy, receiver yield, reset time, and long-run mixture stability are absent.

Refrigeration is an actual thermodynamic charge. At ambient `T0 = 298 K`, removing heat `Q` isothermally at temperature `T` requires at least

\[
W_{\min}=Q(T_0/T-1).
\]

The ideal work per joule of heat is 1.48 at 120 K, 2.87 at 77 K, and 15.56 at 18 K; actual apparatus requires more. For a changing temperature, integrate the heat load at its actual temperature. Cold supplied by LNG remains a consumed exergy resource with an alternative use.

The 18–240 K ramp alone takes 37 minutes. Adding the reported 60-minute exposure gives 97 minutes before cooling, evacuation and handling. Dividing the approximate 0.45 mmol/g retained D2 capacity by that interval gives 0.278 mmol/g/hour. This is **protocol arithmetic**, not measured production throughput, a universal throughput upper bound, or a reason to require 18 K in every industrial design. A faster production cycle could differ, but then its purity, working capacity and release must be measured; they cannot be inherited from the readout sequence.

Higher uptake at a warmer loading state, stronger selectivity at a colder state, and a fast release rate from a third experiment cannot be multiplied into one device result. Nor can years of air stability replace lifetime under repeated mixed-gas thermal cycles.

## One decisive falsifier, then stop or proceed

The only justified next result for this proposed extra purge is a **mass-balanced mixed-feed fractional-release curve on the same packed bed**. It must include all released, retained, lost, and blank-volume gas; HD where present; actual bed temperature rather than only a remote sensor; and final receiver collection rather than an ion-current peak alone.

Predeclare a chosen continuation threshold: twice the initial retained isotope odds while retaining at least 90% of the captured desired isotope. A claimed release window fails if calibrated collected fractions cannot achieve this after uncertainties and receiver losses. This falsifies that measured purge regime, not every possible isotope separator. If a bound on all measured accessible windows gives an escape ratio below 7.58, no rearrangement of those windows fixes the two-species one-way-purge problem.

A passing trace would justify testing complete-cycle energy and feed recovery against the strongest cycling comparator at the same product contract. It would not establish priority or a transformative technology. No run is recommended on the strength of synthetic rates; no new waveform is developed here in place of the missing exchange/escape measurement.

## Short qualification of a different room-temperature state sequence

A second candidate was an electrochemical **isotope capture-and-release electrode**: selectively deuterate graphene, remove weakly retained H, then release retained D into another reservoir. The relevant paper demonstrates reversible hydrogenation and deuteration, an isotope-dependent potential shift, and roughly `10^14` adsorbed hydrons/cm2. Its device has a 15 µm exposed hole; hydrogen evolution competes with storage. Crucially, its isotope substitution tests use separate proton/deuteron electrolytes, not a mixed-feed separator. [Soong et al., 2025](https://www.nature.com/articles/s41467-025-65771-3)

Capacity arithmetic is decisive for what may presently be claimed. At that density, the exposed microdevice holds only `2.93\times10^-16` mol of hydrons, or 0.59 femtogram if every site carries D. Even one square metre of active surface stores at most 1.66 micromol, or 3.34 micrograms of D, at the stated density. These upper-bound calculations grant neither all-D occupation in a mixture nor collection into a product stream.

Electrical switching can be technologically valuable for memory, but that is already the source's application. It supplies no measured mixture purity, reservoir exchange, or bulk isotope turnover. Higher surface area and faster hypothetical fluid switching would introduce a new unqualified apparatus. **Stop this separation proposal at qualification.**

## Disposition

Retain the explicit purity–retention screening identity and the source-linked capacity calculations as negative research results. The isotope-sequence investigation found a physically real and interesting operation, already developed by others, and identified what additional purge would have to demonstrate. It did not discover a new qualified physical capability or establish a lower-cost isotope technology. No further conditional cycle modeling is warranted without the actual mixed-feed release measurement.

The supplied hBN and adjoint attachments informed the requirement that effects and access coexist in one apparatus. No favorable coefficient, missing artifact, or claimed earlier success was imported into this route.
