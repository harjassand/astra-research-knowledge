# Independent receiving review of actual logical two-design comparison v9
2026-10-29. Reviewer: review_actual_logical_comparator.

## Disposition
The declared v9 comparison is accepted as a reproducible, conditional-on-one-training-history mathematical fixture. It does not establish hardware performance, training-average yield, historical novelty, or practical superiority after full control and storage costs. The preserved source is unchanged. Additional optimized-weighted and matching comparisons are separate follow-on files, not replacements for v9.

## Actual construction and shared inputs
The program imports exactly the v8 no-reset acquisition/guard fixture. Its fitted frame uses the completed physical-record counters and fixed basis embedding. Both test families use the same learned encoder E, CPTP reset-completed decoder D, final two-dimensional bath state and fixed post-training source U0. The source rule changes at the learning/guard boundary as disclosed in the accepted v8 review; “no reset” is not a claim of unchanged parity-selected source dynamics.

For each of the six logical Pauli eigenstates psi, the test constructs bath Kraus matrices
B = (outket* tensor I) (D_alpha tensor I) U (E psi tensor I) / sqrt(6),
with outket=psi for pass and its normalized orthogonal complement for fail. Summing over every decoder Kraus operator is essential: leakage replacement is included rather than projected away. This is an actual instrument, not a rescaling of a service-error probability. Pass plus fail is trace preserving. For every bath state, the six-state 2-design identity gives the failure effect F=(2/3)W, where W is the nonidentity Pauli service effect. The program checks this full bath-operator identity for U0 and the separately supplied burst unitary, not just one initial bath expectation. The known-generator use of U and sigma is evaluator-only; neither is granted to the physical controller.

The comparator replaces the test CP maps, then executes exactly the same service maps and outer decoder. Its s=0.4, C=1.5 choice gives R=Cs/(1-s)=1, t=6 and b=0, so the prior reviewed accepted-subnormalized soundness bound stays 1/128. The 155 inner services encode 35 payload qubits using the same GF(32) outer code. The cap is500 instead of1400; cap exhaustion aborts and is accounted in both results. Ideal trusted endpoints/private pads and complete role-independent source boundaries remain assumptions.

## Reproduction
The complete author program was rerun, including the million-call learning trajectory and selected outer-ledger decodings. Parsed output equals the preserved JSON exactly. It reproduces six-state acceptance0.9290072246126571, expected373.48934793445227 source calls and accepted >6-fault mass1.765501554839748e-12; 920 of1000 sampled mathematical continuations accept and50 selected nonzero accepted ledgers are actually decoded. The universal1/128 bound comes from the prior theorem, not the tiny simulated tail. The probabilities are floating-point mathematical computations, not interval-certified probabilities or measurements. The trajectories are forks from one conditional bath state, not repeated physical preparation of an unknown bath.

## Scope of the negative comparison
The preserved weighted comparison uses conservative C=6 even though the exact n=4 coefficient is3, as disclosed in v7/v9. Its acceptance0.7757656926028677 and expected957.4809003757346 calls are correct for that declared policy. Thus v9 establishes that the conventional six-state policy wins against that policy; v9 alone is not an optimized comparison against every weighted policy. Follow-on optimized-C=3 results are reported separately.

The deliberate omission of the absolute-call500–511 burst comparison is scientifically appropriate: protocols with different duration would encounter different disturbances, and this would confound a mechanism comparison. Both use the same fixed U0 for the reported comparison.

Full logical testing includes the inner encoder/decoder on each test and can absorb their actual noise in the tested complete logical operation when the same physical operation is used for service. The weighted witness bypasses those operations and must independently budget their errors. Conversely, weighted/matching preparations can reduce test-control complexity. Neither scalar call count establishes a total gate-duration/fidelity winner.

## Independent checks
The associated independent_review.py reconstructs Choi matrices, checks CP and trace preservation, rebuilds bath Kraus operators from the Choi matrices and executes a separate matrix-state, explicit terminal-bucket DP. Its output and a SHA-bound receipt accompany this review. Follow-on matching tests are not used to justify acceptance of v9.
