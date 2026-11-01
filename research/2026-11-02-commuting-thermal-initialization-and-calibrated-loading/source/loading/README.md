# Thermal loading: calibrated noise and reachability

1 November2026. Ordinary proof/code package with internal independent reviews and explicit limits.

## Completed narrow bridge
CALIBRATED_LOADING_JOIN.md gives the accepted scoped result: a positive, efficiently sampleable pre-distorted syndrome distribution compensates a sufficiently small KNOWN independent terminal Pauli-noise layer for the actual COMMUTING recursive code. It preserves a supplied reference-entangled encoded input up to the stated error. Existing polymer machinery is credited and used.

This is not a full noisy encoder/readout or a generic spin-bath initializer. Required fault probabilities can be extremely small at low temperature. Finite high-precision negative examples are included, rather than hidden.

## Main files
- calibrated_terminal_noise_candidate.md: frozen proof, despite its historical candidate label.
- CALIBRATED_NOISE_WHOLE_ANALYTIC_RECEIPT.md: qualified whole analytic acceptance.
- ROOT_INTERACTING_POLYMER_SAMPLER.md and its audit: positive sampling, not signed samples.
- ROOT_NOISE_POTENTIAL_EVALUATION.md: explicit polynomial coefficient computation.
- BACKWARD_NOISE_PRECOMPENSATION_GATE.md: strongest inspected prior machinery and fair resource comparison.
- ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md and recursive_initialization/: prior accepted actual-code representation and portable checks.

## Decisive next barrier, preserved separately
quantum_reachability/ contains a separately reviewed operator-polymer positivity result for a weakly noncommuting quantum Gibbs inverse-noise state, plus independent accessible/inaccessible-bath constructions and limitations. A positive state is not a preparation algorithm. Generic noncommuting loading remains open.

The conserved-sector reference note removes an unnecessary canonical reweighting requirement only when its stated conditional preparation is earned. Benign stabilizer-only bath coupling is explicitly not a substitute for damaging interactions.

## Executable checks
Run scripts from their own directories. NumPy/SciPy and mpmath are needed for numerical tests; combinatorial fixtures use standard Python.
- test_calibrated_terminal_inverse.py: inverse/forward and every-prefix identities on the2048 valid syndromes of an actual19-qubit RX fixture.
- test_calibrated_inverse_highprecision.py:80-digit confirmation of positive and genuinely negative regimes.
- test_positive_preimage_chain.py: exact positive trace-chain detailed balance, potential-rate identity, finite stationary distribution and numerical spectral check. No asymptotic gap is inferred from this small fixture.
- Additional independent quantum matrix-gas tests are included with their receipts.

Portable helper copies are included. No source-paper body or figure is redistributed. The source code family and conventional polymer algorithms belong to their cited authors.

No practical memory, favourable hardware threshold, laboratory validation, peer review, exhaustive novelty or civilisation-level breakthrough is claimed. The goal remains physically usable reliable quantum information, not accumulation of conditional coverage.
