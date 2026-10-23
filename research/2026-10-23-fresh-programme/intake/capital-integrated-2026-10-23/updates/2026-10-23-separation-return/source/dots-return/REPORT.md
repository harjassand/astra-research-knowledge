# Separation and return: 23 October 2026

## Decision
Replace the proposed unsupported hot pressure-selective return with an experimentally motivated **cooled bicarbonation / filtration / carbonate precipitation comparator**. This is an ordinary recovery mechanism, not an invented advantage. Do not reopen the thermochemical fit. A compatible chemical step has now been observed on metasilicate-containing mineral residues; the complete Fe/Si/Al/carbonate purge operation has not. Hot precipitation has no identified advantage over this comparator at present.

## New primary observations (not transplanted yields)
Zaitsev & Zhang, Canadian Metallurgical Quarterly (2026), DOI 10.1080/00084433.2026.2650964, sections 3.1.3–3.2.2 and Fig.14: caustic-leached petalite residue underwent atmospheric bicarbonation at 30 C, CO2 1 L/min, in a 1 L mixed vessel. After one hour, solution Li was 3.7 g/L; residual solid Li 0.139%; authors report approximately 94% extraction using an Al-normalized residue balance (Al leaching below 0.5%). Metasilicate XRD peaks disappeared. Mica extraction was below 90%. These are not final carbonate-return yields. Downstream decarbonation is explicitly outside the experimental study. The feed and iron phase are not our molten ore purge. This identifies a real aqueous Li/metasilicate separation pathway but not ferrite recovery, orthosilicate kinetics, colloidal silica removal or a closed melt loop.
Primary author full text: https://www.researchgate.net/publication/403780740_Metso_caustic_leach_process_alkaline_extraction_of_lithium_from_petalite_and_micaceous_aluminosilicates

The government-hosted 1970 Singmaster & Breyer evaluation of Atomics International's molten-carbonate process, pp.5-14 to 5-22, reports experimental fly-ash filter cake containing 65% melt. A proposed 50% cake value and commercial filter suitability were assumptions, not achieved scale-up. Carbonate recovery still required development. Different carbonate mixture, ash, temperature and chemistry prohibit importing 65% into our calculation. It is evidence against treating hot filtration as zero-entrainment separation, not a bound on modern equipment or this bath.
https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9100DXHE.TXT

Ramirez Velazquez et al., Journal of Crystal Growth 631 (2024)127625, DOI 10.1016/j.jcrysgro.2024.127625, recovered indexed experimental text describes bicarbonate reprecipitation at 80 C for 60 min. The original synthetic feed uses 4.4 M LiCl/NaOH solutions. Its extraction/precipitation yields cannot be multiplied into our dilute mixed-purge train. Direct full-page request returned403; indexed experimental section only was read. No claim to complete numerical results.

## Actual proposed comparison
Both arms process the SAME original ore feed, at the SAME iron product recovery and impurity inventory steady state, returning lithium as qualified carbonate. Both get ordinary bicarbonation, filtration/washing and mother-liquor recycle if useful.
A: any genuinely measured hot gangue partition, drain cake, cool only cake/entrained melt, aqueous recover, return carbonate; retain or separately recover iron.
B: cool a representative purge, aqueous recover carbonate/Li, separate gangue and iron-bearing residues, recover iron where feasible, return carbonate. Neither may count iron retained in discarded residue as recovered iron. Reintroducing an unseparated Fe/Si residue also reintroduces the rejected gangue.
No identified hot partition was acquired, so A currently lacks its decisive operation. B is a comparator construction, not yet a measured complete molten-ore recovery plant.

## Atom balance, not equilibrium assertion
Li4SiO4 + CO2 -> Li2CO3 + Li2SiO3.
Thus the familiar first carbonation step releases only half the silicate's lithium into carbonate. It does not regenerate all lithium.
Li2SiO3 + 2 CO2 + H2O -> 2 LiHCO3 + SiO2.
2 LiHCO3 -> Li2CO3 + CO2 + H2O.
Net: Li2SiO3 + CO2 -> Li2CO3 + SiO2. Hydration/gel water is additional inventory, not absent by notation.
These balances neither prove kinetics nor permit transferring 94% from the mineral residue. Even hypothetically granting 94% extraction of the remaining metasilicate and perfect recovery of all other Li gives 97% Si-associated Li extraction, not 97% final return. The saved feed then loses 0.927825 kg Li/t original Fe before aluminate, ferrite, entrainment, liquor purge and precipitation losses. The 1 kg/t ceiling is an expressly selected design target, NOT an economic threshold. The small residual allowance is a discriminator, not a claimed failure of real equipment.

## Governing measured observable
For element j, per mole of permanently removed Si, measure solid-bound inventory s_j, entrained-liquid inventory beta*c_j, and final usable return fractions r_sj,r_lj. Net loss:
L_j = S * [s_j*(1-r_sj) + beta*c_j*(1-r_lj)] + other purge/export_j + inventory drift_j.
S is removed Si per original feed Fe. beta is kg INITIAL-CARBONATE-EQUIVALENT liquid per mol Si, NOT actual mixed-melt mass fraction. The c_j must be measured on that same normalization. Actual wet-cake melt fraction cannot be converted without melt composition, reaction mass loss and cake phase assay.
Dissolution percentage is not r: r includes filtration, mother liquor, precipitation, drying and accepted bath return. Wash filtrate must have a destination. Measure phase-bound Fe separately from liquid Fe; tracer/liquid assay and drained wet/dry cake masses distinguish entrainment from genuine solid partition.

The numerical script evaluates only declared ideal silica-solid/nominal-liquid scenarios. Without Fe return, beta must be <=0.0670876 kg carbonate-equivalent/mol Si to meet the selected 1% original-Fe loss target. Without Li return, beta <=0.00477827 for the selected 1 kg Li/t Fe target. Neither is a measured separation specification. At illustrative beta=.11, liquid alone contains 23.0209 kg Li/t Fe and 1.63965% feed Fe; meeting those targets requires >95.656% Li return and >39.011% Fe return from that liquid, even before solid losses. These scenarios use no historical cake fraction as a transferable parameter.

## How an actual comparison is decided
Acquire matched net dry reusable carbonate, Fe product/return, permanently removed Si/Al, all retained liquid masses and compositions, water/CO2/reagent makeup, filtration pressure/throughput, heating/cooling duties with heat grades, electric loads and restored inventories. Normalize to identical accepted iron output and bath impurity ceiling, not only ore fed. Compare measured total resource vectors first; do not monetize with invented prices. For any explicitly chosen resource weighting, A beats B only if its avoided purge heating/recovery burden exceeds its added hot separation and material-loss burdens at the same return quality. A heat-duty lower bound for one arm cannot rank actual total energy. Ordinary B may also exploit heat recovery and aqueous recycle.

## Failed approaches preserved
1. 5.5-to-11 mol/kg binary saturation does not concentrate the dilute feed.
2. Hot carbonation alone cannot remove all silicate lithium.
3. Metasilicate extraction is not complete carbonate recovery, and it does not establish ferrite dissolution.
4. Historical measured entrainment is not this bath's entrainment; assigning 50% instead of measured65% is not experimental progress.
5. Battery leach precipitation results are not mixed molten-ore purge yields.
6. Preliminary scratch calculation converted hypothetical cake mass fraction into carbonate-equivalent liquid without a fully specified melt mass. Removed before reporting; final code uses explicit beta scenarios. No source measurement altered.

## Continuation
The next physically identified issue is not a new G fit: it is whether selective bicarbonation of the actual mixed solid can return lithium while rejecting gangue and preserving iron. Present sources do not identify that joint response. No long process trajectory is justified. Pursue primary phase-specific carbonate-recovery/entrainment observations, with a finite stop at compatibility rather than collecting generic high recovery percentages. If this response remains absent, retire the proposed hot-return advantage, retain ordinary recovery capital, and choose a distinct physical mechanism. Other assignment unchanged. No hardware, outreach or paid work performed.

## Additional observed mechanisms, 09:20 UTC
Yanase et al. J. Ceram. Soc. Japan118(2010)48–51, DOI10.2109/jcersj2.118.48, measured ferrite carbonation/phase evolution at 200–500 C. Table1 reports Li:Fe=.71 and .93 for differently prepared powders; Fig.6 shows carbonate plus maghemite after425 C treatment for one preparation, while another develops beta-prime ferrite. This is a real phase-sensitive chemical partition, not quantitative Li/Fe recovery from our purge. Neither powder may silently replace stoichiometric ferrite in the old Gibbs cycle. It motivates measuring phase composition after cooling, not choosing a favorable fit.
https://www.jstage.jst.go.jp/article/jcersj2/118/1373/118_1373_48/_pdf/-char/en

Wang/Licht/Licht, Separation and Purification Technology255(2021)117719, DOI10.1016/j.seppur.2020.117719, reports95% molten electrolyte extraction at750 C,493psi,30min from a carbon-nanotube/electrolyte composite. Its80/20 Li/Na carbonate and fibrous carbon matrix differ from our reactive silicate/iron solids. This is experimental evidence for hot mechanical return, but NOT evidence that dissolved gangue becomes filterable. Accessed indexed primary abstract/sections; full direct page403. It is a useful ordinary component comparator, not our invention.

Taken together, observations support component operations but do not discriminate the proposed mixed-bath hot-return advantage. I retire that advantage claim pending a joint phase/entrainment/return observation, not all molten-carbonate ironmaking. Rather than invent its missing partition, I have started a separate physically different attack on aqueous iron reduction and impurity-conditioned interfaces (aqueous_iron/). It avoids the lithium-carrier loop; it still pays water, caustic, gangue disposal and product separation. No claim that it beats molten electrolysis follows.
