# Exact damped-ancilla representation and rate-independent event count

Root working construction, 31 October 2026. Independent review pending. This is not yet an efficient simulation algorithm or a novelty claim. It follows the delivered single-operator theorem, but is separate new work.

## 1. Target process
Let independent stationary symmetric signs xi_i flip at rates lambda_i>0. Let A_i and H0 be bounded Hermitian system operators; the A_i need not commute. Set v_i=sqrt(gamma_i*lambda_i), gamma_i>=0, and

H_xi(t)=H0+sum_i v_i xi_i(t) A_i.

Write L0(X)=-i[H0,X] and Li(X)=-i[A_i,X]. For each subset S of {1,...,r}, define the classical signed moment
x_S(t)=E[(product_{i in S} xi_i(t)) rho_xi(t)].

These obey the finite closed hierarchy
x_S'=L0(x_S)-2(sum_{i in S}lambda_i)x_S+sum_i v_i Li(x_{S symmetric_difference {i}}).
Initially x_empty=rho and all other x_S=0. The desired system state is x_empty.

## 2. A positive quantum dilation with the same full process
Introduce r two-level ancillas initially in |0...0>. Let X_i be their Pauli X operators, P_i=|1><1|, and sigma_minus_i=|0><1|. Define

H_ext=H0 tensor I+sum_i v_i A_i tensor X_i,
J_i=2sqrt(lambda_i) I tensor sigma_minus_i.

Evolve by the ordinary Lindblad generator -i[H_ext,.]+sum_i D[J_i]. Define y_S=Tr_anc[(product_{i in S}X_i) rho_ext].

For the dissipator, D[J_i]^dagger(X_i)=-2lambda_i X_i and D[J_i]^dagger(I)=0. For the Hamiltonian, the ancilla X operators commute with one another. Partial-trace cyclicity for ancilla-only operators gives

Tr_anc[X_S(A_i X_i rho-rho A_i X_i)] = [A_i,Tr_anc(X_{S symmetric_difference {i}}rho)].

Consequently y_S obeys exactly the x_S hierarchy, with the same initial conditions: ground ancillas have zero expectation for every nonempty X product. Uniqueness of the finite linear ODE proves y_S=x_S for every S and every time. In particular, the system marginal is identical.

This is more than one-time channel equality. A system-only instrument applies the same linear CP map to every x_S and y_S in each unnormalized outcome branch. Induction between intervention slots proves equality of all system/retained-ancilla/reference outputs and outcome records for arbitrary adaptive system instruments at prescribed times. The damping ancillas and their jump records stay private. No commutativity of the A_i was used. No fast-rate limit or weak-coupling approximation was used.

The hierarchy has 2^r blocks, but it is used for the equivalence proof; implementing the displayed Lindblad dilation requires r ancillas, not a classical table of all blocks.

## 3. Physical jump count independent of the fast switching rates
Let N count all J_i jumps in the standard jump unraveling of this dilation. Fix theta>0 and put kappa=exp(theta)-1, delta=2kappa. Define the positive ancilla weight

V=product_i (I+delta P_i).

The count-tilted generator replaces each J_i rho J_i^dagger by exp(theta) times that term and leaves its anticommutator unchanged. On V, the ith dissipative adjoint term is

4lambda_i [exp(theta)-1-delta] P_i V_other = -4lambda_i kappa P_i V_other.

H0 commutes with V. The ith Hamiltonian commutator is i v_i delta A_i tensor [X_i,P_i] V_other. In the ith ancilla's 0/1 decomposition, the sum of these two terms is the Hermitian block matrix

[[0, i v_i delta A_i],[-i v_i delta A_i, -4lambda_i kappa I]] tensor V_other.

For vectors u,w in the remaining system/ancillas, completing the square gives
2v_i delta a_i ||u||||w||-4lambda_i kappa||w||^2
<=v_i^2 delta^2 a_i^2/(4lambda_i kappa) ||u||^2,
where a_i>=||A_i||. Since delta=2kappa and v_i^2=gamma_i lambda_i, the coefficient equals gamma_i a_i^2 kappa. Thus this block is at most gamma_i a_i^2 kappa I, and hence at most gamma_i a_i^2 kappa (I+delta P_i). Tensoring the commuting positive V_other preserves the inequality.

Summing yields G_theta^dagger(V)<=Gamma kappa V,
Gamma=sum_i gamma_i a_i^2.

The tilted evolution preserves positivity. Gronwall and the initial ground-ancilla value Tr(V rho_ext(0))=1 imply

E exp(theta N) <= Tr[V rho_theta(T)] <= exp[Gamma T(exp(theta)-1)].

The first inequality uses V>=I. This is a Poisson moment-generating-function upper bound, not necessarily a stochastic domination coupling. In particular E N<=Gamma T, and ordinary Chernoff optimization gives Poisson-type upper tails. The bound is uniform in every lambda_i, even for noncommuting A_i and arbitrary entangled system input.

System-only CPTP controls preserve V in the Heisenberg picture. Including their records and branch-dependent operations therefore preserves the same bound across prescribed intervention slots. A normalized rare postselected branch is not covered by the unconditional statement.

## 4. Why this is potentially useful, and what it does not earn
The conventional sign-register unraveling has rate lambda_i and processes a typical sum_i lambda_i*T flips. This exactly equivalent positive representation instead has a jump count controlled by Gamma*T, the accumulated diffusion scale. It removes the signed-normalization issue from the event-count representation itself.

However its no-jump generator is
H_eff=H0+sum_i v_i A_i X_i-i2sum_i lambda_i P_i.
Its norm is still large. A cheap method to acquire the holding times and apply the corresponding no-jump Kraus maps on actual reachable states is NOT supplied by a small expected count. Neither a normalized no-jump propagator nor a general non-Hermitian solver may be assumed free. Full return, source, control and numerical costs remain open. The result is an exact representation plus a resource inequality, not a completed noncommuting-noise compiler.

Quantum pseudomodes, damped-ancilla embeddings, quantum-jump gauges and Zeno/adiabatic elimination are strong ordinary comparators that must be checked before claiming novelty. The exact hierarchy proof here does not rely on an unreviewed external construction.
