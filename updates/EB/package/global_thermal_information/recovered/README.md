# Global thermal information: research packet

Date: 12 October 2026.

## Main mathematical claim
For a canonical family of distinct, nonidentity Pauli strings with support size
at most k and candidate incidence at most Delta per site, and a Hamiltonian with
incident coefficient strength at most g, the manuscript derives

    BKM_covariance(A,A) >= centered_KMS_norm(A)^2
        >= exp[-C_(k,Delta) (1 + beta*g)^2] * sum_a u_a^2,

where A = sum_a u_a P_a. The constant does not depend on n or m. The Gibbs state
is unrestricted on the full qubit tensor product. The incidence condition
includes zero-coefficient candidate terms. The statement does not assume decay
of correlations, commutativity, a spectral gap, or rapid mixing.

The proof reconstructs the previous local spectral-multiplicity lemma. The new
global step constructs Gaussian-filtered gradients with exactly localizable
KMS adjoints, controls the high-frequency residual in coefficient l2 norm, and
bounds the Gram kernel of transformed observables by transferring the exact
adjoint before spatial truncation.

The manuscript also proves that weighted interaction strength without bounded
candidate incidence is insufficient, using a classical star with nonzero
couplings. A fixed-charge projection is not covered by the positive theorem.

## Status
Newly derived mathematical proof; no external review, formal verification,
independent replication, or original-priority certification. The uniform proof
is in the manuscript, not supplied by the finite checks. The targeted prior-art
comparison concerns specified inequalities and does not establish novelty
against all literature. No generic efficient equilibrium-preparation or
classical reconstruction algorithm is claimed. Temperature constants are not
optimized and may be impractical.

## Files
- global_thermal_information.pdf: full proof, counterexample, and consequences.
- global_thermal_information.tex: editable LaTeX source.
- finite_checks.py: reproducible finite algebraic and spectral tests.
- finite_checks.json: actual output of the provided script.

## Reproduce
Requires Python 3.10 or later, NumPy and SciPy:

    python finite_checks.py --output finite_checks.json

To compile the paper, use pdflatex twice on global_thermal_information.tex.
The tests use seed 261012 and perform six algebraic/quadrature instances,
24 covariance-matrix instances, and a sequence of analytic star examples.
The tolerances and diagnostic limitations are in the script and JSON.

## Provenance
Astra repository revision inspected:
3a9880bf4b1913a1b9e522f15414092e57c66eec

openai/math revision appearing in targeted search results:
fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb

No unreviewed repository theorem is assumed, and no repository was modified.
Primary literature references and exact comparison scopes are in the paper.
