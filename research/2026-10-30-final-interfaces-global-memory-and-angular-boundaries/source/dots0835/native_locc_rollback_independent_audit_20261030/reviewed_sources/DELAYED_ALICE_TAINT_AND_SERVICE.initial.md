# Live-engine FIFO, delayed Alice taint, and actual good service
2026-10-30. Companion to `EXTENDED_MACHINE_AND_OPERATOR_PROOF.md`. New candidate; old atomic theorem and clean rollback audit remain frozen.

## Result first

The native engine can be connected to the finite FIFO without erasing a live prefix or losing a canceled READ. The necessary changes are concrete:

1. Bob captures a private program once, ignores all subsequent replies while active, and starts a new complete purge only at an **actual complete Q0 retirement**.
2. Alice keeps one pending READ through rollback and cleanup; neither a held reply nor a new request may cross its worker boundary until its engine is I.
3. Dirty Alice DATA emissions are explicit new causes of neighboring Bob semantic marks. Primitive faults alone are not enough. The resulting causal graph has depth at most two, because Bob emissions cannot affect Alice and cannot invalidate another clean Bob engine's locked snapshot.

These are actual machine/record statements. A new uniform actual service path exists. The scalar independent-watchdog marked moment from the atomic theorem is **not** imported; the new distinct-root COUNT-moment candidate is in DEPTH_TWO_EMISSION_COUNT_MGF.md and awaits independent review.

## 1. Alice worker: complete finite transition table

For each Alice check/read hub a use a worker register

    IDLE, REQUEST, HOLD(ACK), HOLD(DATA(y)),

where y ranges over the fixed finite read alphabet. Its engine I/A/C/B/Q/R is the machine in the companion. The worker is genuinely classical: all entry/write/read channels are basis-resolved and all interparty packet hops are measured/dephased before transmission.

| Guard/event | Worker action | Engine action |
|---|---|---|
| I + IDLE + front SYNC | dequeue request; HOLD(ACK) | stay I |
| I + IDLE + front READ | dequeue request; REQUEST | stay I |
| I + REQUEST + load attempt | keep REQUEST | complete W/P load, I->A0 |
| native successful READ terminal | overwrite worker with HOLD(DATA(y)) | complete C_L->Q0 reset |
| native rollback/dirty/nonprefix retirement | preserve worker | complete reset to Q0 |
| native cleanup READY | preserve worker | Qk->I |
| I + HOLD(v) + reply space | enqueue v; IDLE | stay I |
| every other combination | no worker/request/reply action | only its declared engine transitions |

A nominal READ does not alter Alice's stabilizer syndrome in the dressed frame. Its exact terminal unitary/instrument is the compiled stabilizer-read circuit, with all W outcomes separately resolved and the outcome y written to this **physical held register**. A rollback keeps REQUEST and retries after readiness; it does not pretend a canceled READ generated DATA. SYNC produces ACK without launching the quantum engine.

The table applies even to malformed combinations such as C+HOLD or B+IDLE. In C+HOLD, HOLD cannot enqueue; terminal replaces it before Q->I, or rollback/abort preserves it. No branch can enqueue the old HOLD and later also export the same old active engine. This is why the old worker allowance of ONE pending response remains valid. If enqueue were allowed while the engine is C/B, the allowance would be two and the old purge capacity argument would be invalid.

The worker never accepts a new request until both IDLE and I hold. Thus an unfinished old READ cannot be hidden behind newly answered SYNCs. In a healthy REQUEST, all abort/cleanup cycles preserve the pending request until one successful read produces one held reply.

## 2. Bob master: immutable cache transfer and actual retirement

Use the atomic theorem's master phases FLUSH_SEND(c), FLUSH_WAIT(c), READ_SEND, READ_WAIT, WANT(a), with finite c=0,...,G, plus BUSY and DRAIN. Here

    G=C_req+C_resp+1.

Q0 retirement resets the master to FLUSH_SEND(0), clears the outer cache, and resets the engine W,P. It does not itself release any tag. Cleanup runs until I. Flush traffic may proceed during cleanup, but native LOAD is enabled only at I+WANT(a).

The complete new rules are:

- responses are dequeued in **every** master phase;
- ACK advances c only in FLUSH_WAIT;
- DATA(a) writes WANT(a) only in READ_WAIT;
- every other response is discarded, including BUSY/DRAIN responses;
- I+WANT(a) loads P=a, W=0, engine A0, master BUSY in one onsite resolved instrument;
- P is immutable in A/C/B and their live-prefix abort leaves;
- the prefix watchdog C_t->B_(t,t) sets DRAIN but does NOT clear P, W, tags, or semantic history;
- every complete T_h retirement starts FLUSH_SEND(0), consuming the old program;
- no master transition can start another quantum engine before I.

The actual retirement therefore establishes a **future quarantine**: a later load cannot occur without passing the complete G+1-SYNC purge. It is sound to clear an analytical mark at retirement, rather than at flush completion, because no uncharged commit can occur during the mandatory intervening quarantine. This assertion fails if LOAD is reachable directly from a stale WANT/cache or if retirement does not force c=0.

## 3. FIFO purge remains exact with live engines

At a Bob retirement at most C_req old requests, C_resp old queued replies, and ONE worker-held/active potential reply exist. The active and held possibilities cannot both be exported by the table above. Every accepted old READ generates at most one reply; retrying a canceled read does not duplicate it. The worker completes its previous request before processing the next. Therefore at most G old replies can be generated/dequeued after the retirement, regardless of how long the native engine takes.

After G+1 accepted SYNC acknowledgments, at least one accepted ACK is fresh. FIFO order and the worker's no-next-request rule put every old request and reply before it. A later READ thus receives a genuinely post-purge Alice result, absent a new relevant fault or a separately charged delayed dirty emission. Leftover SYNC/ACK packets cannot generate DATA. There are no epoch tags or delay assumptions.

`check_fifo_engine.py` explores every initial old queue/worker/engine combination for capacities (1,1) and (2,2), including malformed active-engine/HOLD combinations. Results: 2,643 reachable states, 7,482 directed transitions, zero accepted stale DATA, zero nonterminal dead states, and a finite path to fresh success from every state. The abstraction preserves pending requests and native rollback/cleanup order; it checks classical causality, not Hamiltonian probabilities.

## 4. Why primitive-only marks fail: an actual allowed delayed mechanism

An Alice owner g can be mechanically corrupted in acquisition before it owns all eventual DATA. For example order its resources (r2,r1), corrupt A1 so that expected r2 is missing while r1 is still free, and leave the primitive fault in the past. A Bob master h can now retire, flush, and receive an Alice stabilizer read involving r1 before g acquires r1.

The corrupted g subsequently takes the permitted A1,free(r1)->A2,o_g(r1) edge, commits into C0, and runs the owned r1 part of a stabilizer-read circuit. Choose the local gate order so that a controlled-X on r1 precedes a gate on the missing r2. The latter gate is disabled. A failed ownership test then drives a dirty R(C_t,j) leaf and a complete dirty reset. Tracing the partly entangled ancilla can dephase by X_r1; this changes a neighboring Z-type Alice stabilizer. The previously cached Alice value at h is now stale, even though no physical fault occurred after h's reset/purge. All these finite desired path segments have positive actual monitored probability.

Thus this is not defeated by the fact that a dirty committed engine holds its current DATA: a malformed acquisition component can acquire r1 **after** the neighboring read. It is precisely the delayed first retirement permitted by the native full-Hilbert machine.

The naive atomic rule, 'a physical fault marks h and the next h watchdog clears h forever until another physical fault', incorrectly labels the later Bob correction unmarked. The fix must account for the dirty Alice retirement at its actual time.

## 5. Exact two-layer mark invariant

Maintain passive classical marks on the real fault/reset record. These marks are not physical perfect flags and are never measured to control the machine.

### Mechanical marks

Each primitive dressed fault marks the bounded set of Alice/Bob engine history neighborhoods it touches. Each T_h clears h's mechanical mark **after** counting that retirement. The companion's individual-instrument no-creation proof makes every mechanically unmarked source a genuine clean prefix source coefficientwise.

### Bob semantic marks

A primitive fault sets all Bob semantic marks whose complete Alice read dependencies, classical paths/cache/program, or Bob local engine/dependencies it can corrupt. In addition, each mechanically marked Alice T_g retirement sets every Bob semantic mark whose Alice raw-read footprint intersects the ACTUAL potentially changed Alice DATA or whose reply can be emitted by g. A fixed bounded superset of that footprint may be used for charging. Bob T_h clears h's semantic mark after its own possible emission, because it starts the forced purge.

Every semantically and mechanically unmarked Bob terminal is exactly the intended ordinary GPT move on the **current dressed relative syndrome**:

1. post-retirement purge removes every prior packet/source contamination;
2. a later invalidating Alice primitive fault or dirty retirement would have set h's semantic mark;
3. clean Alice terminal measurements preserve all Alice stabilizers;
4. Bob's full read/write footprint is exclusively owned from acquisition completion to actual retirement, and the clean prefix is removed by the forest frame;
5. Bob's snapshot/correction is the exact finite local payload with immutable P.

### Why no Bob-to-Bob propagation is missing

A dirty Bob retirement's dressed DATA action is supported only on resources ACTUALLY tagged to that retiring owner. It does not act on every resource of its worst-case declared footprint when those resources belong to another owner. A different mechanically clean Bob engine in C/B owns its ENTIRE raw-read footprint, so those actual supports are disjoint. A clean Bob engine still acquiring has not taken a fixed snapshot; it reads current data after commitment. Therefore a dirty Bob emission cannot invalidate a different clean Bob snapshot. If the other engine is already mechanically dirty it is already charged. This actual-ownership statement, not mere bounded support, is what prevents further nominal taint generations.

Bob never changes Alice DATA. Classical traffic from Bob contains SYNC/READ only, not quantum operations on Alice. Hence the only emission-mediated mark edge is

    primitive fault -> dirty Alice T_g -> Bob T_h,

alongside direct primitive-fault -> Bob T_h. There is no unbounded infection process.

## 6. Deterministic bounded ancestry and its quantitative boundary

Let b_A,b_B bound the numbers of Alice mechanical and Bob combined marks set by one primitive fault, and let c_AB bound the number of Bob marks set by one dirty Alice retirement. Choose the LAST incident primitive fault as ancestor of each mechanically marked Alice retirement. Each fault ancestors at most b_A such retirements. Choose the LAST mark cause as ancestor of each charged Bob retirement; this is either a primitive fault or an Alice retirement. A mechanically clean but semantically marked engine is charged only at SUCCESS: its clean rollback is DATA identity even for a wrong immutable program. Each cause ancestors at most one subsequent retirement at each marked Bob owner. Consequently one primitive fault ancestors at most

    b_A + b_B + b_A c_AB

potentially bad reset emissions, with ancestry depth at most two. Overlapping faults and overwriting marks only reduce this count. The claim is deterministic on every complete physical record, not an independence claim.

For a direct ancestor edge, the target owner has no T retirement between the ancestor and its marked emission. A two-edge path requires an Alice no-T interval followed by a Bob no-T interval. The companion supplies actual finite-support killed witnesses for both laboratories. A single path's total delay therefore has an exponentially summable bound (a convolution of two exponential survival kernels, weakened if needed to a smaller exponent). This statement is uniform in retained quantum states and references when proved using the killed instruments rather than normalized rare records.

**Not yet certified here:** the full many-target partition sum with shared Alice parents and overlapping Alice/Bob witness supports. The direct-parent theorem `transactional_physical_cell_faultmass_20261029/ANCESTOR_WITNESS_THEOREM.md` is an exact useful starting point, but it cannot be cited verbatim: its roots are physical Poisson points, whereas the second-layer births here are delayed quantum reset events, and shared parents must not be counted as independent Poisson roots. One must retain the bounded causal forests, charge each shared Alice survival interval once, use the actual joint killed-witness comparison on a bounded overlap coloring, and prove a summable forest row bound. No scalar mean lifetime or marginal exponential tail alone closes that obligation.

Accordingly we have NOT claimed a new arbitrary-spacetime marked-emission MGF, or the final native exponential-time Bell-buffer theorem. What is now explicit is its correct finite-depth causal mechanism and the actual reset/service operators it needs; the old incorrect primitive-only two-state mark model has been removed.

## 7. Uniform actual useful service, not an external schedule

A favorable finite **actual-record event** can force a correct full transaction from arbitrary local machine/channel contents, absent newly charged faults/dirty Alice emissions during the relevant segment:

1. force Bob h through a complete T_h retirement, which normalizes the master and mechanical history;
2. clear all competing local Alice and Bob owners of h's finite footprints through their complete retirement and cleanup paths, ending I with no own tags; condition on no LOAD and no I-to-Q0 watchdog emissions afterwards for the rest of the word, retaining all their bounded no-jump losses in the native projected-path norm budget;
3. handle an Alice old active/pending/held response using the table in Section 1 and native finite paths; run a fixed round-robin of request/hop/worker/reply/receive transitions enough times to complete the G+1 purge;
4. every REQUEST macro executes native load, acquisition, complete commitment, forward gates, terminal read, cleanup and held-reply enqueue, suppressing that engine's watchdog during this selected successful macro;
5. after the fresh DATA arrives, load Bob's immutable program, acquire his full footprint, commit, execute the finite Bob gates, and take its actual terminal reset.

The atomic packet-accounting bound remains finite; every old pending read or current READ is replaced by a finite quantum macro, not by an assumed atomic read. Competing entries are onsite actual LOAD jumps with finite rate, so excluding them for the finite word has positive probability. All Hamiltonian background terms remain present; selected projected paths are justified by the finite-rate native monitor/Dyson estimate, not by turning those Hamiltonians off.

The union over initial local basis labels and all syndrome outcomes is a CP record event with a uniform effect lower bound p_service I for some fixed positive p_service and finite T_service. No specified syndrome outcome is required. Coherent initial controllers are covered by the initial actual monitor windows and their instrument estimate. The event is a proof witness, not feedback sent by an external perfect scheduler.

For a window that may start with dirty h, counting at least two actual successful Bob C_L terminal resets ensures the last follows a complete regenerative retirement; a favorable word can produce this in fixed time as well. Faults and delayed Alice dirty emissions that spoil semantic correctness must be charged separately. Repeated uniform service alone is not yet a large-deviation bound for many simultaneous service misses. A local analytical counter for the first two actual terminals and the inherited anchored-killed-witness construction are the appropriate route; the required joint event should be stated and audited, not replaced by iid word trials.

## 8. Initialization, noise, and honest completed scope

The native result starts with engines/workspace/program/owner tags clean (or with a separately charged sparse initial history/forest source). For the concrete initialization here Bob master is FLUSH_SEND(0) with empty cache; engines are I, W/P are initialized, and all resource tags are free. FIFO contents and Alice worker may be arbitrary finite classical states. Thus the first quantum LOAD is behind the actual full purge. Arbitrary Bob master/WANT is NOT included without a separate physical bootstrap latch. Arbitrary initially malformed quantum engines are not harmless: N dirty engines may each emit one O(1) DATA error even at external epsilon=0. Slowing successful commits does not suppress dirty abort resets. Nor does a Bell-source condition on bare DATA control an arbitrary extensive initial F dressing.

Noise here is additive sparse physical Poisson CPTP kicks with retained bath and bounded supports, while the nominal T_h instruments remain actual records. No continuous coherent/common-bath perturbation theorem has been imported from the separate native continuous-noise memory construction. Its reviewed ownership/forest/native gate machinery is reused only where explicitly rechecked.

Completed local steps: extended phase/claim table; exact full-Hilbert frame; individual no-creation and owner hold; actual full-state retirement tail; explicit classical live-engine FIFO; semantic taint-clear invariant; depth-two bounded ancestry; uniform actual useful-service path. Remaining promotion steps: independent review of the new two-layer COUNT-moment lemma and the many-owner useful-service tail, common positive-record window budgets and new global energy proof with their constants, followed by independent exact-source audit. This is substantially narrower than claiming a completed native LOCC memory theorem.
