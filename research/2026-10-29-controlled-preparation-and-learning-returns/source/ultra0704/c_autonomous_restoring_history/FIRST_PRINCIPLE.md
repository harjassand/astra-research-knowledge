# Exact stochastic-event admission, not Zeno elimination

29 October 2026. Developing principle; no full autonomous charged-memory theorem is claimed.

For a fixed Hermitian Pauli P and unknown real h, choose a positive ballast rate lambda BEFORE h. The exact Lindblad gauge identity is

    lambda (Ad_P-id) - i h [P,.] = r (Ad_U-id),
    r=lambda+h^2/lambda,
    U=(sqrt(lambda)P+i h/sqrt(lambda) I)/sqrt(r).

The physical controller implements only the known ballast. It does not need to learn h or enact U: the right hand side is an exact representation of the actual unknown generator. The construction admits no Trotter, finite-order, infinite-dephasing or O(n time) remainder. It sacrifices a fixed local stochastic-noise budget. This is an application of the established Lindblad gauge freedom, not a new generator identity.

For q-qubit H=sum_{P!=I} h_P P, put m=4^q-1. If ||H||<=epsilon, Parseval gives sum h_P^2<=epsilon^2. Uniform ballast lambda=epsilon/sqrt(m) has a worst-case total event rate <=2sqrt(m)epsilon. A rational alternative lambda=epsilon/2^q gives rate <2^(q+1)epsilon. All coefficients and supports are chosen without unknown microscopic errors. Additional local unitary jump errors remain unitary jumps. These errors need not obey detailed balance with the nominal Gibbs Hamiltonian.

NONUNITAL errors are separate: no mixture of unitary-jump generators can reproduce E(I)!=0. For an arbitrary local trace-annihilating Hermiticity-preserving E, depolarizing Choi padding instead yields a CPTP event map Phi=D+E/kappa when ||J(E)||<=kappa/d. This is not a reduction to the literal unitary-jump class.

The remaining LOAD-BEARING gate is a physical-time restoring-history threshold for a fully autonomous controller. A synchronous fault threshold cannot be substituted. A positive mean successful update rate does not establish multipoint fault bounds or repair local clock defects. The primary continuous construction 2601.20818v1 Section IV is being checked at that exact interface.
