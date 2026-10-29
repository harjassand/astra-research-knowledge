# A finite-rate transport supplier with unknown reversible memory

29 October 2026. Independent continuation5 physical-mechanism investigation.

**Status.** This is a complete conditional construction and a sharp structural
boundary. Its thermodynamic principle is the established single-affinity,
tightly coupled motor principle. It is not a new geometric-pump formula, a
priority claim, an apparatus, or a demonstrated practical advantage. The useful
interface-level result is that a finite-rate controller can enforce that
principle on an unknown microscopic reversible menu, without averaging the
controller infinitely fast or reconstructing hidden transition rates. A
substantial hidden-connectivity premise and an actual driven controller remain.

## 1. Question and the first mechanism that failed

Can the ordering of unknown reversible native operations generate a sustained,
kinetically robust physical current?

If every native generator Q_j is reversible for the same mu, an open-loop
switching schedule started at mu stays at mu at every time. Every microscopic
edge current mu(x)q_j(x,x')-mu(x')q_j(x',x) is then zero. The same holds for
independent randomized schedules after conditioning on the schedule. No
noncommutativity calculation changes this physical fact.

For example, on three equiprobable states, let P average states 0 and 1 and
leave 2 fixed; let Q average 1 and 2 and leave 0 fixed. Their chronological
product is

    PQ = [[1/2,1/4,1/4], [1/2,1/4,1/4], [0,1/2,1/2]].

It is not reversible in the uniform law. Its apparent endpoint circulation is
not an actual net traversal current: every elementary P or Q call has zero
mean antisymmetric transition count when started at the common equilibrium.
Finite partial averages give the same distinction and can be actual finite
CTMC pulses. Endpoint nonreversibility and physical pumping are different
quantities.

The [Rahav-Horowitz-Jarzynski no-pumping theorem](https://arxiv.org/pdf/0808.0015)
and the [Chernyak-Sinitsyn pumping-restriction theorem](https://arxiv.org/pdf/0808.0205)
are stronger established warnings against trying
to promote a formal commutator to a motor. The construction below uses actual
state-dependent finite-rate switching, whose joint dynamics are driven.

## 2. Actual menu and controller

First fix a finite microscopic state space X. Later we allow an arbitrary
frozen device parameter theta, with a finite state space in each sector.
The noninvasive visible label Y is onto Z/LZ, L >= 3. Write X_i={Y=i}.
There is a common positive probability mu, unknown to the controller.

For every visible edge e_i=(i,i+1), an actual continuous-time native generator
Q_i is available. It preserves X_i union X_(i+1), and on that set is reversible
for mu restricted to that set. It may change all hidden coordinates and its
rates may depend arbitrarily on them. At labels outside that pair its action
is irrelevant to this construction. No relationship between different Q_i's
kinetic prefactors is used.

The actual operational state includes an active-edge register E. Only

    Omega = {(x,e): Y(x) is an endpoint of e}

is used. While E=e_i, the specimen follows Q_i. Thus a native jump can change
Y only between the two endpoints of the active edge. The controller switches
between the two incident edges at the current label without changing x.
At Y=i define the forward switch as incoming e_(i-1) -> outgoing e_i.
Supply rates

    k_i^+(x)=gamma_i(x) r_i,
    k_i^-(x)=gamma_i(x),            r_i>0.                 (1)

The common factor gamma_i(x)>0 can be unknown. A literal visible controller
can instead use a known gamma_i depending only on i, a fresh exponential
clock, and the observed current label. An autonomous physical gate may have
hidden-dependent gamma_i, provided its two directions have the stated common
factor at the SAME microscopic x. There is no averaging or fast-controller
limit. Every switch leaves the operational specimen state unchanged; an
additional microscopic kick must be included in the actual instrument.

All rates are finite in a finite sector. A bounded-rate family gives the usual
nonexplosion and event-count budget. These are actual continuous-time generator
controls. A fixed-duration endpoint kernel cannot silently be invoked as an
instantaneous Poisson event; it needs a separate timing construction.

Define the reference probability on the joint state by

    m(x,e)=mu(x)/2,                                         (2)

and A=sum_i log r_i. Native rate ratios are m(v)/m(u); a forward controller
switch has the additional ratio r_i. Hidden energies and native barriers do
not have to be learned.

**Connectivity.** Assume the full joint generator is irreducible. Strict
transport additionally requires a closed microscopic walk whose phase winds
nontrivially around the visible cycle. A simple sufficient supplier is that
every Q_i is irreducible on X_i union X_(i+1). Irreducibility of the full joint
generator alone does NOT imply winding accessibility; Section 7 gives an
eight-state counterexample.

## 3. Exact stationary direction and stall

Let p be the full joint stationary probability. Let J_i be the net native
current from label i to i+1 while e_i is active, summed over all hidden source
and destination states. Let C_i be the net forward controller-switch current
at label i, summed over its hidden states.

### Theorem 1

Under the interface above,

    J_i=C_i=J for every i,
    sigma=A J >= 0,                                      (3)

where sigma is the full Markov entropy-production rate. If A is nonzero and
a nonzero-winding microscopic closed walk is accessible, J has the strict
sign of A. If A=0 the full joint chain is reversible and J=0. These statements
hold at every finite controller rate, for every positive compatible choice of
hidden kinetic coefficients.

**Proof.** Resolve the joint visible phase into 2L states:

    (Y=i,E=e_(i-1)) -> (Y=i,E=e_i)
                   -> (Y=i+1,E=e_i).

The first arrow is the forward controller gate, the second a forward native
crossing. Same-label hidden transitions do not change phase. Stationarity of
each phase implies equality of all its adjacent net currents, proving the
first part of (3).

For every unordered microscopic edge {u,v}, put
j_uv=p(u)k_uv-p(v)k_vu with an arbitrary chosen orientation. Then

    sigma=sum_{u<v} j_uv log[p(u)k_uv/(p(v)k_vu)] >= 0.

The terms involving the potential log[p/m] sum to zero by microscopic flow
conservation. Every native edge has zero remaining affinity. A controller
edge at i contributes log r_i. Hence sigma=sum_i (log r_i) C_i=A J.

If sigma=0, every edge has zero stationary current and the chain is reversible.
The product of forward/backward rate ratios on any microscopic closed walk
is exp(A w), where w is that walk's integer phase winding: every phase cut
has the same signed crossing number on a closed walk. A walk with w!=0 makes
reversibility impossible if A!=0. Thus sigma>0 and J has the strict sign of A.

If A=0, the controller affinity is a gradient on the phase ring. Choose
positive constants h_phase successively so h_(2i+1)/h_(2i)=r_i and
h_(2i+2)=h_(2i+1); the product condition makes them periodic. Then m h,
normalized, satisfies detailed balance on all full microscopic edges. This
also proves exact stall, including when individual r_i differ from 1. QED.

The microscopic graph can have arbitrarily many hidden loops. The construction
forces every loop affinity to equal A times the same observed winding, so
additional hidden loops cannot create an independent thermodynamic drive.
No finite predictive representation or hidden reset is required.

To verify the sufficient winding supplier, choose any x_i in each nonempty
X_i. Pair-mode irreducibility supplies a native path from x_i to x_(i+1).
Join these paths using the allowed gates, with x_L=x_0. The resulting closed
microscopic walk has phase winding one, even if an individual native path
recrosses its visible pair. These chosen states are proof objects; the actual
controller does not recognize, prepare, or copy them.

Exact numerical setpoints are not essential for the sign. If the actual gate
ratios remain label-local constants with known bounds
r_i in [r_i^low,r_i^high] and prod_i r_i^low>1, the same proof guarantees a
positive current. Arbitrary hidden-state-dependent ratio errors do not have
this protection, because they can introduce an additional cycle affinity.

## 4. What the current physically means, including the clock

Let N_i(t) be the signed count of actual native i -> i+1 crossings up to
physical time t. C_i(t) denotes the corresponding signed controller count.
They are retained in the actual visible path/mode record. Each pair of counts
across two cuts of the 2L phase circle differs by the change of occupancy of
the phase interval between those cuts. Pathwise, that difference has absolute
value at most 1. Consequently all counts have the same long-time rate.

In a finite irreducible sector, the ergodic theorem gives

    N_i(t)/t -> J almost surely,                         (4)

from every initial full state. A stationary specimen has E N_i(t)=t J.
An arbitrary initial/calibration record need not supply stationarity, and (3)
is not a uniform positive finite-time current claim from arbitrary records.

If the labels are stations around an actual physical ring and each gated
native edge follows the declared adjacent passage, N_i is a traversal count
and J is revolutions per unit physical time. If labels are logical states,
it is only transport in that configuration graph. A label alone does not
establish spatial displacement, cargo transport, force, or mechanical output.

The protocol runs continuously; there is no discarded stopping time, selected
endpoint clock, or unrecorded action key. It does not claim that the entire
record law is independent of hidden kinetics. Its current direction and stall
are, while speed, fluctuations, phase occupations, and finite-time records are
generally not.

There is no uniform positive throughput from reversibility and support alone.
Replace every Q_i by eta Q_i, leaving all equilibrium measures and controller
rates fixed. Native activity, hence |J|, is at most eta times its original
uniform exit-rate ceiling. It tends to zero with eta. The same family prevents
a universal equilibration or finite observation-time guarantee. Timing must
be measured or bounded separately if a useful speed is required.

## 5. Complete microscopic path relation from an available baseline

For an actual initial X~mu, choose its incoming or outgoing mode with an
independent fair bit. This supplies m in (2) without any hidden preparation.
Let R be the complete visible-label/controller path over a fixed physical
time t, including jump times. The full operational microscopic path measure,
started at m, obeys

    dP_m(omega) / dP_m(reverse omega)
       = exp(sum_i log(r_i) C_i(omega)).                 (5)

Indeed, reversed paths have the same holding-time factor, rate ratios telescope
to m(end)/m(start) times the displayed force, and initial m cancels the
microscopic endpoint factor. The exponent is measurable in R. Integrating
hidden paths preserves the same likelihood relation between a visible record
and its time reverse. This is an ordinary transient fluctuation relation.

If all driving is placed at one gate, r_0=R>1 and r_i=1 otherwise, then for
each integer n,

    P_m(C_0(t)=n) = R^n P_m(C_0(t)=-n).                 (6)

The relation retains the fixed observation duration and is valid jointly with
any additionally retained record statistic that transforms appropriately under
the same reversal. It is NOT an equality conditional on an arbitrary fixed
old calibration record. For that conditional statement, the actual initial
law given the old record and device parameter must still be m, and future
controller randomness must obey the declared conditional instrument.

Nor does (6) imply a logistic law for the sign of an arbitrary first-passage
event. Reversing a first-passage path can change its first-passage property,
and hidden boundary distributions can differ. Known Haldane/cycle-time
relations have their own renewal or bottleneck hypotheses. No such reset is
supplied here. C_0 also counts a controller transition, not a complete physical
turn at short times; its difference from a native cut current is bounded but
need not vanish at the endpoint.

Repeated runs of (5) require actual baseline initialization each time. At the
driven stationary law p, the finite-time path ratio includes the unknown
boundary term log[(p/m)(start)/(p/m)(end)]. It cannot be silently omitted.

## 6. Actual energy supply, load, and resource accounting

Equation (3) is a mathematical Markov entropy identity. A thermodynamic reading
requires an actual local-detailed-balance supplier, not merely a programmed
ratio of electronic switching rates.

One idealized supplier has common specimen energy E_0(x)=-kBT log mu(x) plus
a constant, equal mode energies at fixed x, a single temperature T, and a
gate reaction at label i consuming chemical free energy Delta mu_i=kBT log r_i
in its forward direction and returning it in reverse. Its activation barriers
and prefactors can be unknown. Native transitions obey the stated equilibrium
ratios; the gate's local detailed balance supplies (1). Then net fuel power
is kBT A J. This is a familiar tightly coupled autonomous-motor architecture,
not a constructed material implementation.

More generally, known native weights w_i(Y) can be incorporated by reference
m(x,e_i) proportional to mu(x) w_i(Y(x)) and gate ratios

    k_i^+/k_i^- = r_i w_i(i)/w_(i-1)(i).                (7)

The stationary direction proof is unchanged. Its convenient initial reference
state has specimen marginal proportional to mu(x) times the sum of the two
incident w's, so ordinary baseline mu no longer automatically supplies (5).
This preparation cost must be paid or the transient relation omitted.

An actual load is a separate operational contract. If one complete forward
physical turn delivers work W_load, and its local rate-ratio modifications
subtract W_load/(kBT) per winding without opening another thermodynamic cycle,
then replace A by

    A_load=(sum_i Delta mu_i-W_load)/(kBT).             (8)

The exact stall is W_load=sum_i Delta mu_i, independent of compatible kinetic
prefactors. Equilibrium weights alone do NOT specify the rates after a new
load is attached, or verify (8). Without that supplied load interface there is
only a circulation theorem, not a work-extraction theorem.

A digital implementation charges continuous/event-based label sensing, finite
clock accuracy, mode storage, switching latency, actual native waiting, and
all retained records. Under a ceiling Lambda+Gamma, the expected number of
full jumps in time t is at most (Lambda+Gamma)t. Exponential waiting has no
hard maximum and fixed hazard selection is not a free physical timer. Detector
or switch delays change the joint generator unless explicitly modeled. In an
autonomous realization the couplings and chemical reservoirs replace that
electronics; their construction and replenishment remain physical resources.

Controller event activity can remain large while native motion is arbitrarily
slow, so an external controller's event/record cost per turn can diverge.
The ideal net chemical power in (8) is not the total power of an arbitrary
electronic realization. Keeping all controller records is allowed by the
current theorem but does not make their production or eventual disposal free.

## 7. Hidden connectivity is load bearing: a finite exact obstruction

Take four microscopic states a,1,2,b with uniform mu and visible labels
Y(a)=Y(b)=0, Y(1)=1, Y(2)=2. Mode e_0 permits only a <-> 1; mode e_1 only
1 <-> 2; mode e_2 only 2 <-> b. Each allowed pair has symmetric positive rates.
All other microscopic states remain fixed under that native mode. Every
visible edge of the triangle therefore occurs under some actual mode, and
all native generators are reversible for the same full-support mu.

Add both incident modes at every microscopic state and the positive gates (1),
with r_0>1, r_1=r_2=1. The full joint graph has eight vertices and seven edges:
four controller edges and the three native edges. It is a connected TREE.
It has a unique stationary law, but every edge current is zero. Thus J=0,
despite A>0 and despite visible forward traversal a -> 1 -> 2 -> b looking
like one full turn. It has stored its displacement in hidden memory.

This exactly defeats the stronger claim that full joint irreducibility plus
visible edge access guarantees strict transport. Each pair-mode irreducibility
or another actual winding-accessibility supplier is needed. A visible loop is
not automatically a microscopic loop. In unbounded hidden spaces one must also
establish recurrence; a finite-state stationary proof is not a guarantee
against hidden runaway.

## 8. A general robust-sign criterion and its failure mechanism

Consider a known finite connected undirected microscopic graph G with positive
reference masses m_u and a fixed antisymmetric drive f_uv. Allow arbitrary
positive symmetric conductances c_uv in

    k_uv = c_uv exp(f_uv/2)/m_u.                         (9)

Let d_uv be an antisymmetric increment of a desired measured current. For a
directed simple cycle C, write F(C)=sum_C f and D(C)=sum_C d.

### Theorem 2

The stationary desired current J_d is nonnegative for EVERY choice of the
positive conductances if and only if

    F(C) D(C) >= 0 for every directed simple cycle C.   (10)

**Sufficiency.** Orient each nonzero stationary edge current positively and
decompose its divergence-free flow into positively weighted directed simple
cycles, each following that orientation. On every such cycle,

    F(C)=sum_C log[p(u)k_uv/(p(v)k_vu)] > 0,

because all constituent current ratios exceed 1. By (10), D(C)>=0. Summing
the positive cycle weights gives J_d>=0. This is the conventional positive
cycle-flow decomposition used in network thermodynamics.

**Necessity.** Suppose a simple cycle has F(C)D(C)<0. Keep its edges and add
a spanning forest attaching every remaining vertex to it, creating a connected
unicyclic graph. Set all other conductances to zero temporarily. Its stationary
tree-edge currents vanish, while the single cycle current has sign F(C), so
J_d<0. Give all removed chords sufficiently small positive conductances.
Irreducibility and stationary probabilities vary continuously, so J_d remains
negative. This is an actual compatible choice in (9). QED.

Theorem 1 enforces the stronger identity F(C)=A D(C) by actual mode topology,
with D the phase winding. Arbitrary hidden loops then satisfy (10) automatically.
The criterion is not presented as a new result distinct from the established
[positive cycle theory](https://arxiv.org/pdf/1605.07542); the useful point is
which supplier permits invoking it without
learning the hidden graph.

It also explains why small uncontrolled leaks are not automatically harmless.
A leak can open a cycle whose affinity drives the measured transport backward.
If the useful cycle is made arbitrarily slow by unknown kinetic disorder, any
fixed nonzero leak can dominate it. A leakage-rate upper bound alone cannot
replace a relative kinetic margin or the structural identity F=A D. Knowing
that total entropy production is positive does not fix the sign of one
loosely coupled transport current.

### An arbitrarily small leak that reverses a chosen current

This failure needs no complicated hidden source. On states 0,1,2,3 put one
driven edge k_01=R>1, k_10=1. Every other pair below has symmetric rates:

    k_12=k_30=eta,  k_13=k_20=epsilon,  k_23=1.        (11)

The intended cycle is 0->1->2->3->0. The cross-links of size epsilon open the
oppositely oriented path 0->1->3->2->0 through the SAME fuel gate. Let

    g=(2 eta epsilon+eta+epsilon)/(eta+epsilon+2).

Solving only the two passive-node balance equations and normalization gives

    p_1-p_0=(R-1)/[2(R+1+2g)] > 0,
    J_23=(eta-epsilon)(p_1-p_0)/(eta+epsilon+2).        (12)

Thus the target transport reverses whenever epsilon>eta, while the driven-edge
current and total entropy production remain positive. For every arbitrarily
small fixed leakage epsilon, a compatible unknown bottleneck eta<epsilon
defeats the intended sign. This is a single driving affinity acting through
loosely coupled cycles; having only one chemical reservoir is insufficient.
The alignment of its cycles with the intended transported quantity is what
matters.

## 9. Concrete family and a distinct consequence

Take three visible stations and two unobserved internal states at each station.
Let mu be any positive six-state distribution. For each pair mode, choose any
positive symmetric conductances between its four states and divide by mu(x)
to obtain the native rates. Each mode then has arbitrary hidden-state-changing
relaxation and is reversible for its restricted mu. Add the two incident gate
modes at every state with (1). The resulting twelve-state device has a strict
current of sign log(prod r_i), at all positive conductances and finite positive
gate rates. It is not a visible Markov chain in general.

An arbitrary frozen parameter theta can select those conductances and mu.
Every theta sector separately has the same chosen current direction. Theta
is never estimated or reset. A mixture of stationary sectors preserves that
direction. A pathwise long-time statement holds separately in every finite
irreducible sector; averaging limits requires the corresponding integrability
or common activity bound. Arbitrary old data can select a posterior over theta
without altering the conditional sign theorem. It does not establish that
the state within each selected sector is stationary at a finite start time.

The same wiring works for a known Hamiltonian Gray cycle in a binary
configuration graph if an actual native bit-i mode changes only bit i and
hidden coordinates while preserving all other bits. The controller retains
which of the two Gray-cycle edges is active. Native modes are shared across
the many edge contexts. This supplies a cyclic addressing operation whose
orientation is immune to hidden rate variation, conditional on the same
irreducibility and gate contracts. It is not a deterministic computation,
error-correcting memory, or bounded-latency sequencer; it has thermal backsteps.

## 10. What this investigation actually adds and leaves open

### Strong ordinary feedback comparator

At a supplied decision boundary, read the current label i, activate its
forward edge e_i, execute that actual native mode for any fixed time Delta>0,
and read again. The endpoint is either i or i+1. In the former case repeat;
in the latter advance to its next forward edge. Every completed pulse has
signed physical net crossing 0 or +1 because the only open passage is the
active pair. Within-pulse backward recrossings cancel exactly. No microscopic
rollback, hidden-state estimate, or hidden reset is needed.

If each finite pair mode is irreducible, exp(Delta Q_i)(x,X_(i+1))>0 for every
starting x in X_i. Finiteness gives a positive per-device minimum p_star, so
the number of pulses to each forward step is geometrically dominated with
mean <=1/p_star. Repeating produces an exactly oriented sequence of endpoint
steps, with all waits and intermediate records retained. p_star can be
arbitrarily small over the promised unknown-kinetic family; it is a proof of
per-device finiteness, not an acquired latency certificate.

This comparator uses the SAME actual pair operations and visible information.
Its boundary sensing/selection must either be an actual ideal decision-time
contract or be implemented with a supplied holding/switching protocol. A
nonzero uncontrolled delay is not automatically safe. Continuous event
detection and switching at the first label change is another ordinary version.
Its physical controller work is not specified by the native equilibrium rates.

Thus unknown kinetics alone do not create a new directional-control capability:
ordinary feedback already provides one at that interface. The finite-rate
construction contributes an explicit autonomous, thermodynamically accounted
supplier with backward controller transitions and no pause/instantaneous
decision between native phases; it does not outperform the ordinary comparator
on directionality. The finite-rate gate and the ideal decision boundary are
different timing/control contracts, and neither is granted free hardware.

### Scientific disposition

The construction gives an explicit finite-rate physical control interface for
a known robust motor principle, and proves why two tempting shortcuts fail:
noncommuting common-equilibrium words need not transport anything, and a
visible cycle can fail to close through hidden memory. It identifies the exact
topological/thermodynamic protection needed for rate-independent direction.

Conventional tightly coupled motors already achieve the same directional and
stall consequence. Strong geometric pumps also supply robust mean quantization
in their stated adiabatic/low-temperature limits. No superiority to either has
been established here. The microscopic control/sensing implementation and a
useful rate or power remain unresolved. A foundational new capability would
need a weaker supplier for the required winding connectivity and joint gate
ratio, or a substantive way to certify/repair leaks without estimating the
hidden kinetics. This completed unit does not claim to have supplied that.
