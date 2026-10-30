# Candidate efficient mathematical readout via appended noiseless SSF scans

2026-10-29. Constructive extension of the conditional spacetime proof, not yet independently audited. It replaces expensive final minimum-syndrome optimization by a polynomial-time ideal SSF decoder. It does NOT solve noisy physical readout or give its wall-clock resource accounting.

## 1. Fixed deterministic decoder

After the memory interval and the required forest-frame conversion, perform the mathematical decoding channel:

1. Measure the complete stabilizer syndrome ideally.
2. Run a fixed-order scan of every SSF hub in both CSS sectors, updating the classical syndrome after every accepted correction. Each accepted correction strictly lowers total syndrome weight. Repeat complete scans until a scan makes no change.
3. Apply the computed Pauli correction and decode the stabilizer code. If the final syndrome is nonzero, declare decoding failure (or output any fixed logical state for the channel definition).

Let n_chk be the number of stabilizer checks used in the syndrome-weight potential. Noiseless correct SSF updates can make at most n_chk accepted moves, since each lowers that integer potential by at least one. Every productive complete scan includes at least one move. Thus n_chk+1 full scans suffice for every input syndrome, including failed ones. Pad the algorithm to this fixed number of scans. The naive classical work is O(N n_chk)=O(N^2) under bounded-degree/check geometry; faster implementations are not needed for this claim.

The initial full syndrome snapshot makes every subsequent simulated local syndrome test deterministic within its measured sector. Appending those ideal SSF evaluations therefore introduces no further syndrome dephasing within that sector, even with a retained entangled bath.

The mathematical channel needs only ONE ideal syndrome snapshot: all subsequent syndrome evaluations and updates are classical, and only the final accumulated Pauli mask is applied to the data. With bounded check weight, the snapshot uses O(N) bounded-arity check-measurement gadgets; a bounded-conflict coloring permits constant ideal depth on the interaction graph, assuming the requisite noiseless controls/ancillas. The final Pauli mask uses at most N single-qubit Pauli operations. These are ideal operation counts, not a physical noise analysis.

A complete scan is a deterministic D1 service window with no missed opportunity: each hub is evaluated, and an initially good packed candidate either is resolved earlier or is resolved when its own hub is evaluated. There are no bad events during this ideal decoder. Bounded conflict coloring can also implement a scan in constant-depth ideal local layers, but the present argument claims only an efficient mathematical decoder.

## 2. Append these scans only to the proof history

Group the scans into blocks of R windows, with final padding. There are

    J=ceil((n_chk+1)/R)

additional ideal blocks, each with Q=0 and M=0. They need not be physical noise-free storage periods: they define the mathematical readout map being analyzed. The original noisy memory evolution is unchanged.

For each Pauli-expanded branch, apply exactly the same virtual sectorwise representative bookkeeping and first-cutoff-bad-block test to the combined memory-plus-decoder history. D0 and D1 are deterministic and therefore apply to these extra blocks. No minimum-syndrome representative is computed by the decoding algorithm; it remains an analysis-only gauge.

If no cutoff-bad component occurs anywhere, every final canonical sector representative is stabilizer-equivalent to the actual error. A final nonzero syndrome would, by the good-component FGL progress premise, have a beneficial SSF candidate in some small component. Its full hub would therefore have made a correction in the final no-change scan, a contradiction. Thus the terminal syndrome is zero. Its sectorwise minimum representative is the empty set, so the actual final error is a stabilizer. Logical decoding succeeds.

Consequently any logical failure or stuck nonzero syndrome of this efficient decoder implies a first cutoff-bad component in the extended history.

## 3. The certificate must end in the real noisy interval

Run the same backward chain from that first bad component. A terminal fresh-density event cannot occur in an appended noiseless scan block, because Q=M=0 there. The chain therefore continues backward until it reaches a genuine fresh event in the original noisy memory interval. Exact initial encoding again excludes nontermination at time zero.

All connectivity and terminal-volume estimates are unchanged. Rooting at any of L+J block layers and applying the existing positive terminal-record bound gives, in the two-sector CSS case,

    ||E_efficient-dec-id_L||_diamond
       <=2 min{1, 2(L+J) R N r^ℓ/(1-r)}.               (1)

The extra O(N) blocks cost only a polynomial prefactor, preserving the exponential-in-sqrt(N) scale. This avoids an invariant quantum residual law and avoids taking the union of coherent branch supports.

For a root in an appended block, terminal certificates whose earliest layer is also appended have zero probability and are omitted. The remaining fixed terminal sets lie in the true physical noise record and obey the same unconditional moment bound. Padding cannot introduce new accepted moves after a genuinely no-change scan because the syndrome then remains unchanged.

## 4. Important qualifications

* This relies on the deterministic good-component progress premise used in D1: nonzero syndrome of the canonical reduced residual has a good SSF candidate. That premise and the original D0/D1 contracts remain subject to their independent audit.
* The algorithm's global complete-syndrome measurement is a real component of the proposed *mathematical decoding channel*, not a dephasing silently inserted into the memory evolution. It can only be invoked as a terminal readout operation.
* Its correction path is exactly the syndrome-determined SSF path, so all coherent Pauli branches with the same measured syndrome receive the same correction. No inaccessible branch label is used by the decoder.
* The final global code-basis decoding can be synthesized from the stabilizer description in polynomial time, but implementing its gates reliably is a separate physical task.
* Nothing here grants a noise-free O(N)-time physical readout. The frame conversion, syndrome measurements, classical computation latency, continued storage noise, reliable classical computation, and output circuit must be charged in an operational implementation. The actual autonomous process continues during O(poly(N)) classical computation; it cannot be frozen at the syndrome snapshot for free. Destructive classical logical readout might use a different strategy by measuring data first, but general quantum retrieval is a separate unsolved operational task here. The claim is polynomial-time *ideal mathematical recovery* with a proven conditional logical-error bound, not an efficient noisy end-to-end machine.

## 5. Stronger root-block variant: no O(N) counting penalty is necessary

The preceding padded-block proof is valid but wasteful. D0 is an unconditional finite-work bound for ANY finite serial interval; its constant does not grow with the number of noiseless evaluations. Treat the entire terminal SSF computation as ONE final D0-only root block. If its enlarged components are all below ℓ, the final no-change scan has zero syndrome by the good-component progress premise, and the actual output differs from the empty minimum representative by a stabilizer. Hence a decoder failure supplies a cutoff-bad connected component in this single final suffix.

If any memory block was already cutoff-bad, use its usual first bad root. Otherwise all previous memory blocks are good, and the terminal suffix root satisfies

    |K|<=C_seed |R_previous intersect K|

because Q=0 in the suffix. Choose the incoming target there and apply D1 only in the earlier genuine memory blocks. The backward chain, geometric growth and terminal-volume estimate remain unchanged. There is no fresh obstruction in the final suffix. Thus (1) can be sharpened to

    ||E_efficient-dec-id_L||_diamond
       <=2 min{1, 2(L+1) R N r^ℓ/(1-r)}.               (2)

No D1 service window or temporal length is assigned to the long offline computation. This root-only use of D0 will also permit a finite noisy readout tail followed by noiseless classical SSF simulation, without pretending that a noise-only tail had good SSF service.
