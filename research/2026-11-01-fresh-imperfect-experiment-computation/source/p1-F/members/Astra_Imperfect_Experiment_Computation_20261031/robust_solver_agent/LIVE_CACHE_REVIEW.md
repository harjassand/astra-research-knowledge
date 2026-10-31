# Review of the root's live-source Galerkin cache construction

This review checks the mathematical proposal communicated by the root; it does
not claim to have reviewed the eventual implementation or all later revisions.

## Contract checked

For a fixed Hermitian `B`, later tasks solve `(alpha I+B)x=b`, with a known
uniform lower bound `alpha I+B >= mu I`. Let `U` be the retained orthonormal
image basis and `V` an orthonormal basis of `span(U,b)`. Cached/source actions
form `Y` with `||Y-BV||<=sigma<mu`. Form

\[
H=\alpha I+\operatorname{sym}(V^*Y),\quad
Hz=V^*b,\quad x=Vz,
\quad\widehat r=b-\alpha x-Yz.
\]

The reduced matrix is positive definite because
`H >= (mu-sigma)I`. With `tau=mu epsilon/(1+epsilon)`, accept if

\[
\|\widehat r\|+\sigma\|x\|\le\tau\|x\|.
\]

Otherwise append the normalized residual of `y=Yz/||x||` outside `U`, provided
`b!=0`; the zero-load case is solved immediately.

## Checks that pass

The true residual differs from `rhat` by at most `sigma||x||`. Acceptance implies
`||x-xstar|| <= (tau/mu)||x||` and hence
`||x-xstar||/||xstar|| <= tau/(mu-tau)=epsilon`.

The small Galerkin equation implies

\[
V^*\widehat r=
\left[\operatorname{sym}(V^*Y)-V^*Y\right]z,
\qquad \|V^*\widehat r\|\le\sigma\|x\|.
\]

The projected true compression is Hermitian, so the skew part here comes only
from the permitted action error. A failed acceptance test gives

\[
\|(I-P_V)Yz\|>(\tau-2\sigma)\|x\|.
\]

Since `range(U)` is contained in `range(V)`, the same lower bound holds for
the residual of `y` outside `U`. Thus if `g=tau-2sigma>0`, every enrichment
normalizes a vector of size at least `g`. Tiny source noise cannot create
unbounded spurious QR directions in this construction.

Each accepted raw image has the form `y=Bv+e`, where `||v||=1`, `||e||<=sigma`.
Its norm is at most `M=L+sigma` if `||B||<=L`. If all relevant `Bv` are within
`eta` of one (unknown and unsupplied) `r`-dimensional subspace, then the noisy
raw images are within `h=eta+sigma` of that subspace.

For `m` accepted raw images, with `m>r`, the QR pivots are at least `g` and a
rank/tail determinant bound gives

\[
g^{2m}\le
\left(\frac{mM^2}{r}\right)^r
\left(\frac{mh^2}{m-r}\right)^{m-r}.
\]

If `h<=g/2` and `m>=2r`, let `t=m/r`. Then
`t-1 <= log_2(t)+2 log_2(M/g)`. For `t>=4`, `log_2(t)<=t/2`; consequently

\[
m\le r\max\{4,\;2+4\log_2(M/g)\}.
\]

When `r=0`, `||y||<=h<g` already precludes an enrichment. The statement must
also handle the trivial `m<=r` regime and the ambient cap `m<=n`.

## Implementation issue that must be handled

As `U` grows during one solve, the normalized temporary direction
`b_perp/||b_perp||`, where `b_perp=(I-P_U)b`, changes. Computing its source image
from a previously noisy `Bb` by subtraction and division can amplify error
without bound as `||b_perp||` becomes small. Requery that currently normalized
direction after each enrichment, or propagate the transformed errors rigorously.

Requerying is straightforward and only adds at most one source action per
enrichment, plus one per later task. Querying every newly retained basis vector
and refreshing prior columns at dimension-doubling points still gives
`O(R+T)` actions over `T` tasks and `R` enrichments. At cap `D`, each column
needs tolerance at most `sigma/sqrt(D)` (with constants for the extra temporary
column) to obtain a deterministic spectral-norm error `sigma` on the stack.
For a tolerance-squared cost, this gives the advertised order
`(R^2+TR)/sigma^2`. Vector-reading, QR, small-system solves, and finite-precision
certification costs remain additional charges.

## Primary conventional comparisons

The determinant inequality is established machinery. DeVore, Petrova and
Wojtaszczyk, **Greedy Algorithms for Reduced Bases in Banach Spaces**, Lemma
2.1, proves the triangular-matrix projection/AM--GM inequality directly:
https://people.tamu.edu/~gpetrova/DPW_submission.pdf . Their subsequent theorem
uses weak maximization over a family. The root's task-triggered sequence does
not require that maximization oracle, but the determinant step itself should
be credited to the existing lemma.

Binev, Cohen, Dahmen, DeVore, Petrova and Wojtaszczyk, **Convergence Rates for
Greedy Algorithms in Reduced Basis Methods**, section 3.3 and Theorems 3.4--3.5,
already analyze bounded-error snapshots and prove approximation rates down to
a noise floor. Their route still assumes weak selection over the family and
access to approximate snapshots. Primary author PDF:
https://people.tamu.edu/~gpetrova/BCDDPW_10.pdf .

Parks, de Sturler, Mackey, Johnson and Maiti, **Recycling Krylov Subspaces for
Sequences of Linear Systems**, SIAM J. Sci. Comput. 28(5), 1651--1674 (2006),
DOI 10.1137/040607277, already provides methods that acquire and continually
improve retained subspaces while solving sequences with changing matrices and
loads. Primary institutional PDF:
https://vtechworks.lib.vt.edu/bitstreams/00c3845d-2805-4731-b2da-53456a824b5a/download .

Thus 'noise-tolerant basis acquisition' and 'reusing previous solves' should
not be claimed as new. The precise possible contribution is the combined
task-triggered source-action, source-precision, and lifetime-enrichment theorem,
with actual source-based residual certification and no supplied snapshot solver.
Originality and superiority over the strongest practical recycling methods
remain unestablished.
