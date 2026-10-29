# Extension to arbitrary physical data/auxiliary states

The local progress and extensive no-emission theorems extend beyond the legal independent-set clock code to the full guarded-Kraus implementation, including illegal simultaneous occupancies, arbitrary excited labels, and arbitrary entanglement with data/reference systems.

At box x, let P_x be ready-auxiliary projector, Q_x=I-P_x, V_x=sum_s K_xs tensor |s><0| with V_x^*V_x=P_x, and E_x=V_xV_x^*<=Q_x. Let G_x=product_{y~x}P_y and H_x=gG_x(V_x+V_x^*). Graph edges include every data-support overlap. Reset operators are sqrt(kappa) I_data tensor |0><s|_x.

## Dimension-free local identities

The summed jump intensity is kappa Q_x<=kappa I. H_x has norm g. The bundled reset adjoint at x is

 D_x^*(A)=kappa sum_s |s><0| A |0><s| - (kappa/2){Q_x,A}.

Its CP part has norm kappa since its value on I is kappa Q_x; the anticommutator part also has norm <=kappa. Thus ||D_x^*||<=2kappa independently of the number of excited labels or the data dimension.

For f=Tr(rho Q_x), the first derivative is an x-ready/excited off-diagonal coherence minus kappa f. The self-Hamiltonian curvature is

 2g^2 G_x(P_x-E_x)
 =2g^2G_x-2g^2G_x(Q_x+E_x).

Because E_x<=Q_x, the expectation of the diagonal residual is bounded by 4g^2 f. All other Hamiltonian curvature terms are x-off-diagonal, only adjacent centers contribute, and each has norm <=2g^2. Bundled dissipators preserve the x-off-diagonal sector; only the closed star contributes with the same norm estimates as for qubits. Therefore EXACTLY the previous safe bound remains valid:

 |f''-2g^2 <G_x>| <= C sqrt(f),
 C=4g^2+kappa^2+4g^2D+4kappa g(D+1)+2kappa g.

For projectors Pi_m onto m occupied neighboring auxiliaries (occupation means Q_y, irrespective of internal label) and P_k=sum_{m<=k}Pi_m, bundled resets obey

 D^*(P_k)=kappa(k+1)Pi_{k+1}.

Only neighboring H terms change these counts, with total norm <=gD. Thus every cutoff inequality and the same explicit positive c(D,g,kappa,t) apply to the full physical Hilbert space. No code-space or dark-label assumption enters.

## Local polynomial and packing

Use K_x=L^*-J_x^*, where J_x^* is the bundled CP jump map, of norm kappa. The same nested-term count works if a support-label set A denotes the union of data supports and auxiliaries belonging to boxes in A. A Hamiltonian term can intersect that physical support only if its center lies in A or a graph neighbor of A. There are at most (D+1)|A| such terms. Each term enlarges A by at most D vertices; graph-radius grows by at most two. Reset terms have the dimension-free norm above. Thus the same C0=4(g+kappa)(D+2)^2 and finite-support polynomial F_x^(m) work.

One extra graph-distance unit is prudent for the product construction: supports of different labeled balls can share data when their label sets are adjacent. Choose selected centers pairwise distance >4m+3, so the physical support of K_xF_x^(m), contained in labels B_{2m+2}(x), is disjoint from the physical support of every other F_z^(m), contained in B_{2m}(z). Replace the packing bound by

 B=(D+1)^(4m+4).

Everything else in EXTENSIVE_NO_EMISSION_THEOREM.md is unchanged. In particular, with C=3delta/a and gamma=c/(3delta B),

 sup_rho P_rho[no completed resets at any x in S during t]
 <= C^|S| exp(-gamma |S|t),

for arbitrary physical initial data/auxiliary states. Chronological-slab composition yields the genuine joint clock-stall law.

## Essential limitation

Progress despite arbitrary occupancy/internal-label defects does NOT prove that the resulting reset acts as the intended data channel, that defects are repaired, or that physical errors have bounded spread. Exact completed-channel semantics still requires the clean invariant code. This extension supplies only a robust progress observable and a full-Hilbert-space Lyapunov inequality useful for subsequent perturbation analysis.
