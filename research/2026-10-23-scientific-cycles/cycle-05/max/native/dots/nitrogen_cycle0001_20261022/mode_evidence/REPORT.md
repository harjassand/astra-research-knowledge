# Chemical mode partition: bounded source reconstruction

## Decision

A source-backed **forward, state-resolved calculation is now possible**, particularly for N2(v)+O→NO(w)+N using the recovered 2017 interpolation and its own N2/NO energies. It is not yet an identified reversible six-species closure. Do not launch a trajectory. A pointwise rate/energy-moment comparison against the same QCT model at LTE is scientifically better justified than arbitrary partition coefficients. The separate original seven-reaction Arrhenius baseline must remain separate, not be silently rescaled to QCT.

The observable that matters is the **net chemical production and selective removal of mode energy together with net NEW NO production**, not a product vibrational temperature alone or a total thermal rate. Parent reports 99.9216% ideal once-through retention already; preserving the residual loss is therefore a narrow benefit. A forward-only enhancement is not evidence of net production or useful feed-preheat.

## Actual retrieved numerical assets

2017 Esposito–Armenise, DOI https://doi.org/10.1021/acs.jpca.7b04442:
- SI1: https://doi.org/10.1021/acs.jpca.7b04442.s001, local jp7b04442_si_001.pdf, vibrational levels.
- SI2: https://doi.org/10.1021/acs.jpca.7b04442.s002, local jp7b04442_si_002.pdf and extracted text, complete Fortran interpolation of forward exchange and O-collider dissociation, not executed here.
- Source code initializes temperatures 1000–20000 K. Exchange uses N2 v=0…59, NO w=0…47 and k=(1/3)exp(a0+a1/T+a2/T²), cm³/s. Preserve its included 1/3 factor. Precise dissociation-zero energies include N2(v0)=−9.7582737 eV, N2(v1)=−9.4680532 eV; NO(v0)=−6.5096986 eV, NO(v1)=−6.2808127 eV. Use excitation differences E(v)−E(0) for stored vibrational energy; do not confuse negative binding energies with excitation inventory. The code's extra boundary/pseudolevel entries are not automatically populated bound levels. No reverse-rate routine was found. SI3 contains quasibound lifetimes, not a missing reverse table.

2021 Esposito–Armenise, DOI https://doi.org/10.1021/acs.jpca.0c09999:
- SI2: https://doi.org/10.1021/acs.jpca.0c09999.s002, local jp0c09999_si_002.txt, actual reactive matrix N+O2(v)→NO(w)+O.
- Header fixes Trot=Ttrans. Columns are v,w,k[cm³/s],variance; sqrt(variance) is the Monte Carlo standard deviation, not systematic model uncertainty.
- Five temperatures: 2000,5000,10000,15000,20000 K. Each contains 2112 distinct pairs, v=0…43,w=0…47. No negative rate rows. At 2000 K, 0→0 has k=8.6283e−13 and variance=4.0362e−29. Raw tables do NOT cover1700 K;2700 K would require explicit interpolation.
- SI4, advertised as dissociation, is **byte-identical to reactive SI2**, including header. Both MD5 a74b700eed17a230bc813c592fc8683e; SHA25683105d1564c2fbd301b725fa8cd6e99646c56effe6d9e5917c339b42e22735ef. This duplication is in publisher metadata too. It cannot supply dissociation/recombination data.

All exact files, official Figshare metadata, byte counts and hashes are local. See manifest.json, reactive_table_audit.json,2017_levels_transcribed.json and audit_sources.py. The latter only audits/transcribes source data, not chemistry.

## What is measured versus modeled

The 2021 primary study compares its integrated reactive rate to thermal measurements across approximately300–5000 K; its product-distribution comparison is at300 K. Ground-state reactive PES contributions carry factors1/6 and1/3. Rotational interpolation is assessed from1000 K upward. These facts support a computational mechanism candidate, not measured state-to-state energy partition at1700–2700 K. Source: https://pubs.acs.org/doi/abs/10.1021/acs.jpca.0c09999 . The recovered SI must not receive those factors a second time without verifying its construction.

The subsequent interpolation paper, https://doi.org/10.1016/j.chemphys.2021.111325, explicitly covers1000–20000 K and five neutral species, including state-resolved exchange/dissociation. Its full coefficient set and O2 energy ladder were not reconstructed in this bounded pass. The2023 extension https://doi.org/10.1016/j.chemphys.2023.111937 instead fits300–1000 K; do not extrapolate it upward. Its2024 correction https://iris.cnr.it/handle/20.500.14243/452425 changes low-temperature O+N2 dissociation coefficients. It is not a correction to the2017 source by implication.

A directly measured NO2 channel exists: Smith–Tuckett–Whitham1992, https://doi.org/10.1016/0009-2614(92)80099-W, measures nascent NO(v0–4) and O2(v6–11) from O+NO2. NO vibrational yield≈4.6%; O2 yield≈26% is a surprisal-analysis inference from a partial population window. This is not a validated1700–2700 K full-mixture partition. It prevents saying that NO2 chemistry has no primary population evidence, but does not close target-temperature NO2 association/dissociation or mode-transfer channels.

The existing EUCASS2025 non-preferential closure assigns average internal energy with chemical species production. It is a conventional hypothesis, not such a population measurement. Its five-species scope still excludes NO2; see owner-local ORDINARY_MODEL_ALTERNATIVE.txt.

## Missing reversible closure and permissible next calculation

For a state-pair event define J_vw=kf_vw n_A(v)n_B−kb_wv n_C(w)n_D. Its chemical mode moments are sums of −epsilon_A(v)J_vw and +epsilon_C(w)J_vw. This directly identifies the mode energy entering/leaving chemical channels, while net NO production is sum J. The forward moment can be contracted now for the2017 source after an independently checked transcription, with specified population ansatz.

Reverse detailed balance needs **state-resolved equilibrium density ratios**, not merely the bulk NASA equilibrium constant and a guessed factor. Required: compatible electronic degeneracies/fine structure convention, level-dependent rotational partition sums, nuclear-spin/symmetry conventions, translational mass factors, source ground-state energy offsets, and consistent level truncation. The recovered forward files do not establish all of these. No claim that an arbitrary common Boltzmann mode temperature reproduces reaction-tail populations is warranted. The2017 N2/NO ladder is present; the source-matched2021 O2 ladder and full reverse convention remain unverified. Assuming O2 and NO at bath temperature is a declared comparator, not evidence.

Recombination follows state-resolved reverse dissociation only with collider-specific detailed balance and correct bimolecular/termolecular units. The2017 O+N2 dissociation source can support its own O-collider inverse after these checks; it does not supply every third-body channel. The2021 duplicated SI4 is unusable for this purpose. N+O+M↔NO+M and NO+O+M↔NO2+M, plus O+NO2↔O2+NO, cannot be silently deleted from a rigorous six-species closure.

**Usable now:** a bounded forward N2 mode-selective NEW-NO production/energy-removal diagnostic from2017, compared first to its own LTE contraction; or the2000 K forward N+O2 table with explicit O2 populations. **Unidentified:** net reversible chemical source, complete recombination, target-temperature NO2 partition, actual bath-cap crossing, and kinetic reachability. To promote the diagnostic to a reversible point calculation, first reconstruct the state equilibrium weights; if unavailable retain this scoped limitation. No energy-export certificate is altered.

## Access log and stopping point

CNR PDFs returned403. Official Figshare API metadata and normal file downloads subsequently succeeded; no CAPTCHA or access bypass. A HEAD request to a short-lived signed storage link returned403, but the original authorized GET operations completed. All download processes have ended. No numerical trajectory, full contraction, hardware, payment, or outreach was performed.

## Additional literal-source defect: 2017 seam interpolation

Parent identified a potentially misplaced index. I rendered and visually inspected original PDF page S15 (saved2017_S15.png). The published line literally reads:

    aexchON2(i,lim_v(iw),iw+1) = a*En2(lim_v(iw)+1) + b

This is NOT a text-extraction error. Neighboring comments describe interpolation of four N2-energy nodes around E_N2(v)=E_NO(w), suggesting that the intended left index could be (i,lim_v(iw)+1,iw). That is an inferred repair, not a published correction. Any source contraction must preserve both literal and proposed-correction variants and quantify sensitivity; do not silently repair. The earlier 'usable' conclusion is thus conditional on this explicit source-defect treatment as well as transcription verification.

## 2020 primary erratum recovered (DOI0c00869)

Official publisher indexed text at https://pubs.acs.org/doi/10.1021/acs.jpca.0c00869 (Esposito–Armenise2020,J.Phys.Chem.A124,1465) specifies two corrections to printed **thermal** fits:
- Main text §3.1: R_react(T)=1.2686×10^-13 T^(+0.874) exp(−36899/T). The original temperature power had the wrong sign.
- Main text §3.4: R_diss(T)=6.1002×10^-5 T^(−0.926) exp(−117130/T). The original expression used two temperature substitutions incorrectly.

The correction does not identify a change to the SI state-to-state coefficients, energy references,1/3 statistical prefactor, or S15 seam indices. Therefore its documented scope is resolved, but it does **not** repair or adjudicate the independently verified SI seam defect. A reconstructed LTE sum should be checked against the corrected rather than uncorrected thermal fit; disagreement is a diagnostic, not permission to rescale the state-resolved matrix. These are published fit corrections, not new physical measurements.

Retrieval: official ACS web-search result returned the correction text and formulas on2026-10-21; no restricted CNR attachment was accessed. No computation performed in this addendum.

The bounded2022 DOI10.1088/1361-6595/ac9082 title/DOI search located official CNR bibliographic records, but no additional primary passage changing the erratum interpretation. No full-text review of that paper is claimed. Retrieval stopped once the explicit2020 correction scope was recovered; no broad VT/VV review reopened.
