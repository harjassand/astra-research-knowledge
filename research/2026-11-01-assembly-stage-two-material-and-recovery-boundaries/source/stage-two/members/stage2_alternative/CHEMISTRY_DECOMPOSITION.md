# Separately deprotect the PTC patches, then restore the native backbone

## Decision

The strongest refinement is to replace the proposed 80-nt patch at positions 2437–2516 with a **52-nt D/Ψ patch and a 28-nt dense mixed patch**, join them covalently, and retain the ordinary magnesium/temperature reconstitution baseline. This localizes the critical chemistry experiment and avoids exposing D to the ho5C synthesis/deprotection workflow. It does **not** establish that the dense four-modification patch has already been made.

I do not presently claim that a ligation splint can select the productive ribosome assembly path. An aligned, ligatable nick is a local chemical condition. A misfolded RNA can satisfy that condition, and a globally productive fold can hide its nick. Removing the splint also removes its imposed geometry. Neither the DALI results nor the modified-nucleotide extension results demonstrate global fold discrimination, reusable resetting of a chemically intact 23S ribosome, full translation fidelity, or working lifetime.

## Exact practical refinement

Positions refer to the 2,904-nt ENA V00331.1 reference already checked against 4YBB entity 22. G2445 remains unmodified during chemical manufacture and is later methylated by RlmKL.

| Patch | Positions | Length | Marks |
|---|---|---:|---|
| DP52 | 2437–2488 | 52 nt | D2449, Ψ2457 |
| DENSE28 | 2489–2516 | 28 nt | Cm2498, ho5C2501, m2A2503, Ψ2504 |

The modification-annotated sequences are:

```text
DP52
GUACUCCGGGGA[D]AACAGGC[Psi]GAUACCGCCCAAGAGUUCAUAUCGACGGCGG

DENSE28
UGUUUGGCA[Cm]CU[ho5C]G[m2A][Psi]GUCGGCUCAUCA
```

The new bond is after G2488, before U2489. Both nick termini are canonical ribonucleotides with the usual 3′-OH/5′-phosphate chemistry. Cm2498 is inside the right 12-nt splint flank, so the original calculation for modification-free local duplexes cannot be copied to this junction. Full-length product purification and chemical qualification remain necessary.

### What chemistry precedent actually supports

Gasparutto et al. chemically synthesized a natural *E. coli* alanine tRNA containing D, ribothymidine and Ψ and measured alanine acceptance. This earns coexistence of D and Ψ in one chemically synthesized RNA under a compatible protection scheme; it is not evidence that this exact 52-mer has the same recovery. [Gasparutto1992]

Küpfer and Leumann synthesized ho5C-containing 12- and 31-nt RNAs, using a photoremovable nitrobenzyl group. The reported workflow includes ammonia/ethanol deprotection followed by fluoride and photodeprotection. Thus 28 nt is within an experimentally demonstrated ho5C oligo length range. It does not follow that Cm, m2A and Ψ can be combined with ho5C using that workflow without validation. Separately deprotecting DP52 prevents its D residue from being subjected to this untested combination. [Kupfer2011]

Agris et al. reported m2A phosphoramidite incorporation and a mixed yeast-tRNA anticodon fragment containing Cm, Gm, m1G, Ψ and m5C. These are useful compatibility precedents, but neither that work nor the ho5C paper proves the DENSE28 mixture. [Agris1995]

The immediate constructive experiment is therefore a **chemically verified DENSE28**, followed by the single added canonical G|U ligation. The 80-mer is no longer the smallest substrate on which mixed chemistry must be resolved. Site identity, modification retention, absence of damaged D in the separately processed fragment, and the exact joined sequence should be established before interpreting ribosome assembly failure. DENSE28 success would still leave the other mixed patches in the complete construction to qualify.

## Counts and exact RNA-feed accounting

The whole 23S construction changes from 9 chemical patches plus 10 IVT spacers to **10 chemical patches plus 10 IVT spacers**. Total chemically supplied sequence remains 386 nt; IVT sequence remains 2,518 nt. There are **20 fragments and 19 joins**, one extra join relative to the original design.

A balanced grouping is 20 → 7 → 3 → 1. It has **10 ligation operations: nine ternary and one binary**, with a maximum of three purified tiers. The binary first-tier product spans 2540–2904 and is carried through the second tier, then joined at the final tier. The first 2,539 nt consequently traverse three operations; the last 365 nt traverse two.

Let `u` be an assumed common net ligation yield times purification recovery. Exact matched-feed cost is:

```text
Total input nt per recovered full-length RNA = 2539/u^3 + 365/u^2
Chemical input nt                          =  308/u^3 +  78/u^2
```

At the purely illustrative `u = 0.272 × 0.8 = 0.2176`, the totals are **254,134.309 input nt**, of which **31,540.628 are chemically synthesized** and **222,593.681 are transcribed**. Equal molar input loading still has a limiting output fraction `u^3 = 1.03033%`.

These are accounting results, not an rRNA yield prediction. The small reduction from the original 255,315.035-nt ledger is a tree-grouping effect: a 78-nt chemical tail moves from three operations to two while the final 287-nt IVT tail moves from one to two. It is not evidence that an added bond improves yield. If the binary and ternary operations have different net yields `u2` and `u3`, replace the second term by `365/(u2*u3)`.

Successful-product ligation stoichiometry increases from at least 18 to at least **19 ATP-dependent joining events**. RlmKL still requires at least two SAM methyl donations. Initial synthesis loss, terminal processing, futile ATP turnover, enzyme use, DNA splints and downstream assembly losses remain outside this RNA-feed ledger.

## Why complete separation into single-modification patches loses

For comparison, the program constructs an exact six-piece separation:

| Positions | Length | Mark |
|---|---:|---|
| 2437–2452 | 16 | D2449 |
| 2453–2487 | 35 | Ψ2457 |
| 2488–2499 | 12 | Cm2498 |
| 2500–2501 | 2 | ho5C2501 |
| 2502–2503 | 2 | m2A2503 |
| 2504–2516 | 13 | Ψ2504 |

This is an exact sequence decomposition, not six demonstrated ready-to-ligate products. It adds five joins, giving 24 global fragments and 23 joins. A direct 24 → 8 → 3 → 1 tree has 12 operations, still three tiers. Under a common assumed net operation yield, all leaves traverse three operations and the input cost is `2904/u^3`, or 281,851.233 nt at the illustrative `u` above.

The short-fragment problem is unavoidable under the single-modification-class restriction. Because ho5C is at 2501 and Ψ at 2504, a distinct contiguous m2A2503 piece can extend at most from 2502 to 2503. The code enumerates all 1,968 six-piece partitions and confirms that the best possible minimum fragment length is two nucleotides. Ordinary long-fragment splint ligation cannot be credited to this substrate merely by borrowing DALI's measured yield.

### An actual extension operation, and its boundary

Sudakov et al. used T4 RNA ligase 1 to add a modified nucleoside 3′,5′-bisphosphate, rSAP to remove the blocking phosphate, and splinted T4 RNA ligase 2 to join a second RNA. In a 61-nt model, the reported extension/dephosphorylation/splint-joining yields were D: >95%/83%/64%; Ψ: 56%/41%/90%; Cm: >95%/56%/27%. The stages were not all measured after product purification. ho5C and m2A were not among the tested modifications. [Sudakov2023]

One possible local adaptation would join the first three pieces to a 63-mer, append a blocked U-ho5C dinucleotide, dephosphorylate, append a blocked G-m2A dinucleotide, dephosphorylate, then join the final Ψ-containing 13-mer. Keep the initial precursor 5′-OH to suppress self-circularization and phosphorylate the final 80-mer before global joining. This would add four local ligation operations, two dephosphorylations and one final 5′-phosphorylation, and introduces Rnl1, rSAP and PNK as explicit protein services.

This adaptation is **not earned**: exact blocked-dinucleotide synthesis, dephosphorylation at the unusual terminal bases, and joining across the ho5C/m2A/Ψ contexts have not been demonstrated by the retrieved primary evidence. The validated modified-nucleotide operation is a reason to investigate the adaptation, not permission to substitute its yields.

For local stage retentions `a,h,m,f`, the exact conditional RNA input per recovered 80-mer is `63/(a*h*m*f) + 2/(h*m*f) + 2/(m*f) + 13/f`. The accompanying executable ledger includes every added stage and the zero-yield possibility. This expensive unresolved branch is why the DP52/DENSE28 split is the preferred practical refinement.

## Scientific judgment relative to native reconstitution

The refinement wins on **localizing a real chemical uncertainty** without changing the native sequence or leaving a backbone gap. It requires only one new canonical junction in the main route and supplies a short substrate on which the missing mixed chemistry can be resolved directly.

It loses to native-RNA reconstitution on demonstrated capability: no manufactured continuous 23S substrate here has yet earned full translation, error rates or usable lifetime. Chemistry qualification does not erase possible folding-history effects. Nor does successful local ligation create an assembly selector. Aoyama's recombinant-protein/native-RNA physical cycle remains the evidence-backed assembly baseline; our intervention changes the RNA supply, with all downstream functional gates retained.

## Primary sources and computation

- Gasparutto et al.1992. *Chemical synthesis of a biologically active natural tRNA with its minor bases*. DOI [10.1093/nar/20.19.5159](https://doi.org/10.1093/nar/20.19.5159), [PMID1383941](https://pubmed.ncbi.nlm.nih.gov/1383941/).
- Küpfer and Leumann2011. *Synthesis, base pairing properties and trans-lesion synthesis by reverse transcriptases of oligoribonucleotides containing the oxidatively damaged base 5-hydroxycytidine*. DOI [10.1093/nar/gkr673](https://doi.org/10.1093/nar/gkr673), [PMC3241664](https://pmc.ncbi.nlm.nih.gov/articles/PMC3241664/).
- Agris et al.1995. *Site-selected introduction of modified purine and pyrimidine ribonucleosides into RNA by automated phosphoramidite chemistry*. DOI [10.1016/0300-9084(96)88115-6](https://doi.org/10.1016/0300-9084(96)88115-6), [PMID7599270](https://pubmed.ncbi.nlm.nih.gov/7599270/).
- Sudakov et al.2023. *Site-Specific Labeling of RNAs with Modified and 19F-Labeled Nucleotides by Chemo-Enzymatic Synthesis*. DOI [10.1002/chem.202203368](https://doi.org/10.1002/chem.202203368). Table1 and the 3′-extension/dephosphorylation/splinted-ligation sections are the direct source of the operation and yields.
- Aoyama et al.2022, DOI [10.1093/jb/mvab121](https://doi.org/10.1093/jb/mvab121), and Xu et al.2025, DOI [10.1093/nar/gkae1280](https://doi.org/10.1093/nar/gkae1280), remain the assembly and long-fragment ligation baselines in `PROPOSAL.md`.

Run `python scripts/refine_cluster_patch.py` for the preferred two-patch refinement, and `python scripts/decompose_cluster.py` for the six-piece obstruction and alternative stage ledger. Both use captured sequence data and Python's standard library. Outputs include exact sequences, modification maps, operation trees, per-leaf input quantities and explicit unearned operations. No calculation is presented as a new experimental demonstration.
