# Astra Chemistry: cooperative product footprints and a chemically separable donor guide

26 October 2026. Mathematical/computational continuation of the product-footprint and chemically quiet molecular writer. Not a chemical experiment, and no newly demonstrated synthetic capability. Executable verification: `astra_cooperative_footprint_compiler_20261026.py`.

## Physical change of priority

The current primary comparison identifies two different bond topologies.

- **Lee et al., Nucleic Acids Research 2026, DOI 10.1093/nar/gkag638**: assembly-triggered oxanine–amine covalent DNA crosslinks and chain-like DNA products. The donor DNA is permanently attached through the crosslink; its chemical and physical footprint can affect adjacent sites. No proof that three-body obstruction occurs in that particular system.
- **He & Liu, JACS 2011, DOI 10.1021/ja201361t**: a deliberately self-cleaving NHS-ester *DNA substrate* transfers its organic acyl group to a growing DNA-anchored amine. Aminolysis cleaves the substrate oligonucleotide's chemical linkage; a next DNA strand physically displaces the spent substrate strand. Six steps at 35% total conversion (~83% mean per step) were demonstrated. This is the closer mechanism for leaving no **covalently attached donor recognition strand** on the product. Importantly, hydrolysis may also consume an ester without productive transfer, and chemical cleavage of the guide linkage does NOT itself eject the spent strand from the DNA duplex. Strand displacement/washing remains a separate operation. Movement in that paper was externally scheduled and was not bond-qualified.
- **Schaub et al., Nature Catalysis 2026, DOI 10.1038/s41929-026-01576-x**: tailored CoA-ligase/N-acyltransferase cascades mediate broad on-DNA amide chemistry (>120 examples; >91% mean conversion in the constructed encoded library). Strong comparator for chemical diversity; no demonstrated sensorless distributed sequential polymer writer.

Selected proposed architecture (not acquired): permanently registered molecular scaffold with multiple independently addressable *primary-amine acceptors*; each incoming DNA-addressed donor contains a transferable organic acyl payload and a donor DNA recognition strand connected through a **self-cleaving leaving-group topology** rather than the product bond. After exposure, chemically inactive or unreacted donor strands are displaced/removed; rooted amides persist. A completed site consumes its sole targeted primary amine, making repeated feeding idempotent if the acylated cargo does not introduce a new accessible nucleophile. An unsuccessful competent site keeps its original amine. This is a distributed postsynthetic writer, not a claimed solution to arbitrary protected-terminal chain growth. Each site needs unique positional registration and right/wrong chemical-address selectivity, which have not been experimentally integrated.

## Finding A: pairwise assays can miss an absolute three-body deadlock

For target site j and reaction port p, define a collection of **minimal simultaneous blocking sets** B_{j,p}. The port is accessible after products with still-retained *steric guides* occupy set F iff no element H of B_{j,p} is a subset of F. Permanent product-guide footprints and monotonic steric blocking are assumed. The case H={i} is the previous pairwise graph model. H={i,k} is cooperative obstruction, unmeasured for oxanine chemistry.

Three sites 0,1,2, each with a single port, each has a blocking set consisting of the other two sites:

    B_0={{1,2}}; B_1={{0,2}}; B_2={{0,1}}.

All pairwise reactions can succeed in either order. Nonetheless, for **every** complete serial permutation the last site is completely blocked, so full success probability is zero even when all individual couplings would otherwise be certain. Verified by enumeration and subset-DP. Giving site 2 one second port insensitive to this blocking makes a successful schedule exist (0,1,2), but in an unobserved equal-rate asynchronous reaction exactly 2 of 6 sampled orders work, so reliability is 1/3. Existence of a good sequence does not ensure the physical reaction follows it.

General compiler: state (S,F) = completed product set and still-attached donor-guide footprint set. Site j may react when prerequisites are complete and at least one port is unblocked. After successful reaction, a guide may either remain (F←F∪{j}) or be physically removed (S←S∪{j}, F unchanged). A finite DP minimizes the number of assumed perfectly safe guide releases. On the symmetric triple, minimum release count is 1, or zero if site 2 has the extra safe port. This describes **existence with outcome-aware scheduling** and must not be mistaken for an autonomous protocol lacking a bond receipt.

## Finding B: release minimization has an exact graph-theoretic characterization

For single ports with only pairwise permanent blockages, no chemical prerequisites, and immediate release of a selected product's DNA footprint after success, the minimum number of distinct product-guide releases needed to admit a serial completion order equals the minimum directed feedback-vertex-set size of the pairwise blockage graph.

Proof: releasing product i suppresses every blockage edge sourced at i, as its footprint is absent thereafter. The remaining graph has a serial feasible order iff acyclic. All directed cycles must contain at least one released vertex, and selecting any directed feedback vertex set is sufficient. This uses *physical guide release* that does not sever or damage the desired product bond; no such independent guide-release operation is established for the oxanine adduct.

Exhaustive independent dynamic compiler and minimum feedback-set comparisons over **all 4,096 directed graphs with four vertices and no self arcs** passed: 543 need zero guide releases, 2,632 need one, 920 need two, and one needs three. Chemical prerequisites can create other ordering conflicts; feedback-vertex-set equivalence is limited to the prerequisite-free model. Hypergraph blocking may have cooperative jams missed by ordinary directed edges.

## Finding C: blind chemical timing destroys deterministic schedules

For independent, simultaneously activated exponentially distributed bond times with identical rates, and irreversible pairwise blockages i→j, full success requires j's reaction time to precede i's. The exact success probability equals the number of linear extensions of the reverse blockage order divided by n!. This is an application of standard order-statistics, not a new abstract mathematical theorem.

A single directed blockage gives 1/2 correctness, a three-site blocking chain gives 1/6, and 500 independent directed blocking pairs give 2^(-500)≈3.055e-151, **despite every isolated chemical reaction having eventual success probability 1**. Exhaustively checked small graphs and independently simulated continuous reaction clocks. Repeated harmless chemistry does not change the final ordering law if the first successful reaction times retain independent exponential distributions.

Outcome-confirmed staging can choose a valid topological reaction order; blind finite staging needs enough retry attempts before exposing blocking products. If per-opportunity correct probability p=.6, no wrong chemistry, and L=1000 independent sites, 13 attempts per site before potentially blocking it give (1-.4^13)^1000≈.99331. Twelve attempts give ≈.98336. Persistently inactive sites defeat this assumption.

## Finding D: chemical separability changes cooperative-error scaling, but correlated cleanup removes the gain

In a three-site cooperative motif the final site is blocked only if **both** earlier products still carry obstructing donor recognition guides. If each earlier guide is independently cleared with probability r before the next reaction, then

    P(no cooperative jam) = 1-(1-r)^2.

For r=.9 the one-motif no-jam probability is .99, but 100 independent motifs succeed with probability only (.99)^100≈.3660. To give >=.99 success over 100 such independent motifs, the guide-clearance probability per donor must be >=.989975.

If guide-clearance failures are perfectly shared/common-mode, the probability both fail is (1-r) instead of (1-r)^2; at r=.9, the 100-motif success falls to .9^100≈2.656e-5. More generally for marginal post-clearance failure q_i,q_j, Frechet bounds imply max(0,q_i+q_j-1) <= P(both uncleared) <= min(q_i,q_j). Marginal wash performance is not sufficient to establish long-run cooperative reliability: *joint retention across neighboring guides* must be measured.

A global toehold-invader/wash operation is simpler than site-specific cleavage, but may create exactly such correlated residual occupancy. Self-cleaving acyl transfer makes all these donor guides physically removable without breaking desired product bonds, not automatically removed from the hybridization environment. Hydrolyzed donors and noncovalently trapped oligonucleotides must also be cleared.

## Finding E: sensorless retries are mathematically robust only when the covalent product is self-inactivating

For a distributed site's unique free primary amine, one exposure yields correct amide with probability p, irreversible incorrect acylation with probability w, and otherwise leaves a chemically competent retriable parent (1-p-w). The correctly formed amide is stable and contains no newly exposed nucleophile capable of further targeted acylation. Donor recognition DNA is not covalently in the finished product and can be removed without detaching the rooted chemical cargo.

After m independent donor-feed opportunities the correct fraction is exactly

    P_site(m) = p/(p+w) * [1-(1-p-w)^m].

For L chemically independent sites the full correctly modified fraction is P_site(m)^L. This proof is a geometric renewal sum; it fails for persistent dead-site heterogeneity, wrong-site cross-acylation, reagent depletion, guide-retention obstruction or another amine arising on the payload.

For purely illustrative p=.6, w=1e-6, L=1000 and m=14: full correct fraction ≈.9956585. Even with unlimited retries, the 99% target is impossible if w>p*(.99^(-1/1000)-1)≈6.03e-6. Thus chemically separable guides solve an important **topological** failure, not the permanent wrong-amide problem.

## Finding F: a four-cohort assay for cooperative steric suppression

Preset two independently measured product footprints A,B and challenge chemical modification at site C. Let p0, pA, pB, pAB be the correct C product fractions after the same exposure t for scaffold with neither, only A, only B, or both completed products. Under individual homogeneous first-order kinetics infer k_x=-ln(1-p_x)/t. The independent multiplicative inhibition benchmark predicts k_AB*k0=k_A*k_B. Define

    eta=1-k_AB*k0/(k_A*k_B).

eta>0 implies additional inhibition in the both-products configuration compared to this explicit null. It is not a unique steric proof: electrostatic changes, changing salt/DNA density, and chemically competing nucleophiles may also produce a nonzero eta.

Hypothetical example at t=30 min: k0=kA=kB=.04/min, kAB=.002/min gives eta=.95, while all pairwise reaction-rate comparisons appear identical. A second C approach that remains reactive when AB is present, or selective removal of only the donor-guide DNA while preserving the A/B covalent cargo, is the decisive recovery challenge. Include A-before-B and B-before-A, old site competence, wrong-site amides, hydrolyzed donors, and static optimal tether controls.

## Primary mechanism and strongest alternative

He/Liu 2011 experimentally used 50 mM MOPS, 10 mM magnesium acetate, pH 7.5, one DNA substrate every 30 min, producing a six-step product in 3h. This establishes a *particular* self-cleaving NHS–DNA substrate and noncovalent strand replacement, not general on-demand guide disappearance, non-destructive internal site reconfiguration or independent progress in a large mixed pool. The original 2013 Niu/Hili/Liu DNA-programmed PEG/peptide synthetic polymers with PNA recognition adapters and cleavable disulfides demonstrate larger structural diversity, but one-time adapter cleavage is not a root-preserving reversible reset. The 2026 Schaub enzyme cascade is significantly more mature for broad individual amide modifications on DNA.

The strongest proposed next operation is therefore **blind, idempotent, locally addressed chemical writing with an expendable donor guide and permanent rooted product**. Its special capability, if physically acquired, would be to retry incomplete chemistry without a per-site success sensor and without accumulating permanent donor-DNA footprints. The strongest physical uncertainties are real donor-guide clearance despite multivalent binding, wrong-site acylation among free amines, site-specific registration after switching, and compact organic products themselves sterically obstructing a site. None is measured by the script.

### Primary sources (externally verified in this continuation)
- He & Liu 2011, *A Sequential Strand-Displacement Strategy Enables Efficient Six-Step DNA-Templated Synthesis*: https://doi.org/10.1021/ja201361t
- Lee et al. 2026, *Stable and programmable formation of DNA nanostructures via inter-strand crosslinking by assembly-triggered oxanine and amine linkage*: https://doi.org/10.1093/nar/gkag638
- Niu, Hili & Liu 2013, *Enzyme-free translation of DNA into sequence-defined synthetic polymers structurally unrelated to nucleic acids*: https://doi.org/10.1038/nchem.1577
- Schaub et al. 2026, *A tailored CoA ligase–N-acyltransferase cascade for on-DNA amide bond formation gives access to broad substrate scope*: https://doi.org/10.1038/s41929-026-01576-x
- Cabello-García et al. 2025, *Information propagation through enzyme-free catalytic templating of DNA dimerization with weak product inhibition*: https://doi.org/10.1038/s41557-025-01831-x
