# A state-based asynchronous FIFO with bounded fault edits

29 October2026. This is a different constructive interface from a fixed-
source copy. It supplies causal capture/overwrite, backpressure, reusable
storage and a quantitative all-state eroder under continuing noise. It
does NOT supply an exponentially accurate single-bit acknowledgement or
a fully protected logical streaming processor. Those stronger claims are
explicitly separated below.

The enabling representation is ordinary exclusion/FIFO occupancy: EVERY
phase-bit configuration is valid queue state. There is no malformed clock
state from which a nominal reset must rescue the controller. The protocol
core is conventional asynchronous micropipeline logic, not a new claim.

## 1. Actual finite controller and ports

Choose capacity M>=1 and packet width B>=1. Store M payload words
v_0,...,v_(M-1) of B physical bits, and M+1 physical tag bits
t_0,...,t_M. There are

    N=(B+1)M+1

physical controller bits, ALL subject to noise. There are no other
persistent registers, counters, history tapes or timing phases.

The internal stage i, 1<=i<M, attempts the following update at independent
Poisson rate r_i in[1/2,2]:

    if t_(i-1)!=t_i and t_i==t_(i+1):
        (v_i,t_i) <- (v_(i-1),t_(i-1)) atomically.        (1)

The downstream tag t_(i+1) is a local acknowledgement: equality says the
downstream stage has consumed the current contents of stage i. The first
inequality says a new predecessor value is available. Payload and its tag
are captured TOGETHER; no separately timed bundled-data promise is used.

An input capture carrying b is enabled only if t_0==t_1. It atomically
performs

    (v_0,t_0)<-(b,1-t_0).                                (2)

The input is accepted at THIS action, so the supplying module can thereafter
change its own offered word. This is an input port, not a learned-model or
stream-storage oracle. A caller's offered values and availability must be
supplied. Arbitrary attempted captures while full are rejected without
changing state. A noisy physical notification observed by an external
caller is not granted error-free; see Section5.

The output stage attempts at rate r_M in[1/2,2]:

    if t_(M-1)!=t_M:
        commit v_(M-1) to the consuming module;
        t_M<-t_(M-1) atomically.                         (3)

The commit can be a specified bounded-local state operation by the consumer.
It is not a persistent ideal record used by the controller. Input/output
words below are mathematical traces of these native actions. To connect
two links, identify the consuming stage with the next stage and its local
acknowledgement; no ideal observer checks a global majority or runs a clock.
The receiver must actually be available for the drain-time theorem. With
backpressure from a busy application, safety remains but that extra wait
is not bounded by our ready-receiver result.

The nominal channels measure the relevant local computational values,
perform the indicated Boolean writes, and discard outcomes. An internal
channel has support at most2B+3 bits and is nearest-neighbour on the line
of stage cells. Its finite neighbourhood truth table specifies the channel;
an actual transistor implementation, non-atomic hazards and circuit/noise
qualification are NOT acquired by writing that truth table. The full
Pauli-times-Z-projector form is available if used as a classical auxiliary
controller, but no new quantum-noise admission is inferred here.

Unknown faults are independently clocked, state-independent Poisson events
on catalogue supports X of at most q controller bits. Their rates k_X have
per-bit incidence<=lambda. Write Lambda=sum_X k_X<=N lambda. At each
fault all bits in X may be replaced arbitrarily, even with labels selected
after the complete nominal/fault schedule is known. The results in
Sections2--4 are PATHWISE for any such replacements. No Markov assumption
about their labels is made. Fixed tag/payload transition functions and
nominal Poisson clocks are the model; permanent broken circuitry and
arbitrary deletion of update clocks are outside it.

## 2. Every tag state is an ordinary queue

Define M occupancy bits

    e_i=t_(i-1) xor t_i,       1<=i<=M.                  (4)

All2^M occupancies occur, with a twofold global tag-phase redundancy.
Define Q(s), in EXIT-FIRST order, to be the payload word list

    (v_(i-1): i=M,M-1,...,1 and e_i=1).                (5)

It has length at most M. This definition applies to EVERY physical state,
not just a noise-free code subspace. No global queue-membership oracle is
needed to run (1)--(3).

An enabled internal move has (e_i,e_(i+1))=(1,0). Rule(1) changes this to
(0,1) and copies the carried payload. Therefore Q(s) is unchanged. An
accepted input appends b to its tail. An output commit removes its head
and outputs exactly that head. This is the totally asymmetric simple
exclusion/FIFO picture, with the important payload copy retained.

The overwrite rule is hence causal. A stage changes its payload only
when its old packet has been consumed downstream, and its new payload is
captured from an occupied predecessor. No fixed source-holding INTERVAL
is requested. A value can wait arbitrarily long under backpressure without
allowing a nominal overwrite. These statements hold under any nominal
event order, without assuming positive mean update speed.

After all packets drain, all t_i agree, with either common value. The
next input capture works in either phase. Old payload bits at empty cells
are irrelevant: every nominal creation of an occupied cell overwrites
its payload with a newly captured packet. There is no trusted reset-to-zero
phase. This is reuse/overwrite of bounded storage, not allocation of a fresh
register bank per message.

## 3. A local fault causes a bounded number of stream edits

Use Levenshtein distance on packet words, counting insertion, deletion or
substitution as one edit. A payload-bit flip changes at most the one
packet at its own occupied cell, so costs at most one substitution. If
that cell is empty, it changes no queued packet.

An interior tag flip toggles the TWO adjacent occupancies. There are only
four cases:

    00->11: insert two adjacent packets;
    11->00: delete two adjacent packets;
    10->01 or01->10: replace at most one packet value.

The last two cases move the sole packet between adjacent positions; there
is no intervening packet to reorder. Its payload may now be stale, so a
SUBSTITUTION is charged rather than assuming the move copied it. A boundary
tag flip inserts or deletes one packet. Thus each bit flip changes Q by
at most two edits. Any q-bit replacement is a sequence of<=q flips and
therefore costs at most2q. All affected local control and payload bits
are included. No noiseless tag is hidden in this bound.

Let I(T),O(T) be the accepted input and committed output words through T,
let Q_T be the actual current queue, and Q_0 the initial queue. If F(T)
fault events occur, then PATHWISE

    d_edit(O(T) Q_T, Q_0 I(T)) <=2q F(T).               (6)

Proof: initially the words agree. Internal nominal moves do not change
either side. Input appends the same symbol to both. Output moves the head
of Q_T into the end of O(T), so leaves their concatenation unchanged.
A fault changes only Q_T and costs<=2q. Triangle inequality proves(6).

For an initially empty queue, at an actual drained endpoint,

    d_edit(O(T),I(T)) <=2q F(T).                        (7)

At a general prefix add at most M for the uncommitted tail. An arbitrary
initial state adds at most M initial ghost packets. None of these are
silently asserted to be valid new input. A bad tag cannot cause unlimited
future duplicate/loss drift after the fault: its FULL effect is already
charged in (6), for all future event orders and future fault labels.

The statistical budget is honest: F(T) is Poisson with mean Lambda T, so
Poisson count tails apply directly to(6). There is no claim that the raw
channel's edit rate vanishes when M or its payload redundancy grows. For
example, a single endpoint-tag flip can create one ghost packet. Sections5
and7 explain why this is not the exponentially reliable handshake which
the earlier fixed-source register might tempt one to assume.

## 4. All-state drain/recovery with continuing noise

Suppose no further input capture occurs during the interval under study,
and output commits remain enabled whenever a packet reaches the end.
Put

    W(s)=sum_(i=1)^M (M+1-i)e_i,
    Wmax=M(M+1)/2,       C=2Mq.                         (8)

Each successful internal move or output decreases W by exactly1. Whenever
W>0, at least one such nominal action is enabled (take the rightmost
packet). Every fault increases W by at most C. Payload faults do not
increase W at all. No arbitrary tag configuration is a trapped clock.

Use FIXED analysis windows, not a physical global timer, of integer length

    w=2 ceil(log2(16M)).                                (9)

Let F_j count all faults in window j and J_j indicate that some one of
the M internal/output clocks did NOT ring in that window. By independence
and r_i>=1/2,

    Pr(J_j=1)<=M exp(-w/2)<=1/16,   E F_j=Lambda w.      (10)

The primitive variables belonging to disjoint fixed windows are independent;
F_j and J_j are independent too. No conditioning on an adversarially
selected controller state is used. If there is no fault and all clocks
ring, a nonempty queue loses at least one unit of W. Otherwise each fault
can add C, and the loss of the one promised service is charged once.
Thus for EVERY initial state and EVERY choice of fault labels,

    W_(j+1) <= (W_j-1)^+ + A_j,
    A_j=(C+1)F_j+J_j.                                 (11)

This deterministic inequality is simultaneous over all configurations and
labels; it is stronger than an adapted-rate drift estimate. It remains
true if fault labels encode the future clocks.

Assume the explicit sufficient noise condition

    Lambda w <=1/[16(C+1)],
    i.e. lambda <=1/[16 N (C+1)w].                      (12)

Define z=1+1/(C+1) and a dominating workload chain

    Z_0=Wmax,    Z_(j+1)=(Z_j-1)^+ + A_j.

The queue W is below Z pathwise for ALL states, so no independence of the
actual initial state from future schedules is necessary. Since
z^(C+1)<=e<3, log z>=1/[2(C+1)] and log(1+x)<=x, (10)--(12) imply

    log E[z^(A_j-1)]
       <=-1/[2(C+1)]+1/[16(C+1)]+2Lambda w
       <=-5/[16(C+1)] =:-r.                            (13)

Before Z hits0, exp(r j)z^Z_j is a nonnegative supermartingale. If tau
is that first hitting window, optional stopping gives

    E exp(r tau)<=z^Wmax,
    Pr(tau>m)<=exp{[Wmax-5m/16]/(C+1)}.                (14)

Also EA_j<=(C+1)Lambda w+1/16<=1/8, so the stopped linear drift gives

    E tau<=8Wmax/7.                                    (15)

When Z=0, the actual queue is empty. Therefore these are certified drain-
epoch bounds under CONTINUING faults, not a promise that a long global
quiet interval will occur. A completely rational sufficient choice for
the probability of NO empty epoch yet being<=2^-p is

    m=ceil{16[Wmax+(C+1)p]/5}.                          (16)

No trajectory, equilibrium initialization or random real-number oracle
is required to acquire this number.

This is a hitting-time result. Noise can refill a queue after an empty
epoch, so it is NOT a certificate that a deterministic later read finds
an empty queue, nor a physical error-free reset-done notification.

At an arbitrary closure time sigma, start the comparison at the next fixed
window boundary, costing at most one window and using Wmax again. If sigma
is allowed to depend on the WHOLE future schedule, do not strong-Markov it.
For sigma<=L there are at most J=ceil(L/w)+1 possible next boundaries.
A union bound makes (14) simultaneous with factor J. Equation(11) already
holds for all states and all labels, so there is no entropy-union cost over
future-selected initial patterns. This pays that particular composability
gate rather than assuming the old copy output is a fresh source state.

For several separate pipes, the schedule-only bad-drain events depend on
private nominal clocks and incident fault streams. A q-bit support can
touch at most q pipes. The ordinary Finner/read-q inequality gives

    Pr(all selected r pipes miss their stated drain epochs)
       <=product_(a=1)^r delta_a^(1/q).                 (17)

Use J_a delta_a for the future-selected closure-time version. Dynamic
injection from another pipe violates a CLOSED-input promise unless its
input has actually ceased; we do not count a busy upstream component as
an empty input oracle.

### Transfer deadline without closing the input stream

Attach conceptual unique identities to newly accepted packets for the
proof only. They are NOT stored in the controller. A nominal move copies
the carried identity; an edit caused by a fault either removes an identity,
marks its value changed, or inserts a fresh ghost identity. Choose any
accepted packet a. Until a is edited, consider the FIFO prefix consisting
of a and all packets ahead of it. Later legitimate inputs are BEHIND this
prefix and never block its rightmost packet. Define W_a as the weighted
sum(8) over the prefix's occupied cells. It is<=Wmax.

Every nominal prefix move lowers W_a by1. If W_a>0, at least one prefix
move/output is enabled. Non-prefix moves leave it unchanged. A fault can
increase its potential by at most C; if it edits packet a itself, classify
a as DAMAGED rather than promising its correct delivery. Consequently the
SAME schedule-only inequality(11) holds up to delivery or damage, including
when new real packets continue to enter behind a.

Therefore every accepted packet is either committed by time w(m+1) after
acceptance, or is one of the fault-edited packets, except on the event in
(14). For ALL acceptance times<=L simultaneously, multiply that bound by
J=ceil(L/w)+1 as above. This is a deadline-OR-edit contract. It neither
conditions a possibly future-selected packet identity on fresh randomness
nor requires a source to stay fixed for an external copy interval. In
particular, a future-labelled fault cannot create unlimited uncharged stale
deliveries or unlimited uncharged latency from one corrupted phase bit.

## 5. What a consumer can and cannot know

Inside a composed line, causal acceptance is the LOCAL atomic capture
action. The predecessor is released through its adjacent tag, and the
consumer commits the captured payload through(3). There is no global
majority decision, external copy interval, or perfectly stored message
index. The sender can overwrite when the actual downstream acknowledgement
matches its tag. In a fault-free execution from empty state, stale payloads
are never accepted. Under faults, stale/false acceptances are bounded
packet edits in(6); they are NOT certified absent at each notification.
The edit locations and the analysis-only damaged-packet labels are NOT
heralded to the consumer. An outer layer must correct unlocated edits,
not assume a supplied erasure flag or postselected correct delivery.

A consumer that trusts a single held notification bit alone cannot obtain
error exp(-c n) merely because
other payload storage has n redundant bits. For example, let an idle
notification bit a be repaired to0 at total rate at most R, and allow a
fault reset a<-1 at rate lambda. During a window h, the event that a fault
occurs and no later repair occurs gives the exact lower bound

    Pr(a=1) >=lambda/(lambda+R)
                    [1-exp(-(lambda+R)h)].             (18)

At h=1/(lambda+R), this is at least lambda/[2(lambda+R)]. No n appears.
In the FIFO itself, an endpoint-tag flip creates a head packet which a
nominal consumer may commit before another repair. Hiding that tag behind
an ideal final-majority reader would change the physical consumer.
This is not a no-go for an encoded consumer that verifies a larger state
or a paid history/temporal test. It identifies the missing interface rather
than forbidding those different operations.

Likewise, from an arbitrary state a queued packet is indistinguishable
from a packet just lawfully captured before initialization was lost.
Ghost-free liveness from EVERY state is unavailable without a trusted
freshness/preparation promise. The bounded initial ghost allowance is
therefore explicit. The standard data-link literature has stronger exact
initial-corruption metrics for its stated channel models; no new generic
impossibility theorem is claimed from this elementary indistinguishability.

Thus this packet supplies a composable DYNAMIC NOISY FIFO, with bounded
edits and a real state-restoring tail. It does not turn its physical ack
tag into an exponentially accurate logical acceptance state. A fault-
tolerant encoded consumer/codec is the next resource, not an invisible
ideal register. The earlier expander register/copy contract is preserved
frozen; it is not used as though arbitrary mutable phase bits were already
protected by it.

## 6. Geometry, costs and ordinary comparator

All control is one-dimensional nearest-neighbour at the stage-cell level,
with fixed B. Each bit participates in O(1) nominal maps at bounded rates;
every map has support<=2B+3. Packet width B growing with the problem must
pay its actual bits and support, or a serial implementation with its own
protocol. Poisson attempts are the stated ideal generator, not a claim of
acquired physical gates, readout, atomicity or reservoir realization.

No extra state is retained for error detection, pulse timing or history
rewind. Source and consumer application states are not silently declared
perfect: an internal application can be incorporated as another stage;
a noisy external scalar notification has the limitation in(18). Accepted
input values themselves are explicit supplied data. This is not a full
reliable-computation theorem for the applications producing/using them.

Serial composition is literal stage concatenation. At any prefix its
error bound remains(6), with total fault count; it does not multiply the
number of edits by the number of downstream stages. The work of each
nominal packet hop and actual controller noise remain charged. For a
growing line, sufficient reset noise in(12) is O(1/[q M^2 log M]) per bit,
not a length-independent threshold. Constant-size pipe cells have an
explicit constant-rate noise contract, but no global constant-noise wire
or protected computer is inferred by renaming those cells.

The controlling ordinary mechanisms are Sutherland's micropipelines,
Muller/dual-rail asynchronous handshakes, exclusion/queueing graphical
representations, and stabilizing data links. The positive construction
admits them fully. See PRIOR_AND_DECISION.md for actual primary scopes.
Its useful output is an explicit bounded-effect sustained-noise transducer
and schedule-uniform reset lemma. Historical priority is UNKNOWN; the
generic architecture is already established.

## 7. Feedback rings require a separate restoring mechanism

The open ready-consumer boundary is load-bearing. Closing these stages
into a ring makes the occupancies an exclusion process on a cycle, where
nominal moves conserve particle number. For an even number of tag cells,
the alternating pattern0101... has every occupancy equal1. No10 pair
exists, so EVERY nominal channel is the identity. All equal tags likewise
give an empty ring with no enabled move. Flipping one tag of an alternating
pattern gives two adjacent holes; flipping it back fills the ring again.
Thus a single local phase fault can reach a nominal deadlock from a valid
nearby ring state. It is not legitimate to turn a proved feed-forward
FIFO into a fault-tolerant autonomous clock by closing a feedback wire.

This is an ordinary token/bubble conservation obstruction, not a new
general autonomous-computation impossibility result. Noise can also
unfreeze a ring, and we do not infer a lifetime law from this one state.
A source/drain, protected token/hole maintenance, or a different eroder
must be paid for feedback. The all-state line theorem does not supply it.
