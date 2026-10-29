# Astra P2: protection, quantum connections and purification flow

29 October 2026. This tranche continues the frozen graded-record, reusable-coupler, service-rate and causal-normalization work in `p2_reuse/`. All predecessor proofs, actual reviews and source gaps retain their scope. No equipment operation, external outreach or new export was performed.

## What the completed construction makes possible

The main advance is an operation-level resource principle for **maintaining protection while the physical encoding may change**. It separates three obligations that a particular recovery circuit can obscure: the quantum connection needed to reincorporate a replacement, the space available for mixed gauge information or disconnected spares, and the purification that must remain in returning memory or leave through a genuine retirement interface.

The question was initially fixed-encoding local repair. That was too narrow: a conventional decoder can recover the logical state while abandoning the prescribed physical code, and a rotating spare can avoid the newest replacement. The stronger question is whether the restored information still has the declared protection against the next loss. At maximum exact single-erasure packing, the answer imposes a connection requirement independent of which encoding or recovery schedule is chosen. Below that packing, explicit spare and mixed-gauge constructions show real architectural freedom.

The result is foundational rather than a claimed hardware speedup. It supplies a way to reject an invalid resource comparison before spending effort on a gate schedule, and constructive recovery/supply machinery for interfaces that remain viable. Strong conventional recovery and prepare/compress/send/expand methods are used when they are better.

## 1. Encoder entropy is part of the protection budget

Let a CPTP encoder carry a logical space of dimension `K` into `n>=3` physical nodes of dimension `d`. After loss of any one node, a fixed decoder using the remaining nodes must recover every logical input and reference exactly. If an actual record selects the decoder, the following entropy and distance formulas apply **separately to each normalized CPTP record branch**, with its Choi state `J_c`. They need not hold for the unconditioned physical mixture of different record-selected encoders. Applying the formulas to an unconditioned encoder requires common decoders without that preparation label. An external quantum share is not free side information.

For its normalized Choi state `J`, the completed theorem is

\[
S(J)+\frac{n}{n-2}\log_2K
\le \sum_{i=1}^n S(A_i)
\le n\log_2d.
\]

With packing slack `Delta=(n-2)log_2d-log_2K`, it follows that `S(J)<=n Delta/(n-2)`. At zero slack the encoder itself is an isometric channel. Arbitrarily declaring a hidden mixed gauge cannot evade this conclusion.

The proof keeps the encoder environment `E`. Exact decoding forces `R` independent of `A_i E` for every erased node. An exact identity expresses the displayed deficit as a sum of ordinary and conditional total correlations. Their nonnegativity proves the inequality without an entropy-cone optimizer or a subsystem-code classification.

The entropy coefficient is attained on explicit factorizable alphabets: append an independent maximally mixed `r`-level gauge inside every node of a supplied saturated code. Then `S(J)=n log_2r` and `Delta=(n-2)log_2r`. Four ququart nodes built from the ordinary four-qubit erasure code and three six-level nodes built from a three-qutrit code provide independently executed examples. These examples also refute a tempting unrestricted bound using `log rank J` in place of the correct entropy allowance.

There is an exact source-channel metric consequence:

\[
\min_{W\ \mathrm{isometry}}\frac12
\|\mathcal N-\operatorname{Ad}_W\|_\diamond
=1-p_{\max}(J)
\le1-2^{-n\Delta/(n-2)}.
\]

Every spectral Choi component is a full-input isometric encoder with the same exact erasure decoders. Convexity gives the upper bound; the pure-target Choi projector gives the matching lower bound. This concerns the physical data output and arbitrary logical references. A prescribed returned preparation purification can have square-root discrepancy. Exact future-erasure correctability remains a premise; packing slack is not a physical error probability.

Proof and scope: [channel encoder rigidity](algebra/singleton_rigidity/CHANNEL_ENCODER_RIGIDITY.md). Attainment: [distributed mixed gauges](reviews/mixed_encoder_challenge/DISTRIBUTED_GAUGE_SHARPNESS.md).

## 2. Reencoding cannot remove the replacement connection at saturation

At `K=d^(n-2)>1`, allow the target encoder to change, to depend on the actual record, and initially even to be mixed. The common exact-decoder condition forces every vector in its Choi support to define a correctable isometry. Every such vector has a maximally mixed replacement-node marginal. Polarization yields an operator identity on the whole support; flatness of a marginal alone would not suffice.

If the actual protocol can produce Schmidt number at most `M` across the replacement/helper cut, the protected target's support projector accepts it with probability at most `min(1,M/d)`. Therefore its source half-diamond error is at least

\[
\max(0,1-M/d).
\]

For actual cq histories, the valid lower bound weights this expression by the **actual** branch probabilities and branch resource budgets. It does not assume that ideal and actual record laws coincide. Exact restoration needs `M>=d`; in the declared fresh-ebit/quantum-message model this gives `e+q>=log_2d`. Shared entanglement, every crossing direction, returning carriers, approximate catalysts and direct interactions retain their actual resource roles. A direct entangling gate is a legitimate port, not free local processing and not necessarily pair delivery.

A separate bound handles a jointly disconnected set `S`: if the encoded Choi state is separable across all of `S` versus the reference and remaining nodes, then, for `K>1`, at least three nodes remain and

`K <= d^(n-|S|-2)`.

Joint separability matters; separate one-node statements cannot replace it. A three-qutrit code plus a spare saturates the one-disconnected-node allowance and provides a rotating-spare repair. It pays later coherent access to the old replacement. Thus the storage bound is not automatically a contact count or bitrate.

Proof, actual records, exact tests and boundary examples: [protection-preserving reencoding](repair/PROTECTION_PRESERVING_REENCODING.md).

## 3. The actual-record bridge closes the repeated-loss argument

The final synthesis starts from a cq checkpoint instrument, without assuming its postselected branches are channels. If record-controlled decoding after any node erasure sums to the identity channel, positivity of the decoded Choi branches forces each branch to be `p_c` times the identity. Consequently `p_c` is input independent and each normalized encoder branch is CPTP. At maximum packing, Section 1 then makes it isometric.

For a Bell logical test input, the conditional code/reference state is pure and factors from all old apparatus. Each completely lost node is therefore `I_d/d` independently of prior losses, even under adaptive code and erased-node choices. For `N` fresh nonreturning complete losses,

`rho_(P_0 E_1...E_N)=rho_(P_0) tensor (I_d/d)^(tensor N)`.

Here `P_0` purifies **all initial mixed resources**, including initial classical apparatus and any finite mixed supply bank. Later outside input ports are pure; internally prepared mixed gauges retain their purifiers in the dilation. Unused bank ports remain counted at the output. This is a total resource boundary, not simultaneous active-processor storage. Unmodeled history-conditioned mixed suppliers require an extended theorem.

Let `M_N` contain all returning quantum memory and remaining supplies, and `F` all genuine retirement. The retirement theorem requires the actual record to be classical jointly against the inaccessible systems and returning memory after logical decoding, not just diagonal in its own marginal. Its physical purifiers remain in `F`. Under that complete-record premise,

\[
S(F)\ge N\log_2d-[S(M_N)-S(M_0)],
\qquad
\operatorname{rank}(\rho_{M_0})d^N
\le\dim(M_N)\dim(F).
\]

Thus bounded returning memory can defer purification but cannot absorb an indefinitely growing fresh-loss load. This applies to measurement-free recovery as well as measurement-based recovery under the same completed contract. It is not a reset-energy theorem. The replacement cut and entropy flow are different resources; neither formula alone establishes a sum of native gate costs.

Proof and reviewed closure boundary: [protection-flow corollary](flow/PROTECTION_FLOW_COROLLARY.md).

The underlying [purification-flow theorem](flow/PURIFICATION_FLOW.md) is sharper: if the inaccessible-system spectrum is `lambda` and returning memory has dimension `D`, the retired spectrum is majorized by the vector obtained by grouping successive `D` eigenvalues of `lambda`. Actual record sectors give a physical pinching after a corrected controlled uncompute. This bounds entropy, rank and other Schur-concave functions. A one-qubit causal three-arrival parity construction reaches the endpoint spectrum and beats greedy retirement. The exact partition compiler has a gap from five through eight arrivals; that is a representation gap, not a proved causal impossibility.

## 4. Constructive operations and the strongest conventional comparisons

For a specified locally repairable code, the helper normal form exposes the lost node's fixed entangled partner. Exact full-code repair is equivalent, at the declared cut resource interface, to supplying the corresponding fixed pair and routing the old purification. A four-qubit example has a seven-CNOT reset-assisted repair, including six helper CNOTs; logical-only recovery can use fewer resources by abandoning the future-protection contract. The nonflat five-qubit encoding gives a concrete `(4/5,1/5)` pair spectrum while retaining exact single erasure protection; it does not inherit the original code's full distance.

For approximate interfaces, the optimized canonical conventional recovery can emit the restored data directly. The supplied full-input extractor defect `a` then gives complete error at most `a`, improving the generic two-pass `2a` construction. Remote output delivery and the physical flag embedding remain paid. No separately prepared pair is universally necessary in that realization. The older partner-swap construction remains useful when its smaller helper interface is the one actually available.

The exact fixed-resource reduction also compares the **optimized source half-diamond error**, not just fidelity. For target `(4|00>+3|11>)/5`, an allowed separable preparation has exact trace optimum `12/25`, better than the fidelity-optimal pure truncation's `3/5`. That optimum does not automatically preserve a prescribed complete record or preparation environment.

Files: [exact repair factory](repair/LOCAL_REPAIR_FACTORY.md), [general purified repair](algebra/PURIFIED_LOCAL_REPAIR.md), [connection-resource reduction](information/QUANTUM_CONNECTION_REPLENISHMENT.md).

### A causal supply compiler with explicit active memory

The [pair factory](factory/CAUSAL_PAIR_FACTORY.md) deterministically prepares a truncated binary pair block, coherently ranks allowed strings, sends the compressed index, and expands at the receiver. Conditional rotations use finite binomial masses. No rare postselection or hypothetical repeated starts are required. Independent blocks may be prepared just before their causal use; no physical global bank is assumed.

For `B` blocks with retained probability `Z`, complete comparison against any specified compatible causal consumer is at most `sqrt(1-Z^B)`. The consumer includes its actual records and returning memory. Fresh pure ports, arithmetic controls, startup and holding noise are separate inputs. The cleaned message is at the receiver; returning it to the helper costs an additional transfer.

At `(4/5,1/5)`, one million supplied pairs and total source-comparison allowance `10^-3`, exact integer certificates give:

| Block pairs | Quantum message qubits per pair, including padding | Pair-bank qubits with two banks at each end |
|---:|---:|---:|
| 32 | 1.000000 | 128 |
| 128 | 0.984438 | 512 |
| 512 | 0.892978 | 2,048 |
| 2,048 | 0.815652 | 8,192 |
| 8,192 | 0.775023 | 32,768 |

Arithmetic/message work is additional. The asymptotic transmission rate is the established binary entropy `H_2(1/5)`, but finite storage and service time can make direct coupling or uncompressed delivery preferable. Saturated erasure codes have flat node spectra, so this entropy-rate compression provides no saving there. The compiler is a conditional capability for biased fixed resources, not an advantage over equally informed conventional source coding.

The plotted resource frontier is in [resource_frontier.svg](factory/resource_frontier.svg). The service condition is explicitly `T_prepare+T_send+T_expand <= b*tau` for double buffering; no physical rate has been established.

## 5. Review, execution and source status

All principal results have distinct internal reviews at their stated scopes. These are actual internal mathematical/code reviews, not external peer review or hardware validation.

| Subject | Independent review |
|---|---|
| Exact helper/repair construction | Root; independent exact basis-gate audit |
| General purified recovery and helper overlap | Classical-capacity agent; direct-output and clean-work corrections |
| Connection-resource reduction | Protected-algebra agent; stronger separable trace comparator |
| Purification spectrum and causal examples | Architecture agent; complex physical-support correction |
| Causal pair factory | Classical-capacity agent; pure input ports and message location clarified |
| Protection-preserving reencoding | Protected-algebra agent; mixed-encoder challenge also by classical-capacity agent |
| Encoder rigidity | Classical-capacity agent; root separately validates the contributed exact metric equality |
| Distributed mixed-gauge attainment | Protected-algebra agent; different exact code instance |
| Protection-flow synthesis | Architecture agent; mixed-input-bank closure made explicit |

Receipts under `reviews/` pin the exact files and exclusions. Reviewers' own contributed refinements are not presented as independently self-reviewed. Earlier proof versions and actual corrections are retained. [Corrections and failures](CORRECTIONS_AND_FAILURES.md) records the decisions they changed.

The exact executions include 8,568 signed helper-Pauli pairs with 132,960 independently checked operator-column equalities; full logical matrix-unit and actual-record repair identities; 27,648 independent factory prefix paths and 16,092 reversible ranking inputs; complete retained-memory consumer checks; non-Clifford adaptive reencoding; mixed-encoder/key failures; and distinct distributed-gauge constructions. Finite tests support the analytic proofs. Floating trace/spectral and entropy-cone diagnostics are labeled and do not certify physical noise or quantum attainability.

Run `python p2_flow/verify_integrity.py` from the workspace root to check the inventory, actual receipt pins and 463 preserved files across the immediate predecessor and its four predecessors. This is byte integrity, not revalidation of historical theorems. The scientific executables are beside their data, with reproduction notes in the algebra and information folders. Most exact checks use standard Python; some diagnostics require NumPy/SciPy, and the optional plot uses Matplotlib. Scripts normally regenerate their adjacent JSON results.

Primary source read scopes and genuine gaps are in [SOURCE_SCOPE.md](SOURCE_SCOPE.md) and branch ledgers. Astra U1064's actual toggled-frame/recovery correction remains attached; absent producer archives and a physical netlist have not been promoted into an implementation claim. Accepted channel-undecidability foundations were not reopened. Quantum Singleton bounds and the general-CPTP common-decoder reduction are established in [Grassl–Huber–Winter](https://arxiv.org/abs/2010.07902); the entropy accounting, concentration/dilution and state-preparation constituents are credited in the source ledger. Historical priority for the present derived identities and bridge has not been exhaustively investigated.

## Scientific boundary left open

The consequential remaining boundary is **approximate future protection with a real service and noise interface**, rather than a smaller comparison number for an exact target. The current theorem can diagnose maximum exact packing, and the counterexamples explain how redundant architectures change the available operations. It does not yet prove a universal rate law for approximate codes, correlated/returning loss, noisy syndrome acquisition or history-conditioned outside mixed supplies. Those cases require their actual quantum information and causal supply boundary; they are not repaired by relabeling a sufficient norm bound as a physical threshold.
