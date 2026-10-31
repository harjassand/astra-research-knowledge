# Vacuum cutoff limit and the exact thermal interface

Root domain/physics receiving candidate, 31 October 2026. Independent review pending. It supplements the first construction and is not in any delivered archive.

## 1. Allow the genuinely quantum coupling
For each mode let C_i be an arbitrary bounded system operator, not necessarily Hermitian. Write

H=H0+sum_i Omega_i n_i+sum_i g_i(C_i a_i^dagger+C_i^dagger a_i),
J_i=2sqrt(lambda_i)a_i, lambda_i>0,
Gamma_i=g_i^2 alpha_i^2/lambda_i, Gamma=sum_i Gamma_i,

where alpha_i is an accessible, charged normalization for C_i. Birth insertions use C_i/alpha_i and death insertions its adjoint. The positive scalar path weights are unchanged. Known number rotations are explicit diagonal operations, with their phase precision paid; their frequencies need not be small or positive in an auxiliary representation.

All initial auxiliary modes are vacuum. External controls act only on the system/reference/record space at prescribed times. No reservoir reset is allowed at those controls.

## 2. Finite-cutoff weighted squares require no exact CCR
At any finite local cutoff, a_i^dagger a_i=n_i and [n_i,a_i]=-a_i remain exact. Let V=z^(sum n_i). The conjugated Hamiltonian commutator is

i g_i(sqrt(z)-1/sqrt(z))(C_i^dagger a_i-C_i a_i^dagger).

With count tilt exp(theta), the conjugated dissipator is
-4lambda_i(1-exp(theta)/z)n_i.

For z>exp(theta), completing the square of
sqrt(k)a_i+i g_i(sqrt(z)-1/sqrt(z))C_i/sqrt(k),
k=4lambda_i(1-exp(theta)/z),
gives the scalar upper bound

Gamma_i (z-1)^2/[4(z-exp(theta))].

H0 and all Omega_i n_i commute with V. At theta=0 this gives E z^N(t)<=exp[Gamma*t*(z-1)/4]. At z=2exp(theta)-1 it gives E exp(theta N_jumps(T))<=exp[Gamma*T*(exp(theta)-1)]. Initial vacuum has weight one; system-only CPTP instruments preserve V. The estimates apply to all finite local cutoffs and arbitrary entangled system inputs, without invoking a false finite-dimensional CCR.

## 3. Finite-to-finite comparison and a controlled limit
Embed a local-L-cutoff evolution and a larger-local-cutoff evolution in the same larger Hilbert space. On states supported in the smaller cube, all damping terms coincide: lowering stays inside and a^dagger a is the same number operator. Free number rotations and H0 also coincide. Only raising terms at n_i=L cross the boundary.

For a smaller-cutoff density rho, the crossing outputs for different modes occupy orthogonal subspaces (one specified mode is at L+1 and the others remain<=L). Hence

||[H_cross,rho]||_1
 <=2 sqrt[(L+1)sum_i g_i^2 alpha_i^2 Pr_rho(n_i=L)]
 <=2 sqrt[(L+1)sum_i g_i^2 alpha_i^2]
       exp(Gamma*t/8) 2^(-L/2).

The first inequality follows from ||H_cross rho||_1<=sqrt(Tr rho H_cross^2). The second uses the smaller dynamics' number moment at z=2. Duhamel and trace-norm contraction of the larger finite channel yield

||rho_large(T)-rho_L(T)||_1
 <=2T sqrt[(L+1)sum_i g_i^2 alpha_i^2]
       exp(Gamma*T/8)2^(-L/2).

This bound holds uniformly over larger cutoffs, references and prescribed system instruments, by splitting the Duhamel integral at controls and keeping their records. There is no extra factor p in this physical cutoff error; total free-evolution duration remains T.

The finite channels are therefore Cauchy on vacuum-source inputs in the completely bounded output trace norm relevant to these controlled experiments. Their limit is a trace-preserving CP controlled process. For an initial finite-particle state, the same argument has its finite initial exponential-moment prefactor. This gives a dense state class from which a contractive extension can be defined. The theorem should refer to this controlled limit, not casually assert uniqueness of every possible unbounded formal Lindbladian extension.

Choose L by the explicit inequality that the displayed bound is <=the cutoff error budget. It has

L=O(Gamma*T+log(2+T^2 sum_i g_i^2 alpha_i^2)+log(1/epsilon)).

Log L is absorbed by increasing a universal constant or by a finite doubling search on the logarithmic inequality. Every local mode uses dimension L+1; their joint space is not enumerated.

## 4. Identification with ordinary physical product dynamics
There is a constructive way to identify this limit without assuming an unpriced infinite-dimensional solver. Split evolution into ordinary free number/system unitaries, linear system-boson interaction unitaries, and Gaussian damping channels. Each is individually well defined. For a general C, split its Hermitian real/imaginary parts into bounded-system controlled quadrature displacements. Work first with a finite product mesh and finite cutoffs.

A uniform SECOND-number-moment estimate suffices for this identification step; it need not carry the optimized stiffness resource bound. During a bounded-system linear interaction, Cauchy-Schwarz on the number commutator gives

|d/dt E(N+1)^2|<=C(sum_i |g_i|alpha_i) E(N+1)^2

for an absolute constant after harmless finite-mode factors are included. The cutoff version has the same bound because a a^dagger<=n+1. Free rotations/system operations preserve number, and vacuum damping decreases increasing number moments. Thus all product meshes have a common finite second-moment bound at fixed physical parameters. For thermal damping the corresponding polynomial moment estimate may grow with the finite damping/temperature parameters, but remains uniform in mesh size; it is used only for identification, not the compiler's resource estimate.

The boundary comparison with that second moment gives an error tending to zero with the Fock cutoff, uniformly over product meshes. At each fixed cutoff, ordinary bounded-operator Trotter convergence identifies the product limit with its finite Lindblad evolution. The resulting double-limit comparison identifies the controlled vacuum limit above with this physical product dynamics. This is the required receiving route; any claim using a different formal unbounded dynamics must first identify it with the same conservative process.

## 5. Thermal doubling on the full observable algebra
For one physical thermal mode b, occupation nbar, frequency Omega and damping jumps
2sqrt(lambda(nbar+1))b and 2sqrt(lambda nbar)b^dagger,
introduce vacuum modes a,c and set

b=sqrt(nbar+1)a+sqrt(nbar)c^dagger.

This is a canonical embedding because [b,b^dagger]=1. In Weyl form,

W_b(z) maps to W_a(sqrt(nbar+1)z) W_c(-sqrt(nbar)conjugate(z)).

The two-vacuum expectation is exp[-(nbar+1/2)|z|^2], exactly the thermal state's characteristic function. Evolve the vacuum modes with frequencies +Omega,-Omega and jumps 2sqrt(lambda)a,2sqrt(lambda)c. Their product Gaussian attenuator restricted to the embedded b-Weyl algebra has the physical thermal attenuator's drift and covariance. This is an algebraic channel intertwining, not merely a match of a two-time correlation function.

The physical interaction g(C b^dagger+C^dagger b) maps to

g sqrt(nbar+1)(C a^dagger+C^dagger a)
+g sqrt(nbar)(C^dagger c^dagger+C c).

The second virtual raising operator is C^dagger, which matters when C is not Hermitian. A direct Langevin backaction check gives db=-(2lambda+iOmega)b dt-i g C dt plus thermal input increments: the two terms contribute -(nbar+1)i g C and +nbar i g C, leaving the correct coefficient. No weak-coupling or classical-noise substitution is used.

For complete controlled-process equivalence, use the Weyl-algebra embedding on each free Gaussian channel and each bounded-system controlled quadrature interaction. Every finite product experiment, including system-only instruments, intertwines exactly. The product-limit identification in Section4 then transfers the full system process, not only terminal expectations. Thermal preparation is represented by the virtual vacuum restriction; known nbar and its acquisition remain inputs.

The effective vacuum resource is Gamma_i^(thermal)=g_i^2 alpha_i^2(2nbar_i+1)/lambda_i. This thermal strength is paid, not declared free. Negative-frequency auxiliary number rotations are a digital representation, not a thermodynamic hardware claim.

## 6. Exact classical OU is only a special interface
At Omega=0 and Hermitian C, the q=a+a^dagger observable algebra is commuting and invariant under the free attenuator. Its stationary vacuum restriction is Gaussian with variance one and OU generator 2lambda(d^2/dq^2-q d/dq). The coupling unitary is diagonal in q and acts pointwise on system operators. Thus finite products reproduce the classical OU Markov/Hamiltonian products, and their limits reproduce the continuous OU-driven system process. Finite Fock matrices do not themselves possess this exact quadrature algebra; the identification is at the controlled limit.

At nonzero frequency or general non-Hermitian coupling, the quantum bath's ordering/backaction is retained. Do not call it classical OU noise merely because a correlation function is exponential.

## 7. Still required
The positive immigration-death source, finite-word endpoint conditioning, factorized row/column access, jump envelopes and entire private-clock compiler must be separately received. These domain/interface arguments do not earn them by themselves. Standard thermofield, Gaussian pseudomode, multi-time equivalence and bosonic truncation literature must be credited; no generic novelty is claimed for those ingredients.
