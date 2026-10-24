# A certified reaction interface after an unresolved total count

New work in this Pro3 continuation. The operation conditions on a total
number of reactions in a known time window when the reaction products do
not identify their source modules. It retains the resulting correlated
entrance law as a positive count-accumulator tensor train, together with a
pointwise relative certificate usable under later conditioning.

Tensor trains, finite-state accumulators, and cardinality inference are
established machinery. This construction uses those methods; it does not
claim to invent them. The scientific object is the source-obtained,
conditioning-stable posterior and its admitted later operations. The
companion `conditioning_stable_entrance.md` proves the projective certificate
and the local count-resolved propagator used below.

## 1. Source, entrance and observation contracts

There are finite local hidden-state spaces E_1,...,E_n. During the observation
window of duration T, the physical source is a product of local continuous-time
Markov processes. For local module i, let A_i be its subgenerator with counted
reactions removed but their hazard retained as killing, and let J_i be the
nonnegative counted-reaction/reset matrix. A_i+J_i is a conservative generator.
Every counted reaction changes only its own module.

A shared public controller or phase is known throughout the window. There
are no unobserved common resets, event-dependent shared phase changes, or
hidden cross-module reactions during the window. Known external schedules
can be admitted with corresponding local time-dependent propagators, but
the formulas here use constant local generators within the window.

The acquired normalized entrance law is supplied exactly as

    nu = sum_{r=1}^R w_r tensor_i mu_(r,i),
    w_r>=0, sum_r w_r=1, mu_(r,i)1=1.

The weights and local factors in the implemented operation are rational.
The exact physical entrance is related to this acquired entrance by a
previously obtained measure sandwich. Its projective spread is denoted
R_0>=1. This certificate is substantive; the operation does not infer an
arbitrary correlated entrance from a list of its marginals.

The observed quantity is

    N_1(T)+...+N_n(T)=K,

where K is a specified nonnegative integer and N_i counts the selected local
reaction. Individual N_i, event timestamps, and the global event ordering are
unobserved. The window endpoint is known. A finite total-count probability
that is positive is required for conditioning.

## 2. Local obtaining step

For k>=0 define

    B_(i,k)(T) = [z^k] exp(T(A_i+z J_i)),
    v_(r,i,k) = mu_(r,i) B_(i,k)(T).

The row vector v_(r,i,k)(x_i) is the joint probability, for component r, of
k local reactions and final local state x_i. Its entries are nonnegative.

To obtain all k<=K, augment module i by a local counter 0,...,K. The augmented
subgenerator has A_i on its diagonal blocks and J_i on its first upper block
diagonal; excess counts beyond K are killed. The initial-layer to layer-k
block of its exponential is B_(i,k). The construction has |E_i|(K+1) local
states and need not enumerate any product of different modules' states.

Obtaining B_(i,k) separately for each k is also correct. A common augmentation
can share work across k. Local matrix and numerical costs must be counted.
The dependence on the numeric value K is explicit; this is not a claim of
complexity polynomial in log K.

Positive uniformization gives entrywise enclosures of these matrices. A
finite truncation with a geometric Poisson-tail bound is detailed in
`conditioning_stable_entrance.md`, Section 6.2. The tail concerns numerical
evaluation of the finite local exponential. Counts above K need not be
approximated or enumerated, because they cannot contribute to a total of K.

## 3. Exact posterior and positive count-accumulator representation

The unnormalized acquired joint law of final states x and count allocation k
is

    F_K(x,k) = 1_{sum_i k_i=K}
               sum_r w_r product_i v_(r,i,k_i)(x_i).

Its hidden-state marginal is

    F_K(x) = sum_r w_r [z^K]
               product_i (sum_{k=0}^K v_(r,i,k)(x_i) z^k).             (1)

The normalizing constant is F_K1. Independence holds conditional on the
entrance component r, so the exact local joint probabilities multiply;
summing the unobserved allocations proves these formulas.

Expanding (1) as a positive mixture of product laws would introduce as many
as binomial(K+n-1,n-1) count allocations per entrance component. The
following representation sums them without listing them.

For each r use a carry index c=0,...,K and define a nonnegative core matrix
for each local final state:

    G_(r,i)(x_i)[c,d] = v_(r,i,d-c)(x_i)   if 0<=c<=d<=K,
                       0                 otherwise.

Let e_c be the carry basis vector. Then

    F_K(x) = sum_r w_r e_0^T
                G_(r,1)(x_1)...G_(r,n)(x_n) e_K.                    (2)

### Theorem 1: finite count-interface representation

For a fixed observed total count K, the exact acquired posterior has a
positive tensor-train representation of bond dimension at most K+1 per
initial mixture component. There are at most R such components. They can
also be represented by a single block-diagonal tensor train with bond
dimension at most R(K+1).

**Proof.** A nonzero term in the matrix product has a carry sequence
0=c_0<=c_1<=...<=c_n=K. Its increments k_i=c_i-c_(i-1) are exactly one
allocation of K among the modules. Conversely every allocation defines
exactly one such carry sequence. The term is product_i v_(r,i,k_i)(x_i).
Summing carry paths gives (1). All core entries are nonnegative. QED.

The carry is an algebraic index that accumulates counts across the chosen
ordering of modules. It is not the physical ordering of reaction events.
The label r is a representation index, not an observed physical variable.
The increments k_i, however, are the physical unobserved per-site counts.

An explicit dense core would store O((K+1)^2 |E_i|) entries. Here its upper
diagonals repeat the same increment vectors, so storing only v_(r,i,k) uses

    O(R(K+1) sum_i |E_i|)

scalar entries. Arithmetic bit lengths, local generator data and certificate
data are additional costs. No TT rank is claimed minimal.

## 4. Exact convolution and scientific queries

For a product test g(x)=product_i g_i(x_i), set

    h_(r,i,k) = sum_x v_(r,i,k)(x) g_i(x).

The unnormalized query is the coefficient of z^K in
sum_r w_r product_i sum_k h_(r,i,k)z^k. For each r compute it by

    d_0(0)=1, d_0(c)=0 for c>0,
    d_i(c)=sum_{k=0}^c d_(i-1)(c-k) h_(r,i,k),
    query=sum_r w_r d_n(K).                              (3)

The normalizer is the same calculation with every g_i=1. A direct truncated
convolution takes O(R n K^2) arithmetic operations, beyond obtaining the
h entries. It uses O(K) working memory per component. Faster polynomial or
tree-based cardinality contractions are possible incumbents; the direct
algorithm is chosen for transparent exact arithmetic, not claimed optimal.

This computes local marginals, arbitrary product guards, joint patterns on
specified modules, and products of future local survival probabilities. It
does not require enumerating the physical configurations or the count
allocations. A sum of finitely many product queries is evaluated by linearity.

The same contraction permits a test g_i(x_i,k_i), by including it when
forming h_(r,i,k). Thus the representation can answer questions about the
unobserved physical allocation, for example whether site i produced any
reaction, or the conditional expected number it produced. This requires
retaining the increment coefficients, as the implemented representation
does. It is not permission to treat the artificial mixture label r as an
identified physical cause.

## 5. Obtaining a relative numerical certificate before global expansion

Suppose local arithmetic produces componentwise enclosures

    0<=l_(r,i,k)(x)<=v_(r,i,k)(x)<=u_(r,i,k)(x),
    u_(r,i,k)(x)<=c_(r,i) l_(r,i,k)(x)

for all required k<=K and x. One sufficient choice is

    c_(r,i) = max_{k,x} u_(r,i,k)(x)/l_(r,i,k)(x),

over positive lower entries, with any shared structural zeros handled
exactly. If a required upper entry is positive while its lower entry is
zero, this ratio certificate has not been obtained. More terms, more
precision, a structural support argument, or another method is needed.

Keep the mixture weights w_r exact. Define

    c_r = product_i c_(r,i),
    c_num = max_r c_r.

Build L_K by replacing every v with its lower vector l in F_K. Then

    L_K(x,k) <= F_K(x,k) <= c_num L_K(x,k).               (4)

**Proof.** For a fixed r,x,k, multiply the nonnegative local inequalities.
Summing over r preserves the lower and common upper bounds. Restricting to
sum k_i=K and summing allocations also preserve them. QED.

Thus the same bound holds for the hidden-state marginal. In particular,
positive coefficient extraction has not introduced an allocation-count
factor into the relative error. The bound is available from local factors
and does not require examining every global configuration.

If the exact physical entrance and acquired entrance have projective spread
R_0, applying their common joint count/state operator, followed by (4), gives
an output spread at most

    R_total = R_0 c_num.                                 (5)

After conditioning on total K, the posterior-TV upper is

    (sqrt(R_total)-1)/(sqrt(R_total)+1).                  (6)

The bound holds for the joint physical count-allocation/final-state law as
well as its final-state marginal: the entrance sandwich is propagated by
the same positive joint kernel before the allocations are marginalized.

It survives every common exact later positive operation, including further
conditioning. There is no inverse probability of the observed total-count
event in (5) or (6). New later numerical errors still need their own relative
certificates. The result does not make a TV-only initial certificate into a
relative one.

For an event A with acquired posterior probability q, the same spread gives
the sharper probability enclosure

    q/(q+R_total(1-q)) <= P_true(A)
                      <= R_total q/(1-q+R_total q).       (6a)

Indeed, the relative order bounds the ratio of the two A masses by the same
constants as the ratio of the two complement masses, so the true odds differ
from the acquired odds by at most R_total. This gives useful relative
accuracy even for an event much rarer than the posterior-TV upper bound.
The limiting values q=0 and q=1 are fixed by common support. With an interval
for q, use the lower endpoint in the monotone lower formula and the upper
endpoint in the monotone upper formula, with outward arithmetic.

For a normalized acquired input nu and no separately evaluated entrance
mass calibration, if Z_L=L_K1, the true total-count probability belongs to

    [Z_L/R_0, Z_L R_0 c_num].

A tighter calibrated initial sandwich can replace these conservative
multipliers, exactly as in `conditioning_stable_entrance.md`.

## 6. Exact rational retained law by integer coefficient rescaling

The numerical executor selects rational lower entries l_(r,i,k)(x). For
each r,i choose a common positive integer denominator D_(r,i) so that

    a_(r,i,k,x)=D_(r,i) l_(r,i,k)(x)

is a nonnegative integer for every k,x. This is an exact change of scale.
Let

    C_r=[z^K] product_i sum_{k=0}^K
                             (sum_x a_(r,i,k,x)) z^k,
    z_r = w_r C_r / product_i D_(r,i),
    Z_L = sum_r z_r,
    alpha_r = z_r/Z_L.

The coefficients C_r are computed by exact integer convolution. Components
with C_r=0 contribute no mass and can be dropped. For the remaining
components define the normalized joint law

    T_r(x,k) = 1_{sum_i k_i=K} product_i a_(r,i,k_i,x_i) / C_r.

Then the acquired posterior is exactly

    Q_K(x,k)=sum_r alpha_r T_r(x,k).                      (7)

Its weights sum to one exactly. The integer coefficients, C_r and rational
alpha_r identify the complete retained probability object. The local
denominators cancel inside T_r, while their effect on component masses is
retained in alpha_r. Dropping that mass factor would change the law.

For a binary product guard, the numerator of each T_r query is an integer
coefficient contraction and the result is an exact rational. Query
evaluation with later transcendental propagators instead requires its own
outward arithmetic. A numerical query enclosure and the existence of the
serialized exact law are distinct pieces of evidence.

## 7. Closure for later local operations; repeated coarse windows

The count-interface tensor train can be reused under a common product
operator B=tensor_i B_i on the physical state. Replace its local vectors by

    v'_(r,i,k)(y)=sum_x v_(r,i,k)(x) B_i(x,y).

This changes only the physical index of each core. The count carry remains
0,...,K, so the bond bound K+1 is unchanged. This covers local propagation,
site-resolved count windows, and known-time local observations or product
resets whenever their source conditions make the global operator a product.
Exact product guards likewise preserve the carry. After normalizing the
updated core contraction, the correlated law can be passed to another such
operation. The mathematical closure is proved here; a generic executor for
every such later operation is not claimed merely from a query demonstration.

A second unresolved-total-count window is different. Its local kernels have
another count index, and enforcing both observed totals introduces another
carry. For totals K_1,...,K_m, a direct exact construction has a carry tuple
with at most

    product_{j=1}^m (K_j+1)

states per mixture component. Additional structure or a separately certified
compression may reduce this, but no bound independent of the number of
coarse windows has been proved here. Exact filtering may retain the same
entrance spread while its representation grows.

## 8. Finite-state observation automata

The count accumulator is one instance of a broader positive observation
interface. Suppose each module produces a local finite summary s_i in an
alphabet Sigma_i, with nonnegative local joint rows v_(r,i,s_i)(x_i).
These can describe a capped count, a count residue, whether any event
occurred, a local finite-state record observer, or a function of the final
local state. Each such row must be obtained from the local source with its
own evaluation certificate.

An observation likelihood on the summaries is supplied by nonnegative
m-state automaton matrices W_(i,s), initial row lambda and terminal column rho:

    g(s_1,...,s_n)=lambda W_(1,s_1)...W_(n,s_n) rho.

For a Boolean observed predicate, a deterministic automaton with an accepting
indicator rho ensures g is exactly zero or one. A general nondeterministic
automaton can count multiple accepting paths, so its path sum cannot be
silently treated as a Boolean indicator. Nonnegative weighted automata are
admissible when their computed function is the actual intended likelihood.

The resulting hidden-state cores are

    G_(r,i)(x)=sum_{s in Sigma_i} v_(r,i,s)(x) W_(i,s),

and the unnormalized observation-conditioned law is

    sum_r w_r lambda G_(r,1)(x_1)...G_(r,n)(x_n) rho.

Expanding the matrix product proves this identity directly. Its bond is at
most m per entrance component. It has the same positive order certificate
as (4) if local summary rows have common relative bounds and the automaton
weights are exact. There is no extra error factor for the number of accepted
summary sequences.

Useful examples include parity with two carry states, threshold counts with
a saturating counter, and finite-state logical constraints on which modules
emitted a product. A local indicator of whether any reaction occurred can be
obtained by a two-state saturating event flag attached to that module; it
need not be evaluated by subtracting nearly equal total and zero-count
probabilities. Count residues similarly use a local cyclic counter.

This extension is a proved representation algorithm. The concrete new code
implements the total-count specialization, not a generic automaton compiler.
Obtaining a small automaton for an arbitrary observation predicate is not
assumed free, and some predicates require large automata for a given module
ordering.

## 9. Why changing the representation matters

Even a simple fixed-cardinality posterior can require exponentially many
positive product components. On n binary variables, consider the uniform
law on the configurations with exactly K ones, for 0<K<n. Any positive
product component supported on this set must be a point mass: if one of
its factors gives positive probability to both zero and one, holding the
other factor choices fixed yields two configurations with different counts,
one outside the allowed support. Therefore every positive product-mixture
representation requires at least binomial(n,K) components.

The same law has the count-accumulator representation of Section 3 with
bond K+1. This elementary representation separation explains why a coarse
observation can destroy fixed positive-product-mixture width while leaving
a compact positive tensor train. It does not prove that this tensor train
is minimal or that every reaction posterior has a small tensor network.

### A support lower bound for the actually retained joint law

The executed binary turnover model has strictly positive activation,
deactivation and turnover rates and a positive observation-window duration.
From either local initial state, every finite turnover count k and either
terminal state have positive probability: a suitable finite alternating
activation/turnover path, followed if needed by a silent state change, has
positive probability in a positive time interval. A path with no turnover
likewise reaches either terminal state. Conditional on a supplied initial
configuration, the modules are independent during this window. Hence every
weak allocation

    k_i>=0,  sum_i k_i=K

has positive probability in the joint count/state law, for any nonzero
nonnegative initial mixture. The implemented local lower factors are also
positive at every (k_i,x_i), so the retained rational law has the same
allocation support.

Consider any exact nonnegative CP representation of this JOINT law, with
each local factor defined on (k_i,x_i). Every nonzero product component must
itself have support inside sum_i k_i=K, because nonnegative summation cannot
cancel mass outside that set. Within one component, if one local factor
supported two different count values, fix any supported value in every
other factor. The two resulting global count sums differ, so at least one
lies outside the allowed set. Therefore each product component fixes one
count value at each site and covers only one count allocation. All weak
allocations have positive mass, so the number of components is at least

    binomial(K+n-1,n-1).

For the executed n=24, K=8 law this is binomial(31,8)=7,888,725. The bound
does not depend on the rank of the initial mixture. The retained 256-component
counter representation instead uses bond 9 within each component. This is
a concrete restriction on representation by nonnegative product mixtures;
it does not assert a matching lower bound on every other tensor format.

The same obstruction applies to any nonnegative CP approximation Q that
admits a finite relative certificate

    a Q <= M <= b Q,     0<a<=b<infinity,

for this true joint law M. The inequalities force identical supports:
M=0 implies Q=0, and M>0 implies Q>0. Such an approximation must therefore
cover every allowed count allocation with components restricted to that
allocation, and also needs at least 7,888,725 components in this example.
This connects the choice of representation to the required guarantee under
arbitrary future positive selection. It is not a lower bound for ordinary
TV-only approximations, which may change support.

All these lower bounds concern the joint retained PHYSICAL COUNTS AND
TERMINAL STATES. They imply no nonnegative-rank lower bound for the endpoint
state marginal obtained after summing out counts. The support argument is
an elementary cardinality observation, not a historical novelty claim.

The meaningful capability is to acquire and preserve the correlations
created by an admitted coarse reaction observation, query them, and carry
their relative certificate into later work. Existing cardinality-inference,
tensor, and network-free methods receive the same source and observations
and may implement this construction. There is no special architecture
necessity claim or claim to outperform every incumbent contraction method.

## 10. Concrete executed specialization

The new `unresolved_count_interface.py` constructs and reloads
`unresolved_count_posterior_24sites.json`. It reuses the already acquired
24-site entrance with 256 positive mixture components, observes a total of
eight turnovers over a half-unit window, and does not observe their allocation.
Its retained object follows the exact integer-coefficient construction in
Section 6. The positive tensor trains have bond dimension nine per mixture
component. There are 216 local increment operators; the largest local
counter augmentation has 18 states. Product configurations and count
allocations are not enumerated.

The completed output `unresolved_count_interface_results.json` reports

    total-count probability in
    [0.161512257992014207599515675136791350901276688,
     0.161512258591113834205093354246416128712287435],

    joint count/state posterior TV at most
    4.63664208016393462417317532333669617002900577e-10,

    later local numerical spread minus one at most 1.36e-42.

The actual retained object supports the following certified queries:

| Query | True probability lower bound | True probability upper bound |
| --- | ---: | ---: |
| Site 0 active at window end | 0.171815376145390109341733731793964116234811170 | 0.171815376673206351311592577747425883499644283 |
| Site 0 supplied at least one of the eight reactions | 0.0700916614584626711339057260398020950971007894 | 0.0700916617002313608356875483168303535849646579 |
| All 24 sites active at window end | 1.94487722531360608083272940987941624833376541e-13 | 1.94487723252776576112434876964293655403108065e-13 |
| All 24 sites active after another 0.1 time units | 2.02990404806026002633018265966144171913465651e-13 | 2.02990405558981086263843958277745647902585654e-13 |

For the last query, the original independent local turnover dynamics continue
without another count observation. The all-active query is an instantaneous
cooperative-probe hazard divided by the probe rate if such a probe is
introduced at that query time. It does not by itself give the whole
first-event law of a cooperative probe acting throughout the interval.

The implementation reloads the serialized law, recomputes its integer
normalizers, verifies the rational mixture-mass identity, and checks the
projective-to-TV conversion. Its separate three-site, total-count-two check
uses a 24-state expanded counter reference with rational positive
uniformization; all eight final-state coordinate enclosures lie inside the
tensor bounds. That small comparison checks indexing and counter direction;
the general certificate comes from the local order proof and enclosures.

The reported outcomes were read from the completed new execution. This proof
does not claim an additional independent rerun. General automaton compilation
and arbitrary sequences of unresolved-count windows remain mathematical
extensions with the scope stated above, not additional executed experiments.

## 11. Primary antecedents and implementation status

- I. V. Oseledets, *Tensor-Train Decomposition*, SIAM Journal on Scientific
  Computing 33(5), 2295-2317, 2011.
  https://doi.org/10.1137/090752286
  https://epubs.siam.org/doi/abs/10.1137/090752286
- Daniel Tarlow, Kevin Swersky, Richard S. Zemel, Ryan Prescott Adams and
  Brendan J. Frey, *Fast Exact Inference for Recursive Cardinality Models*,
  UAI 2012, 824-833. This establishes efficient cardinality marginalization
  and sampling using auxiliary-variable inference; count accumulation is
  an incumbent primitive, not a new discovery claimed here.
  https://proceedings.mlr.press/r10/tarlow12a.html
  https://arxiv.org/abs/1210.4899
- Tianyu Li, Doina Precup and Guillaume Rabusseau, *Connecting Weighted
  Automata, Tensor Networks and Recurrent Neural Networks through Spectral
  Learning*, arXiv:2010.10029v2, 2022; Machine Learning.
  This directly relates weighted automata and tensor-train representations.
  https://arxiv.org/abs/2010.10029v2
  https://doi.org/10.1007/s10994-022-06164-1

The local marked-count primitive and the sharp projective-TV conversion are
attributed separately in `conditioning_stable_entrance.md`. This proof file
contains new derivations and obtaining contracts for their composition.
Numerical execution reports, exact serialized laws, and implemented routines
remain distinguishable from the general mathematical extensions proved here.
