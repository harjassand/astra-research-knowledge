# Prestress transfer: decisive correction and prior-art check

**Decision: reject the proposed “replace the external clamp with a self-equilibrated tensile scaffold” operation as a novel mechanism.** Cui et al.’s retained shape-memory-alloy (SMA) ring is already a tensile member that compresses LLZO in plane. More directly, a 2024 published patent application describes and experimentally tests co-sintered LLZO compression skins balanced by an LLZO tensile core. Those results do not settle production-scale battery performance, but they close the proposed architectural novelty. No concrete advantage for a distributed internal scaffold over these precedents was specified or evidenced.

## Cui apparatus and what was measured

The primary article is Teng Cui et al., “Dendrite initiation and deflection in biaxially stressed solid electrolytes,” *Nature* 655, 631–637 (2026), [DOI/full-text page](https://doi.org/10.1038/s41586-026-10734-x) ([Nature article URL](https://www.nature.com/articles/s41586-026-10734-x)). Its official Supplementary Information is the [publisher-hosted PDF](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-10734-x/MediaObjects/41586_2026_10734_MOESM1_ESM.pdf).

In Methods, “Biaxial stress application,” the paper describes an approximately 11.9-mm-diameter, 1-mm-thick LLZO pellet surrounded by a Ni₃₈Ti₄₈Nb₁₄ SMA ring. The ring’s initial room-temperature inner diameter is about 12 mm. Heating through the transformation at 170 °C contracts the ring around the pellet; the article states that it “maintained its shrunken state after cooling to room temperature.” The reported inner diameters are 11.96 mm at 170 °C and 11.43 mm after cooling to room temperature. These are measurements at different temperatures, so the 0.53-mm difference should not be treated as an isothermal transformation stroke. A thin PEEK liner electrically isolates the ring. The ring stays installed during cell assembly and cycling: Supplementary Fig. S1 explicitly measures XRD “after cycling with ring,” and Fig. S3 shows the ring around the pellet in the cell, with 6-mm lithium pads and 5-MPa stack pressure. Thus the ring is an integrated, self-equilibrated load path; it is not a press removed before cycling. It remains an inactive packaging/volume cost, but the force does not depend on a separate operating press.

**Read receipt and access boundary.** The official Nature article URL and DOI are above. In the current web reader, the article page and its PDF redirect to Nature’s authorization page; the Methods text was checked in an indexed full-text copy, not independently retrieved from Nature during this turn. I do not cite that mirror as the source. The official SI PDF was retrieved and read in the preceding scout; the page/figure/table receipts below refer to that publisher PDF. The raw-data record is [Zenodo 20373114](https://doi.org/10.5281/zenodo.20373114), a 397.8-MB archive; I inspected its metadata but did not download the archive.

Supplementary Table S1 (PDF p. 24) reports XRD sin²ψ biaxial stress measurements, distinct from the nominal 330-MPa condition used to label the cycling/transport experiment:

| SI Table S1 specimen/state | XRD stress |
|---|---:|
| As received, sample 765 | 169 ± 14 MPa |
| As received, sample 1064 | 176 ± 5 MPa |
| Polished + heat treated | 91 ± 15 MPa |
| Polished + heat treated + ring | 420 ± 30 MPa |
| Ring removed | 133 ± 14 MPa |
| After cycling with ring | 450 ± 20 MPa |
| Polished + ring | 422 ± 8 MPa |
| Sample 7, side A / side B | 473 ± 21 / 375 ± 17 MPa |

The 4xx-MPa entries are XRD measurements in the specific Table S1 specimen/state; they are not the nominal 330-MPa cycling setting. They should not be averaged together or substituted for the nominal setting. Table S1 is a surface-sensitive measurement; circular symmetry is used to infer a largely equibiaxial state, and the 98-MPa side-to-side difference in sample 7 is a warning against calling the measured field spatially uniform through the whole pellet.

Supplementary Fig. S2 (p. 4) reports charge-transport measurements for the nominal 330-MPa treatment. Its electronic-conductivity plot is on the order-of-10⁻⁹ S cm⁻¹ scale. The out-of-plane Li⁺ activation energy changes from 0.37 eV (unstressed) to 0.40 eV (stressed). I did not extract exact pointwise conductivities from the plot, so no more precise conductivity claim is warranted here. Keep these transport conditions/values separate from Table S1’s measured residual stresses.

Supplementary Fig. S21 (p. 23) also resolves a gap in the old obstruction note: it specifies a capacity sweep from 0.1 to 1.0 mAh cm⁻², with ten cycles at each step through 0.8 and 100 cycles at 1.0, followed by a 10-to-100 mA cm⁻² current sweep at 1 mAh cm⁻² with ten cycles per current increment. The prior note’s claim that the high-capacity supplementary sequence was not exposed is superseded.

## The proposed self-equilibrated architecture is already disclosed

The closest exact prior disclosure is the public primary patent document [WO2024009109A1, “Solid electrolyte”](https://patents.google.com/patent/WO2024009109A1/en). Claim 1 specifies a solid electrolyte with surface first layer(s) in compression and a second layer in tension; claim 14 produces this state by heating a layered structure and cooling it, and claim 19 specifies co-sintering. The description explicitly identifies CTE mismatch as the mechanism: a lower-CTE surface layer is compressed while the higher-CTE internal layer is tensile (description §§ “Lamination” and “Example 1”).

The patent’s Al-LLZO/Ta-LLZO example gives CTEs of 7.9 and 9.2 × 10⁻⁶ K⁻¹, respectively. It reports a co-processed/sintered laminate, shorter Vickers cracks in its Al-LLZO surface layer than in monolithic Al-LLZO (45.9 ± 1.7 versus 52.7 ± 3.7 μm in one test), and an estimated 126-MPa surface compression in a second test series. The laminate’s reported room-temperature conductivity is 8.6 × 10⁻⁴ S cm⁻¹. Its Li symmetric-cell test uses 3-mm contacts and 0.1 mAh cm⁻² per half-cycle, increasing current by 0.01 mA cm⁻²; the reported failure currents are about 0.023 mA for the laminate and 0.004 mA for monolithic Al-LLZO. This is a very small-cell, low-areal-capacity demonstration, not production validation. But the proposal here is architectural novelty, and this is already a directly relevant co-sintered ceramic stress-balanced laminate with electrochemical testing. It therefore rules out presenting “compressed ceramic balanced by a tensile internal ceramic scaffold/skin” as a new operation.

Two further primary precedents close relabelings of the same stress-generation idea:

- Fincher et al., [“Controlling dendrite propagation in solid-state batteries with engineered stress,” *Joule* 6 (2022)](https://doi.org/10.1016/j.joule.2022.10.011), explicitly propose CTE-mismatch lamination as a way to build residual in-plane compression. The accessible [author manuscript](https://chemrxiv.org/engage/chemrxiv/article-details/62c71d91252b212a49ddd817) discusses LLZO/LFP and dissimilar-electrolyte laminates in “Engineering solid-state batteries for dendrite deflection.” That route is a proposed design in this paper, not its experimentally demonstrated load case; the later patent supplies a closely matching co-sintered LLZO laminate experiment.
- Yu et al., [“Dendrite suppression in garnet electrolytes via thermally induced compressive stress,” *Joule* 10 (2026)](https://doi.org/10.1016/j.joule.2025.102232), experimentally use a sustained through-thickness thermal gradient in LLZTO. The publisher’s article summary reports a temperature difference as low as 20 °C and nearly threefold higher critical current density, with stress checked by strain gauges and optical curvature. This is another direct stress-engineering operation, though it requires the maintained gradient and is not a passive stress-free internal scaffold.

The screened cold-sintering study, Lan et al., [“Cold Sintering Enables the Reprocessing of LLZO-Based Composites,” *ChemSusChem* (2024)](https://doi.org/10.1002/cssc.202301920), uses pressure/low-temperature processing to reprocess LLZO–polymer–salt composite electrolyte; it does not report engineered residual prestress or a dendrite-deflection test. This is not evidence that no cold-sintered prestress work exists, only that this directly inspected cold-sintering example is not one. The 2024 patent above is conventional co-sintering and is the decisive sintered-LLZO precedent.

The 2026 Ta-LLZO fiber-network paper, Weckelmann et al., [*Advanced Science*](https://doi.org/10.1002/advs.76063), reports an in-plane aligned porous ceramic network infiltrated by PEO/LiTFSI. It studies tortuosity and dendrite blocking; it does not report a residual tensile scaffold that prestresses a continuous ceramic separator. A fiber network as a structure is therefore not itself the proposed novelty, and no stress advantage for an internal network was identified.

## Equilibrium and the “tensile core” question

For a thin ring of radius $R$, thickness $t$, hoop tension $T=\sigma_\theta t$, and interface pressure $p$, radial force balance on a short arc gives

\[
T=pR,\qquad p=\frac{\sigma_\theta t}{R}.
\]

The ring’s tensile hoop stress balances the pellet’s radial/in-plane compression. That is already the root candidate’s essential force path; moving the tension-bearing member into the separator does not create a new stress operation.

For a free, flat, self-equilibrated laminate with no in-plane boundary traction and no bending resultant, the in-plane force resultants must satisfy

\[
\sum_k h_k\,\sigma_{xx}^{(k)}=0,
\qquad
\sum_k h_k\,\sigma_{yy}^{(k)}=0,
\]

where $h_k$ and $\sigma^{(k)}$ are layer thickness and residual stress. Thus compression skins imply balancing tension somewhere in the composite. That tension need not be in the ceramic core: a ring or internal tensile scaffold can carry it. A surface-compressed, unconstrained ceramic without such a separate load path generally needs a balancing tensile region; whether it is a dangerous central core depends on the actual depth profile and geometry. Consequently, “surface compression necessarily leaves a tensile ceramic core” is false as a universal claim, while the self-equilibrium constraint itself is real. The Cui ring and the patented CTE laminate instantiate the two already-known ways to place the balancing tension—in an added hoop member or in a tensile ceramic layer.

No concrete differentiator remains for the root candidate. A future project could separately compare ring versus laminate/network by active-area fraction, separator thickness, full-area stress uniformity, manufacturability, relaxation, conductivity, and high-capacity cycling. That would be a comparative engineering study of known architectures; it is not the new stress operation proposed here.

## Primary source list and read receipts

1. Cui et al. (2026), [Nature article / DOI](https://doi.org/10.1038/s41586-026-10734-x), [official SI PDF](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-10734-x/MediaObjects/41586_2026_10734_MOESM1_ESM.pdf), [raw-data record](https://doi.org/10.5281/zenodo.20373114). Read receipts: article Methods, “Biaxial stress application” and “Biaxial stress quantification”; SI Figs. S1–S3 (pp. 3–5), Fig. S21 (p. 23), Table S1 (p. 24), and transport Fig. S2 (p. 4). The official article web page redirected in this reader; SI PDF was directly read. Raw archive not downloaded.
2. [WO2024009109A1](https://patents.google.com/patent/WO2024009109A1/en), primary published patent document. Read receipts: claims 1, 14 and 19; description, “Lamination”; “Example 1”; and “Vickers indentation residual stress measurement” plus “Galvanostatic cycling.”
3. Fincher et al. (2022), [Joule DOI](https://doi.org/10.1016/j.joule.2022.10.011), [author manuscript](https://chemrxiv.org/engage/chemrxiv/article-details/62c71d91252b212a49ddd817). Read receipt: “Engineering solid-state batteries for dendrite deflection,” including the CTE-mismatch laminate discussion.
4. Yu et al. (2026), [Joule DOI](https://doi.org/10.1016/j.joule.2025.102232). Read receipt: publisher article summary/highlights and stress-validation description; no numerical MPa value is asserted here.
5. Lan et al. (2024), [ChemSusChem DOI](https://doi.org/10.1002/cssc.202301920). Read receipt: article description of LLZO–PPC–LiClO₄ composite reprocessing; no residual-stress or dendrite-steering result reported in that study.
6. Weckelmann et al. (2026), [Advanced Science DOI](https://doi.org/10.1002/advs.76063). Read receipt: abstract and synthesis/results description for electrospun, calcined Ta-LLZO network infiltrated with PEO/LiTFSI.
