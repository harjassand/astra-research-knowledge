# Exact microscopic leakage-energy audit

2026-11-01. Audit of ROOT_MICROSCOPIC_LEAKAGE_ENERGY.md (specified SHA cec20c64ab1318ee8297061f4309886ba907e8031f697ed1c96d85d6cf19b392). **PASS, conditional on the explicitly stated native Hamiltonian/jumps.** This is an occupation-energy admission, not a cache-refresh, initialization, or memory theorem.

## Model and explicit constants

Use m apparatus cells (replace m by c_app n when reporting per-data-size constants). Each cell has two disjoint length-w chains, w>=2, with low states g_c,e_c and intermediate states v_cj. N is the sum of intermediate projectors. All edges carry arbitrary norm-one unitary data factors; they need not commute across cells. Boundary and middle amplitudes have absolute value <=g=eta Delta. H_low is a sum of apparatus-local Hermitian operators supported on the low-state subspace, each with norm <=h0 eta^2 Delta. This includes finite diagonal Stark counterterms and reference edges. It does NOT include arbitrary uncontrolled data-dependent low terms.

Cleanup jumps are sqrt(delta)|g_c><v_cj|, endpoint jumps sqrt(kappa)|g_(1-c)><e_c|, tensored with data identity. Other noise and reservoir absorption are additional admitted perturbations, not part of this ideal estimate.

Let d_b be the largest number of boundary edges incident to one intermediate vertex (<=2; 2 for w=2, 1 otherwise), d_m the largest middle-edge degree (<=2). Each low vertex has at most one boundary edge. Set

    C0 = 4 d_b + h0,
    B = 2 d_b (delta+kappa)^2/delta + 2 kappa h0.

Require d_m eta + h0 eta^2 <=1/4. This is a sufficient finite condition, not an optimized constraint.

## Global energy sandwich without commutation assumptions

For each boundary edge T=|v><l| tensor U, Young's operator inequality gives

    +/- eta(T+T†) <= t Q_v + eta^2/t Q_l.

Taking t=1/(4 d_b), summing all edges and using the orthogonality of low levels WITHIN each cell yields

    +/- H_boundary/Delta <= N/4 + 4 d_b eta^2 m I.

For each middle edge, +/- eta(T+T†)<=eta(Q_v+Q_u), hence

    +/- H_middle/Delta <= d_m eta N.

Consequently

    N/2 - C0 eta^2 m I <= H/Delta <= 3N/2 + C0 eta^2 m I.

Define E=H/Delta+C0 eta^2 m I. Then E>=N/2>=0, E<=3N/2+2C0 eta^2 m I, and [H,E]=0 exactly. These are full-network operator inequalities. Overlapping data supports introduce NO degree factor in this step.

## Exact dissipator action and coherences

Each cleanup/endpoint dissipator acts only on its own apparatus. It annihilates every other cell's Hamiltonian term, even if that other term uses shared data qubits. Thus it is legitimate to sum single-cell identities globally, with no commuting-Hamiltonian assumption.

* On Delta N: action is -delta Delta N.
* On a middle edge: action is -delta times that edge.
* On a g-v boundary edge: action is -delta/2 times that edge.
* On a v-e boundary edge: action is -(delta+kappa)/2 times that edge.
* Cleanup on H_low: the anticommutator vanishes by low/intermediate orthogonality. Recycling injects its g_c diagonal value at v_cj, bounded above by delta h0 eta^2 Delta N.
* Endpoint decay on H_low: recycling has norm <=kappa h0 eta^2 Delta and the anticommutator has norm <=kappa h0 eta^2 Delta PER CELL. This includes the finite ground Stark energy injection and reference-edge damping; it is not set to zero.

For boundary damping alpha<= (delta+kappa)/2 apply Young's inequality with t=delta/(8d_b):

    +/- sum alpha eta(T+T†)
       <= delta N/8 + 2 d_b (delta+kappa)^2/delta eta^2 m I.

It follows that

    L*E <= [-delta + delta/8 + delta d_m eta + delta h0 eta^2] N
             + B eta^2 m I
         <= -delta N/2 + B eta^2 m I.                 (1)

In particular the root's weaker -delta N/4 bound is valid. Using the upper energy sandwich,

    L*E <= -(delta/3) E
              + [B + (2delta/3) C0] eta^2 m I.        (2)

For delta and kappa comparable to J, this has precisely the proposed -c J E+C J eta^2 m form. Arbitrary boundary/intermediate coherences are already included by the operator Young inequalities; no stationary distribution, adiabatic elimination, or epsilon-times-runtime estimate occurs.

## Cleanup disturbance payment and its exact condition

In the controlled-prefix frame, conjugate the ENTIRE generator and E by the same fixed unitary. Equations (1)-(2) persist. To assert L_cleanup* W<=D_W delta N one additionally needs W to commute with each source projector and the conditional partial-Pauli update to obey U†WU-W<=D_W I on that source. These conditions hold for an apparatus-block-diagonal local syndrome/witness potential with a verified bounded local change. They do not follow for an arbitrary coherent W merely from a bounded jump norm.

With these conditions, coefficient A>2D_W multiplying E pays cleanup-induced W growth using (1). The remainder is A B eta^2 m. One should use the N-form (1) for this payment before converting the unused fraction to E-restoring drift.

## Scope and costs

The exact energy proof survives arbitrary bounded-degree overlap; degree enters the eventual D_W, locality of the dressed frame, and exponential-moment constants, not the energy estimate above. Apparatus dimension 2w+2 is fixed but not a qubit. Native two-body apparatus/data couplings, detuning, finite Stark tuning, and dissipators remain physical premises.

Optional apparatus dephasing is not silently included. Diagonal level dephasing adds explicit edge damping; the same boundary/middle estimates can charge it, but a rate much larger than J may worsen the floor/coefficient. Finite-temperature upward transitions and uncontrolled Hamiltonians likewise require their own action-on-E admission.

E contains O(1) energy for an initially occupied intermediate level. Small stationary leakage or small initial mean does not establish the required initial exponential leakage tail. No small-z bounded correction is claimed. The initial exponential-moment/low-energy preparation condition remains. Nor does (2) imply uniform cache refresh, useful conditional sensor reports, or the complete joint exponential Lyapunov theorem.

## Numerical sanity check

`leakage_audit/check_single_cell.py` evaluates the exact matrices at w=2,3,4,5, eta=.005,.02,.05, Delta=1, delta=kappa=eta^w, and nonzero opposite-sign endpoint Stark shifts plus reference edges. All energy-sandwich and drift matrix margins are nonnegative. The script checks the scalar-data sector only; the full noncommuting-network result rests on the operator proof above, not these numerics. Results are in `leakage_audit/single_cell_results.txt`.
