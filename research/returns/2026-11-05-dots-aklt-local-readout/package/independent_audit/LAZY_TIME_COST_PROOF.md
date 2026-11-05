# Finite expected lazy-time arithmetic cost

This note strengthens almost-sure termination to a qualitative finite-expected-cost statement for the particular timestamps created by local_perfect_sampler.py. It does not give a useful latency constant, an optimal query-size bound, or a general theorem for arbitrary adaptive exact-real expressions.

## 1. Inputs already established

For fixed finite K, the resource proof gives a positive exponential moment for P, the number of all seed and parent oracle proposals. There are at most2P exponential atoms and at most2P newly created birth/death timestamps. Each new timestamp is an already created birth time, or0, plus or minus one fresh independent Exp(1) atom. The code never creates a query time by multiplying or otherwise nonlinearly transforming a previously sampled timestamp.

Every queried comparison is between these timestamps, or a timestamp and0. Each symbolic expression has at most2P atoms; all coefficients are integers of magnitude at most1 after cancellation. The number of comparisons is at most a fixed polynomial in P: the crude bound4P²+P suffices because M<=P.

The following argument refers to ideal independent bit arrays assigned to atoms when they are created. Revealing their bits lazily, in an adaptive order, has the same distribution. It is legitimate to condition on full previously assigned atom values when proving an unconditional bound, even though the implementation has revealed only a prefix.

## 2. Anti-concentration under adaptive timestamp creation

Order timestamps by creation, rather than by numerical time. Conditional on all previous full atom values, the current control history and other past random choices, the next timestamp has the form T_old +/- E_new. Its conditional density is bounded by1. For any earlier timestamp x and delta>0,

Pr(|T_new-x|<delta | past) <=2 delta.

If the algorithm stops, append fictitious timestamps of the same form with fresh independent exponentials. Thus for the first m created timestamps, including comparison with0,

Pr(minimum pair separation <delta) <=m(m+1)delta.

This union bound concerns newly created distinct timestamps. Reusing an old symbolic timestamp is handled by exact coefficient cancellation, not by a small-gap test. Distinct creations coincide with probability zero.

Let D be the minimum nonzero separation among timestamps actually created, also including0. On a run with no such pair set D=1. For u>=0 and any integer m,

Pr(log_+(1/D)>u) <=Pr(2P>m)+m(m+1)exp(-u).

Choose m of order exp(u/4). The exponential moment of P makes the first term superexponentially small in u, while the second is of order exp(-u/2). Hence log_+(1/D) has all fixed moments and even a sufficiently small positive exponential moment.

Similarly, if R is the largest exponential atom created, pad the atom stream after stopping. For any m,

Pr(R>r) <=Pr(2P>m)+m exp(-r).

Choosing m of order exp(r/2) proves the same qualitative tail and moment conclusion for R. No independence between P, R and D is needed afterwards; Holder's inequality combines their finite moments.

## 3. Required precision

An atom is E=-log U. If E<=R and b revealed uniform bits satisfy2^-b<=exp(-R)/2, the lower uniform endpoint is positive and at least U/2. The log error due to the uniform interval is then at most2 exp(R)2^-b.

The rational log enclosure reduces to y in[1,2] and uses the atanh series. With N=b/2 terms, its omitted tail is bounded by a constant times3^-b. The log2 range-reduction multiplier has magnitude O(R+1), once the lower endpoint is at least U/2. Consequently the complete atom enclosure width is at most

C[exp(R)2^-b+(R+1)3^-b]

for an absolute constant C. An expression involving at most2P atoms has at most2P times this error. It follows that all nontrivial timestamp comparisons have resolved once

b >= C'[1+R+log(1+P)+log_+(1/D)].

The implementation doubles both b and N, so its final precision exceeds this sufficient threshold by at most a constant factor. Its special initial loop for a zero lower uniform endpoint uses no more than O(R+1) bits and obeys the same bound. Reusing cached intervals can only reduce work.

## 4. Rational arithmetic

At precision b, the reduced atanh argument has O(b+R) input bits. Its first O(b) rational powers and their odd-denominator sum can be formed with polynomially many integer operations on polynomial-bit-length integers. A coarse grade-school bound suffices: powers have O(b(b+R)) bits, and a common denominator for the odd divisors introduces at most O(b log b) additional bits. Range-reduction by powers of2 is polynomial in R+b. Summing enclosures for O(P) atoms and manipulating their symbolic coefficient maps is also polynomial in P,R,b.

There are only polynomially many comparisons. Therefore the entire exact-time arithmetic cost is bounded by a fixed polynomial in P, R and log_+(1/D), apart from fixed implementation constants. These variables have all fixed moments, so expected exact-time bit cost is finite for each finite K. This also gives finite expected memory for the time expressions and cached rational enclosures.

## 5. Remaining primitives and scope

This argument is specific to the lazy-time stage. The loop bridge separately has geometric path-length tails and exact finite integer choices, and the resource MGF charges every call. Coordinate bit length is an input cost. No enclosing-volume parameter appears, but this does not imply linear bit complexity in |K|.

The exact Poisson primitive also has finite expected arithmetic cost, as quantified in the next section. No optimized numerical constant is claimed here.

The decisive new fact is that adaptive comparisons cannot force a hidden infinite-mean precision cost in this implementation: all queried real times belong to a sequentially generated family with conditional density at most1. Generic continuity alone would not have been enough to establish that stronger conclusion.

## 6. Poisson primitive: a sufficient, not all-order, arithmetic bound

The small-rate subroutine has lambda in[0,1]. At refinement r it uses b=32(r+1) uniform bits and n=12 times2^r exponential-series terms. The CDF enclosure error is at most3/(2n+1)!, uniformly in the output index k, because its positive partial exponential sum is at most e<3. This factorial error is smaller than a constant times2^(-64(r+1)).

To reach refinement r>=1, the previously exposed uniform interval must meet one CDF boundary within its enclosure error. Restrict first to the event that the final Poisson output N is at most32r. A union bound over those32r+1 boundaries gives O((r+1)2^(-32r)). The complement is bounded by Pr(Poisson(1)>32r), which is even smaller by the elementary factorial tail bound. Therefore

Pr(reach refinement r) <=C(r+1)2^(-32r).

Rates used by this sampler have denominators dividing the fixed local-oracle denominator, or are1. Thus their rational input bit lengths are uniformly bounded. A deliberately coarse grade-school implementation bound for all CDF evaluations in stage r is

cost_r <=C_D n^6 (N+1)^6.

Indeed, the denominators of the exponential partial sum divide D^(2n)(2n)!, with O(n(log D+log n)) bits; the Poisson positive partial sum has the analogous bound with N. Repeated rational powers, factorials, additions, gcd reduction and comparisons all fit inside the displayed polynomial bound. The bound need not reflect Python's faster actual integer algorithms.

For the first and second arithmetic moments, Cauchy-Schwarz and the bounded moments of Poisson(1) give

E[1_{reach r} cost_r^p]
<=C_p 2^(6pr) sqrt(Pr(reach r)),   p=1,2.

The resulting series converges since6p<16. Applying the triangle inequality in L^p to the stage sum proves uniform finite first and second moments of one small-rate Poisson call. No claim of all arithmetic moments is made: the series order doubles while uniform bits grow only linearly.

The outer exact-Poisson routine makes floor(lambda)+1 small-rate calls. Across the local sampler, their number is at most a fixed constant times |K|+A+M+1, whose expectation is finite. Each successive call is chosen from past history and has the same uniform conditional mean-cost bound. Predictable conditional expectation therefore gives finite expected total Poisson arithmetic cost. Together with the geometric oracle tails, polynomial data-structure work, and the timestamp argument above, this closes a qualitative finite-expected-bit-cost statement for every fixed finite input query, without furnishing a practical complexity constant.

## 7. Random unbounded source paths in a physical attempt

Fixed-K finiteness alone would not justify averaging over an unbounded random source path. Here the required rate comparison holds explicitly. The path proposal has a prefix of at most6 steps and a continuation tail C rho^n, with rho=709007/750000<1, from the same memory-6 Collatz certificate. A uniform, deliberately loose finite-state prefactor C=421 suffices. The queried set has size at most6+T+1, and the local conditional joint MGF has exponent H|K| with H<2039/10^9.

The exact checker verifies

H < 1-rho =40993/750000,
exp(H)rho <=rho/(1-H)<1.

Therefore the source path has E exp(H|K|)<infinity. More explicitly, put R=1/(1-H). The elementary tail-sum formula gives the rational upper bound

E exp(H|K|) <=R^7 [1+(R-1)421rho/(1-Rrho)].

Averaging the local resource MGF over the independently drawn path retains a positive exponential moment for total local proposal count. Null path proposals can be bounded by pretending they also make such a query, which only increases the cost. All sequential timestamp, Poisson and arithmetic arguments consequently apply to the full physical attempt, not just to fixed-K conditional queries. The source-path work itself has geometric tails. This closes the integrability step without claiming that fixed-K finiteness automatically suffices.
