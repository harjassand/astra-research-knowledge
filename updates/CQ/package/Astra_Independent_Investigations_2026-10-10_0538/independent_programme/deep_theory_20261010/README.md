# Directed-triangle mechanism audit, 2026-10-10

**Outcome: failed mechanism, closed. No CH progress or foundational breakthrough.**

Read `RESULT.md` for the complete construction, proof, preserved failures, and exact scope. The decisive certificate is the triangle-free 52-outregular graph on 160 vertices with stationary mean indegree plus exact second-neighborhood size equal to `104 - 2493/485524`.

Main exact reproductions:

- `verify_combined_counterexample.py`: reconstructs the 64- and 160-vertex 0/1 counterexamples and checks all claims with rational arithmetic.
- `independent_certificate_n160_r52.json`: full adjacency, full rational stationary distribution, and local counts.
- `combined_counterexample_verified.json`: concise exact outputs for outer parameters 1–4.
- `verify_route_obstructions.py`: exact uniform-stationary weighted-kernel obstruction and maximum-stationary-vertex failure.
- `audit/`: separately implemented discovery, symbolic formulas, and exact certificates.
- `PRIMARY_SOURCES.md`: verified primary context and explicit no-priority boundary.
- `EVIDENCE_SHA256.txt`: frozen file hashes after validation.

Heuristic search logs are retained as failed discovery methods. They did not detect the subsequently constructed counterexamples and are not positive evidence for the failed statements.
