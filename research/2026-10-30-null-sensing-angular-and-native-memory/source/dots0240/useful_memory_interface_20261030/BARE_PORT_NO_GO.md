# Fixed-size bare quantum ports have a finite-rate error floor
2026-10-30. Ordinary proof, not a novelty claim. This rules out an entire tempting class of loading/retrieval bridges without assuming a fictitious final ideal gate.

## Statement and model
Let Q be a fixed d-dimensional physical input/output port. The rest of the apparatus may be arbitrarily large and may contain the reviewed autonomous memory. Split its controlled generator near the port as

    L(t)=L_notQ(t)+K_Q(t)+gamma (D_Q-id),
    D_Q(rho)=I_Q/d tensor Tr_Q rho.

L_notQ is arbitrary well-defined CPTP dynamics that does not act on Q. K_Q comprises all intended terms acting on Q, with ||K_Q(t)||_diamond <= g independent of the memory block size N. This is the finite-rate, bounded-incidence port assumption; a Hamiltonian port coupling H contributes at most 2||H||. The depolarizing kicks form an independent exogenous Poisson process of rate gamma>0. They are an explicitly allowed one-site CPTP noise process. The non-kick base evolution L_notQ+K_Q must itself be CPTP, as it is for an independently added exogenous kick process. Adaptive controls are included in the joint controller state. Condition only on the exogenous port-kick record, never on a postselected internal instrument. Other allowed noise can be included in the CPTP rest dynamics and is not required to be globally absent.

Put a=1-1/d^2. Choose a fixed delta>0 with g delta<=a/2. The loading/retrieval operation must last at least delta. No postselection conditioning is included: a declared failure is part of the overall channel.

## Retrieval: last-event proof
Take a reference R maximally entangled with the desired logical output. In the final interval [T-delta,T], the event that at least one Q-depolarization occurs has probability

    q=1-exp(-gamma delta).

Condition on the last such event at time s and all preceding state preparation. Immediately after this event Q is maximally mixed and product with everything else. Compare the actual evolution from s to T with the evolution in which K_Q is suppressed. Duhamel's formula and CPTP trace-norm contraction give a joint trace-distance bound <=g(T-s)<=g delta. This estimate is independent of the size, complexity, or correlations of the rest of the apparatus. In the comparison evolution Q stays maximally mixed and uncorrelated with R, so its overlap with the target maximally entangled state is 1/d^2. The actual overlap is at most 1/d^2+g delta (a deliberately conservative observable bound).

The no-event branch has overlap at most one. Consequently every bare-output retrieval channel obeys

    1-F_ent >= q(a-g delta) >= q a/2,
    ||Retrieval-id_d||_diamond >= 2q(a-g delta) >= q a.  (1)

The ideal target can equally be a specified unitary, absorbed into the Bell test. There is no assumption that information sat on the port for the whole interval. The bounded-rate argument applies even if the protocol tries to reconstruct it immediately after the final kick.

## Loading: first-event proof
Initially the unknown source occupies Q and is maximally entangled with R, while the entire apparatus state is fixed independently of it. Condition on the first Q-depolarization at s<=delta. Compare the pre-event evolution with K_Q suppressed. Their joint distance is <=g delta. In the comparison, Q,R are still maximally entangled and independent of the apparatus until the event; D_Q then makes R maximally mixed and independent of the entire accessible apparatus. Subsequent encoding, memory, and arbitrary decoding cannot recreate its correlations with R. CPTP contraction gives the same upper bound 1/d^2+g delta for final entanglement fidelity on this event, and the same floor (1).

Thus deterministic loading of a fresh unknown unencoded qubit cannot become exponentially accurate merely by choosing a larger destination memory. A constant injection error can be acceptable for some workloads, but it must be accounted for separately from an exp(-cN) storage error.

## Exact escapes, not loopholes hidden in notation
- Supply an already encoded source or keep the receiver encoded; a fixed one-site depolarization no longer destroys its whole logical information.
- End with a destructive classical result and protect the classical record. This is why the earlier CSS readout is operationally useful.
- Grant a port whose noise rate shrinks with N, an unbounded-rate interaction, or a noise-free instantaneous endpoint. Those change the resources.
- We do not claim a general lower bound for postselected conditional success, a growing quantum port, or an encoded receiver equipped with its own further recovery.

The practical bridge is therefore an encoded-to-encoded transfer such as ENCODED_BELL_SWITCH.md, not a promise that an ideal mathematical decoder emits an exponentially accurate bare flying qubit. This limitation applies equally to conventional fault-tolerant memories.
