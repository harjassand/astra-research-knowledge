# Independent review: finite repeated on-site service factorization

28 October 2026. Reviewer `producer-workspace/review_repeated_service_factorization`.

**PASS, scoped to the revised source** `ordinary_onsite_repeated_service_factorization_20261028.md`, SHA-256 `bfa2f03e320a14fbbb8d3d60909a96899ac135ea064df94ac4d85a2b597f94ab`. The root adopted two requested precision fixes and preserved the original as `_initial.md`: conditional payload/reference independence for the payload-only diamond channel, and a distinction between detectable replacement histories and latent bad fitted histories. Neither fix changes the factorization or constants. No author or governing source was modified by this reviewer.

The new mathematical claim is valid. Independent exact checks establish the complete two-slot map equality, not just selected state fidelities, for a physically admissible retained-coherent-memory instrument. Explicit witnesses also demonstrate why fresh frames and completed-output isolation are genuine load-bearing assumptions.

## 1. Governing acquisition result actually imported

Read the complete exact on-site train/freeze proof and its root and independent statistics receipts. Its on-site algebra is a physical tensor-factor assertion: two anticommuting true logical generators on one physical qubit generate that qubit's full matrix algebra; distinct logical factors occupy distinct sites. Correct true local extraction therefore leaves `I_L tensor V_G`, not a gauge-controlled logical correction. The fitted receiver differs from this extraction by a fixed product unitary `W=tensor_i(Vhat_i^dagger V_i)` on the logical factors.

The existing coarse/fine banks and proper quaternion fit supply a **record-defined** event of probability at least `1-beta` on which

`e_h = 1-product_i |Tr(W_i)/2|^2 <= 9 epsilon0/32`.

The rotation error is independent of the current gauge and retained-memory state. The martingale confidence derivation accepts arbitrary positive beta; only its later one-service epsilon-only corollary restricts beta relative to epsilon0. Therefore substituting `epsilon0=epsilon/T` while retaining `beta<=epsilon/8` is legitimate. It does not require the stronger and unnecessary condition `beta<=epsilon/(8T)`.

Reverified the 14 direct on-site statistics bindings, its 39 main/statistics/Jacobi dependency bindings, and the three direct on-site root bindings. The inherited fixed fine schedule and physical fallback are defined even for missing/nonunique matching. No new statistical sampling or acquisition claim is needed for the repeated-service extension.

## 2. Independent instrument-level derivation

Include all future-accessible source degrees of freedom in M. After true on-site extraction one slot is

`E = sum_alpha (Ad_Palpha tensor G_alpha)`

on `L tensor M`, with the gauge output either retained in the displayed instrument or subsequently discarded. This expression is an equality of linear maps, not a specification only on product inputs. Inserting the private input frame Q and inverse output frame after the fitted inverse produces

`Ad_(Q^dagger W P_alpha Q) tensor G_alpha`.

Pauli conjugation gives `Q^dagger P_alpha Q = chi_Q(alpha) P_alpha`. The scalar sign disappears from the CP map. Consequently each fixed alpha term has the same left logical factor `Ad_(Q^dagger W Q)` relative to exact extraction. Since the entire source map is nonanticipating with respect to this fresh private Q,

`average_Q E_learned,Q = (Lambda_W tensor id) E`.

The equality holds on **every** operator on `L tensor M`, hence also with arbitrary logical-memory correlations and arbitrary external reference extension. It is stronger than proving an input-Bell fidelity identity. One does not condition on a latent alpha outcome to discard its probability or assume that source labels are independent.

Expand `W=sum_P w_P P`, with `w_P=Tr(P^dagger W)/2^q`. Orthogonality of Pauli-conjugation characters eliminates all `P != P'` cross terms under Q averaging, yielding the physical Pauli channel

`Lambda_W = sum_P |w_P|^2 Ad_P`.

Parseval gives total probability one. Since W is a tensor product, its coefficients and channel factor over logical sites, and its identity mass is `p0=product_i |Tr(W_i)/2|^2=1-e_h`. Global CP identity dominance is not used: that additional hypothesis belonged to the earlier full-CPTP one-slot oracle interpretation, not this same-source closeness theorem.

## 3. Retained coherent memory does not obstruct composition

Let E_t be the actual time-t source operation, including retained quantum/classical source state and any admissible dependence on earlier source history. It acts on the current input and source state, not on completed outputs. A local error channel Lambda on a completed output therefore commutes with every subsequent E_t as a superoperator on disjoint tensor factors. Entanglement does not invalidate commutation of local linear maps.

Fresh independent frame averaging can be performed slot by slot inside the composed circuit. Moving each resulting output error to the end gives

`E_learned^(T) = (Lambda_W^tensor T tensor id_final_memory) E_exact^(T)`

if final memory is kept, and the source's displayed formula after that memory is traced. This stronger map identity allows correlated Pauli histories, coherent retained memory, nonstationary instruments, and entangled future inputs. No source reset or product-source-trajectory assumption appears.

For a conventional channel from the qT payload inputs alone, the initial source memory must be fixed independently of the full payload/reference, conditional on calibration h. The revised source now says this explicitly. If that initial independence is removed, the enlarged-domain map on payload **and** M still obeys the identity and a corresponding state bound, but it is not in general an induced channel on arbitrary payload inputs alone. Current-input/memory correlations formed during service are unrestricted and are already handled by the enlarged map proof.

The benchmark is the same physical source process starting at the physically actual conditional post-calibration memory, with true extraction at each slot. It is neither an alternative calibration trajectory nor a collective decoder optimum.

## 4. Diamond constant and calibration averaging

For a Pauli channel with identity mass p0, the half-diamond distance from identity equals `1-p0`. The convex decomposition gives the upper bound; applying the channel to half of a maximally entangled state gives mutually orthogonal Pauli-labelled Bell outputs and attains it. On T **distinct** output registers the identity mass is `p0^T`, with no cancellation of errors acting on different registers. Contractivity under precomposition by the exact source gives

`half ||E_learned^(T)-E_exact^(T)||_diamond <= 1-(1-e_h)^T <= T e_h`.

Equality of the first bound is not claimed for an arbitrary noisy source. It is attained when the source's exact extracted joint channel is identity. Conditioning on h is essential: there is no substitution of the mean e inside a nonlinear power.

At `epsilon0=epsilon/T`, the same good event bounds `T e_h<=9 epsilon/32`. Its physical probability can fall by at most `nu_cal` under the declared calibration-record TV discrepancy. On every other physical record, both complete services are CPTP, so their half-diamond distance is at most one. Detectable flagged/undefined histories can deliberately replace; a latent bad but unflagged history still deploys its physical fit. One bad-event debit suffices for the entire block, without a factor T. Adding the whole-service implementation error yields

`actual mean joint-channel error <=9 epsilon/32+beta+nu_cal+nu_svc<=21 epsilon/32`.

This is an average-over-calibration guarantee, or a controlled classical-record channel guarantee with the record distributed by acquisition. It is not a certificate that a particular accepted record has small posterior error.

## 5. Exact independent evidence and failure witnesses

`onsite_repeated_service_factorization_independent_check_20261028.py` uses exact rational/Gaussian-rational arithmetic, no author fixture functions, random draws or floating tolerances. It constructs two different time-dependent weak instruments on a retained memory qubit. Each has two noncommuting rational Kraus operators, sums to a TP map, retains off-diagonal memory information, and is not reset between calls. Logical Pauli weights conditioned on its instrument branch have uniform X/Z CP contrast `2/5`; one branch has Y contrast `-1/5`. Identity dominance also happens to hold, though the tested identity does not require it.

The fixed rational SU(2) mismatch has Pauli probabilities

`(400/441,16/441,25/441,0)`.

The check directly enumerates all 16 independent two-slot frame histories and compares the entire 64-by-64 Pauli-transfer map on two payload qubits and one memory qubit with the independently assembled output-noise expression. Equality is exact on all 64 input operators while retaining final memory. Thus arbitrary initial correlations and arbitrary external references are covered by linearity. A GHZ payload-memory input is also evaluated explicitly. The two-output nonidentity probability is exactly `34481/194481`.

Two exact boundary checks are deliberately nonzero:

* **Reused private frame:** even for an identity source, using the same Q at both slots gives a Pauli-transfer difference of `1600/194481` at `(XX,YY)` from independent output noise. Freshness cannot be replaced by secrecy alone.
* **Forbidden output feedback:** insert a CNOT from the first completed output into retained memory between slots. The factorization then fails even after tracing final memory. For the product input `X+ tensor Y+ tensor X+` on payload1, payload2, memory, the payload observable `Z tensor Y` differs from the incorrectly factored prediction by `5902688/2170546875`. Thus the failure does not depend on initial payload-memory correlation or access to final source memory.

Fifteen exact finite-T budget cases check the final constants. The numerical author fixtures were inspected only as secondary context; the receiving decision rests on the independent derivation and exact complete-map check.

## 6. What the implementation interface must actually mean

Calibration-record TV suffices here only because the good event is record-defined and its extracted rotation bound holds uniformly for every later memory state. It can therefore be evaluated on the physically changed post-calibration source memory. The nominal service is then compared with the implemented service from that **same** actual initial memory, using the complete T-slot implementation discrepancy.

A sufficient hybrid bound uses per-slot **control** maps diamond-bounded on their complete acting registers, tensor arbitrary untouched reference/source registers. All actual waiting-input and completed-output storage during that interval, routing, local frames, inverse rotations, disposal/reset and other declared trusted controls must be inside the budget. Summing those per-slot bounds at most `nu_svc/T` gives at most nu_svc. Bounds for reduced single-payload channels tested only at product or freshly reset memory do **not** imply this hybrid statement and are not accepted as substitutes.

The resource mechanism is explicit but conditional: one finite calibration and rational classical fit, then T ordinary source calls, q known inverse one-qubit rotations per slot, two local Pauli frame applications per logical per slot using `2qT` fresh bits, optional paid routing, and isolated live storage. If the whole batch is supplied at the service boundary, approximately qT logical input/output storage locations are live across the batch (plus current source/routing workspace); their holding time spans the declared finite schedule. A physical implementation must supply a total buffer/holding error bound for that schedule, not only gate accuracy on the currently served q qubits. The conservative inherited nearest-neighbor routing cost is `O(T n q)` SWAPs when fixed output placement is required. Flagged records additionally pay their declared replacement resets.

The source does not supply a hardware noise model, gate library, service duration or verified isolation device. Accordingly the theorem is a conditional finite resource/interface result, not a demonstrated construction of arbitrarily accurate quantum storage or a hardware advantage. The exact fixture executes classical algebra only. No environment reconstruction, free payload storage through training, protected calibration reference or source-reset capability is added.

## 7. Receiving scope

Accepted: finite predetermined T; exact persistent on-site logical factors; acquired matching/fixed proper fits; private independently refreshed current frames; arbitrary retained coherent memory; isolated completed outputs and source-inaccessible unserved inputs; whole-block joint-channel comparison to true extraction on the same source; and the explicit implementation interfaces above.

Not accepted or claimed: indefinite reuse, same-register repeated error cancellation, key-conditioned accuracy, output-feedback policies, approximate locality/drift without a new bound, a collective full-CPTP decoder optimum, redundant-code discovery, a fault-tolerance threshold, or practical superiority to the conventional estimator. No unresolved mathematical obligation remains **within this scoped interface**. Supplying and validating an actual physical isolation/storage/control interface remains an external implementation obligation.
