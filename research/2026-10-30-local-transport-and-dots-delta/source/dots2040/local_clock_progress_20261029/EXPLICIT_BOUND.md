# Explicit local progress without a mixing or spectral-gap assumption

For the independent-set clock on a finite graph of maximum degree D, with H=g sum_x (b_x+b_x^*) and jumps sqrt(kappa)b_x, every initial density matrix obeys a size-independent positive lower bound for an emission at any fixed x by every t>0. Here g,kappa>0. The proof uses only local differential identities and positivity.

Write n_x=b_x^*b_x, G=product_{y adjacent x}(1-n_y), and f(s)=Tr(rho_s n_x). Let

    C = 4g^2+kappa^2+4g^2 D+4 kappa g(D+1)+2 kappa g.

Then

    |f''(s)-2g^2 Tr(rho_s G)| <= C sqrt(f(s)).                 (1)

Indeed L^*(n_x)=ig(b_x-b_x^*)-kappa n_x. The H_x contribution to L^{*2}(n_x) is 2g^2(G-2n_x). All H_z contributions with z other than x are off-diagonal in the x occupation, and only adjacent z can contribute. Their total norm is at most 2g^2 D. The dissipative action on ig(b_x-b_x^*) is also off-diagonal and only closed-star sites can contribute, with norm at most 2kappa g(D+1). The remaining off-diagonal term has norm kappa g; the remaining diagonal term is kappa^2 n_x. For an off-diagonal self-adjoint A, |Tr(rho A)|<=2||A||sqrt(Tr(rho n_x)); also f<=sqrt(f). These give (1).

Let Pi_m project onto exactly m occupied neighbors of x, and P_k=sum_{m<=k}Pi_m. For k>=degree(x), P_k=I. The exact dissipative identity is

    D^*(P_k)=kappa(k+1)Pi_{k+1}.                              (2)

Only the Hamiltonian summands centered at neighbors of x fail to commute with P_k. Their sum has norm at most gD. Thus, with p_k(s)=Tr(rho_s P_k),

    p_k'=i Tr(rho_s[H,P_k])+kappa(k+1)Tr(rho_s Pi_{k+1}),
    |i Tr(rho_s[H,P_k])|<=2gD sqrt(p_k).                     (3)

Set delta=t/[4(D+1)] and I_j=[j delta,t-j delta], j=0,...,D+1. Choose a nonnegative C^2 cutoff phi_j supported on I_j and equal to one on I_{j+1}, using quintic smoothstep ramps of width delta. These satisfy ||phi_j'||<=2/delta and ||phi_j''||<=6/delta^2.

Let u=(1/t)integral_{I_0}f, and b_k=(1/t)integral_{I_{k+1}}p_k. Twice integrate (1) against phi_0 and apply Cauchy-Schwarz:

    b_0 <= A sqrt(u),
    A = 3/(g^2 delta^2)+C/(2g^2).

Integrate (3) against phi_k, noting p_k=p_{k-1}+Tr(rho Pi_k). Since all normalized integrals are <=1,

    b_k <= C_k sqrt(b_{k-1}), k=1,...,D,
    C_k = 1+2/(kappa k delta)+2gD/(kappa k).

Here the appropriate cutoff for k is phi_k: it is supported on the interval defining b_{k-1} and equals one on the interval defining b_k. Define

    K=A^(2^(-D)) product_{k=1}^D C_k^(2^(-(D-k))).

Because p_D=1 and |I_{D+1}|=t/2, the iteration gives

    1/2=b_D <= K u^(2^(-(D+1))),
    u >= (2K)^(-2^(D+1)).                                  (4)

Finally let N_x(t) count x emissions. Its stochastic intensity is kappa times the conditional occupation, hence is bounded by kappa. E N_x(t)=kappa t u. Conditional on the first emission time, the expected number of further emissions is at most kappa t. Therefore

    P[N_x(t)>=1] >= E N_x(t)/(1+kappa t)
                 >= [kappa t/(1+kappa t)](2K)^(-2^(D+1)) >0.

The constants are intentionally very crude. No stationary state, rapid mixing, spectral gap, uniform global norm bound, or independent-renewal assumption was used. Arbitrary initial mixed states, including ones entangled across the full graph, are covered. This is a single-site progress theorem, not a spatially joint fault law.

## Qualitative no-dark alternative

If f vanishes throughout a nonempty time interval, (1) forces p_0=Tr(rho G)=0 throughout. If p_k=0, positivity kills its Hamiltonian commutator expectation, and (2) forces Pi_{k+1} expectation zero, hence p_{k+1}=0. After at most D steps this says Tr(rho)=0, a contradiction. All identities are local, so the same argument extends to locally well-defined infinite-graph dynamics.

## Detailed locality and algebra checks

All calculations above are on the invariant independent-set Hilbert space. For locality reasoning one may embed into qubits and represent b_z as sigma_z^- product_{w adjacent z}(1-n_w), then restrict back. On that subspace b_z^*b_z=n_z, b_z b_z^*=G_z-n_z, and ||b_z+b_z^*||=||i(b_z-b_z^*)||<=1. Although the full-qubit guarded jump number is n_z G_z rather than n_z, this distinction disappears after restriction; the proof does not assume n_z<=G_z outside the independent-set sector.

For z neither x nor adjacent to x, b_z and b_z^* commute with b_x and b_x^*. Their guards may share qubits, but shared guards are diagonal; neither flip site is in the other guard. Hence their Hamiltonian commutators and dissipators on i g(b_x-b_x^*) vanish exactly. For every z != x, both b_z and its adjoint commute with n_x, so its commutator and dissipator preserve the off-diagonal x-blocks. The x dissipator also preserves off-diagonal x-blocks: b_x^* A b_x=0 for such A, and its anticommutator with n_x remains off-diagonal. Thus the precise decomposition is

    L^{*2}(n_x)=2g^2 G+(kappa^2-4g^2)n_x+B,
    Q B Q=n_x B n_x=0, Q=I-n_x,
    ||B|| <= 2g^2 D+2kappa g(D+1)+kappa g.

The first term in the norm bound sums ||i[h_z,A]||<=2g||A||=2g^2 over at most D neighbors, where A=ig(b_x-b_x^*). The second uses ||D_z^*(A)||<=2kappa||A|| at D+1 sites. The last is the -kappa A contribution. For a density matrix, Cauchy-Schwarz on its positive sesquilinear form yields |Tr(rho B)|<=2||B||sqrt(f(1-f)); the stated C follows.

For (2), jumps outside the neighbor set commute with P_k. On a neighbor configuration of occupancy count m, the sum of gain terms b_y^*P_k b_y contributes m if m-1<=k, while the sum of anticommutator terms contributes m if m<=k. Their difference is exactly (k+1)Pi_{k+1}. Every operator here is diagonal after the indicated gain-loss combination, so this is an operator identity, not merely a classical-state argument.

For (3), set H_N=sum_{y adjacent x}h_y. All remaining h_z commute with P_k, since only a flip centered in the neighbor set can change its occupation count. For any projection P and Hermitian K, |Tr(rho[K,P])|<=2||K||sqrt(Tr(rho P)); apply ||H_N||<=gD.

The quintic ramp is q(v)=10v^3-15v^4+6v^5 on [0,1]. It has q(0)=0, q(1)=1 and first and second derivatives zero at both endpoints, with |q'|<=15/8<2 and |q''|<=10sqrt(3)/3<6. Set phi_j=q((s-j delta)/delta) on the left ramp, one centrally, and the reflected ramp on the right. Integration by parts has no endpoint terms.

For completeness, the initial integrated inequality before simplification is

    2g^2 t b_0 <= (6/delta^2)t u + C t sqrt(u).

For recursion step k=1,...,D use equation (3) with index k-1 and cutoff phi_k. Since phi_k=1 on I_{k+1},

    integral_{I_{k+1}} Tr(rho Pi_k)
      <= [2/(kappa k delta)] integral_{I_k}p_{k-1}
        + [2gD/(kappa k)] sqrt(t integral_{I_k}p_{k-1}).

Adding the P_{k-1} contribution on I_{k+1}, dividing by t, and using b_{k-1}<=sqrt(b_{k-1}) gives the stated recursion. The terminal interval length is t-2(D+1)delta=t/2 exactly.
