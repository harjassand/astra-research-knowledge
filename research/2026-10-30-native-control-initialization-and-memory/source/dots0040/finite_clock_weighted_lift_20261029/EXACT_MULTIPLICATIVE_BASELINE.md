# Exact positive multiplicative clock dressing for the independent pure-death fixture
2026-10-29. Solvable baseline, NOT an SSF/guarded-overlap theorem.

Each site has one data bit and an independent driven/damped qubit clock. Its completed-reset data channel sets the bit to zero. The dressed exact generator is H=g sum X_i with reset Kraus operators sqrt(kappa) sigma_i^- tensor K_is for that channel. All distinct-site terms have disjoint supports. This model has no logical protected information; it is a diagnostic of the finite-clock Lyapunov mechanism.

Let q=1-theta and use the positive isolated Poisson solution A from LINEAR_CREDIT_NOISE_FAILURE.md, with L_clock*A=kappa n-r I. For any 0<epsilon<=1 define
B=I+epsilon q A, bmax=||B||,
F_i=theta |0><0|_data tensor I_clock+|1><1|_data tensor B.
Thus theta I<=F_i<=bmax I, and all F_i at distinct sites commute.

## Exact local drift
In the data-zero block the drift is zero. In the data-one block,
L_i*F_i=L_clock*B+kappa a^*(theta I-B)a
       =-q[(1-epsilon)kappa n+epsilon r I+epsilon kappa a^* A a]
       <=-epsilon q r I
       <=-alpha B,
alpha=epsilon q r/bmax>0.
Therefore L_i*F_i<=-alpha P_i F_i, with P_i the occupied-data projector. This is an operator inequality for arbitrary entangled clock/data states; no stationary clock approximation occurs.

## Multiplicative animals
For a connected check-graph animal A of size m put
F_A=exp(a m) product_{i in A} F_i,
Vtilde=sum_A F_A, Wtilde=sum_A m F_A.
Because all generator terms are on single sites, the exact Lindblad product rule gives
L*F_A<=-alpha (sum_{i in A}P_i)F_A.
There is no disconnected m^2 cross term. In each classical data sector, separate animals with s>=eta m occupied sites from sparse ones. Sparse animal operators satisfy
F_A<=theta^{(1-c-eta)m} bmax^{eta m} I, a=c log(1/theta),
where the RHS bounds the sector s<eta m (the monotonic dependence on s is used).
If the rooted animal count is <=A0^m and
A0 theta^{1-c-eta} bmax^eta<1,
then the usual sparse-animal sum yields
L*Vtilde<=-alpha eta Wtilde+C N.
Parameter compatibility is immediate for c<1, eta<1-c and sufficiently small theta, since bmax stays bounded at fixed clock rates.

## Generic local quantum perturbations retain only one animal-size factor
For an arbitrary bounded operator supported on at most k site+clock pairs (and an unrestricted shared bath), factor F_A into its factors inside and outside that support. Outside factors commute with the perturbation. The inside positive factor has condition number at most (bmax/theta)^k, uniformly in |A| and total volume. The standard conjugation/relative-form estimate therefore bounds each local Hamiltonian commutator or Lindblad adjoint by a fixed constant times F_A in quadratic-form order. Only perturbations whose physical support meets A contribute. With bounded local incidence, summing perturbations costs at most C_noise |A|F_A, not |A|^2F_A. Thus sufficiently weak bounded-strength continuous local Hamiltonian/Lindblad/shared-bath perturbations are absorbed by the exact drift.

This baseline isolates what the guarded SSF proof must preserve: a positive per-animal product, bounded single-local-error condition numbers, and a negative drift linear in animal size. Replacing products by their first-order expansion loses these properties at arbitrarily large |A|. Overlapping guards and syndrome-dependent multi-bit flips prevent simply copying this product to SSF; their local generators no longer act on only one factor and the mixed-update charging must be redone.
