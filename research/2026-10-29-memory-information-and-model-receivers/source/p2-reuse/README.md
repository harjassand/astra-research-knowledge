# Astra P2 — irreversible information, reusable interactions and coherent service

29 October 2026. This tranche continues the accepted causal-receiver, actual-record, exposure-code and measured-syndrome work. Earlier tranches are preserved byte for byte. The new objective was to turn protection at a completed interface into a reusable information-processing resource, while identifying which resource a small mediator does not supply.

## Scientific result

Three different resources must be kept distinct: quantum information that can safely remain in memory, information that must irreversibly leave a correction interface, and the rate at which lost quantum connections can be restored. The constructions below make those distinctions mathematical and executable.

The main foundational advance is a **graded criterion for irreversible syndrome conversion**. After an acquired coherent recovery correcting through fault order t, it is enough to dephase the capped minimum fault-cost tier c(s)=min(r(s),t), rather than the entire fine syndrome, to retain complete-channel order d=2t+1. The fine syndrome can remain quantum. For odd phase repetition, t+1 irreversible sectors are sharp within the specified nondemolition converter family, and residual coherence between tiers a distance Delta apart must scale as O(eta^Delta). A finite physical pointer construction attains that graded law with all actual detector outcomes retained. This identifies what must be lost, rather than treating full syndrome measurement or complete coherence as the only choices.

The operational bridge is **whole-space closure of reusable couplers**. A completed gate acting as G_source tensor identity on every admitted mediator input prevents old mediator memory from broadcasting errors through later good gates. A source-support compiler transfers that property to conventional fault-tolerant circuits. The explicit witness includes noisy syndrome acquisition, preparation, readout and all serial idles; it meets both algebraic Flag 1-FTEC conditions. The bridge supplies a reusable gate interface conditional on its native ports and noise contract. It does not claim that the coupler is cheaper than direct gates.

A separate **coherent service-rate converse** explains the limit of serialization. Under independent complete replacement erasure, a finite protected controller and a bounded number of source-service completions cannot preserve an indefinitely growing quantum register, regardless of code, classical feedback or final decoding. The proof counts the quantum wires surviving a last-erasure causal cut. This is a physical-model converse, not a reinterpretation of a small interaction norm as a loss probability. Distributed closed couplers give a concrete way to supply parallel service with linear coupler count and constant depth overhead on a bounded-degree conventional circuit.

## Entry points and exact scope

| Package | Result | Load-bearing interface | Review |
|---|---|---|---|
| [Graded record principle](record_principle/GRADED_RECORD_PRINCIPLE.md) | Minimal irreversible tiers and sharp graded imperfect conversion | Supplied coherent extraction/correction, acquired fault-cost grading, retained fine syndrome, all actual records, no return of retired purifications | [Accepted after two scope clarifications](reviews/graded_record/INDEPENDENT_REVIEW.md) |
| [Closed-coupler compiler](architecture_challenge/EXACT_CLOSED_COUPLER_COMPILER.md) | Fault-support transfer plus full noisy Flag 1-FTEC and distributed continuation | Whole admitted mediator space, stated native ports, local completed faults, trusted address/lookup controller | [Accepted](reviews/coupler/INDEPENDENT_REVIEW.md) |
| [Coherent service rate](contact_rate/COHERENT_SERVICE_RATE.md) | Arbitrary-code cut bound and adaptive strong converse | Independent complete no-return replacement erasures, finite protected quantum memory, acquired interval completion cap | [Accepted after an adaptive-conditioning clarification](reviews/contact_rate/INDEPENDENT_REVIEW.md) |
| [Reusable closure and causal normalization](reusable_algebra/REUSABLE_CLOSURE_AND_CAUSAL_NORMALIZATION.md) | All-memory algebra certificate, selected-subset noise adapter and causal comparison comb | Entire returning memory included; certified boundary slots; actual record-control support; comb-level good-part factorization | [Accepted, including the overlapping-window norm adapter](reviews/closure/INDEPENDENT_REVIEW.md) |

These results can be used together only after their interfaces have been matched. In particular, the graded-record converter assumes coherent correction has already been acquired. It is not silently substituted for the separately constructed flag circuit's noisy syndrome acquisition. The coupler's source-support proof does not alone supply a selected-subset norm bound. The service converse does not use or infer a probability from that norm bound.

## 1. A sharper question about measurement and irreversibility

Let r(s) be the least acquired fault cost of a syndrome, and set c(s)=min(r(s),t), d=2t+1. A path in tier c needs degree at least c; one with a nonidentity residual logical operation needs degree at least d-c. When only equal-tier ket/bra paths remain, every logical-dependent cross term therefore has total degree at least d.

A physical instrument can dephase the tiers while retaining the finer syndrome register. The normalized common memory channel is extracted from the actual full channel using the earlier dummy-input projection; that normalization is ancestry, not a new claim in this tranche. The new content is the irreversible partition and the criterion for residual coherences. For degenerate stabilizer codes the distance premise is about nontrivial logical cosets, rather than treating every equal-syndrome Pauli pair as harmful.

If alpha_cb is the completely bounded norm of a converter's cross-tier block, its first potentially harmful degree is d-|c-b|. Thus alpha_cb=O(eta^|c-b|) restores order d. The repetition construction supplies a matching physical lower bound against any logical-identity tensor common comparison channel. An independently computed five-qubit repetition example has first complete-channel defect order 3 without conversion, 5 with ideal tier conversion, 5 with the graded finite meter, and only 4 with uniform off-tier overlap O(eta).

Fresh unary threshold pointers realize alpha_cb=kappa^|c-b| with kappa=O(eta). This includes the complete actual measurement word. A random phase key kept in the accessible record does not achieve the same cancellation; forgetting it only in an analysis marginal is insufficient. A retired measurement purification that returns likewise changes the interface.

The t+1 optimum is a **purified Stinespring environment/Kraus-rank** bound for the specified converter family achieving the order, not a lower bound on a bare detector supplied mixed. It is also not a Shannon entropy, heat, reset-time or universal recovery bound. Coherent decoder cost, tier lookup, fine syndrome storage, meter supply and eventual reset remain real costs. An unrestricted optimized recovery or ordinary full syndrome reset remains a strong alternative.

## 2. From a closed gate to an actually reusable correction component

The chronological bus sequence

    CX(a,M), CZ(b,M), CX(a,M), CZ(b,M)

is CZ(a,b) tensor identity_M. Source Hadamards on b before and after give CNOT(a,b). Its validity on the whole admitted bus input is what permits arbitrary returning memory and earlier correlations. A calibration on M=0 is a different, weaker interface.

The finite compiler retains every real measurement record and permits common, noncommuting bath coefficients. Physical contact or participating-source faults stay on the current abstract gate's two endpoints; spectator-idle faults retain their own labels under the stated support condition. This is a statement about error spaces. Its noise-strength adapter is separate.

The first one-pass flag controller was a useful failure. It corrected every single input Pauli with no faults and every single fault on clean input, but it did not meet arbitrary-input output containment. The saved witness leaves a syndrome which no weight-one error can produce. The construction therefore adopted the stronger conventional two-pass Flag 1-FTEC controller from [Chamberland–Beverland](https://arxiv.org/pdf/1708.02246), retaining that paper's two distinct recovery conditions.

The new circuit explicitly supplies two source ancillas, their preparation and reuse, noisy contacts and source controls, quantum measurement, separate readout faults, actual records, deterministic fallback on every record and all serial idles. Its classical address/lookup logic is trusted. The common correctable operator span supports coherent faults, not merely a stochastic Pauli sample. A late fault may leave a correctable non-code output; no ideal decoder is inserted between physical rounds.

### Strong matched comparison

| Per abstract CNOT | Direct source gate | Closed bus | Qualified reset bus |
|---|---:|---:|---:|
| Entangling primitives | 1 direct CNOT | 4 source–bus contacts | 3 source–bus contacts |
| Source Hadamards | 0 | 2 | 2 |
| Bus resets | 0 | 0 | 1 |

The closed bus exchanges one extra contact for one avoided reset. Under the declared serial timing model it is faster than the reset route exactly when reset time exceeds contact time. This is not a noise, energy or device-advantage conclusion. Direct gates remain cheaper if their ports are available on the same terms. Verified ancillas and teleportation can buy parallelism at larger supply cost; they are not excluded.

The full clean/maximal two-pass ledgers have respectively 1,464/1,896 total locations with direct gates, 5,016/6,626 with the closed bus and 5,088/6,722 with the reset bus. Unit ticks are a counting convention; physical waits and classical feedback latency must add their real idle exposure. On a degree-Delta source graph, at most Delta n/2 separate buses compile each source matching layer in six parallel substeps. That constructive option supplies parallel service instead of assuming it from a small global mediator.

## 3. A quantum cut measures the service needed after loss

Let A(t) count idle sites which have not been completely erased since their last quantum connection. Let w be the number of source qubits held in coherent service and b the number of other protected/returning quantum memory qubits. All actual classical histories are retained, and the final decoder can be arbitrary. For preservation of K unknown logical qubits,

\[
F_e(t)\le \mathbb E\min\{1,2^{A(t)+b+w-K}\}.
\]

After a site's last independent replacement erasure, local operations and classical communication cannot reconnect it quantumly to the rest. A refined convex decomposition therefore has Schmidt rank at most 2^(A+b+w). No physically unobserved Kraus label is turned into a free classical record by this argument. Returning erased purifications, fresh Bell supplies and protected bypasses have explicit negative controls and must be counted as additional quantum resources.

For loss rate gamma, interval length Delta, q=exp(-gamma Delta), and at most c completions per interval, an adaptive strategy is dominated at interval endpoints by

\[
B_{m+1}=\operatorname{Binomial}(B_m,q)+c,\qquad B_0=N.
\]

Its exact generating function is

\[
G_m(z)=[1+(z-1)q^m]^N\prod_{j=0}^{m-1}[1+(z-1)q^j]^c.
\]

The proof preassigns clocks before within-interval scheduling. It does not claim that an adaptively selected never-serviced subset has conditionally independent survival. This distinction was corrected in review and the initial wording preserved.

If M=K-b-w grows, c/(1-q)<=rho M for some fixed rho<1, and the initial survivor population Nq^m=o(M), the best attainable entanglement fidelity tends exponentially to zero. Complete operation error tends to one. For small gamma Delta the required coherent service scale is of order gamma(K-b-w). This is a necessary scale under destructive storage loss, not an optimized capacity or a sufficiency theorem.

The strongest direct-coupling, teleportation and adaptive classical protocols receive the same allowances. Independent local replacement, a no-return environment, finite protected memory and a completion cap are substantive premises. Passive self-correction, decreasing physical loss, extra protected memory or extensive parallel quantum activity change the problem rather than contradict the theorem.

## 4. Acquire closure and keep the comparison causal

For a complete isometry, first remove the specified target G and call the resulting identity-target isometry V. With r touched data/control qubits and z<1, local Pauli intertwining defects supply

\[
z=\tfrac12\sum_i\bigl(\|X_iV-VX_i\|+\|Z_iV-VZ_i\|\bigr),
\qquad
\|V-I\otimes W\|\le z+1-\sqrt{1-z^2}.
\]

Define f(x)=x+1-sqrt(1-x^2) for 0<=x<1. The proof uses a finite conditional expectation and its variance identity, with no bath-dimension factor. For an actual joint unitary V, set delta=one half of the diamond distance between Tr_M composed with Ad_V and Tr_M, as channels whose full input is A tensor M. This includes arbitrary correlated data-memory inputs and references; a supremum of separately prepared bath-state tests is not the premise. If 2delta<1, the product-unitary defect is at most f(2delta), linear for small delta. Fixed-bath calibration does not supply this certificate; fresh isometries can retain the usual square-root separation.

Once local full-interface closure is acquired, forced fault subsets can be resummed with every unmarked operation left actual. This gives product strength bounds without a factor exponential in total computation volume. That receiving condition is standard coherent fault tolerance, not a newly proved universal threshold. Overlapping physical contact/idle windows can use a separate mixed-Duhamel finite-difference adapter on their actual Hamiltonian supports; source-span regrouping alone does not prove its norm premise.

For a multitime service, endpoint normalization is insufficient. A saved exact counterexample polar-normalizes an endpoint good operator into a map whose first output depends on a future input. A deterministic causal tester instead extracts a normalized common memory comb from the actual comb while preserving record times. This requires good-part factorization at the retained slots. It cannot upgrade an endpoint statement or protect an undeclared internal intervention.

## Evidence, corrections and continuation

All four packages keep proofs, exact executable evidence, source ledgers and actual review receipts. The principal author checks include 113,646 low-degree repetition pairs, complete noncommuting-bath polynomial maps, 2,663,343 native arbitrary-input one-fault cases, and exact finite adaptive service models. Independent audits use different representations: a degenerate Shor-code and rational polynomial instrument challenge, word/matrix circuit reconstruction, and labelled-site adaptive optimization with direct Schmidt-rank fixtures. These finite checks challenge the proofs; they do not replace them or acquire hardware parameters.

Preserved failures include the one-pass reuse failure, retained phase key, returned purification, fixed-bath calibration, exposed internal SWAP slot, endpoint polar causality failure, freely corrupted command record, and the adaptive-selection wording correction. The reviewer-only dirty-bus calculation correction is recorded separately.

A practical computing advantage still needs an acquired source/control interface, encoded supply and logical operations under compatible physical noise and timing. Those are not supplied by a memory representation, a small comparison error or the present algebraic 1-FTEC test. The foundational opening is already concrete: certify exactly which coherent information may survive an interface, which must become irreversible, and which quantum connections must be continually replenished. This permits architecture choices to be made against the resource actually missing rather than by refining a representation error that was already small.

### Reproduce

Run from the workspace root:

```bash
python p2_reuse/record_principle/record_principle_checks.py
python p2_reuse/reusable_algebra/reusable_algebra_checks.py
python p2_reuse/architecture_challenge/closed_bus_flags.py
python p2_reuse/architecture_challenge/reusable_flag_ec.py
python p2_reuse/contact_rate/contact_rate_checks.py
python p2_reuse/verify_integrity.py
```

Independent audit programs are in `reviews/`. No external circuit package or hardware connection is required. Scientific scripts use the exact scalar helpers identified in their source; byte-integrity verification is separate from scientific acceptance. [SOURCE_READ_SCOPE.json](SOURCE_READ_SCOPE.json) and the package-specific ledgers record actual governing-source reads and full-text gaps. Nothing is inferred from unavailable archives. `MANIFEST.json` inventories this tranche and verifies the frozen predecessor bytes; it does not revalidate their science.
