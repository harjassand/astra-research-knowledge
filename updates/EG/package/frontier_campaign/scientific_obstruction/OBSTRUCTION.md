# Candidate obstruction: scalable stress steering for garnet solid-state batteries

> **Correction — 12 October 2026:** The original report materially mischaracterizes Cui et al.’s stress source as a dedicated external fixture and treats removing it as the unresolved transfer problem. Their Ni–Ti–Nb shape-memory-alloy ring contracts around the LLZO pellet and remains installed during cell assembly and cycling. The ring is the tensile balancing member for the pellet’s in-plane compression: this is already a self-equilibrated shrink-fit architecture. A retained ring is still an inactive packaging component, but it is not a force-maintaining external press. The proposed “replace the external fixture with a self-equilibrated tensile scaffold” operation therefore has no novelty as stated. A 2024 patent application also directly discloses sintered LLZO compression skins balanced by a tensile LLZO core; see [PRESTRESS_TRANSFER.md](PRESTRESS_TRANSFER.md) for the geometry, measured stress/transport data, source-access record and prior-art check. The original scouting text below is preserved as historical material; its external-fixture premise and verdict are superseded. Its statement that the high-capacity 100 mA cm⁻² supplementary sequence was not exposed is also superseded by the protocol in Supplementary Fig. S21. **The bold verdict immediately below is the historical verdict retained verbatim; the correction supersedes it.**

**Verdict:** one credible, consequential materials/manufacturing opening survives a primary-literature check. This is a candidate for a targeted strongest-worker pass, not a new capability claim. The broad chemo-mechanical explanation is already being pursued in a recent preprint, so the valuable opening is the experimentally testable design/transfer question below.

## Task contract and evidence boundary

Question: can a manufacturable, chemically robust residual-stress field keep lithium cracks from traversing a garnet separator at practically relevant current and areal capacity, while preserving lithium-ion transport and avoiding costly external clamping?

The requested evidence is a current primary-literature audit plus an explicit mathematical construction/counterexample. No experiment, atomistic calculation, device model, proof, novelty search beyond the sources listed here, or physical validation was performed. “Best method” below means strongest directly relevant demonstration located in this scout.

The Astra route was pinned to `787ab8b8ec23d17d4ab44a5cf2af602e5050355b`. I read the start file, the on-demand workflow and access notes, and the materials lexical shard. The shard exposed N707 (solid-iron transport), which I screened and excluded: its card is explicitly `source_derived_unreviewed`, concerns a different process, and is not used as a premise. The separate Astra checkout was already dirty; I did not change it. All writing for this scout is in this directory.

## The obstruction

Lithium metal can plate into microscopic flaws in oxide garnet electrolytes, pressurize them, and drive a crack through the separator, shorting the cell. A direct mitigation appeared in July 2026: impose biaxial compression in the plane of an LLZTO separator, orthogonal to the electric field, so the growing lithium cracks turn sideways instead of crossing the separator.

That result leaves a consequential transfer problem. The paper’s demonstrated field is about 330 MPa and is applied by a dedicated mechanical fixture. Its main current sweep reaches 100 mA cm⁻², but uses half-cycle capacities of 0.05 mAh cm⁻² up to 50 mA cm⁻² and 0.1 mAh cm⁻² at 55–100 mA cm⁻². The latter is 3.6 seconds per half-cycle. Separately, it reports 2,000 cycles at 10 mA cm⁻² and 1 mAh cm⁻² per half-cycle. It also mentions a supplementary test up to 100 mA cm⁻² and 1 mAh cm⁻²; the retrieved primary-source text did not expose that test’s full duration/cycle count, so I leave those unknown. The demonstrated method is therefore promising, but does not yet establish a production-compatible stress field across a full separator, at practical capacity and high rate, with the fixture removed.

The difficulty is now coupled: a separate 2026 operando study finds that fast-growing cracks in the same garnet family can propagate at stress intensities up to 75% below the purely mechanical fracture reference, and cryogenic STEM finds decomposition products with net molar-volume contraction. Another 2026 study images lithium filling crack tips, finds no measurable lithium nuclei ahead of the tip in its model geometry, and supports a large hydrostatic pressure mechanism. These observations need not contradict each other: they use different geometries and regimes. They do show that an operation designed against a purely mechanical threshold may not remain effective when crack-tip chemistry changes the local stress or fracture resistance.

## Strongest methods and their exact scope

- **In-plane biaxial compression and crack deflection.** Cui et al., [Nature 655, 631–637 (2026)](https://doi.org/10.1038/s41586-026-10734-x), apply biaxial compression orthogonal to the field in LLZTO. They report no through-thickness cracks in 32 compressed samples, lateral cracks throughout the separator, and localized lithium deposits near grain-boundary junctions and pores under extreme cycling. The 100 mA cm⁻² sweep is short-capacity; the 2,000-cycle point is 10 mA cm⁻² at 1 mAh cm⁻². This is the strongest direct system operation found.
- **Electrochemically assisted crack growth.** Fincher et al., [Nature 652, 906–911 (2026)](https://doi.org/10.1038/s41586-026-10279-z), use operando birefringence to measure the stress field and crack-tip intensity in Ta-doped LLZO. At higher current and crack velocity, propagation occurs at up to 75% lower stress intensity than the mechanical reference. Cryo-STEM finds new phases and net volume contraction. Their supplementary analysis already estimates that a 75 nm transformed layer with about 7% contraction can account for much of the observed intensity reduction; the scout does not present that mechanism as a new theory.
- **Mechanically filled-crack propagation.** Zhang et al., [Nature 652, 912–918 (2026)](https://doi.org/10.1038/s41586-026-10415-9), use a 150 μm in-plane LLZTO model geometry, cryogenic microscopy, and fracture modelling. They observe lithium filling nanoscale crack tips and no detectable lithium ahead of the tip; the model reaches roughly 600 MPa hydrostatic stress in confined lithium. Transverse voids redirect a crack in the model geometry. This establishes a physical steering proof of concept, not a manufactured separator.
- **Grain-boundary charge control.** [Nature Nanotechnology (2026)](https://doi.org/10.1038/s41565-026-02206-0) reports a −0.15 V grain-boundary potential at 20 °C, 30-fold higher electronic conduction than bulk, and oxygen-activity/dopant processing that raises the reported intrinsic critical current density to 1 mA cm⁻². This is a separate initiation mechanism/material knob; the operation’s interaction with biaxial stress and crack-tip phase change has not been tested here.
- **Compressive ion-exchanged surface layers.** Morris et al., [Advanced Energy Materials (2026)](https://doi.org/10.1002/aenm.71296), report 300 MPa–1 GPa stress from Ag⁺/Li⁺ exchange and a threefold increase in critical current density. Their abstract explicitly identifies diffusion kinetics versus electrolyte decomposition as process tradeoffs. This offers a possible route away from an external clamp, but it is a surface layer and does not establish the full-thickness in-plane stress field used by Cui et al.

## Mathematical opening

The next useful object is a robust, orientation-aware crack-steering criterion under both an eigenstress field and a current-dependent transformed tip region. In linear elasticity, for a given crack path \(\Gamma\), use the conditional form

\[
G_{\rm mech}(\Gamma;\sigma^*) + W_{\rm rxn}(\Gamma;\chi,j)
\;\ge\; G_c(\Gamma;\chi,q),
\]

where \(\sigma^*\) is the manufacturable residual/eigenstress field, \(\chi\) is local transformed-phase fraction, \(q\) is grain-boundary charge state, and \(j\) is current. The left chemical term is a trial interface contribution, not a settled constitutive law. The design task is to find a realizable \(\sigma^*\) that routes every admissible crack path laterally while satisfying a lower bound on through-plane ionic conductivity and a process/stack-pressure budget. The crucial missing service is a worst-path certificate or counterexample for heterogeneous stress, grain-boundary topology, and phase-dependent toughness together.

One sharp dimensional check follows from the reported largest reduction. If propagation occurs at \(K_I=0.25K_c\), as in the maximum 75% reduction, and the usual linear-elastic relation \(G\propto K_I^2\) applies at fixed geometry and modulus, then the purely mechanical energy term is only \(1/16\) of its reference value. An additive chemical contribution would have to supply at least \(15/16\) of the reference fracture energy, or the effective fracture resistance must fall to at most \(1/16\). This is conditional on interpreting the measured reduction as a reduction in \(K_I\), which is how the article presents its crack-tip analysis; it is not a universal bound independent of model assumptions.

## Nonstandard construction / counterexample

Compare two equal-area, two-lane separators with the **same mean in-plane compressive stress** \(-P\):

- uniform lane stresses \((-P,-P)\);
- a heterogeneous field \((-2P,0)\), with the zero-compression lane aligned with a connected grain-boundary/flaw path.

Both pass a mean-stress specification, but only the second leaves a full-thickness path with no compressive shielding. In a minimal local-response model, let the crack-opening intensity in lane \(i\) be \(K_i=K_{\rm load}+\lambda\sigma_i\), with \(\lambda>0\) and compression \(\sigma_i\le0\). For any \(K_c<K_{\rm load}<K_c+\lambda P\), the uniform field makes both lanes subcritical, whereas the heterogeneous field leaves its zero-stress lane supercritical, despite the same mean stress. A lower local toughness \(K_c^{\rm eff}(\chi)\) from a transformed tip only widens this failure interval. The construction proves that mean stress alone cannot certify safety. It can be assigned the same bulk ionic conductivity in both specimens; matching a bulk conductivity or a coupon-average critical current measured at another scale still does not certify the local weakest path. A real claim must resolve the local stress/GB/crack graph and the phase-dependent crack-tip term.

This is a counterexample template, not an experimentally established failure result. A direct falsifier is a matched LLZTO test in which a mapped, deliberately heterogeneous field and a uniform field have equal mean stress, current, capacity, chemistry, porosity, and interface preparation. If local crack paths and shorting statistics are indistinguishable after accounting for phase transformations, this particular weakest-lane mechanism fails.

## Targeted next gate

First, reconstruct the Cui paper’s stress geometry, exact capacities, fixture load path, and the Fincher paper’s crack-tip phase/volume analysis from full text and supplement. Then preregister one small-pellet experiment: measure the full stress field, compare uniform versus equal-mean heterogeneous stress, and cycle at both the paper’s 10 mA cm⁻² / 1 mAh cm⁻² condition and the 100 mA cm⁻² short-capacity condition. Record crack orientation and every short; use arrested-tip cryo-STEM to test whether the reaction-zone term changes the steering threshold. The first pass criterion is reproducible lateral steering with no vertical crack and no loss of conductivity under both conditions; only then test ≥3 mAh cm⁻² and manufacturing-scale stress generation.

The key costs to charge are fixture or stress-processing energy and materials, Li inventory, pellet area and separator thickness, pressure uniformity, lithium-ion transport loss, chemistry/decomposition, and the run time/number of cycles. No evidence here establishes economics, pack-scale safety, commercial readiness, or a novel material.

## Novelty and confidence limits

An August 2026 ResearchGate-indexed preprint titled *Confined Electrodeposition Fracture: A Chemo-Mechanical Theory Reconciling Mechanically Driven and Corrosion-Assisted Lithium Dendrite Penetration in Ceramic Solid Electrolytes* explicitly attempts a combined theory. I could not locate a stable repository identifier or a primary-hosted version during this pass. I therefore do not claim that a combined chemo-mechanical equation is novel. The candidate contribution is narrower: test and optimize a manufacturable stress-steering operation against current-dependent chemistry, on matched full-capacity regimes. That transfer question also remains unverified.

## Primary sources

1. Cui et al. (2026), *Dendrite initiation and deflection in biaxially stressed solid electrolytes*, Nature 655, 631–637. [DOI](https://doi.org/10.1038/s41586-026-10734-x); [source data](https://doi.org/10.5281/zenodo.20373114).
2. Fincher et al. (2026), *Electrochemical corrosion accompanies dendrite growth in solid electrolytes*, Nature 652, 906–911. [DOI](https://doi.org/10.1038/s41586-026-10279-z).
3. Zhang et al. (2026), *Mechanically driven Li dendrite penetration in garnet solid electrolyte*, Nature 652, 912–918. [DOI](https://doi.org/10.1038/s41586-026-10415-9).
4. *Charged grain boundaries limit short-circuit endurance in garnet solid-state battery electrolytes* (2026), Nature Nanotechnology. [DOI](https://doi.org/10.1038/s41565-026-02206-0).
5. Morris et al. (2026), *Critical Length Scales to Inhibit Dendritic Fracture in Ion-Exchanged LLZTO*, Advanced Energy Materials. [DOI](https://doi.org/10.1002/aenm.71296).
