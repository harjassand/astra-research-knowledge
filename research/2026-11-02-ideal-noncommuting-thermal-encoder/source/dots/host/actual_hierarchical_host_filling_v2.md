# Logarithmic hierarchical-host filling for the actual recursive memory

2026-11-01, version2 (paired completion). **Proof candidate for independent geometry audit.** This note earns an actual bounded-degree analytical host and removes its Steiner vertices by a bounded-load quotient. It does not assert that arXiv:2411.02384v3 applies literally without the supergraph extension identified below.

## 1. The actual ancestry host

At final level L, include every actual Tanner vertex (X check, qubit, Z check) from levels0,...,L as an analytical vertex. Include:

* every within-level Tanner incidence edge;
* within-level edges between overlapping checks and between qubits belonging to a common check;
* an ancestry edge from every fine basis cell to the unique old vertex v indexing its direct-sum local complex C_v;
* optionally, edges between top physical qubits within any selected fixed Euclidean range R.

The ancestry relation is not a guessed spatial parent: it is the ACTUAL decomposition C_fine=⊕_v C_v from §3.2.2 and its dual. Each fine Tanner vertex has exactly one parent. Each parent has at least two children (the local gadget has two copies), and at most

    B=14(2ell^2+2ell−1)

children. A bound for an X-star gadget is |Y_x(0)|+|Y_x(1)|+|Y_x(2)|≤F_x(2ell^2+2ell−1), F_x≤14; Q gadgets have at most14ell−5 cells, and endpoint gadgets have2. RZ is dual.

Each within-level Tanner vertex has degree≤7. The added overlap/co-occurrence cliques contribute at most42 neighbors. Hence the host degree obeys

    Delta_H≤B+50+D_R,

where D_R is the optional bounded physical-neighbor degree. Bounded physical density makes D_R a constant for fixed R. All constants are independent of L and n.

Every check is nonempty, so the number of Tanner vertices at a level is ≤8n_i. Also n_(i+1)≥(ell+1)n_i≥4n_i. Consequently

    |V(H_L)|≤8Σ_i n_i≤(32/3)n_L.

No auxiliary host vertex is introduced into the quantum Hilbert space, the Hamiltonian, or a physical device. These are analytical labels for already defined coarser cells only.

## 2. Actual filling has logarithmic host radius

Use the accepted two-sheet contraction rather than physical-radius estimates. At every RX step, the chosen X cocycle readout is supported on a Q apex or its incident radial X-gadget paths. Each participating fine cell is joined in H to its gadget's old label; an old X label is one Tanner edge from its old Q neighbor. Thus the parent output lies within at most2 host edges of a contributing fine input. Its anchored primitive uses only a touched X gadget, again within2 host edges of that input. The dual statement holds for RZ Z.

The complementary coarse map is parity on disjoint Q blocks and is supported within one ancestry edge. Its homotopy reconstruction uses the FULL local-cohomology contraction, with extra check-relation spaces retained. A local h stays in one gadget; g moves only X→Q→Z. Corrected HPL maps have at most two g factors. Therefore a one-level correction, coarse map or lifted generator moves at most a fixed number of host edges. A conservative common bound4 is sufficient for these moves; using a larger fixed bound leaves the conclusion unchanged.

After at most t≤2ceil(log2(max(1,m)))+O(1) coarse steps, a weight-m stabilizer's residual vanishes, or the finite seed is reached earlier and filled there. Every nonzero residual or correction retains an ancestry path to the original support, because untouched gadgets give zero primitive and all linear maps send zero to zero. Lifting each selected generator back to the top adds at most another4 host edges per level.

Hence there are family-independent constants c0,c1 such that every stabilizer p of weight m has a representation using ACTUAL TOP Hamiltonian checks with

    dist_H(alpha,supp(p))≤c0+c1 log(1+m)

for every selected top check alpha. Their entire qubit supports are within one further host edge. One can conservatively use a form c0+16ceil(log2(1+m)), with c0 absorbing the finite seed and endpoint conventions. The proof requires only the bounded-map support claims, not this nonoptimal numerical coefficient.

This bound holds for globally known stabilizers without a distance cutoff. For local centralizers, the separately proved power-law distance excludes nontrivial logicals below d.

## 3. Eliminate all analytical Steiner vertices without dummy checks

The ancestry edges form a forest whose leaves are exactly the top Tanner vertices. Every internal node has at least two children. Match each internal node injectively to a descendant leaf. Such a matching exists constructively: process subtrees postorder, assigning the internal node one unused descendant leaf; a subtree always has more leaves than internal nodes. Equivalently, descendant-leaf sets are laminar and satisfy Hall's condition.

Define f(v) as that matched leaf for internal v, and f(t)=t for every leaf t. Then

    max_t |f^(-1)(t)|≤2.

This is an analytical many-to-one vertex map, not a physical encoding or operation. Every host edge may now be projected to an edge between its leaf images; self-loops are ignored. The resulting graph on the REAL top Tanner vertices has degree≤2Delta_H. Distances do not increase along projected host paths. No zero Hamiltonian terms or fictitious stabilizers are inserted.

## 4. Compatible graphs by paired completion on real checks/qubits

For each top Tanner leaf t choose an INCIDENT pair (a(t),q(t)) of an actual top check and qubit:

* if t is a check alpha, set a(t)=alpha and choose q(t)∈supp(alpha);
* if t is a qubit q, set q(t)=q and choose a(t)∈supp_c(q).

Every check/qubit has such an incident partner. Project every host edge uv to a check edge a(f(u))—a(f(v)). The check graph Gamma_c contains these projected edges and the original check-overlap graph. If fixed-range physical edges x—y are included, ALSO insert ALL edges supp_c(x)×supp_c(y), not just the selected incident-check pair.

The real check vertices are fixed by this projection. A check receives at most2(1+w_c) host vertices. Thus, writing D_R for maximum physical-nearness degree, a safe bound is

    D_c:=degree(Gamma_c)≤16Delta_H+w_c w_q D_R.

Define the FINAL qubit graph Gamma_q by paired completion, not by an unrelated projection:

* make supp(alpha) a clique for each actual check alpha;
* for every Gamma_c edge alpha—beta, add all edges supp(alpha)×supp(beta).

Its maximum degree is bounded by

    D_q≤w_q w_c(D_c+1)≤49(D_c+1).

Both graphs have only REAL top check/qubit vertices. No Hamiltonian terms are changed. This completion contains all simultaneously projected host qubit edges q(f(u))—q(f(v)): their endpoints belong to the two projected check supports, or to the same check support when the projected check edge collapses. It also contains every desired physical-nearness edge, due to the full check-pair lift inserted above.

The required exact support-connectivity implications now follow immediately:

(A) If A is connected in Gamma_q, then supp_c(A) is connected in Gamma_c. For a qubit edge x—y, either both endpoints lie in one check support, or x∈supp(alpha), y∈supp(beta) for a Gamma_c edge alpha—beta. The incident-check sets supp_c(x),supp_c(y) each form an original overlap clique and include alpha,beta respectively. Thus their union is connected. Extend along A. No checks outside supp_c(A) are needed, and |supp_c(A)|≤w_q|A|.

(B) If S is connected in Gamma_c, then supp(S) is connected in Gamma_q. Each check support is a clique, and every check edge has the full bipartite connection between its two supports. No qubits outside supp(S) are needed, and |supp(S)|≤w_c|S|.

This paired completion is deliberately explicit; neither implication is inferred merely from bounded degree or from choosing two independent quotient graphs.

## 5. TQO-II in the analytical real-check supergraph

Let S be ANY nonempty set of actual top checks (connectedness is not required for this estimate), and let p∈G with supp(p)⊆supp(S). Then wt(p)≤w_c|S|. The host filling theorem and quotient projection put each selected generator alpha within

    c0+c1 log(1+w_c|S|)+1

Gamma_c-distance of S. The extra1 accounts for a support qubit's chosen incident check possibly differing from the member of S containing it; those two checks share that qubit and are adjacent.

For integer s≥1, log(1+w_c s)≤s log(1+w_c). Thus for a constant ell_* independent of n,

    G(S)⊆G_(B_{ell_*|S|}^{Gamma_c}(S)).

This has exactly the algebraic form of Eq.(2.15) of arXiv:2411.02384v3, and holds in particular for every connected S and every desired cutoff d_tilde=Theta(d). It is established on Gamma_c, NOT asserted on the original overlap graph.

Ball growth on both final graphs is at most exp(kappa r) for a constant kappa≥log(max(D_c,D_q)+1). Power-law code distance was established separately and supplies d_*≥c log n. H0 and all its checks are unchanged.

## 6. Precisely what theorem extension remains

The primary paper defines its graphs literally from shared physical supports (§2.1), and explicitly says its perturbation locality uses those graphs (§2.3). Therefore simply citing Theorem2.1 with our shortcuts would be unjustified without an extension argument.

A candidate extension replaces the literal overlap/co-occurrence graphs by bounded-degree SUPERGRAPHS satisfying(A),(B), while leaving support_c, supp, operator classes, check projectors, Hamiltonian and Hilbert space unchanged. Preliminary source inspection identifies the relevant uses:

* §3.1 word support algebra and disjoint-word commutation use actual check supports, not the converse “every graph edge is an overlap.” These identities remain unchanged.
* §3.3 connected initial word covers use(A).
* §3.4 and AppendixB Pauli↔word norm estimates use(A),(B), unchanged cardinality bounds w_q,w_c, and ball growth.
* §§5.1 and8 use the TQO-II neighborhood and check-ball growth.
* The iterative word commutator estimates use overlap of word SETS and connected unions, which still hold in a supergraph.

This is a specific proof-transfer candidate, not yet a claim that every line of the published theorem has been independently audited. Constants kappa and ell_* must be replaced by the new values. The original qubit/check degrees used in incidence bounds remain w_q,w_c; graph growth uses the new quotient degree.

Fixed-range physical perturbations can be included by the optional physical-neighbor edges above. Their bounded-size supports then have bounded connected covers in Gamma_q, so sufficiently small physical interaction strength gives a finite small published Pauli norm, with possibly enormous fixed constants. No claim is made here for arbitrary slowly decaying physical tails: the theorem's exponential connected-SIZE norm must be checked separately.

Likewise, a quasi-local unitary in the shortcut graph is NOT automatically physically quasi-local. Any physical preparation/phase-equivalence conclusion or filtered-parent consumer requires its own argument.

## Primary source inspected

De Roeck–Khemani–Li–O'Dea–Rakovszky, arXiv:2411.02384v3, https://arxiv.org/pdf/2411.02384, §§2.1–2.3,3.1–3.5,5.1,8 and AppendixB. The abstract PDF is dated12August2026. No alternate access was attempted for the separately blocked work arXiv:2411.01002v3.

## Version provenance

Version1 remains at `actual_hierarchical_host_filling.md`, SHA2564628c91a701b43e43738926d0e435a19791960c953321ebabb85a465a9ce65a6. Version2 explicitly uses the paired-completion construction requested by the independent theorem-interface audit. It does not modify frozen filling or distance proofs.
