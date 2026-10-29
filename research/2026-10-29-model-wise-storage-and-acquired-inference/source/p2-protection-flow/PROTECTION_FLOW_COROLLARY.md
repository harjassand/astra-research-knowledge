# Exact protection forces a replenishment and retirement interface

Author: `/root`, 29 October 2026. Synthesis of the protection-preserving reencoding, encoder-rigidity and purification-flow results. Independent review is separate. This is an exact protected-storage principle, not a device threshold or historical-priority claim.

## 1. Operational statement

Consider a coherent logical register of dimension `K=d^(n-2)>1`, stored in `n>=3` nodes of dimension `d>=2`. Allow arbitrary recovery, measurement-free correction, classical feed-forward, reencoding, and preparation or disposal of mixed gauge systems. At every completed checkpoint the **actual available classical history** `C` and the `n` nodes must permit exact logical recovery after erasure of **any one** node. Decoders have only the surviving nodes and that history. External quantum shares or a returned erased node are additional interfaces.

The cq checkpoint instrument from the full logical input is

`E(rho)=sum_c |c><c| tensor E_c(rho)`,

with completely positive trace-nonincreasing branches. For every erased site `i` there are CPTP decoders satisfying

`sum_c D_(i,c) Tr_i E_c = id_L`.                                      (1)

A known history-dependent logical unitary can be absorbed into the specified decoder. General logical measurement, reset or a change of logical dimension is a different checkpoint contract.

Then every nonzero branch has the form

`E_c(rho)=p_c V_c rho V_c^dagger`,                                    (2)

where `p_c` is input independent and `V_c` is an exactly single-erasure-correctable isometry. Purity of the protected checkpoint is thus a consequence, even though it was not assumed of the implementation.

Let `E_1,...,E_N` be `N` fresh completely lost nodes, taken after such checkpoints and never accessed again. Let `M_0` contain **all initial mixed resources**, including initial classical apparatus and any supplied finite mixed input bank; `P_0` purifies this entire input. The initial state factors as `rho_(RL) tensor sigma_(M_0 P_0)`, including the logical reference. Subsequent external ancillary inputs are pure. Internally generated mixed gauges are permitted, with their purifications retained in the completed dilation. Unused input-bank ports are counted at the final output as well. Then

`rho_(P_0 E_1 ... E_N) = rho_(P_0) tensor (I_d/d)^(tensor N)`.          (3)

At a final completed checkpoint let `M_N` contain all returning quantum memory and remaining supply ports, and `F` all other genuine retirement, including the purifiers that make `C` an actual record. There is no additional inaccessible input purifier outside `P_0,M_N,F`. **For the retirement bounds, actual record has the complete-interface meaning of the flow theorem:** after the mathematical logical decoding, `rho_(Q M_N C)` is block diagonal in `C`, where `Q=P_0 E_1...E_N`. Diagonality of `C` alone, or of the reduced data/record channel, is insufficient. This is a physical record-retention premise, not a conclusion from (1). Under this premise the complete dilation obeys

`S(F) >= N log_2 d - [S(M_N)-S(M_0)]`,                               (4)

`rank(rho_(M_0)) d^N <= dim(M_N) dim(F)`.                             (5)

The sharper spectral bound also holds: if `lambda` is the sorted spectrum of `rho_(M_0) tensor (I_d/d)^(tensor N)`, and `v_D(lambda)` groups successive `D=dim(M_N)` eigenvalues, then `eig(rho_F)` is majorized by `v_D(lambda)`. Entropies are in bits; no temperature, heat or reset-work claim follows.

The input-bank boundary is an accounting definition for a finite process, not a claim that every port is simultaneously stored in the active processor. Pure inputs can be prepared on demand. A mixed supplier conditioned on later history, with an additional inaccessible purifier outside this boundary, is a different open interface and is not covered by the displayed sharp spectrum. Its supply and purifier must first be included in an extended theorem; charging a name alone is insufficient.

## 2. Actual records imply normalized branch channels

Apply (1) to half of a maximally entangled state. The decoded positive branch Choi matrices sum to the rank-one Bell projector. Each is therefore a nonnegative multiple `p_(i,c)` of that projector. Since erasure and decoder are trace preserving, `Tr E_c(rho)=p_(i,c) Tr rho` for every input. This trace is independent of `i`, so `p_(i,c)=p_c`. Every positive-probability normalized branch `E_c/p_c` is a CPTP encoder with all the exact erasure decoders.

Its rigidity slack is `Delta=(n-2)log d-log K=0`. The encoder-rigidity theorem forces zero normalized Choi entropy. A CPTP map with pure Choi state is an isometry, proving (2). In particular the record cannot carry logical information at this exactly reversible checkpoint. It may still carry noise, syndrome and apparatus information.

This proves the channel property of the branch rather than postulating it for an arbitrary postselection. No division by a rare-event probability is used in an approximate estimate: this argument is exact.

## 3. Adaptive histories and the lost-node spectrum

Use a maximally entangled logical reference `R`. Conditional on actual history `c`, (2) makes `R` and the stored code jointly pure. A pure marginal factors from every extension, hence from all old apparatus, including `P_0`, previous lost nodes and record purifiers, in that history branch.

Every node of a Singleton-saturating single-erasure isometric code has marginal `I_d/d`. Immediately before the next complete loss, that node therefore has this marginal independently of the old inaccessible systems, in every history branch. Averaging over history leaves the same tensor factor `I_d/d`. Later operations cannot change the joint marginal of systems never accessed again. Induction proves (3), even for adaptive code and erased-node choices.

The erased-node choice is a classical control identifying a fixed `d`-dimensional output port in each branch. A coherent superposition of loss ports, partial amplitude damping, returning loss or correlated nonlocal noise is a different physical operation; use its actual joint inaccessible state instead.

## 4. Apparatus closure and the separate quantum connection

At the final checkpoint a mathematical record-controlled inverse of `V_c` factors off the common logical Bell state. This is a proof transformation. It grants no free physical decoder or control delivery.

Apply the reviewed purification-flow theorem to `Q=P_0 E_1 ... E_N`, returning memory `M_N`, actual record `C`, and genuine retirement `F`. By (3), `S(Q)=S(M_0)+N log d` and `rank(Q)=rank(M_0)d^N`. The flow theorem gives (4), (5) and the spectral statement. Physical purification of the actual record is included in `F`; classical label storage cannot silently make those distinctions reversible.

A distinct necessary **replacement-cut** condition also follows from the reviewed reencoding theorem. If the attainable Schmidt number across a defined replacement/helper cut is at most `M`, the source half-diamond error from an exactly protected saturated target is at least `max(0,1-M/d)`. Exact restoration requires `M>=d`. Initially shared entanglement, quantum messages, returning entangled carriers and a direct entangling interaction must be classified at their actual ports. A direct interaction is a legitimate alternative to pair delivery.

This per-cut statement is not automatically an additive native-contact count or a rate of `N log d` qubits. A shared spare pool or bus can cross several cuts in one process; count its actual interactions and entanglement. Entropy retirement in (4) and the quantum connection at a cut are distinct resources.

## 5. Consequence and boundaries

At maximum exact protection density, arbitrary reencoding and hidden mixed gauges cannot remove a replacement node from the protected operation. Repeated complete losses also create a fixed independent purification load. Bounded returning quantum memory can defer that load but cannot absorb it indefinitely. The conclusion selects no syndrome circuit and does not require explicit measurement.

Below maximum packing, a product spare may rotate into later helper access; distributed local mixed gauges can attain the permitted encoder entropy. Those constructions remain in the sibling packages. General approximate future protection is still outside this result. Approximating an exactly protected target does not prove the same law for every approximately correctable code.

This gives architecture screening before optimizing a recovery schedule: identify whether an economy uses extra protection space, a counted quantum connection, returning quantum memory, or a retirement stream. It establishes no universal advantage over optimized recovery, direct coupling or reset-assisted designs. Those are valid realizations with their own acquisition, fault and service costs.

## Dependencies

* `repair/PROTECTION_PRESERVING_REENCODING.md`: protection/cut witness and the restricted repeated-isometry result.
* `algebra/singleton_rigidity/CHANNEL_ENCODER_RIGIDITY.md`: exact CPTP rigidity from conditional total correlation.
* `flow/PURIFICATION_FLOW.md`: actual-record spectral theorem with corrected complex physical supports.
* `SOURCE_SCOPE.md`: governing Astra corrections and primary ancestry. Singleton bounds, common-decoder pure-component reductions and entropy exchange are established; this corollary makes their compatible repeated-operation interface explicit.
