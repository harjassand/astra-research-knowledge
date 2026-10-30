ASTRA P1: EARLY INFORMATION AS A DESCRIPTION OF THE REMAINING EXPERIMENT
30 October 2026 UTC

START HERE

p1_information_as_control.pdf is the consolidated report with ordinary proofs,
the concrete final-accuracy comparison, full cost distinctions, construction,
discovery obstruction, useful failures, sources and claim status. Its LaTeX
source is included. CONTROL_AND_EARLY_INFORMATION.txt is the text-first proof
and synthesis. The subdirectories contain independent constructive work and
audits, not replacement versions of the preceding campaigns.

STRONGEST RESULTS

1. Exact equality between arbitrary interactive finite-control Gaussian linear
   sensing and static finite codebooks of precision matrices. It requires
   hard read/control budgets, all informative control distinctions counted,
   and a final predictor retaining the coefficient/first-stage record.
2. A general early-information decomposition into irreducible conditional
   uncertainty and the distributional cost of describing the residual task.
3. A Hermite family where r+1 two-round reads attain final noisy accuracy that
   every fixed arbitrary mixed linear experiment needs Omega(M) reads to
   match, M=binom(r+p-1,p). Finite control is explicit for the cubic family.
4. Actual coefficient acquisition in a declared layout, packed context/output
   messages, packed finite rational actuator patterns, and charged dense work.
5. An NP-hard cubic global-affine-direction recognition problem with an
   inverse-polynomial gap, plus explicit sparse algebraic fixtures.

In the normalized r=128 cubic example, 129 noisy reads, 1408 remote control
bits, 165120 local pattern bits and a 16-bit final ADC achieve MSE<=.029971311.
Every fixed 129-read linear experiment has MSE>=.9535891089. At least 2697 fixed
reads are necessary for MSE<=.03 by the bound; that count is not claimed
sufficient or an exact optimum. Full 8384-coordinate noisy observation is a
separate sufficient benchmark.

WHAT IS NOT CLAIMED

The local pattern still contains M weights and costs O(M) generation and
projection work. A direct native target/function-value service ties the ideal
conditional operation. No sensor is physically built; Gaussian inputs and
read noise are model assumptions. The declared feature layout is not learned.
The precision of synthetic calibration calls is supplied and explicitly paid.
No runtime or deployment advantage over equally informed ordinary methods is
established. The codebook equality does not efficiently optimize an exponential
codebook. Historical priority remains unresolved, especially Jackowski 1991.

MAIN FILES

CONTROL_AND_EARLY_INFORMATION.txt : root ordinary main proof and synthesis.
finite_precision.py / finite_precision_results.json : packed first context and
  final ADC, exact Gaussian-bin risk identity and executed acquired-model run.
finite_actuator.py / finite_actuator_results.json : 20-bit dense local program,
  rational power-cap checks, actual bit packing and executed finite-pattern run.
learning/hermite_control_theorem.md : family, full fixed/noisy proof and costs.
learning/learn_quantized_cubic.py : actual known-layout coefficient acquisition.
learning/learned_cubic_model.npz : acquired r64 model (2080 float64 coefficients).
learning/check_hermite_fixed.py : tensor and independent quadrature checks.
learning/cubic_structure_hardness.md : full reduction and polynomial gap.
learning/check_cubic_hardness.py : exact algebra, assignments and sparse cubic.
control/ : exact control geometry, noisy audit, expected-prefix audit, finite
  actuator audit, prior challenge and classical quantization comparisons.
computation/NOISY_CONTROL_AUDIT.txt : second independent noisy/J0 audit.
computation/model_adequacy_boundary.txt : L2 robustness and a paid holdout route
  under a supplied residual moment bound, not a model-membership certificate.
computation/POSTERIOR_CONVEXIFICATION.txt : complete alternative attack and its
  ordinary spectral tie / enormous elementary normalization-budget failure.
SOURCE_LEDGER.txt : root and agent primary reads, Astra pin, failed access,
  unresolved overlap and claim boundaries; no external paper bytes bundled.
PREVIOUS_HANDOFF.txt / PRESERVATION_CHECK.json : earlier state and hash check.

REPLAY

Python3, NumPy and SciPy are required. No network, API credentials, paid model,
external service or external repository mutation is used by the research code.

Run:
  python3 replay.py --output /absolute/path/to/a/new/replay-directory

The runner creates an isolated copy of the Python sources and retained model,
then runs the numerical checks and acquired pipeline in dependency order. It
does not rewrite this delivered evidence or the previous campaign directories.
Its logs and replay_summary.json are written to the supplied new directory.
Use --include-posterior-sampling to reproduce the companion's already recorded
747,968 scalar-value sampling calls as well; the default repeats its calibration
and frame checks without that optional kernel execution. Its enormous general
normalizer budget is a calculation, never an executed request.

The report's proof does not depend on a replay obtaining a particular Monte
Carlo mean. Stochastic seeds are fixed for reproducibility; reported standard
errors and analytic bounds are separate. Timings can change and are not used
as speedup evidence. Full dense inputs and true targets are generated only by
the software source/scorer for numerical validation; their cost is not hidden
inside the deployment observation budget.

To rebuild the PDF, run pdflatex twice on p1_information_as_control.tex.
MANIFEST.json lists the authored files, byte counts and SHA-256 hashes. Build
intermediates, bytecode caches, external paper bodies and temporary transfer
helpers are excluded. Capital integration is deliberately separate.
