# Combinatorial primitive pass, 2026-10-10

**Closed without an affirmative general theorem.** No logarithmic loss was eliminated.

`RESULT.md` gives the exact fold-and-prune operator, a locally irreducible family with `exp(Theta(w^2))` alphabet box but only `exp(O(w))` rows, a simultaneous surgery retaining more than two-thirds of its rows, an exact factor-three adaptive-erasure gate, and a proof that a prescribed coordinate can require unbounded pruning loss.

The key distinction is prescribed versus adaptively chosen coordinates. The negative result leaves adaptive erasure open; a constant-retention adaptive theorem would itself settle an exponential sunflower bound. No adequate adaptive potential was found, so this mechanism is closed rather than advertised as a breakthrough.

Files:
- `RESULT.md`: constructions, proofs, precise limitations.
- `PRIMARY_SOURCES.md`: selective primary-source check and unverified newer claims.
- `check_folds.py`, `fold_checks.json`: exact irreducibility and simultaneous-surgery checks.
- `check_projection_embedding.py`, `projection_checks.json`: exact hypergraph representation checks.
- `verify_erasure_certificate.py`, `erasure_certificate.json`: standard-library verification of the twelve-row erasure certificate.
- `test_erasure.py`, `erasure_results.json`: exploratory integer optimization with solver status recorded.

All three standard-library verifiers pass. The alphabet-five ambient optimization timed out without proving its found family maximal; that claim is neither needed nor made.
