# Small-scale explicit thermal memory: root whole-construction candidate

2026-11-02. Status: integrated candidate for independent whole-join review. Do not treat this document alone as an accepted lifetime theorem.

## 1. Target and exact source boundary
The target is the small deterministic three-dimensional sheaf-code architecture of Balasubramanian–Davydova–Lin, arXiv:2605.10943v1 Section6, with scale ell=8. The source proves its geometric closure/locality and explicitly leaves the complete exponential-lifetime proof to future work (Introduction1.2.4). Its raw syndrome contraction sketch is not imported as a theorem.

Use the DECLARED skeleton-first, intrinsic-page completion in explicit_cochain_fibers_20261102/ATLAS_NORMALIZATION.md. Every old abstract edge owns one routed source edge word shared by all incident pages; pages retain parent IDs; free crossings never identify abstract cells by coordinate coincidence. Ordinary page refinements, the finite three-page T charts and their subcharts, and Rep4/Par4 tree resolutions are relative to their complete exterior ports. Physical cells follow the source routing. Common refinements used for cochain comparison are VIRTUAL and are composed back; no fractional physical mesh is iterated.

Geometric admission invokes the source's Lemma6.9/Claim6.11/Corollary6.12 for its finite integer-grid routing rules. The new work supplies algebra and decoding for this declared abstract realization. An independently compiled coordinate table for every source chart is not part of the evidence. If an alternative completion changes the source routing or adds physical subdivisions, the quoted source density theorem does not automatically transfer.

The checks are the actual CSS checks from the cellular complex C0(F)->C1(F)->C2(F), with strong sheaf stalks and fixed edge-local physical bases. Boundaries, degree-one red/blue codes, redundant checks and extra H0/H2 relations remain explicit. The local Pauli check weight is uniformly bounded but is NOT assumed to equal the random family's bound7.

## 2. Algebraic refinement/doubling machinery
The governing algebra theorem is explicit_cochain_fibers_20261102/ALGEBRA_AND_FILLING_THEOREM.md.

- Ordinary parent-page syndrome compression is parity plus a bounded tree homotopy.
- The actual triangle/pentagon T charts have ports-relative H0=H1=0; 28 finite cases (all page deletions, both colors, both listed charts) are checked.
- Rep4/Par4 resolution is an explicit exact local complex. It preserves degree-one cohomology but Rep4 can inflate RAW syndrome Hamming weight: its auxiliary face may project to an old two-face pattern.
- Blue doubling is a sheaf mapping cylinder over the rib graph. Complement-chamber costars are exact in degrees0,1, so restriction gives the needed H0/H1 control. Extra degree-two classes are retained, not mistaken for logical qubits.
- Unequal shifted rib restrictions are compared by a bounded cellular prism homotopy. The periodic coordinate warp moves ordered middle markers while fixing the boxed/branch strata; no equality of the two restrictions is asserted by fiat.
- Red doubling has a direct prescribed projection: total parent-page parity on syndromes and sum of inherited old-edge values on errors. Its kernel contraction retains extra H0 relations. No thermal-lifetime duality is used to guess its metric.

For each blue step obtain bounded-local sheet projections PA,PB, a common lift J, and a bounded K such that on valid fine syndromes

 pA sigma+pB sigma=d_old K sigma,
 sigma+d fA sigma=J pA sigma,
 fB=fA+J K, so sigma+d fB sigma=J pB sigma.

If PB J is only homotopic to identity, the required formula includes the local homotopy term K=PB hA+L PA; it is not silently dropped. For an error e and a mixed component choice, the coarse error is PA e+sum_selected K sigma_C, not necessarily PA e.

## 3. The new packet metric repairs a genuine obstruction
Raw refinement weight nonincrease is false for certain valid auxiliary patterns in the specified Rep4 resolution fixture. This is preserved as a counterexample, not hidden in a constant.

Define mu(sigma) by cost-one singleton faces and ALL six face-pairs incident to each current blue degree-four edge. It is a minimum-XOR atomic norm, computable as occupied-pair matching, and

 |sigma|/2<=mu(sigma)<=|sigma|.

The pair graph stays inside a bounded parent-face cylinder hashtag; all4096 local configurations have been checked. There is no change to the physical Hamiltonian or Gibbs energy.

The owned atlas packet contract verifies atomic columns:
- A Rep4 auxiliary projects to one allowed old pair, cost1 in mu.
- A Par4 auxiliary can project to one old face.
- In blue doubling, new blue degree-four pair atoms are cylinder-supported and killed by the sheet projections; the remaining single-face domains are disjoint.
- In red doubling, the direct parent-page projection is packet-nonincreasing.

The fixed maps are F2-linear. Subadditivity of the SAME XOR atomic norm therefore gives

 mu(pA sigma)+mu(pB sigma)<=mu(sigma)  [blue],
 mu(p_red sigma)<=mu(sigma)           [red].

An atom check would be invalid for arbitrary nonlinear maps; that failed shortcut and its correction are preserved in the independent packet audit.

## 4. A component decoder, not a hidden global minimum
Build a fixed bounded-degree dependency graph from complete local packet blocks, all-branch preimages of coarse packet blocks, correction stencils and residual cochain rows. Activate only bounded footprints of genuinely nonzero inputs; zero halo nodes do not recursively activate empty space. Each active component contains whole packet-block states and has support O(mu(component)).

For each blue component choose the lower-mu sheet projection, with deterministic component-local tie breaking. The residual-row closure ensures its local cochain identities survive restriction even if that component's top syndrome has not yet been proved globally valid. The formula pA sigma+d sum_selected K sigma_C makes the recombined coarse syndrome valid. Each output packet block has a single component owner because all possible preimages were included before choosing sheets. Thus blue charge halves componentwise; red charge does not increase.

All corrections are supported in a fixed enlargement of their charged component. The choice can depend on the entire component and is NOT called bounded-radius. A fixed finite base decoder completes correction and has zero output on zero syndrome.

## 5. Thermal probability and logical stability
For ANY binary linear allowed-syndrome space and positive commuting check energies, the Gibbs syndrome law obeys

 Pr[T subset supp(sigma)]<=exp(-beta sum_(g in T)J_g)

for every set T, even when its indicator is not a valid syndrome. This follows from nonnegative Walsh coefficients of product weights and zero-coset maximality; ROOT_PRODUCT_SYNDROME_BOUND.md contains the proof and exhaustive small-subspace checks. This elementary ingredient is not claimed historically novel.

The independently audited charged-component theorem in component_decoder_threshold_20261102 controls two-run influence of one physical error, including component merges/splits. Whole-component ancestor closure yields a rooted connected space-scale animal with size linear in the number of distinct occupied Gibbs leaves. Common lifts and code distance control the case when influence dies before the chosen scale; reaching that scale forces many leaves. Finite-state packet charge is admitted only with whole-block ownership.

For a fixed local error and cutoff h, the result is of the form

 Pr[logical decoder instability]<=C exp[-c min(2^h,d/S_h)],
 S_h=sum_(i<h)(K_lift/2)^i,

under sufficiently small fixed syndrome fugacity. A conservative weaker choice gives an exponent alpha=log2/log(2K_lift)>0, avoiding special K_lift cases. Constants and depth restrictions are part of the theorem.

## 6. Distance, filling and the second error sector
With fixed edge-stalk bases adapted to the local tree resolution, physical error projections have columns0 or one old coordinate. Blue readouts are disjoint and induce the same nontrivial old logical class; hence X-distance doubles at blue steps and does not decrease at red steps. The same argument runs on the orthogonal-sheaf family with colors exchanged.

The local duality construction in local_duality_transfer_20261102 uses the actual primary double complex and finite per-cell/per-costar contractions, not just a homology identity. It provides bounded-local F,G,H with I+GF=dH+Hd. The transferred decoder is

 R_A(s)=G R_B(Fs)+Hs.

Local-stochastic laws push forward with a constant loss in fugacity; a bounded physical error maps to a bounded dual error. The mixture argument handles the necessary finite sequence of dual single errors. Therefore the ANY-local-stochastic instability theorem transfers to the physical opposite sector WITHOUT requiring that the pushed-forward distribution equal a dual Gibbs law. This is the needed thermal decoder bridge, separate from the source's merely expected lifetime-duality claim.

Applying distance comparison once at the final level gives d_X,d_Z>=c2^k after2k iterations, with no per-generation comparison loss. A stabilizer of weight m can be descended using existential smaller-error-sheet choices until zero or the fixed seed; lifting the local h-generated check coordinates gives polynomial-radius filling (a crude bound Cm^6 is recorded). These fillings use actual checks, not new interaction terms.

## 7. Candidate physical consequence
For the source-bounded embedding, n_(2k)<=C8^(6k)=C2^(18k). The preceding distance and charged-contour bound therefore give a positive power eta of n and an unstable-syndrome probability poly(n)exp(-c n^eta), at sufficiently low fixed nonzero temperature, for BOTH Pauli sectors.

The established thermal-memory criterion then yields stretched-exponential retention under its stated bounded-local, Gibbs-stationary thermal dynamics, with ideal thermal encoding and decoder. This is not a noisy physical WRITE theorem. Noise model, rate normalization, ideal endpoints and internal reviews must remain explicit.

Extension to the earlier native two-body/generic-perturbation compiler is NOT automatic from this paragraph. That compiler's local Gibbs-ratio consumer needs removable valid witnesses (or another appropriate perturbed-law bound); product-Gibbs local stochasticity alone does not provide one. A canonical full-trace removable-witness extension is being constructed separately. If that and the whole join are accepted, the actual explicit-family check-weight bound must determine clock dimension K; seven-level clocks cannot be inherited without proof.

## 8. Scope of the claimed advance
This is intended to complete a scientifically consequential small-scale architecture using a new metric/decoder framework, rather than optimize the huge random-layout sufficient constant. It still relies on the source geometric construction and has not been turned into a complete executable full-scale coordinate generator. It does not establish practical temperatures, sizes, gate error budgets, noisy initialization, or an optimal lifetime exponent. Historical novelty beyond the explicit cited machinery has not been certified.
