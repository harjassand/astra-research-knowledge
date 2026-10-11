# Exact finite-seed compiler for rational DFA couplings

Status: internally reconstructed mathematical result with runnable exact-rational
certificates. The universal proof below is independent of the finite examples.
Historical originality, specialist review, and mechanized verification remain
open. This extends the finite-population theorem developed by the structural
worker; it does not claim to resolve ordinary quantum-capacity computability or
the other obstructions in `RESULT.md`.

The useful operation is: **optimize over an explicitly finite population graph,
then compile its binary-length witness into an exact-marginal random-access
coupling whose terminal distribution is computed exactly.** Shared quantile
repair, rather than independent filler coordinates, prevents the randomness and
probability-denominator costs from growing with the horizon.

## 1. Supplied interface and notation

Input is an explicitly listed finite total deterministic automaton with states
`s=0,...,d-1`, a start state `s0`, and transition table `f(s,a)`. The rational
letter law `mu` and rational target state law `nu` are supplied. Every coordinate
has marginal `mu`; arbitrary correlations across coordinates are allowed. Remove
letters of zero marginal exactly before graph construction. Let `m` be the
positive support size, `alpha=min_a mu(a)>0`, and write

    mu(a)=u_a/M,    sum_a u_a=M,    u_min=min_a u_a,

where `M` is the least common multiple of the supplied denominators. No oracle
for transition products, optimal input words, independence, or a stationary
infinite process is provided. Reading the table costs at least `d*m` entries.
A succinctly represented semigroup must first supply or acquire this table;
that acquisition is not covered by the theorem.

Use population `P>=1` below. The executable calls this parameter `Q`; its `M`
has the same meaning as here. Define

    H = binom(P+d-1,d-1),
    B = binom(P+d*m-1,d*m-1),
    r = d/(2P),       beta = d/(P*alpha+d),
    F = d*M^2,       R = M*(P*u_min+d*M).

For `n>=1`, `R_n` is the set of terminal laws from all length-`n` joint input
laws with these exact one-coordinate marginals. `R_*` denotes their union over
positive finite horizons. `TV` is half the L1 distance.

## 2. Rounding an entire correlated history without accumulating time error

Take any attainable terminal law `p` at a fixed horizon `n`. Scale its layered
automaton flow by `P`: the labelled transition `(t-1,s,a)` has flow
`P Pr(S_{t-1}=s,X_t=a)`. Add one edge from each final state to a common sink,
with flow `P p(s)`. All node balances are integers: the source supplies `P`,
the sink consumes `P`, and all other balances are zero. Distinct letters with
the same successor remain parallel edges.

Here is a direct rounding proof. Among the nonintegral edges, every incident
vertex has degree at least two, since a single fractional incident edge would
contradict its integer balance. There is therefore an undirected cycle; a pair
of parallel edges is a permitted cycle. Push flow around the cycle with signs
from edge orientation, until one further edge first reaches its floor or
ceiling. This preserves balances and all original floor/ceiling intervals.
Repeat until no fractional edges remain. A loop can be rounded alone. This is
a finite constructive proof, with at most the original number of fractional
edges cycle adjustments.

The resulting integral acyclic layered flow decomposes into `P` complete
words. At each time `t` and letter `a`, summing the errors of at most `d`
labelled edges gives

    |c_t(a)-P*mu(a)| <= d.

The explicitly included final-to-sink edges give

    TV(p,g) <= r,

where `g` is the empirical terminal law of the `P` words. There is no factor
`n`: the entire flow was rounded jointly, including its terminal edges.
The executable `round_layered_flow` implements the cycle operation for a
supplied finite rational word mixture; it does not purport to acquire an
arbitrary unknown original coupling.

## 3. Complete graph enumeration without a redundant vertex factor

A histogram is `x in N^d` with `sum_s x_s=P`. For every weak composition of
`P` into `d*m` cells `k_{s,a}`, compute

    x_s = sum_a k_{s,a},
    y_t = sum_{s,a:f(s,a)=t} k_{s,a},
    c_a = sum_s k_{s,a}.

Keep the arc `x->y` exactly when `|c_a-P*mu(a)|<=d` for all letters. Keep one
allocation per ordered pair `(x,y)`, since terminal reachability only needs
existence of an allocation. There are exactly `B` candidates, not `H*B`:
each candidate already determines its source histogram. There are `H` vertices
and `E<=min(B,H^2)` distinct arcs.

Let `G_{P,n}` be terminal empirical laws reachable in exactly `n` steps from
`P delta_s0`, and let `G_P` be their positive-length union. Whole-flow rounding
proves that every `p in R_n` has `g in G_{P,n}` with `TV(p,g)<=r`.

For unbounded horizons, deleting cycles from a graph path gives a path of
length at most `H-1` when the final histogram differs from the initial one.
A positive return to the initial histogram needs a nonempty cycle, of length
at most `H`. A zero-step word cannot substitute for it. The solver implements
a fresh dummy start pointing to the original start's outgoing neighbors;
ordinary reachability from that dummy preserves this positive-length rule.

## 4. One shared quantile seed repairs every coordinate exactly

For a graph trajectory, let its empirical letter marginal at time `t` be
`c_t(a)/P`. Put

    q_t(a) = [mu(a)-(1-beta)c_t(a)/P]/beta
           = ((P*alpha+d)mu(a)-alpha*c_t(a))/d.

The upper discrepancy `c_t(a)<=P*mu(a)+d` implies

    (P*alpha+d)mu(a)-alpha*c_t(a)
       >= d*(mu(a)-alpha) >= 0.

The `q_t` sum to one. Their common-denominator numerators are

    v_t(a) = P*u_min*u_a + d*M*u_a - M*u_min*c_t(a),
    q_t(a)=v_t(a)/F,              sum_a v_t(a)=F.

Choose **one** uniform integer `J in {0,...,F-1}`. At every time use the same
`J` and output the inverse-CDF letter under `q_t`, with a fixed letter order.
That letter has marginal `q_t` at each coordinate; independence is unnecessary.
Mix the empirical `P`-word law with this filler law in weights `1-beta,beta`.
Every coordinate marginal is now exactly `mu`, since

    (1-beta)c_t(a)/P + beta*q_t(a) = mu(a).

The terminal law `p'` obeys `TV(p',g)<=beta`, whatever filler terminal states
occur. Thus, for every fixed `n`,

    d_H(R_n,G_{P,n}) <= max(r,beta).

The same argument after loop deletion gives a positive witness horizon at
most `H` for every member of `G_P`. It follows that

    d_H(closure(R_*), R_{<=H}) <= r+beta.

Taking `P=ceil(2d/(alpha*epsilon))` makes `r+beta<=3epsilon/4`.

There is also a single uniform seed for the **whole** corrected coupling:
choose `Z` uniformly from `0,...,R-1`. Its first `P*M*u_min` values form `P`
blocks of size `M*u_min`, one block per empirical word; its remaining `F`
values correspond one-to-one with quantile seeds `J`. If `c_t(a)` empirical
words have letter `a`, the exact number of whole-coupling seeds outputting `a`
at coordinate `t` is

    M*u_min*c_t(a) + v_t(a)
      = u_a*(P*u_min+d*M)
      = R*mu(a).

These are exact integer quotas at every position, including at a binary
encoded horizon. Seed length is independent of `n`.

## 5. Binary horizon and balanced witness DAG

For supplied positive binary `n`, let `A` be the Boolean adjacency matrix.
Compute `A^(2^j)` by squaring for `0<=j<bitlength(n)`; combine the set-bit
powers to find all exactly length-`n` terminal histograms. Minimize the exact
rational quantity `TV(nu,x/P)` over those histograms. No `n`-step simulation
is used.

For a witnessed matrix entry `(A^(2^j))_{x,y}=1`, choose a midpoint `z` with
`(A^(2^(j-1)))_{x,z}=(A^(2^(j-1)))_{z,y}=1`. Recursively join the two halves.
Memoize nodes indexed by `(j,x,y)`. Base nodes carry one actual graph allocation.
Join the set-bit blocks using a balanced concatenation tree. If `W` is the
node count and `L` the number of distinct leaf allocations, then

    W <= H^2*bitlength(n) + bitlength(n)-1,
    L <= E <= H^2,
    depth <= bitlength(n) + ceil(log2(bitlength(n))).

Source and target histograms and binary segment length are checked at every
node. The DAG describes an actual path, not just an asserted reachable pair.

## 6. Canonical slots make every empirical coordinate query consistent

Represent a histogram `x` by `P` canonical slots, grouped by state order.
For a leaf allocation, divide the source-state slots consecutively by letter
order according to `k_{s,a}`. Assign each such slot the indicated letter. Its
destination slot is in the appropriate successor-state block, ordered by
incoming `(s,a)` pair. This constructs a bijection `pi_e` on `P` slots and a
letter array `lambda_e`. Repeated edges use the same canonical assignment.

At an internal node with left and right children, precompute

    pi_node = pi_right o pi_left.

Start with a uniform empirical slot `I`. To query coordinate `t`, descend the
DAG. When descending right, update `I <- pi_left(I)` and subtract the left
length; when descending left keep `I`. At a leaf return `lambda_e(I)`.
This exactly tracks the same particle through the entire witness. A bijection
preserves the uniform slot law at every boundary, so the leaf allocation has
its intended letter counts and terminal histogram. The quantile branch uses
the same descent but ignores slot permutations and returns the letter
determined by its fixed `J`.

The original seed determines the complete word. Repeated queries and queries
in arbitrary order are consistent without a cache or fresh randomness. After
permutation preprocessing, each query takes `O(log n)` node/array operations,
plus `O(m)` inverse-CDF work at its leaf. Emitting all `n` coordinates still
requires at least `n` outputs; the compiler does not remove that cost.

## 7. Exact terminal law without enumerating quantile seeds or word positions

Every occurrence of a given leaf allocation has the same filler law `q_e`.
Take the union of all its cumulative integer thresholds, together with `0,F`.
There are at most

    K <= min(F, 1+(m-1)*L)

nonempty integer intervals. On each interval every leaf emits a fixed letter.
For a representative `J`, assign leaf `e` the state map

    T_e(s)=f(s,letter_e(J)).

At an internal node put `T_node=T_right o T_left`. Applying the root map to
`s0` gives the exact filler terminal state for every seed in that interval.
Sum its interval size into a terminal count `b_s`; then `sum_s b_s=F` and

    p'(s) = (M*u_min*x_s+b_s)/R.

This is an exact rational terminal law with a denominator independent of `n`.
Its computation does not enumerate the `F` possible seeds or `n` positions.
The whole input-word law has support at most `P+K`: one word per empirical
slot and one per quantile interval, with possible duplicates reducing support.
For a single sampled `J`, the terminal state costs one DAG map evaluation;
it has no interval factor `K`.

## 8. Optimization guarantees and certificate distinction

For either a fixed horizon or the positive unbounded union, write

    v = inf_{p in R} TV(nu,p),
    v_P = min_{g in G} TV(nu,g).

The two directed approximations give

    max(0,v_P-r) <= v <= min(1,v_P+beta).

The exact repaired witness also gives the often tighter feasible upper bound

    v <= TV(nu,p').

The program outputs both the graph-only interval and the tightened interval.
No exact cutpoint or exact closure-membership decision follows from arbitrary
precision alone. Under a promised gap `v<=a` versus `v>=a+gamma`, choosing
`P=ceil(4d/(alpha*gamma))` gives `max(r,beta)<gamma/3`, and comparison of
`v_P` with `a+gamma/2` decides the promise.

**Local certificate verification** checks integer leaf allocations, discrepancy
budgets, DAG endpoints/lengths, exact coordinate-repair equations, permutations,
quantile intervals, and exact terminal counts. It certifies an actual feasible
coupling and its attained objective. It does not by itself certify the global
finite-graph minimum, and therefore does not by itself establish the lower
bound on `v`. The verifier's separate `recompute_optimum` mode reconstructs the
entire graph and exact-length reachability and checks `v_P`; the receipts say
explicitly when that replay was performed. No short global optimality
certificate is asserted.

## 9. Explicit resource and precision accounting

Let `b=ceil(log2(P+1))`, `a=ceil(log2(M+1))`, `h=ceil(log2(H+1))`, and
`t=bitlength(n)`. Let `L_in` include the binary transition-table encoding,
all rational numerators and denominators, and the target law. The common
denominator has `a<=L_in+1` because `log lcm <= sum log denominator`.

| Operation | Arithmetic/Boolean work | Stored information |
| --- | --- | --- |
| Acquire/validate supplied model | polynomial in `L_in` | `L_in` bits |
| Enumerate graph | `B * poly(d*m,b+a+log d)` bit work | `H*d*b + E*d*m*b` bits, up to dictionary overhead |
| Positive unbounded reachability | `O(H+E)` graph operations | `O(H*d*b+E*d*m*b+H*h)` bits including graph |
| Binary horizon reachability | `O(H^3*t)` Boolean operations; `O(H*W)` midpoint search fits this bound | `O(H^2*t)` packed Boolean power bits in addition to graph |
| Slot permutations | `O(P*W)` integer-array operations | `O(P*W*b)` bits |
| One coordinate | `O(t+log t+m)` node/array/integer operations | fixed seed `O(log R)` bits plus a descent workspace; no query cache |
| One sampled filler terminal | `O(m*L+d*W)` map operations | `O(d*W*log d)` temporary map bits |
| Full exact terminal law | threshold sorting plus `O(K*(m*L+d*W))` map operations | same map workspace plus `O(K*log F+d*log R)` bits |

Map entries use `log d` bits; slots use `b` bits; coordinate/segment lengths
use `t` bits; probability numerators and denominators use
`O(b+2a+log d)` bits, independent of `n`. These are explicit arithmetic-operation
counts with explicit operand lengths, not unit-cost arithmetic on arbitrary
reals. Ordinary binary integer arithmetic yields polynomial bit overhead.
Matrix powers can be recomputed to save memory; the executable stores them.

The certificate omits internal permutation arrays because they can be
reconstructed. Its bit length is bounded by

    O(W*(d*b+t+log W) + L*d*m*b
      + L*m*log F + K*(log F+log d) + L_in).

This is polynomial in the explicit graph parameters and `log n`; it is not
necessarily polynomial in the original rational input size. Small `alpha`
can make `P` exponential in the input bit length, and variable automaton size
makes `H,B` large. For fixed `d,m,alpha` and accuracy, preprocessing and exact
terminal evaluation grow polynomially in `log n`; fixed `d,m,alpha` also make
the graph polynomial in `1/epsilon`.

**Exact random-bit source.** The public `Witness.sample(getrandbits)` uses one
uniform integer in `[0,R)`. Draw `k=ceil(log2 R)` fresh fair bits and reject
values `>=R`. Acceptance probability is greater than `1/2` unless already
exactly one; expected requests are below two and expected fair bits below
`2k`. Worst-case requests are unbounded. The method reports bits requested,
request count, and rejected integers, and returns the reusable branch/seed and
its exact terminal state. Default `secrets.randbits` is an operational source;
mathematical exactness assumes the stated fresh independent fair-bit contract.
Seeded PRNG receipts are reproducible demonstrations, not evidence that their
source is an ideal fair-bit stream.

**Polynomial space.** For a rational promised terminal gap, `log P` is
polynomial in `L_in+log(1/gamma)`. A histogram is `O(d*b)` bits; an allocation
is `O(d*m*b)` bits. Adjacency is decidable by enumerating the `B` weak
compositions in this workspace, so there is no adjacency oracle. Unbounded
positive reachability on the implicit `H+1` graph has Savitch space
`O((d*b)^2+d*m*b+L_in)`, using the dummy start described above. Histograms and
exact objective fractions can be enumerated in polynomial space. Thus the
promised gap problem is in PSPACE. With supplied binary `n`, a nondeterministic
`n`-step graph walk stores only one histogram, one allocation, and a `t`-bit
counter; NPSPACE=PSPACE gives the same upper bound polynomial in
`L_in+log(1/gamma)+t`. This space result does not promise an efficiently emitted
explicit witness or include the explicit permutation compiler in polynomial
space. No PSPACE lower bound is claimed here.

## 10. Executable receipts and limits

Run from this directory or use the absolute file paths:

```sh
python3 dfa_checks.py
python3 dfa_solver.py solve dfa_noncommutative.json result.json --horizon 1000000000000
python3 dfa_solver.py verify dfa_noncommutative.json result.json
```

The interface validates exact rational strings and rejects JSON floats.
The implementation defaults to a two-million-candidate resource guard and a
500-bit horizon recursion guard. These produce `RESOURCE_LIMIT_UNKNOWN`, not
a false negative; `--max-allocations 0` disables the first guard.

Focused receipts in `dfa_checks.json`:

* Three states, noncommuting transitions, non-point target, and an explicitly
  removed zero-support letter: `P=12,H=91,B=6188,E=779`. A trillion-step witness
  uses 111 nodes, eight leaf allocations, two quantile intervals, 14 word atoms
  at most, and a single uniform seed of denominator 36. Its exact terminal law
  is `(1/2,1/3,1/6)`. The target is `(1/4,1/2,1/4)`, attained TV is `1/4`, and
  the certified optimum interval is `[0,1/4]`. The finite check does not assert
  that this witness is optimal among exact-marginal couplings.
* Positive return fixture: the optimum witness has length two, and its terminal
  law is exactly the initial state. It excludes a zero-step substitution.
* Nondegenerate marginal `(1/3,2/3)` and parity transitions at a trillion steps:
  `P=32,H=33,B=6545,E=33`, 53 DAG nodes. Target `(1/3,2/3)` has exact attained
  distance `2/3`; the graph-only interval `[61/96,47/57]` tightens to
  `[61/96,2/3]` by exact terminal evaluation.
* Layered flow rounding starts from two words with probabilities `1/2,1/2`
  and population three. Two cycle adjustments preserve every integer balance
  and every edge floor/ceiling interval; terminal TV is `1/6`. Original and
  rounded words, terminal counts, and every coordinate discrepancy are saved.
* Short witnesses additionally expand all empirical and quantile-interval
  atoms and evaluate the resulting words directly. Huge witnesses use the
  finite DAG verification; their positions are not silently materialized.

The theorem does not impose stationarity, ergodicity, input independence, or
an external stochastic transition-noise law. Its time-homogeneous identical
coordinate marginal is needed for cycle deletion. Position-varying marginals
can be handled at a supplied finite horizon with a layered graph, but the
unbounded homogeneous cutoff does not automatically extend. Exact cutpoints,
historical priority, and major-problem implications require separate arguments.
