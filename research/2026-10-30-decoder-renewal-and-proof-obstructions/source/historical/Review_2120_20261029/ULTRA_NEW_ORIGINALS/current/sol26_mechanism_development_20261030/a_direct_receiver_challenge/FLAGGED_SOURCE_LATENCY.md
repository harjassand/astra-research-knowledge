# Exact minimax source latency for an opaque, perfectly correctable family

This is an all-size native source theorem and a strong matched ordinary comparator for streamed recovery. It is not a numerical channel fixture, a lower bound for all low-rank sources, or a counterexample to the direct-sign recovery guarantee. It separates small LIVE quantum workspace from source-call latency and shows why an arbitrary mixed junk rank cannot disappear from every acquisition bill.

## 1. Literal source and access

For any integer `r>=2` and unknown string `s in {0,1}^r`, define the fixed memoryless channel

`N_s(rho)=(1/r) sum_(j=1)^r |j><j|_J tensor Z^(s_j) rho Z^(s_j)`.       (1)

Its input dimension is `k=2` and output dimension `D=2r`. The output register decomposition and computational flag basis are known. The bits are not supplied. Each forward call has a fresh uniform classical flag independent of the input and every other call. No controlled source, inverse source, conditional flag oracle, or chosen-flag preparation is granted. An algorithm may use arbitrary entangled inputs, keep quantum programmes, interleave queries and operations on its payload, and make adaptive measurements. Its reference half is inaccessible.

Each source is EXACTLY correctable by reading the flag and applying `Z^(s_j)`. Its actual mean is `I_(2r)/(2r)`. Its normalized Choi state and partial transpose are

`J_s=(1/r) sum_j |j><j| tensor |Phi_(s_j)><Phi_(s_j)|`,

`C_s=(1/(2r)) direct_sum_j (I tensor Z^(s_j)) SWAP (I tensor Z^(s_j))`.

All eigenvalues of `|C_s|` are `1/(2r)` and `||C_s||_1=2`. Thus the exact sign decoder recovers perfectly, as does the ordinary flag-controlled correction when the string is known. There is no physical noise failure in the family; the operation which costs resources is acquiring the unknown correction.

The family can be embedded by a PUBLIC isometry into ANY ambient `D>=2r`, with zero weight on the unused subspace. Its actual mean then has exact rank `d0=2r` and zero tail beyond d0, even when d0 is tiny compared with D. The query theorem and ordinary comparator are unchanged. Thus the lower bound concerns effective occupied rank, not a requirement that the mean fill the ambient physical space.

Count `Q` ADDITIONAL forward calls besides the call which produced the encoded payload. The calls can precede the payload, follow it, or be interleaved with decoding, with at most `Q` in total. They must be counted even when their returned flags are unwanted.

## 2. The exact optimal fixed-budget error

Let `M_(s,Q)` be the logical channel induced by any one algorithm with at most `Q` such calls and arbitrary final recovery. The channel averages the native payload flag and programme histories, exactly as composition with N_s does; it is not a guarantee conditioned on an adversarially selected flag. Its worst-case entanglement infidelity obeys

`sup_s [1-Fe(M_(s,Q))] >= p_Q := (1/2)(1-1/r)^Q`.        (2)

The SAME lower bound holds for worst-case half diamond distance to identity. Both bounds are attained by the ordinary procedure in Section 3, for EVERY string simultaneously. Hence these are exact minimax values, not merely asymptotic lower bounds for the polar supplier.

Proof: use a uniform independent-bit prior on `s` only as a minimax proof device. Condition on the payload flag `j` and on the sequence of flags of all additional queries. The source has an orthogonal environment record of each flag, so the entire adaptive comb can be expanded as a classical mixture of such histories. Every flag sequence has its usual product-uniform probability independent of inputs, the reference, and the string. This statement remains true for entangled inputs and quantum processing of the visible flag registers.

With probability `(1-1/r)^Q`, none of these calls addresses the payload's flag. Fix all the other bits and all those flags. Every subsequent or preceding source operation then depends only on `s_l` for `l!=j`. It is independent of `s_j`. Averaging that still-unobserved bit acts on the encoded half of a Bell pair as

`rho ->(rho+Z rho Z)/2`,

which is entanglement breaking. All algorithmic operations and all the other source calls are on the decoder side of the reference cut; they cannot restore entanglement. Measurement outcomes and adaptation are included in this trace-preserving comb, rather than being conditioned on as successful postselection. Therefore the final normalized Choi state on this branch is separable and its Bell overlap is at most `1/2`. On every other branch allow fidelity one optimistically. This proves the prior-average bound in (2), hence its worst-case bound.

Algorithms using fewer calls can be padded with discarded calls, preserving a fixed budget for the argument. There is no assumption that a call simply measures a bit; that simple strategy is only used for achievability. In particular feeding a payload-dependent state back into the source does not evade the bound: without a flag-`j` call, the rest of the comb remains independent of `s_j`, so it acts on an entanglement-breaking average input.

For any logical channel, measurement of the Bell projector gives

`halfdiamond(M,id)>=1-Fe(M)`.

This transfers (2) to the reference-aware metric.

## 3. Equally informed ordinary procedure achieves the bound

For each query prepare the known state `|+>`. Read its output flag and measure its output qubit in the X basis. The outcome is EXACTLY `(-1)^(s_j)`. This acquires an ordinary classical dictionary for the encountered labels; it consumes the same opaque forward calls.

On the encoded payload read its flag nondestructively. If that bit has been acquired, apply its correcting `Z`. Otherwise apply an independent fair random choice of `I` or `Z`. The averaged logical channel for EVERY fixed string is

`M_(s,Q)=(1-p_Q)id+p_Q Ad_Z`.

Consequently its entanglement infidelity and its half diamond error are BOTH exactly `p_Q`. The construction attains the quantum lower bound without an entangled query, coherent source call, channel reconstruction, partial-transpose simulation, or a protected quantum programme. It is a legitimate stronger ordinary comparator on this supplied family, not an incumbent for an arbitrary unknown frame.

For `0<epsilon<1/2`, fixed-budget error at most epsilon is possible iff

`Q>=ceil[ log(1/(2epsilon)) / -log(1-1/r) ]`.             (3)

In particular `Q>=(r-1)log(1/(2epsilon))`. Thus even exactly correctable sources can require a linear-in-r source bill at constant precision.

## 4. Streaming, offline service, and actual resources

For one ONLINE payload, first read its flag `j`. Query `|+>` repeatedly until flag `j` appears, discard other outputs immediately, measure X, and correct. This gives exact recovery almost surely with expected `r` additional calls. The source call count is geometric, not capped. A cap `Q` followed by random guessing gives precisely Section 3's finite channel. At fixed positive query latency `ell`, the expected payload retention time of this serial perfect protocol includes `r ell`.

This expected count is also necessary for perfect recovery uniformly over strings, if there is no earlier dictionary. A zero-error algorithm must encounter the target label almost surely: otherwise its averaged no-hit branch would be entanglement breaking. The expected number of hits by any finite-mean adaptive stopping time is `E Q/r`; at least one hit is necessary, so `E Q>=r`. This is the elementary stopped iid-indicator identity, valid by Tonelli and the predictable decision to make the next query.

Live protected storage can be only the physical payload, one returned query at a time, and `O(log r)` control qubits. This does not remove the paid source latency. If `B` simultaneous source ports are available, parallelism trades elapsed time for that separately supplied throughput and programme/workspace; it is not free in the bound on total calls.

For arbitrary future payloads, a stronger OFFLINE ordinary alternative is available on this family. Query until all labels have appeared. The expected count is the coupon-collector value `r H_r`. Store the acquired `r` bits plus label-presence bookkeeping classically. Thereafter every payload is recovered exactly with no more source calls and no protected quantum programme. A single logical table lookup and conditional Z suffice. This unlimited reuse is a property of the explicit classically parametrized family, not something transferred to arbitrary opaque channels or unknown output frames.

All these claims use the ideal native fixed-channel/control contract. Physical preparation/readout/calibration errors and fault-tolerant logical controls are separate resources; no device or source sampling was executed here.

## 5. Consequence for the universal direct receiver

The joint-sign decoder and the source-specific second-moment simulation are still valid. Their meaningful advantage is an acquired universal processor under its stated actual-mean-tail promise, with a small online live workspace. They do not imply rank-independent acquisition or negligible coherence time.

Here the actual mean is flat on its occupied support. Its tail after rank `d0<=2r` is `(2r-d0)/(2r)` and its nonzero Choi polar eigenvalues are `1/(2r)`, whether or not the source is padded into a larger ambient carrier. To make that tail small requires `d0=Theta(r)`. The linear source lower bound therefore supports, rather than contradicts, the universal theorem's effective-rank dependence, and still applies to exact low-rank means in an arbitrarily larger ambient space. The ordinary dictionary is better than a generic quadratic-copy simulation of this polar Hamiltonian on this family. No comparison to a loose general upper bound is called a speedup or a lower bound on all universal algorithms.

The exact all-r minimax result is an access/latency theorem for recovering ONE already singly encoded payload in this native family. It is not a channel-capacity statement, a lower bound for a different multi-use encoder, a generic recovery hardness claim, or a claim that the fresh-programme architecture lacks value in an unknown high-dimensional quantum frame. Historical priority of this worked comparator is UNKNOWN.
