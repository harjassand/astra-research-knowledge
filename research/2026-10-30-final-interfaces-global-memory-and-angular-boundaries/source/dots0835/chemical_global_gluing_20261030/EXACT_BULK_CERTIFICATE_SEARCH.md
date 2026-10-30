# The bulk construction can be synthesized without a supplied barrier

Scope: rational positive rate constants and integer stoichiometry; existence/termination, not efficiency. This does not construct the missing global boundary certificate.

The finite killed-generator compactness lemma proves strict l^p dissipativity for ALL sufficiently large p. Thus p can be found by an explicit terminating search rather than supplied as an oracle:

1. Enumerate integers p≥2. For the full strongly connected complex generator Q, decide the real polynomial sentence

       for every u≥0 with sum u_i^p=1 and product u_i=0,
           sum_i u_i^(p−1)(Qu)_i <0.

   Rational real quantifier elimination decides each instance. The proved boundary contraction guarantees eventual acceptance.
2. Find a rational eta>0 by searching reciprocals1/k and checking the same sentence with upper bound−4eta. Compactness guarantees termination. Retain explicit slack: continuity supplies an interior boundary-neighborhood margin of at least2eta, and choose the factorial-error bound at mosteta.
3. Use the exact factorial finite-product bounds to choose a rational/integer high-count threshold K that absorbs the O(1/min x) error. All finite graph/rate/p constants are explicit finite products and sums once p is fixed.
4. For a fixed rational stoichiometric class x0+S, find a finite radius R by another integer search with quantifier elimination. Express the exact adjoint inequality using positive auxiliary p-th roots for the factorial-ratio finite products; all relevant expressions at fixed reaction shifts are algebraic functions of x. Alternatively use the ideal monomial functional and the certified error bound. The classwise escape proof guarantees that the bad semialgebraic set with x_i≥K is bounded, so this search terminates.

The output is a finite exact bulk certificate (p,K,R and the verified polynomial inequalities). No deterministic permanence barrier, stationary law, or recurrence hypothesis is queried.

Costs are NOT controlled: p, phase alphabets, quantifier-elimination degrees, coefficient sizes and R may be enormous. This is not a polynomial-time synthesis theorem or a practical physical compiler. For noncomputable real rate inputs, no effective acquisition claim is made.
