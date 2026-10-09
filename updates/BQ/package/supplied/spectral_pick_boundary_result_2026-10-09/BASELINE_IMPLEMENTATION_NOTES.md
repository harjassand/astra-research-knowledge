# Baseline implementation and fair-comparison notes

The primary same-model source is Ying (2025), ACHA 79 101802, https://web.stanford.edu/~lexing/fdc1.pdf , especially section 3.2 and examples 3.1–3.2. It assumes known atom count for finite-N examples and acknowledges nonconvexity of its noise-scale objective. Its coarse-grid plus local-search strategy is implemented here using an own NumPy/SciPy implementation, not downloaded executable author code.

## Eigenmatrix settings

- Input is the same empirical spectrum as the candidate.
- Spectral dictionary interval is the observed [minimum,maximum]; affine-normalize it to [-1,1].
- 32 Chebyshev dictionary points and 64 transform points (32 conjugate pairs) on an observed-scale enclosing ellipse.
- Normalized Cauchy columns, SVD relative cutoff 1e-10, with rank decreased as needed to keep eigenmatrix norm at most 3 (except minimum rank k+1).
- Krylov powers 0,...,k+1, rank-k ESPRIT extraction, real/imaginary least-squares weights.
- Search variance in [0, empirical spectral variance], 61 coarse points. Refine up to five lowest feasible local coarse minima with bounded scalar minimization, x tolerance 1e-9.
- Feasibility filter: weights >=-1e-6, recovered normalized root imaginary parts <=1e-4.
- The reference paper leaves several of these tolerances and counts unspecified. The present implementation has passed exact-data smoke tests, but no author certification or claim of globally optimal numerical tuning is made.

An initial non-enclosing transform line made the eigenmatrix dictionary approximation ill-conditioned; that version failed the exact baseline check and was not used for comparative claims. The enclosing ellipse and shorter admissible Krylov sequence fix the check. This is why a deliberately fragile implementation was not used as a baseline.

## Full nonlinear forward fit

- Fits the complex limiting free-convolution transform, not the exact joint finite-N eigenvalue likelihood.
- Every forward evaluation solves the Pastur fixed point with damping and tight residual tolerance.
- The implicit analytic Jacobian includes derivatives of all atom locations, k-1 softmax weight coordinates and variance; it was independently checked by central finite differences.
- Atom bounds are the observed spectral interval. Variance is in [0, empirical spectral variance]. Logit bounds are +/-12.
- Independent initial noise fractions are .1,.35,.65,.9 of empirical variance. Initial centers use empirical quantiles scaled toward the observed mean, and weights are uniform. An additional candidate warm start is included, with its cost counted.
- SciPy least_squares with ftol, xtol and gtol=1e-12, max_nfev=500. Every convergence status, optimality measure and objective is saved.
- Four starts are not a global optimization certificate. In these tests the same-k fits agree with the algebraic construction; the construction itself supplies the exact theorem's global selection.
- Full multistart timings and retrospectively selected fastest independent successful starts are both recorded. Accuracy improvement from extra transform samples must not be presented as a same-observation comparison.

## Cost boundaries

The data-generation eigendecomposition is shared and excluded from solver timings. Candidate timing includes transform evaluation, initial normalized-PSD validity check, 55 bisection tests and the positive realization. All methods receive known k. No method receives true locations/weights or true noise variance in initialization. The exploratory fixed-geometry results are preserved but superseded for comparisons by the observed-scale matched script.
