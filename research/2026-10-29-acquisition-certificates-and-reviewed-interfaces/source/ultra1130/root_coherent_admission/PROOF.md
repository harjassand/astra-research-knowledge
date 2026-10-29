# Coherent support admission without positive physical fault flags

29 October 2026. Root construction; independent challenge in progress.
Historical novelty UNKNOWN. These are conditional receiver theorems, not a
physical quantum-memory or fault-tolerant-computation demonstration.

## 1. Input that is actually required

On a finite set V of N labelled fault slots let F_M, M subset V, be one
CONSISTENT family of Hermiticity-preserving linear process maps. For the
fixed experiment, sum_M F_M is the actual CPTP process. All initial
environment registers, interventions and final receivers are included in
the map or admitted as common contractions in its complete strategy norm.
Assume, uniformly over the exogenous schedules used below,

    B(R) = sum_(M superset R) F_M,
    ||B(R)|| <= epsilon^|R|,       R subset V.                 (1)

F_M need not be CP. There is no positive probability law on M in this
assumption. The R=empty bound is just the norm-one physical full process.
Every support assertion below is an additional input; (1) alone does not
assert spatial locality, an ideal reference, or successful error correction.

For disjoint T,Z define a forced/forbidden hybrid by

    H(T,Z) = sum_(M: T subset M, M intersect Z=empty) F_M.

Finite inclusion-exclusion gives the useful exact identity and bound

    H(T,Z) = sum_(U subset Z) (-1)^|U| B(T union U),
    ||H(T,Z)|| <= epsilon^|T| (1+epsilon)^|Z|.          (2)

This explicitly pays the cost of forbidding faults on a boundary. It is
not an assumption that arbitrary normalized conditioned channels are close.

## 2. Cancellation for the component bad event

Fix ANY finite graph H on V, and integer d>=1. Put b(M)=1 if H[M] has a
connected component with >=d vertices, otherwise 0, and define

    a_R = sum_(S subset R) (-1)^(|R|-|S|) b(S).

Boolean inversion gives, as an exact identity of maps,

    sum_M b(M) F_M = sum_R a_R B(R).                        (3)

We have |a_R|<=2^|R|. More usefully, a_R=0 whenever H[R] has even ONE
component of size <d. Proof: g=1-b factorizes on the components C_i of
H[R], and its Mobius coefficient on R is the product of its coefficients
on the C_i. On a component of size <d, g is identically1 on all subsets;
its nonempty coefficient is (1-1)^|C_i|=0. For nonempty R the constant
function has zero coefficient, so a_R(b)=-a_R(g). Also a_empty=0.

Consequently

    ||sum_bad F_M|| <= sum_(R: every H[R] component >=d) x^|R|,
    x=2epsilon.                                            (4)

This is a sum over families of large components. It does not sum arbitrary
benign background faults separately. It holds without factorizing F_M
over disjoint components, and without independent local environments.

## 3. An annealed asynchronous read graph

Seeds j have source supports X_j. Each seed touches at most b>=1 checks;
each check meets at most K>=1 seed supports. Make slots v=(j,k), where k
runs through a finite collection of consecutive time blocks of duration
tau. A support touching the same check more than once still counts once.
Each check has an independent exogenous rate-Gamma Poisson READ process,
independent of noise and of nominal coins. Assume Gamma*tau>=log2.

Z_(a,k)=1 means at least one read OCCURRED in block k. These flags are
independent over a,k and P(Z=1)>=1/2. They do not certify a measurement
outcome, a correct controller bit, or a successful noisy operation.

On all slots define H_Z: two distinct slots are adjacent if they touch
a common check a and there is no block strictly between their block
indices on which Z_(a,k)=1. In the same or adjacent blocks they are
therefore adjacent. Endpoint-block reads are ignored. This overapproximates
every edge between insertion times which lie in one actual uncut check
interval, even when a slot contains arbitrarily many insertions.

Introduce AUXILIARY independent Bernoulli occupancy theta on the slots.
It is solely a device for enumerating graphs and is not a physical fault
law. Force a prescribed set S of r roots occupied. Explore their occupied
components breadth-first. Processing a slot exposes, on each touched check,
its own block and scans left/right up to the first Z=1 block inclusive.
Whenever a block is scanned, reveal ALL previously unknown occupancy
variables for seeds touching that check in that block, and enqueue every
new occupied slot immediately. Cache whole rows, cut flags and occupations.
Roots are already queued and never count as offspring.

Here is the deferred-decision point: a previously revealed zero-read run
contains no hidden candidate occupations on that check; a previously
revealed successful-read block truncates a scan. A scan from a successful
endpoint block may continue on its other side, but that side has fresh
independent flags or another cached boundary. Thus at each processed slot,
the number of fresh blocks is dominated by one own block and two independent
geometric(1/2) variables on {1,2,...}, separately for each of <=b checks.
Occupation exposures from other checks and already queued roots only
decrease the count of NEW children. This is conditional domination under
the exploration filtration, not a claim that full component sizes are
independent.

Set theta=1/(64bK). If Y is the number of new children, put
A=1+3theta and a=A^K. Fresh occupancy independence then gives

    E[4^Y | past] <= a^(3b) (2-a)^(-2b) < 2.               (5)

For an explicit rational certificate, let u=3/(64b). Binomial expansion
gives a<=(1-u)^(-1). Hence the right side is at most

    (1-u)^(-b) (1-2u)^(-2b)
      <= (64/61)(16/13) = 1024/793 < 2.

The last inequalities use (1-z)^m>=1-mz twice. Denominators are positive.
If P vertices have been processed and Q are queued, 2^P 4^Q is a
nonnegative supermartingale, initially4^r, since its next-step conditional
multiplier is E[4^Y]/2. The finite graph makes the stopping time bounded.
Writing C(S) for the union of occupied components of the forced roots,

    E_(Z,occupancy) 2^|C(S)| <= 4^r.                       (6)

This counts vertices, not physical clock precision or actual fault events.

## 4. Rooted polymer enumeration

Suppose x<=theta. Every R appearing in (4) has r>=1 components of size>=d.
Assign its components their distinct least-labelled vertices, the root
set S. For a fixed S, sum over R with exactly one prescribed root per
component. If R minus S is virtually occupied then R is a subset of C(S).
The probability of this inclusion event is theta^(|R|-r). Therefore

 sum_R x^|R| P_Z(R is such a component family)
  <= x^r (x/theta)^(r(d-1))
       E_(Z,occupancy)[number of eligible R contained in C(S)]
  <= x^r (x/theta)^(r(d-1)) E 2^|C(S)|
  <= [4theta (x/theta)^d]^r.                              (7)

The first inequality uses |R|>=rd and x/theta<=1. For each graph and union
R its component partition is unique, so no uncharged partitions appear.
There are at most N^r/r! root sets. Combining (4),(7) yields

 E_Z ||sum_(M: H_Z[M] has component >=d) F_M^Z||
    <= exp[4Ntheta (2epsilon/theta)^d]-1.                 (8)

The maps may depend arbitrarily on the fixed read schedule, provided (1)
holds uniformly for that schedule. No Jensen substitution of an average
single-polymer activity is used. For example epsilon<=1/(256bK) makes
2epsilon/theta<=1/2. Actual Poisson timestamps can be retained in the
conditioning; the coarse flags only overapproximate their components.

## 5. Logical Pauliization, and its exact limit

An additional supported-label receiver hypothesis makes (8) useful. Let
the source be a distance-d_code stabilizer code. Each marked slot supplies
only source Pauli insertions on X_j, with |X_j|<=q. Between insertions the
nominal Kraus operations have ONE Pauli label times a check function;
arbitrary environment coefficients diagonal in source syndrome and
identity on the logical algebra are allowed. Coherent superpositions of
different nominal source Pauli labels are not granted by this premise.
The initial encoder is syndrome diagonal with logical-input-independent
weights. The final Pauli decoder includes check dephasing. Condition on
exogenous schedules/coins only; retain Born records UNNORMALIZED.

For any two bra/ket Pauli words surviving the same read records, their
relative Pauli on EACH actual uncut coherence component commutes with all
checks. Its support is the union of that component's fault supports;
nominal Pauli corrections do not spread the relative label. A component
with fewer than ceil(d_code/q) slots is erasure-correctable, so that
relative Pauli is a stabilizer. This is the same recordwise algebra as
the frozen c_poisson_syndrome_history proof, extended linearly to signed
maps and operator-valued check-diagonal environment coefficients.

Thus every good F_M^Z is invariant under logical Pauli twirling. Let T_L
be that mathematical norm-one CP projector and Lambda the actual final
CPTP logical map, averaged over exogenous schedules. With d=ceil(d_code/q),

 ||Lambda-T_L(Lambda)||_diamond
   <= 2 {exp[4Ntheta (2epsilon/theta)^d]-1}.               (9)

T_L(Lambda) is a physical Pauli channel. If records are retained, it is a
Pauli instrument. This establishes proximity to SOME Pauli channel, not
to the Pauli-twirled microscopic rates, a causal Markov path law, a thermal
distribution, or the identity channel.

In particular, a minimum-weight decoder can turn two physical errors on
the standard perfect [[5,1,3]] code into a nontrivial logical Pauli. Their
two-vertex component is smaller than3. This is consistent with (9) and
disproves an inference from small coherence components to successful
memory. It is not the programme's CSS [[5,1,2]] diagnostic seed.

If a SEPARATE pathwise receiver theorem says every Pauli word on every
good support decodes to the identity, good F_M are scalar multiples of
identity. Trace preservation then instead gives ||Lambda-id||<=2B, where
B is (8). That pathwise premise has not been proved for the native
autonomous controller. A causal-adversary threshold cannot replace it.

## 6. What the Gaussian-memory packet does and does not supply

The frozen b_conventional/clock_memory proof supplies a consistent family
with (1), epsilon=sqrt(2e eta), around EXACT fresh within-slot bath dynamics.
It marks cross-slot covariance insertions. It does not mark every within-
slot data disturbance. Therefore its norm theorem does NOT automatically
supply the supported-label reference premise in Section5. That premise
must be checked on the chosen fresh reference. A generic data bath can
change source Pauli labels in unmarked slots.

Conversely, an exactly check-diagonal CLOCK-only bath is nominal good
dynamics by CLOCK_ALGEBRA.md, including its memory, so it need not be
called a source fault at all. That algebra is useful but does not admit
generic data baths, preparation, cooling bias, or hardware coupling errors.
Equation(9) closes a coherent-to-Pauli norm interface under explicit inputs;
it does not close these physical or classical persistence gates.

## 7. Close established results and the distinct remaining question

AGP, quant-ph/0504218v3 Section11, already uses coherent inclusive fault-path
norm conditions and cancellation to establish concatenated thresholds.
He--Nguyen--Pattison, arXiv2508.08246v2 Section5.3, gives a composable
coherent-error bound with explicit gadget-volume/support-ratio cost.

The stronger fresh prior is Han et al., arXiv2609.20537v1, 17 Sep2026,
AppendicesB.5--B.7 and C.3--C.6. They already prove constant qLDPC CODE
CAPACITY thresholds for local constant-depth coherent and CPTP noise,
with perfect syndrome extraction, using cluster resummation. Their
interpolation factors independent disjoint local channel errors for
optimal recovery; their MW proof resums outside channels before norms.
The generic discovery of cluster cancellation and the static qLDPC
threshold must not be claimed here as new or still unsolved.

The distinct conditional construction above accepts only the consistent
inclusive norm (1), permits nonfactorizing F_M, and pays the annealed
unbounded-degree asynchronous read graph through (5)--(8). The true
remaining technological question is whether a physical reference and a
faulty asynchronous classical recovery operation jointly satisfy its
supported-label and pathwise-correctness premises. UNKNOWN.

Primary links: https://arxiv.org/html/quant-ph/0504218v3 ;
https://arxiv.org/html/2508.08246v2 ;
https://arxiv.org/html/2609.20537v1 .
