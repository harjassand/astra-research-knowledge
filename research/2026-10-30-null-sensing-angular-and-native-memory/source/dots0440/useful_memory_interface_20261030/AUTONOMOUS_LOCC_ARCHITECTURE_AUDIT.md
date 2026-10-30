# Concrete autonomous LOCC bilateral buffer in a broader jump model
2026-10-30. Architecture and proof audit. This is NOT the native two-site-Hamiltonian/onsite-reset compiler. It uses explicit finite-rate, bounded-body CPTP instrument jumps within a laboratory and finite-capacity classical FIFO channels between laboratories.

## Result first

A concrete baseline-free autonomous architecture exists in this broader model. It needs no global schedule, persistent random syndrome baseline, distributed locks, or unbounded message identifiers:

- Alice performs ONLY local measurements of commuting code stabilizers.
- Bob alone applies all nominal Pauli corrections.
- A Bob hub obtains an Alice syndrome reply through a private finite FIFO request/response channel.
- Its commit is one local bounded-body CPTP jump that measures Bob's CURRENT full relevant syndrome, compares it with the cached Alice reply, and applies the fixed GPT move.
- A local watchdog cancels pending work, resets the hub to a finite FIFO-flush protocol, and clears its cache.

Alice's nominal syndrome is unchanged by every nominal operation. Bob's snapshot is obtained AT commit. Therefore neither distributed locks nor Bob locks are needed in this atomic-local-instrument model. They would return if one compiled the Bob commit into a finite sequence of quantum gates.

Finite tags alone are not an answer to arbitrarily delayed stale packets. The explicit finite-capacity FIFO protocol below removes all pre-epoch READ/DATA messages, without sequence tags, before a new read may be used. Every packet and pending reply must be an actual counted channel/register state; an unrepresented external in-flight queue is excluded.

## 1. Scope and physical primitives

For each sector/view hub h, let Q_h be its bounded correction support, V_h the affected potential views, and R_h their full DATA union. These are the same finite local footprints as the explicit GPT table. There are two copies R_h^A,R_h^B.

Allocate per hub:

1. At Bob, one finite classical master: a flush counter, phase, and Alice-reply cache.
2. At Alice, one finite worker with states IDLE or HOLD(response).
3. A private directed FIFO path Bob->Alice for requests and another Alice->Bob for responses. The paths have fixed total capacities C_req,C_resp and a fixed number of local hops. All alphabets are finite: requests are SYNC or READ; responses are ACK or DATA(a), where a is the finite local syndrome tuple.

Each nominal transition is attempted by its own independent fixed-rate Poisson clock. A disabled transition is the identity channel. These clocks are internal autonomous dynamics; the favorable clock words used in the proof are not an external operating schedule.

Allowed primitives:

- finite classical measure/compute/prepare transitions on a bounded number of local registers;
- a classical FIFO-hop transition, moving a basis-valued packet to the next hop when space exists;
- a local Alice stabilizer-measurement instrument on R_h^A;
- a local Bob read/table/Pauli instrument on R_h^B plus its cache;
- a Bob-local master watchdog/reset.

Every classical transition reads/dephases its inputs in the prescribed basis. A cross-laboratory hop is a CLASSICAL measure/send/prepare channel, not a coherent CNOT or a shared quantum workspace. Within-laboratory quantum support can be as large as the fixed R_h. Rates, capacities, path lengths, arities and local dimensions are finite constants independent of N; they can be impractically large.

This is bounded graph locality. It is not a claim of fixed-dimensional Euclidean layout, an arbitrarily long constant-latency communication link, or a derivation of the above instrument jumps from two-site Hamiltonians. A hop's finite stochastic waiting time and all intermediate storage cells are counted. If channel length/capacity or mean latency grows with N, the constants and fault budget must be recomputed.

## 2. Exact local commit: why locks disappear here

Given Alice cache a, define the Bob commit instrument

    Phi_(h,a)(rho_B)=sum_b P_(f_h(a+b)) Pi_b^h rho_B
                               Pi_b^h P_(f_h(a+b))†.   (1)

The same jump consumes the cache, resets the master counter/phase to FLUSH_SEND(0), and cannot execute a second correction from that cache. Here Pi_b^h is the full local simultaneous stabilizer projector; f_h is the fixed finite syndrome-only strict-energy-decrease lookup table, including its no-op default.

All nominal Alice instruments measure elements of the same commuting code stabilizer group. None changes Alice's syndrome, and Alice never applies a nominal Pauli correction. Consequently a genuinely fresh Alice read remains valid until a physical Alice fault changes it. Other Bob hubs may correct while h waits: (1) reads Bob's CURRENT syndrome, so their changes are automatically included. Poisson jump times serialize overlapping Bob instruments almost surely. There is no multi-step quantum prefix hidden inside (1).

On a coherent Bell-target component (I tensor E)W|gamma>, Alice's local result is a gauge projection and Bob's result differs from it by the relative syndrome of E. Thus an untainted commit is exactly the ordinary relative GPT instrument, uniformly on coherent common-syndrome/bath states. This is the same Bell-target algebra proved in BILATERAL_BELL_ALGEBRA_AUDIT.md.

If (1) is replaced by a circuit with finite-duration extraction/computation/correction, its snapshot may become stale under another Bob move. That DIFFERENT model needs actual local read locks, safe abort/prefix treatment and an additional compiler proof. This file does not remove that obligation by terminology.

## 3. Explicit finite FIFO protocol

Set

    G=C_req+C_resp+1.                                  (2)

The final 1 counts Alice's possible already-held response. Capacities include every actual packet slot along the two paths. The worker processes requests in FIFO order, and cannot start another request until its previous response has been enqueued:

- IDLE + SYNC: remove the request and enter HOLD(ACK).
- IDLE + READ: remove the request, execute the fixed local stabilizer instrument, and enter HOLD(DATA(a)).
- HOLD(response): enqueue that response when possible, then return to IDLE.

The master starts in FLUSH_SEND(0). For i=0,...,G it enqueues exactly one SYNC and waits for an ACK. DATA replies are discarded. On an ACK it advances to the next probe; after G+1 acknowledged probes it may enqueue ONE READ. While waiting for that DATA reply, it discards ACKs. The first DATA is cached; a later commit attempt performs (1). After commit the master starts a new flush from counter zero.

A watchdog jump of fixed rate mu>0 is available in EVERY master phase. It cancels pending master action, clears the cache, resets the flush counter to zero, and enters FLUSH_SEND(0). It does not change DATA or any remote register. Already enqueued messages remain in their actual queues and are handled by the flush. No remote action needs to be canceled: Alice only measures commuting stabilizers.

### FIFO purge lemma

Immediately after such a reset, arbitrary pre-existing channel/worker contents can generate at most G old responses: at most C_req replies from old requests, C_resp responses already in transit, and one worker-held response. During flushing no new READ is sent, and every newly sent SYNC creates only an ACK.

After G+1 accepted ACKs, at least one ACK was generated by a SYNC of THIS flush. Strict FIFO ordering on both paths and the worker's response-before-next-request rule imply that ALL pre-flush requests and their replies preceded that fresh ACK and have already been consumed. Some SYNCs/ACKs from this flush may remain, but they cannot produce DATA. The subsequent READ lies after all remaining SYNC requests, and its first DATA reply is therefore genuinely its own.

This proves freshness from ANY finite channel contents after a fault-free reset/flush interval. No increasing sequence number, epoch wraparound convention, hidden channel-empty oracle, or bounded maximum packet delay is used. Finite capacity and strict FIFO/no-spontaneous-duplication are essential. Stochastic delay may have an unbounded tail; those delayed packets still occupy the counted finite slots.

A fault may corrupt the master counter or jump it directly to COMMIT, so a single faulty epoch can still make a bad correction. The fault mark below pays for it. The protocol is not asserted to make faults impossible.

## 4. Uniform service from an actual finite clock word

There is a state-independent finite word of local clock ATTEMPTS that takes h from arbitrary controller/channel state through a correct flush, a fresh READ and one commit:

1. Fire h's watchdog once.
2. Repeatedly give master enqueue/receive, every FIFO hop, and Alice worker process/enqueue attempts in a fixed local cyclic order.
3. Allow the READ, its response, and finally the Bob commit; exclude further h watchdog attempts until completion.

There is a fixed upper bound on the number of repetitions needed. Each finite pipeline initially contains at most C_req+C_resp packets; only G+1 flush probes and one READ are subsequently generated. Fair repeated local attempts drain every blocking queue and process these finitely many packets. Ghost ACKs can advance the flush sooner, never require more probes. The worker's measurement outcomes change DATA payload values but not the number or routing of packets. The word therefore succeeds uniformly for all quantum states and all classical channel contents.

Give each required attempt its own positive-duration time box and exclude interfering attempts where necessary. All rates are finite positive constants. The probability p0 of this word in duration T0 is strictly positive, independent of N, initial quantum state, retained bath and common syndrome. Excluding primitive faults on its fixed footprint multiplies p0 by a further positive factor at sufficiently small noise rate. Other Bob corrections need not be suppressed: if they change a packed candidate's raw dependencies, that candidate is already resolved and charged in the usual persistence argument; otherwise they do not invalidate (1).

The service word has bounded physical support. A fixed conflict coloring makes the clock/noise footprints of tested words disjoint. Repeating independent time boxes R times makes the nominal service-miss parameter at most (1-p0)^R, up to the separately charged primitive-fault/marked-operation events. Choose R first, then the primitive fault threshold. These are the ordinary actual-record inputs to the packed-candidate window contraction.

## 5. Fault marks clear at a LOCAL watchdog, not at an ideal global reset

Let a primitive fault mark every hub whose full read/controller/channel dependency patch it touches. The incidence and patch size are bounded constants. In particular, an Alice DATA fault marks every hub whose cached Alice checks could have become stale. Bob DATA faults can be included conservatively, although (1) reads their current syndrome.

Clear h's analytic mark at its next NOMINAL watchdog jump. This is sound even if its remote queues still contain arbitrary old packets: the master is now forced through the entire G+1 purge before it can use any cache or commit. With no subsequent relevant fault, every future commit is clean. A watchdog arriving in the middle of flushing simply restarts it; no incorrect quantum action is performed. A stale DATA packet cannot escape the purge lemma.

These marks are ANALYTICAL labels on the actual record, not an assumed noiseless physical flag. A marked commit is charged as an arbitrary Pauli mask on its bounded Q_h, together with a valid stabilizer measurement. Direct primitive DATA fault masks are charged separately. Unmarked commits strictly decrease the true relative GPT energy whenever nontrivial. This supplies the unconditional D0 bookkeeping without classifying Pauli coefficient amplitudes as probabilities.

## 6. Explicit small bad-mass estimate

Assume exogenous bounded-incidence local Poisson faults of rate at most epsilon per primitive support, with arbitrary CPTP system/bath action at each event. Let nu bound the number of primitive clocks capable of marking h. The master watchdog clock has fixed rate mu and is independent of primitive clock times. Starting clean,

    Pr[h marked at a fixed time] <= epsilon nu/mu.       (3)

This is the probability of a relevant fault since the last watchdog, bounded by the competing-clock birth/reset process. Shared-bath correlations change operator coefficients, not this exogenous positive record.

Let N_h be the independent Poisson clock of commit attempts, rate lambda_c. For a fixed window of duration T, the number B_h of marked commit attempts satisfies, for fixed theta>0,

    E exp(theta B_h)
      <=1+[epsilon nu/mu+epsilon nu T]
              [exp(lambda_c T(e^theta-1))-1].           (4)

Indeed the mark process depends only on primitive/watchdog clocks and is independent of N_h. If h is never marked during the window, B_h=0; otherwise dominate it by all N_h attempts. The probability of any mark is at most its starting mark probability plus the probability of a new relevant fault. Equation (4) is uniform in the window index, even after an exponentially long prior run.

Hub mark processes share primitive clocks only within fixed dependency neighborhoods. Color this bounded-overlap graph. Within each color their exogenous clock sets are disjoint, so (4), followed by Holder over the finitely many colors, gives

    log E exp(theta Q_bad(W)) <= c_theta epsilon |W|    (5)

for a fixed DATA set W and fixed T, after enlarging the fixed patch/incidence constants. Q_bad includes direct primitive masks and the full correction patches of marked commits. The constants can be very poor but are N-independent, and the coefficient tends to zero with epsilon.

In particular, for the all-DATA set and any fixed small q>0, choose epsilon sufficiently small and obtain

    Pr[Q_bad(all DATA)>q N] <= exp(-c N).               (6)

There is no assumption of fresh independent marks each round. Equation (3) explicitly accounts for persistent marks until a real local watchdog; temporal correlations are allowed. For a more general state-dependent fault process, (3)-(5) require an appropriate uniform dominating positive-clock construction and do not follow merely from a claimed marginal error rate.

## 7. From the architecture to relative protection

The reviewed deterministic GPT energy/persistence argument now has the needed semantic inputs:

- exact unmarked relative-GPT commits;
- bounded-support marked commits and primitive masks, with (5);
- uniformly positive actual good-service words and amplifiable miss tails;
- coherent gauge/bath validity of every nominal instrument.

For the linear-distance/linear-confinement Tanner family one can use the parent's global-energy first-exit route. With constants fixed, a physical-window contraction has the form

    U_(j+1) <= (1-a) U_j+A Q_j+B M_j,

with Q_j the common bad-mass majorant and M_j the actual service-miss majorant. Small all-DATA Q_j,M_j keep U and stabilizer-reduced relative weight inside a fixed linear radius; each canonical local edge then has trivial relative logical action. Their positive bad-window tails union-bound to C N(1+t)exp(-cN), or the corresponding discrete-window form. The Bell common-span recovery proof gives the decoded known-Bell target error; it does not protect arbitrary logical inputs against common Pauli errors.

The service-miss construction and chosen deterministic constants should be checked against the parent's exact contraction before promoting the complete numerical theorem. The physical architecture, freshness lemma and low-noise mark estimate above are explicit; they do not rely on an imaginary perfect syndrome register or a global scheduler.

## 8. Exact remaining boundaries

1. **Primitive class changed.** The Bob commit and Alice read are atomic bounded-body local CPTP instrument jumps. No two-site-Hamiltonian/onsite-reset realization has been supplied. Classical hopping is a genuine cross-laboratory communication primitive.
2. **Queues are real resources.** Every delayed packet/ack is in a counted finite FIFO slot. Unbounded hidden packet storage, arbitrary duplication or reordering would invalidate the purge proof.
3. **Source/endpoint costs remain.** Physical Bell sources, their acquisition synchronization, the full-mask encoded teleportation/swap endpoint, finite transmission time and safe mode changes retain their previously stated obligations.
4. **Strict LOCC noise accounting.** The nominal machine is LOCC. If adversarial kicks access an entangled bath shared between laboratories, the robustness statement still has its local-support meaning, but the faulty total channel need not be LOCC as a resource-theory claim. Local baths and shared classical randomness suffice for strict LOCC operation.
5. **No efficiency claim for constants.** All finite alphabets, tables, capacities, rates and graph footprints are fixed in N, not necessarily experimentally reasonable.

This supplies a concrete autonomous finite-state LOCC candidate beyond the previous scheduled circuit, with the key stale-message and persistent-taint mechanisms resolved. It does not relabel the existing shared coherent hub as LOCC or silently claim its native compiler was already proved.
