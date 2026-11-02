# Stationary-state overwrite storage bound

Root construction, 2026-11-02. Conditional dynamical theorem, not a physical write implementation or a static thermal-stability theorem.

## Statement
Let the finite-dimensional memory/environment Hilbert space factor as L tensor G, where L is one decoded qubit. Let Q_X,Q_Y,Q_Z be its exact Pauli algebra, and let rho be any density matrix stationary under the actual Hamiltonian H: [H,rho]=0. No Gibbs form or maximally mixed logical marginal is required.

Let P be a projector and p=Tr(P rho). Suppose, for each of the three Paulis,

    [H,Q_j](I-P)=0,     ||[H,Q_j]|| <= c_j.

Prepare an arbitrary input xi_LR, with reference R, by the ideal overwrite channel

    E_rho(xi)=xi_LR tensor tau_G,     tau_G=Tr_L rho.

Then for U_T=exp(-iHT),

    || (Ad_U_T tensor id_R)(E_rho(xi))-E_rho(xi) ||_1
       <= min(2, T sqrt(p) sum_j c_j).

Consequently the same bound holds after tracing out G and uniformly over reference systems, hence as a diamond-norm bound on the decoded storage channel minus the identity. If c_j<=2 v n, the bound is min(2,6 v n T sqrt(p)).

More generally replace T c_j sqrt(p) by T sqrt(Tr(rho [H,Q_j]^dagger[H,Q_j])) separately for each j. This gives a direct stationary commutator-variance certificate, without a projector or any temperature parameter.

## Proof
Introduce auxiliary input qubit A. Put Omega=xi_AR tensor rho_LG and let S swap A and the decoded L factor. Its exact Pauli expansion is

    S=(I+X_A Q_X+Y_A Q_Y+Z_A Q_Z)/2.

Partial trace over A of S Omega S^dagger equals E_rho(xi), with A's former reference now attached to L. The initial input and stationary memory are independent; no assumption of factorization within rho is used.

Stationarity and the Duhamel formula give

    ||[U_T,Q_j] rho^(1/2)||_2
      <= integral_0^T ||[H,Q_j] exp(-iHt) rho^(1/2)||_2 dt
      = T ||[H,Q_j] rho^(1/2)||_2.

The last equality follows from [H,rho]=0 and unitary invariance of Hilbert-Schmidt norm. Since [H,Q_j]=[H,Q_j]P, the squared final norm is at most c_j^2 Tr(P rho)=c_j^2 p. Commutation of P with rho is unnecessary.

Tensoring a unitary Pauli on A contributes norm factor sqrt(Tr(xi_AR))=1, even for entangled xi_AR. Therefore

    ||[U_T,S] Omega^(1/2)||_2 <= (T/2) sqrt(p) sum_j c_j.

For unitaries V,W and a state Omega, purification or the identity XX^dagger-YY^dagger=(X-Y)X^dagger+Y(X-Y)^dagger implies

    ||V Omega V^dagger-W Omega W^dagger||_1
      <=2||(V-W)Omega^(1/2)||_2.

Apply this with V=U_T S and W=S U_T. Since U_T Omega U_T^dagger=Omega, the second output is S Omega S^dagger. Trace out A and use trace-norm contraction. This proves the assertion; tracing G proves the decoded-channel claim. The variance version is the same proof before using P.

## Consequence and boundary
A static bound p<=exp(-a n^alpha) yields a storage error <=6vnT exp(-a n^alpha/2), uniformly in temperature whenever that static bound is itself uniform. Logical ground-state splitting or logical thermal polarization does not create a separate beta-dependent consumer penalty: the ideal overwrite need not be close to the initial stationary state.

This is not a construction of the swap using local noisy controls. Its acquisition, preparation of tau_G, physical write exposure and final readout costs are not charged here. A full-Gibbs small bad-sector weight at fixed nonzero perturbation strength as beta tends to infinity remains to be proved for the actual native model. Nor does this theorem imply indefinite storage in a finite system: logical splitting and leakage constrain the commutator variances and therefore the bound.

No historical novelty claim. The argument uses elementary stationary commutator control and an auxiliary SWAP representation; its role is removing an unnecessary logical-twirl/temperature dependence in this programme's consumer.
