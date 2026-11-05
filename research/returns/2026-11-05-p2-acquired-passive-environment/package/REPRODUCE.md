# Reproducing this construction

The archive preserves both successful constructions and the initial independent
selection attempts. The main operation is described in acquired_passive_environment.md
and its PDF. It is a conditional theorem for the declared physical class, not an
experimental validation of arbitrary real materials.

## Main operation

From this directory, with Python 3.12 and NumPy, SciPy, SymPy, and Matplotlib:

1. Run: python bridge/acquired_passive_bridge.py. This simulates the retained
   physical source, finite trap probes, guard, release, and query paths. It fits
   the measured reports. The last recorded full LP proposal used about 411 MB
   for its constraint matrix and took about 62 seconds. Peak process memory can
   be substantially larger. This simulation is floating point, not an interval
   enclosure of the physical apparatus.
2. Alternatively, add --reuse-fit. This reuses an existing fit only if every new
   rounded report is identical. It then reverifies the model with exact rational
   exponential intervals. This option was used to add the finite release without
   needlessly rerunning an unchanged LP. The default path constructs the full fit.
3. Run: python independent/passive_execution_compiler.py. The adapter consumes
   the actual fitted model and positive bath-force estimate. It explicitly
   fixes the displayed polynomial visible law and B=T=mu=1. It emits a rational
   path and independently verifies its complete within-step residual.
4. Run: python bridge/finite_digitization_receipt.py, followed by
   python bridge/complete_operation_receipt.py. These bind the source and
   path hashes and add finite ADC and drive-delivery budgets.
5. Run: python bridge/plot_bridge.py for the diagnostic figures.

The final exact path hash is recorded in independent/passive_compiler_results.json.
Source receipt hashes change if a replay updates timing fields; rerun the compiler
after a source replay so the complete-operation checker consumes the current hash.
The path hash is invariant when its actual mathematical inputs are unchanged.

The physical source generator and diagnostics can see microscopic fixture modes.
The fitter and compiler do not receive those modes. The learner receives only
rational reports, declared bounds, and the known visible law.

## Proof modules

- forward/passive_FULL_PROOF.md: finite moving-trap and raw finite-box acquisition.
- forward/RELEASE_HANDOFF.md: finite trap release, independent local viscous-support
  drive, error propagation, force, slew, travel, work, and calibration scope.
- independent/passive_positive_fit_theorem.md: finite positive fitting and exact
  output certificate, with a guaranteed finite fallback.
- backward/passive_initialization_and_prediction.md: retained initial-force
  measurement, maximum principle, energy bound, and query quantifiers.
- independent/passive_execution_compiler_theorem.md: finite rational path
  compilation, termination, within-step residual, and digital resource counts.
- backward/passive_extrapolation_companion.md: the alternative initial-force
  continuation construction and its precision costs.
- backward/JOIN_REVIEW.md: composition review; the later release correction is
  supplied by forward/RELEASE_HANDOFF.md and the final operation receipt.
- independent/passive_prior_art.md: strongest primary comparisons.

Separate boundary and diagnostic scripts are retained with their recorded outputs.
They need not all be rerun to consume the result.

## Prior constructions

The backward, forward, and independent directories also preserve the initial
equilibrium-learning, adaptive-transport, and analytic-ridge constructions.
They are not evidence of a flagship practical improvement. Their precise
obstacles are part of the research record.

The warm archive is byte-for-byte the preceding weak-stream research package.
It includes earlier packages at their original scopes. Hashes are in
PRESERVATION.json. No old theorem is generalized by this return.

## Document build

The PDF was built with:

    pandoc acquired_passive_environment.md --standalone \
      --pdf-engine=pdflatex --include-in-header=report_preamble.tex \
      --resource-path=. --output=acquired_passive_environment.pdf

LaTeX, Pandoc, and Poppler are document tools, not dependencies of the scientific
algorithms. The source report, proofs, code, and records remain usable without them.
