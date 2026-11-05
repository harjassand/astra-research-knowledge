# Circuit-level acquisition and the efficiency gate

The circuit-to-graph acquisition below has been independently checked. The original circuit pilots are floating feasibility diagnostics, not certified rare-event estimates. Any later certified folded-score result must be reported separately with its own source, precommitment, arithmetic and timing ledger.

## Specified circuit and decoder

The source is Stim's public generated `surface_code:rotated_memory_z` circuit. All four noise controls are set to the mathematical rational value p=1/1000: after-Clifford depolarization, before-round data depolarization, before-measurement flips, and after-reset flips. The physical model has independent local uniform depolarizing channels and X-flip preparation/measurement channels. It is a stochastic circuit specification, not acquired hardware calibration.

The d13,13-round instance has169 data qubits and337 used data-plus-ancilla qubits. Stim's index span is376 because its lattice indexing leaves gaps. There are17,367 original noise-channel applications.

The target is the failure of the final logical-Z memory observable when decoded using only its Z-stabilizer detector family. In this generated circuit those detector coordinates satisfy x+y=0 modulo4. The other syndrome family is marginalized. A correlation-aware joint decoder can use information deliberately omitted from this target and is not claimed to have the same failure rate.

The pilot decoder uses fixed integer costs4 or5, stored explicitly with the graph, and minimum-weight matching with deterministic tie behavior. These costs are a specified quantization, not an assertion of exact real-valued log-likelihood matching.

## Exact projection without arbitrary graphification

A backwards Pauli-frame calculation maps every possible local Pauli fault to the selected detector parity vector together with the logical-observable parity. The map is linear over binary vectors.

A uniform k-qubit depolarizing channel, projected to an image group of binary rank r, has the same nontrivial Fourier coefficient

lambda=1-[4^k/(4^k-1)]p.

It is therefore exactly equivalent on that projected output to independent flips of every nonzero image vector, each with probability q satisfying

(1-2q)^(2^(r-1))=lambda.

This follows because exactly half of the nonzero group elements change any nontrivial character. Equality of all binary Fourier coefficients proves equality of the complete projected detector-plus-logical law.

For this circuit family, the acquired projected ranks are at most2, so only rational quantities and square roots are required. Every nonzero image vector flips at most two selected detectors. No projected hyperedge is discarded, and no mutually exclusive events are simply declared independent. The independent factorization is justified by the group identity above.

Identical projected effects from different independent channels are merged by multiplying their survival factors1-2q. Original correlations with the unused detector family are not preserved; the specified marginal is preserved exactly. The full two-basis record contains nongraphlike fault effects, so this restriction matters.

For d13 this yields1,176 selected detectors and6,085 merged independent graph edges. Logical edge labels admit an exact vertex gauge; after gauging internal labels away, boundary mechanisms split into98 left and98 right leaves. Failure is the corresponding residual left-cut parity. No undetected standalone logical fault or inconsistent interior logical cycle was found.

## Controlled numerical conversion

The source probabilities are defined as exact rational1/1000. Square roots and merged products are enclosed with outward192-bit integer arithmetic. Each effective edge is represented by the midpoint of its exact enclosure.

A union coupling gives total variation distance between the true projected circuit law and this dyadic independent-edge law at most

1.7240440663 × 10^-54

for the d13 instance. This is a bound on any event defined by the projected detector/observable record, including failure of the fixed decoder.

Stim's floating DEM is used only as an additional diagnostic cross-check. Its binary representation of0.001 differs from rational1/1000. Coupling that parameter difference across the original channels alone gives a much larger bound, about3.62 × 10^-16. The small192-bit certificate comes from the independent symbolic projection, not from trusting float DEM probabilities as exact.

The acquisition proof applies to these uniform depolarizing and X-flip channels. It does not establish such a positive independent graph representation for arbitrary Pauli channels, leakage, cross-talk or correlated hardware noise.

## First estimator gates

An integer-weight residual witness has nonnegative signed score

S=sum_path c_e(2 error_e-1).

A tilted walk proposal with t=1/2 uses local marked-edge weight P(error_e)2^[c_e(2 error_e-1)]. A completed simple nonnegative-score path is corrected by2^-S and then tested against the decoder's canonical witness.

The unconstrained d13 pilot had a floating normalizer2.10083 × 10^-4 and accepted only1 of10,000 proposals in8.06 seconds. This is a serious efficiency warning, not a certified probability estimate.

A proved necessary condition tightens the cover: two consecutive clean path edges lie in the minimum-weight correction and cannot have a strictly cheaper direct triangle shortcut. XORing that triangle would otherwise improve the correction. Equal-cost shortcuts are retained. A positive automaton tracking the preceding fault bit can enforce this condition without excluding any canonical failure witness.

That automaton reduced the floating normalizer by4.247 times to4.94618 × 10^-5. Its10,000-trial pilot accepted8 proposals in6.00 seconds. It remained a weak efficiency result, with no confidence claim.

The separate score-folded resolvent has now been constructed and certified. Its fixed100,000-trial circuit run accepted1,249 proposals and returned the99.9% interval[2.40981e-8,2.90208e-8], including conversion error. See qec_score_resolvent_20261105/THEOREM.md, the frozen production output and the independent folded-sampler audit. The initial floating pilots above remain diagnostic records, not separate certified estimates. The exact sampler, null/slack treatment, finite stopping and complete setup costs are documented in that separate result.

## Independent evidence

The circuit audit checks all projected Pauli maps at d3, hundreds of forward stabilizer simulations, complete projected-group factorizations, exact rational enclosures and boundary gauges. At d13 it independently propagates46,084 Pauli generators across17,367 channels and checks all6,085 merged probability enclosures. See the separate circuit-audit directory for full code and results.

The same-access benchmark must use this circuit, projected information, probability convention, fixed integer-cost decoder and final logical event. The ideal-check or phenomenological comparison is not a substitute for a circuit-level comparison.
