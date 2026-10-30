# Quantum Tanner local energy -> weighted animals -> linear-size coherent barrier

2026-10-30. Constructive interface proof. **The new active-hub density lemma is a separate load-bearing input under current derivation/audit; it is not implied by the published existence-of-a-flip theorem.** Subject to that lemma and the reviewed weighted-animal/killed-basin theorem, this lift gives exp(cN), rather than exp(c sqrt(N)), ideal-atomic decoded memory.

## 1. Exact primary-source imports

Use the Gu–Pattison–Tang decoder, not raw syndrome-Hamming descent. Its local energy is U_v(e)=dist(e restricted to Q(v),C_1^perp); U=sum U_v is syndrome-computable. The local view has Δ^2 qubits and each qubit belongs to two energy views. The decoder accepts any view-supported flip strictly decreasing U. Their Theorem 12 supplies constant-rate linear-distance families and a linear decoding radius; Corollary 14 supplies U(e)>=Δ^(-2)dist(e,stabilizers) in that radius. Their Theorem 10 proves existence of a decreasing move, not a linear number of active hubs.

Primary text: https://arxiv.org/html/2206.06557, Definition 9, Algorithm 1, Theorems 10–13, Corollary 14. The independently fixed local codes and expansion hypotheses must satisfy the theorem in BOTH CSS sectors. Choose fixed constants 0<ε_0<ε_1<1/28, a sufficiently large fixed Δ, and the stronger admissible local-code distance condition δ<h^(-1)(ρ), with 0<ρ<1/2.

Conservative source constants are

    r_code >= (1-2ρ)^2,
    d_rel >= δ/[4Δ^(3/2-ε_0)],
    r_dec = δ/[6Δ^(3/2-ε_0)(1+2Δ^2)].

Only positivity and N-independence of these constants are essential below. The Δ-dependent constants can be impractically large.

## 2. The density input is explicit, not hidden

For one CSS sector, let A(e) be the set of local-view hubs at which SOME allowed bounded-support flip lowers U. The required strengthening is

    |A(e)| >= κ_T U(e)                               (AD)

for every stabilizer-reduced nonzero e with |e|<=r_AD N, for N-independent κ_T,r_AD>0. One actual accepted flip is selected at each active hub. The selection need not be a special globally coordinated set.

The current robust-density construction is being checked independently by the SSF proof auditor. Until that construction is written and verified, all conclusions below are conditional on (AD). The published linear-time sequential decoder alone does NOT prove (AD); a long cascade can have linear total work and very few initially active locations. The mismatch-based parallel decoder is also not automatically a theorem about this current-syndrome energy.

## 3. Unary energy tokens: no physical ancillas or fictitious syndrome bits

For each local energy view v introduce Δ^2 COMBINATORIAL vertices (v,j), 1<=j<=Δ^2, with occupation

    x_(v,j)(sigma)=1{j<=U_v(sigma)}.

Then

    |x(sigma)|=U(sigma).

These tokens are functions of existing commuting stabilizer-syndrome projectors. They add no physical qubits, no measurements, and no reset resource. Their allowed configurations are restricted unary strings, but the weighted-animal inequalities hold on these configurations just as on arbitrary binary configurations.

Distance to a fixed linear codespace is 1-Lipschitz under one bit flip. For any data flip f,

    sum_v |U_v(e+f)-U_v(e)| <= sum_v |f intersect Q(v)| = 2|f|.

Therefore an accepted local-view flip, |f|<=Δ^2, changes a nonempty token set D with

    |D|<=k0:=2Δ^2,
    #removed tokens - #added tokens
       =U(e)-U(e+f)>=1>=β_T |D|,
    β_T:=1/(2Δ^2).                                   (1)

This is the exact bounded-flip progress needed by the weighted proof. It is NOT a claim about the Hamming weight of an arbitrarily chosen stabilizer generator syndrome.

For a physical Pauli supported on Z, only views meeting Z change. Over its entire local-Pauli syndrome orbit, the energy at v ranges over an interval of length at most |Z intersect Q(v)|. Thus at most 2|Z| tokens can vary in one sector (at most 4|Z| for both sectors). This remains N-independent for fixed support. The physical read projector's full data support, not just the correction mask, must be included in the nominal operator support bound.

## 4. Full-read geometry and component confinement

To evaluate a candidate on Q(h), the atomic hub reads the local stabilizer information for every energy view v whose Q(v) meets Q(h). Its complete DATA footprint is the union of those Q(v). This is a fixed-radius bounded-size region because Δ is fixed. The decoder can evaluate all candidate subsets by a constant-size lookup table; its constant can be exponential in Δ^2 but not N.

For data site q define J_q to contain a dummy vertex q, all energy tokens at views directly meeting q, and all energy tokens that can be changed by a hub whose FULL read footprint contains q. Add bounded-radius data edges so intersecting J_q sets join their data sites; include all full read, correction and allowed noise-support cliques. Define a mixed graph H using these data edges, links from q to J_q, and cliques containing all possible changed-token sets of a hub. All degrees and incidence constants are fixed independently of N. There are O(N) vertices, since |V_1|Δ^2=2N.

For a component C of a sectorwise minimum-syndrome representative E in this enlarged data graph, let J(C)=union_(q in C) J_q. Then:

* J(C) is connected and |J(C)|<=D0|C|.
* Different error components have disjoint J(C).
* Every occupied token in J(C) comes from the error C alone; a local view cannot contain errors in two distinct components.
* Every active hub belongs to exactly one component and its chosen changed-token set is inside that component's J(C).
* Every token lies in at most ν actual hub-change footprints, with ν fixed.

Choose

    ℓ=floor(c_* N),
    0<c_*<min{r_dec,r_AD,d_rel}.

Every component C of size <ℓ is itself stabilizer-reduced. Corollary 14 therefore gives

    U(C)>=h_T |C|,       h_T=Δ^(-2).                   (2)

In particular |J(C)|<=(D0/h_T)U(C). Applying (AD) to the isolated C gives at least κ_T U(C) active hubs. Because their full-read decisions are unaffected by other components, these are ACTUAL globally active hubs, not counterfactual local evaluations.

Equations (1), (2), (AD), and this geometry discharge the weighted proof's entire small-component interface, with occupied tokens replacing violated checks.

## 5. Weighted progress transfers literally after tokenization

For all nonempty connected animals A in H, define

    f_A(sigma)=theta^[u|A|-|A intersect x(sigma)|],
    V=sum_A f_A,       W=sum_A |A| f_A.

Dummy vertices are always empty. The sum is FULL, not truncated. For small fixed theta and u>0, V(vacuum)=O(N).

The per-move completion A -> A union D uses only: bounded changed-token set, its clique property, and the strict removal surplus in (1). It does not require token independence or literal stabilizer-bit flips. The one-poor-component completion A -> A union J(C) uses only: disjoint connected containers, energy confinement (2), bounded token incidence and active-hub density (AD). Hence the already reviewed charging proof gives

    L_clean^* V <= -γ W+bN                          (3)

on the tokenized small-component basin, with γ,b>0 fixed independently of N.

For clarity, one allowed parameter order is: choose u smaller than κ_T h_T/(4νD0) and small enough for β_T's per-move constraint; then choose theta small enough for the source-to-target entropy charges and animal summability. Large local degree changes constants but does not change their N-independence.

Each ideal hub is an actual local syndrome-measurement/conditional-Pauli CPTP instrument, acting at a fixed rate λ>0. There is no global staging, synchronized mismatch register, or hidden parallel round in (3).

## 6. Linear high-V boundary

The canonical syndrome gauge is still defined using the original sectorwise minimum DATA Pauli representatives, not token configurations. If a bounded local Pauli edge with support Z takes a small-component source E toward a minimum target F, the usual componentwise minimum-weight comparison gives, for each component K of E union Z union F,

    |K|<=2(|E intersect K|+s),       s>=|Z|.

All source components in K lie below ℓ, so their energy occupies at least h_T(|K|/2-s) tokens in connected J(K), whose size is at most D0|K|. Therefore

    f_(J(K))(source)
       >=exp{log(1/theta)[h_T(|K|/2-s)-uD0|K|]}.

Choose u<=h_T/(4D0). A source of any edge producing |K|>=ℓ>=8s then has

    V(source)>=exp[log(1/theta) h_T ℓ/8].              (4)

Since ℓ is proportional to N, this is a LINEAR-SIZE exponential barrier. Below it, every local edge has identity canonical logical action and preserves component safety. Tokenization has not changed the logical-distance argument.

## 7. Continuous coherent noise and the killed-basin consequence

Retain the common bath and use the initialized channel Enc(rho_LR) tensor sigma_B, with fixed sigma_B independent of logical input/reference. Add bounded local Hamiltonian terms and added bounded Lindblad terms, with a uniform incident joint-norm budget ε. Bath-only evolution is unrestricted subject to existence of the propagators. All physical support bounds include full nominal read-projector/correction patches and local noise operators/products.

The local orbit of a support Z varies only the bounded token set established in Section 3. The same orbit-oscillation inequalities therefore bound the noisy adjoint drift by ε C_osc W. For ε<γ/(2C_osc), (3) remains negative outside the vacuum-sized term.

Use the reviewed killed-basin construction with threshold half the boundary value (4). Its logical factorization, completely bounded full-versus-killed comparison, and normalization argument give

    ||Dec E_t Enc-id_L||_diamond
       <= min{2, C N^(3/2) t exp(-c N)}.               (5)

Here c,C and the noise threshold are positive N-independent constants depending on the fixed Tanner-code and atomic-channel parameters. The encoded dimension has k>=r_code N qubits. Thus (5), if (AD) is established, supplies constant encoding rate and an exponential-in-N ideal-atomic memory lifetime against sustained bounded local coherent/Lindblad noise with retained bath—without Pauli twirling or added depolarization.

The full ideal-atomic killed-basin review is an imported theorem; this note does not substitute for it. Its application to finite-duration transactional clocks remains separate. The physical controller's instantaneous dynamics is not (3), so no controller corollary follows just by changing the code family.

## 8. Recovery and resource scope

Ideal terminal decoding can scan local views, accepting strict U decreases until none exists. On the killed basin, V never increases and the component barrier cannot be crossed by these local steps. Progress forces U to reach zero, and the logical action remains identity. At most U<=2N accepted moves occur; a naive scan implementation is polynomial, with very large but fixed local lookup costs. This is mathematical ideal recovery, not a noise-tolerant physical extraction protocol.

There are O(N) atomic hubs with O(1) local read/workspace dimensions at fixed Δ. A dilation of each hub operation uses O(1) fresh local workspace, so the supplied entropy-removal CAPACITY at constant attempt rates is O(N) per unit time. This is not a Landauer heat calculation or a bound on the actual entropy removed in a quiet memory.

The intended new capability is the linear exponent and constant rate, not a numerical threshold improvement. Fixed-dimensional Euclidean routing, concrete low-degree practical Tanner families, initial fault-tolerant encoding, the physical-controller coherent-noise lift, and operational quantum retrieval remain separately charged obligations.
