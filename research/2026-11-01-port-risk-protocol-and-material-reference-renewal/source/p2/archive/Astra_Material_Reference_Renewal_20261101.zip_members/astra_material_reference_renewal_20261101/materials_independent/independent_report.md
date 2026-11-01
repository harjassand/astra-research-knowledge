# Independent competitor: templated molecular manufacture with accessible replacement

## Finding

The strongest physical competitor is **finite-alphabet templated synthesis plus component turnover in a solvent-accessible architecture**. DNA replication already manufactures a prescribed chemically heterogeneous macromolecule with enzymatic proofreading and subsequent lesion/mismatch repair. DNA nanotechnology adds prescribed spatial organization, experimentally demonstrated growth proofreading, repair by replacement, and manufacturing scale. These achievements do not yet constitute an integrated demonstration of exact, arbitrary, dense, three-dimensional heterogeneous matter with sustained repair.

The defensible novel objective therefore cannot be merely “error correction applied to material assembly,” “local proofreading followed by repair,” “energy-driven bond weakening,” or “replace damaged parts using supplied matching parts.” Each has substantial prior art. The unresolved conjunction is: **manufacture and restore the intended chemical identity, geometry, and connectivity of a large heterogeneous object, including its reference machinery, under measured physical kinetics and realistic transport.**

I did not inspect Astra. The direction and tests below were chosen independently from the task and primary literature.

## A concrete minimal target and the best existing route

The smallest complete molecular objective is a specified DNA sequence that remains accessible to copying and repair enzymes. The target alphabet has four monomers; template information scales with sequence length while the substrate alphabet stays constant. Existing cellular replication, proofreading, and repair implement local molecular discrimination using finite enzymes and nucleotide fuel. A 2021 yeast experiment quantified distinct contributions of selectivity, intrinsic and extrinsic proofreading, and mismatch repair; its inferred replicative substitution rate was about 1.8×10^-11 per base pair per generation, with nonreplicative mutations larger. That is a model-based in-vivo estimate, not a universal in-vitro synthesis guarantee. [1]

For a spatial object, the strongest immediately credible construction is a hydrated DNA structure whose damaged short components can exchange with a replenished pool. Practical targets include a predefined nanoruler, rod, or nanotube with sequence-specific functional positions. This deliberately keeps repair substrates physically accessible. It does not promise atomic editing through an impermeable solid.

There is evidence for almost every constituent operation:

| Primary result | What it establishes | Remaining issue for the stated objective |
|---|---|---|
| Schulman et al., 2015 [2] | Experimentally increasing redundancy in DNA tile ribbons reduces bit-copying errors; each additional redundancy level reduced errors about threefold, and fourfold redundancy was below 0.1% per copied bit. | Finite-size experiment; no proof of arbitrary chemical payload fidelity or indefinitely maintained bulk structure. |
| Soloveichik, Cook and Winfree, online 2007 / journal 2008 [3] | A combined proofreading/self-healing tile construction has a genuine high-probability finite-time theorem. | Protected boundary, idealized interaction alphabet, reservoir assumptions, unresolved spurious nucleation, and an increasingly delicate physical regime. |
| Li and Schulman, 2019 [4] | Matching replacement tiles enter micron-scale DNA nanotubes during nuclease damage; degradation is at least fourfold slower and survival extends to days. | Predominantly repetitive structure, not recovery of an arbitrary heterogeneous pattern or erasure of every reference. |
| Scheckenbach et al., 2021 [5] | Damaged exposed staples and labels can be replaced in origami. Structural repair reduced defective rods from 63% to 32% by AFM after incubation with missing staples. | Incomplete recovery, possible dimers, temperature/excess-strand requirements; scaffold damage is explicitly not repaired by this strategy. |
| Praetorius et al., 2017 [6] | Bacteriophage precursors with self-excising cassettes manufacture both staples and scaffolds; end-to-end macroscopic rod production in a litre-scale bioreactor. | Accurate program preparation, purification, mutation and off-target assembly remain costs; many copies of one design is different from arbitrarily increasing design complexity. |
| Ong et al., 2017 [7] | 3D addressable structures assembled from roughly 30,000 distinct DNA bricks. | An actual species/preparation cost, rather than evidence that addressing is free; repair is not demonstrated by this result. |

The integrated candidate is therefore a worthwhile engineering programme, but stitching these papers together does not establish that the complete system works. For example, adding stronger protection can impede access needed for replacement; adding more species can reduce correct encounter rates at fixed total concentration; and functional labels can be damaged without compromising their docking domains.

## Exact prior theorem: do not undersell it

For a quarter-plane tile pattern of N×N logical blocks, [3] constructs k×k physical blocks with k=Θ(log N). Under the locking kinetic Tile Assembly Model, starting from an allowed damaged subassembly containing the intact L-shaped boundary, the target completes with probability at least 1−ε in O(N polylog N) time. This is substantially stronger than a hand-waving analogy with error correction.

Its stated assumptions and resource dependencies matter. The proof sets equal per-species concentrations and association rates, assumes matched glue interactions and zero mismatched interactions, and forbids detachment of tiles with at least three bonds in the locking model. It chooses exp(−G_se)=Θ(k^-5); the resulting block cleaning/completion estimate is O(k^13). In the discussion of the full kinetic model, favorable growth constrains the rate imbalance to O(log k/k²). The authors explicitly flag spurious nucleation from strong spines, fragment aggregation, weak mechanical seams, and large tile counts. They also discuss nonzero detachment: a finite-time logical-error bound can survive, while exact full occupancy cannot be guaranteed and eventual failure remains possible. [3]

This prior defeats any novelty claim based only on redundant local matching plus reversible rejection and regrowth. A new physical result would need to close one or more of those explicit gaps.

## First-principles conditions every candidate must meet

### 1. Repair needs surviving information

Let X be the prescribed filling of a damaged region and C the complete surviving state in the causal past of the repair process before its deadline. Include templates, controller memory, neighboring structure, fuel labels, and externally supplied signals in C. If two targets x and x' leave identical C and obey the same physical transition kernel, their repair output laws are identical. Because correct outputs are disjoint,

P(success | x,C) + P(success | x',C) ≤ 1.

For M equally likely, indistinguishable possible fillings, average exact success is at most 1/M. Fuel cannot supply missing target information. A device restoring arbitrary erasures must keep sufficient redundancy outside them or obtain that information through an accessible channel. The same argument applies to a mistaken master template reproduced consistently into every dependent component.

For a general q-symbol N-site target, the programme requires Ω(N log q) bits unless the particular target admits compression. Those bits can live in templates, patterned couplings, a heterogeneous species catalogue, a timed feed, or a controller. Moving the bits between these places does not remove their preparation or protection cost.

### 2. A correct address is not necessarily a correct payload

Suppose a component contains a docking tag and a chemically functional payload. Corrupt the payload while preserving the tag and every interaction measured by the proposed checker. Then the checker receives the same data for correct and wrong material. A geometric bond-consistency code can repair geometry while silently preserving chemically wrong matter.

This is not an assertion that payload measurement is universally impossible. It is a demand to identify and measure the physical reaction that distinguishes the claimed error class. DNA mismatch recognition addresses particular distortions; it does not act as a universal chemical truth detector. A stable double-stranded substitution can be perfectly consistent with local pairing while differing from the prescribed sequence.

### 3. Distinct species impose both selectivity and transport costs

In a deliberately simple occupied-site equilibrium model, one correct species competes at equal concentration with S−1 wrong species, each disadvantaged by free energy Δ. Then

p_wrong = ((S−1) exp(−βΔ)) / (1 + (S−1) exp(−βΔ)).

Under independent-site errors, P(all correct)=(1−p_wrong)^N. To obtain whole-object error at most δ, the small-error regime therefore requires

βΔ ≳ ln[(S−1)N/δ].

This is a model-specific equilibrium result, not a universal energy-accuracy theorem for nonequilibrium proofreading. Driven schemes can change it but must provide their actual reaction network and energy supply.

At fixed total concentration C_tot and equal species fractions, the correct bare arrival rate is k_on C_tot/S. Mean correct encounter time is S/(k_on C_tot). This already penalizes large addressable catalogues before off-target binding, steric obstruction, depleted boundary layers, and failed checks are included. For k_on=10^6 M^-1 s^-1 and C_tot=10 μM, 30,000 equally abundant species give a 3,000 s mean correct encounter time per empty site. These numbers illustrate the formula and are not fitted to the brick experiment.

DNA template copying provides a real finite-species workaround: four substrate identities are reused at every position. The cost is the prepared local template and molecular reading machinery.

### 4. Rates cannot be chosen independently of fuel chemistry

For a thermodynamically consistent elementary transition, local detailed balance relates the forward/reverse rate ratio to the free-energy change and exchanged chemical work. With appropriate state/standard-state conventions,

ln(k_forward/k_reverse) = β(chemical work − ΔG_system).

Around a driven cycle, the log rate-ratio sum equals the chemical affinity. A simulation that switches bonds irreversibly whenever a desired geometry is observed has specified an algorithm, but has not thereby supplied a catalyst, a detector, or a fuel cycle. Each must fit into a reaction network with finite errors and reverse pathways.

Even passive exchange consumes a stock of correctly prepared replacement components when damage destroys material. Maintaining a pool, removing waste, regenerating templates, and repairing the repair apparatus all require explicit throughput. For a homogeneous damage rate d per site and average replacement cost w, merely replacing damage costs order Ndw in sustained power, before background turnover and failed attempts.

### 5. Buried access is a geometric resource

A repair reactant cannot act at an inaccessible site. If it reaches depth h by diffusion coefficient D, the characteristic transport time scales as h²/D. In a uniformly consuming spherical domain with zero-order volumetric consumption q_v and surface concentration c_0, steady diffusion gives c(0)=c_0−q_v R²/(6D). Thus R²≤6D c_0/q_v is necessary for positive center concentration in that elementary model.

A porous or microvascular architecture can keep h bounded as the object grows, but channel volume, pressure losses, surface chemistry, waste removal, and strength become part of the manufacturing specification. An alternative is to expose and replace an entire module. That is genuine repair, but its replacement granularity and removal path must be stated.

### 6. Rare unwanted events accumulate with scale and duration

For an independent unwanted-nucleation process of rate density J, the probability of at least one event in volume V over duration T is 1−exp(−JVT). “Very small J” does not justify ignoring nucleation when V or T increases. Seed specificity, compartmentalization, activation gates and purification can reduce its impact, but are mechanisms with cost and leakage. The same finite-horizon accounting applies to wrong-but-stable structures and reference corruption.

## Public research code audit

I fetched and inspected the actual notebook accompanying Zhu et al., *Proofreading mechanism for colloidal self-assembly*, Phys. Rev. Research 6, L042057 (2024). [8] The fetched notebook blob is `9e54620edd3104f2210375c9cd74458c45758364`.

The notebook's `construct_graph` obtains exact particle species and center/patch distances. `update_species_prob` applies a graph neural network and directly changes the particle's interaction species. The second-stage routine inserts fixed-probability species transitions that weaken bonds. It simulates physical motion between such updates, but contains no explicit molecular sensor, fuel/waste species, or detailed-balance construction for the switching mechanism. That is appropriate for its modelling purpose; it does not realize those missing physical components. I did not run its GPU training.

The public Xgrow implementation and rgrow documentation provide appropriate kinetic tile-assembly baselines, with rgrow also documenting forward-flux sampling for nucleation rates. [9] These baselines should be extended with the candidate's actual chemistry rather than treating perfect glues or absent transport as evidence.

A distinct physical alternative does exist at the microscale: Liang et al. engineer magnetic tetramers that decouple from an applied field while unwanted intermediates remain susceptible. Field cycling selectively breaks intermediates, increasing tetramer yield from a single-quench maximum near one half to about 90%. [10] This is experimentally implemented discrimination through mechanical response, but it does not establish arbitrary heterogeneous repair. It is an excellent competitor to an abstract “recognize correct structure and destabilize the rest” proposal.

## Executable discriminating test and results

`discriminating_test.py` is a standard-library Python programme, executed successfully. `results.json` contains its full numerical output. It is an exact toy stochastic model and algebraic stress test, **not** a molecular simulation or experimentally calibrated prediction.

The four-state repair model has vacancy U, correct material C, wrong payload with correct address H, and wrong address A. Finite arrivals compete. C can chemically degrade to H without changing its docking information. A detaches rapidly; C and H have identical recognition kinetics. Uniform fuel-driven turnover removes all three occupied states. Stationary probabilities are obtained directly from incoming/outgoing flux balance and independently checked in the script.

For one illustrative parameter set, chemical payload damage is 10^-5 s^-1 and correct-address natural detachment is 10^-6 s^-1. Without turnover, only 9.09% of sites remain chemically correct at stationarity even though docking remains mostly occupied. Turnover at 10^-3 s^-1 raises correctness to 98.02%, but faster turnover creates vacant sites faster than finite arrivals repair them. At 10^-1 s^-1, correctness falls to 49.75%. This establishes a concrete failure mode for a docking-only checker and an explicit repair/throughput tradeoff.

A positive control assigns hidden damaged payloads an extra rapid off-rate. It greatly improves fidelity—but that improvement is exactly the engineering debt: the proposed physical mechanism must implement such a discriminator. The script labels it unimplemented rather than silently assuming it.

The script also calculates an error-correcting reference example. Seventeen independent copies each wrong with probability 0.01 give majority error about 2.26×10^-14. Add a 10^-6 common-mode error probability per logical site shared across those copies, and decoded error stays near 10^-6. Under independent logical sites, one million sites then have whole-object yield near e^-1≈0.368. Copy redundancy does not repair a systematically wrong reference.

## Experiments that would discriminate a meaningful advance

1. Use a specified heterogeneous sequence/pattern, with destructive chemical readout where necessary. Geometry or fluorescence occupancy alone is insufficient to verify every claimed chemical identity.
2. Compare isolated missing components, wrong-address components, and wrong-payload/right-address components. A mechanism should state exactly which it repairs.
3. Remove a patch together with any co-located reference. Then repeat with an independently surviving remote reference. This separates reconstruction from filling a cavity according to a surviving stencil.
4. Scale target size and species number independently while holding total concentration and imposed power fixed. Count elapsed time, accepted units, rejected units, waste, catalyst lifetime, and spontaneous nuclei.
5. Induce damage at controlled depth in a hydrated/porous sample and in an otherwise matched sealed sample. Report channels or destructive access required.
6. Include stable, locally consistent wrong structures as adversaries. Do not restrict errors to vacancies or weakly bound mismatches that the design was constructed to reject.
7. Supply an intentionally corrupted master/template and measure whether redundancy propagates or corrects its error. Include common-mode damage to the repair mechanism itself.

The most defensible research claim would close one of these experimentally exposed gaps with a specified finite molecular reaction scheme and a resource bound. A universal or arbitrarily scalable claim is not presently justified by combining local checking with a generic supply of energy.

## Primary sources and code

1. Zhou et al., *How asymmetric DNA replication achieves symmetrical fidelity*, Nature Structural & Molecular Biology 28, 1020–1028 (2021). https://www.nature.com/articles/s41594-021-00691-6 ; full text https://pmc.ncbi.nlm.nih.gov/articles/PMC8815454/
2. Schulman et al., *Increasing Redundancy Exponentially Reduces Error Rates during Algorithmic Self-Assembly*, ACS Nano (2015), DOI 10.1021/nn507493s. https://pubmed.ncbi.nlm.nih.gov/25965580/ ; paper https://www.dna.caltech.edu/Papers/zig-zag-proofreading2015.pdf
3. Soloveichik, Cook and Winfree, *Combining Self-Healing and Proofreading in Self-Assembly*, Natural Computing 7, 203–218 (2008; online 6 April 2007), DOI 10.1007/s11047-007-9036-x. https://www.dna.caltech.edu/Papers/selfhealing_proofreading_preprint.pdf ; record https://authors.library.caltech.edu/records/7gj5t-g0873
4. Li and Schulman, *DNA Nanostructures that Self-Heal in Serum*, Nano Letters 19, 3751–3760 (2019), DOI 10.1021/acs.nanolett.9b00888. https://pubmed.ncbi.nlm.nih.gov/31140279/
5. Scheckenbach et al., *Self-Regeneration and Self-Healing in DNA Origami Nanostructures*, Angewandte Chemie International Edition 60, 4931–4938 (2021), DOI 10.1002/anie.202012986. https://onlinelibrary.wiley.com/doi/full/10.1002/anie.202012986
6. Praetorius et al., *Biotechnological mass production of DNA origami*, Nature (2017), DOI 10.1038/nature24650. https://www.nature.com/articles/nature24650
7. Ong et al., *Programmable self-assembly of three-dimensional nanostructures from 10,000 unique components*, Nature 552, 72–77 (2017), DOI 10.1038/nature24648. https://www.nature.com/articles/nature24648
8. Zhu, Du, King and Brenner, *Proofreading mechanism for colloidal self-assembly*, Phys. Rev. Research 6, L042057 (2024), DOI 10.1103/PhysRevResearch.6.L042057. https://arxiv.org/html/2312.08619v1 ; code https://github.com/brennergroup/paper_notebooks/blob/main/Proofreading_self_assembly.ipynb
9. https://github.com/DNA-and-Natural-Algorithms-Group/xgrow ; https://docs.rs/crate/rgrow/0.22.0 ; https://www.dna.caltech.edu/Xgrow/xgrow_www.html
10. Liang et al., *Magnetic decoupling as a proofreading strategy for high-yield, time-efficient microscale self-assembly*, PNAS 122, e2502361122 (2025), DOI 10.1073/pnas.2502361122. https://pmc.ncbi.nlm.nih.gov/articles/PMC12415251/ ; code https://github.com/melodyxlim/magnetic-decoupling
