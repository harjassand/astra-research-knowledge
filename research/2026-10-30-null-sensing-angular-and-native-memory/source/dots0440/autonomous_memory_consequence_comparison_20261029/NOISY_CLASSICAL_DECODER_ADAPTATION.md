# Constructive ordinary alternative: noisy fixed-depth classical decoding
2026-10-30. Root derivation candidate, not independently reviewed or a novelty claim.

## Source and intended comparison
Bharti–Haug–Khu–Tanggara 2610.03684v1, Sections 2.1–3.3, assumes reliable classical processing and fixed-time bounded-degree parallel Tanner decoding. Its partial decoder contracts residual reduced weight after a fixed number of iterations; physical Pauli correction is an allowed alternative to a persistent frame. Primary source: https://arxiv.org/html/2610.03684 . Their published theorem is not silently changed here. The following is a proposed constructive extension under an explicit bounded-depth implementation.

## Classical fault-light-cone lemma
Implement D fixed classical decoder layers by local basis-measure / Boolean-compute / basis-reprepare CPTP gates. Each gate has bounded fan-in, fan-out f and support, and all output correction bits are used for physical local Pauli corrections. Prepare fresh finite classical work registers each cycle; do not rely on a persistent globally fanned-out frame register. A fixed local truth table may be expensive but is independent of N.

For a set F_cl of faulty classical locations, let L(F_cl) be their output forward light cone, including faults in the final controlled-Pauli stage. Then |L(F_cl)|<=c_D|F_cl|, with c_D independent of N. Fix the decoder's actual input syndrome record y. Outside L(F_cl), the complete circuit is the prescribed deterministic circuit and produces exactly the ideal correction c(y). Inside the cone allow arbitrary CPTP errors and a retained shared bath.

Even if a fault leaves a nominally classical register coherent, the correction operation is a linear combination of Pauli byproducts whose difference from c(y) is supported within L(F_cl). Nominal basis-measure gates remove coherence where encountered; no assumption that every faulty gate is classical is required. Thus the noisy classical layer adds a bounded-support common error span, not an unbounded decoder failure. Mathematical instrument records can be used to analyze y; no extra reliable physical record is supplied.

## Recovery recurrence
Combine with the actual quantum extraction/readout support bound and the deterministic Tanner partial-decoder contraction. For a cycle with f total faulty quantum/classical locations, every Pauli term on the same observed input record satisfies

    r_out <= alpha r_in+C f,   alpha<1,

after adjusting constants for the fixed classical forward cone. The actual correction may differ between terms only on that bounded cone, which is paid as residual DATA support. This requires the usual common-record argument; it is not a Pauli-mixture assumption.

Choose a linear safe radius r_*N and a fault fraction f<=gamma N with C gamma<(1-alpha)r_*. A low-fault cycle preserves the radius. With O(N) locations per cycle and a local-stochastic fault-path law, the probability of exceeding gamma N in any one cycle is exp(-Omega(N)); a union bound handles S cycles. The common correctable-span argument then supplies the same form of encoded logical diamond bound and O(SN) quantum/classical operation count, with changed thresholds and constants.

## Required implementation assumptions and limits
- The actual chosen parallel Tanner decoder must compile to fixed depth, bounded fan-in/out and bounded communication latency. Merely calling an algorithm parallel is insufficient.
- Physical corrections and fresh records avoid unbounded fanout from a long-lived Pauli frame. Reliable preparation, storage and timing are not being granted to the classical gates themselves.
- An external synchronous schedule still specifies the gate locations. The location-set noise law remains classical local stochastic, though fault maps may be quantum and share a bath. Weak coherent errors at every location are not automatically such a random fault set.
- Long-range Tanner connectivity and fixed per-layer communication remain resources, exactly as in the source comparator.
- Initialization and final ideal recovery are still encoded interfaces unless separately constructed.

If these local circuit hypotheses are verified, noise-free classical processing is not the decisive separator from our autonomous memory theorem. The harder difference is time-independent internal timing/control under sustained continuous local noise. This adaptation should be included as a strong ordinary alternative rather than advertising a separation from an unnecessarily weak baseline.
