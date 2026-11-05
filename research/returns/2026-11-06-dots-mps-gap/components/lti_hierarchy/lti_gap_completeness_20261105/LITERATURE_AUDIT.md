# Primary-source and scope audit

Checked on 2026-11-05. This is a targeted literature screen, not an exhaustive proof of novelty. All four primary papers below were acquired and read locally; acquired bytes and hashes for three are in sources/manifest.json. The Rai HTML is rai.html.

## Exact hierarchy being addressed

Kshiti Sneh Rai, Ilya Kull, Patrick Emonts, Jordi Tura, Norbert Schuch, Flavio Baccari, **A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems**.

- arXiv:2411.03680v3, revised April 1, 2026; first version November 6, 2024.
- Quantum 10, 2065, April 13, 2026.
- https://arxiv.org/html/2411.03680v3
- https://doi.org/10.22331/q-2026-04-13-2065

The exact object is the unrestricted primal of Eqs. (11)-(12), equivalently the LTI dual in Eq. (17): rho positive, equal left/right (n-1)-site marginals, Tr(rho h_1)=1, objective Tr rho[h_1^2+sum_(j=2)^(n-1){h_1,h_j}]. The manuscript uses nearest-neighbor h_j in this formula. This package explicitly restricts the nearest-neighbor hierarchy to n>=3, so every omitted pair has disjoint support. Its monotonicity and finite-periodic validity then give gamma_n nondecreasing and gamma_n <= Delta_N for n>=3 and N>=2n. The formal n=2 SDP is invalid as a general gap bound, as the included exact AKLT counterexample demonstrates.

Section 5 explicitly says: “An issue we did not resolve in this paper is the completeness of our hierarchy.” It then distinguishes eventual detection of a positive gap from convergence to the true gap and leaves the 1D frustration-free question open.

**Important numerical-variant exclusion:** Appendix D Eq. (115) restricts the divergence variable to P_(n-1)^perp Y P_(n-1)^perp. The main proof does not assert same-level equivalence. Its dual constraints are weaker than unrestricted full LTI. A separate check, now documented in PROJECTED_VARIANT_EXTENSION.md and the independent review, shows they preserve exactly the energy moments needed, giving a completeness extension with the source’s literal one-level indexing shift.

## Other relevant completeness/convergence results

### Rao: exact finite-system completeness, different limit and algebra

Sujit Rao, **A convergent hierarchy of spectral gap certificates for qubit Hamiltonians**, arXiv:2510.08427v2, October 2, 2026.
https://arxiv.org/html/2510.08427v2

Section 1.2.1 explicitly describes systems “on a finite lattice.” Its NPA construction uses constraints selecting the exterior-square representation of su(2^N), and converges at level N for a given N-qubit Hamiltonian. It can handle frustration and nonlocal geometry. This is a genuine prior completeness theorem, but it is not a proof that the fixed-window Rai hierarchy becomes exact for the thermodynamic periodic gap.

### Xu et al.: general bulk-GNS upper bounds and uncomputability from below

Xiangling Xu, Matthias Schötz, Jie Wang, Victor Magron, Igor Klep, Omar Fawzi, Marc-Olivier Renou, **The bulk spectral gap is certifiable from above but uncomputable from below**, arXiv:2606.03836v5, October 28, 2026.
https://arxiv.org/html/2606.03836v5

Theorem 2.5 proves completeness of a state-polynomial SDP feasibility hierarchy for KMS ground states with a specified locally non-degenerate bulk gap. This yields convergent upper bounds. The lower-bound impossibility construction is general and is not under the proper injective-parent promise here. In its nonhalting construction, the A-product state is explicitly not the only KMS ground state; the chi-product state is also one. The interaction embeds computational terms which can have negative finite-interval energy and is not shown to be frustration free. Thus this result is not a direct obstruction to our restricted theorem.

Its operator-algebraic bulk-gap notion is also not silently interchangeable with a limit of finite periodic gaps. Our theorem uses the latter definition and proves that limit exists; it does not separately establish equality to a GNS spectral gap.

### Rozman, Molnar, Schuch: complete positive detection and convergence to the open-chain gap

Milán Ádám Rozmán, András Molnár, Norbert Schuch, **Lower Bounds on Spectral Gaps of Parent Hamiltonians via Tensor Networks**, arXiv:2607.19078v1, July 21, 2026.
https://arxiv.org/html/2607.19078v1

Section 3.2 defines parent Hamiltonians by eventual equality ker H_N=S_N and distinguishes these from weak parents. Theorem 6 gives uniform open and periodic spectral gaps for normal/block-normal parents, recovering and simplifying classical FNW/Nachtergaele conclusions.

There is also a relevant quantitative convergence claim that must not be omitted: Section 4.4 says the periodic lower bound from their Lemma 2 converges to the infinite **open-boundary** gap, specifically limsup_n Delta(H_n^OBC), as p,q increase with q/p increasing. This does not establish convergence to the actual periodic gap when edge excitations make the two limits differ.

They compute the overlap parameter through matrices of fixed virtual dimension, with the local-block diagonalization remaining the exponential bottleneck. The reported AKLT periodic lower bound is 0.2827; the unrestricted Rai hierarchy already gives stronger numerical AKLT certificates in the original Rai paper. Our work produces no improved numerical certificate over either method.

## What the candidate would add, if correct and original

The proposed result is exact convergence of the existing unrestricted Rai lower-bound hierarchy to the periodic thermodynamic gap for proper injective-MPS parents. Positive gap detection for these models is already known. The candidate's proposed contribution is removal of possible asymptotic underestimation of the actual periodic gap, using a quantitative dual-to-periodic-state boundary construction.

The targeted searches included exact arXiv ID plus completeness, Rai plus convergence, LTI plus gap plus MPS, and parent-Hamiltonian gap convergence. No primary source proving this precise statement was found. This does not rule out unpublished or poorly indexed prior work.

## Why the assumptions suffice for the boundary construction

1. The local interaction is finite-dimensional, translation invariant, positive semidefinite, and frustration free.
2. A normal MPS tensor A is given. Its transfer map is primitive after the stated blocking convention, with a faithful fixed point. This supplies exponentially convergent, uniformly invertible block Gram matrices.
3. For every sufficiently large open interval, ker H_interval equals exactly the MPS boundary space S_length. This is stronger than merely having the MPS as a ground state, or having a unique infinite-chain MPS ground state.
4. The uniform open-chain gap follows from standard proper-parent results. Alternatively take a fixed long block whose kernel is S_L, compare it to I-P_L using its finite positive gap, and compare sums of these blocks with the usual canonical MPS parent. This yields a positive uniform bound.
5. Those exact kernels ensure that the buffer projectors are controlled by their local Hamiltonian energies. Without this equality, the key defect-weight inequality need not hold.
6. Finite periodic ground states are unique for sufficiently large lengths. Single-site excitation quotients give Delta_N <= 2||h|| in the nearest-neighbor setting.
7. Delta_N means the least strictly positive eigenvalue of the N-site periodic Hamiltonian. The proof does not assume Delta_N converges. The two inequalities gamma_n <= inf_(N>=2n) Delta_N and Delta_n <= gamma_n+o(1) force both limits to exist and agree.

The explicit map uses joint access to the two end buffers as a mathematical state-construction device. No locality-constrained quantum hardware implementation is claimed.

## Subsequent independent priority supplement

PRIORITY_AUDIT_SUPPLEMENT.md adds precise Rai Section 3.2 / Eq. (37) source locations, classical Nachtergaele Theorem 2 and Proposition 12, and adjacent Scheer–Khalaf arXiv:2610.18854v1 (October 13, 2026). It also gives explicit proper-parent examples whose open and periodic gap limits differ, including an entangled tensor-product example. That prevents an invalid shortcut from existing open-gap convergence to the proposed periodic result. This supplement audits priority and assumptions, not the boundary-repair proof.

Review scope: all three internal adversarial audits cover the corrected nearest-neighbor unrestricted theorem. Only the first separately checked the projected-Y extension. No report establishes novelty, external peer review, formal verification, practical superiority, or an independently proved GNS identification.
