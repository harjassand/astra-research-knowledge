# Specified branching lower bound and a polynomial direct certificate

These claims come from the [complete returned response](P2_FIRST_FAILURE_OBJECT_TRANSFER_20261106_RETURN.txt) and [full supplied report](package/RESEARCH_REPORT.txt), without a new Capital proof check.

For odd`n=2m+1≥3`, let`S=Σx_i`, `W=n(n+1)/2`, `A=W+1` and

`E_n=A(2S−n)²+Σ_i i x_i`.

Its coefficients are `c=An²`, `a_i=4A(1−n)+i`, `b_ij=8A`. They have magnitude≤`n⁴`, `O(log n)` bits, no auxiliaries and complete indexed input length `L_n=Θ(n² log n)`. The unique minimiser selects the first`m` indices, with `E*=A+m(m+1)/2`. Oddness makes the squared term at least1; moving away from the two middle cardinalities costs more than the entire linear variation, and the ordered weights select the unique cheaper assignment. The family is easy by another method.

The tested tree fixes original coordinates. At each node its lower bound is the first Boolean moment PSD relaxation with means`μ`, moments`Y`, `Y_ii=μ_i`, `0≤μ_i≤1`, and nonnegative pair probabilities `Y_ij`, `μ_i−Y_ij`, `μ_j−Y_ij`, `1−μ_i−μ_j+Y_ij`. A node terminates only if this bound, optionally rounded upward to an integer, reaches the feasible incumbent, or all variables are fixed. Otherwise it branches on a free coordinate. Variable selection and node order may be arbitrary/adaptive. Even the true optimum assignment/value is granted as a **feasible incumbent**, without supplying its optimality as an accepted proof.

At a node with`p<m` fixed ones and`q<m` fixed zeros, write`f=n−p−q` and`r=n/2−p`. The feasible formal moments on free bits are `μ=r/f`, `ν=r(r−1)/[f(f−1)]`. Pair probabilities are nonnegative; the covariance has all-ones eigenvalue0 and orthogonal eigenvalue`r(f−r)/[f(f−1)]>0`. Extended by fixed coordinates, these are valid PSD/pair-local moments, **not a joint distribution**. They assign total cardinality mean`n/2` and variance0, giving zero penalty and a linear value≤`W=A−1<E*`. Integer ceiling cannot close that gap. Their numerators/denominators have `O(log n)` bits, so numerical accuracy is not the missing ingredient.

Every path must therefore reach at least`m` fixed ones or`m` fixed zeros. The first-boundary recurrence gives the exact forced frontier

`T(0,0)=2 binom(2m−1,m)=Θ(2^n/√n)`.

It is independent of adaptive coordinate choice and superpolynomial in complete`L_n`. The lower bound targets this **proof tree**, not arbitrary branching/cuts/preprocessing, shared proof DAGs, aggregate disjunctions or all exact optimisers. Further branches after that frontier may still be needed. The original output request does not require this certificate route.

A direct identity bypasses the tree. With `t=S−m`, the source gives

`4(E_n−E*)=(16A−n)t(t−1)+nt(t+1)+2Σ_(i≤m)(n−2i)(1−x_i)+2Σ_(i>m)(2i−n)x_i`.

Integer` t` makes both consecutive products nonnegative; all other coefficients/literals are nonnegative. Every term vanishes at the stated minimiser, and the literal terms enforce uniqueness. The certificate has`O(n)` terms and short aggregate/`O(log n)` coefficients. For this particular ordered family, recognition, minimiser/value construction and identity verification have the reported conservative bound `O(L+n⁴ log²(n+2))` under sequential access/schoolbook arithmetic. That is a family-specific algorithm, not the general QUBO solver. Consecutive-integer/hypermetric correlation inequalities are established prior machinery, not a new universal method.

The main response/report use the explicit frontier count and `Θ(2^n/√n)`. One available activity sentence instead writes `Θ(2^n/n)`. Both supplied sources are retained verbatim; this guide follows the main explicit count and does not silently rewrite the activity or claim a new Capital asymptotic verification.

The incoming Gibbs trap is retained separately. Its heat-bath convergence failure is irrelevant as an unrestricted optimisation lower bound because its minimum is immediate. Neither the tree obstruction nor its direct integer bypass proves that the scientific transfer caused a general constructive advance.
