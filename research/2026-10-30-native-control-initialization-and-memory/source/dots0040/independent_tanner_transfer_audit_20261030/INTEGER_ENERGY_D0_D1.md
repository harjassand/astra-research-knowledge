# Integer-energy asynchronous DATA witnesses for the GPT decoder
2026-10-30. New deterministic transfer, conditional on the independently reviewable general active-hub theorem. This is not a claim that the general-density construction has passed review.

## Contract and geometry
Work in one CSS sector. Let U(E)=sum_v dist(E|Q(v), C_local) be the GPT potential. Write w=Delta^2 and h=Delta^-2. The actual decoder at an evaluated hub searches all subsets of its w-qubit view and executes a strictly U-decreasing one whenever one exists. Exponential-in-w search is a blocklength-independent constant, not a practical efficiency claim. Both sectors require the corresponding primal and dual robustness assumptions.

Use a fixed bounded-degree DATA graph G which contains as cliques: every full local decision read footprint, every energy view Q(v), every stabilizer check support, and every declared elementary fault support. A decision read footprint includes enough raw stabilizer syndrome to compute all local distances affected by EVERY candidate at that hub. No decoder memory or auxiliary mismatch state is used. Let d be the maximum number of raw check bits toggled by a one-qubit error in this sector.

The needed deterministic inputs are:
1. U is exactly a function of the measured sector syndrome, hence is unchanged by stabilizers and by any same-syndrome replacement.
2. U(E)<=2|E| and |U(E+F)-U(E)|<=2|F|. A correct move has integer decrease at least one and support at most w.
3. For reduced E with |E| below the GPT correction radius, U(E)>=h|E| (Corollary 14, not the larger Theorem 10 radius).
4. For reduced E in that radius, the number of active hubs is at least kappa U(E), where the general-density construction supplies kappa>0 independent of N.

Input 1 follows directly because the local check syndrome determines the coset modulo the local code whose distance defines U_v. Its nearest-codeword tie breaking is irrelevant to the distance. Input 2 is the distance-to-code Lipschitz inequality, with exactly two energy views incident to each qubit. Stabilizer invariance is therefore not an assumption about a hidden Pauli mixture.

Input 4 also holds for a not-necessarily-reduced error E of weight below the radius: choose a minimum-weight representative modulo stabilizers, of weight at most |E|, apply 4, and use syndrome invariance of U and of all activity predicates. This representative need not stay inside supp(E). Nevertheless every active hub must have a currently nonzero local energy in its full read region: if all affected energies were zero, no strict decrease would be possible. Thus its read region meets the ORIGINAL supp(E), which suffices for localization.

## A. Candidate persistence uses raw syndrome, NOT unary energy
Equal energy does not imply equal decisions. For example, distance to {00} gives energy one for both 10 and 01, whereas flipping the first bit decreases only the former. Consequently packing only unary-energy tokens would be an incorrect physical-window proof.

For each active hub select a valid initial candidate and associate its FULL raw-syndrome dependency set. These sets have bounded size and bounded overlap. A conflict graph therefore has bounded maximum degree D. An independent class contains at least

    kappa_p U_start candidates,   kappa_p=kappa/(D+1),

at distinct hubs with disjoint raw dependency sets. Follow each until: a correct move changes a dependency bit; its own hub is correctly evaluated; a bad event changes a dependency bit; or the window ends. Until resolution its full local decision data are unchanged, so it remains valid. Any correct evaluation must execute a strict decrease (possibly a different candidate).

A correct move toggles at most dw raw syndrome bits and resolves at most dw+1 packed candidates, including its own. Let C_res=dw+1. Its integer energy decrease is at least one. A bad mask F resolves at most d|F| candidates. If D_U is the total accepted energy decrease, Q is total bad support mass with multiplicity, and M counts unresolved packed candidates, then PATHWISE

    kappa_p U_start <= C_res D_U + d Q + M,
    U_end <= U_start-D_U+2Q.

Hence, with a=kappa_p/C_res (decrease kappa_p if necessary to ensure 0<a<1),

    U_end <= (1-a)U_start + A Q+B M,
    A=2+d/C_res,  B=1/C_res.                         (1)

A control-only loss of availability is not a data fault and is charged to M. In ideal Poisson evaluation M is bounded by no-ring hubs; in the transactional implementation it is bounded by the already proved actual good-service miss majorant, provided the controller implements THIS larger decision footprint.

## B. Unconditional finite work: D0
On any component of the incoming error plus all actual event supports, accepted moves number at most U_in+2Q<=2|E_in|+2Q. Therefore the execution support has size at most

    (1+2w)(|E_in|+Q).

Append a sectorwise global minimum-syndrome representative R at the endpoint, only as a mathematical gauge choice. Check-support cliques imply same-syndrome equality component by component in the enlarged execution support. Minimality gives |R intersect K|<=|E_actual,out intersect K| in each enlarged component K. Thus

    |K| <= C_seed (|E_in intersect K|+Q(K)),
    C_seed=2(1+2w).                                  (D0)

This holds without a small-component assumption. If |K|<ell and ell is below distance, the same-syndrome difference on K is a stabilizer. Choose ell=c_cut N strictly below both CSS distances and both GPT correction radii.

## C. Exact localization and suffix footprint
For an actual serial event list ending at L define the future support

    U_i = supp(E_i) union union_{events k>=i}supp(F_k)
        = supp(E_L) union union_{events k>=i}supp(F_k).

Here U_i denotes a SET, not the potential U( ). The equality is elementary XOR bookkeeping; the sets are nested. For a target S in the final reduced representative, take W_i to be all G-components of U_i meeting S. Every event support is a clique, and full-read cliques guarantee that its restricted local decision equals the original decision. Active candidates for a restricted component must touch its current error support, as established above. If actually executed, their support belongs to U_i and hence to the same component. Apply (1) separately and add across components; total error weight need not be small, only each relevant component.

When the actual endpoint is not reduced, use the SAME-SYNDROME virtual start R XOR all event masks and the same event list. Its syndrome trajectory and local decisions are unchanged, and its support lies in enlarged execution support. This is branchwise relabeling, not an inserted physical correction.

For the restricted suffix let x_i=U(E_i intersect W_i), y_i=U(E_L intersect W_i), and Q_i its bad support mass. Since final subsets are reduced, y_i>=h|E_L intersect W_i|. Integer accepted decrease D_i satisfies D_i<=x_i-y_i+2Q_i. Thus with C0=max(w,1/h),

    |W_i| <= |E_L intersect W_i|+w D_i+Q_i
          <= C0 x_i+(2C0+1)Q_i.                     (2)

Energy additivity across disconnected components follows because every energy view is a clique. It is NOT an unsupported assertion that U is monotone under deleting arbitrary qubits.

## D. R-window dichotomy: D1
For nested boundary sets W_j, restricted (1) and component additivity give

    x_{j+1} <= (1-a)x_j+A Q_j(W_j)+B M_j(W_j).

Put L0=max(A,B), theta=1-a/2, K0=2L0/a, and Z_j=Q_suffix(W_j)+M_j(W_j). If some x_j<=K0 Z_j, (2) supplies a fresh witness containing S, each component meeting S, with

    |W_j| <= C_bad[Q_suffix(W_j)+M_j(W_j)],
    C_bad=C0 K0+2C0+1.                              (F)

Otherwise contraction by theta holds in every window. At the endpoint x_R>=h|S|, while x_0<=2|W_0|. Therefore

    |W_0| >= c_R|S|,   c_R=(h/2)theta^(-R).          (A1)

For seed density enlarge W_0 to the components of the ORIGINAL full execution support union R which meet S. The enlargement still has every component meeting S, preserves (A1), and D0 gives

    |W| <= C_seed[|E_in intersect W|+Q_block(W)].      (A2)

This is exactly the reviewed D0/D1 contract of SPACETIME_CPTP_MEMORY.md, with changed constants and linear ell. Choose fixed R so c_R/(2C_seed)>1. The one-chain terminal-volume argument is unchanged.

## E. Consequence and exact remaining scope
Conditional on the general-density theorem, the ideal Poisson arbitrary-local-CPTP-kick theorem gives

    ||Dec E_t Enc-id||_diamond <= C N(1+t) exp(-c N)

for a sufficiently small fixed kick rate, fixed sufficiently large evaluation-window duration, bounded-range bounded-incidence supports, exact initial code state tensor fixed bath, and ideal mathematical readout. Constants depend badly on fixed Delta but not N. Pauli expansion is only a linear instrument expansion: one good positive primitive record protects EVERY branch, and there is no classical-error-distribution assumption.

The reviewed transactional positive-record proof can use exactly this D0/D1 interface ONLY after its finite local controller is instantiated to compute GPT energy and reserve the full enlarged dependency footprint. Its good-service/mark constants and dressed fault-support cliques must be recomputed for that fixed circuit. Fixed Delta makes all dimensions/supports finite and N-independent; it does not make this substitution physically free. The accepted FGL controller instance by itself is not already a GPT controller implementation.

A native finite-rate theorem with this local circuit and onsite Markov cushion is consequently a compiler-instantiation task, not a new backward-witness problem. Continuous coherent Hamiltonian noise is instead covered, conditionally on density, by UNARY_ENERGY_LIFT.md's ideal atomic killed-basin route; the Poisson proof does not manufacture a coherent-noise reduction.
