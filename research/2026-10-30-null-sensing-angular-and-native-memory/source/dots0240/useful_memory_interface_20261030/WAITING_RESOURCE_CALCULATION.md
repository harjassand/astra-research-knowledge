# What exponential waiting protection buys for an encoded Bell switch
2026-10-30. Exact elementary resource comparison; the encoded sources and endpoint assumptions are those of ENCODED_BELL_SWITCH.md.

## Workload and equal-access sources
Two independent heralded sources offer the two required encoded Bell links. In each fixed-duration round each source succeeds with probability p. A successful source supplies the exact encoded-link initialization required by the memory theorem, with the allowed fixed ancillary state. This is an explicit source interface, not a claim to have constructed such a source. Arrival times are independent of storage faults.

The no-buffer competitor has the same sources, matching gates, measurements, herald records, perfect classical storage, and postprocessing. It cannot keep an unsuccessful round's quantum link coherent into the next round; a source that secretly holds its emitted link is itself a quantum buffer and must be charged as such.

## Exact completion-time comparison
Without a quantum buffer, both sources must succeed in the same round. Completion time is geometric with

    E T_no-buffer = 1/p^2.

With a quantum buffer, retain the first successful link and stop requesting that source. Let T_1,T_2 be independent geometric(p) waiting times, counting rounds from one. Completion time is max(T_1,T_2). The minimum is geometric(2p-p^2), hence

    E T_buffer = 2/p - 1/(2p-p^2)
               = (3-2p)/(p(2-p)).                    (1)

The factor improvement is

    E T_no-buffer / E T_buffer
      = (2-p)/(p(3-2p)) ~ 2/(3p).

The first link's extra waiting time is D=|T_1-T_2|, with

    E D = E max - E min
        = 2(1-p)/(p(2-p)) <= 1/p.                   (2)

After both links are present, the reviewed encoded Bell switch consumes A,B and creates the encoded remote R,S link, up to its classical Pauli frame.

## Coupling to the certified memory lifetime
Suppose the initialized stored-link channel has error budget <=C N^a(1+t)exp(-cN), with fixed round duration absorbed into C. Uniformity in the logical input and independent arrivals allow averaging this deterministic-time bound over D; no conditioning on a rare storage-fault record occurs. Equations (1)-(2) give

    E storage error <= C N^a(1+1/p)exp(-cN).

Take p_N=exp(-alpha N), with 0<alpha<c. The buffering protocol then has mean completion time O(exp(alpha N)), retains exponentially small storage error O(N^a exp[-(c-alpha)N]), and replaces the no-buffer mean time exp(2alpha N) by exp(alpha N), up to constants. The finite controlled switching error and any subsequent remote/classical-latency storage are added separately.

This is a concrete exponential synchronization gain for exponentially rare quantum-link sources, NOT an exponential speedup in a computational problem and NOT a better source-generation rate. It arises from quantum buffering, not from a new teleportation identity. It has no immediate experimental scale claim: p_N and the certified constants are asymptotic parameters.

## Strong quantum alternative
An ordinary scheduled fault-tolerant quantum memory with the same lifetime, source access, and endpoint operation achieves exactly (1)-(2) and the same exponential waiting benefit. Thus this calculation explains *why the memory is useful* without pretending the benefit uniquely belongs to autonomous control. The architectural question is whether long coherent waiting can be supplied under the reviewed unscheduled noisy-controller resources, at usable constants and wiring costs.
