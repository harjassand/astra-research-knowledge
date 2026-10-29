# Private terminal Bell resource: remove long unknown-payload holding
2026-10-28. Conventional teleportation consumer of the compact prequential construction; candidate pending review. No multi-payload or frozen future-source service claim.

Use exactly the same private terminal T and all-probe learning as CONSTRUCTION_v1. Every call, including T, supplies half of n fresh trusted Bell pairs to the SAME complete source port. At t<T measure the returned data and retained halves in Bell basis, then the random flag Pauli, obtaining the sparse gradient. At T do NOT perform either probe measurement. Instead apply the already fixed flag/Pauli receiver to the returned data, retaining the n reference halves and decoded data. Isolate both sides from all future source interaction. Role-dependent local operations occur only after that complete source call, with no feedback or leaked private T. The source input preparation is now identical at every call, not merely the same averaged input.

The terminal resource, after averaging actual histories, private time and decoder randomization and tracing inaccessible source memory, is

 omega=(1/N) sum_t sum_h p_t(h) (id_R tensor R_(M_th) E_th)(Phi_n).

Its Bell overlap obeys
 1-Tr(Phi_n omega) <= min_fixed M (1/N)sum_t E_h[1-f_th(M)] +(9/8)r^2/sqrt N + nu.

This identity is the ordinary Choi identity and all-probe prefix equality; it needs no continuity bound depending on 2^n. Inter-call memory may be arbitrary and the terminal resource may remain correlated with inaccessible source memory, but its ISOLATED reduced state is sufficient for this one subsequent local consumer. No claim is made about the joint source/resource process conditioned on all hidden or retained keys.

Only after resource isolation accept a fresh arbitrary n-qubit payload, with external reference, initially independent of the resource-generation process and source memory. Standard n-qubit teleportation consumes the resource: Bell-measure payload with the retained reference halves, transmit the 2n classical outcome bits to the decoded-data side, and apply the matched local Pauli correction. Averaging and retiring those outcome records, standard teleportation with omega implements exactly the Pauli channel with probabilities
 q_x=Tr(Phi_x omega).

The arbitrary Bell off-diagonals of omega vanish under the uniform teleportation correction sum; q_0=Tr(Phi_n omega). Therefore
 (1/2)||Teleport_omega-id||diamond =1-q_0,

with equality witnessed by a maximally entangled input and upper bound from the Pauli mixture. The entire previous Bell-loss bound is thus a dimension-independent reference-complete error bound for the one teleportation service. The bound is averaged over resource generation, not a guarantee on every individually heralded resource, terminal time or transcript. A later source call is not used, so no frozen-noise extrapolation occurs.

Resources: worst-case N source calls (mean (N+1)/2), each with n prepared Bell pairs and n protected reference halves through that call; all prior probe Bell readouts and flag measurements; polynomial-cap classical online learning; terminal flag POVM and conditional correction; at most n stored local Bell halves plus n decoded-data qubits while accepting the payload; an additional n Bell measurements, 2n forward classical bits and n Pauli corrections for teleportation. There is no unknown payload held for the entire acquisition horizon. Instead the isolated resource must be held from its preparation until payload arrival/consumption, and its idle/control errors are paid. If physical geometry requires separation, routing and classical latency are paid. No repeatable resource bank or entanglement generation rate is established.

An adversary able to interact again with the isolated resource, access the private receiver/terminal records before the complete boundary, or start correlated with the fresh payload falls outside the stated interface. Retiring keys means not later making them available to the untrusted source; it does not erase the classical communication cost. One total implementation discrepancy nu compares the entire implemented generation-plus-teleportation process with the declared ideal-interface process, without silently transferring its occupation comparator to changed imperfect histories.
