# Independent audit: circuit-level one-basis projection

## Verdict

The acquisition in `canonical_qec_circuit_gate_20261105/acquire_graph.py` is mathematically valid for the declared uniform depolarizing channels and independent X-error channels at exact rational p=1/1000. Independent forward propagation, finite channel enumeration, exact rational bracket checks and separate stabilizer simulation agree. No in-scope counterexample was found.

This does not certify an efficient circuit-level rare-event estimator. The current floating tilted-proposal pilot has one acceptance in 10,000 proposals and explicitly makes no confidence claim.

## What distribution and event are preserved

The circuit is Stim's generated rotated Z-basis surface-code memory, with all four noise knobs set to p: after-Clifford depolarization, before-round data depolarization, before-measurement flips and after-reset flips. Preparation/reset and final readout errors are therefore included. This is not the earlier phenomenological model's perfect-boundary convention.

The preserved joint record comprises detectors with coordinate class (x+y) mod 4 = 0 plus logical observable L0. This is the Z-stabilizer detector sector appropriate to the logical Z-basis memory experiment; an L0 flip is a failure of that memory experiment, not a claim to sample both logical Pauli sectors. Detectors in the other basis are discarded. Their correlations are not claimed to be preserved.

Each projected error includes both its selected-detector bit vector and its L0 bit. The internal logical labels form a gauge coboundary. For every individual edge, original logical bit XOR left-boundary incidence equals the gauge dotted with its detector syndrome. Consequently, on an error-plus-correction residual with zero syndrome, original logical failure equals left-cut parity exactly. The boundary leaves classify mechanisms by this gauge identity; they should not be interpreted as additional physical qubits.

The pilot decoder minimizes integer edge costs 4 or 5. This is a precisely defined decoder but is not exact log-likelihood weighted MWPM, an optimal decoder, or a decoder exploiting the discarded detector sector.

## Exact factorization proof

A uniform k-qubit depolarizing channel assigns probability 1−p to identity and p/(4^k−1) to every nonidentity Pauli. Its projection to a rank-r binary effect image gives the same Fourier coefficient

lambda = 1 − 4^k p/(4^k−1)

to every nontrivial character on that image. Introduce one independent Bernoulli factor on each nonzero image vector, all with probability q satisfying

(1−2q)^(2^(r−1)) = lambda.

Each nontrivial character is negative on exactly 2^(r−1) such factors, so the resulting Fourier coefficient is exactly lambda. All characters match, hence the full projected joint distribution matches. Rank-zero channels disappear. Independent original channels can be transformed independently, and identical effect factors can then be merged through multiplication of their survival factors 1−2q.

This is not the invalid approximation of replacing correlated qubit errors by independent marginal flips. For two-qubit depolarization at p=1/1000, the projected X-error bits have P(11)=1/3750, whereas the product of the two marginals is 1/3515625. The audited three-factor image construction preserves the former.

This theorem is not established for arbitrary nonuniform Pauli channels. For example, an exclusive distribution with positive P(10), positive P(01), and zero P(11) cannot generally be represented by positive small independent factors on all three nonzero image vectors. Uniform depolarization is a substantive assumption.

## Independent executable evidence

`audit_projection.py` and `projection_results.json`:

- Exhaustively checked all 272 maps from two or four Pauli generator bits into two effect bits, using exact rational direct distributions and Fourier coefficients.
- On the d3 circuit, independently propagated all 1,430 original-channel Pauli cases forward using a plain Python frame simulator, rather than the acquisition's backward propagation.
- Ran all 1,307 nonidentity d3 single faults through a separate forward stabilizer simulation and matched every detector and L0 output.
- Verified all 55 merged probability enclosures directly: because projected rank is at most two, each merged survival factor squared is an exact rational, so no numerical square root or acquisition rounding code is needed for this check.
- Matched the total conversion TV budget exactly and checked every graph gauge/boundary identity.
- Found 278 full-record fault cases with more than two detector flips before projection. This confirms why the single-basis scope matters.

`audit_d13_projection.py` and `d13_projection_results.json`:

- Independently propagated all 46,084 Pauli generators through all 17,367 original noise channels using packed forward bit arithmetic.
- Verified every one of the 6,085 merged error effects and exact probability brackets, all gauge identities, and 100 further independent stabilizer simulations.
- Reproduced the exact conversion TV bound: 5411 / 3138550867693340381917894711603833208051177722232017256448, approximately 1.7240440662e−54.

`audit_weighted_decoder.py` and `weighted_decoder_results.json` check the pilot's d3 weighted decoder against a separate syndrome-space shortest-path computation for every syndrome, plus random logical-event and weighted-witness checks. This is separate from projection correctness.

## Numerical boundary

The small TV bound encloses the exact-rational p=1/1000 circuit distribution using 192-bit factor brackets and exact rational midpoint probabilities. It does not include the difference from a literal binary64-parameter Stim sampling distribution.

The parameter difference is exactly 3 / 144115188075855872000. Across 17,367 channels, a simple coupling bound for that distinct model is 3.6152331129e−16. This bound is conservative, but much larger than the 192-bit conversion bound. The floating Stim DEM comparison is therefore a diagnostic, not a source of the 1e−54 certificate. Any result should clearly state which model it certifies.

## Pilot and proposed pruning

The floating d13 tilted proposal reports Z≈2.1008319111e−4 and only one acceptance in 10,000 proposals. A precise circuit-level rare-rate estimate and end-to-end incumbent advantage have not been demonstrated by this pilot.

The proposed strict clean-clean triangle exclusion is sound: if two consecutive residual-path edges have no error, they both lie in the minimum-weight correction. XORing their triangle changes correction cost by −w1−w2+w_shortcut(1−2 C_shortcut), which is negative when w_shortcut<w1+w2, whether or not the shortcut is already in the correction. Equal-cost shortcuts cannot be excluded under deterministic ties. This proves the exclusion's necessity, not the correctness or efficiency of any new automaton implementation.

## Reproduction

Use the existing decoder environment, for example:

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python canonical_qec_circuit_audit_20261105/audit_projection.py

The d13 and weighted-decoder scripts use the same interpreter. Each JSON report records the tested acquisition source hash or its precise scope. No reserved experiment data were used.
