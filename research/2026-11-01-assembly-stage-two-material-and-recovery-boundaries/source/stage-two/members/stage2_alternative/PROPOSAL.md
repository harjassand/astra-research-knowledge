# A covalent, chemically specified 23S route

## Status and central idea

This is an independently constructed experimental route, with an executable sequence and resource audit. It is not a new experimental demonstration. The decisive unearned step is productive, full-function assembly from the manufactured RNA.

**Chemistry refinement:** `CHEMISTRY_DECOMPOSITION.md` replaces the difficult 80-nt patch with a 52-nt D/Ψ patch plus a 28-nt Cm/ho5C/m2A/Ψ patch. This adds one join (20 fragments, 19 joins) and localizes the unproven mixed chemistry; it does not demonstrate that mixture. The original nine-patch construction and its independent ledger audit below remain preserved as the baseline. The refinement has its own exact tree and resource ledger in `data/refined_cluster_route.json`.

Preserve the native *E. coli* 23S sequence and its continuous phosphodiester backbone. Manufacture its modification pattern from nine short, chemically synthesized patches and ten transcribed spacers, seal all 18 junctions, remove the DNA assembly splints, and install two remaining methylations with recombinant RlmKL. Then combine this RNA with synthetic 5S RNA and the individually purified 33-protein large-subunit mixture using the established magnesium/temperature cycle. Couple the result to a transcribed-16S, recombinant-21-protein small subunit and defined translation components.

The physical mechanism is **template-directed covalent manufacture followed by ordinary ribosome assembly**. Chemical patches supply the local stacking, hydration and steric properties normally supplied by rRNA modification enzymes. DNA/RNA hybridization aligns real 3′-OH and 5′-phosphate ends; a ligase forms native backbone bonds. The splints are removed before assembly. There is no assumed helper capable of recognizing every productive folding state.

The substantive gain, if it works, is removal of native ribosomal RNA and an unspecified extract from the productive path. It exchanges numerous biological maturation activities for chemically specified inputs and a small, explicit processing enzyme set. It does not make the chemical inputs renewable by the protein synthesis system.

## Why this starting point is more defensible than a minimal PTC patch

Aoyama et al. demonstrated full-length sfGFP using 50S particles assembled from native 5S/23S RNA and 33 individually purified recombinant proteins, coupled to transcribed 16S and 21 recombinant small-subunit proteins. Their two-step physical assembly is the baseline. Its activity remained below that of native ribosomes, so it establishes possibility rather than manufacturing performance. [Aoyama2022]

The famous 2445–2523 region was localized using a fragment reaction. It is not an earned minimal chemistry specification for initiation, processive elongation, accurate decoding, termination, recycling and long working life. Later work on native-derived RNA lacking several modifications found a much smaller fragment-reaction deficit and explicitly raised RNA fragmentation and the different remaining modification sets as explanations of the older result. [Bao2024]

A direct warning comes from chemically engineered Thermus large subunits: a gapped RNA supported peptide transfer but required covalent connection of its missing segment to recover release-factor-dependent peptide release. This is why an unsealed split scaffold is not the primary design. [Amort2007]

## Exact computed construction

The reference is ENA accession **V00331.1**, 2,904 nucleotides. The script checks that it matches RCSB 4YBB entity 22 after converting the deposited m3Ψ symbol to its parent uridine. This is a sequence identity check, not a claim that the crystal sample and any particular assembly preparation share identical modification occupancy.

Twenty-two modification identities and positions are cross-checked against the deposited entity sequence. The three additional mapped sites, D2449, ho5C2501 and Ψ2604, are supplied by the 2024 PTC modification table. Their absence from the older structure annotation is not interpreted as biochemical absence. [Ero2024]

| Synthetic patch, inclusive positions | Length | Marks installed in that patch |
|---|---:|---|
| 733–759 | 27 | m1G745, Ψ746, m5U747 |
| 943–967 | 25 | Ψ955 |
| 1606–1630 | 25 | m6A1618 |
| 1823–1847 | 25 | m2G1835 |
| 1899–1974 | 76 | Ψ1911, m3Ψ1915, Ψ1917, m5U1939, m5C1962 |
| 2018–2042 | 25 | m6A2030 |
| 2239–2263 | 25 | Gm2251 |
| 2437–2516 | 80 | D2449, Ψ2457, Cm2498, ho5C2501, m2A2503, Ψ2504 |
| 2540–2617 | 78 | Um2552, Ψ2580, Ψ2604, Ψ2605 |

The chemical patches account for **386 nucleotides**, or approximately 13.3% of 23S RNA. The remaining **2,518 nucleotides** occupy ten transcribed spacers. All sequence boundaries, canonical and modification-annotated patch sequences, the 18 junctions and the long DNA splint sequences are generated in `data/`.

The patch lengths are a deliberately simple coverage construction: every chemically installed mark is at least 12 nucleotides from a patch endpoint, and the maximum patch length is 80. This does not optimize sequence-dependent synthesis, compatibility of protecting groups, RNA folding or ligation yield. A second output varies the maximum allowed patch length and makes the increased number of junctions explicit.

This is a **25-site target**, not a claim of precisely reproducing a native modification mixture. ho5C2501 can vary in occupancy and should be bracketed with zero- and fully modified patch variants, then matched to a well-characterized native reference if equivalence is the goal. Enzymatic methylation occupancy must also be measured. Anaerobic-specific chemistry is outside this aerobic reference specification.

## A necessary correction to an attractive all-chemical story

Internal m7G is not treated as an established chemical-synthesis input: this investigation has not established a primary-source route for the required internal m7G patch. Primary cap-synthesis work documents the chemical challenge and uses enzymatic N7 methylation; cap chemistry is not evidence that an internal m7G23S patch can simply be ordered. The route therefore retains **one explicit rRNA modification enzyme: RlmKL**. [Thillier2012]

RlmKL installs m7G2069 and m2G2445 using SAM. Its known naked-RNA substrate preference dictates the order: seal and purify RNA, remove DNA, then perform methylation before adding ribosomal proteins. Kimura et al. demonstrated both marks on full-length naked 23S purified from ΔrlmKL cells, an otherwise native-derived modified substrate. They separately modified an in-vitro-transcribed domain V substrate, with greater than 90% endpoint modification, and documented H74-unwinding activity. This is an actual protein catalyst with experimentally bounded behavior, not an invented universal remodeling factor. Transfer to this chemically manufactured substrate with potentially different folding and modification occupancies remains a validation step. [Kimura2012]

Other unusual patch chemistries are not costless. Published synthesis exists for ho5C-containing RNA, D-containing RNA and the m3Ψ/Ψ pattern of helix 69. That establishes access to the building blocks or short products, not that the proposed mixed-modification 76–80-mers have already been synthesized. Each patch needs mass and site identity qualification. If D and ho5C protecting-group requirements conflict within the 80-mer, split it, deprotect the pieces separately and add the extra covalent joins to the ledger. [Kupfer2011; Nawrot2009; Chui2002]

## Preparation and assembly operation graph

1. **Make and qualify the nine modified oligos.** Native 3′–5′ linkages are the target. No triazole or phosphoramidate replacement is credited as equivalent. Confirm each uncommon modification after deprotection, including D ring integrity.
2. **Transcribe the ten spacers with sacrificial leaders and trailers.** Their actual terminal sequences must not be distorted to satisfy T7 initiation preferences. Established RNase-H processing with chimeric guides can produce exact 3′-OH/5′-phosphate termini; remove the processing enzyme and guides before any long DNA/RNA assembly hybrid is formed. [Lapham1996]
3. **Use a three-tier covalent assembly tree.** Nineteen fragments become seven pieces, then three, then one. There are nine three-fragment ligation operations and eighteen junctions. Only purified, correctly connected products advance. The code generates one sequence-defined dsDNA splint for each operation. This transfers the DALI principle to rRNA; DALI demonstrated two-, three- and four-fragment mRNA ligations, not this complete rRNA construction. [Xu2025]
4. **Remove splints and verify the continuous RNA.** A full-length band is necessary but insufficient. Check junction identity, native backbone chemistry, modification identity and occupancy, terminal chemistry and absence of residual DNA and RNase activity. A PCR product made from RNA is not itself a modification assay.
5. **Apply RlmKL plus SAM to naked RNA, then remove or quantify enzyme carryover.** Methylation and any remodeling contribution must not be conflated: no-SAM or inactive-enzyme controls distinguish them.
6. **Assemble using the established physical baseline.** Use recombinant structural proteins, synthetic 5S and the magnesium/temperature assembly cycle, then transfer to a compatible translation buffer. A transcribed small subunit removes the native-small-subunit scaffold from the productive path. The translation system still needs its explicitly supplied factors, tRNAs, aminoacylation and energy services. [Aoyama2022]

EngA/ObgE could later be tested as a way to consolidate the physical stages, but the route does not depend on transferring their native-component result to synthetic RNA without evidence. Their repair of EDTA-disrupted ribosomes does not establish repair of chemically damaged RNA. [Sato2026]

## Finite yield and thermodynamic limits

DALI reported approximately 31.8% yield for a structured two-fragment example and 27.2% for a three-fragment example. Neither is an estimate for this rRNA. The executable ledger makes three conditional yield scenarios explicit. If each purified tier has a three-fragment ligation yield `q` and recovery `r`, matched quantities of all inputs give a limiting output fraction `(q r)^3` for this tree. This is a pool-and-purify manufacturing model, not the probability that 18 independent bonds all succeed in one pot.

| Assumed yield per three-fragment operation | Assumed recovery | Calculated final fraction | Each fragment supplied per output RNA under equal-input loading |
|---:|---:|---:|---:|
| 27.2% | 80% | 1.03% | 97.1-fold |
| 50% | 80% | 6.4% | 15.6-fold |
| 80% | 80% | 26.2% | 3.81-fold |

The first row borrows a measured value from a different mRNA purely to expose consequences. The other rows are scenarios. We have not shown any of these yields for rRNA, recovered useful side products, or demonstrated repeated operation.

The equal-input loading is not the minimum input allocation for the actual tree. Its first eighteen fragments, spanning positions 1–2617, traverse three purified operations; the final 287-nt fragment enters only the last operation. For `u = qr`, the exact matched-feed RNA cost is therefore `2617/u^3 + 287/u` nucleotides per recovered full-length RNA. At `q=.272, r=.8`, that is **255,315.035 input nucleotides**, including **37,463.697 chemical-patch nucleotides**. Supplying every leaf in the same amount would instead consume 281,851.233 nucleotides and oversupply the final tail. `scripts/audit_ligation_ledger.py` independently verifies root's recursive ledger through leaf-to-root parent traversal. These figures already account for RNA loss through the specified ligation and purification yields; they do not account for initial fragment manufacture, processing, enzyme use, ATP turnover or splint DNA.

For each junction the program also emits a unique 24-nucleotide local complementary DNA sequence. Under the reference nearest-neighbor parameterization of Sugimoto et al., the isolated, unmodified RNA/DNA duplexes have calculated ΔG°37 between −40.514 and −27.061 kcal/mol. These are local duplex diagnostics, not the free energy of invading folded rRNA. The calculation includes no RNA unfolding penalty, tertiary contacts, protein occupancy, magnesium, crowding, strand-release kinetics or ligation catalysis. RNA/DNA hybridization is not universally more favorable than RNA/RNA pairing. The long DALI splint is an empirically supported preparation operation; it is not a proof that every rRNA fragment will expose its ends. [Sugimoto1995]

## What must be earned before claiming capability

**Chemical construction gate.** Recover continuous 2,904-nt material with the intended chemistry. The critical comparison is a native-RNA control cut and covalently resealed at the same positions under the same processing history. If that control fails, the manufacture process itself is incompatible with productive assembly and a synthetic folding claim is premature. An unmodified but identically ligated RNA controls the opposite confound: treatment history rather than chemical marks.

**Full translation gate.** Demonstrate multiple complete proteins with different lengths and sequence demands, full product mass and sequence coverage, start- and stop-codon dependence, release and recycling, and repeated products per ribosome. Reconstituted subunits must be responsible for the activity; fluorescence alone cannot exclude a small native-ribosome contaminant or establish processivity.

**Fidelity gate.** Quantify amino-acid misincorporation, reading-frame errors, start-site selection and stop-codon readthrough against the same defined reference system. A well-folded GFP molecule is compatible with a large amount of incorrect product. This route intentionally does not assume that an unmodified synthetic small subunit has native accuracy merely because it can produce protein.

**Lifetime and renewal gate.** After an initial activity measurement, wash or exchange substrates and test repeated translation intervals. Separate ribosome damage from exhaustion of energy, tRNA charging and translation factors. Count cumulative correct amino acids or full-length products per verified active particle, not hours of declining fluorescence in an unreplenished batch.

For a protein-side renewal calculation, let `v` be correct amino acids produced per active ribosome per second, `tau` its measured usable lifetime, `a` the fraction of productive capacity allocated to rebuilding the machinery, `C` the amortized amino-acid cost of its structural and service proteins, and `y` the probability that a stoichiometric rebuilt set yields a verified working machine. The necessary condition is `a v tau y / C > 1`. It is not sufficient: RNA, chemical monomers, templates, charged substrates and cofactors also have to be supplied at the corresponding rate. No values for `v`, `tau` or `y` of the proposed ribosome have been measured.

## Persistent services and material inputs

The rRNA manufacture protein services are at least T7 RNA polymerase, RNase H, T4 RNA ligase 2, DNase I and RlmKL; DNA preparation additionally requires a defined polymerase if PCR makes the splints. Their purification, functional lifetimes and replacement are separate from their being expressible from sequences. Exact-end guides and synthetic patches are recurring inputs. DNase-based splint removal consumes the splints; reuse is not assumed.

An ideal single 23S product contains 386 chemically supplied nucleotides and 2,518 transcribed nucleotides, and requires at least eighteen ATP-dependent ligation events and two SAM methyl donations. This is only the successful-product stoichiometry; it excludes synthesis losses, failed ligations, hydrolysis, leaders/trailers, DNA manufacture, purification and assembly failures. The full ribosome additionally requires synthetic/transcribed 5S and 16S RNA, the 54 structural protein species with correct stoichiometries, and all translation services. Supplied tRNA modifications are not silently counted as renewable.

The system can, in principle, make replacement protein catalysts. It cannot synthesize the protected chemical monomers or operate a phosphoramidite synthesizer. Thus the achieved claim, if the experiments succeed, would be **a reduction in externally supplied biological assembly services with a declared recurring chemical manufacturing dependency**. Closure from the four canonical NTPs alone remains a different unsolved goal.

## Strongest failure and why the experiment remains useful

The strongest failure is chemically correct, continuous RNA that never enters a sufficiently productive folding pathway, or yields a fragile/low-fidelity particle. The fact that native-derived RNA works with recombinant proteins does not prove that chemical identity erases assembly history. Native modification enzymes can also act as chaperones, so chemical substitution does not automatically replace those physical functions.

The experiment is nevertheless constructive: it directly manufactures a complete candidate substrate instead of asking a hypothetical helper to supply unknown recognition. Its matched controls divide failure into chemical damage, missing chemistry, folding history, structural protein quality and downstream translation demands. A successful full25 construction would provide a sequence-defined baseline from which individual modifications or assembly factors could actually be removed; the smaller `core_plus_RlmKL` and `ptc13` constructions are supplied for those comparisons, without claiming that their sufficiency has already been earned.

## Sources

- **Aoyama2022:** Aoyama et al., *In vitro reconstitution of the Escherichia coli 70S ribosome with a full set of recombinant ribosomal proteins*. DOI [10.1093/jb/mvab121](https://doi.org/10.1093/jb/mvab121), [PMC8863084](https://pmc.ncbi.nlm.nih.gov/articles/PMC8863084/).
- **Xu2025:** Xu et al., *One-pot ligation of multiple mRNA fragments on dsDNA splint advancing regional modification and translation*. DOI [10.1093/nar/gkae1280](https://doi.org/10.1093/nar/gkae1280), [PMC11707544](https://pmc.ncbi.nlm.nih.gov/articles/PMC11707544/).
- **Kimura2012:** Kimura et al., *Base methylations in the double-stranded RNA by a fused methyltransferase bearing unwinding activity*. DOI [10.1093/nar/gkr1287](https://doi.org/10.1093/nar/gkr1287), [PMC3351187](https://pmc.ncbi.nlm.nih.gov/articles/PMC3351187/).
- **Ero2024:** Ero et al., *Ribosomal RNA modification enzymes stimulate large ribosome subunit assembly in E. coli*. DOI [10.1093/nar/gkae222](https://doi.org/10.1093/nar/gkae222), [PMC11194073](https://pmc.ncbi.nlm.nih.gov/articles/PMC11194073/).
- **Bao2024:** Bao et al., *Translational impacts of enzymes that modify ribosomal RNA around the peptidyl transferase centre*. DOI [10.1080/15476286.2024.2368305](https://doi.org/10.1080/15476286.2024.2368305), [PMC11221467](https://pmc.ncbi.nlm.nih.gov/articles/PMC11221467/).
- **Amort2007:** Amort et al., *An intact ribose moiety at A2602 of 23S rRNA is key to trigger peptidyl-tRNA hydrolysis during translation termination*. DOI [10.1093/nar/gkm539](https://doi.org/10.1093/nar/gkm539), [PMC1976462](https://pmc.ncbi.nlm.nih.gov/articles/PMC1976462/).
- **Lapham1996:** Lapham and Crothers, *RNase H cleavage for processing of in vitro transcribed RNA for NMR studies and RNA ligation*. [PMID8608452](https://pubmed.ncbi.nlm.nih.gov/8608452/).
- **Chui2002:** Chui et al., *Synthesis of helix 69 of Escherichia coli 23S rRNA containing its natural modified nucleosides, m(3)Psi and Psi*. [PMID12467398](https://pubmed.ncbi.nlm.nih.gov/12467398/).
- **Kupfer2011:** Küpfer and Leumann, *Synthesis, base pairing properties and trans-lesion synthesis by reverse transcriptases of oligoribonucleotides containing the oxidatively damaged base 5-hydroxycytidine*. DOI [10.1093/nar/gkr673](https://doi.org/10.1093/nar/gkr673), [PMC3241664](https://pmc.ncbi.nlm.nih.gov/articles/PMC3241664/).
- **Nawrot2009:** Nawrot et al., *Preparation of Short Interfering RNA Containing the Modified Nucleosides 2-Thiouridine, Pseudouridine, or Dihydrouridine*. DOI [10.1002/0471142700.nc1602s37](https://doi.org/10.1002/0471142700.nc1602s37).
- **Thillier2012:** Thillier et al., *Synthesis of 5′ cap-0 and cap-1 RNAs using solid-phase chemistry coupled with enzymatic methylation by human (guanine-N7)-methyl transferase*. DOI [10.1261/rna.030932.111](https://doi.org/10.1261/rna.030932.111), [PMC3312571](https://pmc.ncbi.nlm.nih.gov/articles/PMC3312571/).
- **Sato2026:** Sato et al., *Single-step in vitro reconstitution of the Escherichia coli ribosome mediated by two GTPase factors, EngA and ObgE*. DOI [10.7554/eLife.109916.4](https://doi.org/10.7554/eLife.109916.4), [PMC13278734](https://pmc.ncbi.nlm.nih.gov/articles/PMC13278734/).
- **Sugimoto1995:** Sugimoto et al., *Thermodynamic parameters to predict stability of RNA/DNA hybrid duplexes*. DOI [10.1021/bi00035a029](https://doi.org/10.1021/bi00035a029). Parameter data captured from [Biopython1.86](https://github.com/biopython/biopython/blob/biopython-186/Bio/SeqUtils/MeltingTemp.py).
- **Sequence records:** [ENA V00331.1](https://www.ebi.ac.uk/ena/browser/view/V00331.1), [RCSB4YBB](https://www.rcsb.org/structure/4YBB), [entity22 JSON](https://data.rcsb.org/rest/v1/core/polymer_entity/4YBB/22). Raw downloads and SHA256 hashes are preserved in `sources/` and `data/source_manifest.json`.

## Reproduce the computation

Run `python scripts/construct_patch_route.py` from this directory, or invoke the script by absolute path. Python's standard library is sufficient. The script reads captured public inputs, checks the reference and modification map, generates all sequence constructions, evaluates the conditional resource/yield calculations and writes `data/audit_summary.json`. The result is a finite construction and audit, not evidence that the proposed ribosome has been made.
