# Exact killed-face operator: a dimension-independent fact and its open assembly step

Status: internally derived candidate, not independently reviewed. No recurrence theorem claimed.

Discard null reactions y→y, which do not change the generator or connectivity. Let a finite reaction graph be strongly connected and let w be a strictly positive integer vector. Let F be its proper exposed face of complexes maximizing w·y. Retain only reactions with source in F, and kill the process at its first reaction with target outside F. Internal reactions conserve w·x=N. Remove states enabling no source complex in F. The remaining active shell is finite; every internal transition remains active since its target complex is enabled after firing.

Let L be at most the number of complexes: from any enabled y in F there is a simple directed graph path to outside F of length≤L, whose earlier complexes lie in F. If x=z+y initially, following this path gives states z+y_i; nonnegativity and enabling are exact, even on population boundaries. Every path rate is at least kappa_min, since every nonzero falling factorial is a positive integer. On shell N all rates are at most C(1+N)^D, where D is maximum molecularity and C depends only on the fixed graph, rates and w. Consequently every active state has probability at least

    p_N=[kappa_min/(C(1+N)^D)]^L

of being killed within the next L embedded jumps. By the Markov property, survival beyond kL jumps is at most(1−p_N)^k. Expected jumps≤L/p_N; expected physical absorption time≤L/(kappa_min p_N). Thus the killed finite generator Q_N is transient and

    ||(−Q_N)^−1||_infinity ≤ L/(kappa_min p_N).

This is a polynomial bound in shell size N without a spectral-gap, stationary-background, irreducibility-of-shell, or averaging assumption. It is valid with arbitrarily many species, non-simplicial faces and nontrivial residual lattices; inactive shell states must not be silently included. For multiple linkage classes it applies only to face-active linkage components having a path to an off-face complex. Entire linkages contained in the face produce genuinely neutral blocks.

For any positive shell forcing f_N, v_N=(−Q_N^T)^−1 f_N is positive, and sum v_N≤[L/(kappa_min p_N)]sum f_N. This is a real exact dual replacement for a frozen infinite-background stationary law.

## Why this is not a proof of recurrence
Q_N omits reactions sourced below the exposed face. Those reactions can dominate at boundary strata where top-face sources are disabled or only weakly enabled. They couple different shells and add incoming terms in the adjoint. The polynomial resolvent norm alone neither bounds neighboring-shell pointwise ratios nor proves that the resulting correction operator is contractive. An arbitrary rapidly decaying shell forcing does not solve the issue: very small local v_N can receive positive mass from adjacent-shell reactions. Inactive face states must also be treated by other faces, with exact selector/integrability control.

Thus a complete construction needs a uniform inter-shell comparison or a weighted positive-operator contraction built from the original graph, including all boundary faces. Assuming that comparison would supply the missing stability capability. The bound above isolates a piece available for free from weak reversibility; it does not supply the missing assembly theorem.
