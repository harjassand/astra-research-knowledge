# A clockless noisy classical register and buffered copy

29 October 2026. This is a restricted CLASSICAL operation with a fully
specified asynchronous controller and a sustained-noise bound. It is not a
decoder for the programme's recursive quantum code. The interaction graph
is an explicitly admitted expander, rather than an implicitly free
three-dimensional wiring network. No noiseless persistent bit, synchronizing
clock, causal fault-label assumption, or quiet interval is used.

## 1. Primitive and exact input contract

Let P be the symmetric transition matrix of a regular undirected multigraph
on n sites, including multiplicities and loops, with uniform stationary
law. Suppose

    ||P-Pi||_(2->2) <= s,   Pi=11^T/n.

Fix an integer ell. Put W=P^ell and assume

    3(1/64+s^(2ell)) <= 1/8.                              (1)

There is one physical classical bit per site. Each site has an independent
Poisson update clock of a possibly unknown, fixed rate r_i in [15/16,17/16].
The nominal rate is1; this interval allows a stated static calibration
error without a perfect global timing signal. At its update, draw THREE independent
ell-step P walks starting at that site, read their three endpoint bits,
and replace the site's bit by their majority. Sampling is with replacement;
the target and sampled sites may coincide. Every fixed draw gives a monotone,
self-dual Boolean map. There is no state besides these n bits.

Unknown faults occur on a fixed catalogue of nonempty supports X, |X|<=q,
at independent state-independent Poisson rates k_X. They are independent of
nominal clocks and walk coins. At a fault, the replacement of the bits on X
is ARBITRARY. In particular it may depend on the initial bit, the entire
past, all future nominal clocks/coins and all other fault locations. Require

    max_i sum_(X containing i) k_X <= lambda,
    lambda <= 1/[1024(2^q-1)].                            (2)

Thus Lambda=sum_X k_X<=n lambda. The theorem is pathwise over all supported
replacement labels; the maximum is INSIDE expectation over the clocks,
coins and unlabelled fault support process. A state-dependent unknown point
process is not silently substituted for this input.

The classical bit b to be retained is encoded as all b, with at most
m0<=floor(n/256) initially incorrect bits. The locations are arbitrary,
but the initial configuration is independent of future clocks/coins/faults.
The final mathematical decoder is majority of all n bits. It need only be
used for readout; the ongoing controller does not evaluate a global majority.
A noisy local implementation of that terminal readout is a separate resource.

For q>=1 put h=ceil(n/64), and assume h>q. For all T>=0, the probability,
maximized over the labels just described, that the number of incorrect bits
EVER reaches h by T is at most

    delta_reg(T) = min{1, 2^q n(1+lambda) T exp(-n/256)}.   (3)

Consequently the decoded value is correct at EVERY time in [0,T] outside
one event of probability delta_reg(T). An initial qualification failure
delta_init adds directly. The claim protects a classical bit, not a coherent
superposition of the all-zero/all-one configurations.

## 2. Offline labels disappear by a literal monotone coupling

First take b=0. Fix every clock, walk draw and fault support/time. Replace
EVERY fault by setting ALL its bits to 1. Starting from the same initial
configuration, this trajectory pointwise dominates the trajectory under
ANY replacement labels. This follows by induction through event times:
nominal majority maps are monotone, and the all-one replacement is the
largest possible output on its support. No conditional independence of the
adversarial labels is used. This induction is valid even when those labels
were selected after the complete schedule was revealed.

The resulting worst trajectory is an ordinary time-homogeneous Markov
process: the fault labels are now constants, with the original independent
Poisson clocks and fresh walk draws. For b=1, complement all bits and use
the same argument. This is the actual quantifier bridge. Applying a Markov
drift proof directly to future-dependent labels would not be justified.

## 3. Spectral contraction becomes a scalar birth/death bound

For the worst trajectory let S be its set of incorrect bits and m=|S|.
Before the first hit of h, m/n<1/64. The probability that site i's next
nominal output is wrong is

    p_i=3 z_i^2-2 z_i^3,   z=W 1_S.

Therefore, using 0<=z_i<=1 and P's spectral bound,

    B(S):=sum_i p_i <=3||W 1_S||_2^2
       <=3[m/n+s^(2ell)(1-m/n)]m <=m/8.                 (4)

Before multiplying by clock rates, the sums of birth/death probabilities
are at most m/8 and at least7m/8 respectively. The actual nominal birth
rate is thus at most17m/128; the death rate is at least105m/128. A fault
increases m by at most q.

Up to its first hit of h, m is dominated by the scalar branching/immigration
chain Z with per-particle birth rate a=17/128, death rate d=105/128, and batches
of q immigrants arriving at rate Lambda<=n lambda. Start Z at m0. This is
a standard graphical birth/death coupling, not a claim that m itself is
a Markov chain. When the two counts agree, nominal birth/death rate
inequalities give the needed simultaneous transitions; when they differ,
single-particle births/deaths cannot reverse the order. A q-immigration
event dominates the actual increase 0,...,q.

## 4. All-time exponential bound, not mean velocity

Let g_t(z) be the offspring generating function at time t of one particle
under the birth/death part of Z. At z=2, v_t=g_t(2)-1 obeys

    v'_t=-(11/16)v_t+(17/128)v_t^2,   v_0=1.

Hence 0<=v_t<=exp(-71t/128)<=exp(-t/2). For 0<=v<=1, convexity gives
(1+v)^q-1<=(2^q-1)v. Independence of immigrant families then gives

    E[2^Z_t]=g_t(2)^m0 exp{Lambda int_0^t[g_u(2)^q-1]du}
      <=2^m0 exp{(128/71)Lambda(2^q-1)}
      <=2^m0 exp{2n lambda(2^q-1)},                     (5)

UNIFORMLY in t. No stationary or IID snapshot assumption is used.

A first crossing of h by Z must start at a count at least h-q and below h.
At those states the total possible upward rate is at most
Lambda+a(h-1)<=n(1+lambda). Count the possible crossing events by their
Poisson compensator and use Markov's inequality with (5). This proves

    Pr[sup_(t<=T)Z_t>=h]
      <=n(1+lambda)T 2^(m0+q-h)
                    exp{2n lambda(2^q-1)}.             (6)

Because h-m0>=3n/256, ln2>=1/2, and
2lambda(2^q-1)<=1/512, its exponential part is at most
2^q exp(-n/256). This proves (3). The same estimate bounds the event for
ALL supported label assignments simultaneously by Section2. Merely
checking that the average error count decreases would not establish (3).

The explicit scalar domination also gives

    E Z_t=m0 exp(-11t/16)+(16qLambda/11)[1-exp(-11t/16)]. (7)

Equation(7) is optional; it is not substituted for the tail theorem.

## 5. Clockless reliable copy into an arbitrary noisy destination

Use a second n-bit block C, with its own fixed rates in [15/16,17/16]. Its update at label i polls the SAME
three W-walk samples in the SOURCE block A and overwrites C_i with their
majority. It does not read C_i. The source continues its restoring updates
from Section1 and has no nominal feedback from C. Faults may touch both
blocks, still with support<=q and per-bit incidence<=lambda. The entire
system is monotone for every fixed nominal draw, so the all-wrong coupling
still applies. No noiseless receiving register is granted.

Let h=ceil(n/64), l=ceil(9n/1024). Initially C can be completely arbitrary.
For 0<tau<=T, the probability that its decoded value is ever wrong at a
time in [tau,T] is at most

    delta_copy(tau,T) <= delta_reg(T)+n exp(-15tau/16)
           +n(17/16+lambda)T 2^(l+q-h).               (8)

All three terms are paid. The first is source loss. To establish the last
term, first initialize a comparison destination at the CORRECT value b.
Until source exit, its total probability of a wrong nominal output is
F<=n/(512). If j is the destination's incorrect count, then

    G 2^j /2^j <= (49/32)F-(15/32)j+n lambda(2^q-1)
                <=130n/32768-(15/32)j <=0 when j>=l.  (9)

Here G is the stopped generator and (2) was used. During an excursion
from below l to h, 2^j is therefore a nonnegative supermartingale.
The entry overshoot is at most q, giving probability at most 2^(l+q-h)
per excursion (a harmless factor2 is retained). There are at most
n(17/16+lambda)T expected possible entry events. Optional stopping at source
exit preserves the bound. This proves the last term in (8).

Finally couple the worst destination initialized at all wrong bits with
the comparison destination. They see the same source, updates and all-wrong
fault resets. At the FIRST nominal update of each destination site they
agree at that site forever: the copied value depends only on the common
source and draw. The probability that some site has not had a nominal
update by tau is at most n exp(-15tau/16). This proves (8) from arbitrary initial
C without preparing the comparison state in the actual operation.

The controller is always on. tau is a readout latency contract, not an
internal global clock or a periodic noiseless phase reset. This does NOT
prove arbitrary feedback computation: the source is a retained, unchanged
classical bit. Dynamic syndrome streams and noisy multi-bit routing need
their own theorem.

An array of these independent register/copy PAIRS has a useful multipoint
contract even when the fault catalogue couples them. If a fault support
contains<=q bits, each of its independent Poisson streams can touch<=q
pairs. A pair's worst-case bad event from Sections2--5 depends only on
its private nominal clocks/coins and the streams incident to that pair.
For any r specified pairs, the ordinary read-q/Finner inequality therefore
gives

    Pr[all r pairs fail somewhere in their stated time windows]
        <= product_(j=1)^r delta_copy,j^(1/q).          (8a)

Their fixed time windows need not be equal. The same statement holds for
single retained registers with delta_reg. The input error patterns may be
fixed arbitrarily or mixed independently of future primitives. Condition
on them first and use the uniform bounds. This is an all-time local-
stochastic output guarantee, not merely r separate marginal estimates.
It does not hold for arbitrary adaptive inter-pair feedback: the dependency
of a pair on the independent primitive streams would then change. It also
does not turn a static register into a dynamic syndrome decoder.

## 6. Explicit ordinary graph and bit-level controller description

Use the eight-incidence Margulis--Gabber--Galil multigraph on Z_m^2, n=m^2:

    (x+-2y,y), (x+2y+1,y), (x-2y-1,y),
    (x,y+-2x), (x,y+2x+1), (x,y-2x-1),

with the two unshifted horizontal and vertical directions each counted
once. All arithmetic is modulo m. The standard named theorem gives
||P-Pi||<=5sqrt(2)/8 for every modulus. The exact convention and ordinary
primary spectral import are inherited from the frozen c_new_theory
SPECTRAL_SOURCE_BRIDGE.md; no odd-modulus quantum/Wigner restriction is
imported. Choose ell=16. Then

    s^(2ell)=(25/32)^16,
    3[1/64+(25/32)^16] <1/8,                             (10)

an exact rational inequality checked by compile_contract.py.

Each update draws 48 eight-way walk choices, requiring exactly144 fair
bits, reads at most THREE endpoint bits plus its old target, and performs
one majority-and-write. Its support has cardinality<=4 and graph radius
<=16 in the base graph for restoration. Copy adds one matching edge between
the two graph layers, so its radius is at most17. This is an admitted atomic finite-range channel;
it uses no persistent routing register. Equivalently, the finite coin
choice is part of the specified nominal local CPTP map. A physical
implementation by sequential moving messages is NOT supplied for free.
The classical host reference implementation computes the endpoints using
O(log n)-bit modular addresses; those host operations are not claimed to
be noiseless hardware controller operations.

The measured quantum realization, when used only as a classical auxiliary
controller, has Kraus operators proportional to X_target^(old xor majority)
times the relevant Z-eigenspace projector. Repeated endpoints are measured
only once. Thus it fits the frozen trivial-Z-ancilla corollary at its
actual graph-local support scope; all those bits remain subject to faults.
This observation does not itself supply a quantum-data decoder.

compile_contract.py constructs and checks the native eight-incidence
catalogue and emits a dyadic finite contract. It does not simulate any
trajectory, thermal sampler, hardware, or unknown logical state. The
all-n spectral theorem and Sections2--5, rather than finite extrapolation,
pay the all-volume result.

## 7. Why this does not silently solve the three-dimensional task

The graph and the range16 atomic read primitive are load-bearing. They
are NOT bounded-density, constant-range interactions on a growing
Euclidean three-dimensional lattice. Nor does a stable classical bit
automatically decode a time-dependent quantum syndrome.

There is a sharp obstruction to porting THIS random-walk compiler just
by replacing the graph. On the L^3 periodic grid, let P be any symmetric,
uniform-stationary walk whose steps have coordinate displacement<=R.
For L>2R, use f(x)=cos(2pi x_1/L). It has variance1/2. Its Dirichlet form
gives

    1-lambda_2(P) <=4pi^2 R^2/L^2.                      (11)

Thus, for any fixed ell, ||P^ell-Pi|| tends to1 as L grows, so (1) cannot
hold. If the norm is required to be at most a fixed s_*<1 and
4pi^2R^2/L^2<=1/2, then

    ell >= L^2 log(1/s_*)/[8pi^2 R^2].                 (12)

The same proof applies in any fixed grid dimension with this test
coordinate. It is a limitation of this REVERSIBLE sampling construction,
not a no-go for directional Toom rules, nonreversible eroders, Gacs
hierarchies, quantum memory, or every local classical controller.

If these ell walk steps are physically executed serially, their time and
noisy transient states must be included; retaining a rate-one atomic
long-range read would be an unacquired actuator. The useful paid operation
here is therefore a graph-local retained bit and asynchronous buffered
copy under sustained, offline-labelled Poisson faults. The programme's
geometrically local joint syndrome/data persistence gate remains OPEN.

## 8. Conventional methods and what is not claimed

Three-sample majority, expander mixing, subcritical branching domination,
immigration generating functions, coupling, and exit-count bounds are
ordinary methods. Existing noisy consensus and reliable-computation
theorems are controlling comparators, not hidden alternatives withheld
from them. This packet instantiates the required strong schedule/label
quantifier without importing a generic threshold as an oracle. It makes
NO world-priority, hardware, practical-speed, or full autonomous quantum
memory claim. See PRIOR_AND_GATE.md for the actually read primary scopes.
