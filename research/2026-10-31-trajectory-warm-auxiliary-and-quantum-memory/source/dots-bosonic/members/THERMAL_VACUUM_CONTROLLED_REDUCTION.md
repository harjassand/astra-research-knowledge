# Exact thermal-to-vacuum receiving, including quantum backaction

31 October 2026. Independent candidate for review. Thermofield/vacuum thermalization is established ordinary machinery; no novelty is claimed. This note supplies an explicit damped-mode, retained-control interface to the separate infinite-Fock construction. It is not by itself a high-precision compiler.

## 1. Physical and virtual models

A physical oscillator b has frequency omega, damping parameter kappa>0 and stationary thermal occupation nbar>=0. Its free generator has Hamiltonian omega b^dagger b and jumps

    sqrt(2kappa(nbar+1)) b,
    sqrt(2kappa nbar) b^dagger.

It starts in its thermal stationary state and is initially independent of the system/reference. The interaction is

    H_int=S b^dagger+S^dagger b,

where S is a bounded system operator, not necessarily Hermitian. Multiple modes and arbitrary noncommuting system operators are allowed by taking a finite tensor product. H0 is bounded and separately supplied. Prescribed system instruments retain all their accessible outcome records and references; they cannot inspect physical or virtual reservoir coordinates.

Introduce two virtual modes a,c in their joint vacuum, with free Hamiltonian

    omega(a^dagger a-c^dagger c)

and jumps sqrt(2kappa)a, sqrt(2kappa)c. Define

    u=sqrt(nbar+1), v=sqrt(nbar),
    b=u a+v c^dagger.

Then [b,b^dagger]=u^2-v^2=1. A complementary mode d=u c+v a^dagger commutes with b,b^dagger and is canonical. The finite-mode Bogoliubov transform is unitarily implementable, so the bounded physical b-observable algebra is a normal embedded factor in the doubled oscillator algebra.

The interaction becomes

    u(S a^dagger+S^dagger a)
       +v(S c+S^dagger c^dagger).

Thus the two virtual creation coefficients are F_+=uS and F_-=vS^dagger, with frequencies +omega and -omega. Both reservoir jump operators are lowering operators and the initial state is dark. A negative-frequency auxiliary mode is a mathematical digital representation, not a physical device or free thermodynamic resource.

## 2. Exact bounded-Weyl algebra identity

Let W_b(zeta)=exp(zeta b^dagger-zeta* b). Then

    W_b(zeta)=W_a(u zeta) W_c(-v zeta*).

The virtual vacuum expectation is exp[-(u^2+v^2)|zeta|^2/2], precisely the thermal characteristic function with occupation nbar. This establishes the initial-state restriction, not merely its mean energy.

The vacuum damped mode of frequency +omega sends its Weyl observable to

    exp[-(1-exp(-2kappa t))|eta|^2/2]
       W_a(eta exp[(-kappa+iomega)t]).

The c mode has frequency -omega. Applying both maps to the displayed product yields

    exp[-(nbar+1/2)(1-exp(-2kappa t))|zeta|^2]
       W_b(zeta exp[(-kappa+iomega)t]).

This is exactly the physical thermal attenuator. Therefore the doubled free normal CP semigroup preserves the entire b-Weyl algebra and restricts to the thermal free semigroup, not just to one- and two-point functions. Normality extends the identity from Weyl generators to the von Neumann algebra they generate.

System-only maps preserve this subalgebra. The actual interaction Hamiltonian is affiliated with the system-plus-b algebra, and its unitary conjugation is the embedded physical interaction. Hence EVERY finite product of free semigroup steps, interaction unitary steps and system instruments has exactly the same accessible expectation values and retained-record statistics in the physical and doubled models. No reservoir reset is inserted at a control boundary.

The companion `INFINITE_FOCK_CONTROLLED_LIMIT.md` constructs the normal infinite vacuum process and proves a uniform-in-splitting cutoff estimate. It permits passing these finite-product identities to the actual interacting limit. Specifically, the virtual splitting products have a cutoff error uniform in their number, so bounded-cutoff Lie convergence and cutoff convergence can be interchanged. Restriction to the closed physical observable factor then defines the normal thermal interacting process. Its finite-particle generator is the stated thermal oscillator GKSL expression plus the physical interaction. This is a canonical process construction, not an appeal to unspecified uniqueness of arbitrary unbounded extensions.

Generator-domain precision: a physical finite-particle test operator is not a finite-support operator in the virtual basis. Choose its complementary d mode in vacuum. A physical finite-particle vector tensored with that vacuum is mapped by the finite squeezing unitary to a polynomial excitation of a two-mode squeezed vacuum. Its virtual occupation coefficients have an exponential tail for SOME z>1; for one unexcited squeezed pair it suffices that z^2*nbar/(nbar+1)<1. Polynomial excitations preserve a slightly smaller such z. In particular the vector and its cutoff projections converge in the graph norm of total number N. For rank-one test operators |u><v|, this implies trace-norm convergence of the operator and of every formal generator term: H u is controlled by the N graph norm, a_i u by its square root, and a_i|u><v|a_i^dagger=|a_i u><a_i v|. The constructed virtual generator agrees with those terms on the cutoff test operators and is closed. Therefore the transformed test operator belongs to its domain, with the formal generator value. Taking the complementary partial trace and using the algebraic Gaussian restriction identifies the physical thermal GKSL sum on this test class. No virtual finite-support assertion or physical M3 bound is used.

The cutoff/splitting bound is applied ONLY to the doubled VIRTUAL vacuum process, whose initial M3 is1. The physical thermal state can have infinite Tr(3^N rho), and its heating jump does not preserve a smaller physical Fock cube. Neither a physical thermal M3 bound nor agreement of two heated physical cutoffs is assumed. Full physical Gaussian thermal channels are used in the algebraic products.

The linear interaction unitary is identified by the usual analytic-vector argument: finite-particle vectors obey ||H^k psi||<=C^k(n0+k)!||psi||/n0!, so the ordinary linear-oscillator Hamiltonian has the required canonical unitary evolution. The finite-mode Bogoliubov transformation preserves the requisite finite-energy domains; its squeezing is finite for every finite nbar. No cheap finite-dimensional approximation to that squeezing is needed in the digital model: the representation starts directly in virtual vacuum with transformed coefficients.

## 3. Explicit quantum backaction check

Ignoring the input-noise notation but retaining the interaction drift, the virtual Heisenberg equations give

    da/dt=-(kappa+iomega)a-i u S,
    d(c^dagger)/dt=-(kappa+iomega)c^dagger+i v S.

Consequently

    db/dt=-(kappa+iomega)b-i(u^2-v^2)S
          =-(kappa+iomega)b-iS.

This is the physical backaction coefficient, not a temperature-dependent multiple. The two independent vacuum input fields combine with coefficients u,v, giving thermal covariances nbar+1 and nbar. This check is consistent with the exact Weyl-algebra proof; it is not used as a substitute for that proof.

In particular, the virtual bath is not generally a classical Gaussian Hamiltonian noise source. Its noncommutative response remains present.

## 4. Paid temperature resources and moment receiving

For the physical coefficient S and the damping convention above, the virtual occupation moment constant is

    C_th=(2nbar+1)||S||^2/(2kappa),

and the actual virtual jump-count constant is

    Gamma_th=4C_th=2(2nbar+1)||S||^2/kappa.

Sum these over physical modes. In the root normalization F=sqrt(gamma lambda)G, kappa=2lambda, this is Gamma_th=gamma||G||^2(2nbar+1). Encoding normalizations, rather than inaccessible exact norms, are paid in a compiler. Two virtual modes are needed for each nonzero-temperature physical mode; at nbar=0 the zero-coupling auxiliary is omitted.

The finite-cutoff square in the companion note applies to the non-Hermitian F_+,F_- without assuming a CCR at the top cutoff. Therefore occupation and actual jump MGFs, the controlled Fock cutoff comparison, and the canonical infinite limit carry over. The auxiliary frequency sign changes none of these weights because number rotations commute with them.

Temperature has NOT been made free. The transformed coupling action grows by2nbar+1. Supplied nbar, rates, frequencies and operator encodings must be acquired at their real costs. Errors in those physical/model parameters must receive a separate controlled-process error allocation; exact representation formulas do not estimate unknown bath parameters.

The physical thermal initial number tail is

    Pr(N>=L)=(nbar/(nbar+1))^L.

Thus a naive physical local cutoff grows like nbar log(1/epsilon) at large nbar. Virtual vacuum starts at zero and moves temperature into coupling strength. This is not a gate lower bound for direct thermal preparation: a geometric mixed state can itself be sampled using logarithmic-precision classical arithmetic, and binary occupation registers do not require L qubits. Any claimed computational advantage needs the complete simulator's resource ledger, not this tail comparison alone.

## 5. A decisive limit of the classical-noise shortcut

Take nbar=0 and a Jaynes--Cummings interaction S=g sigma_minus. The ground-system/vacuum state stays dark, while an excited system transfers amplitude into the mode and, with damping, eventually emits. At times with excitation-loss probability p(t)>0 the system channel is an amplitude-damping channel, not unital. For zero damping during the comparison interval p(t)=sin^2(gt); positive damping preserves the nonunital mechanism (and the short-time loss is g^2 t^2+o(t^2)).

Any average of Hermitian system Hamiltonian trajectories driven by a classical private stochastic source is a mixture of unitaries and hence unital in the no-control instance. On input I/2, its trace-norm error from the actual amplitude-damping output is at least p(t), or p(t)/2 under the convention defining trace distance as half the trace norm. This rules out a general reduction of quantum reservoirs to classical colored Hamiltonian noise, even when symmetrized Gaussian statistics are matched. It is not a lower bound against pseudomodes, quantum Gaussian influence functionals or retained quantum ancillas.

## 6. Primary comparator scope

Thermal vacuum doubling is ordinary prior machinery. De Vega and Bañuls explicitly map a finite-temperature environment to two zero-temperature virtual environments, then chain-map them for tensor-network simulation. Their primary abstract directly states this scope. [Thermofield-based chain mapping, 2015](https://arxiv.org/abs/1504.07228).

Tamascelli and collaborators establish nonperturbative thermal-to-vacuum environment descriptions using temperature-dependent couplings, forming the basis of thermalized chain methods. This is a strong constructive alternative, not an assumption of a noiseless/classical bath. [Efficient simulation of finite-temperature open quantum systems, 2019](https://arxiv.org/abs/1811.12418).

There is also prior Gaussian multi-time equivalence machinery: matching appropriate one- and two-time environmental correlations can give equivalent system multi-time expectations for unitary versus Lindbladian Gaussian environments. Thus retained multi-time prediction is not a generally absent premise in ordinary pseudomode methods. [Smirne et al., 2023](https://arxiv.org/abs/2209.00293).

Coupled Lindblad pseudomode theory provides a positive quantum-channel representation, theoretical polylog(T/epsilon) mode-count evidence and a constructive realization approach. Mode count is not automatically a high-precision gate bound independent of mode damping/frequency, but it is an especially relevant acquisition/compression comparator. [Coupled Lindblad pseudomode theory, revised2026](https://arxiv.org/abs/2506.10308).

A direct quantum algorithm competitor also exists: the ancilla-train method treats multiple Gaussian environments at arbitrary coupling strength with inverse-accuracy polynomial resources. Its inspected proved Trotter resource bound assumes a time-independent system Hamiltonian; the abstract advertises time-dependent applicability, but this is not treated here as a proved general time-dependent resource bound. It uses a convolution-square-root correlation representation and retained ancilla registers, not a classical-noise surrogate. [Christensen, Agerskov and Nathan, 2026](https://arxiv.org/abs/2509.12717).

These inspected primary statements do not establish or exclude the precise high-precision/stiffness compiler sought here. This is not an exhaustive literature or priority determination. An attempted arXiv HTML fetch for2406.13512v2 returned404; it was not retried or replaced. All earlier denied-source restrictions remain unchanged.

## 7. Receiving boundary

What this note supplies: an exact finite-mode thermal representation with correct quantum backaction, retained controls, explicit temperature costs, and a rigorous receiving route through the separate canonical infinite-Fock limit. What remains separate: efficient positive-path preparation, no-jump/first-event assembly, precision-priced timing at large known frequencies, and the complete gate/resource theorem. No unbounded Fock-space compiler follows from thermofield algebra alone.
