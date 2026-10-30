ASTRA P1: ONE FEEDBACK ROUND FOR QUADRATIC MEASUREMENT
Research construction completed 31 October 2026, Australia/Brisbane.

START HERE
p1_two_round_measurement.pdf is the consolidated research note, with ordinary
proofs, conditions, cost accounting, executed results and primary comparisons.
p1_two_round_measurement.tex is its editable source.

The main capability is an explicit two-round linear-measurement policy for a
known quadratic target under a known Gaussian input law. With at most k+1
exact scalar reads, it has risk no greater than any fully adaptive k-read
policy. Signed spectral compression gives a policy-independent lower bound;
one final outcome-dependent linear read captures the residual linear term.
No comparator policy is supplied or searched. The real expected-budget
version spends at most k+1 reads in expectation, not as a hard integer bound.

A separate all-noisy theorem proves a concrete accuracy separation against
the strongest fixed designs. For F=U^T V/sqrt(128), unit directions and IID
Gaussian readout noise of variance .01, 129 reads in two rounds give risk
.0197039506. Optimal fixed 129-read risk is .5060226939, including repeated,
nonorthogonal and mixed-block directions; 256 fixed reads match the adaptive
risk. The fixed-optimum proof here requires noise variance at most one and
fixed read count at most the latent dimension. The general exact-adaptive
comparison is not silently extended to noisy adaptive competitors.

STATUS
These statements were internally derived, independently reconstructed, and
checked through finite exact calculations, Gaussian quadrature and synthetic
executions. Historical priority, external peer review, a real sensing-device
advantage and total runtime dominance have not been established. Classical
linear information complexity, multilinear problems, spectral approximation,
adaptive sensing, group energy search and junta learning are material prior
work. Source access and unresolved overlaps are recorded explicitly.

RUN THE EVIDENCE
Use Python >=3.10 and NumPy; no network, credentials or external data are used.
From the extracted evidence directory run:
  python3 run_checks.py
Do not use Python -O: assertions implement the finite checks.
The runner executes six scripts, captures stdout/stderr, records versions,
hashes each script and writes replay/replay_receipt.json. The retained full
replay passed all six scripts. Its wall time is finite-check time, not a
scientific or deployment performance advantage.

CODE AND PROOF MAP
two_round_quadratic.py
  Actual scalar model acquisition, spectral plan construction and a sensor
  interface which counts every unit-direction linear read. The predictor
  reads only through the sensor. Validation and source generation inspect
  latent values separately, outside the restricted prediction algorithm.
  Executes a bounded-error unknown dense 32-dimensional model and a separate
  normalized 256-dimensional all-noisy comparison. Floating arithmetic;
  supplied model/noise contracts and numerical residuals are explicit.
two_round_results.json
  Counts, numerical residuals, model error, measured risks, standard errors
  and wall times. Source acquisition, observations and dense coordinate work
  are all charged. Monte Carlo agreement is a diagnostic, not a proof.

alternative/gaussian_quadratic_audit.md
  Independent reconstruction of the adaptive Gaussian transcript, signed
  spectral lower bound, two-round theorem, exact hard-query inertia theorem
  and a same-budget threshold policy that beats the simple compiler.
alternative/noisy_uv_audit.md
  Independent all-noisy inner-product proof, optimal fixed-design comparison,
  high-noise repeated-measurement counterexample and general QAQ=0 formula.
alternative/model_robustness_audit.md
  Acquired-model transfer, scalar interpolation precision, numerical direction
  certificates and a stencil-blind higher-order counterexample. An optional
  sharper interpolation constant is retained here without promoting it into
  the central consequence.
alternative/check_*.py and corresponding *_results.json
  Finite Gaussian quadrature, projection/interlacing checks, exact rational
  coefficient-error vertices and noise/gradient certificates.

feedback/feedback_theorem.txt and feedback/feedback_checks.py
  A coordinate-only companion: reveal an interaction vertex cover, then the
  largest conditional additive variances. It uses |H|+k reads in two rounds
  and dominates every original hard-k policy. Includes exact rare-gate
  allocation comparisons, a graph-acquisition construction, and the failure
  of substituting an unconditional expected budget for a hard continuation
  budget. Its separately priced expected-budget extension is retained.
feedback/central_independent_audit.txt
  A second independent reconstruction and scope review of the central
  Gaussian, signed-spectrum, inertia and noisy-fixed claims.

acquisition/PROOF.txt, STATUS.txt and group_acquisition.py
  An exact Boolean quadratic source-acquisition companion. Four actual scalar
  values construct additive nonnegative group influence and coverage-risk
  estimators. A paid splitting tree acquires a predictor competitive with
  the informed expected-budget adaptive optimum. This is not a Gaussian
  unknown-spectrum acquisition theorem. The full small fixture paid
  1,140,791 calls, versus 137 for ordinary interpolation: a useful efficiency
  failure, explicitly preserved. A noisy group-estimation theorem is proved;
  a noisy end-to-end pure multiplicative risk theorem is not claimed.
acquisition/central_prior_check.txt
  Focused primary-source investigation of the closest older multilinear and
  nonlinear Gaussian information-complexity work, including access gaps.

PREVIOUS_HANDOFF.txt
  Compact factual handoff for the prior fixed-coordinate theorem, sharper
  quadratic bound, rare-concentration lower bound and acquisition/audit work.
  Prior deliverables remain separate and unchanged.
SOURCE_LEDGER.txt
  Pinned Astra navigation, governing source scope, primary URLs and the
  distinction between read sources and access failures.
MANIFEST.json
  SHA-256 hashes of authored delivered files, excluding the manifest itself
  and the enclosing ZIP. These are integrity receipts, not validity proofs.

LIMITS THAT MUST TRAVEL WITH THE CLAIMS
The central exact theorem assumes a known Gaussian law, a known or adequately
acquired quadratic target, arbitrary exact scalar linear measurements, and
Bayesian squared loss. It changes the measurement interface from the previous
coordinate-only theorem. If a dense linear read requires acquiring all raw
coordinates, those acquisitions must be paid. Dense direction construction,
transmission, precision and sensing are not made free by calling the result
one scalar measurement.

Learning a model is distinct from verifying that its class is appropriate.
The interpolation stencil does not detect all higher-order alternatives.
Unknown noise independence, drift, covariance and distributional shape are
not inferred by the synthetic checks. Exact inertia needs certified signs;
approximate risk can use residual certificates without an eigengap. The
floating implementation is not a formal interval arithmetic certificate.

Ordinary fixed eigendirections, full interpolation, a live full evaluator,
standard graph-cover routines and established Fourier/junta learning receive
the same information and are substantive alternatives. Shared preparation
may amortize across inputs; no count alone establishes total cost dominance.

No Astra repository integration or external publication was performed.
Capital integration remains separate. External paper bytes, failed-fetch
pages, caches, and build intermediates are excluded from this evidence bundle.
