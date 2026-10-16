# Independent N887 causal-horizon audit

## Decision

N887's exact countermodel is correct for its deliberately restricted observation interface: two static ethane endpoints and **one fixed-waveform periodic mean**. It is not a joint fit of Xu's duration/voltage grid, current records, spectroscopy, acetylene conversion, or run histories. Do not paraphrase it as proving that every available published observation admits arbitrarily slow dynamics.

The next discriminating measurement is productive-reactor chemistry during a controlled pulse-train withdrawal/recovery, or startup from an independently restored state. Within the explicit scalar model, two equal-duration recovery integrals identify the missing decay rate. In the unrestricted physical system, no finite record alone proves absence of slower hidden modes: an acquired tail/inventory/dynamics bound remains necessary for a global horizon claim. A randomized pulse/sham fresh-carbon comparison can establish the specified finite-horizon effect directly without globally identifying the mechanism.

## Exact proof reconstruction

At positive voltage z'=-mu z and ethane b=1-z; at negative voltage z'=lambda(1-z), b=beta. State remains in [0,1]. Let h,d>0, P=h+d, and D=h+d beta-P rho, with 0<D<h. Choose mu>0 with L=(1-exp(-mu h))/mu>D, z*=D/L, v=exp(-mu h), u=(1-z*)/(1-z*v), and lambda=-log(u)/d.

Both rates are positive and finite. The return map has fixed point z*=1-u+uv z* and contraction uv<1. Cycle ethane is h-z*L+d beta=P rho exactly. Static endpoints are 1 and beta. Starting from z=0, pulse versus duration-matched positive sham gives Delta_iso(T)=(1-u)(1-exp(-mu T))/mu. Starting just before a negative pulse after shared periodic conditioning gives Delta_cond(T)=z*(1-exp(-mu P))(1-exp(-mu T))/mu.

As mu approaches zero, z* approaches D/h, 1-u and 1-uv are O(mu); both fixed-T contrasts vanish. The conditioning e-fold cycle count -1/log(uv) and positive washout 1/mu diverge. At T=h, Delta_cond=D(1-exp(-mu P)). The large-effect endpoint Delta_iso(h)->D is valid only for isolated contrast, not both contrasts.

Independent script reconstruct.py executes only newly authored arithmetic and workbook reading, never acquired code. Illustrative beta=0 uses the independently read final Figure 2 ratio. With mu=0.04/s, isolated/conditioned 10 s deficits are 6.95021/2.58112 static-rate-seconds, washout 25 s. With mu=1e-7/s they are 0.0000347652/0.00000784378, washout 10,000,000 s; both have exactly the same periodic mean 0.22117569044. These models are logical witnesses, not acquired catalyst parameters.

## Minimum observable, with exact scope

Withdraw the negative pulses after matched periodic conditioning and retain the same actual positive electrical and reactive boundary. Measure absolute ethane deficit against a separately established positive-static reference in two adjacent equal windows of length tau:

J0 = integral_0^tau (1-b(t)) dt,
J1 = integral_tau^(2 tau) (1-b(t)) dt.

In this scalar family, J1/J0=exp(-mu tau), independent of unknown starting amplitude. Thus mu=-log(J1/J0)/tau. D then fixes z*, u, lambda and the contraction, so the full family is identified. A calibrated upper confidence bound r_U<1 on the ratio gives mu>=-log(r_U)/tau and a finite washout bound. It also gives Delta_cond(h)>=D[1-r_U^(P/tau)] within this family. Two measurements here mean two independent recovery integrals plus the known baseline; repeated randomization and controls are still required experimentally. No 0.1 s detector resolution is required if long integrated windows and transport/boundary inventories are properly accounted for.

A complementary startup observable is cycle suppression D_n=D(1-q^n) from z=0 with q=uv. Known preparation and cycle-resolved approach to the plateau bound q; a record showing only an already conditioned plateau does not.

Neither expression licenses fitting a single exponential to an arbitrary multimode reactor and declaring all slower modes absent. Finite data plus finite precision can hide weak slow reservoirs. For a claim limited to T, direct randomized execution/omission after identical history identifies that finite-T contrast; to claim a sufficient complete horizon, acquire conservative bounds on unresolved tails/inventories or justify a finite-dimensional dynamics class. The minimum depends on the claim, so there is no model-free universal single measurement that closes every gate.

## Primary-source check, fresh acquisition

Freshly downloaded directly from publisher MediaObjects for DOI 10.1038/s41557-026-02107-8:
- MOESM20 Figure 2 XLSX, SHA256 47a571bed2750c89ba2cf38cc75235f1e7497727c57e2b9b28fc3fdfc667a3fe.
- MOESM24 Figure 6 XLSX, 28af31650f80fe130fef680035e127ab2f257ae681395d52ddb850662132fdfa.
- MOESM8 SI Figure 7 XLSX, c41ad6efa45d475db18b87ca2e88cbaf967f2e2fbfb31f8969a300c2c631d72f.
- MOESM12 SI Figure 11 XLSX, 953c5f0a13da5588d1f853ef8b4c8bddb2d1cab8ec3f7ea9ed2d1f0465ddc983.
- MOESM1 final SI PDF, 9b8926dfc60adfdd2fc5fd3c0f28c830ac3499a6a98885ac47667f3f5126ac69.

All four workbook hashes exactly match the pinned FZ analysis_results.json. This independently reconciles the earlier run-local download failure: primary sources are presently retrievable and FZ acquisition claims have byte-level support.

Figure 2 b!C10:D11 gives static 80.79704%,47.75220% versus pulsed 81.02334%,80.55926%. With the paper's S=a/(a+b), b/Ain=X(1/S-1). Independently obtained ratio 0.22117569043994356 and beta=0 suppression area 7.76612552655657 s. Net ethylene/Ain=X(2-1/S)=0.6147060718105902. These are conditional material-balance reconstructions, not newly measured rates. Preprint-v1 rounded numbers separately give ratio 0.2214772280049756 and area 7.763079997149747 s. This audit did not newly acquire preprint bytes; its rounded transcription was replayed from the pinned original report and kept distinct.

Figure 2 contains 10 static/dynamic rows and two 30-point duration grids, not startup/run-order or recovery chemistry. Figure 6 contains spectra at 56 s (panel a) or 42 s (b-d) spacing, not absolute productive-reactor molecular flux. SI Figure 7 b has time, potential and current only (54,999 samples, 0.0002 through 10.9998 s); the record is the separate 10 s/1 s waveform, not the optimum 10 s/0.1 s. SI Figure 11 has foil spectra, current, and 1 h/12 h low-current endpoint controls, not the required common-hold randomized comparison.

Final SI section 7.3 expressly describes H-preloaded foil with no continuous H feed, several-hundred-ohm contact resistance versus about 0.2 ohm in the fuel cell, and sub-microamp currents. It reports no gaseous hydrogenation products above approximately 1 ppm after 1 h under specified small currents, with nonzero products after 12 h at -50 microamps. These are meaningful controls in that foil regime; they cannot supply the productive mixed-feed recovery rate or upper-bound its slow modes. The SI's product assignment disagrees with workbook Figure 11 c!C5:D5, as already recorded in GA. This audit confirms the distinct source structures and SI wording, without mistaking absence in these four inspected workbooks for absence in all unpublished author records.

## Exact remaining gate

1. In the same productive reactor and waveform regime, acquire known-state startup, randomized train withdrawal, and recovery under common actual positive boundary, with absolute molecular flux or validated integrated balances. Record actual conditioning cycles and reset reproducibility; bound residual tails rather than declaring an arbitrary 10 s null decisive.
2. Randomize isolated pulse/sham and executed/omitted next pulse after identical periodic histories. Introduce fresh carbon only after preparation, collect complete chase or conservative missing-carbon bounds, and quantify both ethane deficit and net ethylene benefit. Exposure, isotope background, source assignment and species-specific recovery require calibration.
3. A positive fresh-cohort result identifies preparation-dependent subsequent chemistry, not an electronic carrier. Adsorbate, hydrogen, membrane, support and structural states remain possible until a state-specific intervention or independently bounded balance distinguishes them.
4. No generic prepare-then-react invention promotion: Lim et al. JACS Au 2021 DOI 10.1021/jacsau.1c00044 already supplies closely related pulse-sweeping precedent, as primary-provenanced by GA. This audit did not newly reacquire that paper. No process superiority claim before matched outlet specification, throughput, lifetime and full preparation/read/reset work.

## Provenance

Pinned repository: https://github.com/harjassand/astra-research-knowledge/tree/61389569d6c53b439764f0d148b35b7fa6083eec
Read N887, GA CAUSAL_IDENTIFIABILITY_THEOREM.md, physical audit AUDIT.md and REPORT.md, archived physical_primary.txt, FZ CAUSAL_IDENTIFICATION.md, and FZ authored analysis_results.json. No repository edits, outreach, purchases, acquired-code execution or laboratory measurements.

Publisher source URL pattern: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_MOESM20_ESM.xlsx (replace object number and extension as above).

## Additional conditioning-protocol check

The freshly acquired final SI was searched in full for stabilization, steady state, conditioning, sampling and time specifications, with relevant sections read in context. It provides electrical charging/reaction timing and foil preparation/control intervals, but I found no quantitative productive mixed-feed startup-to-periodic-attainment tolerance or pulse-withdrawal molecular recovery bound there. Final publisher HTML was also acquired, but exposes abstract/data availability and supporting links rather than the paywalled main Methods: absence from final main Methods is therefore NOT established.

Primary Research Square v1 search-index text explicitly reports a separate XAS preparation: 8 h under reaction conditions in-house, then argon sealing/transport and H2-only potential scans at the synchrotron. It also specifies 30 min H2 preloading and about 5 min acetylene exposure for foil DRIFTS. These are real timed preparation statements, not missing data, but neither establishes the startup horizon of the optimum mixed-feed periodic waveform from positive-static equilibrium. The preprint direct PDF request returned HTTP 403; the local preprint_v1.pdf name contains that error body, not a valid PDF, and must not be counted as an acquired manuscript. The source is the indexed primary URL https://assets-eu.researchsquare.com/files/rs-6845872/v1_covered_135a4fac-50b0-4a57-ac68-a1f9dadbd716.pdf . Main catalytic-test timing is still an access/verification gap, not an established absence.

If a main-methods or run-log statement establishes approach from a known state within N cycles to a specified relative error epsilon, it is an additional observation: in the scalar family q^N<=epsilon, hence -1/log q<=N/log(1/epsilon). It would exclude the arbitrarily slow members for that experiment. An unspecified assertion of stabilization, pre-ageing for XAS, or an unknown previously conditioned initial state cannot supply that inequality. Obtain that protocol/run-history evidence before claiming the countermodel accommodates the entire physical experiment.

## Important continuation: equal-duty grid falsifies the shared scalar model at point-estimate level

See EQUAL_DUTY_TEST.md and equal_duty_results.json. Exact h/d=10 pairs in rows 7,13,19,25 show reconstructed ethane/Ain decreasing from 0.596901 to 0.227691 as period grows from 0.011 to 11 s. Even the 1.1-to-11 s pair decreases by 9.8729%. The fixed-positive-rate scalar model predicts the opposite monotonicity at fixed duty; its arbitrarily slow limit predicts equality. Thus the family is not a joint explanation of the grid's point values under shared rates and comparable exposures. Missing errors prevent a statistical significance claim; waveform-dependent real electrical exposure can invalidate the fixed-rate premise. The endpoint-plus-one-mean theorem remains correct, and no general multimode horizon is identified. This is a substantive new check beyond the earlier statement that the family was not jointly fitted.
