# Mixed sparse/low-rank acquisition: focused prior-art comparison

## Verdict

The initial regime `r = n^{o(1)}`, `M = n^{1+o(1)}` is already reachable by a strong existing binary matrix approximation algorithm, followed by the elementary alternating-core repair below. It should not be presented as a new acquisition regime by itself.

The strengthened construction using deletion of short codewords has a materially larger proved parameter regime: `r=o(n)` and `rM=o(n^2)`, with near-linear residual/factor count. For `M=Theta(n)` it accommodates every `r=o(n)`. The closest exact algorithm located in this focused audit has exponent `O(r sqrt(M log(rM)))`; it does not imply this whole regime. The new algorithm returns an adequate decomposition after deleting a small set of variables, while that prior algorithm solves the stronger full-matrix rank-editing problem. These are different output guarantees. No universal novelty or lower-bound claim follows from this comparison.

## Exact prior result and its parameter translation

Fomin, Golovach and Panolan, *Parameterized low-rank binary matrix approximation*, Data Mining and Knowledge Discovery **34**, 478–532 (2020), Theorem 6, solves the following problem: given an `a` by `b` binary matrix, find a matrix of GF(2)-rank at most `r` with at most `k` changed **entries**, or determine that none exists. Its time is

`2^{O(r sqrt(k log(rk)))} ab`.

The radical includes the logarithm. Section 5.2 states that the decision algorithm can be modified to produce a solution; its kernel has at most `(r+1)(k+1)` rows and columns. This improves the older ICALP 2018/arXiv-v1 exponent. The output is not required to be symmetric or alternating. With `k=2M`, it applies to a promised alternating matrix `B=A+S`, where `rank(A)<=r` and `S` has at most `M` unordered edges.

Primary full text: <https://fedorvf.github.io/articles/2020/2020f.pdf>, printed pages 513–516, Theorem 6 and Lemma 8. DOI: <https://doi.org/10.1007/s10618-019-00669-5>.

## An elementary repair makes this a genuine counting competitor

This section is a derivation for this audit, not a theorem attributed to the cited paper. All ranks and sums are over GF(2). Suppose the prior algorithm returns `X` of rank at most `r` with `wt(B+X)<=2M`. There is a polynomial-time procedure producing a vertex set `E` of size `O(sqrt(rM)+r)` such that `X[R,R]`, for `R=[n]\E`, is alternating of rank at most `r`, and `B[R,R]+X[R,R]` has at most `M` unordered edges.

### 1. Make the output symmetric

The known matrix `D=X+X^T` is alternating, has rank at most `2r`, and has at most `2M` unordered edges: every asymmetric pair in `X` requires at least one error relative to the symmetric `B`.

Choose an integer `Delta>=1`. Remove the vertices `H` of degree greater than `Delta` in the support graph of `D`; then `|H|<=4M/(Delta+1)`. Let `L=[n]\H`, and choose a row basis of `D[L,L]`. Each basis row has at most `Delta` nonzero entries. Let `J` be the union of these supports, so `|J|<=2r Delta`.

Every nonzero column of `D[L,L]` has a nonzero coordinate in some basis row: otherwise all rows would vanish in that column. Consequently `D[L\J,L\J]=0`. Thus `X` is symmetric outside `E0=H union J`, and

`|E0| <= 4M/(Delta+1) + 2r Delta`.

Choosing `Delta=max(1,ceil(sqrt(2M/max(r,1))))` yields the asserted order. The cases `M=0` or `r=0` can be handled directly.

### 2. Remove the remaining nonzero diagonal

Restrict first to `L0=[n]\E0`. Now `Y=(X+A)[L0,L0]` is **symmetric**, has rank at most `2r`, and has at most `4M` nonzero entries. Let `T` be its nonzero diagonal set, which is also the known nonzero diagonal set of `X[L0,L0]`.

For a symmetric binary matrix `Y`, the following useful inequality holds:

`|{i:Y_ii=1}|^2 <= rank(Y) wt(Y)`.

To prove it, form the simple graph on its nonzero diagonal positions, placing an edge where `Y_ij=1`. An independent set induces an identity principal submatrix, and hence has size at most `rank(Y)`. The elementary independent-set bound `alpha >= v^2/(2e+v)` gives the inequality because `2e+v` counts the nonzero entries in this principal submatrix. Therefore `|T|<=sqrt(8rM)`.

Delete `T` as well. The retained approximation is symmetric with zero diagonal. Its remaining entry errors occur in symmetric pairs, so at most `M` unordered edges remain. This procedure needs no knowledge of the promised `A`: that matrix is used only to prove the bound on `|T|`.

**Precision:** the sharper `sqrt(8rM)` diagonal bound is applied *after* the symmetry deletion. Globally `X+A` need not be symmetric.

### 3. Resulting comparison with phase counting

Branching on `E`, expanding the rank-`r` quadratic phase into its Walsh support, and invoking the near-linear local-phase counter gives an adequate prior-based competitor whenever

`r sqrt(M log(rM)) = o(n)`, `r=o(n)`, and the local/residual factor count is `n^{1+o(1)}`.

The extra branch and Walsh costs are `2^{O(sqrt(rM)+r)}` and `2^r`, respectively. In particular, the original `r=n^{o(1)}`, `M=n^{1+o(1)}` case follows. For `M=Theta(n)`, the displayed exact acquisition bound guarantees subexponential time when `r=o(sqrt(n/log n))`; it does not cover all sublinear ranks.

## Other primary comparators checked

* Fomin, Lokshtanov, Meesum, Saurabh and Zehavi, *Matrix Rigidity from the Viewpoint of Parameterized Complexity*, SIAM J. Discrete Math. **32** (2018), Section 5, gives `2^{O(f(r,p) sqrt(k log k))}` for finite fields. Its construction enumerates reduced patterns with up to `p^r` distinct rows and columns. It does not supply the desired near-linear growing-r guarantee. Full primary text: <https://sites.cs.ucsb.edu/~daniello/papers/rigiditySIDMA18.pdf>.
* Velingker, Votsch, Woodruff and Zhou, ICML 2023, Section 3, gives a randomized GF(2) bicriteria `(1+epsilon)` approximation in `2^{poly(r/epsilon)} poly(n)` time, with output rank `O(r log(n)/epsilon)`. The approximation is in the **decomposition's entry error**, which is allowed to be corrected exactly in our counting application. Thus dismissing it merely because it says “approximation” would be incorrect. Nevertheless, its stated rank and running-time dependencies do not imply the full `r=o(n)` regime. Primary paper: <https://proceedings.mlr.press/v202/velingker23a/velingker23a.pdf>.

The older graph-rank-editing work of Meesum–Misra–Saurabh (TCS 2016) is relevant ancestry. The full original proof and its growing-r constants were not recovered in this focused pass, so no precise coverage claim here relies on it.

## Why the strengthened puncturing construction is different

For the correct candidate clean-column span `C`, every true remaining column lies in `C` and every observed column has at most `Delta` errors. Repeatedly deleting the support of a nonzero codeword of weight at most `2Delta` lowers the dimension on every iteration. It costs at most `2r Delta` additional deleted coordinates, found by streaming `2^dim(C)` codewords. The final punctured code has distance greater than `2Delta`; radius-`Delta` decoding is therefore unique. Symmetry, zero diagonal, rank and residual weight can all be checked on the returned matrix, including on incorrect candidates.

This avoids enumerating `2^{Theta(r^2)}` possible inner alternating forms. The published comparators above do not state this weaker retained-core reconstruction result with its stronger parameter dependence. Enumeration must use **unordered subsets** for both basis indices and initially deleted coordinates to obtain the entropy bounds `r log(en/r)` and `s0 log(en/s0)`, rather than the weaker `r log n` bound.

This audit supports describing the contribution as a constructive retained-core compiler and its exact-counting consequence, with the full matrix-editing comparator explicitly stated. It does not establish optimality, practical speed, or first priority.

## Executed finite checks

`mixed_interface_prior_checks.py` uses only Python's standard library. Executed successfully: 1,098 symmetric diagonal inequalities; 285 threshold/row-basis support covers; and 11,009 exhaustive promised alternating-core repairs on dimensions at most three, including 7,331 retaining a nonempty core. The output is `mixed_interface_prior_results.json`.

These checks exercise the elementary repair above. They do not execute the Fomin–Golovach–Panolan algorithm or benchmark the asymptotic phase counter.
