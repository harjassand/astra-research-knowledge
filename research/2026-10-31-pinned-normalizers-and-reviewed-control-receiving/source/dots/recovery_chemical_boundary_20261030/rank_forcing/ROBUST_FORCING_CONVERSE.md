# Rank acquisition has an exact robust-forcing converse

30 October 2026. New abstract theorem candidate, not independently reviewed. It does NOT claim necessity for a fixed raw reaction network.

## Contract and conclusion

Fix a finite type set I, target a, fixed finite baseline rates q_ij>=0, and an allowed excess-edge graph E. The excess controller may assign ANY nonnegative adapted rates supported on E, including zero; require only a nonexplosive resulting process. For each fixed t>0 ask whether

    inf_{initial type i, admissible excess controls} P_i(X_t=a) >0.    (U)

The rank criterion in ROOT_RANK_MONOTONE_COHORT is sufficient, with its explicit c t^L lower bound for 0<t<=1. Conversely, if that rank finder rejects, (U) fails for EVERY fixed t>0. Constant finite-rate controls already witness the failure. Thus the finite rank finder is complete for this robust terminal-forcing interface, not just for the syntax of integer ranks.

## 1. An excess edge leaving a destroys uniform endpoint forcing

If E contains a->j with j!=a, give that edge rate K and all other excess edges rate zero. Put Qmax=max_i sum_{j!=i}q_ij. For p(t)=P(X_t=a),

    p'(t) <= Qmax-K p(t),
    p(t) <= exp(-Kt)p(0)+Qmax/K.

For any fixed t>0 the right side tends to zero as K tends to infinity. This is an ENDPOINT/retention obstruction; it is not a claim that first hitting a is unlikely when starting at a.

## 2. A failed pruning round supplies a fast-reset policy

Otherwise run the layer/pruning finder. Suppose it stops with a proper processed set S containing a. Write R=I\S and

    E0={i in R: some positive baseline edge i->S},
    Z=R\E0.

The final pruning deletes every member of E0. When deleting a node, record an allowed excess edge to a node already removed or in Z; such an edge exists by the deletion rule. Its target stays in R. This gives a chosen directed path from every i in E0 to Z, of length at most k=|I|. Assign an integer path potential d=0 on Z and d(i)=1+d(parent(i)) on E0. In particular d<=k and every chosen excess edge decreases d by exactly one. Z is nonempty whenever E0 is nonempty and a whole pruning round fails.

Use the constant control that gives each chosen edge rate K and every other excess edge rate zero. Stop at the first entry sigma into S. Extend d by zero on S. On R,

    L d <= -K 1_E0 + k Qmax.

Dynkin's formula on this finite stopped chain gives

    K E_i integral_0^(t wedge sigma) 1_E0(X_s)ds
        <= d(i)+k Qmax t <= k(1+Qmax t).

Only baseline edges from E0 can enter S; the selected excess edges stay in R and Z has no baseline edge into S. The actual first-entry compensator therefore gives

    P_i(sigma<=t) <= Qmax E_i integral_0^(t wedge sigma)1_E0 ds
                   <= k Qmax(1+Qmax t)/K.                    (C)

For every initial i in R, P_i(X_t=a)<=P_i(sigma<=t), so taking K to infinity proves failure of (U). If E0 is empty, S is inaccessible from R with all extras off and the conclusion is immediate.

Every constructed control is a finite-state chain with finite rates, so the counterexample does not rely on explosion, an inadmissible infinite-rate limit process, or future-dependent controls. The limit is taken only in its finite-K probabilities.

## 3. Exact simple witness

For baseline 2->1->a at unit rates and excess 1->2, the finder stops at S={a}; E0={1}, Z={2}. Give the excess rate K. The exact mean absorption times are t_2=K+2 and t_1=K+1, while (C) proves the required fixed-time probability tends to zero. Large mean alone would not prove the latter, so the compensator bound remains the argument.

## 4. What this does and does not settle

A successful rank finder now has a matching abstract rejection witness: either a fast departure from a, or a finite fast-reset policy trapped outside a. This can guide a compiler's stopping decision for an unbounded-adversarial-excess interface.

Raw chemical excess intensities are FIXED functions of the actual population and cannot in general be independently turned off or scaled to arbitrary K. Therefore rank rejection is still NOT a recurrence/transience verdict, NOT a necessary condition for raw-network stability, and NOT evidence that the network realizes this adversarial policy. It is a precise proof that baseline reachability plus the support graph alone cannot give a uniform forcing theorem against all such controls. More information about actual rates, occupations or stoichiometry is needed to go beyond the rank class.
