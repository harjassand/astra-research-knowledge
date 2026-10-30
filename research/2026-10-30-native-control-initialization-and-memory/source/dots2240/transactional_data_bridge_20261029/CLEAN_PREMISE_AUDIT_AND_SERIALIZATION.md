# Clean premise audit and sharper serialization route
2026-10-29. Independent review of root's `producer-workspace/CLEAN_TRANSACTION_INSTRUMENT.md`.

## Clean premise: sound with stated output convention
The Feynman-gauge calculation is sound under the declared clock-diagonal workspace-blind monitor instruments, actual complete commit reset, fixed owned tags, and complete equal-rate terminal loss. For a retained terminal workspace label s the channel is the corresponding CP subchannel Phi_s, not Phi; summing s yields Phi. Arbitrary classical clock-record postselection remains unnormalized. No iid/Poisson clean clock law is inferred. This establishes genuine clean committed-operation semantics and should replace any attempt to infer semantics from a monitored clock walk.

## Exact additional algebra inside a dirty computation component
Let D_h=C∪R(C), stopped at its first terminal/abort exit. Fix a possibly coherent own-mask O_h=(1_{lock_r=o_h})_{r∈R_h}. The mask is conserved. Every h gate and abort drive in D_h commutes with every other hub's gate, acquisition, abort, and monitor term while h remains in D_h:

* an external gate on r is supported on a tag different from o_h, so its product with an h gate on r is zero in both orders;
* an external acquisition changes free↔o_g, both non-o_h, so it commutes with every h gate guard and failed ownership test;
* an external term on a different payload resource is disjoint from h's payload/workspace;
* all h abort tests depend only on own versus non-own tags, not which other owner holds a missing tag;
* cleanup of o_h is disabled throughout D_h; lock monitors are label-diagonal and commute with the h computation/abort terms.

This is stronger than a graph-path claim: the local killed D_h evolution has no feedback from changes among external owners' non-h tags. Its output may still be correlated with the conserved quantum mask. Its terminal/abort reset is the boundary where deferred release becomes enabled.

## Broad initial-component coherence
For one marked hub, A∪R(A), C∪R(C), and Q∪R(Q) are distinct Hamiltonian components. Connecting resets are separately labeled instruments with a source in only one component. Consider an output instrument observed until that hub's first post-kick terminal/abort reset. If the actual reset record is refined to include commit/ready/abort source labels, the first component-changing jump on every surviving record annihilates all but one initial broad component. Consequently cross terms between different initial broad components make zero contribution to that retired record map. This permits virtual initial dephasing into broad components for that **retired instrument**, even though it is not valid for the unretired finite-time quantum state.

For several marked hubs, the initial broad-component projectors commute. The same argument can be iterated once every marked hub has retired. It requires a genuine eventual-retirement theorem or an explicit no-retirement remainder; normalization on retirement must not be hidden.

## Candidate route, not a claimed completed proof
Within a selected initial computation component, commuting local killed evolution suggests pulling the dirty DATA/workspace instrument to episode entry, while retaining its full local reset-time/output record and deferring lock release to the original reset time. Initial acquisition components have no payload action before their irreversible fresh-workspace commit; their malformed computation episode can be treated similarly from commit.

The resulting object is naturally a bounded-support quantum instrument with controller memory and record outputs, not immediately a data-only channel. In particular, quantum lock masks can remain correlated with data after the workspace reset. A complete serialization theorem must explicitly carry this memory through the subsequent clean scheduler, or show how the actual clean commit record reduces it to classical causal control. Simply tracing out the masks and drawing an independent clean schedule is wrong.

A finite number of marked episodes plus the above commutation algebra is thus substantial progress toward, but not yet a proof of, a bounded-data-location fault norm. The proof must also fold interrupted pre-kick clean prefixes into a bounded cluster, and handle a finite observation horizon with unfinished clean/dirty transactions.
