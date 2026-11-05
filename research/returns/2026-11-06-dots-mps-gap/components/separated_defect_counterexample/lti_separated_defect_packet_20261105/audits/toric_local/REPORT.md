# Independent audit: exact LTI plateau for the square toric code

## Result and scope

For the usual finite-range truncation of H^2 used by the LTI gap hierarchy, the standard square toric code has **delta_LTI(W)=1 at every admissible finite rectangular level**, while the large periodic-system gap and the frustration-free vacuum GNS gap are **2**. These are the units Q=(I−stabilizer)/2, with h_r=Q^A_r+Q^B_r. Consequently this disproves universal convergence to the exact gap for that hierarchy. It does **not** disprove eventual detection of a positive gap. The obstruction is already present in the H^2 truncation, before the LTI relaxation, and has a simpler 1D Ising analogue.

No novelty claim is warranted from this audit. Targeted searches did not locate this explicit counterexample in the LTI literature, but its mechanism is elementary and familiar from deconfined defects/domain walls. The original hierarchy paper leaves exact convergence open and does not mention toric code; see literature below.

## 1. Exact cell geometry

At r=(x,y) in Z^2, put two qubits in one d=4 cell: a_r on the horizontal edge (r,r+e_1), and b_r on the vertical edge (r,r+e_2). Set

A_r = X(a_r) X(b_r) X(a_{r−e_1}) X(b_{r−e_2}),

B_r = Z(a_r) Z(b_r) Z(a_{r+e_2}) Z(b_{r+e_1}),

Q^A_r=(I−A_r)/2, Q^B_r=(I−B_r)/2, h_r=Q^A_r+Q^B_r.

All these terms commute. The cell support of h_r lies in r+{0,±e_1,±e_2}, hence in a 3×3 rectangle. The Hamiltonian is finite-range, frustration-free, and translation-invariant on d=4 cells. Each h_r has norm2. If a norm≤1 convention is imposed, replace h_r by h_r/2; the exact periodic/vacuum gap becomes1 and the hierarchy plateau becomes1/2.

For W=[a,b]×[c,d], the contained stars have centers

V_W=[a+1,b]×[c+1,d],

and the contained plaquettes have lower-left corners

P_W=[a,b−1]×[c,d−1].

Their equal cardinality is N_W=(b−a)(d−c). Let q_W=2|W| be the number of qubits.

## 2. Direct positive full-LTI dual operator

For each s in V_W let sigma_s^W be the maximally mixed joint syndrome state with A_s=−1, all other contained A_v=+1, and all contained B_p=+1. The independent commuting generators give the explicit normalized positive density operator

sigma_s^W = 2^(−q_W) (I−A_s) product_{v in V_W\{s}}(I+A_v) product_{p in P_W}(I+B_p).

Define rho_W=sum_{s in V_W} sigma_s^W. Its trace is N_W, and its exact expansion is

rho_W = 2^(−q_W) sum_{S subset V_W, T subset P_W} (N_W−2|S|) A_S B_T,

where A_S=product_{s in S}A_s and B_T=product_{p in T}B_p. The unconstrained boundary degrees of freedom are maximally mixed. Positivity is immediate from the syndrome-state sum, not guessed from the Pauli coefficients.

### Support lemma

Every finite product of infinite-plane stabilizer generators supported on the qubits of a cell rectangle U can be expressed using only generators individually contained in U. This expression is unique.

Proof for stars: a finite star product indexed by S has X support equal to the primal edge cut delta(S). Remove all edges E(U) belonging to the cells of U. If delta(S) is contained in E(U), membership in S is constant on each connected component of the remaining graph. The only finite components are the isolated vertices V_U; all other vertices lie in a single infinite exterior component. Since S is finite, it vanishes on that exterior. Therefore S is a subset of V_U. The same argument on the dual square graph gives T subset P_U for plaquette products. In a mixed product A_S B_T, X and Z support cannot cancel each other: an overlap produces Y rather than identity. Thus both individual supports must lie in U. Finally, there is no nonempty finite star or plaquette product equal to identity, since the respective full infinite graph is connected. This proves uniqueness as well.

### Exact marginal identity and full LTI

Let sigma_0^U denote the normalized maximally mixed all-plus syndrome state of the contained generators in U. Partial trace of the expansion, using the support lemma, gives

Tr_{W\U} rho_W = sum_{s in V_U} sigma_s^U + (N_W−N_U) sigma_0^U.

This depends only on the dimensions of U, up to translation. In particular, the opposite-face marginals are exactly equal in both directions. More generally, for every local observable O for which O and its translate both fit inside W, the expectation is translation-invariant: nonstabilizer Pauli words have coefficient0, and a supported stabilizer product has coefficient N_W−2|S|, unchanged by translation. This is full local translation invariance, not merely invariance of h moments.

Adding lambda sigma_0^W for any lambda≥0 preserves positivity and LTI and replaces the expansion coefficient by m−2|S| with m=N_W+lambda. Thus the proposed adjustable-vacuum-mass construction is also exact.

## 3. Dual objective and matching primal certificate

For every h_r supported in W:

Tr(rho_W h_r)=1,

Tr(rho_W h_r^2)=1,

Tr(rho_W h_r h_t)=0 for r≠t whenever both terms fit in W.

The first two equations hold because plaquette defects are absent and each contained star is the unique defect in exactly one sigma_s. The third holds because no syndrome in the mixture contains two star defects. Thus any canonical finite-cutoff objective consisting of h_0^2 plus retained positive multiples of distinct products/anticommutators has value1, with the required normalization Tr(rho_W h_0)=1. Every telescoping LTI correction pairs to0. Weak duality gives delta_LTI(W)≤1.

Conversely h_r^2−h_r=2 Q^A_r Q^B_r≥0, and every retained anticommutator is 2h_rh_t≥0 because the terms commute. The canonical generating local term at delta=1 is therefore positive with no telescoping correction. This gives delta_LTI(W)≥1 and proves exact equality.

## 4. Stronger proof: genuine global TI state, no subgroup lemma needed

Fix any finite hierarchy window/cutoff. Choose a sufficiently large L×L torus and two vertices u,v with separation greater than the window/cutoff in both relevant periodic senses. A finite Z string creates exactly star defects at u,v from a toric-code ground state. Let eta be its density matrix, and average over all L^2 translations to obtain a globally TI state eta_bar.

Every translated local window contains at most one of the two defects. Therefore for the local terms relevant to the hierarchy,

Tr(eta_bar h_r)=2/L^2,

Tr(eta_bar h_r^2)=2/L^2,

Tr(eta_bar h_r h_t)=0 for all retained r≠t.

Then rho_W=(L^2/2) Tr_{W^c}(eta_bar) is positive, exactly full LTI, normalized by h_0, and has objective1. This avoids any question about extensions of LTI marginals. These particular duals are reductions of actual globally TI finite-volume states.

Equivalently, on that two-defect state the full H has energy2 and H^2 has energy4, whereas the truncated [H^2]_W has expectation2 because its cross term between the distant defects was discarded. Thus [H^2]_W−delta H is already nonpositive somewhere for every delta>1. The loss precedes optimization over positive local generators.

The noncommuting limits matter: for fixed L and a cutoff eventually covering the torus, full H^2 is restored and gives2. The hierarchy instead takes a fixed finite cutoff and certifies all sufficiently large L, allowing defect separation to grow beyond each cutoff.

## 5. Exact periodic and vacuum GNS gaps

On an L×L torus, product_all_vertices A_v=I and product_all_faces B_p=I. Consequently star and plaquette syndrome defect counts are each even. The first nonzero energy for H=sum_r(Q^A_r+Q^B_r) is2; a single-edge Pauli Z creates two adjacent star defects and attains2. The fourfold torus ground degeneracy does not affect this gap.

In the frustration-free plane vacuum representation, any finite Pauli word produces an even number of star defects and an even number of plaquette defects, or a vacuum vector. Local Pauli vectors span a dense core. This yields vacuum GNS gap≥2, and the same single-edge Pauli gives equality. Naaijkens Prop.2.2 provides the rigorous lower bound4 in the convention H=−sum A−sum B; dividing energies by2 gives our bound2.

A single-anyon charged state has one unit of local defect energy relative to the all-plus vacuum convention. Do not conflate this with the spectral gap of a charged-sector GNS generator normalized at its own ground energy. Also use 'unique frustration-free plane vacuum,' not 'unique algebraic ground state': non-frustration-free charged ground states exist.

## 6. Simpler 1D warning

For the classical ferromagnetic Ising chain with h_i=(I−Z_i Z_{i+1})/2, the periodic gap is also2, while every finite-cutoff LTI level is exactly1. A pair of domain walls can be arbitrarily far apart; alternatively an n-site equal mixture of all n−1 single-wall locations and their global spin flips is fully LTI after multiplication by n−1. Its h moments are exactly those above.

Thus the toric example should not be advertised as the first reason for nonconvergence without a much broader literature review. It improves the structural setting by giving a unique frustration-free plane vacuum and topological order, but it does not solve positivity-detection completeness.

## 7. Literature checked

1. Rai et al., A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems, Quantum 10,2065 (2026), arXiv:2411.03680v3. https://arxiv.org/html/2411.03680v3 and https://doi.org/10.22331/q-2026-04-13-2065 . Sections2.1–2.3 define the H^2 truncation and LTI dual; Section5 leaves both eventual gap detection and convergence to the exact gap open. No 'toric' occurrence. Its discussion already cautions that the truncated minimizer can differ from the first-excited-state minimizer.

2. P. Naaijkens, Localized endomorphisms in Kitaev's toric code on the plane, Rev. Math. Phys.23 (2011),347–373, arXiv:1012.3857v2. https://arxiv.org/html/1012.3857v2 . Proposition2.2 gives the vacuum GNS gap lower bound4 in the −A−B convention, and Section3 constructs single-charge sectors. Its older blanket uniqueness language must be restricted to frustration-free vacuum states in light of later literature.

3. Nachtergaele, Sims, Young, Quasi-Locality Bounds for Quantum Lattice Systems. Part II. Perturbations of Frustration-Free Spin Models with Gapped Ground States, Ann. Henri Poincare23 (2022),393–511. https://doi.org/10.1007/s00023-021-01086-5 . Explicitly notes additional non-frustration-free infinite-volume toric-code ground states.

4. S. Rao, A convergent hierarchy of spectral gap certificates for qubit Hamiltonians, arXiv:2510.08427. https://arxiv.org/abs/2510.08427 . Different finite-system hierarchy using a representation/exterior-power construction; its convergence does not establish thermodynamic LTI completeness and does not contradict this obstruction.

Searches for combinations of toric code, LTI/locally translationally invariant, truncation, counterexample, and spectral-gap hierarchy did not find the explicit counterexample. This is only a negative search result, not priority evidence.

## 8. Computational sanity check

The adjacent check_lti.py enumerates the exact stabilizer Pauli expansion using integer bit masks, including the cardinality-dependent coefficients. It compares all translated rectangular marginals exactly. It passed W=2×2,2×3,3×3,3×4,4×3 (up to4096 Pauli coefficients). This is a check, not the proof; the argument above covers all rectangles.
