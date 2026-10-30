# Next boundary: a bounded trace cost does not control adverse label resets

This is an abstract Markov-chain interface counterexample, NOT a chemical-network recurrence counterexample and NOT a weakly reversible raw input. It identifies a genuine hypothesis that the accepted phase-type compiler has not removed.

For each n, let n labels have types E,F,A. A is absorbing. In regular mode R, each E changes to F at rate1 and each F changes to A at rate1. Enter a face mode L at rate n. In L, each F changes back to E at rate n; return to R at rate n. Start in R with every label E.

The face exit potential is psi=1/n, so -Q_L psi=1, psi<=1, and ingress rate times face potential is n*(1/n)=1. All repeated face occupation is therefore paid by regular occupation. Initial face holds even vanish with n. Each label's regular finite graph has a two-step path to A. Nevertheless the population-forcing conclusion fails if one ignores the adverse face transfers.

Let u(t)=E[number of F labels times 1_R] and v(t)=E[number of F labels times 1_L]. The exact equations, bounding the regular E birth count by n, give

    u' <= n-(n+1)u+n v,
    v' = n u-2n v.

The comparison system is cooperative. Its equilibrium is u*=n/(n/2+1)<=2 and v*=u*/2<=1. Starting from zero, comparison therefore gives u(t)<=2 for every t. Since A births occur at total rate number(F) in mode R,

    P(first A by time t) <= E[number of A births by t]
                         = integral_0^t u(s)ds <=2t.

Consequently no vanishing horizon t_n can force even one A with probability tending to1, let alone acquire the old n-label reset. The nominal two-step regular-graph scale n^-1/2 is invalid despite perfect trace compensation and a bounded face-exit potential.

The missing fact is exactly that internal face motion must preserve the abstract pooled labels, or be governed by a new joint adverse-transfer estimate. Merely adding a finite face Green, a larger moment bound, or individual paths to A does not supply it. In a raw reaction model, D-free internal reactions may also remain enabled while D>0, making unchecked adverse pooled motion an additional issue outside the erased intervals.

Thus the accepted method has advanced from hand-chosen one-hold faces to acquired finite-phase face potentials, but it has not acquired arbitrary changing pools. A consequential next problem would be a joint two-clock forcing certificate for adverse internal transfers, with actual raw weak-reversibility and stoichiometric constraints retained. This abstract example alone proves neither failure nor success of that chemical extension.
