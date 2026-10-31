# Independent review: task-triggered noisy Galerkin cache

**Reviewer:** robust-solver collaborator.  **Date:** 31 October 2026.

**Review scope.** This checks the root's communicated mathematical construction,
its source-action and precision accounting, and the closest retrieved primary
comparisons. It does not certify the eventual software, arbitrary future
extensions, scientific novelty, or superiority over established methods.

**Conclusion.** The core theorem is sound under the explicit assumptions below.
The cached-image combination is a valid bounded-error operator action even
though it is correlated with earlier data. The proposed lifetime enrichment
bound follows from a standard determinant lemma. Two operational points need
explicit treatment: refreshing the temporary load direction when the cache
changes, and modifying the enrichment margin if a small load component is
deliberately omitted for finite preparation.

## 1. Assumptions that must remain in the theorem

1. `B` is a fixed Hermitian operator on a finite-dimensional real or complex
   Hilbert space. It does not change adversarially between actions.
2. A source accepts chosen unit vectors and returns full vectors with certified
   norm error at the requested tolerance. Bounded adaptive errors are allowed.
   Any finite preparation, measurement confidence, and rounding required to
   realize the error contract must be charged explicitly.
3. Each later task supplies `alpha,b` and has an established coercivity bound
   `alpha I+B >= mu I`, with `mu>0`. This bound is an input-class premise or an
   independently earned fact; the algorithm does not infer it from a few
   action measurements.
4. For quantitative lifetime bounds, `||B||<=L` and there exists an unknown
   `r`-dimensional subspace `S` approximating all relevant unit-input images
   to error `eta`. Neither `S` nor `r` is needed by the actual algorithm.
5. The action stack on an orthonormal current trial basis satisfies
   `||Y-BV||<=sigma<mu`. The spectral norm, not only separate column norms,
   is the quantity used in the proof.

The existence of `S` is a complexity premise, not a supplied useful basis or
solver. Correctness of accepted solutions holds even when this premise is
false; the low-enrichment conclusion then need not hold. The procedure must not
stop or accept merely because a guessed rank has been reached.

## 2. Reduced solve, acceptance, and enrichment

Let `U` be the retained orthonormal basis. First take the exact-arithmetic
version `range(V)=span(U,b)`, with `V` orthonormal. Define

\[
H=\alpha I+\operatorname{sym}(V^*Y),\quad
Hz=V^*b,\quad x=Vz,
\quad\widehat r=b-\alpha x-Yz.
\]

Since `V^*BV` is Hermitian and `||Y-BV||<=sigma`,

\[
H\succeq(\mu-\sigma)I.
\]

Thus a conventional finite dense Cholesky solve earns the small-system solver;
it is not an oracle. Its arithmetic and conditioning still belong in the cost.
The zero-load task is handled separately by outputting zero. For a nonzero load,
`x` is nonzero because `b` lies in the trial span and `H` is invertible.

Let

\[
\tau=\frac{\mu\epsilon}{1+\epsilon},\qquad
\|\widehat r\|+\sigma\|x\|\le\tau\|x\|
\tag{A}
\]

be the acceptance test. The true residual is
`r=b-(alpha I+B)x=rhat+(Y-BV)z`, so (A) implies
`||r||<=tau||x||`. Consequently

\[
\|x-x_*\|\le\frac\tau\mu\|x\|,
\quad
\|x_*\|\ge(1-\tau/\mu)\|x\|,
\quad
\frac{\|x-x_*\|}{\|x_*\|}\le\epsilon.
\]

No probability or independence assertion is needed for this deterministic
implication. Future loads and shifts may be chosen adaptively.

The reduced equation also yields

\[
V^*\widehat r=
[\operatorname{sym}(V^*Y)-V^*Y]z,
\qquad\|V^*\widehat r\|\le\sigma\|x\|.
\]

If (A) fails, then `||rhat||>(tau-sigma)||x||`. Since `b-alpha x` belongs to
the trial span,

\[
\|(I-P_V)Yz\|>(\tau-2\sigma)\|x\|.
\tag{B}
\]

Because `range(U)` is contained in `range(V)`, the raw vector

\[
y=Yz/\|x\|
\]

has residual outside `U` larger than `g=tau-2sigma`. Appending its normalized
residual is therefore legitimate whenever `g>0`. The rule never normalizes a
residual below that controlled threshold.

### Cached combinations are valid actions, not independent samples

Set `v=Vz/||x||`. Orthogonality of `V` makes `||v||=1`, and

\[
y=Bv+e,\qquad
e=(Y-BV)z/\|x\|,\qquad\|e\|\le\sigma.
\tag{C}
\]

Equation (C) proves that the raw image is a valid approximate action at the
computed vector. A fresh source call at `v` is unnecessary. It would be
incorrect to call this an **independent** source sample: the input and error
are typically strongly dependent on the current cache. Independence is not
used by either the acceptance proof or the deterministic packing argument.

If actual experimental error bounds only hold with specified probabilities,
one must first obtain a joint event over all actual calls (for instance with
an anytime confidence allocation). On that event, the deterministic proof
applies. It is not legitimate to reuse a fixed per-call failure probability
over an unbounded task sequence without charging the resulting risk.

## 3. Lifetime enrichment bound

Every accepted raw image has norm at most `M=L+sigma` and distance at most
`h=eta+sigma` from `S`. The accepted raw images span the same retained space as
their orthogonalized versions. If there are `m` enrichments, the QR pivots of
their `n x m` column matrix are all at least `g`.

For `m>r`, the standard rank/tail determinant inequality gives

\[
g^{2m}\le
\left(\frac{mM^2}{r}\right)^r
\left(\frac{mh^2}{m-r}\right)^{m-r}.
\tag{D}
\]

One proof bounds the product of the leading `r` squared singular values by
their arithmetic mean and does likewise for the trailing values; the squared
trailing sum is at most `m h^2`. The same inequality appears as the triangular
matrix projection lemma cited below.

If `h<=g/2` and `m>=2r`, set `t=m/r`. Divide (D) by `g^(2m)` and use
`m/(m-r)<=2` to get

\[
t-1\le\log_2 t+2\log_2(M/g).
\]

For `t>=4`, `log_2 t<=t/2`, so

\[
R\le r\max\{4,\;2+4\log_2(M/g)\},
\qquad R\le n.
\tag{E}
\]

The `m<=r` and `m<2r` regimes are automatically covered. If `r=0`, the norm
bound `||y||<=h<g` forbids an enrichment. The `M/g` logarithm is meaningful
whenever any enrichment occurs; otherwise `R=0` should be stated separately.

This is a lifetime bound across the whole adaptive task sequence. No maximizer
over a task family or precomputed snapshot solutions are supplied. The theorem
does not assert that every direction has been learned after the final observed
enrichment: a later task can still trigger a remaining allowed enrichment.

## 4. Source count and general precision cost

Let `r_current` denote the current retained dimension. Maintain a power-of-two
capacity `D>=r_current+1`. Measure each retained orthonormal basis vector at
column tolerance `sigma/sqrt(D)` (or an appropriate fixed fraction to reserve
other errors). On a capacity increase, remeasure all old retained columns at
the new tolerance. The action-stack error is at most its Frobenius norm, hence
at most `sigma` for any stack of at most `D` columns.

For each task, query its current normalized temporary load direction

\[
q_b=(I-P_U)b/\|(I-P_U)b\|
\]

when that direction is present. If an enrichment changes `U`, recompute and
query the new temporary direction. Do **not** form it by subtracting noisy
cached `Bb` values and dividing by a possibly tiny norm unless the amplified
error is explicitly controlled.

Across `T` tasks and `R` enrichments:

- Temporary directions require at most `T+R` calls.
- New retained directions require at most `R` calls.
- Old retained-column refreshes at doubling events total less than `2R` calls.

Therefore the safe exact count is at most

\[
Q\le T+4R
\tag{F}
\]

under this explicit schedule. Reusing coincident directions can reduce it.
It is also reasonable to state `O(T+R)` if finite arithmetic or source wrappers
add a bounded number of calls. If several separate primitive operators are
queried, their individual actions must each be charged.

For a whole-vector action at tolerance `delta` costing `delta^(-p)`, `p>0`, the
capacity schedule costs

\[
W=O_p\!\left(\sigma^{-p}\left[
(R+1)^{1+p/2}+T(R+1)^{p/2}\right]\right).
\tag{G}
\]

Reason: new retained queries have capacity `D<=2(r_current+1)` and contribute
the sum of `r_current^(p/2)`; the geometric refresh stages are dominated by
the final `(R+1)^(1+p/2)` term. Each temporary query costs at most a constant
times `sigma^(-p)(R+1)^(p/2)`, and there are at most `T+R` of them. When `p=2`,
this is `O((R^2+TR+T+1)/sigma^2)` up to constant-factor simplifications.

This is not the full arithmetic or physical cost. Reading each full vector,
preparing inputs, orthogonalizing, forming small matrices, solving them, and
writing full output vectors must still be counted. A source law `delta^(-2)`
also requires an experimental/statistical justification; it does not follow
from the deterministic error contract by itself.

## 5. Finite preparation cutoff: required correction

Suppose a very small load component is omitted, so `V` spans `U` but no longer
contains all of `b`. Define `b_miss=b-P_Vb`. Acceptance (A) remains sound if
`rhat` is computed with the full original `b`. But the failed-test calculation
now only yields

\[
\|(I-P_V)Yz\|>
\left(\tau-2\sigma-
\frac{\|b_{\rm miss}\|}{\|x\|}\right)\|x\|.
\tag{H}
\]

The enrichment margin and width condition must use this smaller value, or the
algorithm must explicitly ensure `||b_miss||/||x||<=rho` and set
`g=tau-2sigma-rho`.

A concrete cutoff is available without knowing `x_*`. Let
`K=|alpha|+L+sigma`, so `||H||<=K`. If `||b_miss||<=c||b||` with `c<=1/2`,
then `||P_Vb||>=sqrt(1-c^2)||b||` and

\[
\frac{\|b_{\rm miss}\|}{\|x\|}
\le \frac{cK}{\sqrt{1-c^2}}.
\]

Choosing `c` from the known desired `rho`, for example
`c<=min(1/2,rho/(2K))`, suffices. If the projection is zero, that cutoff cannot
discard a nonzero load because `c<1`. Other input preparation and rounding
errors should enter the stack/residual budgets with similarly explicit slack.

## 6. Full-rank small tails and affine families

The useful regime includes `B=B_0+E` with unknown rank-`r` `B_0` and generic
full-rank `E` satisfying `||E||<=eta`. Take `S=range(B_0)` in the analysis;
it is never supplied to the algorithm. The exact generated algebra may be
full-dimensional, while the numerical image-width premise and (E) remain
useful. This directly avoids the need to decide exact algebraic closure.

For `B(theta)=sum_j theta_j B_j`, a shared-image subspace and uniform bounds
can support the same analysis, provided the actual primitive action errors
satisfy `sum_j |theta_j| sigma_j<=sigma` and primitive image tails satisfy the
corresponding bound. A coefficient bound and uniform coercivity are required.
Querying `k` separate primitives costs `k` actions, not one. If the source itself
physically implements a combined action, that stronger interface must be
specified and charged. This review does not verify any broader family theorem
beyond these direct substitutions.

The mechanism supplies well-posed linear solves. A later convex optimization
claim must specify and cost an actual outer algorithm and its error budgets.
Solving a quadratic is direct; arbitrary planning or arbitrary nonconvex
optimization does not become easy from this learned cache.

## 7. Strongest retrieved overlapping primary work

1. **DeVore--Petrova--Wojtaszczyk, Greedy Algorithms for Reduced Bases in Banach
   Spaces**, Constructive Approximation (2013), Lemma 2.1. The determinant
   inequality used in (D) is explicitly established there. Their weak-greedy
   analysis also compares acquired spaces with Kolmogorov widths. Author PDF:
   https://people.tamu.edu/~gpetrova/DPW_submission.pdf .
2. **Binev--Cohen--Dahmen--DeVore--Petrova--Wojtaszczyk, Convergence Rates for
   Greedy Algorithms in Reduced Basis Methods**, SIAM J. Math. Anal. (2011),
   section 3.3, Theorems 3.4--3.5. Bounded-error snapshots and approximation down
   to a noise floor are already analyzed. Their selection still needs a weak
   family maximizer and access to approximate snapshots. Author PDF:
   https://people.tamu.edu/~gpetrova/BCDDPW_10.pdf .
3. **Parks--de Sturler--Mackey--Johnson--Maiti, Recycling Krylov Subspaces for
   Sequences of Linear Systems**, SIAM J. Sci. Comput. 28(5), 1651--1674 (2006),
   DOI 10.1137/040607277. Acquiring, retaining, and improving subspaces across
   changing systems and loads is established numerical machinery. Institutional
   primary PDF:
   https://vtechworks.lib.vt.edu/bitstreams/00c3845d-2805-4731-b2da-53456a824b5a/download .
4. **Frangella--Tropp--Udell, Randomized Nyström Preconditioning**, SIAM J.
   Matrix Anal. Appl. 44(2), 718--752 (2023), DOI 10.1137/21M1466244. Adaptive
   learned preconditioners controlled by effective dimension are a strong
   competitor. Author PDF:
   https://tropp.caltech.edu/papers/FTU23-Randomized-Nystrom-SIMAX.pdf .

The source-assisted lifetime/precision contract is worth recording carefully,
but the general themes of noisy learned bases, residual certification, reduced
solves, and reuse across tasks are not new. A broad novelty or practical
superiority claim would exceed this review. The root's construction must be
compared with retained/recycling methods, not solely with fresh solves.
