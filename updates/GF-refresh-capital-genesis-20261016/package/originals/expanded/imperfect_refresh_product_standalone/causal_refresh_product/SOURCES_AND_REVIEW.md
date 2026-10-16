# Sources and receiving review

## Primary causal theorem

Gus Gutoski and John Watrous, *Toward a General Theory of Quantum Games*, June 22, 2007 version.

Author-hosted source: https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf

Theorem 9: printed page 13, PDF page index 12. This is the maximum-outcome positive domination theorem, with an explicit analogous statement for co-strategies. Proof: printed page 14, PDF page index 13. Theorem 6 and Corollary 7 give the normalized causal trace constraints. Definition 3 and the paragraph following Definition 4 specify dummy one-dimensional message spaces and strategy/co-strategy orientation.

The primary source was opened and the theorem, surrounding definitions, and proof location checked with the web PDF reader on 2026-10-16. No source PDF is redistributed in this packet and no local hash of a downloaded primary PDF is claimed. The explicit tensor derivation and exact-budget Hamiltonian reduction are given in PROOF.md.

## Contextual primary source

Abel Molina and John Watrous, *Hedging bets with correlated quantum strategies*: https://arxiv.org/abs/1104.1140 and author PDF https://cs.uwaterloo.ca/~watrous/Papers/HedgingWithQuantumStrategies.pdf . Its all-pass-versus-hedging distinction is contextual; the proof relies on the multiround theorem above, not on extending a one-round theorem by analogy.

## Mathematical inputs

The sibling joint_refresh_bernstein/PROOF.md supplies the scalar-to-operator sine lemma, with its verified Redheffer primary source, and the singleton/fresh-sink constructions. The sibling staggered_refresh_test/REPORT.md and functional_obstruction_exact.md identify the former open boundary and analytic counterexamples. Their file hashes are recorded in INPUT_SHA256SUMS. They were read, not edited.

## Internal mathematical receiving review

A separate internal mathematical reviewer read the full PROOF.md and independently checked:

- Copy/prover/uncopy/discard preserves the private parities for every prover.
- Desired joint parity-diagonal bath unitaries are implemented losslessly.
- Each single tester retains the exact own-gap Q bound.
- Gutoski–Watrous positive domination tensors after common-round padding.
- Equal-sector padding, contraction decomposition, and integrated-cell Dyson approximation preserve every own-gap budget exactly.

These are internal mathematical checks, not independent external validation or peer review. The reviewer found no substantive gap and requested only the clarifications about one-dimensional dummy messages and tensor-factor orientation; both were incorporated. The parent independently reviewed the complete argument and also found it sound. Fixed/exogenous schedule limits and the stronger all-ever-mismatch version were then made explicit.

## Diagnostics

check_identities.py is newly authored, deterministic Python/NumPy code. It tests identities only; it performs no optimization and imports no acquired project code. It covers two private parity bits, arbitrary joint prover unitary, lossless controlled bath simulation, and contraction decompositions including singular values zero and one. diagnostics.json contains the recorded result. Maximum residual is below 3e-15. These finite examples are checks, not replacements for the analytic proof.

To replay: python check_identities.py .

## Scope

Ideal-model mathematical closure only. Historical novelty, finite-width control realization, experimental performance, scalable hardware feasibility, and physical-fault interpretation are not established. The original functional counterexamples are unaffected.
