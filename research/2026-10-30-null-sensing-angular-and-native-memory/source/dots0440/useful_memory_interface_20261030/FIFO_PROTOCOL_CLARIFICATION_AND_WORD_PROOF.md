# FIFO receiver clarification and universal service-word proof
2026-10-30. Addendum to the FROZEN AUTONOMOUS_LOCC_ARCHITECTURE_AUDIT.md; its original hash is unchanged. This clarification is load-bearing and matches the exhaustive check_fifo_flush.py implementation.

## 1. The response dequeue is enabled in EVERY master phase

Whenever the return FIFO is nonempty, an independent receiver-attempt clock may dequeue its first response, regardless of master phase. Its action is:

- FLUSH_WAIT + ACK: count this ACK and advance the flush counter/phase.
- READ_WAIT + DATA(a): cache a and enter COMMIT.
- EVERY other phase/response combination: discard the response, with no cache/counter advance.

In particular the master drains/discards responses while FLUSH_SEND is blocked on a full request FIFO, while preparing READ, and while in COMMIT. The finite physical table must implement this rule, not merely permit receiving in the two WAIT states.

Without unconditional dequeue, there is an immediate deadlock: the master is FLUSH_SEND with the request FIFO full, the return FIFO is full, and Alice holds a reply. The master cannot enqueue, Alice cannot enqueue her response or process another request, and a reset back to FLUSH_SEND does not clear either FIFO. Thus the interpretation 'receive only while WAIT' is invalid. The exhaustive test used unconditional dequeue and does not certify that invalid interpretation.

## 2. A universal cyclic word, not just a no-deadlock claim

After one watchdog reset, suppress further watchdogs and omit the COMMIT attempt temporarily. Repeat the same finite cycle of all these local attempt types:

1. master SYNC/READ enqueue;
2. every directed request-path hop;
3. Alice process-front-request;
4. Alice enqueue-held-response;
5. every directed return-path hop;
6. the unconditional master response dequeue.

Within-laboratory and channel clocks may be given disjoint positive time boxes in this order. Every attempt is defined on the entire finite state space; disabled attempts do nothing. The worker uses the exact finite IDLE/HOLD alphabet. Any unused hardware encodings, if registers are represented by ordinary bits rather than exact qudits, must first be assigned a finite legal interpretation/cleanup transition.

### No reachable non-COMMIT dead state

From the watchdog-normalized master, with no subsequent fault:

- A queued response can progress along its path or be dequeued at the master.
- A held Alice response can be enqueued, or the return path ahead of it has some enabled move/dequeue.
- A queued request can progress or be processed, unless the worker is holding a response, which is the previous case.
- If both paths and worker are empty, a SEND phase can enqueue.
- A WAIT phase cannot have all its pending communication disappear. The request that entered that waiting phase produces exactly one response of the accepted type, and consuming such a response would leave that WAIT phase. There is no packet-loss or spontaneous-duplication transition in the fault-free protocol.

Therefore, outside COMMIT, at least one attempted transition is enabled. If one complete cycle made no nontrivial transition, the state would stay unchanged throughout that cycle and all its transition types would have been attempted disabled, a contradiction. Every cycle before COMMIT makes at least one progress transition.

### Uniform finite bound on the TOTAL number of progress transitions

Let C_req,C_resp be total actual capacities and ell_req,ell_resp upper bounds on hop counts for any packet. Put G=C_req+C_resp+1. During one epoch the master generates at most G+1 SYNCs and one READ, hence at most G+2 new requests. Together with initial ghosts:

    R = C_req+G+2

bounds all requests that can be processed, and

    S = C_resp+1+R

bounds all responses, including the worker's initially held response. There can be at most:

- G+2 master enqueues;
- ell_req R request-hop moves;
- R worker process transitions;
- R+1 worker response-enqueue transitions;
- ell_resp S return-hop moves;
- S master response dequeues.

Thus one conservative bound on all nontrivial transitions before COMMIT is

    L=(G+2)+ell_req R+R+(R+1)+ell_resp S+S.           (1)

The count includes discarded stale responses and ignored current SYNC acknowledgments. It is independent of packet contents, initial channel/worker state, quantum measurement outcomes and N. No request is ever duplicated by nominal processing, and no new READ is generated until the flush is complete.

Since every pre-COMMIT cycle makes progress, L+1 repetitions force COMMIT. Further cycles cannot leave COMMIT while its commit clock is omitted; any remaining responses may only be discarded. Append ONE Bob commit attempt at the end. The FIFO purge lemma makes its cached DATA fresh. This yields a fixed state-independent finite service word rather than an initial-state-dependent path existence argument.

Every required attempt can be assigned a small fixed time box with its Poisson clock ringing and unwanted local clocks excluded. The probability of the entire finite word is positive and uniform over all controller/channel/quantum states after the initial watchdog. Quantum Alice outcomes change only message payloads; no specified outcome probability is required. Faults on the finite dependency patch are excluded in the clean service event and charged separately.

## 3. Source initialization remains physical

The bilateral quantum DATA need not start in a known syndrome code sector: raw physical Bell pairs are already in the coherent target span W, as proved previously. A bounded-depth bounded-incidence noisy raw-Bell source contributes a COMMON initial relative-support majorant Z_source. The global theorem must include the event Z_source exceeding its chosen linear threshold, not assume an encoded initializer.

The controller/channel initialization also needs an explicit convention. Clean finite master/queue/worker initialization is a legitimate stated apparatus initial condition. If its actual preparation is noisy, initial controller faults must activate the corresponding analytical marks or be included in a source-support event; they cannot be silently treated as unmarked clean controllers. The actual watchdog/flush protocol recovers their future behavior, but any bad commit before that reset remains charged.

## 4. Verification receipt

check_fifo_flush.py exhaustively explored arbitrary old request/reply/held-worker contents for capacities (1,1), (1,2), (2,1), (2,2), and (3,3), under every allowed asynchronous interleaving. It found no accepted stale DATA and no reachable deadlock, using the unconditional receiver rule in section 1. This finite test supports, but does not replace, the capacity-independent FIFO and bounded-word proofs above.
