# Standard linear-time queue implementation of ideal GPT terminal recovery
2026-10-30. Optional implementation improvement; does not alter any frozen source or the terminal D0-only proof. This is ordinary bounded-dependency decoder machinery, not a new architectural advantage over the published GPT decoder.

Fix the local lookup tables and all raw-syndrome dependency sets from EXPLICIT_GPT_TRANSACTION_CIRCUIT.md. After one ideal complete stabilizer-syndrome snapshot, keep its bits in classical memory and compute all subsequent updates deterministically.

Initialize a FIFO queue with all hubs in a fixed order and a Boolean membership flag per hub. Repeat:
1. Pop h and clear its membership flag.
2. Evaluate h on CURRENT stored syndrome using its exact table.
3. If no strict decrease exists, do nothing.
4. Otherwise record its chosen Pauli mask, update the raw syndrome by the precomputed XOR mask, and enqueue every hub whose full raw-syndrome dependency intersects a changed bit, unless already queued.
Stop when the queue is empty. A popped hub can be re-enqueued by its own accepted correction. All tie breaks and initial ordering are fixed, so this is a deterministic syndrome-to-correction map.

The invariant is: every unqueued hub has been evaluated since the last change to any of its decision dependencies, or is currently being evaluated. Therefore empty queue implies no improving hub. No stale candidate is executed: the rule is recomputed at pop time. The same componentwise density argument as the scanned decoder then proves U=0 on the common safe-record span.

Every accepted move decreases nonnegative integer U by at least one, and initially U<=2N, so there are at most 2N moves. Each changes at most d w raw check bits; each bit is read by a fixed bounded number b_dep of hubs. Hence at most d w b_dep new queue entries are added per move. Initial entries are O(N), so the number of pops/table evaluations and queue operations is O(N). Maintain membership flags and direct dependency adjacency lists for O(1) amortized insertion and update cost per fixed-degree event. The cumulative correction mask is updated on at most w data bits per move, also O(N). Classical storage is O(N).

All constants include the enormous fixed local-code table and workspace construction costs; linearity is in N after Delta is fixed. The one full syndrome snapshot costs O(N) ideal local check evaluations. The entire queue computation remains ONE formal noiseless D0-only suffix, not a sequence of fictitious physical-time service blocks. Its order need not match the fixed-scan order; D0 and the common correctable-span argument require only actual strictly decreasing moves and a terminal no-improvement condition.

This reduces ideal classical processing from the conservative O(N^2) scan bound to O(N), but does not solve physical quantum-output retrieval during nonzero classical latency. Noise during extraction, physical inverse-frame gates, classical reliability and fault-tolerant preparation remain separately charged. Destructive basis readout can avoid storing a quantum output during classical processing, but needs its own operational measurement interface.
