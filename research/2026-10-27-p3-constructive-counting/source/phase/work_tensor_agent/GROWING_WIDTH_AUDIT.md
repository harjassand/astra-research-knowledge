# Independent audit of the proposed uniform growing-width counter

27 October 2026. Conditional on the governing ETH manuscript. This audits
the mathematics and uniform resource estimates of the proposed parameter
extension; it does not establish historical priority or practical speed.

## Finding

I found no fatal gap in the claimed range

    k = o((log n / log log n)^(1/3))

provided the squared-factorial sparsification, exact parameter guards, and
entropy factor below are included. In particular, the fixed-k constants in
the manuscript must not simply be reused as uniform constants. The concrete
construction permits them to be replaced by the explicit bounds below.

## 1. Squared-factorial sparsification

Use the branching priority and disjoint children of Appendix A, but set

    theta_j = M^j (j!)^2,   M>=2.

The proofs of A.1 and A.2 only compare a threshold theta_(c-|H|) with a
corresponding occurrence count. They do not require geometric thresholds,
so they remain valid. Consequently the insertion recurrence becomes

    T_1 <= 2n,
    T_j <= 4n theta_(j-1) + 2 sum_{i=1}^{j-1} theta_(j-i) T_i.

The following bound holds uniformly in j:

    T_j <= 16 n M^(j-1) ((j-1)!)^2.

Proof: for j>=2 separate the i=1 term, using T_1<=2n. After division by
n M^(j-1)((j-1)!)^2, the right side is at most

    8 + 32 sum_{a=1}^{j-2} binom(j-1,a)^(-2) <= 16.

For j=2 the sum is empty. Otherwise write m=j-1; each internal binomial
coefficient is at least m, and (m-1)/m^2<=1/4. This proves induction.

Thus the total number of B-children chosen along a path is at most

    (16n/M) sum_{j=1}^{k-1} 1/j^2 < 32n/M.

Depth is at most Cn with

    C = 16 sum_{j=0}^{k-2} M^j (j!)^2
      <= 32 M^(k-2) ((k-2)!)^2.

The tree-size argument from A.3 therefore works with Gamma=32. Choose powers
of two M>=32 until

    32 ceil(log2(4CM)) <= sigma M.

Let H=ceil(log2(4k/sigma)). A power of two in
[2048 kH/sigma,4096 kH/sigma) satisfies the test. Indeed log2 M<=5H,
ceil(log2(4CM))<=9kH, and 32*9kH<sigma M. Hence the first successful M is
at most 4096kH/sigma. The leaf occurrence bound is

    B = 2 sum_{j=0}^{k-1} theta_j
      <= 4 M^(k-1) ((k-1)!)^2,

so log B=O(k log(k/sigma)), with an absolute implied constant.

## 2. Input and sparsification work are not hidden n^O(k) costs

Appendix A describes a possible universe of O_k(n^k) clauses. It is
unnecessary to materialize that universe. Store the present clauses only,
enumerate their at most 2^k subsets to build occurrence counters, and normalize
by comparisons of stored clauses. Along a path at most Cn new clauses are
inserted, so there are at most m+Cn stored clauses, where m is the input count.
The per-node cost is bounded by a universal polynomial in m+Cn,n,k times 2^k;
workspace also has a universal polynomial bound in those explicit quantities.

With lambda=ceil log2 n, nu=ceil log2 lambda, and
sigma=1/ceil(sqrt(lambda)), the proposed range gives

    log B, log C = O(k nu)=o(lambda),
    B,C,2^k = n^o(1).

Thus the node overhead is polynomial in the input length and n in this
range. A universal implementation may guard B,C<=n before constructing
branches, and fall back to exhaustive assignment enumeration otherwise;
these guards eventually pass in the claimed range and enforce polynomial
workspace on all inputs.

## 3. Section 6's exhaustive preprocessing remains subexponential

For a leaf m<=Bn, put mu=floor(log2 m)+1=O(lambda). Unrolling the actual
searches, rather than citing exp(poly(B,log m)), gives:

- Shift tuples: log2 of the work is O(B^2 mu^4).
- Local-code matrices: c_G d_G = O(B^3 mu^6+B^2 mu^3); testing short words
  adds at most lower-order exponent of the same polynomial magnitude.
- Greedy parity-row candidates: log2 of their number is O(B^2 mu^3+log n).

The polynomial-system counter is called once per candidate. Therefore these
exponents add to its running-time exponent; they do not multiply it by an
exponential exponent. Since B=exp(O(k nu))=n^o(1), all displayed preprocessing
and candidate exponents are n^o(1)=o(n).

Each candidate has at most 6n equations. Its monomial lists have at most
2^k max(D_0,P) terms per equation. Their total explicit size is

    S <= n exp(O(k nu)) = n^(1+o(1)).

## 4. The optimized Section 4 parameters are uniformly feasible

After the manuscript's high-incidence-variable branching there are N>=n/2
free variables, with log b,log w=O(k nu). The branch count contributes only
2^O(n/sqrt(lambda)). Compute design parameters using the remaining N; its
logarithms are asymptotically equivalent to the original ones. Put

    a = k^3 nu/lambda,       r=floor(a^(-1/2)),
    t=ceil log2 r,           Q=floor(lambda/(128t)),
    tau=1/(r lambda),        A=ceil log2(2br^2 lambda),
    R=ceil sqrt(8QA)+32,     D=r^(2Q).

Use exact guards for r>=2, R>=32, 6R<=Q, the centered interval, the balance
inequalities and the binomial tail. The centered interval's tail is at most

    2 exp(-R^2/(8Q)) <= 2 exp(-A) <= 2^(1-A) <= 1/(br^2 lambda).

Since a->0, all guards eventually pass. In particular

    D<=2^(lambda/64),
    b,w=exp(O(k nu))=N^o(1),

so 2(b+w)D^2<=N<=M_incidence eventually. Also 2Qr^2<=N. The construction
enumerates D auxiliary labels, with polynomial overhead in D and the explicit
scope lists. It does not enumerate n^k truth-table states. All polynomial
exponents in Lemma 4.7 are universal.

## 5. Degree lift and rational arithmetic remain uniform

Lemma 5.2 is an algebraic degree bound for arbitrary integer k, not a
fixed-k asymptotic assertion. With ell=n+1 and at most 6n tests,

    d = k(m_test+2(ell-1)) <= 8kn <= 16kN.

Constant-one factors have degree zero and do not alter this bound. Retaining
total V-order below ell is essential: replacing it by a separate truncation
budget for each factor would invalidate the degree estimate.

Proposition 5.3 evaluates each explicitly listed monomial using at most k
substituted inputs. Its polynomial overhead is uniform in the displayed
parameters k,S,N,ell,D,Q,R,J,r. Appendix B explicitly gives

    log Omega = O(k m_test ell Q log(Q+2))
              = O(k n^2 Q log(Q+2)),

and polynomial numerator bit sizes in those same parameters. The Hermite
system order is O(knR+Q). All are polynomially bounded in n in the proposed
range. No exponential k-dependence is concealed in the arithmetic.

## 6. The entropy factor must appear in the time bound

Let eta=sqrt(a log(2/a)). The parameter estimates give

    q/N = O(eta),

where q is the Taylor correction subset order. But enumerating the correction
sets costs C_q=sum_{j<=q} 2^j binom(N,j), whose logarithm is

    O(N eta log(2/eta)),

not merely O(N eta). A convenient slightly looser expression is

    O(N sqrt(a) [log(2/a)]^(3/2)).

Both are o(N) as a->0. Measurement and group-assignment costs contribute
O(N/r)=O(N sqrt(a)), while sparsification and high-incidence branching
contribute O(n/sqrt(lambda)). The explicit Section 6 exponents are n^o(1).
These costs preserve subexponential time and polynomial workspace in the
claimed growing-width range.

## Status

The construction appears mathematically valid under the governing proof,
with the explicit changes above. It is a uniform growing-width extension,
not a general CircuitSAT result, a polynomial-time SAT algorithm, an executed
large-instance solver, or a verified historical novelty. Exact small checks
of a kernel support an implementation but cannot establish its asymptotic
running time or practical advantage.
