# Exact-check canonicalization correction

28 October 2026. The first deterministic check run stopped before writing a result JSON at `assert c==c.H` for the rational Hessian's whitening matrix. SymPy had retained algebraically equal complex expressions in different forms. This was a STRUCTURAL equality test without canonical simplification, not evidence of a non-Hermitian mathematical Hessian or an accepted failed PSD certificate.

The first script is preserved unchanged as `prequential_small_loss_rational_bandit_check_20261028_pre_canonical_simplification.py`. The only repair was to apply exact `sympy.simplify` to each trace in `grad` and `hess` before structural equality/PSD tests. The second run passed all rational certificates and wrote the result JSON. No source observations, RNG outcomes, threshold adjustments, scientific parameter changes, or theorem-source changes were made.

The six proximal candidates use eight floating Newton iterations only as proposals, followed by rounding to a fixed dyadic grid and EXACT rational PSD/TP, local-radius, and tangent-gradient-residual checks. Their success is not a production weak-solver execution, a polynomial-time benchmark, or a learner performance trial. All reported acquisition/source calls remain zero.
