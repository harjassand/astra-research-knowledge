# Quantum syndrome coordinates: exact diagonal dynamics and a real positive-moment estimate

2026-10-29. These are constructive identities and a local moment theorem, not a claimed invariant residual-noise theorem.

## 1. Ideal SSF does not feed syndrome coherences into syndrome probabilities

Choose independent stabilizer syndrome bits and projectors Π_σ (dependent check bits may subsequently be functions of these). Write an ideal hub outcome Kraus operator as K_y=P_{F(y)} Π_y, where Π_y projects the measured local syndrome information and F(y) is its fixed accepted correction. For a target full syndrome σ', the restriction of K_y to an input syndrome σ is nonzero only when σ'=σ XOR syndrome(F(y)). For fixed y this XOR map is one-to-one.

Consequently

    Tr Π_σ' Φ_h(ρ)
      = sum_{σ: f_h(σ)=σ'} Tr Π_σ ρ,

with the ordinary deterministic syndrome update f_h, even when ρ has offdiagonal syndrome blocks, is entangled with an arbitrary bath/reference, and no full syndrome dephasing was performed. The different measurement outcomes are summed as a real instrument; amplitudes from different outcomes are not combined.

Thus the *clean* ideal SSF contribution to diagonal syndrome probabilities is exactly classical. This is stronger than assuming a Pauli mixture and does not imply the noisy contribution is classical.

## 2. Why a local quantum perturbation is not a classical transition generator

A local operator expands into boundedly many Pauli syndrome-XOR shifts. Its Hamiltonian commutator can feed diagonal probabilities from offdiagonal blocks. Already a two-sector system with H=g X and event projector Π=|1><1| has

    |d p/dt| <= 2|g| sqrt[p(1-p)],

with equality for suitable coherent states. There is no fixed finite-rate, input-uniform classical Markov bound dp/dt<=r(1-p)-r' p: p=1 requires r'<=0, while p tending to 1 has a possible positive derivative proportional to sqrt(1-p), exceeding any r(1-p).

This rules out one tempting exact diagonal-probability reduction. It does not rule out finite-block bounds with square-root losses or positive-moment methods.

## 3. Local pinching and CPTP Pauli-diagonal domination

For a pinching into D orthogonal syndrome sectors, positivity gives

    ρ <= D sum_a Π_a ρ Π_a.

If one pinches only the O(|W|) stabilizer bits near a fixed region W, the cost is 2^{O(|W|)}, not exponential in total volume. This is a mathematical domination inequality, not a free physical operation.

There is a related exact local channel inequality. Write Kraus operators of a CPTP map on s data qubits and a common bath as

    K_l=sum_{P in Pauli(s)} P tensor B_{lP}.

Define its data-Pauli-diagonalized channel

    Φ_diag(ρ)=sum_{l,P}(P tensor B_{lP})ρ(P tensor B_{lP})^dagger.

Partial trace of sum_l K_l^dagger K_l=I over the data proves sum_{l,P}B_{lP}^dagger B_{lP}=I_B, hence Φ_diag is CPTP. Vector Cauchy–Schwarz proves the CP-map order inequality

    Φ <=_CP 4^s Φ_diag.

It applies with the bath retained and arbitrary input entanglement. Applying it to every kick in the entire volume would give the unacceptable factor 4^{s M_total}. It helps only if a valid argument exposes O(|W|) relevant kicks and leaves all others untouched. Such exposure has not been proved for the adaptive SSF residual event.

## 4. Positive syndrome-moment theorem, including signed HP perturbations

Let J be a fixed set of stabilizer checks and define the violation observable and its positive moment

    n_J=sum_{a in J}(I-S_a)/2,       F_J(a)=exp(a n_J),   a>0.

Suppose each perturbation N_A(t) is trace-annihilating, Hermiticity-preserving, acts on a bounded data support A plus a retained common bath, and the *actual total generator* is physical. Let b bound the number of J checks touching any A. Define the local norm budget

    E_J(t)=sum_{A touching a J-check} integral_0^t ||N_A(u)||_diamond du.

There is no reduced-bath norm here. Let the clean instruments never increase n_J: in operator form Φ_h^*(F_J)<=F_J. Then for arbitrary positive joint initial state,

    Tr[F_J ρ_t] <= exp[e^(a b) E_J(t)] Tr[F_J ρ_0].       (1)

For exact codespace initialization and E_J(t)<=u |J|, this implies

    P[n_J>=β|J|]
      <= exp{|J|[-aβ+u e^(a b)]}.

For u<β/b, choosing e^(a b)=β/(bu) gives

    P[n_J>=β|J|] <= (e b u/β)^(β|J|/b).                (2)

This is a genuine local positive probability bound under coherent noise, with no dephasing, no Pauli mixture assumption, and no exponential-in-total-volume prefactor.

### Proof of the key operator inequality

Factor F_J=F_in F_out, where F_in contains just the checks touching A. These positive commuting factors have 1<=F_in<=e^(ab)I. F_out acts trivially on A and the bath, so the locality/bimodule property gives

    N_A^*(F_J)=F_out N_A^*(F_in).

The retained-bath norm bound implies

    ||F_J^(-1/2) N_A^*(F_J) F_J^(-1/2)||
      <= e^(ab)||N_A||_diamond.

Since N_A is HP, this yields an operator upper bound by e^(ab)||N_A||_diamond F_J. A term not touching a J-check contributes zero because N_A^*(I)=0. Add the nonpositive clean drift, take the expectation in the actual positive evolving state, and apply Grönwall.

Unlike the fault-insertion expansion, this argument does **not** need independently CPTP switching of the signed N_A. It needs the actual evolving state to be positive and the individual HP, trace-annihilating, local norm bounds. This scope distinction is important.

## 5. Where this theorem applies to SSF—and where it fails

For J equal to *all* stabilizer checks, every accepted ideal SSF move decreases n_J, so (1) and (2) apply to the actual ideal atomic decoder under continuous coherent Hamiltonian or suitable signed HP perturbations. This rigorously bounds large **global syndrome density** over a fixed time interval. It does not bound a small local dangerous cluster at finite noise density: typical global syndrome mass can be O(uN), much larger than code distance O(sqrt(N)).

For a proper fixed region J, an accepted correction can decrease total syndrome while increasing n_J by moving syndrome across the boundary. Thus the clean monotonicity hypothesis is not automatic. If H_boundary is the set of such crossing hubs and B bounds their possible increase, the universally valid substitute is

    Tr[F_J ρ_t]
      <= exp[e^(ab)E_J(t)+lambda t |H_boundary|(e^(aB)-1)]
         Tr[F_J ρ_0].                                  (3)

On bounded-degree expanders the boundary can be proportional to |J|, and its coefficient is the fast correction rate lambda, not the weak noise ε. Hence this estimate does not deliver the needed small local-stochastic parameter. The classical backward support localization removes precisely these boundary contributions *for a chosen Pauli history*. A quantum operator-level analogue that does so uniformly over surviving coherent branches is still missing.

## 6. Why minimum-representative projectors do not automatically fix localization

One can define an honest diagonal syndrome projector

    P_S=sum_{σ: S subset supp(R_min(σ))} Π_σ.

But it is generally a global function of the syndrome, even for small S. A local perturbation far from S can change the minimum representative chosen near S through a different global optimum/tie or a nonlocal syndrome configuration. It is therefore false to infer simply from physical locality that such a perturbation commutes with P_S. The supplied classical component argument proves this kind of localization only after a branch-specific small-cluster decomposition.

The stable residual-space problem is consequently not solved merely by changing vocabulary from Pauli errors to syndrome diagonal probabilities. What is needed is a genuinely local positive observable or a controlled family of quantum error-space projectors that both: (i) inherits SSF's backward contraction without a fast boundary penalty, and (ii) admits local-noise moment bounds such as (1). Neither property may be assumed from the classical marginal tail.

## Constructive conclusion

The exact clean diagonal dynamics, retained-bath channel pinching, and positive-moment bounds above are valid partial tools. They also expose two concrete failed shortcuts: finite-rate classical domination of coherent syndrome dynamics, and automatic commutation of distant perturbations with minimum-representative events. No invariant quantum residual contract is claimed.
