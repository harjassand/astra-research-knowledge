# Product forcing with cumulative adverse budgets instead of pointwise rates

30 October 2026. New local candidate extending the reviewed root product argument; not a raw-network or Green theorem.

## Contract and statement

There are n persistent labels, ranks0,...,L, and a genuine disjoint allocation of per-label progress subgenerators of rate q>0. Each allocated event lowers its designated positive rank by at least1, and any collateral changes are safe. No physical event intensity is counted more than once. All additional safe events decrease ranks. Adverse events touch at most k labels, with predictable per-label participation intensities b_i(t). These intensities may be arbitrarily large and adapted. The exact process is nonexplosive and satisfies localized Dynkin/finite-variation calculus.

Fix T. Assume deterministic initial budgets B_i>=0 satisfy the PATHWISE compensator bounds

    integral_0^T b_i(t)dt <= B_i,   for every i, a.s.

Let a in(0,1), C=(1-a)^(-(k-1)), and g_r(u)=P(Pois(qu)>=r), g_0=1. Then

    E(1-a)^(A_T)
       <= product_i[1-a exp(-C B_i) g_(r_i(0))(T)].    (B)

If every B_i<=B, a=1/2 gives target threshold c n exp(-2^(k-1)B) T^L and lower-tail exponent of that same order on0<T<=1. Realized paths need not be independent. Unlike a pointwise-rate bound, this contract permits arbitrarily intense short bursts, provided their per-label cumulative compensators are truly bounded.

## Exact budget-state proof

Adjoin continuous remaining budgets

    z_i(t)=B_i-integral_0^t b_i(s)ds >=0,
    p_i(t)=exp(-C z_i(t)) g_(r_i(t))(T-t),
    F(t)=product_i(1-a p_i(t)).

For fixed rank, budget consumption contributes C b_i p_i to the derivative of p_i. The backward derivative of g cancels its designated one-step progress contribution exactly. Larger progress drops and safe collateral changes only reduce F. Thus the remaining time/progress drift is at most

    -C F sum_i b_i(t) a p_i/(1-a p_i).

For an adverse event touching set A, the new factors are at most1. The same telescoping product inequality bounds its relative increase by

    C sum_(i in A) a p_i/(1-a p_i).

Summing ACTUAL intensities cancels the budget drift. Therefore F is a bounded nonnegative supermartingale after localization.

At terminal time non-target factors equal1, while target factors equal1-a exp(-C z_i(T)) >=1-a. Hence

    (1-a)^(A_T) <= F(T).

Taking expectations and using F(0) proves (B). The direction of this terminal inequality is essential: unused budget weakens the test but does not invalidate it. No future adaptive rate is conditioned on, and z_i is an adapted finite-variation state, not an anticipatory integral over future intensities.

The ordinary pointwise-bounded theorem is recovered by setting B_i=bT and b_i(t)<=b; unused budget is allowed. If b_i(t)=b, terminal remaining budgets vanish and the original product witness is recovered exactly.

## A priced failure version when budgets are not pathwise bounded

For a common chosen B>0, stop charging a label when its accumulated adverse participation compensator first reaches B. At that predictable exhaustion time, retain it as a virtual label: it subsequently follows independent progress, ignores actual safe/adverse changes, and is counted as lost in comparisons with the physical labels. Surviving labels keep their actual dynamics. Actual adverse events still change at most k virtual labels; their intensities for non-exhausted labels are unchanged, and exhausted labels have zero adverse participation. All virtual labels satisfy the pathwise budget B. Persistent physical identities can be retained even after their comparison is lost.

Let J_T be the number exhausted and A_T^virtual the virtual target count. Pathwise,

    A_T^actual >= A_T^virtual-J_T.

With p=exp(-2^(k-1)B)g_L(T), root Markov algebra therefore gives

    P(A_T^actual<=n p/8)
       <=exp(-n p/4)+P(J_T>=n p/8),                 (F)

with harmless adjustments for integer thresholds. Every exhausted label has spent budget B, so

    B J_T <= sum_i integral_0^T b_i^actual(t)dt.

A bound on this total compensator can price the last term, but it must actually be strong enough at threshold B n p. Mere expected occupation/ingress control does not automatically achieve that. For example an O(nT) expectation is not smaller than the desired nT^L target scale for L>1. Thus this is a precise receiving interface, not a declaration that an old time-only face potential suffices.

## Scope

The theorem replaces an instantaneous per-label rate bound by a stronger-than-mean cumulative budget contract, retaining bounded batch size and exact progress allocation. It can be useful when face activity is bursty but its integrated adverse exposure is certified. It neither earns those exposure bounds from a raw network nor removes extinction, physical-time, signed-cycle or replenishment obligations. The finite-budget and priced-failure claims are local deterministic-horizon statements only.
