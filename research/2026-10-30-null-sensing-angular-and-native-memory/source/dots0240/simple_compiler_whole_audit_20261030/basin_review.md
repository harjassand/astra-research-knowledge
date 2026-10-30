# Independent basin, CP-similarity, retained-bath, and logical-output audit

2026-10-30. Reviewer: audit_basin, distinct from the V1 author and the whole-review lead. Inputs were read, not edited. Exact source hashes accompany this note.

## Verdict

**PASS at the specified conditional scope.** Sections 9–10 and the logical-output conclusion of `FULL_SIMPLE_COMPILER_MANUSCRIPT_V1.md`, with its CSS clarification, correctly compose the asserted Sections 5–8 weighted drift with the actual component-safe edge/killed-basin theorem. No counterexample or remaining basin/CP/noise/logical-gauge defect was found. This receipt does not independently certify Sections 5–8 or turn a bounded-body guarded controller into native two-site hardware.

The proofs below make explicit several facts whose omission would invalidate a generic CP-dressing argument. In particular, neither mere positivity of T nor mere preservation of a subspace implies all the conclusions used here.

## 1. The flagged no-jump lower comparison is valid

In gauged coordinates each raw animal is a positive function of DATA stabilizer syndrome and the commuting auxiliary flags C'_j. For every credit coefficient B_h, the source asserts [B_h,C'_j]=0. This can be checked directly: the only nondiagonal part is G_h Y_h, which links ready and good-reference at h only when every neighboring auxiliary is ready. Both linked states have C'_h=0. For an adjacent j the G_h factor forces j ready, making C'_j=0 on the linked states; every nonadjacent flag is unchanged. The diagonal terms of B_h commute trivially. Therefore B_h and sqrt(B_h) commute with every raw f_A, despite f_A now depending on auxiliaries.

For J_hs=sqrt(B_h)K_hs, DATA/auxiliary commutation and completeness give sum_s J_hs^dagger J_hs=B_h. Consequently the exact no-jump summand of exp(t Z_h) has Kraus exp(-t B_h/2). In the structural backward causal cone of one f_A there are at most c|A| gates. Selecting their no-jump branches gives a positive summand Q^dagger f_A Q=f_A Q^dagger Q. Every factor of Q commutes f_A, though factors of Q need not commute each other. Minimum singular values multiply from below, so

    T(f_A) >= exp(-C_T t |A|) f_A.

The cone must be the structural circuit cone, not one inferred after cancellations. A fixed-depth bounded-range circuit has the needed O(|A|) gate bound, including the bounded supports of every flag and all R repeated token vertices. No global circuit condition number or CP-order lower bound T>=c Id is invoked.

Using a_+>a_0 and C_T t<=a_+-a_0 gives F=T(V_+)>=V_0 termwise. All local monotonicity, coverage, vacuum-summability and boundary conditions are strict conditions near c=1, so two admissible exponents can be selected before the final sufficiently small fixed t. Also every gate lowers V_+ because Z_h(V_+)=-B_h d_h<=0; differentiation through the positive semigroup and gate-by-gate order yields T(V_+)<=V_+.

## 2. Restriction to the raw basin really can be pushed through T

Let P select both sectorwise component-safe minimum representatives and V_0<M. A K_hs branch has one fixed local DATA Pauli correction and one local syndrome projector. It leaves every flag unchanged, does not increase either sector's relevant raw potential, and changes only a declared bounded DATA patch. For a source in P, the component-safe local-edge theorem prevents loss of component safety because V_0<M<M_edge. Thus K_hs P is contained in P. Every sqrt(B_h) and exp(-s B_h/2) preserves P because it commutes syndrome and all flags. Each jump-history Kraus of exp(t Z_h), and hence every Kraus of T, therefore preserves P.

Equivalently the Schrödinger adjoint T_* maps P-supported states to P-supported states. This is exactly what is needed: if P A P<=0 then, for any positive P-supported rho,

    Tr rho T(A)=Tr T_*(rho) A<=0,

so P T(A) P<=0. Apply this to the basin-restricted exact-similarity estimate for L_eff V_+. The resulting restricted inequality is the claimed one for L T(V_+). The linear inverse T^{-1} need not be positive or preserve P; neither property is used. Its only use is the globally exact local similarity identity and remainder decomposition.

## 3. Commutation of the dressed F with P needs, and has, extra symmetry

Subspace preservation alone would not prove [P,F]=0. Here each K_hs=F_hs Pi_hs has a definite character under conjugation by every DATA stabilizer. All B_h commute DATA stabilizers. Hence every Z_h and its exponential commute with stabilizer conjugations, and the syndrome-block-diagonal fixed algebra is invariant. Moreover each jump sqrt(B_h)K_hs and each no-jump term commutes every C'_j, so T preserves every exact bad-mask block. Starting from V_+, F is simultaneously syndrome-block-diagonal and bad-mask-block-diagonal.

The basin projector P is a function only of syndrome and bad mask: a fixed minimum representative is selected for each syndrome, and V_0 is scalar on each joint syndrome/mask sector. Consequently [P,F]=0 exactly, even though F can have ready/reference clock coherences inside one mask block. This is sufficient for the standard killed adjoint identity.

## 4. Retained common bath and local perturbations

A local finite-dimensional unitary dilation of the fixed-depth CP circuit uses fresh product environments, distinct from the physical retained bath. If T(O)=E[U_T^dagger(O tensor I_E)U_T], then for a physical perturbation N_Z^* acting trivially on the fresh environments,

    M_Z=Ad_U_T (N_Z^* tensor id_E) Ad_U_T^dagger,
    N_Z^* T(O)=E[U_T^dagger M_Z(O tensor I_E)U_T].

The orientation is correct by direct substitution. M_Z is HP, identity-annihilating, has unchanged cb norm, and enlarges only the physical support by a bounded circuit cone. It may retain arbitrary action on the shared bath. An operator on one physical patch plus that bath commutes every dressing gate disjoint from the physical patch because dressing gates act trivially on the bath.

The augmented orbit estimate extends to all such HP cb-bounded maps: on each orbit of the bounded local DATA-Pauli/auxiliary-matrix algebra, subtract a scalar orbitwise minimum of f_A. The remaining range is bounded by a fixed multiple of f_A because at most a fixed number of check/token occupancies change. Complete boundedness makes the bound stable under both fresh environment and external bath/reference. Positive conjugation and E preserve it. Summing bounded-incidence causal cones contributes only C|A| per animal, hence

    N_t^* T(V_+) <= eta C_noise T(W_+).

No bath reset, reduced-DATA noise assumption, or replacement of coherent noise by Pauli probabilities is present. Bath-only Hamiltonian evolution commutes U_T,P,F and contributes no boundary term. As usual, unrestricted bath-only evolution means unrestricted within a well-defined joint propagator.

## 5. Killed moment and all exit sources

With [P,F]=0 the exact compressed adjoint identity is

    (L^P)^*(PFP)=P L^*(F)P-sum_K P K^dagger (I-P)F(I-P) K P.

The final term is positive and may be deleted for an upper drift bound. Since T(W_+)>=F, the asserted clean drift plus noise margin gives the O(N) killed F-moment, using trace nonincrease and initial F<=V_+=O(N). The encoded ready input is unchanged by the frame U.

A bounded physical operator in the gauged frame changes only boundedly many syndrome/flag-token vertices. The augmented local-orbit ratio is a fixed constant. The enlarged-geometry DATA edge theorem still applies: the same connected container J(K) contains the confined source syndrome, and occupied flag tokens can only increase its animal weight. Consequently a basin exit cannot first arise by producing a component-unsafe target below M_edge. It must cross the raw V_0 cutoff, so every source block of QHP, QKP, and QK^dagger KP is in V_0>=cM. The common boundary source projector B therefore obeys B<=V_0/(cM)<=F/(cM), with no extra sum-over-patches factor. Its killed mass is O(N/M).

The full generator minus the embedded compressed generator is controlled by boundary cross-block Cauchy–Schwarz, including the loss K^dagger K. All actual clean and noisy patches have O(N) total bounded local norm and fixed incidence; bath-only terms have zero difference. Thus the full-versus-killed reference-stable trace-norm estimate is O(Nt sqrt(N/M)). No classical trajectory interpretation is needed.

## 6. Canonical logical factorization survives the frame and flags

The explicit U is bounded-depth and local. Gauged Hamiltonian, reset, noise and loss operators have bounded DATA supports after the declared enlargement. Expanding a general such operator in the finite local DATA Pauli basis leaves arbitrary auxiliary/bath coefficient operators. For every retained source/target syndrome block, the component-safe local-edge theorem says each local Pauli has identity canonical logical action, up to a syndrome-dependent scalar phase. Therefore every compressed Hamiltonian, gain and complete loss acts as I_L tensor an operator on syndrome/controller/bath.

The projector P itself is I_L tensor an ancillary projector. Initialization is an arbitrary logical/reference state tensor one fixed ready-controller and bath state, so the killed encoded-to-decoded map is exactly a_t id_L with input-independent 0<=a_t<=1. Arbitrary initially logical-dependent baths would invalidate this inference but are explicitly excluded. Trace preservation of the full channel bounds 1-a_t by the same full-versus-killed error. Applying the fixed canonical ideal decoder after U^dagger gives the displayed diamond bound with a harmless factor two.

This conclusion concerns dressed DATA and the prescribed ideal frame inverse/readout. It makes no assertion that pending bare DATA already have the decoded state, and it does not certify noisy physical extraction.

## 7. Qualifications to retain

- The Sections 5–8 clean augmented drift and explicit monomial/flag identities remain independent inputs to this subreview.
- Both CSS sector component conditions are imposed; no mixed-sector container-disjointness claim is used.
- The local geometry must include the full gauge, credit, nominal read/reset, perturbation and loss supports.
- The standard asymptotic proof requires encoded vacuum in P, ell>=8s, and ell below distance/confinement. For ell proportional to sqrt(N), these hold for sufficiently large N. Smaller fixed sizes can instead be covered by a separately enlarged trivial constant; they should not be said to follow from the killed-vacuum argument itself.
- Joint dynamics must exist. Bath-only unbounded Hamiltonians are handled without a bath norm budget only under that standard well-posedness condition.

No external mutation or original-source edit occurred.
