# A finite noisy clock trap stops an unrepaired autonomous compiler

29 October 2026. This is a no-go for the precisely defined **unrepaired
modular-handshake architecture**, not for autonomous quantum memory, the
programme's thermal controller, or a Gacs-type controller with an acquired
clock-repair mechanism. Classical modular winding/deadlock is established
unison theory. The consequential composition here is its admissibility
under arbitrarily weak fixed local reset generators and the ensuing quantum
memory failure in physical time.

## 1. Native architecture and permitted noise

Let G be a finite connected bounded-degree graph with n vertices containing
the six-vertex 2-by-3 square-grid rectangle below. A local cell carries a
classical clock c_v in Z/3 and a bounded-dimensional quantum data/workspace
register. Clock attempts occur at independent rate-one Poisson times. An
attempt at v increments c_v by one modulo 3 only if

    no neighbor w has c_w=c_v-1 (mod 3).                    (C1)

An accepted attempt may execute any fixed local CPTP data operation,
including the circuit's extraction, computation or reset instruction.
It changes only its own clock and its acceptance depends only on clocks.
There is no additional repair of clock values. All quantum restoration
operations are gated by accepted attempts. Outside those operations one
may retain any fixed data Hamiltonian. This is an autonomous bounded-local
sum of rate-one CPTP update generators. It includes arbitrarily elaborate
stored programs in the data registers; the obstruction is in their clock.

All clock states remain classical. The encoder may use any classical clock
initialization and any quantum encoded input. The receiver may use all
remaining data/workspace cells, the controller's previously extracted
classical records, and clock-attempt/reset histories. No record of the
subsequent depolarizing noise environment is provided, whether that record
would be quantum or a classical unraveling label. A granted Pauli-kick
label would be different information: with it, depolarization can be undone.

The allowed unknown noise contains:

* At each of six specified clock cells, the fixed generator
  epsilon(R_c-id), where R_c replaces that clock by a specified classical
  phase c. Its diamond norm is at most 2epsilon. There are only six such
  noisy cells, independently of n.
* At every quantum data/workspace cell, weak independent depolarization
  eta(T_v-id), eta>0 fixed. The local cell dimension is bounded.

Both rates can be arbitrarily small fixed positive constants. The clock
resets are genuinely nonunital; the data noise is unital. No adversarial
time switching, state-dependent event rate or global support is used.
The unknown coherent field can be zero; failure in this subcase already
disproves a guarantee quantified over the stated combined error class.
More strongly, the proof is unchanged by any additional Hamiltonian on
the quantum data/workspace registers. It can include a nonzero unknown
weak local field that changes the energy of a nominal stabilizer
Hamiltonian. Such a data field neither repairs the classical clock core
nor alters the post-halt entropy contraction.

## 2. A constant-size absorbing core

List the rectangle vertices cyclically as

    a=(0,0), b=(1,0), c=(2,0),
    d=(2,1), e=(1,1), f=(0,1).

Its perimeter is a six-cycle; there is also the internal edge b--e. Set

    (c_a,c_b,c_c,c_d,c_e,c_f)=(0,1,2,0,1,2).                (C2)

Every vertex has a perimeter neighbor one phase behind it. Hence every
vertex is blocked by (C1), independently of all exterior clocks. Set its
unknown reset channel to its own phase in (C2). Further reset events leave
the core unchanged. Thus (C2) is a permanently frozen core once reached.

The native exact consumer enumerates all 3^6 assignments on this rectangle.
It finds six internally frozen assignments, each needing four nonzero
clock changes from the all-zero assignment. This finite calculation is
not needed for the displayed analytic core, and does not establish the
all-graph theorem by enumeration.

### Acquisition by weak, time-independent noise

In any unit physical-time interval, consider the event that none of the
six core clock-attempt processes rings and that each of the six reset
processes rings at least once. Its conditional probability, given any
past clock/data history, is exactly

    q=e^(-6)(1-e^(-epsilon))^6 >0.                          (C3)

At the end of this event the core equals (C2), regardless of its earlier
state. Exterior updates do not modify its clocks. Events in disjoint unit
intervals use independent Poisson increments. Consequently

    Pr(core not frozen by time M) <= (1-q)^M <= e^(-qM).     (C4)

For 0<epsilon<=1, q>=epsilon^6/46656: use e<3 and
1-e^(-epsilon)>=epsilon/2. Thus the completely explicit integer

    M=ceil(233280 epsilon^(-6))                             (C5)

makes the failure probability <1/100, since e^5>100. This time may be
enormous as epsilon decreases, but is independent of system size. No
trajectory or ideal equilibrium sampler is being supplied for free.

## 3. One frozen core stops every clock in polynomial time

After the core freezes, let a_v in {0,1,2} be the clock phases at that time
and let N_v(t) be each site's subsequent accepted-update count. The integer
lift a_v+N_v(t) agrees with its clock modulo 3. For an oriented edge v--w,
let b_vw be the smallest integer >=a_v-a_w congruent to 1 modulo 3. Then

    a_v+N_v-a_w-N_w <= b_vw.                               (C6)

Initially this holds. An update of w decreases the left side. An update
of v could cross b_vw only from equality; at equality w is one phase
behind, so (C1) forbids that update. This proves the invariant for every
update order. In particular

    N_v <= N_w+2.                                         (C7)

Core counts remain zero. Following a shortest path to the core gives

    N_v <=2 dist(v,core),
    total subsequent accepted updates <=B:=2 sum_v dist(v,core)
                                     <=2n diam(G).         (C8)

Resets on the core now do nothing, and no other clock is reset by the
chosen noise. At any nonterminal state at least one update is accepted
at its rate-one attempt process. Thus the waiting time to the next
accepted update is exponential of rate at least one. The stopping time
is stochastically dominated by a sum of B rate-one exponential variables,
and has expectation <=B. Markov therefore gives

    Pr(any clock still advances more than 100B after trap) <=1/100. (C9)

By (C4)--(C9), with probability >=.98 every restoring data operation has
ceased by deterministic time M+100B. This conclusion allows an arbitrary
quantum code and arbitrarily complex data gadgets. It uses no exact
classical reduction of the unknown quantum noise.

The same mechanism exists for every fixed modulus m>=3. A square-grid
cycle of length m when m is even, or 2m when m is odd, can be filled by
successive phases. It is a constant-size frozen core for a fixed m. The
increment barrier gives N_v<=N_w+(m-1) and B<=(m-1)n diam(G).
Changing to a larger **fixed** clock alphabet only changes constants.
A clock period growing with graph size, or a genuine error-repair rule,
changes the architecture and its resource contract.

### Exact topological escape, with its cost still exposed

For a general graph with the same m-phase rule, a permanently blocked
finite set contains an oriented cycle: choose for every blocked vertex
one neighbor one phase behind and follow those arrows. The cycle length
is divisible by m. Conversely, any graph cycle of length divisible by m
can be assigned successive phases to make a frozen core. Thus the
existence of such a cycle characterizes this **particular** absorbing-core
mechanism. A tree has no such core, for any initial phases.

In fact, without ongoing clock faults a finite connected graph with no
cycle of length divisible by m is live from every phase configuration.
There is always an enabled site. The integer barrier gives
N_v<=N_w+(m-1), so if one site advances infinitely often, every site does.
A coarse quantitative bound follows: after
n[1+(m-1)diam(G)] accepted updates every site has advanced once, and the
expected physical time for these updates is no larger than that number.

This supplies a genuine structural alternative to repairing winding, but
does not supply a size-uniform noisy quantum controller. First, the coarse
time bound grows with n. Second, a computation's data gates must respect
the clock graph: discarding non-tree handshakes while retaining data gates
across those edges silently discards their synchronization premise.
Finally this liveness proof is for fault-free subsequent clock dynamics,
not a threshold under indefinitely repeated clock faults. The topology
observation therefore narrows a viable design question without claiming
an autonomous memory construction.

## 4. Quantum forgetting after the halt, including a purified input

Let Q be all quantum data/workspace registers, of total Hilbert dimension
D (so log D=O(n)). After restoration stops, the remaining quantum dynamics
is the allowed weak local depolarization plus any Hamiltonian on Q.
Condition on the classical clock history and already extracted controller
records, but not on a microscopic record of the future depolarizing bath.
The corresponding quantum
channel remains CPTP: clock attempt and reset rates and their acceptance
are independent of the quantum data state. Let R be a reference qubit.

Set

    F(rho_QR)=D(rho_QR || I_Q/D tensor rho_R).

Always F<=log D+log 2. For the replacement map T_i on cell i,

    -dF/dt >=eta sum_i D(rho ||T_i rho) >=eta F.             (C10)

For completeness, D(rho||T_i rho)=S(T_i rho)-S(rho).
Convexity of relative entropy bounds the generator's entropy production
below by this quantity. The sum bounds F by the chain rule and strong
subadditivity: conditioning the i-th cell on all other cells and R only
decreases conditional entropy. Hamiltonian evolution leaves both total
entropy and the reference marginal unchanged. Thus

    F(t+s)<=e^(-eta s)(log D+log2),
    ||rho_QR(t+s)-I_Q/D tensor rho_R||_1
        <=sqrt[2e^(-eta s)(log D+log2)].                    (C11)

The bound also holds conditionally on each classical history. At

    s=eta^(-1) log[5000(log D+log2)]                        (C12)

the trace distance is <=1/50. After arbitrary decoding of Q and all
classical records the comparison state is separable from R. No separable
state of a decoded qubit and its reference has Bell overlap >1/2.
Trace-norm contraction and the effect bound therefore give, on the
high-probability halt event, entanglement fidelity <=1/2+1/100. Including
the probability <=.02 of its complement gives the safe bound

    F_e(I/2) <= .52 <3/5                                  (C13)

at time M+100B+s. The exact numerical constant is unimportant. It is a
failure for an unknown qubit entangled with a reference even with an
optimal final decoder; it is not just decay of a chosen autocorrelation.
Indeed the decoded channel has diamond distance at least .96 from the
identity, by testing its Bell input and the Bell-state projector.
For a two-dimensional finite lattice the displayed time is polynomial
in n at fixed epsilon,eta. A stretched-exponential family-wide memory
claim is false for this architecture and error class.

## 5. Strong ordinary alternatives and boundaries

The underlying winding and unison obstruction is ordinary distributed
computing. Devismes--Ilcinkas--Johnen--Mazoit, STACS2025, explicitly gives
terminal cyclic clock configurations and a self-stabilizing unison with
B>=2 diam(G)+2, Theta(log B) local bits and polynomial stabilization work.
Its proof also contains the neighboring-update-count argument. We credit
that mechanism; no new classical clock impossibility is claimed.

That ordinary repair is a meaningful comparator but does not finish the
quantum task: it has growing local storage, a transient-fault stabilization
guarantee rather than a sustained-noise containment threshold, and repairs
may rewind phase while quantum computation has already consumed or reset
its earlier state. Quantum history cannot simply be overwritten as a
classical clock value. Those actions must be admitted as correctable data
faults or accompanied by a proved restoring quantum-history operation.

Lake2510.08056v2 already warns that marching-soldier computation speed is
insufficient for fault tolerance, due to long delay regions. The present
native core is a stronger **permanent** obstruction under explicitly allowed
nonunital clock resets. It does not contradict that paper's reliable-clock
assumptions or prove its Poisson decoder fails.

Dünnweber--Styliaris--Trivedi2601.20818v1 has a self-repairing structure
layer in its QCA and a separate marching-soldier continuous-time discussion.
Our theorem does not assert that every implementation of that paper is the
unrepaired module defined here. Rather, to use that route for our unknown
nonunital clock-error task one must supply how those added counters repair
such defects and how the resulting data histories remain correctable.
Its mean-velocity statement alone does not provide that gate.

An independent unclocked thermal/autonomous recovery still operating after
the trap is **outside** this no-go. So is a Gacs clock whose local structural
correction is explicitly proved to repair the core. Errors restricted to
data with perfect clock registers are also outside its admitted noise
class, and must pay that reliability as an extra resource.

The surviving target is therefore precise: a noise-admitted,
fault-contained restoration of **both** the clock and the consumed quantum
history. An autonomous compiler cannot obtain it solely by attaching a
finite modular handshake to an active fault-tolerant circuit.
