# Non-Clifford Choi-buffer interface test
2026-10-30. Conditional transfer established algebraically; no unconditional compatible-code transfer established. This is an interface obstruction, not an impossibility theorem for non-Clifford autonomous computation.

## Native requirements actually tested
Sources read: `producer-workspace/GLOBAL_EXPONENTIAL_COMPILER.md` §§1,3,6,7; `producer-workspace/GENERAL_ACTIVE_DENSITY.md`; `producer-workspace/INDEPENDENT_REVIEW.md`.

The memory input is stronger than LDPC plus decoding: fixed positive constants d/N, h, kappa, r_dec, bounded footprints, and a commuting integer potential with U(e)>=h r(e) and #active_hubs(e)>=kappa U(e) throughout the common reduced-error radius. Each actual selected local orbit-minimizer is idempotent, decreases U at least one, and leaves the opposite CSS sector unchanged. The native proof uses

    sum_h (I-Phi_h*) exp(sE) >= kappa(1-exp(-s)) U exp(sE),
    2 r0 < d/N,     e_cut < h r0/2.

The GPT active-density proof specifically uses two endpoint correction incidences per qubit, Delta²-sized local views, primal/dual robustness, local tie-sensitive reversal, and overlap-ball charging. Its constant is cY/[2 Delta²(1+cY)], cY=alpha/(16 Delta(1+3Delta²)), alpha=delta²/648. The independently reviewed confinement radius is smaller than the active-hub existence radius. None of these statements is a generic consequence of local testability.

## Primary-source comparison
1. [Li–Li–Liu, arXiv:2604.01874v2](https://arxiv.org/html/2604.01874), Theorem 1.1, full main governing statement: for r=3 the LDPC construction has distance Theta(N/log²N); the locally testable alternative has distance Theta(N/log⁵N) and soundness Theta(log^-5N). Both support nontrivial transversal logical CCZ. The main theorem does not promise individually addressable CCZ. Therefore these particular families cannot satisfy a fixed r0>0 with 2r0N<d. No decoder/local-decrement statement was identified; two-way product expansion of their punctured RS constituents does not identify their sheaf complex with the reviewed GPT local-view system.

2. [Golowich–Guruswami, arXiv:2510.06798](https://arxiv.org/html/2510.06798), Theorems 1.1–1.2: the linear-distance family uses O(sqrt(N)) locality and growing alphabet, with noncommuting subsystem measurements and a polynomial-time decoder. The smaller-locality variant has Theta(N^(1/3)) locality and still larger alphabet. These published interfaces do not give fixed-dimensional, fixed-footprint, commuting-energy local correcting instruments. Their noisy-syndrome decoder is not the missing autonomous drift.

3. [He–Vaikuntanathan–Wills–Zhang, arXiv:2507.05392](https://arxiv.org/html/2507.05392), Theorem 1.1 and §3: constant-rate linear-distance qubit CSS codes permit a chosen logical triple's CCZ by depth-one physical CCZ. The construction uses algebraic-geometry codes and fixed-alphabet conversion. This supplies the desired logical addressability and distance but not a bounded-check local energy or the GPT active-hub theorem. Do not assert a newly proved no-LDPC theorem; the needed interface is simply not supplied here.

4. [Menon et al., Magic Tricycles, PRX16 021014](https://journals.aps.org/prx/pdf/10.1103/ghhp-cytl), §I.B and Appendix F: finite-block code examples and bounded-check, constant-depth CCZ circuits are relevant engineering resources. Their single-shot/circuit-noise evidence uses measurement-window BP, BP+OSD, and postselection/BP+LSD variants. It is not a uniform-in-N linear-radius active-density theorem for local physical correcting drift. Thus it cannot certify the requested autonomous buffer by substitution.

## Concrete conditional Choi transfer
Assume a code family satisfies the actual native requirements and has a fixed-depth, bounded-participation physical W preserving the relevant three-block codespace and implementing the desired logical CCZ. Start with the independently established three raw-physical-Bell buffer construction, and act with W on its B halves.

For C=Ad_W, conjugate the full mathematical memory instrument, not only its ideal terminal Pauli correction:

    L'=C L C^-1,  Phi'_h=C Phi_h C^-1,
    U'=W U W†, E'=W E W†, F'=W F W†.

Every operator drift inequality transfers exactly by unitary conjugation. Joint-reference correctness transfers too. The ready/target state becomes the logical Choi state (I_A tensor W_B)|Bell_L> once the original buffer's target and code-preservation hypotheses hold. No independent encoded |+> factory is needed for this conditional argument.

For disjoint physical CCZ triples, each support expands by at most three. Commutativity of energy terms, positivity, idempotence and decrement spectra are preserved. The safe basin must also be conjugated: it is not literally the same Pauli-sector label space. Arbitrary bounded-body physical noise pulled through W remains bounded-body with bounded incident norm inflation, so the original general-noise theorem can apply after fixed constants are reselected.

Teleportation byproducts are W P W†: for one triple W X_i W†=X_i CZ_jk and W Z_i W†=Z_i. These are finite local Clifford corrections, not a magical global decoder. A nontrivial logical CCZ polynomial is not automatically the chosen individual logical CCZ.

Native site-partition correction (15:12 UTC): the preceding locality concern applies ONLY if the old elementary sites must remain separate. The declared model permits grouping corresponding B-resource factors of the three blocks into one fixed-dimensional cell R_i. For W=product_i CCZ(B_1i,B_2i,B_3i), W is onsite on R_i. An original hub/resource term H_(h,B_ai) conjugates to an operator on {h,R_i}; a resource/resource term has at most two new cells. Hub resets/monitors are unchanged; resource-local jumps remain onsite. Thus exact conjugation of the FULL actual generator preserves two-grouped-site Hamiltonians and onsite jumps without a new finite-controller recompilation theorem. This matches the explicit paired-cell precedent in `producer-workspace/REQUEST_DRIVEN_SUBSYSTEM_ROUTER_AND_MODE_OBSTRUCTION.md`, §2, which says the native hub/resource Hamiltonian remains hub plus one paired resource cell.

Grouping must include whatever fixed-dimensional ancillary factors belong to each original resource site, rather than silently splitting an old site. The cell dimension and incident degree increase only by constants (three blocks). All old onsite joint noise remains allowed, and the stronger new-cell joint noise also pulls back to allowed bounded-body noise with constant incidence inflation, after threshold constants are adjusted. Cross-block physical co-location/interactions are now a declared resource; this is not preservation of elementary-site locality or inter-party LOCC. Choi-source/terminal operations still need their previously required implementation checks, but conjugating already established onsite/two-site source/terminal instruments needs no new locality synthesis.

This shortcut is exact for depth-one disjoint triples, including a fixed permutation matching. A general fixed-depth CCZ circuit with overlapping triples need not admit a bounded-size disjoint grouping making every gate onsite: its connected components can grow. For that broader case the original bounded-support/recompilation caveat remains relevant.

## Why merely weakening the distance does not finish the transfer
For the almost-good family, allowing r0(N)=O(log^-2 N) already forces the linear-in-N energy cutoff coefficient to vanish. The published qLTC soundness additionally does not give fixed h for the raw check energy, although a different potential might. The native moment bound requires fixed positive margin s' e_cut - q_t - nu; its fixed controller/noise costs cannot simply be ignored when e_cut tends to zero. This is an obstruction to applying the current theorem, not proof against a new scale-dependent theorem.

## Decision
Do not promote a protected non-Clifford consumer from these sources. The concrete Choi construction isolates the missing bridge cleanly: a SAME family with bounded physical CCZ plus fixed-radius local confinement and quantitative active-hub descent, with native grouped-site conjugation when its CCZ triples are disjoint (or an additional native realization argument otherwise). The closest almost-good code source fails the present linear-radius interface on its stated distance alone. No further speculative survey is needed to settle this attempted substitution.
