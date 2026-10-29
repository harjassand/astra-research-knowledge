# Narrow repeated-storage consequence under a classical fault-pattern model

28 October 2026. Provisional derivation; independent review pending. Depends on `flagged_five_qubit_storage_round_20261028.md` and its exact checker. This is standard fault-tolerance reasoning applied to the instantiated operation, not a claimed new threshold theorem. It is deliberately narrower than general coherent ordered-CPTP noise.

## Model

A storage cycle consists of a declared ideal encoded storage/receiver operation followed by the actual flagged EC circuit. An isolated fault in the pre-EC portion must enter EC on at most one data qubit of each protected block under the existing interleaving contract. The ideal pre-EC portion preserves the code and does not spread a pre-existing correctable error beyond weight one. For the simplest memory case it is the identity in the declared calibrated logical frame. This last assumption is needed when flushing the residual from the previous cycle; merely correcting faults on initially clean inputs does not imply it.

Assume a **classical mixture of fault patterns**, independent of the unknown logical input, with every pattern's conditioned evolution CPTP and faults local at the allowed gates. A fault can be arbitrary local CPTP, not only a Pauli. Fault-pattern probabilities satisfy a local-stochastic two-event bound P(i and j faulty)≤p² for every pair of distinct potential locations. No independence of separate faults is required beyond that bound. Ideal operations and trusted controller are applied at unoccupied locations. This hypothesis is not equivalent to a small diamond-distance gate marginal, and does not license unmodelled shared-bath dynamics.

Use fixed padded potential locations rather than counting only operations executed on a fault-dependent branch. The mathematical unrolling specified in the governing gadget note has **L_EC=751** potential gate/readout/idle locations: four flagged blocks (424), four conditional fresh-check blocks (292), five conditional physical Pauli-correction slots with unused-qubit idles (35). Disabled slots are zero-duration exact bypasses, not hidden physical waiting periods, preserving the original protocol. Actual reached branches have at most 737 counted locations. Receiver/native stage locations add to L_EC. Conditional operations are selected by trusted classical outcomes; the declared noise event envelope must obey the pair bound on these fixed potential slots. Inactive slots have no event. Initial preparation/encoding and actual final readout are outside the cycles.

## Good patterns and proof

Call a fault pattern good if:
- each cycle has at most one fault; and
- no two consecutive cycles both contain a fault.

Starting from an ideal encoded unknown state, a fault-free cycle outputs that encoded state. A single-fault cycle starting clean produces an element of the common correctable error span tensored with its environment. The next cycle is fault-free, so the no-fault correction property restores the exact encoded logical state, decoupled from any error syndrome/environment. The declared ideal receiver must preserve that correctable span as specified above. Therefore induction across isolated faulty cycles shows that every good pattern has the identity logical channel after an ideal final decoder. A last-cycle residual is removed only by that declared ideal final decoder; it is not silently physically reset.

The same argument applies to coherent local Kraus faults inside each fixed pattern: the check's common correctable-span condition supplies a single recovery and prevents error-syndrome amplitudes from carrying logical information.

## Bound

For T cycles, each padded to L locations, the bad-pattern event is contained in the union of

    T * binomial(L,2) pairs in a single cycle
    + (T-1) * L² pairs in adjacent cycles.

Thus

    P_bad ≤ min{1, [T L(L-1)/2 + (T-1)L²] p²}.

Because each good-pattern logical channel is identity and each pattern is CPTP, half the diamond distance of the mixture from identity is at most P_bad. For variable budgets, replace the coefficient by sum_t binomial(L_t,2) + sum_t L_t L_(t+1). For heterogeneous pair-event envelopes q_ij, sum q_ij over these same neighboring pairs.

This is a finite-time O(T L² p²) storage statement under the stated classical fault-pattern model, not an iid decoded-round composition. It explicitly permits an isolated physical syndrome residual and charges its interaction with a neighboring fault. Its loose constant is not a useful threshold estimate, and it is not a hardware performance claim. Encoding/injection, terminal real decoding/readout, block-crossing fault support, calibration drift, leakage, and controller failures need separate interfaces. A general coherent gate-difference expansion requires an additional cluster/rectangle argument; this probability proof does not provide one.
