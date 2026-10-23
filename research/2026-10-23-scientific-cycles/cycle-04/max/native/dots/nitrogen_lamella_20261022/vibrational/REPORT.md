# Vibrational admissibility of the 400 µm lamella

## Scientific decision

The **one-temperature microsecond trajectory is not certified as internal thermal equilibration**, especially not to its roughly 6 K transient margin below 1700 K. It is a useful equilibrium-thermodynamics baseline, not an exclusion of an actual rapid translational-temperature drop. This check does **not** prove the heat path impossible or produce a new temperature trajectory.

Atomic oxygen must be included. Its measured effectiveness is large and removes the misleading inference that pure-N2 millisecond relaxation is a mixture bound. NO, present at about 2.95 mol%, also supplies potentially important vibration–vibration (VV) transfer. Including both still gives no convincing small relaxation parameter during the steep part of this saved trajectory.

The parent's fully relaxed endpoint energy certificate is independent of this issue: freezing vibrational energy cannot remove the heat that must ultimately be exported before reset. Nothing here changes the ≥53.995 kJ/kg-fresh necessary heat-export result under its stated composition and radical limits.

## Primary measurements and applicability

1. **N2–O, the most directly applicable result.** Eckstrom (1973), DOI [10.1063/1.1680410](https://doi.org/10.1063/1.1680410), studied shock-heated nitrogen over **1200–3000 K** using a CO infrared tracer. Reported pτ varies from **0.8 to 2 atm·µs**, with **±50% uncertainty**. The broad whole-range envelope 0.4–3 atm·µs is used here without pretending it is a temperature-resolved confidence band. The original manuscript also appears as Appendix B of [SRI report AD-757050](https://citeseerx.ist.psu.edu/document?doi=9b6592e5fd5812ba0a48377e14b940e9228385e2&repid=rep1&type=pdf). Its indexed original-report abstract was retrieved; downloading that archived PDF returned 404 and the publisher returned 403. The values are not invented from a plotted curve. This interval covers the cooling hot gas, but not the initially 300 K cold gas.

2. **Pure N2.** Millikan and White (1963), DOI [10.1063/1.1734039](https://doi.org/10.1063/1.1734039), report, for **1900–5400 K**, log10(pτ/[atm·s]) = 102 T^(-1/3) − 11.24. It gives 121.6 µs at 2700 K and 1 atm. The 13 ms hot residence spans about 107 such times; a thermal hot inlet is credible if the gas actually spends that residence near 2700 K. At 1700 K this particular measured fit is an extrapolation. It is never used as a mixture bound.

3. **N2–O2 must not be represented only by molecular VT.** White (1968), DOI [10.1063/1.1670074](https://doi.org/10.1063/1.1670074), measured 5–50% O2 mixtures. Its published abstract reports a VV transition probability increasing from 10^-6 to 2.3×10^-5 across **1000–3000 K**, with distinct fast oxygen and slower nitrogen relaxation components. That is evidence of coupled finite reservoirs, not a single universal air relaxation time. Colgan and Levitt's [2500 K measurements](https://doi.org/10.1039/TF9676302898) likewise identify O2 as an exception to the simple Millikan–White correlation.

4. **NO matters.** Taylor, Camac and Feinberg's [1967 measurements](https://doi.org/10.1016/S0082-0784(67)80133-4) covered approximately **800–3250 K**, including NO–N2 mixtures. Modern measurements by Streicher, Krish and Hanson, DOI [10.1063/5.0122787](https://doi.org/10.1063/5.0122787), covered NO/N2 at **1900–7000 K, 0.05–1.14 atm**, plus NO/N2/Ar to 8200 K. They find VV slower than the earlier inference. Applying the newer fit at 1700 K is explicitly extrapolative.

5. **Modern O2-mixture validation.** Streicher et al. (2020), DOI [10.1063/5.0015890](https://doi.org/10.1063/5.0015890), measured oxygen relaxation in O2 and N2 partners over **2000–9000 K**. N2-partner VT and VV times were about 70% larger than their respective prior correlations. These data inform oxygen modes, not a direct N2 energy-decay constant; below 2000 K use is extrapolation.

## Calculation on the saved trajectory

Source: restored_cross_width400um_N48_trajectory.npz. No new ODE was run.
At 1 atm a collider's pure-bath pressure-time product must be divided by its **local mole fraction**, not by the packet-average atom fraction.

| Time (µs) | Center T (K) | Local xO | N2–O measured-envelope τ (µs) | Fast additive VT+VV screen (µs) |
|---:|---:|---:|---:|---:|
| 0 | 2700.0 | 0.01556 | 25.7–192.8 | 12.3 |
| 9.87 | 2258.5 | 0.01113 | 35.9–269.4 | 19.9 |
| 24.56 | 1827.6 | 0.007319 | 54.7–409.9 | 33.8 |
| 50.43 | 1700.1 | 0.005452 | 73.4–550.2 | 41.1 |
| 110.43 | 1699.7 | 0.003535 | 113.1–848.6 | 43.4 |

The last column combines Park-style VT with fast legacy VV fits reproduced and checked in [Jans et al., SAND2025-12571J, Appendix A](https://www.osti.gov/servlets/purl/2997343). **It is an illustrative additive-rate screen, not a measured six-species eigenmode, a rigorous fastest possible bound, or a substitute for a coupled energy equation.** In particular, VV receivers cannot actually be held as infinite equilibrium sinks. The appendix does not state a formal low-temperature validity interval. An alternative using its newer NO fit gives 19.2–87.3 µs across the same times, but is extrapolated below 1900 K and is not promoted to a certified prediction.

During 5–25 µs, the center's equilibrium N2 vibrational energy changes on a **22–61 µs** timescale. The fast additive screen is about **0.55–0.90** times that scale, not much smaller than it. The center cools from 2700 K to 1828 K in 24.6 µs. These diagnostics establish a missing scale-separation justification, not the sign or precise size of the actual temperature error.

For energy scale only: harmonic-N2 vibrational inventory is about 301.4 kJ/kg-fresh initially versus 216.3 kJ/kg-fresh for equilibrium populations along the near-50 µs saved state. The 85.1 kJ/kg difference is **not predicted retained energy**. Diffusion can redistribute it; VT and VV can convert it. It makes clear why an unexamined mode closure cannot establish a 6 K tolerance. A parcel-only passive Tv calculation would omit vibrational diffusion and is deliberately not performed.

## Exact extension needed for the transient claim

At minimum add an independent N2 vibrational-energy state and distinguish Ttr from Tv,N2. A defensible reduced model must either explicitly carry O2 and NO vibrational energies or demonstrate their elimination through the coupled VT/VV relaxation matrix and a controlled error bound. Simply assigning all three one common Tv assumes away their different relaxation rates.

The natural minimal robust test is Ttr plus Ev,N2, Ev,O2, Ev,NO, with:
- Molecular and atom-assisted VT at local partial pressures, including measured N2–O uncertainty.
- N2↔O2 and N2↔NO VV, reverse rates satisfying detailed balance, and correct translational energy for mismatched quanta.
- Consistent total-energy bookkeeping, chemical production/destruction energy partition, and vibrational dependence of relevant dissociation/exchange rates.
- Mode-specific conductive transport and species diffusion carrying actual internal energy, rather than equilibrium NASA heat capacity and conductivity silently transferring vibrational energy instantaneously.
- Initially thermal hot/cold populations, then a check whether a vibrational-temperature/Boltzmann closure remains adequate. Only go to state-to-state kinetics if that closure fails.
- A declared treatment of trace NO2 modes. Relevant high-temperature N2–NO2 transfer data were not found in this pass. Missing rates are not zero and are not exclusion evidence.

NO2 is ~2×10^-5 initially in the hot cell, rising to ~1.3×10^-4 near50µs. This low abundance justifies a sensitivity test, not deleting its channel from a rigorous bound. The endpoint certificate remains usable while this transient closure is unresolved.

## Reproduction and provenance

Run python check_relaxation.py. Numerical results: relaxation_diagnostic.json and center_timescale_table.csv. Locally saved supporting originals: sandia_2025.pdf, eucass_2025.pdf, and gollan_thesis.pdf with extracted text, plus plos2020.html. The original Eckstrom numerical measurement is preserved in source_data.json; archived full-text retrieval was not successful. The bibliography distinguishes primary measured results from later numerical correlations and secondary reproduction.
