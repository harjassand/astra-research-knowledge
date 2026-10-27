# Acquired, capped Gaussian-mean channels at square-root dimension cost

27 October 2026. This is a constructive general comparator, not a solution
of N687's polylogarithmic dimension target and not a novelty claim. The
positive likelihood mechanism is the Gaussian cloud fluctuation correction
of Chen--Chewi--Lu--Zhang, arXiv:2609.38710v1, Theorem 4.2. Below its relevant
Gaussian specialization is reconstructed with explicit conservative constants,
an everywhere-defined value-only action, actual Brownian-path acquisition,
and a deterministic cap. No source-dependent fitting is performed.

## Theorem and fully specified costs

Let `g=grad F:R^d->R^d` be globally `L`-Lipschitz, `F in C^{1,1}`,
`sigma>0`, and `0<epsilon<=1/4`. Exact whole-vector values of `g`, standard
Gaussian seeds and real arithmetic are available. There is a positive
randomized algorithm whose ideal-real output is within TV `epsilon` of
`N(Eg(G),sigma^2 I)` and whose EVERY-execution source-query count is at most

    1 + A [M + 8 J K].                                  (1)

Put `rho=L/sigma`; the `L=0` case is one query followed by Gaussian noise.
For `L>0`, use the following explicit parameter choices. Ceilings can be
implemented by bounded scalar loops; the logarithms only specify integers.

    p = 2 ceil(log(128/epsilon)/log 16),
    R_p = sqrt(d p)+p,
    M = ceil(256(1+rho^2) R_p),
    alpha = 2rho^2/M,
    K = max(1,ceil(log(64d/epsilon)/log(1/alpha))),
    B = 1/4,
    A = ceil(log_2(64/epsilon)),
    J = ceil(log_2(64A/epsilon)),
    s = epsilon/[32 max(1,rho) sqrt(d)],
    r = s epsilon/[192 max(1,alpha d)].                   (2)

One additional query at zero removes an arbitrary constant offset. It is
optional in exact real arithmetic, but included in (1). All other queries,
including rejected proposals, are included. The leading dimension cost is
`sqrt(d)` up to logarithms, while accuracy costs are logarithmic. The large
displayed constants are for a transparent proof, not practical optimization.

## 1. The acquired homogeneous secant

For a fixed center `c`, smoothing scale `a>0`, radius `r>0`, Gaussian seed
`xi`, and input vector `v != 0`, define

    D(c,a;v,xi)=||v|| [g(c+a xi+r v/||v||)
                       -g(c+a xi-r v/||v||)]/(2r).      (3)

Set its value to zero at `v=0`, while still querying the repeated center
twice. It uses exactly two source values on every execution. Every realized
map, with `c,a,xi` fixed across its different inputs, is odd and positively
homogeneous, satisfies `||D(v)||<=L||v||`, and has Lipschitz constant at most
`sqrt(2)L`.

Proof of the Lipschitz statement: on the unit sphere the secant vector `H(u)`
has norm at most `L` and Lipschitz constant at most `L`. For `b<=a_0`,

    ||a_0 H(u)-b H(w)|| <= L[(a_0-b)+b||u-w||]
      <= L sqrt(1+b/a_0) sqrt[(a_0-b)^2+a_0 b||u-w||^2]
      <= sqrt(2)L ||a_0u-bw||.

The zero case follows by continuity. The map need not be linear.

Let `H_a(c)=D(P_a g)(c)`. Gaussian smoothing gives
`Lip(H_a)<=sqrt(2/pi)L/a`, using one weak derivative of `g` and one Gaussian
density derivative. Integrating the Jacobian along the radius-r line gives
the uniform, all-direction bias bound

    ||E D(c,a;v,xi)-H_a(c)v||
       <= L r/(sqrt(2pi)a) ||v||.                       (4)

Unlike an ordinary secant with endpoints `c +/- rv`, this has a linear
relative error for every input vector, not an error quadratic in its norm.
The fixed-seed joint Lipschitz contract is the reason for this representation.

With two independent Gaussian seeds, compose two such maps at the same
center. The composition is odd, has norm at most `L^2||v||`, Lipschitz
constant at most `2L^2`, and conditional mean within
`2L^2 r/(sqrt(2pi)a)||v||` of `H_a(c)^2v`. Conservativity makes `H_a` symmetric,
so this is exactly the needed covariance product, with no transpose oracle.

## 2. Actual covariance-action acquisition and retained path

For each proposal generate `M` independent Brownian endpoints
`G_i=B_1^i~N(0,I_d)`. The analytical comparison map and actual proposal map are

    Phi^circ=(M sigma)^(-1) sum_i P_s g(G_i),
    Phi_hat=(M sigma)^(-1) sum_i g(G_i).                 (5)

No smoothed value is acquired. Both the pointwise value discrepancy in (5)
and the discrepancy of their means are bounded by `rho s sqrt(d)`.

Given the full Brownian paths only for analysis, write

    H_i(t)=D(P_sqrt(1-t+s^2) g)(B_t^i),
    Sigma=(M^2 sigma^2)^(-1) sum_i integral_0^1 H_i(t)^2 dt.

Then `0<=Sigma<=rho^2 I/M<=alpha I`. To acquire an action, choose independent
`I` uniformly in `1,...,M` and `T` uniformly in `[0,1]`; obtain `B_T^I` as
described next; use the four-value composition of (3) with center `B_T^I`,
scale `sqrt(1-T+s^2)`, and two fresh Gaussian seeds; divide its output by
`M sigma^2`. Denote the resulting random map by `S_hat`.

For every fixed set of its seeds and path anchor, `S_hat` is odd,
`Lip(S_hat)<=alpha`, and `||S_hat(v)||<=alpha||v||`. Conditional on the full
paths,

    ||E S_hat(v)-Sigma v|| <= eta alpha||v||,
    eta=r/(sqrt(2pi)s)<=r/s.                            (6)

It uses four values per input. Two evaluations of the SAME random map at
different vectors reuse `I,T`, the path anchor and both smoothing seeds.
They cost eight values. Fresh random maps use fresh action seeds conditional
on the same retained Brownian paths.

No Brownian-path oracle is assumed. Initially retain `(0,0),(1,G_i)` for each
path. When a new time `T` is requested, find its nearest retained neighbors
`a<T<b` on that path and draw a Gaussian bridge with mean and variance

    ((b-T)B_a+(T-a)B_b)/(b-a),
    (T-a)(b-T)/(b-a) I_d.

Store it and reuse it on subsequent requests. Repeated times and endpoints
return retained values. This is exact finite-dimensional Brownian sampling
even at adaptive requested times. All randomness requesting a time is
independent of the unobserved bridges. Uniform variables use
`(1+C_1/sqrt(C_1^2+C_2^2+C_3^2))/2` from three Gaussian seeds; assign a fixed
value on the zero-radius null event. Uniform indices use interval comparisons.

## 3. Positive likelihood correction

For one proposal generate `Z~N(0,I_d)` independent of its Brownian endpoints.
The exact covariance-completing joint law would retain the original Brownian
law and take `Z|B~N(0,I-Sigma)`. The output `Phi^circ+Z` is then exactly
`N(E Phi^circ,I)`: Clark--Ocone writes the centered comparison map as
`integral A_t dB_t` with quadratic variation `Sigma`, and the bounded complex
exponential martingale has expectation one. This is a full characteristic-
function identity, not covariance matching.

For the finite implementation define the analytical log tilt

    w_K(B,Z)=1/2 sum_(k=1)^K
                [(1/k) tr(Sigma^k)-Z^T Sigma^k Z].       (7)

This tilt is never evaluated. Its covariance at fixed `B` is

    C_K=(I+Sigma+...+Sigma^K)^(-1)
       =(I-Sigma)(I-Sigma^(K+1))^(-1).

An acquired estimator of (7) draws fresh `Z'~N(0,I_d)`, starts word vectors
`V_0=Z,V'_0=Z'`, and for `k=1,...,K` draws a fresh map from section 2 and sets
`V_k=S_hat_k(V_(k-1))`, `V'_k=S_hat_k(V'_(k-1))`. It returns

    W=1/2 sum_(k=1)^K [(Z' dot V'_k)/k-Z dot V_k].       (8)

Each estimator uses exactly `8K` values. Clip it to `[-B,B]`.

For each proposal draw `N~Poisson(2B)`, independently acquire `N` estimators
with the same retained proposal paths and `Z`, and accept with probability
the product over factors of `(B+clip(W))/(2B)`. A zero count accepts. This
is a positive operation; an independent Gaussian-generated uniform implements
the final probability. Conditional on the proposal, averaging the Poisson
product gives `exp(-B+E clip(W))`, so its accepted joint density has exactly
the clipped log tilt. Return `sigma(Phi_hat+Z)`, with the optional subtracted
constant offset restored.

## 4. Explicit full-law error bounds

Here are bounds sufficient to verify parameters (2). They also expose the
dimension bottleneck. For even `p>=2` define

    e_p=5alpha(sqrt(d p)+p)+3alpha^2 d.                  (9)

When `alpha<=1/4` and `d alpha^(K+1)<=epsilon/64`, the uncapped algorithm's
TV error is bounded by

    4d alpha^(K+1)
      +12 eta alpha d
      +6B(e_p/B)^p
      +2rho s sqrt(d).                                (10)

### Truncation

At fixed path, the log normalizer of (7) has absolute value at most
`(4/3)d alpha^(K+1)`. This follows by separately bounding the tails of the
log-determinant and geometric series. Reweighting the path by this normalizer
costs at most twice that bound when it is at most `1/4`. Comparing `C_K` to
`I-Sigma` by Gaussian KL and Pinsker costs at most
`sqrt(d) alpha^(K+1)`. Their sum is below the first term of (10).

### Acquired-estimator bias

Fresh map compositions and (6) give
`||E V_k-Sigma^k v||<=k eta alpha^k||v||`. Consequently the sum of the
absolute conditional bias of (8), averaged under the proposal and under
the finite tilted law, is at most `4eta alpha d`. The covariance of `Z`
under the latter is `C_K<=I`; the estimate is uniform in the paths.

### Likelihood tails

For any fixed odd `a`-Lipschitz map `T`, rotation of two independent Gaussian
vectors yields, by the fundamental theorem of calculus and conditional
Gaussian moments,

    ||Z' dot T(Z')-Z dot T(Z)||_p
       <= pi a sqrt(p) sqrt(d+p).

Indeed the gradient of `z dot T(z)` has norm at most `2a||z||`; the rotation
angle has length `pi/2`; the orthogonal velocity is an independent Gaussian.
For even powers, `||N(0,1)||_p<=sqrt(p)` and
`||||Z||||_p<=sqrt(d+p)` follow directly from Gaussian moment products.

Apply this to each word map, of Lipschitz constant at most `alpha^k`, and
separate the uncancelled `k>=2` terms in (8). Under the proposal this gives
`4alpha(sqrt(dp)+p)+alpha^2d`. Under the finite tilt write
`Z=C_K^(1/2)Z_0` and use `||C_K^(1/2)-I||<=alpha`. The extra contribution is
at most `(4/3)alpha^2(d+2p)`. These two estimates are bounded by (9). Thus the
sum of the clipping tails under the two joint laws is at most
`2B(e_p/B)^p`.

For completeness, if `P_K` is the finite target tilt and `Q` its proposal,
`Z_K>=1/2` and the clipped tilt is bounded by `B`, normalization and
`|exp u-exp v|<=|u-v|(exp u+exp v)` imply

    TV(P_K,P_clip)
       <= E_(P_K)|w_K-w_clip|+(e^B/Z_K)E_Q|w_K-w_clip|
       <= 3 [E_(P_K)|w_K-w_clip|+E_Q|w_K-w_clip|].

This proves the second and third terms of (10). Finally, conditionally on
the original path the completed Gaussian covariance is at least `3I/4`.
The Gaussian shift TV bound handles (5), followed by its mean shift; their
sum is at most the last term of (10).

### Checking the chosen scales

Parameters (2) give `alpha<=1/4`, `e_p<=B/4`, and
`4^-p<=epsilon/128`. Thus the four terms in (10) are at most
`epsilon/16`, `epsilon/16`, `3epsilon/256`, and `epsilon/16` respectively.
Their sum is less than `epsilon/4`, leaving ample room for the caps and
scalar-constant approximation below. There is no fitted field, hidden
Jacobian, exact mean, potential value, conditional-mean evaluation or
adaptive unbounded stopping in the implemented algorithm.

## 5. Every-execution caps, Poisson generation and arithmetic

Cap the number of attempts by `A` and the Poisson count per attempt by `J`,
returning a fixed output on overflow. Since every attempt accepts with
probability at least `exp(-2B)=exp(-1/2)>1/2`, the probability of exhausting
attempts is at most `2^-A<=epsilon/64`. Markov's inequality applied to
`2^N`, whose mean is `exp(1/2)<2`, gives
`P(N>J)<2^-J`; the union bound costs at most `epsilon/64`.

Poisson is not an extra primitive. Precompute an odd-degree alternating
Taylor lower bound `p0_minus` for `exp(-1/2)`, with degree `D` large enough
that `0<=exp(-1/2)-p0_minus<=epsilon/(128A)`; for example take the least odd
integer at least `ceil(log_2(128A/epsilon))`. Use the finite probabilities
`p0_minus (1/2)^j/j!`, `0<=j<=J`, and declare all remaining probability to be
overflow. These are nonnegative rational numbers summing to at most one.
An inverse cumulative table and a Gaussian-generated uniform sample them
using at most `J+1` comparisons. Their difference from the exactly capped
Poisson law has TV at most `2|exp(-1/2)-p0_minus|`, so all attempts together
cost at most `epsilon/64`. There is no exponential/logarithm primitive at
runtime, only these finitely precomputed rational constants.

Source queries obey (1). Source-independent vector arithmetic is
`O(d A[M+JK])`; a naive sorted-list bridge implementation adds
`O(A(JK)^2)` scalar work, and choosing uniform indices by binary interval
comparisons adds `O(AJK log(M+1))` scalar work. Precomputing Poisson rationals costs polynomial
work in `D+J` and their bit lengths. Storage is `O(d[M+JK])` with rejected
attempts discarded sequentially. Gaussian seeds have the same polynomial
count. Exact returned oracle reals are handled in the declared real-arithmetic
model; no bound on their bit lengths is invented. The floating implementation
is diagnostic. A finite-bit claim must compare to a commonly rounded target
and budget finite-difference cancellation, Gaussian approximations and
roundoff; that additional claim is not made here.

## 6. Actual output reuse and comparison

For any acquired center `x` and scale `r0`, apply the construction to
`z -> g(x+r0 z)`, whose Lipschitz constant is `Lr0` and which is still a
gradient field. Conditional on any past history, fresh seeds give the same
uniform TV guarantee around `E g(x+r0G)`. Therefore a finite adaptive user of
these actual outputs has joint transcript error at most the sum of its
conditional per-call errors. Each invocation pays its full cap; no cache of
unproved shared Gaussian noise is assumed.

At fixed accuracy, S1's fixed-positive-exponent candidate is a stronger
dimension comparator than this square-root method. At very small accuracy,
this construction removes elementary averaging's inverse-epsilon factor.
It is an explicit acquired instance of existing Gaussian cloud methodology,
not a claim to improve its historical generality. It proves that current-law
operations, full-law correction, positive output and deterministic query caps
can coexist. The unsolved N687 issue is reducing the factor `sqrt(d)` in the
likelihood size (9) without an unacquired covariance, mean difference, or
small-innovation joint oracle. More likelihood terms only reduce truncation;
they do not reduce that leading size.

The accompanying executable implements all the charged operations and checks
the homogeneous-action contracts on a rotated multidimensional conservative
source. Its synthetic runs are not used as moment-based TV evidence; the
full-law conclusion is (10) plus the cap analysis.

## 7. A dimension obstruction for this particular proposal/tilt design

The square-root scale is necessary for this averaged proposal with a single
bounded log tilt, not merely an avoidable term in the preceding proof. Any
accepted joint law from a tilt bounded in `[-B,B]` has density at most
`exp(2B)` times the joint proposal. Its output has the same domination.

Take the legal conservative affine source `g(x)=lambda x`, put
`beta=lambda^2/(M sigma^2)`, and normalize output by `sigma`. The averaged
proposal is `Q=N(0,(1+beta)I_d)`, whereas the requested target is
`P=N(0,I_d)`. For the event

    E={||y||^2 <= d(1+beta/2)},

Gaussian variance and Chebyshev bounds prove that every output `P_clip`
obtained by this bounded global tilt satisfies

    TV(P,P_clip) >=
      1 - 8[1+exp(2B)(1+beta)^2]/(d beta^2).             (11)

For `0<beta<=1`, elementary chi-square Chernoff bounds give the sharper

    TV(P,P_clip) >=
      1-exp(-d beta^2/24)-exp(2B-d beta^2/64).          (12)

Indeed the target upper-tail parameter is `beta/2`; the proposal lower-tail
parameter is `beta/[2(1+beta)]>=beta/4`. The Gaussian squared-norm moment
generating function yields these two exponential bounds directly. A single
event of the entire output law proves the result. If caps and scalar
approximations change the uncapped clipped law by TV at most `delta_cap`,
subtract `delta_cap` from the right sides of (11)--(12).

At fixed `lambda/sigma` and fixed `B`, taking `M=o(sqrt(d))` makes this
architecture's TV error tend to one. Replacing `M` in (2) by a
polylogarithm, while increasing word order or shrinking secants, cannot solve
the original target. This is a mechanism obstruction, not an N687 lower
bound: the same affine source's mean is acquired exactly by querying `g(0)`.
An improved construction must exploit source structure in its proposal or
use a different law transformation, rather than merely refine the bounded
likelihood estimator for this averaged proposal.

Primary reference inspected:
https://arxiv.org/html/2609.38710v1
