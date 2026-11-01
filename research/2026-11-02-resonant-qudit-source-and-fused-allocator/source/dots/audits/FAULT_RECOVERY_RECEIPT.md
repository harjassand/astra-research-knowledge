# Adversarial all-state audit: fused abort-on-contention allocator

2026-11-01. Read the independent constructor's first derivation, reconciliation audit, and FUSED_GRAPH_PROTOCOL_REFRESH_THEOREM.md. This is a receiving audit after architecture exposure, not an independent invention. No external actions or source retrievals.

## Verdict

No structural counterexample found. The fused protocol has a graph-size-independent local self-stabilization proof from EVERY phase/edge-owner assignment, conditional on the separately established uniform native completion bound from arbitrary active quantum states and neighboring dynamics. Exhaustive finite-graph SCC checks support the exact invariant below. This receipt does not replace the native quantum completion proof with exponential ACTIVE timing and does not certify practical service constants.

## 1. Local invariant that survives arbitrary neighbor phases

For vertex v with ordered incident edges e_1,...,e_d, define L_v:
* CLEAN_j: none of e_1,...,e_j is owned by v; the rest may have any owner.
* WAIT: no incident edge is owned by v.
* COLLECT_j: e_1,...,e_j are owned by v, and none of e_(j+1),...,e_d is owned by v.
* ACTIVE: every incident edge is owned by v.

CLEAN_0 always satisfies L_v, regardless of all initial locks and other phases. Every intended transition by v preserves L_v once true. In particular, a failed collection enters CLEAN_0; successful acquisition grows the owned prefix; completion enters CLEAN_0. The apparently redundant already-self acquisition branch is allowed on malformed initial states but is not needed to preserve a valid unprocessed suffix.

More strongly, EVERY intended transition by a neighbor preserves L_v regardless of whether that neighbor itself satisfies its invariant. A neighbor can only acquire an edge that is free or already its own, and can only release its own edge. It cannot overwrite owner v. Therefore local legitimacy cannot be lost by ideal neighbor activity. No global legitimate starting state is assumed.

When L_u and L_v hold, adjacent u,v cannot both be ACTIVE because their shared qutrit cannot equal both owners. Thus the intersection of all L_v is a closed, mutually exclusive controller set. This proves closure, not just absence of an observed deadlock.

## 2. All-state repair and explicit tail

From any starting phase, v reaches CLEAN_0 in a bounded number of its OWN nonblocking classical transitions plus at most one naturally completed native job and one WAIT delay. If it starts in CLEAN_j for j>0, finishing that partial scan does not certify removal of arbitrary stale locks; it must proceed through an attempt/abort or active completion and return to CLEAN_0. It then completes an entire cleanup.

Every classical CLEAN or COLLECT step has total hazard g regardless of neighbor ownership; a busy collection aborts rather than waits. The WAIT hazard is nu*g. All source lock-value branches are included, so arbitrary initial lock coherence does not introduce a zero-hazard state for these block observables. At most 3(d+1) rate-g steps, one rate-nu*g WAIT, and one active job suffice for the full-cleanup stopping time R_v.

Under the supplied conditional native bound E[exp(theta tau_A)|past,state]<=M_A(theta), and theta<min(g,nu*g), conditional moment multiplication gives
 E exp(theta R_v)
 <= [g/(g-theta)]^[3(d+1)] [nu*g/(nu*g-theta)] M_A(theta).
Independence of active completion clocks is NOT needed. The bound is local and independent of graph size. A local union bound over N[v] supplies a graph-size-independent regeneration tail for the target's conflict neighborhood. No claim is made that the time until ALL n vertices regenerate has an n-independent tail.

An orphan edge owned by v is removed during v's next full cleanup. It cannot persist forever while v is held behind another owner, since contention aborts immediately. Fusion is essential: there is no separate controller that can remain RUN with no probe, start cleanup while an unrelated probe remains active, or restart a probe halfway through its native job.

## 3. Exact finite-graph model checking

`check_fused_allocator.py` enumerates the full Cartesian product of all controller phases and all edge values {free,u,v}. It asserts preservation of each already-valid L_v under EVERY transition, checks that every legitimate state excludes adjacent ACTIVE vertices, computes all strongly connected components, and confirms that every closed SCC is entirely legitimate. Reverse BFS also verifies reachability of the legitimate set from every initial state.

Results:
| Graph | All states | Transitions | SCCs | Closed SCCs | Legitimate states | Maximum shortest repair path |
|---|---:|---:|---:|---:|---:|---:|
| isolated | 4 | 4 | 1 | 1 | 4 | 0 |
| edge | 108 | 216 | 32 | 1 | 40 | 5 |
| path3 | 2,592 | 7,776 | 552 | 1 | 405 | 9 |
| triangle | 13,824 | 41,472 | 4,946 | 1 | 1,026 | 11 |
| star4 | 58,320 | 233,280 | 7,900 | 1 | 4,182 | 13 |

The ACTIVE->CLEAN_0 transition is only an enabled STRUCTURAL abstraction. No exponential active holding time, numerical throughput, quantum fidelity, or first-passage moment was inferred from this graph. The graph theorem and native conditional completion theorem have distinct roles.

## 4. Fault descendants and contaminated in-flight reports

After an isolated apparatus/edge fault and absent further faults, the affected vertices regain L_v on the same bounded local repair window. An initially unvalidated ACTIVE state may overlap a neighbor; this is explicitly allowed before regeneration. It cannot create malformed controller phases through a report because the control logic never branches on cached syndrome values. A well-formed neighbor holds all its own locks and cannot in turn overlap a newly launched well-formed neighbor. Thus controller/ownership defects do not reproduce into an unbounded epidemic under the ideal transition rules.

This statement concerns allocator defects. Data/cache errors and probe entanglement created by an actual physical fault remain physical errors for the surrounding quantum-memory proof; they are not declared erased by cleanup.

Do NOT conclude that the first report after local control stabilization is correct. A target cycle already active when local regeneration completes may have been contaminated earlier. After max_(u in N[v]) R_u, allow that target cycle to finish (using the separate native residual completion tail), then demand one fresh isolated target cycle. A no-attempt drain word on N[v] followed by one target attempt gives a uniform positive local refresh event. Its probability may be extremely small. This additional flush is required to replace stale cache data.

The fused theorem's burn bound m S_R(B/2)+S_A(B/2), with m<=D+1, correctly handles this distinction: initially collecting jobs that launch after B/2 are already protected by the local invariants; only a target job active at B/2 needs the additional residual-completion allowance. A later fresh completed job overwrites the older contaminated report; target fusion prevents out-of-order completion of two jobs at the same vertex.

## 5. QND/source and quantum-coherence scope

The lock/cleanup/collection transitions act only between classical apparatus phases, whose Pauli-prefix dressing is identity. Preparation enters the native prefix-I stage. Native completion exits from the completed-check prefix, which commutes with every code stabilizer. Therefore these extra ideal transitions preserve the dressed true-stabilizer labels, assuming the parent's native factor-hop algebra. They do not add a probe reset/stop operation during activity.

Within native activity the supplied source proof, not this classical state graph, establishes transport and completion. An arbitrary initial ACTIVE state need not make a correct report. A freshly prepared isolated job uses the native QND instrument and its finite-purity error budget. Cache values are absent from the structural model because all controller hazards and destinations (apart from the written cache value itself) are independent of their sign.

The rank-one source-phase jumps and block-observable closure permit this classical phase/lock audit to imply operator statements for those observables even from arbitrary off-block coherence; they do not authorize physically inserting an extra dephasing step. Native within-stage coherences and arbitrary environment entanglement remain under the quantum completion premise.

## 6. Resource and consequence boundary

Accepted resource model: one finite per-vertex fused apparatus (dimension 8w+4D+10 in the supplied implementation), one physical edge qutrit per conflict edge, pairwise apparatus-edge acquisition/release jumps, nonblocking classical transition rates, native apparatus-data Hamiltonians, finite-purity preparation, coherent-preserving native decays, and physical report/cache disposal. All apparatus, lock and cache faults are charged. An error rate per whole apparatus is not interchangeable with the same rate independently assigned to every possible level transition.

This confirms the finite-qudit fault-recovery/ownership gate and the need for a separate report flush. It does not synthesize those qudits/jumps from fixed-small-dimensional hardware, establish advantageous throughput constants, or prove the final protected-memory theorem. A timed active comparator must receive exactly the same locks, apparatus dimensions, reservoirs and noise charges.
