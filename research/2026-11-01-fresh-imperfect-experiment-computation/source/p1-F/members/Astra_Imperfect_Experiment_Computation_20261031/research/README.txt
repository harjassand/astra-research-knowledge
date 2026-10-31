Astra_Imperfect_Experiment_Computation_20261031

Start with research/RESULTS.txt for the scientific conclusion and comparisons.

Main construction
  research/PROOF.txt
    Complete contract, algorithm, soundness proof, lifetime width bound,
    source/precision/arithmetic costs, finite-preparation variant, original
    Hermitian-source adapter and downstream convex consumer.
  research/INHERITED_SCOPE.txt
    Exact-algebra capital and failures preserved as supplied; original link.

Main executable checks
  task_solver_experiments/noisy_galerkin_benchmark.py
  task_solver_experiments/benchmark_results.json
  task_solver_experiments/check_affine_noncommuting.py
  task_solver_experiments/affine_noncommuting_results.json
  task_solver_experiments/README.md
    Six equally informed comparison policies, late task and tightened-accuracy
    challenge, plus the two-primitive adaptive noncommuting extension.

Information lower bound and convex design
  foundations_agent/precision_observability.md
  foundations_agent/check_precision_observability.py
  foundations_agent/precision_observability_results.json
  foundations_agent/convex_design_and_finite_arithmetic.md
  foundations_agent/check_convex_design.py
  foundations_agent/convex_design_results.json

Complementary construction and shared-context proof review
  robust_solver_agent/RESULT.md
  robust_solver_agent/variable_precision.py
  robust_solver_agent/results.json
  robust_solver_agent/ROOT_THEOREM_REVIEW.md
  robust_solver_agent/LIVE_CACHE_REVIEW.md

Competing passive/dissipative route, proofs and failures
  alternative_agent/PROOFS_AND_COMPARISONS.md
  alternative_agent/check_dissipative.py
  alternative_agent/check_results.json

Reproduction from the extracted package root (Python with numpy and scipy):

  python3 task_solver_experiments/noisy_galerkin_benchmark.py
  python3 task_solver_experiments/check_affine_noncommuting.py
  python3 foundations_agent/check_precision_observability.py
  python3 foundations_agent/check_convex_design.py
  python3 robust_solver_agent/variable_precision.py --output robust_solver_agent/results.json
  python3 alternative_agent/check_dissipative.py

Scripts regenerate their result JSON files. Dense exact solves/eigenspectra used
for reference checks are excluded from learner decisions and source counts,
but these checker runtimes must not be presented as learner timing measurements.

Claims are scoped in the proofs. No practical superiority, physical device,
formal floating-point proof, external independent review or historical priority
is asserted. No repository integration or publication was performed.
