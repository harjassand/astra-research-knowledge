# Reduced energy-moment SDP: exploratory benchmark

## What was tested

Restrict the local divergence Y in Rai's gap SDP to the span of h_i, h_i^2, and {h_i,h_j}. For projector interactions, h_i^2=h_i. This is a polynomial-coefficient restriction of existing quadratic gap certificates, not a new positivity principle. The physical PSD cone remains exponentially large. See ../REDUCED_HIERARCHY_PRIOR_ART.md for close Cruz et al. 2022 and Rai antecedents.

For AKLT, the resulting real symmetric problem uses 4, 7, and 11 scalar variables including delta at levels n=4,5,6. A general real-symmetric full Y would use 378, 3321, and 29646 coordinates respectively, before exploiting SU(2), reflection, other symmetries, or ground-space reduction. This raw parameter comparison is not a measured speedup against the strongest implementation.

## Results

All values below are floating-point exploratory optima, **not rigorous gap certificates**.

- n=4: reduced about 0.282108; Knabe 0.173434. Eigenvector-exchange solve 0.293 seconds, 47 iterations, 62828 KiB peak RSS.
- n=5: reduced about 0.341787; Knabe 0.217653. Exchange solve 5.41 seconds, 400 iterations, 81336 KiB peak RSS.
- n=6: reduced about 0.345553; Knabe 0.248064. Exchange solve 59.54 seconds, 400 iterations, 265164 KiB peak RSS.

The n=5,6 runs reached the iteration cap because default HiGHS feasibility tolerances caused repeated nearly identical cuts. The final exploratory primal-mixture and box-LP objective gaps were about 8.5e-7 and 1.2e-7 respectively. These are numerical diagnostics, not validated rigorous brackets. Coefficient bounds were +/-100; observed coefficients stayed below 0.91. The final candidate's lowest complementary eigenvalues were around -8.3e-8 and -1.1e-8 before the positive-witness mixture. This is why the outputs must not be called certified gaps.

An independent Clarabel solve at n=4 gave 0.282107965 with status AlmostSolved and minimum complementary eigenvalue 8.6e-9, agreeing with the exchange result. It took 37.66 seconds and 273032 KiB peak RSS. This comparison demonstrates solver sensitivity within the reduced formulation; it is not a speed comparison against Rai's full SDP.

## Strongest directly relevant prior

Rai et al. already report a **certified** AKLT bound 0.34976 at n=6, compared with finite periodic n=12 gap about 0.35012. The present reduced n=6 value is weaker by about 0.00421, or 1.2%. No improved physical gap estimate, matched-budget runtime advantage, or broad practical leap was established.

Rozman–Molnar–Schuch report an AKLT periodic lower bound 0.2827 using their improved martingale machinery. Their method is a different resource tradeoff and was not rerun here.

## Algorithms and resources

- benchmark.py: Clarabel 0.11.1, real PSD cone, exact known-ground-space removal done numerically, coordinate orthogonalization. Clarabel was installed from PyPI into /tmp/lti_solver using a 1.2 MB wheel; no dependency upgrade was made.
- exchange.py: SciPy HiGHS LP relaxation with eigenvector separating cuts; no additional solver package required. A strictly positive-on-the-complement quadratic witness at delta=-1 is used to turn the eigenvalue violation into a numerical feasible mixture.
- No interval arithmetic or exact rational PSD certificate was produced.
- No full/projected-Y SDP was independently solved at equal time/memory budgets, and no nonprojector/deformed near-critical model was benchmarked.

To reproduce the exchange runs, use Python with NumPy and SciPy:

    OPENBLAS_NUM_THREADS=1 python exchange.py

The Clarabel comparison additionally needs Clarabel 0.11.1 importable. The script currently checks /tmp/lti_solver before the ordinary Python path.

The mathematical convergence consequence is potentially useful even if this first benchmark is not a practical breakthrough. Its novelty and significance require external review.
