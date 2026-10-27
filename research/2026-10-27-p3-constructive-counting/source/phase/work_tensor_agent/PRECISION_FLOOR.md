# A sharp-order obstruction to reducing Appendix D's precision to output size

27 October 2026. This is an exact limitation of the supplied Hermite recovery
interface, not a lower bound against all algorithms for counting circuits.

## Source and question

The source is Lemma D.5 and equations (D.10)--(D.15) in the supplied manuscript:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf

Could a circuit with M wires but only n independent inputs be counted faster
by using root precision p=n+1, replacing the M/sqrt(log M) exponent with an
expression of the order sqrt(M p/log M)? The existing proof instead raises
local precision by order M D/u, irrespective of root p. The construction below
shows that this order cannot be removed under Lemma D.5's hypotheses alone.

## Proposition: the precision floor persists when the answer is one bit

Let 1 <= u <= a, M >= u, L=2^a, alpha=2L, and

    S = {-L,-L+1,...,L-1},   h=floor(M/u),
    q_i = h max(0,u-i).

Define the rational polynomial

    F(T) = product_{q in S, q != 0, v2(q)<u} (1-T/q)^(q_{v2(q)}).

Then:

1. F(0)=1.
2. deg F <= M(2L-1).
3. F(t+alpha*z) has 2-adically integral coefficients for every t in S.
4. At each active node t with i=v2(t)<u and D_i=L/2^i, the minimum
   2-adic valuation of its nonzero coefficients is exactly

    c_i = h(u-i)(a+1-i)
          + h D_i sum_{j=1}^{a-i} j min(j,u-i)/2^j,

   and therefore c_i >= M D_i/(4u).

Consequently, if the local precision at every active node is no greater than
c_i, the entire supplied local polynomial is zero modulo that precision.
Those observations are identical for F and the zero polynomial, although
their required values at zero differ modulo 2. This holds even if all local
coefficients are supplied, rather than merely the truncated jets in D.5.

### Proof

The value at zero is immediate. There are L/2^i nonzero members of S with
valuation i for 0 <= i < u. Hence

    deg F = h L sum_{i=0}^{u-1} (u-i)/2^i
          = h L (2u-2+2^(1-u)).

This is at most h L(2u-1), at most M L(2-1/u), and at most
M(2L-1), since L>=u.

Consider the coefficients after substituting T=t+alpha*z. If t=0, each
factor has constant term one and an integral slope. If v2(t)>=u, each active
q has smaller valuation, so 1-t/q has valuation zero and the slope -alpha/q
has positive valuation. Thus both cases have integral coefficients.

Now let i=v2(t)<u. The factor for q=t contributes

    (-alpha*z/t)^(q_i)

and has coefficient valuation q_i(a+1-i). Every other factor has a constant
term of valuation v2(t-q)-v2(q), smaller than its slope's valuation. The
minimum valuation of the coefficients of a product is the sum of the minimum
valuations of its factors: reduce their normalized polynomials modulo two,
where the product of nonzero polynomials remains nonzero. Thus the exact
content is

    c_i = q_i(a+1-i)
          + sum_{q != 0,t} q_{v2(q)} [v2(t-q)-v2(q)].

The residue-grid calculation in (D.10), with its sign reversed, gives

    c_i = q_i(a+1-i)
          + D_i sum_{j=1}^{a-i} j [q_i-q_{i+j}]/2^j.

Since q_i-q_{i+j}=h min(j,u-i), this is the displayed formula, and it is
nonnegative. Keeping only j=1 yields c_i >= h D_i/2. Because M/u>=1,
floor(M/u)>=M/(2u); hence c_i>=M D_i/(4u). This proves all assertions.

## Algorithmic implication and exact limit

In D.12--D.15, the mode count is exp(O(sqrt(M p_t/D_i))). An attempted
drop-in refinement using only p_t=O(p D_i/u), with root p=o(M), would eventually
fall below all the c_i above. The recovery interface then lacks information
to recover even the least significant output bit. The M D_i/u precision
overhead is therefore necessary up to constants for this generic interface.

This is not a circuit lower bound. The polynomial F above has not been shown
to arise from a canonically lifted Boolean circuit under exactly the packing
chosen by the manuscript's algorithm. A successful extension could impose
and exploit a genuinely stronger invariant on circuit-induced deformations,
use additional observations, or replace the deformation/recovery interface.
It cannot justify the refinement merely by the final answer's small bit size.

## A separate canonical 0/1 example

Even normalization and canonical tensor lifting do not automatically tie
local precision to output precision. Set a=u=1, L=2, alpha=4. For a packet
with one real diagonal port, the Cauchy kernel is

    w(T)=W_00(T)=product_{q in {-2,-1,1}} (1-T/q).

Use M independent edges, each with a delta_1 unary tensor at either endpoint,
and put one real port in each such packet. There are no independent inputs;
the contraction is one and all tensor entries are canonical zeroes or ones.
The deformation is F(T)=w(T)^M. Direct factorization shows that both
F(-1+4z) and F(1+4z) have coefficient content exactly 2M, whereas F(0)=1.

This is a small-parameter instance of the deformation algebra and obeys the
packet count M<=3M/L. It is not a claim about the asymptotic parameter schedule
or the specific output of its deterministic packing algorithm. The underlying
network is itself trivial to contract. Its purpose is to demonstrate that
canonical zero-one entries, determinism, and a one-bit answer alone do not
force small interpolation precision.

## Further exact barrier for globally Boolean-normalized deformations

Let A_n=Q[x_1,...,x_n]/(x_i^2-x_i), the algebra of all rational-valued Boolean
functions. It is isomorphic to the product Q^(2^n). If h(T) in A_n[T] obeys
h(T)^2=h(T) identically, then for each Boolean assignment x the polynomial
h(T,x) is an idempotent of Q[T], hence either the constant zero or constant
one. Thus h(T) is constant in T. In particular, a polynomial family of algebra
homomorphisms A_n -> A_n[T] that equals the identity at T=0 is identically the
identity.

A direct circuit deformation cannot both vary the exact input representation
and preserve every Boolean algebra identity along a polynomial parameter.
It must weaken an identity, change the target algebra, use a non-polynomial
representation, or control an additional reconstruction cost. This restricted
statement does not preclude useful nodewise identities or interpolation.

## Executed verification

`precision_floor.py` expands exact rational polynomials at every grid node
for (a,u,M)=(1,1,1),(2,1,4),(3,2,6), verifies all degree and integrality bounds,
and independently compares the actual coefficient content with the formula.
The third example has degree 60, output one, and local contents 78 at odd
nodes and 21 at nodes of valuation one. An eight-edge canonical pin example
has output one and content 16 at both active nodes. All assertions passed.
