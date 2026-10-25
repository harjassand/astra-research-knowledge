# Astra chemistry: topologically retained packets for reversible failure recovery

26 October 2026 — Working proof notes. Hypothetical kinetics and architectural design, not an experimentally realised synthesis. Computations and finite-state checks: `astra_covalent_island_repair_20261026.py`.

## Verified physical footholds and scope

- Niu, Hili and Liu (2013), *Nature Chemistry*, DOI 10.1038/nchem.1577 (PMC4277153): DNA-templated macrocyclic PNA-coded AA/BB CuAAC, synthetic PEG/alpha-(D)-peptide/beta-peptide backbones, up to 16 consecutive couplings, ~70% full-length in one optimised short construction. Experiments at 4 C overnight, HEPES pH 8, DNA codons and PNA five-base adapters, CuSO4/ascorbate/THPTA. Their reaction already positions multiple building blocks and can create multiple connections in one global exposure. No automatic molecular defect repair established. AA/BB reduces—but cannot logically eliminate—all erroneous inter-site pairings. Their PNA adapters are attached through cleavable disulfides; cutting the latter ends template alignment.
- Brudno et al (2010), *Nature Chemical Biology*, DOI 10.1038/nchembio.280 (PMC2808706): polymerase-mediated PNA strand displacement while retaining covalent DNA/PNA root; different 40-base PNA polymer, heated polymerase/dNTP conditions, not demonstrated repeated stripping of several CuAAC-crosslinked PNA-adapter islands at 4 C. Isolated multivalent PNA islands may be very slow to release.
- Nian et al (2025), *Nature Communications*, DOI 10.1038/s41467-025-60143-3: BTT-DNA localises copper click catalysis for ligation, including nucleic acid-templated reactions. Not evidence that per-junction catalyst placement suppresses organic wrong-pair rate enough for long translated polymers.
- Huang et al (2014), *ACS Nano*, DOI 10.1021/nn5024472: photocleavable DNA linkers split oligonucleotide strands in controlled photolithography. Not evidence for complete thousand-site chemical reset compatible with CuAAC, roots and reusable PNA recognition.
- Frommer et al (2024), *Angew Chem Int Ed*, DOI 10.1002/anie.202317482: abasic duplex pocket protects a particular thioester from hydrolysis; strongly substrate-dependent and not generally transferable to PNA/click.

## I. Exact irreversible-wrong-partner matching theorem

Let n independent *desired* azide/alkyne end-pairs be present. A cognate pair reacts with hazard k. Every noncognate chemically compatible ordered pair reacts with hazard beta. Consumed handles never react again. Any incorrect bond disqualifies the product. If r desired pairs remain and all prior bonds were correct, correct event hazard = r*k and off-target event hazard = r*(r-1)*beta. Exponential competing-clock calculation gives

P(all correct) = product_{r=1}^n [1+(r-1) beta/k]^-1.

As beta/k ->0 with n bounded, log P = -(beta/k)n(n-1)/2+ O((beta/k)^2 n^3). For n=1000, a target 99% fidelity requires beta/k <=2.012092738e-8. This is *conditional on all-to-all accessibility with constant per-pair rates*; DNA geometry should make beta distance-dependent. At beta/k=1e-7 the 1000-edge probability is 0.95127857, even after unlimited time to exhaust intact handles.

**Bounded-access theorem.** If in any surviving reaction state every unconsumed site has aggregate wrong-partner rate at most D*beta, its correct rate is k, and only correct events shrink the number of remaining sites, then induction on the number of remaining pairs gives

P(all correct) >= (1+D*beta/k)^(-n).

A finite spatial interaction degree prevents the quadratic exponent, even if all steps occur in the same fluid bath. A 2^n-subset exact DP in the companion code verifies the all-partner formula in the uniform limit and computes distance-dependent couplings, e.g. for 14 pairs, beta/k=.001, nearest-neighbor dominated decay length .25, Pcorrect .986874 vs .913389 for all-pair beta=.001. Geometry and rate constancy unverified for Niu's chemistry.

**Topology assay obstruction.** For 2m distinguishable alternating A/B monomers with fixed first A and last B, there are ((m-1)!)^2 distinct Hamiltonian path orders of the same monomers with the same end identifiers, bond count, mass, and alternating AA/BB-compatible connectivity. With 20 monomers this is 131,681,894,400 possible alternating orders. Full length plus exact mass and end labels therefore cannot certify correct molecular order unless physical geometry disallows the alternatives. This does *not* imply these alternative paths all occur chemically.

## II. Catalyst-pulsing null result

Suppose on a still unreacted pair the desired event has hazard k*c(t), irreversible wrong bond w*c(t), and time-dependent catalyst availability c(t)>=0. Let A=integral c(t)dt be total exposure. Exact correct yield is

Y(A) = k/(k+w)*(1-exp(-(k+w)*A)).

The shape of c(t) cancels. Six catalyst pulses or one continuous pulse with equal integrated exposure have identical correct/incorrect final probabilities under this kinetic model; repeated feeding is not by itself a novel repair mechanism. An improvement requires replenishing *chemically damaged* handles, releasing persistent wrong binding, increasing correct/incorrect selectivity, changing template configuration, or another changed operation. Verified by iterative transition update in companion code.

## III. Persistent multivalent DNA-binding islands

A completed run of adjacent clicked junctions gives an island bearing multiple PNA adapters. If each of m bound arms leaves at rate u and each unbound arm rebinds intramolecularly at rate a, the number n of arms bound forms a birth-death chain, n->n-1 at n*u, n->n+1 at (m-n)*a. n=0 absorbs to a perfect wash sink. Starting n=m, exact mean clearance time is

E[T_m]=sum_{n=1}^m (1/(n*u))*sum_{j=n}^m [C(m,j)/C(m,n)] (a/u)^(j-n).

If a=0, E[T_m]=H_m/u, logarithmic in m. If a>0, its n=1 term alone gives lower bound

E[T_m]>=((1+a/u)^m-1)/(m*a),

so unrestrained rebinding creates exponential trapping. Example hypothetical u=a=.3/s: m=14 mean 4275.4s (71.3 min), while a=0 gives only 10.84s. The calculation does not assert rates of the 2013 macrocyclic PNA adapters. Under independent Bernoulli edge success probability .6 on a 1000-edge template, there is a 26.7% chance of at least one run of 14 successful adjacent edges; other downstream islands may thus contain many binding arms. Distribution computed exactly by a finite-run-length Markov chain.

**Physical mechanism:** active suppression of rebinding during displacement, plus a selective sink, is not merely speeding a wash; it changes the asymptotic clearance law. Precedent for other PNA systems: polymerase-mediated duplex displacement, Brudno et al 2010. Must show displacement of *multi-adapter CuAAC islands* while preserving product and root registration, not infer it from single PNA4 kinetics.

## IV. Covalent-continuity ratchet: exact rounds and chemical waste

Proposed architecture: covalent rooted monomer at beginning of an encoding DNA track; temporarily bound PNA-adapter organic monomers downstream; parallel AA/BB CuAAC; deactivate copper, remove unrooted material by active displacement/denaturing wash; all organic fragments not **covalently connected** to root are discarded; refill track and rehybridise rooted chain into its original positional register; repeat. Correct clicked edges are chemically inert at those specific handles. Wrong stable off-register links escape this topology filter: it certifies *rooted connectivity*, not complete sequence/order.

Ideal independent model: each exposed junction forms correctly with probability p each round, no wrong bonds, chemical damage or register changes; every disconnected island completely removed, while rooted prefix survives. For L edges, number R of rounds to finish is exactly R=1+NegBin(L,p) (number of failures before L successful frontier crossings). Therefore E[R]=1+L(1-p)/p and Var[R]=L(1-p)/p^2. In contrast, if completed unrooted islands remain templated and are never damaged, all n edges complete by m rounds with probability [1-(1-p)^m]^L, giving O(log L) rounds.

**New waste theorem.** Every failure at edge i forces another round in which every later edge j>i can react and subsequently be discarded. Expected # failures before successful frontier crossing at i is (1-p)/p. Each later edge click success wastes a covalent bond with probability p per such failed round. Sum over ordered i<j gives

E[wasted already-formed correct links] = (1-p)*L*(L-1)/2.

For L=1000,p=.6 => 199,800 lost successful links versus 1000 finally retained, plus 667.67 expected reset rounds. Verified by independent Monte Carlo with explicit rounds and discarded islands. **Topology selection without retention of disconnected islands is not a free high-throughput repair scheme:** it incurs quadratic material waste as L grows.

If chain is split into independently anchored packets of exactly b edges, expected **within-packet** waste drops to (1-p)*L*(b-1)/2 (for b|L); 20-edge packets in an L=1000,p=.6 model waste 3800 bonds. This excludes the chemistry, throughput, and fidelity of fusing the completed packets; assuming perfect packet fusion would be circular.

## V. Packet size and connector competition

If each packet of b junctions suffers all-pair wrong-partner kinetics with ratio beta/k, packets are chemically isolated, and each connector between packets fails independently with probability q, then at L divisible by b:

Ptotal = [product_{j=0}^{b-1}(1+j*beta/k)^(-1)]^(L/b)*(1-q)^(L/b-1).

For small beta/k and q, -log Ptotal ≈ L(b-1)beta/(2k)+(L/b-1)q. Optimum finite packet size trades intrapacket wrong pair exposure against connector failures. Illustrative L=1000,beta/k=1e-7,q=1e-4 gives P_1000=95.13% unsegmented, P_40≈99.566%, P_50≈99.566%, and P_1≈90.49%. Rates and q entirely hypothetical, connector independence and physical isolation assumptions untested. Number of rounds to finish all independently rooted b-edge packets (excluding fusion), for L=1000 p=.6 at 99%: b=20 ->35; b=50 ->63; b=1000 ->747.

## VI. Attempt at physical reset and its independent failure

Two available classes of operations: (i) replace PNA-DNA recognition with a more stable DNA-DNA duplex via strand displacement (Brudno 2010) while retaining the organic product at a separate covalent root, then reset DNA template; or (ii) put sacrificial photocleavable bonds between template codons to disconnect DNA-bound *unrooted* islands from the carrier without waiting for multi-arm PNA release. Photo-cleavable oligonucleotide cleavage is an existing operation (Huang 2014), but complete codon-by-codon reset is *not* demonstrated. The latter also requires cleanup of retained short DNA fragments before rooted PNA reannealing and risks chemistry/photodamage.

Under the stringent worst-case topology where any one of N uncleaved tethers traps a discarded island, independent cleavage probability c gives overall clearance c^N. To reach 99% for N=1000 requires c>=0.9999899497. A seemingly good c=.999 gives 0.3677 for 1000 tethers. Extra cleavage rounds may help but have reagent/damage cost. Likewise repeated root reset with independent irreversible root damage probability d must satisfy (1-d)^R>=.99, hence d<=1-.99^(1/R); R=668 permits at most d≈1.50e-5 per reset. These are conditional counterexamples; not universal impossibility if residual tether is removed noncovalently or by follow-up cleavage.

Neither photolysis nor polymerase displacement is yet verified to be compatible with the exact macrocyclic CuAAC substrate, root, and repeated template re-registration. A permanent proximal register and stringent mixed-program cross-link controls remain necessary.

## VII. Concrete minimal discriminating construction

Demonstrate two DNA programs and a three- or four-monomer AA/BB target array with a single permanent upstream organic root plus temporary PNA coding adapters. Compare: (A) Niu-type uninterrupted click with matched total catalytic exposure, (B) catalyst pulsing without structural reset (should *tie* under memoryless uniform hazards), and (C) click -> remove/free donors and unrooted islands -> regenerate template registration -> resume coupling. Independent analytes:
- chemically correct site-specific bonds, not only polymer length, end labels or intact mass;
- correct rooted frontier survival after hybridization reset;
- clearance distribution of isolated donors *and* multivalent clicked islands;
- active residual azide/alkyne handles and permanent wrong crosslinks;
- cross-program wrong join rate in a mixed bath;
- material consumed and time per correct sequence.

The engineering target is not universal 1000-edge fidelity immediately. It is a **nontrivial surviving operation**: demonstrate a missed first or middle bond can be repaired **without losing the prior correct organic junction or contaminating the rooted product with downstream disconnected islands**, compared against retaining the reaction for equivalent time. Achieving that would justify the complex controller; failure or a tie would favor the simpler, experimentally established templated click assembly.
