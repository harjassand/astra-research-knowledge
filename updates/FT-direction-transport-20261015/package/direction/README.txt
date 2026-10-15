ASTRA Direction-Field Audit — 15 October 2026

Read DIRECTION_REDUCTION_LIMITS.md first.
Run: python verify_direction_obstruction.py
Dependencies: Python 3, SymPy.

Main mathematical state:
- Fixed-direction amplitude convexity and Picone inequality survive audit.
- Global amplitude elimination leaves an explicitly nonconvex phase objective.
- Global radial optimality across translated centers equals Euler-Lagrange
  stationarity for the unconstrained radial comparison.
- Fully minimized small-direction charts converge quantitatively to arbitrary
  Cartesian single-output minimization of the original affine-boundary problem.
- Fixed fourth mass converges to a scalar mean constraint, not positivity.

No complete quasiconvexity theorem or negative compatible quasiconvexity test
was obtained. The exact negative tests concern reduced convexity only.

verification.json records 12 finite algebra groups. audit/ contains a copy and
successful replay of the previous 10-group verifier. Analytic claims are proved
in the note, not established by those finite checks. No external validation,
formal proof, novelty clearance, or numerical optimization advantage is claimed.
