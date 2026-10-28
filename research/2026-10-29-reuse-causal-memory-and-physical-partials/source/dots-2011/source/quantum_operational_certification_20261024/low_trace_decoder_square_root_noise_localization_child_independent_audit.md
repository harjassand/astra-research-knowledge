# Independent deterministic square-root-noise localization audit

27 October2026. PASS, local post-cutoff, exact orthogonal-reset source only.

I checked the four-block nuclear-norm proof without imposing rank F<=r. With P the true rank<=r Bell projector and A block diagonal, l1+l2<=2L follows from A<=2|H| on its positive/negative spectral blocks. Factorizing the diagonal blocks through(I-F11)^1/2 and F22^1/2 gives nuclear norms<=sqrt(r l1) and sqrt(r l2), using their trace bounds. For off-diagonal blocks, their rank is bounded by rankP, and F^2<=F gives the stated positive block inequalities. Weighted Hilbert-Schmidt norms are bounded by l1/l2. Summing all four embedded blocks gives2sqrt(r)(sqrt(l1)+sqrt(l2))<=4sqrt(rL).

Variational optimality against P pairs the square-root noise with D A^1/2, costing8z sqrt(rL), and the residual with||D||1<=TrF+TrP<=2r. Young's inequality then yields64rz^2+4rb; additive objective tolerance contributes2delta. No unknown A or noise decomposition is required operationally.

For G<=c(A+tI), Douglas factorization gives sqrtG=(A+tI)^1/2 K with||K||<=sqrtc. Since the scalar functional-calculus difference||(A+tI)^1/2-A^1/2||<=sqrtt, choosing Z=K E0 and retaining its adjoint correctly handles noncommutation. Residual norm is at most2sqrt(ct)epsilon. The final64cr epsilon^2+8r sqrt(ct)epsilon bound follows. Exact-source commutation and domination are essential; no overlapping-reset localization is inferred.
