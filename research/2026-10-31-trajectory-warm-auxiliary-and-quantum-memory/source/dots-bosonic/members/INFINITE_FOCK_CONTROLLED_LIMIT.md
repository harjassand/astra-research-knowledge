# Controlled infinite-Fock receiving by finite-cutoff Cauchy limits

31 October 2026. Independent proof candidate; unreviewed. This supplies the domain/limit interface, not the positive-path compiler. No infinite-dimensional theorem is inferred from the prior finite-source compiler.

## 1. Model and conventions

There are finitely many modes, initially vacuum for the quantitative compiler bound, and bounded system operators H0 and F_i. F_i may be non-Hermitian and need not commute. Consider

    H=H0+sum_i omega_i n_i+sum_i(F_i a_i^dagger+F_i^dagger a_i),
    J_i=sqrt(2 kappa_i) a_i, kappa_i>0.

The known omega_i may have either sign. For the root convention, kappa_i=2lambda_i and F_i=sqrt(gamma_i lambda_i)G_i, ||G_i||<=alpha_i. Put

    C=sum_i ||F_i||^2/(2kappa_i),
    Gamma=4C=sum_i 2||F_i||^2/kappa_i,
    F2=sum_i ||F_i||^2.

Charged encoding bounds may replace all operator norms. System-only CPTP instruments occur at finitely many prescribed times, with arbitrary references and records retained. They do not inspect the reservoir. Bounds are unconditional; normalized rare postselection is excluded.

Use a local cutoff L for every mode. Its a_i satisfy a_i^dagger a_i=n_i exactly; their CCR is NOT assumed at the top level. All finite-cutoff generators are bounded and define ordinary normal CPTP evolutions.

## 2. Uniform weighted square, including non-Hermitian couplings

Set N=sum n_i and V=z^N, z>1. Conjugating the untilted adjoint by V^-1/2 gives the i-th contribution

    -d_i a_i^dagger a_i + i c_z(F_i^dagger a_i-F_i a_i^dagger),
    d_i=2kappa_i(1-1/z), c_z=sqrt(z)-1/sqrt(z).

System factors commute with a_i. With B_i=sqrt(d_i)a_i+i c_z F_i/sqrt(d_i), this expression equals

    -B_i^dagger B_i+(c_z^2/d_i)F_i^dagger F_i
       <= [(z-1)/(2kappa_i)]||F_i||^2 I.

The calculation uses only the weighted lowering identities and a_i^dagger a_i=n_i; it is valid at every cutoff. Number rotations and H0 commute with V. Thus, for vacuum input,

    Tr[V rho_L(t)] <= exp[C t(z-1)].

For an initial state with moment M_z, multiply the right-hand side by M_z. Instrument records can be included in the system factor: each unconditional instrument leaves the V expectation unchanged, so the estimate survives prescribed interventions without a factor proportional to their number.

For actual jump-count tilt exp(theta), take z=2exp(theta)-1. The same square has d_i=2kappa_i(1-exp(theta)/z), yielding

    E exp(theta J_T) <= exp[Gamma T(exp(theta)-1)].

This is first a finite-cutoff fact. It is not a pathwise bound on instantaneous intensity, nor a classical occupation trajectory assertion.

## 3. Exact comparison of two finite cutoffs

Let M>L and embed the cutoff-L evolution into the cutoff-M Fock space. If rho is supported in the smaller space, the damping dissipators and number Hamiltonians agree exactly: lowering preserves that space and a_M^dagger a_M=n. The generator difference on rho is solely the boundary Hamiltonian commutator.

Let P_L project on occupations <=L in every mode. Its outward raising block is

    B_L=sum_i sqrt(L+1) F_i tensor |L+1><L|_i
                      tensor identity_on_other_small_modes.

Different i terms have orthogonal OUTGOING ranges: precisely mode i is outside the smaller cube. Therefore

    B_L^dagger B_L=sum_i (L+1)F_i^dagger F_i tensor P_(n_i=L).

For a positive state rho_L, trace-class Cauchy--Schwarz gives

    ||[B_L+B_L^dagger,rho_L]||_1
      <=2 sqrt(Tr[rho_L B_L^dagger B_L])
      <=2 sqrt((L+1)F2) sqrt(M_z) exp[Ct(z-1)/2] z^(-L/2).

Duhamel's formula propagates this source by the larger CPTP evolution, a trace-norm contraction. With instruments, apply Duhamel on each control-free interval and telescope the subsequent normal CPTP instruments. The integrals sum to at most the full time integral; there is no p-fold error multiplier. Uniformly over references and retained outcome records,

    ||rho_M(T)-rho_L(T)||_1
      <=2T sqrt((L+1)F2) sqrt(M_z)
             exp[CT(z-1)/2] z^(-L/2).

For vacuum and z=2 this is

    2T sqrt((L+1)F2) exp(Gamma*T/8) 2^(-L/2),

exactly the root candidate's cutoff bound. This is a comparison of ACTUAL finite processes, not a claim that measuring number throughout the evolution is harmless.

One can select L by checking this explicit scalar inequality. It has order

    L=O(Gamma*T+log(2+T^2 F2)+log(1/epsilon)),

absorbing the logarithm of L into a larger constant. Its role is a quantum local cutoff; the joint dimension (L+1)^r must not be enumerated by the eventual compiler.

## 4. Constructing the normal infinite process

For an arbitrary trace-class joint input define a CPTP cutoff-input map

    E_L(rho)=P_L rho P_L
             + |vac><vac| tensor Tr_F[(I-P_L)rho(I-P_L)],

with the system/reference factors retained in the second term. E_L converges strongly in trace norm to the identity. Evolve its output with the cutoff-L generator and embed the result into the full Fock space.

For inputs supported in a fixed finite Fock cube, Section3 applies with finite M_z and proves that these maps are Cauchy uniformly on compact time intervals. Such inputs are trace-norm dense. Contractivity extends the limit to every trace-class joint input. The limit is a normal CPTP map, completely positive also with arbitrary reference systems. Composition passes to the limit by contraction and strong convergence, yielding a strongly continuous normal CPTP semigroup before controls. Insert any fixed finite sequence of normal system instruments to obtain the controlled process. The vacuum-initial quantitative bound of Section3 is uniform over system/reference inputs and is therefore a controlled-channel bound, not only a pointwise state convergence assertion.

The limiting generator agrees with the formal oscillator GKSL expression on finite-Fock-supported trace-class test operators. To see this, divide the Section3 error bound by t, uniformly for small t. Its residual coefficient tends to0 as L grows. For L beyond the test operator's support plus one, the finite generator acting on that test operator is already the formal expression. First let t tend to0 at fixed L and then L grow. Linear decomposition handles nonpositive test operators.

This establishes a concrete normal conservative process and its specified test-domain generator. Merely agreeing on that dense test domain is not, by itself, a theorem that every imaginable unbounded extension is identical. The canonical finite-cutoff/Trotter process below is the target received by the compiler; no unproved global domain uniqueness is needed.

The finite jump-count MGF also has a canonical receiving: augment the finite processes by classical counters and use the same bounded nonnegative count tests and monotone limit, or first cap the count register. Initial finite-cutoff bounds are uniform, so the limiting count distribution retains the MGF bound. The count cap is not inferred from occupation alone.

## 5. A separate uniform-in-splitting bound

To identify the limit with alternating free-damping and interaction evolutions, a uniform Lie-product limit is needed. Do NOT use an unpriced interchange of two limits. The following deliberately coarser bound supplies it.

Let u be the accumulated interaction-unitary time, 0<=u<=T, excluding pure damping/number-rotation steps. Set

    z(u)=1+2/(1+u/T), so z(0)=3, z(T)=2,
    (z-1)^2/(-z')=2T.

During an interaction interval, differentiating V(u)=z(u)^N adds (z'/z)NV. Complete the same oscillator square against this negative term, now without relying on damping. The coefficient is

    (sqrt(z)-1/sqrt(z))^2/[-z'/z]
      =(z-1)^2/(-z')=2T.

Consequently

    Tr[z(u)^N rho] <= M_3 exp[2T*u*F2].

Free vacuum damping decreases the number weight, number rotations leave it unchanged, and system CPTP instruments preserve it unconditionally. The bound therefore holds for EVERY finite splitting sequence whose total interaction time is at most T, independent of the number of steps. In particular its final and intermediate 2^N moment is at most M_3 exp(2T^2 F2).

Comparing two cutoffs along such a splitting sequence, free damping and number rotations still agree on the smaller subspace. Boundary Duhamel errors occur only during interaction-unitary pieces, whose durations total T. Thus the difference is at most

    2T sqrt((L+1)F2) sqrt(M_3)
           exp(T^2 F2) 2^(-L/2),

uniformly in the splitting count. This coarse bound may scale poorly with the microscopic rate through F2. It is for EXISTENCE/limit identification only, not the compiler's cutoff complexity. The sharper continuously damped bound in Section3 remains the algorithmic cutoff.

Interaction-clock qualification: the displayed coarse bound assumes the TOTAL duration of interaction-unitary pieces is at most T, as when each step applies the complete interaction Hamiltonian once. If Re/Im components or individual modes are split into separate pieces whose durations sum to U>T, use u<=U and z(u)=1+2/(1+u/U) instead. The resulting identification bound uses exp(2U^2 F2) for the moment and 2U sqrt((L+1)F2)exp(U^2 F2)2^(-L/2) for cutoff comparison (and sqrt(M3) for nonvacuum finite-moment input). This is still uniform in splitting count for fixed U, but must not be mislabeled as a physical-T bound. The sharp continuously damped algorithmic cutoff is unchanged.

For each fixed finite cutoff, ordinary bounded-generator Lie splitting converges to its exact finite Lindblad evolution. The uniform splitting cutoff estimate now permits exchanging the cutoff and splitting limits. Thus the canonical infinite process is exactly the strong limit of free Gaussian damping/rotations alternated with the actual linear interaction unitary. Retained system instruments can be inserted at their prescribed boundaries throughout.

## 6. Existence of the linear interaction unitary

This argument does not require treating an unbounded linear Hamiltonian as a free oracle. Its existence can be obtained by the same cutoff Cauchy comparison at wavefunction level, with the coarse moment bound and no dissipator. Apply it for positive and negative times to finite-particle vectors; the strong limits are inverse unitaries and form a strongly continuous group. The formal finite-particle Hamiltonian is its generator on that test domain.

For completeness, finite-particle vectors are analytic for this linear-plus-number Hamiltonian: H maps the total-number<=n subspace into <=n+1 and has norm there at most C0(n+1), for a finite C0 depending on the bounded system coefficients and finite frequencies. Therefore

    ||H^k psi|| <= C0^k (n0+k)!/n0! * ||psi||.

Its power series has nonzero radius for every finite-particle psi. This also identifies the usual selfadjoint linear-oscillator Hamiltonian, rather than an unspecified boundary condition at infinity. The possibly large C0 is not an algorithmic step count; the eventual compiler must separately earn its frequency-independent representation.

## 7. Exact scope

The normal infinite reservoir process, controlled cutoff error and splitting interchange are constructive. A cheap birth-death bridge source, factorized first-event isometry, and full high-precision gate ledger are NOT supplied by this note. The root positive-path construction must still earn those independently. Temperature reduction is a separate algebraic receiving map whose proof uses the canonical splitting limit established here.
