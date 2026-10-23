# Reverse release from a PFAS-loaded porous bead: useful transport control, not a fate test

**Disposition:** bounded physical no-go for the proposed decision use. A target-start washout can measure desorbability when the starting target inventory is independently known. Under ordinary inlet/outlet access it does not bypass the rare-arrival cost, and a finite reverse-release trace cannot by itself separate parent PFAS retained in a bead from parent transformed to unmonitored products. The decision-grade operation is a closed endpoint fluorine/parent balance. No experiment was run, and no novelty or performance claim is made.

## Concrete target decision and operation

Consider a spent granular activated-carbon (GAC) bead or bed after a declared regeneration/destruction step, with a known PFOA-derived loading. The consequential decision is whether apparent aqueous removal means (a) PFOA is still retained as parent/organic fluorine on the sorbent, (b) it was transferred to another liquid or gas fraction, or (c) its fluorine was converted to inorganic fluoride. This is narrower than a general treatment-efficacy claim.

A physically executable reverse-chase test is: load a weighed GAC bed with a fixed amount of isotopically labelled PFOA, apply the declared regeneration/destruction step in a closed apparatus, then place the remaining bed in a flow-through holder and switch to PFAS-free matrix-matched water. Collect time-resolved chase fractions; recover the whole bed, tubing, filters, vessel rinses, and treatment off-gas/scrubber. Quantify parent and targeted shorter-chain products by isotope-dilution LC-MS/MS (with suspect/non-target LC-HRMS as a screen), extractable/adsorbable organic fluorine by a validated CIC workflow, and inorganic fluoride by ion chromatography. Destructively assay a representative whole-bed aliquot or the full bed for retained parent and total fluorine. Use pristine GAC, a no-GAC plumbing/treatment recovery blank, a known PFOA-loaded GAC recovery control, and matrix-matched PFOA and fluoride spikes; subtract measured pristine-media fluorine rather than assuming it is zero.

The result is a closed fluorine ledger, in moles of F. Count each recovered physical compartment once; speciate its fluorine with parallel assays rather than adding product amounts to a compartment total:

\[
F_0=F_{\rm aqueous\ output}+F_{\rm bed/ash}+F_{\rm filters/vessel}+F_{\rm offgas/scrubber}+U_F.
\]

Report intact parent on each phase separately from total organic fluorine and inorganic fluoride. CIC alone does not identify the fluorinated molecule, and an unclosed or unassigned fluorine term is unresolved rather than mineralized. A target-state fraction such as \(f_{\rm parent,bed}=M_{\rm parent,bed}/M_{\rm parent,in}\) is then directly measured without fitting a kinetic network. Fluoride recovery is evidence of defluorination only to the extent that the fluorine balance closes and matrix-specific background/recovery are controlled; it does not by itself establish that every non-fluoride product is harmless.

## Exact obstruction to a release-only fate inference

Let a known parent mass \(M\) be retained in the target sorption state. In the one-compartment special case where desorption enters the measured chase channel with first-order rate \(k\), the parent mass appearing by finite time \(T\) is

\[
Y_{\rm retained}(T)=M(1-e^{-kT}).
\]

The alternative fate model converts the parent to an unmonitored product before the chase and produces no parent signal, so \(Y_{\rm converted}(T)=0\). For any finite mass-resolution \(\varepsilon>0\), choose \(0<k\le\varepsilon/(MT)\). Since \(1-e^{-kT}\le kT\), the still-retained parent produces \(Y_{\rm retained}(T)\le\varepsilon\). Thus no finite-time, finite-resolution parent-only washout can uniformly certify conversion: an arbitrarily slow but nonzero release is observationally as small as the converted case. A lower bound on \(k\) would repair this only by adding an independently validated desorption/accessibility assumption, which is the kinetic oracle the proposed operation was meant to avoid.

If a fresh labelled probe is injected after the treatment to measure the target-start relaxation, its output is an assay of the current bead's probe transport. In the valid pair of histories where the bead's pore network is unchanged but the historical PFOA was retained in one case and converted in the other, the fresh probe produces exactly the same trace. It therefore does not report the historical parent fate. If instead the original labelled parent is followed, the finite-window slow-desorption counterexample above still applies.

There is also an access bottleneck. With only the normal feed port available, linear tracer loading from source state \(S\) places expected mass \(m_T=D P_\tau(S,T)\) at target state \(T\) after load time \(\tau\), for inlet tracer dose \(D\). Creating a known target-start mass \(m\) requires \(D=m/P_\tau(S,T)\) (or at least \(D\ge m/\sup_{u\le\tau}P_u(S,T)\) when dosing over a time window). When target access is rare, the loading cost scales inversely with that same rare forward-arrival probability. A pre-embedded or section-injected label could avoid this loading cost, but it would require new internal access and an independent demonstration that the label occupies the native target state without perturbing it.

For a closed reversible linear transport model, detailed balance gives the pointwise relation \(\pi_S P_t(S,T)=\pi_TP_t(T,S)\). With calibrated equilibrium weights and true target initialization, a reverse response is the weighted forward cross-kernel; it can improve practical signal-to-noise in some geometries, but it adds no ideal identifiability beyond that kernel. It cannot replace the solid/product inventory measurement needed for the chemical-fate decision.

## Strongest equally informed incumbent and verdict

The fair incumbent is not an effluent-only sensor. It is the same labelled forward feed/chase with whole-bed endpoint extraction, targeted LC-MS/MS, and total/organic/inorganic fluorine accounting across all recovered phases. It observes the fate variable directly and requires no transport model. A long-running pilot study has already used multi-port breakthrough profiles, isotope-labelled analytical standards, targeted PFAS LC-MS/MS, and molar adsorption balances for GAC and anion-exchange columns; that is a strong adsorption-performance comparator, although it does not by itself establish chemical mineralization. Modern total-organic-fluorine methods complement targeted PFAS assays by capturing fluorinated species outside the target list. A 2026 primary study specifically shows that CIC fluorine recovery can depend strongly on sorbent/mineral matrix and analytical conditions, so the whole-ledger controls and background correction above are mandatory rather than optional.

**Verdict:** reverse release is a useful transport/desorption control only when the target loading is known and physically realizable. It neither bypasses boundary-only rarity nor establishes the fate of historical PFAS. For the declared hazard decision, the strongest comparator is the closed inventory assay and it is at least as informative with fewer special access assumptions. Do not advance the reverse-release mechanism as a new chemical-fate capability unless a target-specific preloading operation can be demonstrated and it beats that comparator on decision error, time, or cost under a matched recovery budget.

## Primary sources checked

1. Chow et al. (2022), [Comparative investigation of PFAS adsorption onto activated carbon and anion exchange resins during long-term operation of a pilot treatment plant](https://doi.org/10.1016/j.watres.2022.119198), *Water Research* 226, 119198. The reported 441-day pilot used multi-port breakthrough and molar adsorption balances; it is an adsorption/uptake comparator, not a destruction proof.
2. Forster et al. (2023), [Improved total organic fluorine methods for more comprehensive measurement of PFAS in industrial wastewater, river water, and air](https://doi.org/10.1016/j.watres.2023.119859), *Water Research* 235, 119859. Targeted LC-MS/MS and CIC-based total organic fluorine provide complementary coverage; CIC by itself does not speciate fluorine.
3. Lin et al. (2026), [Matrix effects on fluorine mass balance during simulated incineration of PFAS-laden solids](https://doi.org/10.1038/s44454-026-00042-4), *npj Emerging Contaminants* 2, 26. Its PFOS/fluoride spike recoveries across GAC, ion-exchange resin, soils, and mineral matrices show why background and matrix recovery must be measured before interpreting fluorine closure.

Scope note: literature pages/abstracts and the primary full-text pages were checked for these specific method/comparator claims. This is not an exhaustive novelty search or an experimental validation.
