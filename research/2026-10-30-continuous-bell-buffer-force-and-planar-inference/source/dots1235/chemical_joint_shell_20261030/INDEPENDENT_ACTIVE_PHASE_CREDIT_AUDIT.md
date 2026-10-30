# Independent audit: active-phase credit trace

Reviewed 2026-10-30. Source: `ACTIVE_PHASE_CREDIT_TRACE_CANDIDATE.md`.

**Core verdict: the capped trace and stopped-cost construction pass.** Constants may depend on the fixed dimension, fast graph, and positive rates; no dimension-uniform complexity or global recurrence conclusion is established. A degenerate singleton/no-outgoing-edge contract case was flagged for clarification below.

## 1. Indicator and connector increments

Interpret I as enabling of a composition complex, separately from its common 4B catalyst. In the large-r domain B>=4 automatically. If a fast edge is enabled at x=z+y, its target is z+y'. A complex return path to y is enabled with the same nonnegative residual z, so the target has an enabled fast outgoing edge. Hence no fast jump can leave the active set; an inactive state cannot initiate a fast jump. This proves exact invariance, not an average statement.

Adding A cannot disable any composition source. Since 3A is a fast source, activation from an inactive state with A>=1 ends active. Since every pure 3X_i is a fast source, I=0 implies every X_i<=2 and N<=2d. Clearing starts with A>=3 and therefore I=1. Direct subtraction in r=B-N-I gives precisely the stated increments: immigration 0 or -1, inactive activation 0, active activation +1, and clearing -1 or 0 depending on target activity.

For d>=2, strong connectivity and the distinct pure complexes guarantee the required outgoing sources. If d=1 and the graph is a singleton with no edge, strong connectivity is vacuous but I is always zero; the claimed predicate properties would fail. Require a nontrivial/outgoing-edge condition or explicitly restrict to d>=2. This is a contract edge case, not a failure for the intended multidimensional graphs.

## 2. Active absorption without a mixing assumption

From any active state choose an enabled cubic complex and follow a fixed-length complex path to 3A, then clear. The same composition residual keeps every path reaction enabled. Normalized total rates are O((1+N)^3), desired enabled rates have a fixed positive lower bound, and path length is bounded only by the finite graph. Thus bounded-jump block attempts give the stated polynomial absorption bound uniformly over active states, including separate residue classes. Fast invariance ensures all surviving intermediate states remain in the set to which the bound applies.

On the logarithmic cap, competing birth intensity is <=C(1+N)B while clearing/fast dynamics have the common (B)_4 scale. The stopping-time/hazard estimate therefore gives r^{-3+o(1)} probability of a birth before clearing and r^{-4+o(1)} mean stopped duration, uniformly in active composition. This is valid for any fixed p>0 because every fixed power of log r is subpolynomial.

If N>2d+3, clearing leaves N-3>2d and thus necessarily leaves I=1. Its residual jump is therefore down. This establishes the claimed direct downward alternative throughout the large composition tail.

## 3. Bounded-head block protocol

An inactive A>=1 state has A in {1,2}, so activation beats immigration with probability at least 1-C/r. Activation is neutral and creates activity. Clearing before the next birth succeeds with probability 1-O(r^-3) on this bounded head. If its target is inactive, total N after the activation/clearing pair has decreased by exactly one, irrespective of the fast path or final composition. Therefore at most 2d such successful pairs either produce a down exit or reach an inactive A=0 state. Starting active in N<=2d+3, the first successful clearing either exits down or enters an inactive N<=2d state.

At inactive A=0 only immigration is enabled. After it, if activity has not turned on, A=1; a second prescribed immigration beats activation with probability at least c/r. If still inactive, A=2; a third prescribed immigration has the same lower bound and must turn activity on because A becomes three. Turning on I by immigration is a downward residual exit. Earlier success only improves the bound. Thus this final protocol succeeds with probability at least c/r^2.

Every failure is correctly handled: a failed prescribed activation is immigration, which is either neutral or already down; a failed prescribed immigration is inactive activation, which is neutral; a competing birth during an active episode is neutral immigration or an up activation. Any cap departure is a stopping event. Thus a nonterminal failed block restarts at exactly the same r. Prescribed bounded-head paths fit inside the cap after fixing a sufficiently large threshold, for example one with L(r)>=2d+5.

There are only a bounded number of active absorption episodes and inactive holding periods in a block. Their conditional mean durations are uniformly bounded. The block up probability is at most r^{-3+o(1)}; its down probability is at least c/r^2 from every capped state, with the large active tail having the stronger near-one down probability.

## 4. Renewal and the stopped value

No independence of blocks is required. Conditional on each surviving block start, the stop probability is at least c/r^2. Hence the expected number of blocks is <=Cr^2. Summing conditional up probabilities gives total first-up probability <=r^{-1+o(1)}, and summing conditional duration bounds gives expected stopping time <=Cr^2. Cap exits can only improve these inequalities.

At fixed r the cap contains finitely many actual states and has finite rates, so its neutral excursion is nonexplosive. The terminal live residual is exactly r+1 or r-1. For every fixed alpha<1 and the displayed slowly varying tilt, the factorial ratio and first-up bound give contraction tending to zero. Multiplying the weight by (1+r)^2 preserves contraction. This proves finite expected stopped running cost, the upper bound C(1+r)^2 phi(r), and finitely many residual excursions before the cap/threshold target. First-jump decomposition gives the actual LW=-phi inside the domain without a recurrence assumption.

## 5. Cap-entry geometry can also be settled

This small additional interface calculation does not solve the higher-dimensional global selection problem. For large integer r, L(r+1)-L(r)<=1. Immigration increases N and weakly decreases r, so cannot enter from above the cap. Inactive activation increases N by two at fixed r; active activation increases N by two while increasing r by only one. Neither can enter. Fast jumps preserve both variables. Thus only clearing can enter at large r.

For clearing, r_target is either r or r-1, while N_target=N-3. Therefore an incoming exterior source necessarily satisfies

    L(r)<N<=L(r)+3.

The target weight is at most a polynomial multiple of phi(r), since the target residual never increases. The positive incoming forcing is consequently polynomial(r) phi(r). On this collar B-r=N+I>=N, giving the same factorial separation as before whenever an appropriate quantitative outer certificate is available. Threshold entry requires bounded target residual and capped N, so has finite support.

## Scope

The credit predicate eliminates the inactive-hole first-up obstruction structurally, without enumerating a finite-head matrix. The dimension-dependent head protocol is proved directly. It does not establish the missing global d>=3 entropy/interface comparison, nor does a valid cap-entry bound supply the required outer certificate automatically.

### Current-contract verification

The current cubic source explicitly assumes d>=2 and includes the actual cap-entry calculation. This resolves the degenerate singleton qualification and incorporates the interface bookkeeping above. Final verdict on the amended local trace: **pass**, with the higher-dimensional global gluing obstruction unchanged.

Reviewed source hash:
e8013d843c10bd0a531a4a4c0ced85ce9219464bba6564a2b3aaee9ca30c3071  chemical_joint_shell_20261030/ACTIVE_PHASE_CREDIT_TRACE_CANDIDATE.md
