# Two precise barriers to reusing Gaussian mean channels

27 October 2026. These are obstructions to particular representations, not
lower bounds for the original N687 single-output Gaussian-mean problem.
The frozen sources and the previous construction are unchanged.

## 1. An unshared compiler cannot become polylogarithmic by choosing its order

Consider the following explicitly scoped tree interface, extracted from the
uncached mean-elimination construction in S1, sections 5--7. A call has labels
`(c,p)` and is terminal only if `p <= c`. Every genuine nonterminal centering
circuit retains both an output-mean child with labels `(c+t,p)` and an
internal-mean child with labels `(c-10t,p-1/4)`. The two child computations use
disjoint source-query trees. All other children only increase cost. Assume
`0 < t <= 1/4`; S1's constraint `10t(4K+1)<1/4` is stronger.

This is a theorem about this two-child topology. A compiler which proves that
an internal branch can be removed, or shares dependent children under a new
joint-law contract, is outside this theorem. In particular, this statement
does not call the topology an information-theoretic necessity for N687.

Put `q=p-c`. The two child gaps are `q-t` and `q-1/4+10t`. Neither decreases
the gap by more than `1/4`. From root `(1,K)`, with integer `K>=3`, every path
therefore contains at least `4(K-1)` edges before it can terminate. Binary
branching before that depth gives at least

    2^[4(K-1)]

terminal calls per noisy copy. The literal tree may be much larger.

S1's final averaging step uses `M` independent copies, `delta=M^(-1/2)`,
and the declared certificate `B M^(1-K/2) sqrt(d) <= epsilon`, with `B>=1`.
Writing `D=log(d)+2log(1/epsilon)` and `x=log M`, this certificate requires

    (K-2)x >= D.

Thus this interface and certificate together imply

    log Q >= x + 4(K-1)log 2
           >= x + 4log 2 + (4log 2)D/x
           >= 4sqrt((log 2)D)+4log 2.

The unshared tree cannot certify a polylogarithmic query bound by merely
letting `K` depend on `d,epsilon`. The lower envelope is already stretched
exponential in the square root of the logarithmic problem size. This is a
lower bound on the resource count of the stated construction when tuned via
its stated sufficient error bound, not a necessary error-vs-cost relation
for every sampler, nor even for every possible tighter analysis of S1.

There is a second, simpler inconsistency in a naive tuning of S1 unchanged:
its `R=delta^t<1/2` and `t<1/(160K+40)` force
`log M > (320K+80)log 2`. Taking `M` polylogarithmic while taking
`K` of order `log d/loglog d` violates that cutoff condition. A new choice
of smoothing/labels might remove this particular condition, so the tree
argument is the more informative one.

## 2. Perfect common-noise reuse silently acquires a noiseless mean difference

Let

    m_g(x)=E[g(x+G)],  G~N(0,1),

for arbitrary scalar globally `L`-Lipschitz `g`. In one dimension every such
continuous `g` is the gradient of a `C^{1,1}` potential. Fix any `S>0`.
Suppose a proposed reusable acquired object promises a joint sample within
TV `epsilon<1` of

    (m_g(0)+S Z, m_g(2)+S Z).                 (1)

No finite, uniform, every-execution value-query cap can provide this contract
for every such `g`, even with arbitrary internal computation.

Proof. Let `t` be uniform on `[0,1/2]`, let `A` be independent uniform on
`[L/2,L]`, and for `0<delta<1/2` define

    g_{A,t}(u)=A delta (1-|u-t|/delta)_+.

This is globally `L`-Lipschitz. Its two-center mean difference is

    s(A,t)=A delta integral (1-|u-t|/delta)_+
                             [phi(u)-phi(u-2)] du > 0,

because its support lies strictly to the left of `1`. For fixed `t`, this
difference is a nonzero linear function of the continuously distributed `A`.

Fix all random seeds of an `n`-query algorithm. Until it hits the bump's
support its transcript is the zero-function transcript. Each point on that
zero-transcript path can hit a set of locations `t` of Lebesgue measure at
most `2delta`. Since the location interval has length `1/2`, the union bound
gives hit probability at most `4n delta`. This argument allows adaptive
queries, arbitrary unbounded query locations and unlimited computation.

On a miss, the algorithm's output is independent of `A`; its output
difference cannot equal `s(A,t)` except on a null set of `A`. Therefore,
averaged over these legal source functions, the probability that its output
lies on the support line of target (1) is at most `4n delta`. Target (1)
assigns that line probability one. Average TV is at least `1-4n delta`.
Taking `delta` sufficiently small contradicts any uniform `epsilon<1`.

The problem is the singular JOINT promise. Each marginal of (1) is an
ordinary noisy target; this proof gives no lower bound for either marginal.
One cannot cache standalone approximately Gaussian samples and declare
their shared-seed joint law to be (1).

## 3. Quantitative innovation cost for near-perfect sharing

Consider the less singular joint contract

    (m_g(0)+S Z+nu Z_1, m_g(2)+S Z+nu Z_2),       (2)

where all three normals are independent and `nu>0`. The difference has law
`N(s_g,2nu^2)`, independent of the size of the common noise `S`.

For integer `n>=1`, set `delta=1/(16n)` and use the preceding random-location
family with deterministic `A=L`. Its support lies in `[-1/16,9/16]`. Hence

    phi(u)-phi(u-2) >= c0,
    c0=phi(9/16)-phi(23/16)>0,

and `s_g >= s_min=c0 L/(256n^2)`, because the integral of the triangular
bump is `L delta^2`. The zero and bump oracle transcripts couple with
failure probability at most `4n delta=1/4`.

The event `y_1-y_2 > s_min/2` separates the zero-source target from every
bump-source target by at least

    2 Phi[s_min/(2sqrt(2)nu)] - 1.

The same bound holds after mixing the bump locations. Consequently a
uniform TV guarantee `epsilon` under contract (2) must satisfy

    2epsilon + 1/4 >= 2 Phi[s_min/(2sqrt(2)nu)] - 1.       (3)

In particular, if

    nu <= c0 L/(1024sqrt(2)n^2),

then `epsilon >= (2Phi(2)-1-1/4)/2 > .352`. A fixed, smaller error tolerance
therefore requires an independent innovation standard deviation of order
at least `L/n^2`, with the explicit constant displayed above.

If each marginal is to have variance `sigma^2` and correlation `rho`, then
`nu=sigma sqrt(1-rho)` and this gives the scoped requirement

    n > sqrt[c0 L/(1024sqrt(2)sigma)] (1-rho)^(-1/4)

for error below `.352`, when `0<=rho<1`. Perfect or almost-perfect common
noise is not a free way to cancel large affine weights in a mean circuit.
The relevant joint innovation must be acquired and paid.

## 4. Implication for a better representation

The old unshared positive compiler pays for independent children. A naive
joint Gaussian cache can remove that price only by accidentally promising
an unacquirable, nearly noiseless mean difference. A useful replacement
must track an actual joint law with a quantitatively sufficient innovation
budget, or exploit a source-specific algebraic cancellation proved from the
permitted values. Marginal Gaussian closeness and common seeds alone do not
establish either property.

These results preserve the original target as open. They do not contradict
the fixed-positive-exponent candidate in S1, the acquired two-value actions
in S4, or the preceding coercive inverse and scalar full-law constructions.

## 5. Ordinary alternatives remain charged

S5's averaging-plus-noise method is a fully explicit general
`O((L^2/sigma^2)sqrt(d)/epsilon)` whole-vector value method. S1 is a stronger
fixed-positive-exponent candidate, subject to its own proof obligations.
Chen--Chewi--Daskalakis--Rakhlin, *High-accuracy log-concave sampling with
stochastic queries*, arXiv:2602.14342v2, Theorems 3.1--3.2, supplies a
stronger high-accuracy FORS comparator when its estimator tails and proximal
center are actually acquired. Its stochastic-oracle tail assumption is on
the VECTOR NORM; directional sub-Gaussian tails of `g(G)-Eg(G)` alone cannot
be inserted with a dimension-free norm parameter. The actual prox center,
clipping bias, rejection tail and deterministic truncation cap all remain
charges. The current source already recognized this alternative; it is not
new machinery here.

Primary source inspected:
https://arxiv.org/html/2602.14342v2

The companion `check_reuse_obstructions.py` checks the discrete tree theorem
with exact integers and prints the Gaussian event separation in (3). The
numerical values illustrate the analytic full-law event proof; they are not
moment-based empirical TV certificates.
