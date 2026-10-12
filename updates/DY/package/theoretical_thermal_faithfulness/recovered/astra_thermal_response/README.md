# ASTRA: local thermal faithfulness from bounded coupling

Date: 12 October 2026. This is a generated research packet, not a published repository update.

## Contents

- `thermal_response.pdf`: nine-page research note with self-contained proofs, current comparators, limitations and exact counterexamples.
- `thermal_response.tex`: editable mathematical source.
- `check_bounds.py`: reproducible floating-point falsification checks. Run `python check_bounds.py --output checks.json` with Python 3.10+, NumPy and SciPy.
- `checks.json`: actual results from the supplied script (seed 19371; 300 random instances plus an explicit counterexample family).
- `manifest.json`: content hashes, repository revisions, and claim status.

## Mathematical contract

All Hilbert spaces are finite-dimensional. The Hamiltonian is
`H = I_S tensor K + V`, where `dim(S)=d`, `K` is an arbitrary bath Hamiltonian,
`V` is Hermitian, and `||V||op <= v`. All subsystem-only terms belong in V.
The input state is the exact Gibbs state at beta > 0.

For every local operator `X=x tensor I`, not necessarily Hermitian,

`Tr(sqrt(rho) X* sqrt(rho) X) >= 4 exp(-4 beta v) ||x||op^2 / (9d)`.

The part of this quadratic form with energy differences at most `7v` is at least
`exp(-5 beta v) ||x||op^2 / (72d)`.

A singular-value-profile generalization and a conditional local-field inverse theorem are included. A fully explicit family disproves a subsystem-dimension-independent comparison with normalized local Hilbert--Schmidt norm, even for traceless Hermitian operators.

## Evidence status

The finite-dimensional proofs are supplied in full. The programmed numerical checks passed within their declared floating-point tolerances. These checks are neither a mathematical proof nor independent verification.

Original priority, external proof review, and independently major foundational significance have not been established. The output does not claim a global many-body covariance tensorization theorem, efficient evaluation of the partition function, efficient Gibbs-state preparation, rapid mixing, or an end-to-end technological advantage. The finite-band statement permits zero-frequency weight and is not a lower bound on transport or dissipative absorption.

## Prior-work scope

The direct faithfulness comparators are Chen--Anshu--Nguyen, arXiv:2504.02706v1, Lemma III.6, and Bergamaschi, arXiv:2610.01074v1, Lemma 3.6. The latter was inspected including the rendered PDF page. Both display temperature dependences with beta log(beta) in the exponent at fixed local support/degree; the supplied bounded-coupling estimate has a linear beta exponent. This is a comparison of specified inequalities, not a comprehensive priority certificate or a proved full-algorithm speedup.

Other checked learning comparators: Bakshi--Liu--Moitra--Tang, arXiv:2310.02243v2; Anshu--Arunachalam--Chen--Hwang, arXiv:2610.02178v1, particularly Appendix D.

Repository snapshots:

- Astra: `3a9880bf4b1913a1b9e522f15414092e57c66eec`.
- OpenAI/math: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` (revision of targeted search results).

No repository theorem is used as a premise. The broader operator-algebra and bounded-perturbation literature has not been exhaustively checked.
