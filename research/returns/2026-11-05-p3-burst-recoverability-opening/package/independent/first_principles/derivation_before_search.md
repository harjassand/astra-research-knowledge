# First-principles construction before literature search

Date: 5 November 2026. This route is independent of other tournament proposals.

## Candidate question

Can private logical-to-physical reassignment turn an otherwise arbitrarily
correlated, budgeted physical fault field into a provable useful-computation
interface at fixed local interaction strength, finite signal velocity, and bounded
resource cost per logical operation? The question is whether the missing
correlation contract can be produced operationally rather than inferred from
unrestricted finite records.

## Exact opening

Let F be any fixed set of m bad physical sites among N. F is fixed before a
uniform private permutation Pi is sampled. Logical role i is assigned to physical
site Pi(i). For any k distinct logical roles S,

  P(Pi(S) subset F) = (m)_k/(N)_k <= (m/N)^k.

Here (x)_k is the falling factorial. Thus arbitrary spatial arrangement of the
bad sites becomes a local-stochastic support bound in logical coordinates. The
claim is a single-round spatial bound; reusing one permutation does not produce
a local-stochastic bound over repeated temporal faults. The
same bound holds for a random F provided it is independent of the private
permutation and |F| <= epsilon N almost surely. It is not implied merely by
E|F| <= epsilon N: the distribution F=all sites with probability epsilon and
empty otherwise gives probability epsilon, not epsilon^k.

For a logical block of n roles, its number Z of bad sites is hypergeometric.
For any alpha>epsilon,

  P(Z >= alpha n) <= exp[-n D(alpha || epsilon)].

One elementary proof uses the negative dependence of sampling without replacement,
which also follows by expanding the product generating function and bounding
P(all sites in any prescribed subset bad) by epsilon^k. This gives
E exp(tZ) <= (1-epsilon+epsilon exp(t))^n for t>=0 and the Chernoff bound.

If a component code corrects any alpha n adversarial faults, a private assignment
produces exponentially small block failure despite arbitrary physical correlations
inside the fixed fault set. To serve L blocks for R independently refreshed rounds,
a union bound needs n >= log(LR/delta)/D(alpha||epsilon), assuming each round's
fault set is fixed before that round's fresh assignment. The entire fault field
may depend on earlier history. Correcting faults need not cost an independence
assumption, but coding, state transport and reliable permutation-control remain
physical operations.

## Strict information-order boundary

If the fault field can be selected after learning Pi, take F=Pi(S) for a chosen
logical block S with |S|<=epsilon N. Then that block fails with certainty. Private
random bits matter only while the physical choice of F cannot respond to them.
No claim about arbitrary reactive noise follows.

## Physical geometry bill

On a d-dimensional bounded-degree grid with N sites at constant density, a uniform
permutation sends a constant fraction of roles a distance Omega(N^(1/d)). If an
existing unknown state is moved to implement that permutation and propagation
speed is bounded by v, implementation time is Omega(N^(1/d)/v). Equivalently, with
fixed per-edge transport capacity, a hyperplane bisection carries Omega(N) roles
through O(N^((d-1)/d)) edges, requiring Omega(N^(1/d)) communication rounds.
The total transport-distance bill is Omega(N^(1+1/d)). Logical relabeling on paper
does not evade this when useful gates must follow the logical graph: gate routing
then bears the nonlocal communication bill. Initial assignment can avoid moving
preexisting data only if preparation and subsequent interaction geometry support it.

Thus the immediate construction buys an error-law transformation, but not a
constant-overhead local computer. The central operation is a routing/encoding
architecture that preserves the private information order and useful throughput
while paying its geometry and its own faults. A strong completed result would be
an attainable sharp tradeoff between noise correlation length/response time,
private reassignment scale, code redundancy, latency and energy.

## Possible fatal ordinary comparator

Random interleaving and coding against an oblivious adversary may already provide
the exact mathematical consequence. Error-correcting codes that directly correct
a bounded total fraction of errors may render randomized assignment unnecessary.
This must be checked before selecting this as a new foundational question.
