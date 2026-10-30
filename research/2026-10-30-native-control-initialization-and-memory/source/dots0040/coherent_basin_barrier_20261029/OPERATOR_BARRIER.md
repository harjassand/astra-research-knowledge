# Continuous coherent noise via an operator barrier, not positive records

2026-10-29. New conditional mechanism; NOT a proof for the SSF compiler. The precise unresolved task is a cluster-Lyapunov inequality for SSF. Everything below separates this from the algebraic coherent-noise lift.

## 1. A useful exact reduction: logical currents only near a barrier

Let D be a fixed CPTP decoder. Work on data plus any retained common bath, with an initially encoded logical state independent of the bath; references are arbitrary. Let B be a syndrome-diagonal bad-boundary projector and P=I-B. Suppose the physical generator L(t) satisfies

    (D tensor id_R) L(t)(P X P) = 0                    (LC)

for every operator X on data/bath/reference, after discarding the bath. This says that the generator has no decoded logical current on the interior. It is NOT the claim that the physical state is stationary there. A sufficient coefficientwise condition is: every local Hamiltonian, jump, and ideal correction Kraus operator intertwines the same canonical logical subsystem on every transition sourced in P, including its destination. Merely saying the source and destination are individually correctable is insufficient: the common recovery must give the same logical action on the edge.

Let the sum of diamond norms of the data-acting generator terms be Gamma_N <= C N (bath-only terms drop out). For any state rho, including a reference, p=Tr(B rho), block decomposition and Cauchy-Schwarz give

    ||rho-P rho P||_1 <= p+2 sqrt(p(1-p)) <= p+2 sqrt(p).

By (LC), ||D L(rho)||_1 <= Gamma_N [p+2 sqrt(p)]. Consequently, if p(t)<=p_* uniformly, then

    ||D E_t Enc-id||_diamond <= min(2, Gamma_N t [p_*+2 sqrt(p_*)]).  (1)

No physical barrier measurement, no trajectory stopping, no bath reset, no twirling, and no positive noise records occur. The square-root loss is genuine coherent boundary leakage. Equation (1) follows by integrating the decoded derivative on the *actual noisy state*, not comparing two unrelated processes.

A barrier observable V>=0 with V>=exp(a ell) B and uniform E[V]<=C_V N therefore gives p_*<=C_V N exp(-a ell) and an exp(a ell/2)/poly(N) lifetime. Logical dimension does not enter; high rate is compatible with this reduction.

## 2. Exact local-orbit oscillation lemma

Let V be diagonal in a commuting syndrome algebra. For a local data support Z, partition syndrome labels into orbits under all Pauli operators on Z. A Z-supported operator, even with arbitrary bath coefficients, preserves each orbit subspace. Define Omega_Z(V) on an orbit as (max V-min V) times its identity. Thus Omega commutes with every Z-supported operator and bounds the oscillation of V on that orbit.

For any Hermitian h_Z and arbitrary jump K_Z (both may act on a common bath),

    i[h_Z,V] <= 2 ||h_Z|| Omega_Z(V),
    D[K_Z]^*(V) <= 2 ||K_Z||^2 Omega_Z(V).             (2)

These are Loewner-order bounds. Proof: subtract the orbitwise minimum of V, obtaining 0<=W<=Omega; this subtraction commutes with h,K and is annihilated by their adjoint generators. On each orbit use ||[h,W]||<=2||h||||Omega|| and ||K†WK - {K†K,W}/2||<=2||K||²||Omega||. Blockwise tensoring proves the reference/bath-uniform version.

For a syndrome-diagonal V, an ideal syndrome-measurement/Pauli-feedback generator L0 has diagonal L0*V, so its inequality is a classical pointwise calculation. If there are W>=V>=0 and constants independent of N,ell such that

    L0* V <= -kappa W + b N I,                       (3)
    sum_Z Omega_Z(V) <= c W,                         (4)

and every support's combined budget 2||h_Z(t)||+2 sum_j||K_Zj(t)||² is <=epsilon, then arbitrary time-dependent continuous coherent and Lindblad noise satisfies

    L(t)*V <= -(kappa-epsilon c) W+b N I
            <= -(kappa-epsilon c)V+b N I.            (5)

For epsilon c<kappa, E[V(t)]<=max(E[V(0)],bN/(kappa-epsilon c)). Equations (1)-(5) are a rigorous conditional continuous-noise memory theorem. No slow time dependence or total-variation bound is imposed. The hypotheses concern a barrier observable, not uniqueness or global rapid mixing.

## 3. A concrete robust candidate: softened connected animals

For a bounded-degree occupancy graph, let x_v in {0,1} be syndrome-diagonal defect indicators. For all connected A with 1<=|A|<=ell define

    f_A(x)=exp(a|A|) theta^{|A|-sum_{v in A}x_v},  0<theta<1,
    V=sum_A f_A,   W=sum_A |A| f_A.

A fully occupied size-ell connected animal implies V>=exp(a ell). If at most A0^m animals of size m contain a given root and A0 exp(a)theta<1, V(empty)<=C N.

Suppose a primitive support changes at most k occupancy bits, with bounded incidence z. Its orbit oscillation satisfies

    Omega_Z(f_A) <= theta^{-k} f_A

pointwise when its affected bits intersect A, and is zero otherwise. Therefore

    sum_Z Omega_Z(V) <= z k theta^{-k} W.             (6)

Overcounting incidence only enlarges the constant. Thus the coherent-noise bound (4) is already automatic for this candidate, with no Pauli coefficient expansion and no exponential-in-N cost.

Why soften holes? The tempting V_hard=sum_components exp(a|component|) fails: adding a single bridge between two occupied components of size m changes O(exp(am)) into exp(a(2m+1)). Its local oscillation/V ratio diverges exponentially. This kills a direct local-perturbation absorption argument. Softened animals already charge the almost-connected precursor by theta, so the ratio is bounded.

The remaining nontrivial SSF question is precisely (3). Total syndrome weight decrease alone DOES NOT imply (3): a correction may move defects so as to merge clusters, and the weighted-animal potential can increase despite a reduction in defect count. Likewise a sparse-component contraction at a finite block endpoint does not imply an infinitesimal generator inequality. A corrected candidate may require an integrated semigroup potential or a bounded clock/controller augmentation; then (4) must be reproved rather than assumed.

A second gap is choosing local occupancy indicators that both dominate the actual logical-current boundary B and admit (3). Canonical minimum-error-representative occupancy is generally nonlocal under a local physical change, so the bounded-k premise of (6) cannot be asserted for it. Raw violated checks are local but their relation to the boundary needs a confinement theorem strong enough to find a connected dense syndrome witness.

## 4. Nonvacuity: exact drift for independent defect healing

For independent 1->0 resets at rate lambda, L0 f_A=-lambda(1-theta) k_A f_A with k_A=sum_A x. Fix eta in (0,1). Since k_A>=eta |A| except on sparse animals,

    L0 V <= -lambda(1-theta) eta W
            +lambda(1-theta) eta sum_{A:k_A<eta|A|}|A|f_A.

The latter sum is <=C N whenever A0 exp(a) theta^{1-eta}<1. Therefore (3) holds with kappa=lambda(1-theta)eta. This verifies a genuinely continuous-noise-stable rare-cluster phase for this model. It is not an autonomous quantum-code construction: the logical-current boundary condition still needs an appropriate correctable-subsystem realization.

## 5. Why the suggested literature does not close these gaps

- Cubitt et al., *Stability of local quantum dissipative systems*, arXiv:1303.4744: their abstract states stability of local observables/correlations under unique-fixed-point logarithmic mixing. That is not stability of an extensive degenerate encoded algebra. https://arxiv.org/abs/1303.4744
- Montaña-López et al., *Is rapid mixing stable?*, arXiv:2609.36016: the abstract explicitly gives weak local Hamiltonian perturbations destroying rapid mixing. Hence a gap/mixing assertion cannot replace (3)-(4). https://arxiv.org/pdf/2609.36016
- Yu and Wei, *Universal energy-space localization...*, arXiv:2510.14160v2: energy-space localization is a different Hamiltonian mechanism; do not import its time-dependent claims as a theorem for sustained bounded arbitrary Lindblad noise. https://arxiv.org/html/2510.14160v2

## 6. Exact deliverable status

PROVED here: local-orbit operator inequality; barrier-to-diamond logical-current reduction; softened-animal oscillation bound; independent-healing drift; a conditional theorem that covers coherent Hamiltonians and arbitrary local Lindblad jump/no-jump evolution without twirling.

NOT PROVED: SSF weighted-animal drift, syndrome boundary witness for the actual decoder, coefficientwise LC for the physical transactional compiler. These are explicitly stronger/different checks than the existing positive-record spacetime theorem. No general coherent SSF threshold is claimed.

### Source follow-through and verification

Read the energy-localization source beyond its abstract: Theorem 1 Eq.(12) bounds integral_0^T ||partial_t H||_X dt <= lambda n; its localization discussion requires total variation smaller than half the configuration barrier. Thus sustained bounded-amplitude fast variation is genuinely outside that theorem, not merely a difference in proof presentation.

Read Han et al., arXiv:2609.20537, actual Appendices B5-B6 and C3-C5. Its C4 resummation is potentially compatible with chronology: outside insertions are summed in original circuit order (Eq.139), and the remaining filter is a terminal CP syndrome subinstrument (Eqs.140-143). A spacetime extension must establish that the selected syndrome-record filter is independent of all resummed outside insertion choices. An arbitrary branch-dependent spacetime witness does not provide this. The B5 alternative uses commuting disconnected-component maps and therefore is not directly valid for data-disjoint operators sharing a bath. https://arxiv.org/html/2609.20537

`check_barrier.py` exhaustively verifies the independent-healing drift decomposition on all 64 states of a six-cycle, and tests the Hamiltonian and arbitrary-Lindblad Loewner inequalities for random two-site complex operators. `check_barrier.json` records positive minimum eigenvalues (20.3 and 197.1) and drift numerical error below 7e-17. This is a sanity check, not a substitute for the analytic proof.
