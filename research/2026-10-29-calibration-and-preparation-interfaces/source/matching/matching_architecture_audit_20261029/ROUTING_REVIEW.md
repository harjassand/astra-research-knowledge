# Independent review of random-matching routing lower bound
2026-10-29. Scope: producer-workspace/ROUTING_BOUND.md and check_routing.py/.json as read this date.

Accepted at the stated pure-unitary, fixed one-dimensional nearest-neighbour preparation interface. No additional entanglement/routing resources or measurements are implicitly granted.

I checked the proof independently: exact matching state cut entropy equals crossing-pair count; its expectation is j(n-j)/(n-1). A crossing two-qubit unitary changes cut entropy by at most two bits, by writing the entropy difference as a conditional entropy difference of the one boundary qubit given the unchanged left remainder. Summing gate counts over cuts counts each nearest-neighbour gate once. The identity sum_j j(n-j)/(n-1)=n(n+1)/6 gives expected G>=n(n+1)/12. The middle-cut argument gives expected depth>=n^2/[8(n-1)], since at most one gate per layer crosses that cut. These are lower bounds, not necessarily sharp constants.

For per-matching trace-distance eta approximation, reduced-state contractivity and finite-dimensional entropy continuity give S_actual>=X_j-eta min(j,n-j)-h2(eta). Sum_j min(j,n-j)=n^2/4 for even n yields precisely the reported subtraction eta n^2/8+(n-1)h2(eta)/2. The output remains pure and unitary-produced as required. Mixed outputs/preshared entanglement/measurement-mediated links are not covered.

The uniform-matching distribution TV error produces at most that TV error in a bounded binary test mean; hence the additive C eta witness allowance is correct. Unbiased rejection sampling's worst-case random-bit count is unbounded; a cap must be separately charged as stated.

Re-executed check_routing.py and compared parsed JSON with the saved data: all 100 exact rational identities match. No theorem correction required. This does not establish superiority of the matching architecture over a same-layout Schur or logical-design implementation.
