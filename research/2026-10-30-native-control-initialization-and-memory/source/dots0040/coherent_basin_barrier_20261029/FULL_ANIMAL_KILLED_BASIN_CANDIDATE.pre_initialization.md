# Tuned full-animal SSF drift and a killed-basin continuous-noise construction

2026-10-29. **New load-bearing proof candidate, not independently audited.** This manuscript does not alter the frozen Choi/Poissonization results. It attempts to close the ideal atomic SSF continuous-noise problem directly, including a retained common bath and without adding dephasing or depolarization. The physical transactional compiler is NOT covered by the argument below.

The substantial new point is a one-component completion charge proving weighted aggregate progress from FGL componentwise progress. It is not an assumption of an instantaneous weighted Lyapunov inequality.

## 0. Exact imported SSF hypotheses and geometry

Work first in one CSS sector. For every globally minimum-weight syndrome representative E, each subset is stabilizer-reduced. For every reduced error C of size <ell, assume the accepted FGL small-error estimates:

    |sigma(C)| >= h |C|,
    number of distinct active hubs for C >= kappa |sigma(C)|.       (H)

Here h,kappa>0 are N-independent. The second estimate follows from the packed-candidate consequence already used in the asynchronous witness proof: bounded candidate syndrome size and conflict degree turn Proposition 14's candidate mass into distinct active hubs. A hub chooses some accepted correction whenever any accepted candidate exists. Every accepted move changes a set D of k<=k0 syndrome bits and decreases syndrome count by d>=beta k>0. Hubs ring at rate lambda (or uniformly bounded below rates). All footprint sizes/degrees are bounded.

Let G0 be the fixed DATA graph containing full hub read-footprint cliques, check-support cliques, and declared primitive support cliques. A full read footprint includes every data qubit needed to evaluate the checks used by the hub.

For each data site x let J_x contain a dummy vertex x and all syndrome-check vertices that either touch x or can be changed by a correction at a hub whose full read footprint contains x. These are bounded sets. There is a constant r such that two J_x share a check only if dist_G0(x,y)<=r: a common changed check is read by both corresponding hubs and its data support lies in their full read footprints. Set G=G0^r, enlarging r if necessary. All degrees remain bounded.

Use a mixed animal graph H whose vertices are DATA dummy vertices (always unoccupied) and syndrome-check vertices. Include G edges between dummy vertices, edges from x to each check in J_x, and a clique on every possible changed-check set D. H has bounded degree and O(N) vertices.

For a connected component C of E in G define

    J(C) = union_{x in C} J_x.

Then:

1. J(C) is connected in H and |J(C)|<=D0 |C|.
2. Different E-components have DISJOINT J(C). Otherwise their error sites are adjacent in G by construction.
3. sigma(C) lies in J(C), and syndromes of distinct components are disjoint.
4. Every active hub is associated to exactly one E-component: its read footprint contains an erroneous site, and it cannot contain errors from two components. Its actual chosen changed-check set D_h is contained in J(C).
5. Every check belongs to D_h for at most nu distinct hubs (a fixed incidence constant).

The dummy vertices avoid silently assuming that projecting a connected data support onto checks preserves connectivity. They are merely combinatorial vertices, not added physical systems. Their occupancy is identically zero.

For E with every G-component <ell, (H) applies to each C. Let sigma_C=sigma(C), g_C be the number of actual active hubs associated with C, and D_h their actual selected moves. Then

    g_C >= kappa |sigma_C|,
    |J(C)| <= (D0/h)|sigma_C|.                       (0.1)

This is the only use of expansion in the aggregate proof.

## 1. Tuned FULL animal observable

Choose u in (0,1), c=1-u, theta in (0,1), L=log(1/theta), a=cL. For every NONEMPTY connected A in H, with no size truncation, define

    f_A(sigma) = exp(a|A|) theta^{|A|-|A intersect sigma|}
               = theta^{u|A|-|A intersect sigma|},
    V = sum_A f_A,      W = sum_A |A| f_A.

These are positive syndrome-diagonal observables. At finite N the sums are finite. If at most A0^m animals of size m occur per root and A0 theta^u<1, V(vacuum)<=C N. Dummy vertices contribute to |A| but never to occupied count.

### 1a. Exact per-move charging

An accepted move removes m_- occupied bits and adds m_+ previously empty bits, k=m_-+m_+, d=m_--m_+>=beta k. For an increasing animal A write r=|A intersect removed| and t=|A intersect added|; then t>r. Its completion B=A union D is connected because D is a clique and A meets D. Direct algebra gives

    f_B(pre)/f_A(post)
      = exp[a(k-r-t)] theta^{m_+-r}
      >= exp(a m_-) theta^{m_+} =: R_move.           (1.1)

The inequality uses a<L: the minimum is at t=m_+,r=0. Every B has at most 2^k preimages A. Every B containing D is DECREASING, with decrement (1-theta^d)f_B(pre), so these targets are never increasing source animals.

If

    R_move >= 2^(k+1)/(1-theta),                     (1.2)

the positive increments consume at most half the available D-containing decrement. Therefore

    Delta_move V <= -(1-theta)/2 sum_{B connected: D subset B} f_B. (1.3)

To arrange this for every move, define zeta=[c(1+beta)-(1-beta)]/2. Choose c>(1-beta)/(1+beta), so zeta>0; then R_move>=theta^(-zeta k). Taking theta sufficiently small establishes (1.2) uniformly. This uses FULL animals: a truncation would discard B=A union D and invalidate the charge.

## 2. Actual weighted aggregate coverage in the small-component basin

Fix a syndrome whose minimum representative E has G-components <ell. Define

    S(sigma)=sum_B n(B) f_B,
    n(B)=number of active hubs h with D_h subset B.

Summing (1.3) gives L_SSF*V<=-lambda(1-theta)S/2. We now bound W by S plus a vacuum-sized term, rather than assuming local candidate coverage.

For animal A set k_A=|A intersect sigma|. For each E-component C let

    q_C(A)=number of active hubs associated C with D_h intersect A nonempty,
    q(A)=sum_C q_C(A).

### 2a. Directly covered animals

Call A covered if q(A)>=kappa k_A/4. Then

    sum_covered k_A f_A <= (4/kappa) sum_h sum_{A:D_h meets A} f_A.

For fixed h complete A to B=A union D_h. Connectivity follows from the D_h clique, and

    f_B/f_A >= theta^(u k0).

There are at most 2^k0 preimages for fixed h,B. Therefore

    sum_covered k_A f_A
      <= (4/kappa) 2^k0 theta^(-u k0) S.             (2.1)

### 2b. Uncovered animals: complete ONE poor component

For uncovered A call C poor if

    q_C(A) < (kappa/2)|A intersect sigma_C|.

The nonpoor components carry less than half k_A, otherwise q(A)>=kappa k_A/4. Hence

    k_A <= 2 sum_{C poor for A}|A intersect sigma_C|. (2.2)

For a poor C, at least kappa |sigma_C|/2 active hubs have D_h disjoint from A, using (0.1). Each of these moves removes at least one occupied check outside A, and each check is in at most nu such D_h. Consequently

    |sigma_C outside A| >= kappa |sigma_C|/(2nu)
                        >= rho |J(C)|,
    rho := kappa h/(2nu D0).                         (2.3)

Complete only this C:

    B=A union J(C).

It is connected: poor implies |A intersect sigma_C|>0, and J(C) is connected. The added occupied checks include sigma_C outside A. Therefore

    f_B/f_A >= theta^(-(rho-u)|J(C)|).               (2.4)

Choose u<rho/2 and theta so theta^(-(rho-u))>=2. For fixed C,B the preimage A differs only inside J(C), so there are at most 2^|J(C)| choices. Also |A intersect sigma_C|<=|sigma_C|. Thus

    sum_{A poor for C: A union J(C)=B} |A intersect sigma_C| f_A
       <= |sigma_C| f_B <= (g_C/kappa) f_B.           (2.5)

This is the essential entropy cancellation. It completes ONE component per charge, not all poor components at once; simultaneous completion would create unnecessary product entropy.

For fixed B, summing g_C over C with J(C) subset B counts distinct active hubs whose D_h are contained in B, so it is at most n(B). Combining (2.2)-(2.5),

    sum_uncovered k_A f_A <= (2/kappa) S.             (2.6)

Consequently

    sum_A k_A f_A <= C_cov S,
    C_cov=(4/kappa)2^k0 theta^(-u k0)+2/kappa.        (2.7)

### 2c. Sparse animals cost only O(N)

Put eta=u/2. If k_A<eta|A| then f_A<=theta^((u-eta)|A|). Choose theta so A0 theta^(u/2)<1, obtaining

    sum_sparse |A| f_A <= C_sparse N.

For all remaining animals, |A|f_A<=eta^(-1) k_A f_A. Hence

    W <= (C_cov/eta) S + C_sparse N,
    L_SSF*V <= -gamma W + bN,
    gamma=lambda(1-theta)eta/(2C_cov),
    b=gamma C_sparse.                               (2.8)

This pointwise inequality is proved on EVERY syndrome whose minimum representative has small G-components. It is not asserted globally: trapped large components may violate it.

All parameter requirements are compatible: first choose u>0 smaller than rho/2 and the beta bound, then choose theta sufficiently small. Later also require u<h/(4D0) for the boundary lemma. Constants may be very small/large but are independent of N.

## 3. Local orbit oscillation absorbs arbitrary coherent/Lindblad data-bath noise

For a local primitive support Z let Omega_Z(V) be the maximum-minus-minimum V on each orbit of syndrome labels obtainable by Paulis on Z, times that orbit's identity. Such an orbit changes at most k_noise bounded check bits. It is invariant under arbitrary Z-supported data-bath operators. The exact Loewner inequalities are

    i[h_Z,V] <= 2||h_Z|| Omega_Z(V),
    D[K_Z]^*V <= 2||K_Z||^2 Omega_Z(V).

They follow by subtracting the orbitwise minimum and bounding the remaining positive operator by its orbitwise range. They remain valid with a common retained bath/reference.

Only terms f_A whose A contains an affected check have nonzero oscillation, and their orbitwise ratio is at most theta^(-k_noise). Bounded primitive incidence therefore gives

    sum_Z Omega_Z(V) <= C_osc W.                     (3.1)

Assume the combined joint norm budget per primitive support obeys

    2||h_Z(t)||+2sum_j||K_Z,j(t)||^2 <=epsilon.

Then, ON the small-component basin,

    L(t)^*V <= -(gamma-epsilon C_osc)W+bN.            (3.2)

Bath-only dynamics commutes with V. No positivity of a Hamiltonian Dyson expansion or twirl is invoked. Choose epsilon C_osc<gamma/2.

## 4. Actual high-V boundary lemma

Let source E be a minimum representative with every G-component <ell. Let P_Z be any data Pauli supported on a declared bounded support Z, |Z|<=s, and let F be a minimum representative of sigma(E)+sigma(P_Z). Include Z as a clique in G. For any component K of E union Z union F, the syndromes agree componentwise; otherwise a check touching two union components would connect them in G.

Replacing F inside K by (E xor P_Z) inside K preserves syndrome. Minimum weight therefore gives

    |F intersect K| <= |(E xor P_Z) intersect K|,
    |K| <= 2(|E intersect K|+s).                     (4.1)

Every source E-component meeting K is wholly in K, and these components have disjoint syndromes and obey confinement. Thus the actual source syndrome has at least

    h |E intersect K| >= h(|K|/2-s)

occupied checks in J(K)=union_{x in K}J_x. This set is connected in H, has size <=D0|K|, and includes those occupied checks. Therefore

    V(source)>=f_{J(K)}
       >= exp{L[(h/2-uD0)|K|-hs]}.                  (4.2)

Choose u<=h/(4D0). For |K|>=ell>=8s,

    V(source) >= exp(L h ell/8) =: M_edge.           (4.3)

If every K has size <ell<distance, then E xor P_Z xor F is a product of stabilizers componentwise. Thus the canonical logical action of that edge is identity (up to syndrome-dependent scalar phase).

Consequently every bounded local Pauli edge sourced at a component-safe syndrome with V<M_edge has identity canonical logical action, and its target minimum representative still has only small components. This is not a claim that arbitrary distant large-representative/low-syndrome states have large V; the assertion is an edge barrier FROM the safe basin.

Use s large enough to include the full support of any clean atomic Kraus operator (read projector times correction), noise operator, and its local products K†K. The support dimension and incidence stay bounded.

## 5. Killed low-V safe basin: candidate quantum closure

Let M=M_edge/2 and let P be the syndrome-diagonal projector onto states whose minimum representatives have components <ell and V<M. For CSS codes impose this in both sectors and use V=V_X+V_Z, W=W_X+W_Z, with common worst-case constants. At sufficiently large N, the encoded vacuum has V=O(N)<M.

Compress the FULL noisy generator to the P-space:

    L^P_t(rho)=P L_t(P rho P) P.

This is a CP trace-nonincreasing generator. Explicitly H is replaced by PHP; each jump gain uses PKP, while the loss retains P K†K P, including the positive loss for jumps exiting P. P is only an analytical projection, not a physical measurement or recovery.

Because [P,V]=0, Hamiltonian compression preserves the V commutator. Deleting outgoing jump gains subtracts a positive contribution to the adjoint V drift. Thus (3.2) implies for the killed positive state

    d Tr(V rho_P)/dt <= -(gamma/2)Tr(V rho_P)+bN Tr(rho_P),
    Tr(V rho_P(t)) <= C_V N.                        (5.1)

The local edge barrier ensures exits cannot arise from a source component-safe state below M_edge by creating a large target component. Exits from P therefore require target V>=M. A local Pauli changes V by a factor at most theta^(-k_noise), so an exit source has

    V(source)>=theta^(k_max) M.

The same conclusion applies to source blocks of QHP, QKP, and QK†KP, by Pauli expansion on their bounded supports. Let B be the union of all such source syndrome blocks. Then

    B <= V/[theta^(k_max)M],
    Tr(B rho_P(t)) <= C_B N/M.                      (5.2)

All compressed local data-bath operators have identity logical action in the canonical syndrome gauge by (4.3). This includes the loss P K†K P and Hamiltonian PHP, not only observed jumps. Therefore the killed encoded-to-decoded CP map has exactly the form a_t id_L, with input-independent a_t in [0,1], after discarding bath/syndrome.

### Full versus killed comparison

Embed rho_P in the full Hilbert space. Variation of constants gives

    rho_full(t)-rho_P(t)
      = integral_0^t E_full(t,s)[L_s-L_s^P]rho_P(s) ds.

For positive rho_P with boundary mass p, cross-block Cauchy-Schwarz gives O(||h|| sqrt(p)) for a Hamiltonian term, and O(||K||² sqrt(p)) for a dissipator: outgoing gain mass is <=||K||² p, its cross blocks are <=||K||² sqrt(p), and cross loss blocks are treated with K†K. Clean atomic instruments have bounded Kraus counts/supports and contribute O(N) total norm. All these estimates hold with a reference and common bath.

With total local data-acting norm budget Gamma_N<=C N, (5.2) therefore yields

    ||E_full(t)Enc - E_killed(t)Enc||_diamond
       <= C' N t sqrt(N/M).                        (5.3)

Trace preservation of the full channel gives 1-a_t bounded by the same error. Applying the fixed canonical decoder and adding this normalization difference yields the proposed ideal-atomic bound

    ||Dec E_full(t)Enc-id_L||_diamond
       <= min{2, C'' N^(3/2) t exp[-L h ell/16]}.    (5.4)

No added stabilizer dephasing or depolarization is required by this candidate. Constants depend on local geometry, FGL constants and the noise bound, not N. For ell proportional to sqrt(N), this is an exponential-in-sqrt(N) candidate lifetime against sustained arbitrary bounded local Hamiltonian/Lindblad noise with a retained common bath.

## 6. Audit-critical points, not to be skipped

A. Verify the full-read geometry truly makes the J(C) containers disjoint after a fixed graph power; do not replace full read footprints by only correction masks.
B. Verify the imported packed-candidate mass (H) componentwise for minimum representatives using the enlarged graph, and for both CSS sectors.
C. Check the one-component completion entropy calculation (2.5), especially that one sums g_C only over containers contained in B and never performs simultaneous closure.
D. Verify the chosen canonical recovery and minimum-weight component replacement in (4.1), with the same syndrome graph and declared primitive support cliques.
E. Verify killed-generator factorization and Duhamel estimates in (5) at completely bounded/reference level; the comparison is to a trace-decreasing process, not a normalized conditioned state.
F. The physical transactional controller is not atomic SSF: its clock position can be coherent and its instantaneous drift need not obey (2.8). This manuscript grants no physical-controller corollary.

These are the specific load-bearing review obligations. The elementary Choi-assisted Markov theorem remains a separate reviewed route; this manuscript is a new candidate for the stronger no-added-noise/common-bath ideal model.

## 7. Support bookkeeping and efficient terminal SSF decoding

The boundary parameter s is the maximum DATA support size of an actual operator, not merely the size of a chosen correction mask. For nominal atomic Kraus K_h,a=F_h,a Pi_h,a it includes the full support of the syndrome-read projector and the correction. A bounded number of bounded-weight read checks gives bounded s. K_h,a†K_h,a is supported on that same patch. Each unknown h_Z,K_Z,j and K_Z,j†K_Z,j uses its declared patch Z, so products here do not double the support. Bath support is unrestricted; only joint norms are bounded. Define k_max as the maximum number of stabilizer-check bits changed by any data Pauli on any such patch, including nominal patches. Both s,k_max are N-independent. Include these declared patches as cliques in G0.

For the geometric construction one may take r=2: if a check lies in both J_x and J_y, a qubit of that check belongs to both relevant full read footprints, giving a G0 path of length at most two from x to y. The direct-incident cases are shorter. Thus G=G0^2 makes distinct error-component containers disjoint. This uses the FULL read footprint assumption explicitly.

The final minimum-syndrome decoder can be replaced, on the killed basin, by the fixed noiseless SSF readout algorithm already described in the existing notes. Each nominal correction is a bounded-support Pauli; below M the boundary lemma prevents a component-safe exit. Full V does not increase under any accepted move by (1.3), so V remains <M. Every accepted move strictly decreases the integer syndrome count. A no-change scan with nonzero syndrome contradicts componentwise active-hub progress. Consequently the ideal terminal SSF computation reaches zero syndrome in O(N) accepted moves / O(N^2) naive classical work and implements identity logical action throughout. This is an ideal mathematical readout statement, not fault-tolerant physical extraction during continued noisy operation.
