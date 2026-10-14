# Follow-up: dual-template DNA-frame repair

## Verdict

A dual-template frame could support *sequence-agnostic, local repair* of a clean single-strand nick or short gap in either strand, provided the opposite strand is continuous across the gap, the damaged strand retains a usable upstream 3′-OH primer and downstream 5′-phosphate, and enzymes can reach the site. Polymerase copies the local sequence already present in the complementary strand; ligase closes the remaining nick. No site-specific repair oligo is needed.

That is a plausible extension of existing DNA repair chemistry, not yet a demonstrated general repair operation for DNA origami. It does not repair an absent whole staple (there is no primer), a double-strand break, a gap in both strands, a damaged/missing template, or all common chemically blocked termini without additional end-processing enzymes. Standard origami also does not provide a continuous complementary strand along every routed segment. The idea becomes experimentally testable if designed as a 2D repair frame with continuous complementary corridors and crossovers kept outside the polymerase path. The largest independent physical gate is enzyme access in folded origami: ligase reaches a practical limit in 3D even for clean, designed nicks.

## What has actually been shown

Scheckenbach et al. demonstrated autonomous self-healing of damaged staples by adding an excess pool of matching staples; scaffold damage remained outside that mechanism. Their 0.2% serum assay also showed some nonspecific sacrificial-DNA protection, while 10% serum degradation was too fast for specific self-healing to dominate. This is a strong comparator, not evidence for template-directed repair of scaffold breaks ([2021 paper](https://doi.org/10.1002/anie.202012986), especially its discussion of scaffold limitation).

Polymerase gap filling inside origami is already established for *designed* substrates. Agarwal et al. used T4 DNA polymerase to fill deliberately unpaired scaffold regions in wireframe structures; optimized filling took under 3 minutes and changed the structures’ shapes ([2018 paper](https://doi.org/10.1021/acsnano.7b08345)). Yan et al. used Q5 polymerase to extend at designed allosteric sites at 37 °C for 5 hours and used T4 ligase to join designed split effector staples at 16 °C for 17 hours. The component operations therefore work in origami, but they were directed to designed sites and used separate reaction conditions; the paper does not establish a shared-bath repair of random strand damage ([2020 paper](https://doi.org/10.1093/nar/gkaa488)).

End chemistry, not just sequence complementarity, determines whether that extension-and-seal sequence can run:

| Substrate at the damaged strand | Required operation |
|---|---|
| Clean nick, adjacent 3′-OH and 5′-phosphate | Ligase alone seals it; no nucleotide insertion is needed. |
| Short single-strand gap, upstream 3′-OH and downstream 5′-phosphate | Polymerase extends the 3′ end using the opposite strand and dNTPs; ligase seals the final nick. |
| 5′-OH end | Kinase activity plus ATP must first create a 5′-phosphate. |
| 3′-phosphate or 3′-phosphoglycolate | A suitable 3′-phosphatase/end-cleanup activity is required to restore 3′-OH; some damage also deletes a nucleotide. |
| Abasic site, oxidized base, crosslink, or blocked primer | Requires lesion-specific processing or can stall/miscode; generic gap fill alone is insufficient. |
| Double-strand break, missing whole staple, or coincident gaps in both paired strands | No intact local template/primer pair; this operation cannot reconstruct it. |

T4 DNA ligase specifically joins juxtaposed 3′-OH and 5′-phosphate ends. A primary in-vitro study showed mammalian PNK plus ligase I repairing 3′-phosphate/5′-OH nicks, and PNK + polymerase β + ligase I filling and sealing a 1-nt gap. The authors note that strand-break products have multiple terminal chemistries and must be restored to 3′-OH/5′-phosphate for synthesis and joining ([1998 NAR study](https://doi.org/10.1093/nar/26.19.4395)). This supports end-processing as an achievable extension, but not an all-in-one origami cocktail.

## Topology and crossovers

In standard origami, one long scaffold is paired by many short staple segments. A staple can template repair of a local scaffold gap only where a staple segment spans the full gap and the polymerase’s path; the reverse is true for a gap in a staple. Staple ends and crossovers partition the complementary coverage. A double-stranded-scaffold origami has used both constituent strands in one integrated object, but its two paths are intentionally asymmetric and periodically converge; that architecture does not by itself prove uninterrupted, enzyme-accessible template coverage at every base ([2012 paper](https://doi.org/10.1021/nn302896c)).

An origami crossover is a branched, four-strand junction. A polymerase can copy along its template strand in ordinary duplex DNA, but none of the repair demonstrations above establishes efficient polymerase transit through an origami crossover. Crossovers should therefore be outside the initial gap-repair corridor. If an arbitrary break lands at the junction, or the gap spans the crossover, repair and preservation of strand routing are unknown. Polymerase synthesizes a strand; it does not itself recreate a missing crossover or decide which alternate arm to follow.

Covalent crosslinks can preserve a folded topology after nicks: Gerling et al. placed thymidines at strand termini and crossover sites, then UV-induced CPD bonds to point-weld strands. Crosslinked multilayer origami resisted heat, low-cation buffers, and nucleases, and retained its crossover network ([2018 Science Advances paper](https://doi.org/10.1126/sciadv.aau1157)). These links are structural constraints, not an information-bearing repair guide. A CPD is itself a DNA lesion and crosslinks near a repair tract may block polymerase or ligase; put them at frame anchors away from repair corridors and test enzyme access. Near-quantitative 2024 ligation work also identifies tight physical access as a limitation: T4 ligase plus 20% DMSO improved 2D nick sealing, while 3D origami required chemical CNBr ligation because the enzyme-access problem persisted ([2024 paper](https://doi.org/10.1002/smtd.202300999)).

## Concrete achievable design

Start with a **2D frame**, not a dense 3D object. Lay out one or more long, uninterrupted duplex repair corridors. Each corridor should have a continuous complementary template over at least the maximum test gap plus flanking bases, one accessible 3′-OH primer, and an adjacent 5′-phosphate on the damaged strand. Put crossovers and thymine crosslinks outside these corridors. Use a sequence with no intended lesion or secondary structure in the track. Include matched damaged substrates in which the gap is introduced separately into the scaffold-derived strand and the staple-derived strand.

Run three substrates: (i) nick with 3′-OH/5′-phosphate; (ii) 1-, 3-, and 10-nt single-strand gaps with 3′-OH/5′-phosphate; (iii) blocked-end controls, 3′-phosphate and/or 5′-OH. Compare no enzyme, ligase only, polymerase only, polymerase + ligase, and end-cleanup + polymerase + ligase. Start with polymerase and ligase in sequential compatible buffers; separately test simultaneous incubation. A shared bath is a hypothesis because published origami work used a Q5 polymerase system at 37 °C and a T4 ligase system at 16 °C, while a later 2D ligation protocol used 37 °C, 0.5 mM ATP, 1× PNK buffer at pH 7.5, and 20% DMSO overnight. The DMSO ligation condition should not be assumed compatible with the polymerase. All staples in that ligation study were purified and 5′-phosphorylated before assembly; it was not repair of damaged sites in situ.

For a sequence-agnostic test, prepare at least two equally frequent site variants or randomize the gap location across the corridor and do not provide repair oligos. Quantify strand-length restoration by denaturing PAGE or capillary electrophoresis, correct ligation by an end-specific assay, sequence the repaired tract, and measure frame retention by AFM or cryo-EM. Assay both the original and repaired substrate after a nuclease challenge. Report repair per eligible lesion and total frame yield; do not count only intact survivors. The critical negative controls are gaps without an opposite continuous template, damage at a crossover, and an otherwise identical 3D-packed structure.

**Independent physical gate:** show that the enzyme actually reaches and traverses the designed corridor in the folded object. A practical success criterion is sequence-verified closure of ≥90% of accessible 1–3-nt clean gaps in each strand class, with no-template and crossover-spanning controls near background, while retaining the frame geometry. Then vary corridor depth/packing to map access loss. Failure in 3D would limit the claim to 2D or exposed corridors, regardless of a successful solution-phase duplex assay.

## Claim boundary

If the gate passes, the result would be random-location repair of *eligible single-strand gaps* in a deliberately redundant DNA frame, using generic enzymes and dNTPs rather than a sequence-specific oligo pool. It would not show general repair of arbitrary random molecular damage, every staple or scaffold loss, or autonomous repair without energetic/material inputs. Polymerization consumes dNTPs; ligation consumes ATP, and end cleanup may consume ATP. Any energy/throughput advantage over matching-staple replacement must count those reagents, enzymes, preprocessing, folding, purification, and measured repair yield against a matched incumbent. No such full-cost advantage is established here.

## Primary references

- Scheckenbach et al., “Self-Regeneration and Self-Healing in DNA Origami Nanostructures,” *Angew. Chem. Int. Ed.* 2021, DOI: [10.1002/anie.202012986](https://doi.org/10.1002/anie.202012986).
- Agarwal et al., “Structural Transformation of Wireframe DNA Origami via DNA Polymerase Assisted Gap-Filling,” *ACS Nano* 2018, DOI: [10.1021/acsnano.7b08345](https://doi.org/10.1021/acsnano.7b08345).
- Yan et al., “Allostery of DNA nanostructures controlled by enzymatic modifications,” *Nucleic Acids Research* 2020, DOI: [10.1093/nar/gkaa488](https://doi.org/10.1093/nar/gkaa488).
- Yang et al., “DNA Origami with Double-Stranded DNA as a Unified Scaffold,” *ACS Nano* 2012, DOI: [10.1021/nn302896c](https://doi.org/10.1021/nn302896c).
- Gerling et al., “Sequence-programmable covalent bonding of designed DNA assemblies,” *Science Advances* 2018, DOI: [10.1126/sciadv.aau1157](https://doi.org/10.1126/sciadv.aau1157).
- Krishnamurthy et al., “Near Quantitative Ligation Results in Resistance of DNA Origami Against Nuclease and Cell Lysate,” *Small Methods* 2024, DOI: [10.1002/smtd.202300999](https://doi.org/10.1002/smtd.202300999).
- Kuhn et al., “Repair of DNA strand gaps and nicks containing 3′-phosphate and 5′-hydroxyl termini by purified mammalian enzymes,” *Nucleic Acids Research* 1998, DOI: [10.1093/nar/26.19.4395](https://doi.org/10.1093/nar/26.19.4395).
