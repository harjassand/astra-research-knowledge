Physical contracts for molecular completion, temporary retention and renewable construction
13 November 2026 Brisbane

This note contains conditional physical models and source scopes. It does not supply measured molecular rates, an implemented detector, a new covalent synthesis cycle or a working apparatus.

Independent introduced kinetic model
Let a temporary bridge start bound, unbind at rate a and rebind at rate b. The probability that it is bound at one observation time is
P_B(t) = b/(a+b) + a/(a+b) exp(-(a+b)t).
Consequently a long wait leaves a false-retention floor b/(a+b). For introduced a=1/s and b=100/s the floor is100/101, so one late retention observation cannot reach a0.001 false-pass target.

With ideal instantaneous samples every Delta, requiring every sample to remain bound has probability P_B(Delta)^n. This charges finite observation frequency but still omits a physical detector. At a=1,b=100 and false-pass0.001, Delta0.0001s requires69424 samples/6.9424s; Delta0.1s requires695/69.5s; Delta1s requires695/695s; Delta10s requires695/6950s. With introduced irreversible good-product loss d=0.00001/s, good survival is exp(-dt). A0.001 good-loss tolerance permits at most100.0500s, so the latter two sampling cases cannot satisfy both requirements under this model.

An alternative introduced chain has B->U at a, U->B at b and U->D at c, where D is physical irreversible separation of a weak bridge. Taking survival outside D as a conservative false pass, z=a+b+c, lambda_s=2ac/(z+sqrt(z*z-4ac)), lambda_f=(z+sqrt(z*z-4ac))/2, gives
S(t) = (lambda_f exp(-lambda_s t)-lambda_s exp(-lambda_f t))/(lambda_f-lambda_s).
The equal-root limit is exp(-lambda*t)*(1+lambda*t); c=0 gives survival1. The implementation uses the stable slow-root expression, explicit limits and binary64 arithmetic.

For a=1,b=100, targetS0.001 and d=0.00001, c0.01/s requires69775.2s and good survival0.4977; c1/s requires704.533s and0.992979; c10/s requires76.6228s and0.999234; c100/s requires13.8551s and0.999861. A physically achieved absorbing separation could change the discrimination, but neither its rate nor force, geometry, clearance, finite travel, energy, reset and chemical compatibility is provided by this Markov calculation. With no rebinding and no other error, simultaneous bad-survival<=0.001 and good-loss<=0.001 require a/d>=ln(1000)/[-ln(0.999)]=6904.300825.

Retention does not identify the desired chemistry. An unintended strong covalent bridge or wrong isomer can have the same mechanical observation as the desired product. Sequence selection and linkage identity require additional chemical restrictions or independently testable signals. A spent activating group can arise from successful transfer or hydrolysis, so its release is not in itself a product-specific witness.

If a test has bad-pass0.001 and good-pass0.999, the posterior fraction of bad products among passes is pi*0.001/[pi*0.001+(1-pi)*0.999], where pi is the incoming bad fraction. At pi0.1 it is about0.0001112; at pi0.99 it is0.09016; at pi0.9999 it is0.90917. A false-pass number cannot be used as an accepted-product purity without paying the input mixture, rejected stock, useful yield and reset.

Construction interface
A candidate product-dependent bridge could connect two otherwise separate local handles only after covalent transfer, and permit progression after redundant temporary paths are removed. This is an unconstructed hypothesis, not a molecular mechanism. It needs actual compatible groups, geometry and a route through all intermediates. Hydrolysis, rebinding and wrong strong products remain adversarial branches; removal can damage product, consume program or stall the next operation. A reaction network that labels the desired branch as observed does not implement the interface.

Material output, release and renewal require actual product chemistry, rather than treating an instruction record as proof of product. Identify reusable catalysts, supports, recognition and program stocks separately from stoichiometric monomers, activators, protecting groups, adaptors and chemical fuels. Include their preparation, replacements, product separation, inhibitory species, rejected chains, waste and restored readiness. Capping an incomplete chain can suppress error propagation, but it rejects that chain rather than repairing its missed extension.

Primary exposure and limits
Meng etal2016 has the bounded main exposure and hold recorded below. Its narrative rates are not joint stochastic parameters for this model.

Shuluk etal2025 actual main through229 describes adaptation of a commercial parallel synthesizer, incomplete-chain capping, destructive sequence reconstruction and a short analytical scan on six9mers. Physical robot calibration, reagent vessels and product handling are real parts of that construction. The scan is not total synthesis time or a self-renewing molecular factory. Later main/Methods/SI are unread after the first followup exposed a browser check. Kassem etal2017's previously read molecular arm changes substrate proximity and stereochemical outcomes with externally supplied inputs; it does not provide autonomous completion control.

Source and access bindings
NEW PRIMARY/SOURCE SCOPE OUTSIDE SCIENTIFIC BODIES --13November2026Brisbane/06:13UTC ROOT review. Completed dependent local identity/alias/hold checks preceded first navigation. Every earlier known/unknown hold persists; failures are observation limits, not scientific negatives.
NEW HELD exact https://users.ox.ac.uk/~dplb0149/publication/pub217.pdf: actual Meng--Muscat--McKee etal2016 An autonomous molecular assembler for programmable chemical synthesis/DOI10.1038/nchem.2495 mainpp0--3/lines0--462 read. The FIRST governing followup at460 returned400Timeout. SAME identity HELD against furtherlookup/retry/Nature/author/repository/provider/version/title/PDF/SI/export recovery. Read scope: alternating instruction/chemistry hairpins, proximity chemistry, explicit lack of coordination between covalent reaction and hybridization, short-chain products and missed reactions. Main narrative20min/hairpin and5min acyl half-time are not jointly qualified rate distributions; SI/Methods/later product-record validation unread. A DNA program record is not authenticated covalent sequence. This is DISTINCT from already-held Bath--Turberfield2026 d5nh00505a, whose checkpoint/parallel-DNA/polymerase mechanism remains unavailable and is not imported.
NEW HELD exact https://pure.manchester.ac.uk/ws/files/30033043/POST-PEER-REVIEW-PUBLISHERS.PDF FIRST ROOT open400Unsupportedcontent-type application/octet-stream. SAME Lewandowski etal2013 Sequence-Specific Peptide Synthesis by an Artificial Small-Molecule Machine/DOI10.1126/science.1229753 held against retry/Science/author/repository/provider/version/title/PDF/SI/export recovery. No governing paper passage read; search-rendered rotaxane, product or scale claims not operating premises.
NEW HELD exact https://pmc.ncbi.nlm.nih.gov/articles/PMC3427124/ FIRST ROOT open browser-check/reCAPTCHA only. SAME Friddle--Noy--DeYoreo2012 Interpreting the widespread nonlinear force spectra of intermolecular bonds/DOI10.1073/pnas.1202946109 held against challenge/reload/redirect/PNAS/author/repository/provider/version/title/PDF/SI/export recovery. No governing force-law/test passage read; ROOT's two-state model is independently derived, not reconstruction of this paper.
NEW HELD exact https://pubs.rsc.org/en/content/articlehtml/2024/sc/d4sc00973h FIRST ROOT open403Forbidden. SAME Efficient automated solid-phase synthesis of recognition-encoded melamine oligomers/DOI10.1039/d4sc00973h held against retry/PDF/PMC/author/repository/provider/version/title/SI/export recovery. No governing passage read; search lengths/yields/purity/recognition not imported.
NEW HELD exact https://pmc.ncbi.nlm.nih.gov/articles/PMC11937967/ FIRST governing followup229 exposed browser-check/reCAPTCHA. SAME Shuluk etal2025 A Workflow Enabling the Automated Synthesis, Chain-End Degradation, and Rapid Mass Spectrometry Analysis for Molecular Information Storage in Sequence-Defined Oligourethanes/DOI10.1021/jacsau.4c01070 held against challenge/reload/redirect/ACS/author/repository/provider/version/title/PDF/SI/export recovery. Initial actual main through229 read: adapted commercial parallel synthesizer, incomplete-chain capping, physical reagent/vessel/calibration operations, destructive sequence reconstruction and six9mer/under30s analytical scan. Later main/Methods/SI/code/images unread. The scan is not total synthesis throughput, molecular retry, renewable factory or full-cost advantage; intro cited-original efficiencies retain secondary scope only.


Executable artifacts
ROOT_MOLECULAR_RETENTION_REBINDING_AND_COMPLETION_WITNESS_SCREEN_20261113.py
4097 ASCII bytes, SHA25639e602d9376625afc38bc7560e11a54360f611c9968cce61f25ae0dceec5831c
ROOT_MOLECULAR_RETENTION_REBINDING_AND_COMPLETION_WITNESS_SCREEN_20261113.json
5401 ASCII bytes, SHA2567736512d89702c6c598e2500ece2fdee2d425e378532a0c8dfec9aa2fd0af602

These are independently authored and executed calculations. No producer code, linked report, source-data, supplemental artifact or held identity was recovered or executed. All chosen rates, good-product hazards and separation rates remain introduced. Analytic limit checks are not experimental validation.
