# Exact noise-assisted Poissonization of arbitrary local Markovian generators

2026-10-29. This is a different physical design mechanism: deliberately add weak local full depolarization. It is NOT a Pauli twirl and does not approximate the existing coherent dynamics. It changes the physical generator by a specified noisy primitive.

## Exact lemma

Let N be any Hermiticity-preserving, trace-annihilating superoperator on a finite d-dimensional local data Hilbert space, with ||N||_diamond<=epsilon. In particular N may be an arbitrary Hamiltonian commutator plus local Lindblad dissipators. Let Delta(X)=Tr(X)I/d be full depolarization. Choose delta>=d² epsilon and define

    Phi = Delta + N/delta.

Phi is trace-preserving. Its normalized Choi matrix satisfies

    J(Phi) = I/d² + J(N)/delta,
    ||J(N)||_infinity <= ||J(N)||_1 <= ||N||_diamond <=epsilon,

so J(Phi)>=0. Thus Phi is CPTP, and EXACTLY

    N + delta(Delta-I) = delta(Phi-I).                (1)

There is no small-time/Trotter/adiabatic error. The added depolarizing generator provides an interior CP cushion that an isolated Hamiltonian generator lacks.

## Autonomous memory consequence

Suppose the ideal atomic memory is subjected to arbitrary unknown deterministic-time-dependent local Markov generators N_Z(t), each on a declared support Z of size at most s, with uniform ||N_Z(t)||_diamond<=epsilon_Z. Supports have bounded incidence. Add engineered independent full depolarization on every such support at rate delta_Z>=d_Z² epsilon_Z. Then its exact total generator is

    L_SSF + sum_Z delta_Z(Phi_Z(t)-I),

where every Phi_Z(t) is a local CPTP map. This is exactly the independent exogenous Poisson-kick model of the existing spacetime theorem. The maps may be unknown; no online noise characterization is needed beyond a worst-case strength bound and declared bounded-size support architecture.

If max delta_Z is below that theorem's primitive-rate threshold, the same exponential-in-cutoff lifetime follows. Since d_Z<=2^s is a constant, this is a nonzero unknown continuous Markovian-noise threshold. One may bound epsilon_Z by 2||h_Z||+2sum_a||K_Za||². Ideal depolarization at its selected constant weak rate is part of the new physical architecture.

If noise can occur on any support from a prescribed bounded-radius neighborhood family, add depolarization for each support in that family; bounded degree and radius make this a constant incidence overhead. Alternatively overcover a primitive's support by a fixed bounded-size patch and use that patch dimension in the bound. Unknown unbounded-range support architectures are not covered.

## What this does and does not prove

- Covers unknown, arbitrary time-dependent local DATA Markovian Hamiltonian and Lindblad generators, including ordinary amplitude damping, after adding the specified physical depolarization.
- Does not require stabilizer covariance, dephasing limits, a signed Dyson sieve, or a Hamiltonian perturbation series.
- It is not a proof for the original unmodified decoder. The deliberate extra noise is essential to identity (1)'s CP representation.
- Does not automatically cover arbitrary shared retained bath interactions. Data-only depolarization has rank-deficient Choi support on the joint data-bath map, so it cannot cushion arbitrary bath directions. Depolarizing an inaccessible bath is not authorized or assumed. Bounded, accessible local ancillary Hilbert spaces could be included in the patch at a larger constant d, but a shared uncontrolled bath cannot.
- Physical noisy controllers require their separate compiler interface. Depolarization acting on a controller patch is a new primitive; it must satisfy architecture/locality constraints and be charged to controller faults. The ideal atomic conclusion must not be silently promoted to the full compiled device.

This is an exact route to a broad UNKNOWN MARKOVIAN continuous-noise information phase with a modified autonomous architecture, conditional only on the existing atomic D0/D1 memory theorem. The stronger common-bath generality remains open.

## Conditional physical-controller composition (stronger than data-only)

If each declared primitive support Z includes a bounded number of finite-dimensional physical controller/workspace sites as well as data, the exact lemma applies to that FULL patch. Its dimension d_Z must remain independent of N. A local deviation N_Z may even be a signed HP trace-annihilating difference between actual and ideal generators; it need not separately be GKSL. Engineered full-patch depolarization turns it into a CPTP-kick generator exactly.

Therefore, IF the already-reviewed physical compiler theorem accepts arbitrary CPTP kicks on those full patch supports and the added depolarizing primitive is physically available with the required bounded locality, Eq.(1) composes directly with that theorem. This avoids the continuous controller no-jump issue that invalidates a mere DATA-covariance argument. It does not establish the new engineered primitive's implementation automatically; locality, dimension, incidence, and its own implementation errors must be included in the stated primitive model.
