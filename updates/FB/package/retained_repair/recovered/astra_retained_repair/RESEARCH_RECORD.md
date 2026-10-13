# ASTRA: retained bond repair — qualification record

Date: 13 October 2026.

## Status

No genuinely new, material-qualified physical operation was established in this investigation. The surviving question is whether a mass-conserving lattice bond repair can preserve and release an electronic excitation, allowing that excitation to initiate another repair. Neither the reaction pathway nor the outgoing mobile excitation has been acquired for hBN. Generic excitation-preserving chemical chains are prior art, not an Astra invention.

This packet contains a literature-linked qualification analysis and executable arithmetic. It contains no atomistic trajectories, electronic-structure calculation, experimental measurements, independently verified new theorem, or demonstrated manufacturing advantage. The numerical assertions in the Python script check arithmetic only.

## Endpoint and hypothesis

Endpoint: return an identified, isolated topological bond defect to the correct lattice connectivity without supplying or removing atoms. This deliberately differs from vacancy filling, oxygen passivation, net ionic pumping, and fluorescence quenching.

Hypothesis: D + X -> D* -> H + X', where D is an incorrect local bond topology, H is the corrected topology, and X' is a transferable surviving excitation. The technologically significant question is not whether light changes a defect, but whether a complete lattice-repair event preserves a usable excitation and remains selective against damage.

Triplet spin can motivate investigating a spin-conserving reaction surface. Spin conservation does not ensure excitation survival, mobility, favourable bond rearrangement, or resistance to ionization. All these outcomes must arise from the same electronic structure and nuclear dynamics.

## Prior-art exclusions

- Recombination-enhanced defect annealing is established: Lang and Kimerling, Physical Review Letters 33, 489 (1974), DOI 10.1103/PhysRevLett.33.489.
- Room-temperature ionization-assisted annealing in crystalline silicon was reported by Mihai et al., Acta Materialia 261, 119379 (2023), DOI 10.1016/j.actamat.2023.119379. Room-temperature recovery alone cannot identify a new mechanism.
- Excitation-preserving triplet quantum chains in Dewar-benzene derivatives are established. Rivera et al., Chemical Science 14, 5802–5810 (2023), DOI 10.1039/D3SC01074K, report about 100–120 products per absorbed photon in submicron specimens and approximately 300 in a qualitative microcrystalline-powder comparison. Those gains cannot be assigned to hBN.
- Recent post-growth carbon-nanotube repair uses alternating oxidant and carbon supply: Shen et al., Small Methods (2026), DOI 10.1002/smtd.202502417. This is a relevant capability benchmark, not a matched hBN process.

## hBN: one theoretical model, not an assembled material

Hamdi et al., npj Computational Materials 6, 178 (2020), DOI 10.1038/s41524-020-00451-y, calculate a neutral Stone–Wales defect with B–B and N–N bonds. Their model gives formation energy 7.2 eV, vertical singlet excitation 4.53 eV, and excited-state relaxation of 0.47 eV. It also predicts radiative lifetime 2.4 ns and singlet-to-triplet intersystem crossing of order 100/s.

These are theoretical predictions. The relaxed excited geometry remains a defect; stretching the incorrect bonds is not a computed healing path. The 0.47 eV relaxation is not a repair barrier. The formation energy is not an excited-state activation barrier. A fully cooled, healed ground-state structure would pay the formation energy to recreate the same isolated defect, but this does not establish operational lifetime under further illumination, irradiation, chemical exposure, or other failure channels.

A critical experimental correction is supplied by Plo et al., Physical Review X 15, 021045 (8 May 2025), DOI 10.1103/PhysRevX.15.021045: isotope substitution and stacking/pressure tests identify the studied ubiquitous ultraviolet centre as a carbon dimer. The common approximately 4.1 eV optical signal therefore cannot establish that an addressed site is a Stone–Wales defect. This does not prove Stone–Wales defects cannot emit near that energy.

## Conditional calculations

For the published relaxed optical cycle, ignoring additional loss,

eta_T = k_ISC / (k_ISC + 1/tau_rad) = 2.399999424e-7.

Thus the mean productive absorbed-photon count per triplet loading is approximately 4.17 million. At 4.53 eV this is 3.024 pJ of absorbed optical energy. It is not a wall-energy estimate and is not a universal bound on other preparation mechanisms.

If G denotes mean retained repairs per loaded triplet, the absorbed-photon quantum yield is eta_T G in this model. Exceeding one retained repair per absorbed photon requires G > 4.17 million. No hBN value of G is known here. Low quantum yield alone does not prove unacceptable manufacturing energy or low throughput.

For a no-chain, terminal competing-hazard model, write r = eta_T y, where y is the unknown repair probability conditional on triplet loading, and d is the damage probability per optical event. After Poisson exposure M:

P_repair(M) = r/(r+d) * [1 - exp(-(r+d) M)].

A 99% terminal yield requires d <= r/99. Even the optimistic y=1 ceiling gives d <= 2.424e-9 per event. This is a qualification threshold, not a prediction of damage. It also neglects subsequent damage to already repaired sites.

For independent, unsaturated, damage-free sites without recycling, a fixed absorption cross section sigma_D yields:

F_99 = [h nu * ln(100)] / [sigma_D eta_T y]
     = 1.392654e-11 J / [sigma_D(cm^2) * y],

where F_99 is incident optical fluence in J/cm^2. The absorption cross section and y remain unacquired; no favourable values have been substituted.

The script also calculates exact one-sided 95% binomial upper bounds following zero successes in independently verified trials: 0.0950 for 30 trials, 0.00994 for 300, and 0.000998 for 3000. A trial must be a verified preparation, not an incident photon of unknown absorption or branching.

## Decisive acquisition

Compute or measure the connected reaction sequence from the actual identified defect excitation to corrected lattice plus a mobile surviving excitation. Mapping only the ground-state healing path, a relaxed emitting state, or a fixed charge-state barrier does not answer that question.

The calculation must allow competing bond reconstructions, spin changes, internal conversion, ionization and atom loss. Multireference crossings deserve explicit treatment: excited-state Stone–Wales studies in pyrene show that electronic excitation can leave a large reaction barrier rather than automatically remove it (DOI 10.1021/jp306894x). This is a methodological caution, not a quantitative hBN barrier.

An experiment must jointly demonstrate structural repair, retention after excitation removal, and an outgoing excitation capable of another repair. PL loss alone is insufficient. Run light-only, probe-only, dark, absorbed-energy-matched, temperature-matched, and controlled-atmosphere arms. Use an independently identified starting structure, and keep the structural probe off during the actuation window where possible.

Electron microscopy is not an inert observer. Bui et al., Small 19, 2301926 (2023), DOI 10.1002/smll.202301926, measure hBN vacancy creation under 50–90 keV electrons. Javed et al., Nature Communications 17, 9620 (2026), DOI 10.1038/s41467-026-76612-2, show that very small oxygen partial pressures change beam-induced pore growth and shape. Neither lower beam energy nor a generic vacuum specification guarantees absence of damage or chemistry.

## Outstanding obligations

1. Structural identification and state preparation of the same defect population.
2. A verified repair path and competitive nonadiabatic branching probability.
3. Survival and mobility of the outgoing excitation.
4. Measured absorption, spatial range, repair/damage selectivity and retained lifetime.
5. A matched existing process for the same hBN endpoint and a causal functional benefit.
6. Whole-process wall energy, treatment area per time, usable yield and readout cost.

Do not promote this record as a discovered mechanism or optimize an hBN manufacturing device from it. The specific optical implementation remains unqualified. The source correction and quantitative qualification conditions are the completed outputs.
