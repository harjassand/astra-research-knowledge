ASTRA: CUMULATIVE INTELLIGENCE THROUGH ACQUIRED EXPERIMENT OPERATIONS
31 October 2026

Main result
-----------
PROOF.txt gives the complete finite-noise construction and proof. Scalar return
correlations acquire bounded signed representations of operation successors.
The resulting matrices preserve the coefficient l1 unit ball and support every
later word of length L with error <=L*rho+beta (plus numerical execution error).
No hidden coordinates, useful basis, minimum Gram eigenvalue, representation
oracle, or known rank is required for soundness of a completed certificate.

Finite metric packing gives termination and full expected cost; its general
dimension dependence is exponential. The work does not establish a general
efficiency advantage or historical novelty. Prior invariant-polytope, kernel
conditional-gradient, symbolic-model, spectral-learning and control results
are explicitly credited. The main new bridge is acquisition at the specified
noisy hidden-moment interface, with full reuse and resource accounting.

The strong comparisons are part of the result:
- An ordinary retaining signed-frame learner wins the first noisy fixture.
- An ordinary exact Gram-closure learner discovers a rank-two reflection model
  from 12 short scalar moments; the initial metric cover is much more costly.
- A finite exact l1-stable raw-feature lift may not exist for an irrational
  rotation, although an exact rank-two Euclidean model does.
- The refined convex compiler reduces the initial metric dictionary but can
  trade prediction accuracy for storage; it is not a universal winner.

Files
-----
PROOF.txt                           Full main theorem, costs, derivations, limits.
metric_compiler.py                  Main construction, noisy atomic fixture,
                                    convex diagnostics, cumulative extension.
results.json                        Executed source/computation/error ledgers.
compiled_models.json                Learned finite noisy-fixture programs.
metric_cover_counterfixture.py      Exact rational strong spectral comparison.
metric_cover_counterfixture.md      Counterfixture proof and prior-art notes.
metric_cover_counterfixture_results.json/.csv
                                    Exact acquisition and verification counts.
recovery_access.md                  Separate controller-access theorem and proof.
fresh_opening_check.py/.json        Its small Bayesian-planner numerical comparison.
convex_closure_review.md            Internal shared-construction proof review.
metric_review.md                    Initial metric theorem and expected work.
adjoint_gram_conditioning_challenge.md
                                    Failed broader polynomial-acquisition attacks.
source_conditions.md               Pinned Astra conditions and read scope.
literature.md                       Complementary primary-research notes.
SOURCES.txt                         Governing source links and credited methods.
MANIFEST.json                       File identities, sizes, SHA-256 checksums.

Reproduction
------------
Main and recovery programs: Python 3 with numpy. Executed with Python 3.12.14
and numpy 2.3.5. The rational reflection checker uses the standard library.

    python3 metric_compiler.py
    python3 metric_cover_counterfixture.py
    python3 fresh_opening_check.py

The scripts write their corresponding JSON/CSV outputs in their own directory.
Elapsed CPU seconds can change on rerun. Source experiment counts are explicit.
No network, external services, installation, source credentials or private
research database are needed to run these supplied simulations/checks.

Evidence scope
--------------
The noisy signed-orbit experiment samples exact binomial aggregate counts from
the source's endpoint-product law. The ledger charges every simulated physical
primitive, preparation and readout; this is not a hardware experiment. The
generic convex and incremental-intervention executions use exact-moment
numerical fixtures. The full finite-noise generic theorem is analytical and
internally reconstructed; a production interval-arithmetic implementation and
useful noisy real-system advantage are not established.

The recovery comparison uses a finite Bayesian state model and floating-point
value iteration. Its small residual is a numerical diagnostic, not a certified
rational optimum. The upper/lower recovery cost theorems have ordinary proofs.

The original parity handoff and older Astra results remain separate capital.
No repository publication or integration was performed by this research run.
