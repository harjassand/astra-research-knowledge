# When the control record arrives: causal memory for one quantum payload

This construction shows that a small payload and small coherent source workspace do not by themselves bound the quantum memory required to recover that payload from mixed physical outputs. In the specified emitted family, moving a short classical control record from before the stream to after it changes a constant-workspace local reader into an operation requiring extensive retained quantum memory and quadratic memory-time. It does not resolve the separate low-memory receiver problem for a homogeneous weak partial-SWAP stream.

Read the complete [report](package/causal_payload_memory.pdf), [editable proof](package/causal_payload_memory.tex), [algebraic theorem](package/proofs/late_selector_theorem.txt), [independent proof/interface audit](package/proofs/late_selector_independent_audit.txt), and [physical small-bias instantiation](package/proofs/small_bias_instantiation.txt). Channel errors are **half diamond distance**. Recorded normalized-Choi half trace residuals are not numerical diamond-norm evaluations.

| Distinct result | Direct route |
|---|---|
| Finite-error capacity, every-prefix and expected memory-time law | This page |
| Actual early/late readers, two selector families and finite error costs | [Finite implementations](finite-readers.md) |
| Restricted one-tracial-qubit partial-SWAP receiver | [Separate no-go](scalar-receiver-no-go.md) |
| Unknown linear diffusion under a new common thermal port | [Thermal-pulse identification](thermal-pulse-identification.md) |
| Translational force functional from raw blurred images | [Calibrated image-query construction](image-force-query.md) |
| Original material | [ZIP](original/causal_payload_memory_research_package.zip), [complete captured return](P2_CAUSAL_PAYLOAD_MEMORY_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

## Exact task and memory cut

A fixed source encodes one arbitrary input qubit, with external-reference correlations, using a tracial gauge register of dimension D. Selector j chooses `E_j(rho)=V_j(rho tensor I_D/D)V_j^dagger`; the emitted payload dimension is `N=2D`. The physical late decoder may depend on j. Before any selector information arrives, the causal receiver implements one common compression C into dephased classical branches, each with quantum dimension at most m. Classical records may be unlimited. **Every accessible coherent register crossing the cut counts**, including delay lines, ancillas, meters and entanglement halves.

The emitter accepts no feedback changing its future encoding or record schedule. Receiver-internal adaptive processing is allowed. Timing, routing or metadata cannot leak a selector early without changing the experiment. Strong finite source gates and a final full SWAP are actual resources; this is not a weak-action replacement for the earlier tracial stream.

## Capacity theorem from a finite binary family

Let `H_j=V_j(Z tensor I_D)V_j^dagger` be balanced Hermitian involutions. Suppose for **every complex matrix K**, in unnormalized Hilbert–Schmidt norm,

```text
sum_j p_j ||[K,H_j]||_2^2
 >= kappa ||K-Tr(K)I/N||_2^2.
```

If selector-averaged decoded arbitrary-payload recovery has half diamond error `epsilon<=1/2`, then

```text
m/N >= max(0,1-8 epsilon(1-epsilon)/kappa).
```

This does not assume one actual whole-output decoder. Recovery of the two encoded basis probes `(I+-H_j)/N` implies average discrimination bias at least `1-2epsilon`. With `sigma=C(I/N)` and `x_j=C(H_j)/N`, a **single analytic Petz witness** `R(X)=C^*(sigma^-1/2 X sigma^-1/2)/N` has correlation `q_j>=||x_j||_1^2`. The gap bounds its entanglement fidelity below, while every composite Kraus operator through dimension-m memory has rank at most m and bounds it above by `m/N`. The Petz map is an analytic witness with a trace-preserving support extension, not an efficiently compiled physical operation required of the receiver.

The supplied audit verifies the factor eight and the selector-dependent/common-witness distinction. It also repairs an essential instantiation issue: families consisting only of `X_flag tensor U_j` have a nontrivial commutant. The final family includes a Z-flag anchor; dropping it destroys the stated positive gap.

## Prefix capacity, actual branch occupancy and time

For a stream of s output qubits, algebraically defer a prefix operation past untouched future source steps and grant the suffix free. At prefix length ell the same bound gives `m_ell/2^ell>=r`, where `r=1-8epsilon(1-epsilon)/kappa`. If `r>1/2`, a whole-qubit implementation needs **maximum/provisioned** capacity ell. That does not assert every classical branch holds ell qubits.

For branch dimensions `m_y=2^q_y`, under the maximally mixed payload or Bell-input marginal, the actual branch probabilities obey

```text
r <= E[2^(min(q_y,ell)-ell)],
E[q_y] >= f_ell=max(0,ell(r-2^-ell)/(1-2^-ell)).
```

These are expectation bounds for compatible physical branch probabilities, not sums of maxima from unrelated histories. With arrival spacing at least tau, retained qubit-time before selector information is at least `tau sum_(ell=1)^(s-1) f_ell`, hence `Omega(tau s^2)` at fixed positive r. A further interval with **no selector information** adds `t_header f_s`. Progressive disclosure changes the conditional family: the whole serial-header duration cannot be charged using the unconditional gap without a new argument.

The [actual-emission refinement](package/proofs/emission_error_refinement.txt) separately handles noisy emission and branch probabilities. At half-diamond emission error nu with the same physical arrival/record schedule, use `epsilon+nu` in capacity. Actual expected occupancy is bounded by `max(0,f_ell(r_(epsilon+nu))-ell nu)`. The correction transfers a bounded occupancy statistic under prefix-record total variation; final-channel closeness alone does not control earlier record arrival or unbounded timing changes.

## Complete operation and recorded example

The [finite-reader page](finite-readers.md) supplies a small-bias Pauli family with exact `kappa=4/5`, a logarithmic header and a once-through early reader using local eigenmeasurements and a parity bit. The equally informed late baseline stores every carrier, then runs the **same O(n) decoder** after receiving the record. The separation is memory/protection exposure, not an invented quadratic processing disadvantage.

At 1000 gauge carriers, the supplied small-bias construction uses a 25-bit header and error 0.01 gives `m/2^1001>=0.901`. Maximum whole-qubit capacity before the flag is at least 1000 and after it at least 1001; expected retained qubits after the flag are at least 901.901. Pre-record expected memory-time is at least `450950.228340645 tau`, against direct storage's `500500 tau` over those intervals. These are analytic/classical arithmetic points, not a 1000-qubit simulation or device.

The [recorded channel checks](package/proofs/payload_memory_verification.json) and [original program](package/proofs/verify_payload_memory.py) include 344 full Pauli/anchor cases through n=4, mixed-correlated gauge checks, commutator spectra, hybrid-memory examples and a specified early-measurement late-reader baseline. Maximum reported normalized-Choi half trace residual is `3.89e-16`. [Finite-field checks](package/proofs/small_bias_execution.json) and [resource figure](package/figures/causal_memory_bounds.png) supply further finite evidence and evaluated formulas. No large quantum state, SDP optimum, formal proof assistant or physical experiment was executed by Capital.

Post-measurement information, measurement-relative compression, common compression with setting-dependent measurements, small-bias Pauli mixing, Petz recovery and environment-assisted correction have strong prior machinery. The [prior addendum](package/proofs/prior_addendum.txt), [source ledger](package/sources.json) and report explicitly credit Ballester–Wehner–Winter, Bluhm–Rauber–Wolf and the closer Ioannou et al. comparator. No first late-information phenomenon or exhaustive historical-priority finding is claimed.

The substantive independent audit is credited at its actual main-theorem/interface scope; independent companions retain their own proof/evidence status. Both earlier nonquantum companions and complete rare-failure/tracial packages are preserved in `package/warm/`. The pure-port weak-export gap and the homogeneous weak mixed-stream causal-receiver gap remain unresolved. No new Capital reproof, audit or scientific rerun occurred. Generated current retrieval is unchanged; complete proofs and scoped pages are directly public on GitHub.
