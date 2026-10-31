ASTRA: COMPUTATIONAL KNOWLEDGE FROM IMPERFECT EXPERIMENTS
31 October 2026

START HERE

Scientific conclusion
---------------------

Imperfect full-vector experiments can acquire a reusable, certifying solver
whose total correction work is finite across an arbitrary future request stream.
The useful structural quantity can remain small under generic full-rank
perturbations even when exact generated algebra becomes large.

The completed theorem couples experimental precision, the time at which the
task becomes known, approximate spectral structure, and the paid cost of
reliable answers. It is not a new generic online-learning principle. Its
least-change numerical components have strong predecessors; the ordinary PSB
implementation slightly wins the controlled comparison.

A fixed-accuracy source-free compiler faces a sharply different information
problem. Even condition-number-two sources of algebra dimension two can require
exponentially many task-blind actions under calibrated, possibly nonlinear
action error. A separate precision-price theorem quantifies one way to avoid
that obstruction. This distinction is earned without unstable inverses.

What is proved
--------------

1. A reliable service for adaptively requested systems
       (sum_j theta_j A_j)x=b,
   where theta is in the simplex, known mu I<=A_j<=L I, and each original
   action has norm error at most eta times the input norm.

2. Against every unknown comparator C_j within operator error zeta of A_j,
   total individual halfspace corrections obey
       U <= sum_j ||C_j-alpha_j I||_F^2 /
              [(tau-eta)(tau-eta-2zeta)]
   when zeta<(tau-eta)/2. No comparator, basis or rank is given to the learner.

3. Accepted solutions have relative error at most
       (a+eta)/(mu-a-eta),
   where a is the measured normalized candidate defect. Every returned answer
   is checked. For T requests and p optional single-generator directed probes
   per failing request, original action work is at most kT+(k+p)U.
   Vector work, basis storage and small dense solves are also charged.

4. A fixed-source obstruction, valid for real or complex adaptive probes:
   offline uniform inverse service or one promised positive trace can require
   exp[Omega(N eta^2/beta^2)] original actions, even with unlimited local work.
   If an accuracy-eta action costs eta^(-p), promised spike detection has
   precision-work dimension dependence Theta(N^(p/2)) at fixed confidence.
   The upper bound is for detection, not offline inverse reconstruction.

5. A separate offline construction learns a certified spectral decision
   envelope over a fixed low-dimensional control polytope. Subsequent
   resource-constrained design queries reduce to explicit linear programs.
   Under general bounded per-query error it pays for very fine acquisition
   precision; its practical experiment uses a different coherent-error model.

The full main proof is MAIN_PROOF.txt. The strongest controlled comparison is
../robust_solver/CONVENTIONAL_COMPARISON.txt, not the earlier adaptive-task
fixture. RESULTS.txt gives the compact evidence and important useful failures.
SOURCES.txt records the relevant governing and primary sources.

Program and proof map
---------------------

robust_computation/
  MAIN_PROOF.txt             Central service and access theorem; paid costs.
  demand_solver.py          Aggregate halfspace prototype; acquired basis.
  check_demand_solver.py    Adaptive-task mechanism checks, not a fair benchmark.
  demand_solver_results.json
  CENTRAL_AUDIT.txt         Independent mathematical/implementation review.
  README.txt, RESULTS.txt, SOURCES.txt

robust_solver/
  NOISY_OFFLINE_OBSTRUCTION.txt
                            Real/complex lower bounds and precision price.
  compare_conventional.py  Identical-task halfspace/PSB/BFGS/CG comparison;
                            individual responses and directed probes retained.
  conventional_comparison_results.json
  CONVENTIONAL_COMPARISON.txt
  check_masking_obstruction.py, masking_obstruction_results.json

stable_algebra/
  HALFSPACE_CORRECTION.txt, check_halfspace_exact.py, halfspace_exact_results.json
                            Exact rational potential/clipping fixture.
  SAFE_AMPLIFICATION.txt, check_safe_amplification.py, safe_amplification_results.json
                            Three-action rank-one result with full-rank tails.
  HIGHER_RANK_FAILURE.txt, check_higher_rank_failure.py, higher_rank_failure_results.json
                            Why bounded column errors can accumulate as sqrt(r).
  NOISY_SECANT_BALL.txt, RESIDUAL_AMPLIFICATION.txt, check_components.py,
  component_checks.json     Supporting constructions and discarded routes.
  SPECTRAL_ENVELOPE_AUDIT.txt
                            Independent audit of the offline supplement.

operational_learning/
  theorem.md                Full offline envelope construction and source costs.
  spectral_envelope_demo.py Large-state, two-control numerical demonstration.
  results_n1024.json, results_n32768.json, results.json, envelope_demo*.png
  audit_demand_solver.py, central_audit_results.json
                            Independent complex-source checks of main solver.
  useful_failures.py, useful_failures.json, README.md

Reproduction
------------

Run commands from the directory containing these four folders. The environment
used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib. No external data
or hidden pretrained model is required.

  OPENBLAS_NUM_THREADS=1 python robust_computation/check_demand_solver.py
  OPENBLAS_NUM_THREADS=1 python robust_solver/compare_conventional.py
  OPENBLAS_NUM_THREADS=1 python operational_learning/audit_demand_solver.py
  python robust_solver/check_masking_obstruction.py
  python stable_algebra/check_halfspace_exact.py
  OPENBLAS_NUM_THREADS=1 python stable_algebra/check_safe_amplification.py
  OPENBLAS_NUM_THREADS=1 python stable_algebra/check_higher_rank_failure.py
  OPENBLAS_NUM_THREADS=1 python stable_algebra/check_components.py
  python operational_learning/useful_failures.py

The larger envelope demonstration is optional and takes substantially longer:

  OPENBLAS_NUM_THREADS=1 python operational_learning/spectral_envelope_demo.py --n 32768

Scripts write result files beside their source. Numerical timings are not
controlled performance claims. The exact rational fixture uses Python's
standard-library fractions and is separate from NumPy's empirical checks.

Implementation and scope
------------------------

The main code defaults to no arbitrary update cap. A caller may set an explicit
lifetime max_updates cap; this can stop the computation before the theorem's
finite bound has been exhausted.

The source error bound and spectral interval are input contracts. The program
does not infer them from repeatability or a few successful responses. The
proof is exact local arithmetic with a separately specified sufficient
finite-precision budget. The NumPy implementation is not outward-rounded
certified software, and no complete finite-bit runtime theorem is claimed.

Full-vector actions remain stronger access than passive observations. The
exponential obstruction uses query-dependent norm-bounded error and must not
be transferred to independent unbiased noise or one fixed linear perturbation.
The lower-bound fixture has an ordinary one-action inverse formula after b
arrives; it is not an example on which the acquired solver beats ordinary
numerical analysis.

The PSB comparison earns the same kind of lifetime contract with a more
conservative noise margin. Therefore neither halfspace novelty nor practical
superiority is claimed. This package preserves a concrete service/access result
and a separate compiled design construction; it does not claim the portfolio's
civilisation-changing objective has been achieved.

Astra continuity
----------------

The user-supplied exact compiler is accepted at its stated scope and was not
re-audited or imported as an oracle. The governing older corpus is pinned at
cb87e72296824ae2a677ccd337025d02d20cbb0a. This is a separate new research record.
No integration, publication or repository changes are included.

