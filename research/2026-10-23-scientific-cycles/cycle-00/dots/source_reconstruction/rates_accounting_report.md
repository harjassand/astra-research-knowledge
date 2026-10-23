# Nitrogen plasma investigation: rates and energy-accounting handoff

Research date: 2026-10-21. Scope: source audit only. No simulator, hardware, spending, or outreach performed. The selected next calculation is thermal finite-quench/heat-recovery coupling. No selective-electron or vibrational advantage is established here.

## 1. Recommended atmospheric thermal kinetic source

Albrechts, Tsonev, Laitl & Bogaerts, *Towards predictive multidimensional modeling for industrializing microwave air plasma-based NOx formation*, Energy Conversion and Management 349 (2026), 120842. DOI: https://doi.org/10.1016/j.enconman.2025.120842

Verified author-hosted main PDF: https://medialibrary.uantwerpen.be/files/7783/685e44c1-b0c3-424d-a9d5-ab9a2e2d8755.pdf

SI: https://medialibrary.uantwerpen.be/files/7783/8778b6d7-0d5e-45bd-a78a-42bb2cd9776e.pdf

Local: mw2026.pdf/.txt; mw2026_si.pdf/.txt.

Main Table 1, printed pages 4–5: six neutral species N2, O2, N, O, NO, NO2 and seven reversible reactions. T in kelvin; forward units m3 molecule−1 s−1 except association R6, whose low-pressure limit is m6 molecule−2 s−1:

- R1: N2 + M ⇌ 2N + M; k = 5.0e−14 exp(−113200/T)[1−exp(−3354/T)].
- R2: O2 + M ⇌ 2O + M; k = 3.7e−14 exp(−59380/T)[1−exp(−2238/T)].
- R3: N2 + O ⇌ NO + N; k = 3.0e−16 exp(−38000/T).
- R4: O2 + N ⇌ NO + O; k = 9.7e−21 T^1.01 exp(−3120/T).
- R5: NO + M ⇌ N + O + M; k = 2.4e−15 exp(−74700/T).
- R6: NO + O (+M) ⇌ NO2 (+M); reference-55 falloff, resolved below.
- R7: NO2 + O ⇌ NO + O2; k = 5.5e−18 exp(188/T).

Reverse rates use detailed balance with Gibbs free reaction energy, except R6 uses the reference-55 equilibrium fit. Atomic N and O third-body efficiencies: 2.2 for R1 and 3.5 for R2. N2 efficiency: 0.25 for R2. Other molecular efficiencies: unity. NASA-9 thermochemistry is used. This is a thermal kinetic model validated against reactor experiments, not a universal lower bound. SI excludes four tested reactions because their effect was negligible in its studied domain, not necessarily every quench trajectory: 2NO⇌N2+O2; 2NO+O2⇌2NO2; N+NO2⇌2NO; N+NO2⇌N2+O2.

## 2. Resolving R6 and uncertainty

Reference 55 is Baulch et al., *Evaluated Kinetic Data for Combustion Modeling: Supplement II*, JPCRD 34 (2005), 757–1397, https://doi.org/10.1063/1.1748524 . Accessible full primary publication: https://academicweb.nd.edu/~powers/ame.60636/baulch2005.pdf . Local baulch2005.pdf/.txt.

Printed pp.818–819, O+NO(+M)→NO2(+M):

- k0(N2) = 9.2e−28 T^−1.6 cm6 molecule−2 s−1.
- k∞ = 4.9e−10 T^−0.4 cm3 molecule−1 s−1.
- Recommended kinetic range 200–2200 K; Fc = 0.8.
- Kc = 1.28e−28 T^0.622 exp(36930/T) cm3 molecule−1, valid 300–5000 K.
- Δlog10 k0 = ±0.3; Δlog10 k∞ = ±0.3 below 1000 K, ±0.5 above; ΔFc = ±0.2.

Multiply k0 by 1e−12 and k∞/Kc by 1e−6 for metre-based number-density units. The 2026 table labels R6 Lindemann, while Baulch specifies broadening Fc=0.8: record whether F=1 or the broadened expression is implemented and test sensitivity. Do not silently treat an extrapolation beyond 2200 K as measured. Detailed-balance equilibrium concentrations must use consistent molecule/mole units and standard-state factors.

## 3. Energy benchmark audit

Vervloessem et al., Green Chemistry 24 (2022), 916–929, https://doi.org/10.1039/D1GC02762J . Main: https://medialibrary.uantwerpen.be/files/7783/70cdbb7e-b66d-478e-9bc2-51f101343ca1.pdf ; SI: https://medialibrary.uantwerpen.be/files/7783/653ae1a5-e979-4d69-a9bc-17006bb507c9.pdf . Local pulse2022.pdf/.txt and pulse2022_si.pdf/.txt.

Its 0.42±0.03 MJ/mol-N record is pulse-power-only, not wall-plug consumption. SI p.6 explicitly excludes power-supply loss AND interpulse dark-discharge power. Main Table 2 gives only 0.02% NOx. The model imposes gas-temperature evolution rather than solving heat balance. SI pp.44–45 lists N2–N2/N2–O2/N2–N VT processes; no N2(v)–O VT was found. This is an audit observation, not proof that the experimental result is wrong or that one omission explains it.

Qiao et al. (2025), https://doi.org/10.1088/1361-6595/ade33c , is an experiment-plus-state-resolved-model counterpoint at 10 kPa: abstract reports 46.97% vibrational-energy loss through N2–O VT, 52.8% diffusion, less than 1% into NO. Only publisher abstract/first-page preview verified; full mechanism not obtained. Its fractions cannot be transplanted to a different reactor.

## 4. Closest matched nonthermal/thermal comparison, not selected for execution

Shen et al., *Boosting the NOx production in microwave air plasma: a synergy of chemistry and vibrational kinetics*, PSST 35 (2026) 015013, https://doi.org/10.1088/1361-6595/ae2d91 . Full publication: https://oa.tib.eu/renate/server/api/core/bitstreams/1248b542-beb3-4d1f-a167-e5a31de53eeb/content . Local boost2026.pdf/.txt.

At 80 mbar, experiment 3.43±0.1 MJ/mol-N; coupled nonthermal model 3.38 versus thermal model 4.72. Roughly 74% electron energy enters N2 vibration, but only 9.6% cumulative vibrational energy reaches chemistry. Appendices include neutral, excited, charged, and electron-impact channel lists. This is useful matched reactor evidence, not atmospheric or wall-plug proof. Table S1 R8 has a potentially consequential units ambiguity: 2.92e−28 T^−1.41 marked m6/s amid otherwise cm-based rates; verify before transcribing.

## 5. State-resolved extensions and explicit limitations

Armenise, Laporta & Esposito atmospheric 2025 study: https://doi.org/10.1088/1361-6595/adf996 ; accessible full paper https://oa.tib.eu/renate/server/api/core/bitstreams/c5120117-3c7d-4673-b012-f9bb7d212711/content . Local atmospheric2025.pdf/.txt. This paper prescribes constant electron density and temperature, omits attachment/recombination, and says reusable supporting data require author request. It is NOT a source-complete whole-system efficiency baseline.

Harding & Gasque, published 15 October 2026: https://doi.org/10.1029/2026JA035379 . Authors' code and inputs: https://github.com/bharding512/STEVE_2026_Paper_Figures . Local steve_n2v.py is downloaded for inspection only, not executed. It includes an Armenise N2(v)+O→NO(w)+N implementation, Laporta cross-section input and BOLSIG-derived EEDFs in the repository. This is a LOW-DENSITY GEOPHYSICAL model, not atmospheric reactor evidence. It tests both ideal monoenergetic and self-consistent electron distributions. Useful later as transparent input provenance, not as a nitrogen-fixation efficiency result.

The related rate publication and correction are https://doi.org/10.1016/j.chemphys.2023.111937 and https://doi.org/10.1016/j.chemphys.2023.112088 . The correction concerns Table S13 O+N2(v) dissociation interpolation stability. Thus the code comment claiming corrected exchange rates should not substitute for checking which coefficients actually changed.

Tsonev et al. 2026 https://doi.org/10.1016/j.cej.2026.176405 reports modeled minima 1.84 MJ/mol with Boltzmann VDF, 1.40 with non-Boltzmann VDF, and 1.79 when VT relaxes. Full paper was not obtained; author index has no PDF/SI link. Treat these as abstract-level model-specific results, NOT universal thermodynamic bounds. No new search or outreach is needed for the current thermal finite-quench calculation.
