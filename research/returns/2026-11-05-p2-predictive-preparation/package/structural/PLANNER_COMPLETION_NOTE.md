# Completed finite robust planner

All files are complete. No second physical deployment is claimed. The retained-source table is the only plant input.

## Main results

- Uniform physical radius for every TV <= 1 candidate: 9692661/100000000 = 0.09692661.
- Certified whole-path band [-0.3, 0.3]; exact primal-dual gap zero; acquired predicted endpoint 0.19886232184661864.
- Two nonzero quintic ramps, duration 1/20, at t=0 and t=1/5; nominal center speed <=15 and rational acceleration bound <=960. Separately charged return duration 1/10.
- Actual selected-programme physical radius 0.08438833166123201; endpoint interval [0.11447399018538665, 0.28325065350785067].
- Exact active-basis region for a future fresh readiness baseline [-0.016431228690490723, 0.1111480752645874]. Same optimal dual, affine primal. Precompute offline, then two comparisons and one nontrivial rational multiply-add. Certified controller latency still must be reserved. Outside this single region, abstain; no conditional-confidence inflation.
- 10 variables, 171 inequalities; 325 response coefficients independently reconstructed; 342 endpoint inequalities verify the full affine region; 700 exact polynomial identity samples and 7,350 exact quadrature boxes verify 100 path segments.
- Construction measured 0.05379776400513947 seconds; not a hard realtime bound. Fallback enumeration 4,505,395,859,893,071 systems is explicitly finite and expensive; theoretical polynomial rational LP alternative is standard.

## Files

- finite_robust_planner_theorem.md: complete theorem, quantifiers, hardware, bit cost, finite optimization, all-time safety, larger-class approximation with paid acceleration, executed result and ordinary-method comparisons.
- finite_robust_planner.py: constructor, exact active-basis recovery/dual repair, finite fallback, parametric baseline region, smooth program and exact path.
- verify_robust_planner.py: independent direct-integration coefficient and exact primal/dual/region verifier.
- verify_robust_planner_path.py: independent Boole-quadrature complete-path verifier.
- robust_planner_certificate.json; robust_planner_program.json; robust_planner_prediction_path.json; robust_planner_verification.json; robust_planner_path_verification.json.

## Provenance and scope

Certificate SHA256: 58a584ef631bf7e079f28084646747d9c533ded2425be271d87fd373ccdd4b56
Path SHA256: 1a273bd6ba9341b4615696d2bf146a2bd339924b15e4374417b9c95b6dcb4dba

This is ordinary step-response predictive optimization and explicit parametric LP joined to the new acquisition/readiness contract, not a new general MPC algorithm. Optimization comparison is only with the declared tightened quintic polytope. No recursive/infinite-horizon safety claim.

Primary source refs for root to open before citing: Cutler-Ramaker original paper https://skoge.folk.ntnu.no/puublications_others/1980_Cutler-Ramaker_Dynamic-matrix-control_JACC1980.pdf (turn278view0); Bemporad-Morari-Dua-Pistikopoulos institutional primary record https://old.control.ee.ethz.ch/publications/2002/12.html (turn278view1).

Earlier sectorial and random-window companion files are unchanged apart from this new planner addition.
