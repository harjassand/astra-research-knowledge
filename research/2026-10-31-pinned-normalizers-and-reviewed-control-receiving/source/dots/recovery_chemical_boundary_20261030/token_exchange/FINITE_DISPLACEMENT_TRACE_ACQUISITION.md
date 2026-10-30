# Acquiring collective trace bounds from finite-displacement fibers

30 October 2026. New conditional local compiler construction; not reviewed or globally integrated.

The collective forcing theorem suggests a useful generalization of frozen ordinary fibers. The interior ordinary state may MOVE, provided its displacement from entrance lies in a finite phase-indexed set.

## Exact finite displacement test

Suppose a raw residual module has an acquired one-flag finite phase set and a reference phase D, as in RAW_FINITE_CONTROL_REALIZABILITY.md. For every internal edge p->q record its ordinary stoichiometric displacement nu_pq. Acquire vectors delta_p by the equations

    delta_q-delta_p=nu_pq.

Solve by graph traversal and check every edge; parallel edges with different increments reject. For each admitted entrance, initialize its entry displacement and check consistency along all reachable interior paths. Different entrance components can be treated separately. This is a finite exact test. Every path then has ordinary state y+delta_p, where y is its retained entrance configuration. Nonzero-displacement interior cycles reject; they cannot be hidden in a finite matrix.

Actual nonnegativity/enabling constraints must be retained: an edge with insufficient y+delta_p has rate zero. Thus the killed finite phase matrix Q_y uses EXACT mass-action rates at y+delta_p, not formal rates at y. Terminal marks from phase p with ordinary increment nu_l have actual output y+d_l, d_l=delta_p+nu_l. The set of d_l is finite. Retain all terminal outputs, including non-return outputs; do not discard seeds or connector changes.

For a terminal returning to the reference face, assume sum_i d_l,i=0. Its minimal ordinary net replacement batch is k_l=sum_i(-d_l,i)_+. Set k=max_l k_l. At an admitted y, y_i>=(-d_l,i)_+ automatically when that terminal is feasible. Assign each removed type-i identity uniformly without replacement among its y_i labels, then match them to positive output types by a fixed predetermined matching. The aggregate ordinary counts are exact. This relabeling is abstract and does not assert physical histories were independent.

A terminal is safe if a finite transport matching sends every removed identity only to an equal/lower rank output. Otherwise conservatively classify its entire replacement batch as adverse. This decision is a finite bipartite flow check on integer d_l, independent of population y. Zero-displacement outputs do nothing to ordinary labels.

## Terminal-reward supersolutions acquire participation rates

For each source type i let

    g_i(l)=1{terminal l adverse} (-d_l,i)_+.

This is an actual terminal reward (number of affected source-i identities), NOT a holding cost. Seek a nonnegative supersolution V_i(p,y) of the finite Dirichlet inequality

    Q_y V_i(p,y) + sum_l q_l(p,y) g_i(l) <=0.

Q_y has all exit rates in its diagonal and zero exterior values. This is the usual killed reward equation with marked source h_i=sum_l q_l g_i. Localized Dynkin bounds E_p g_i(exit)<=V_i(p,y). Other terminal outputs must have their own retained bookkeeping; if this local interface is applied only to returns, use reward0 there without discarding their probability.

Require the uniform entrance inequality

    sum_e lambda_e(y) V_i(p_e,y) <= b_i y_i.

Then the full traced adverse departure count from type i is <=b_i y_i. Uniform source selection makes each individual type-i label's adverse participation intensity <=b_i (zero if y_i=0). The terminal batch bound k and the maximum b_i satisfy the collective forcing theorem's exact hypotheses, provided the baseline progress and safe components are in the SAME trace clock and the trace is separately nonexplosive.

This route can tolerate arbitrarily many interior transitions and moving ordinary counts: what matters is finite displacement at actual exits plus the terminal reward inequality. Ordinary time/ingress potentials do not imply that inequality. A finite phase inverse computes V for each fixed y, but uniform symbolic bounds still have to be acquired and verified.

## Scope

This construction does not assume the current uncolored protected-particle architecture has a conserved finite flag or finite-displacement fiber. It gives a checkable sufficient raw structural condition, not a general decomposition algorithm. It broadens the local design from frozen fibers to integrable finite displacements without inventing independent realized label histories. No global recurrence, physical-time estimate, active-output condition, or signed-cycle closure follows without its separate certificates.
