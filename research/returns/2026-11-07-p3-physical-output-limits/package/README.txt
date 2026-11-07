P3 PHYSICAL OUTPUT LIMITS — 7 NOVEMBER 2026

Start with P3_PHYSICAL_OUTPUT_LIMITS_20261107_RETURN.txt.

This package resolves the constant-per-site-strength threshold question for
complete pure physical outputs under the specified continuing local noise.
It retains the larger repeatable-state-control programme as unfinished.

Main delivered results:
- A global fidelity differential inequality uniform over arbitrary auxiliary
  systems and initial correlations, with a local incidence proof.
- Product-state and bounded-degree graph-state physical-noise applications.
- Finite restoration, storage, delivery and scheduled-acceptance bounds.
- A separate residual-generator budget and a simultaneous repeated-output bound.
- Necessary general coherent strength growth; matched order of required rate
  within the target-preserving controller class, using established ideal pumps.
- Application to the already declared native interval regime without new
  numerical identification of its noise rates.

FILES

P3_PHYSICAL_OUTPUT_LIMITS_20261107_RETURN.txt
  Self-contained proof, governing assumptions, consequences, complete abstract
  resource accounting, limitations and source credit.

physical_output_bounds.py
  Standard-library exact-rational certificate emitter. Inputs are warranted
  supports, local target-block or Hamiltonian/jump norm bounds, noise rates,
  optional graph, precision and requested delivery parameters. It does not
  acquire those inputs or execute a physical controller.

run_audits.py
  Exact Gaussian-rational finite operator checks (using pairs of Fraction
  arrays), exact LDL positive-semidefinite certificates, graph and pump
  identities, instantaneous sharpness, support-cover enumeration, and
  separately labeled binary64 dynamics checks.

make_figure.py
  Creates the standalone scientific PNG/SVG from the mathematical bounds.

EXACT_AUXILIARY_OPERATOR_AUDIT.json
EXACT_INSTANTANEOUS_SHARPNESS.json
EXACT_GRAPH_AND_PUMPING_AUDIT.json
EXACT_SUPPORT_COVER_AUDIT.json
FINITE_RESOURCE_CERTIFICATES.json
ACCEPTED_NATIVE_REGIME_BOUND.json
FINITE_DYNAMICS_DIAGNOSTIC.json
RUN_SUMMARY.json
  Reproducible finite records. Rational certificate fields are strings. The
  dynamics record is explicitly binary64 and is not a diamond-norm proof.

PHYSICAL_OUTPUT_LIMITS.png / PHYSICAL_OUTPUT_LIMITS.svg
  Plot of the proved ceilings, necessary strength and high-quality duration.
  Curves are neither measurements nor claims of achievable general fidelity.

SOURCE_ACCESS_NOTES.txt
  New reads/hold, then the complete preceding notes verbatim. The new N517
  governing-path 404 is held; N236 and all earlier holds remain binding.

MANIFEST_SHA256.json
  Byte inventory of the files above, excluding the manifest itself.

REPRODUCTION

From this directory:
  python run_audits.py
  python make_figure.py

The certificate emitter needs only Python's standard library. The audit
uses numpy and scipy; the figure uses numpy and matplotlib. No network,
quantum simulator service, physical oracle, sympy installation, paid service
or hardware access is required. The finite records are deterministic except
for explicitly seeded synthetic vectors, whose seeds are in the code.

Example certificate:

  from fractions import Fraction as F
  from physical_output_bounds import compile_uniform
  e = compile_uniform(1000000, 1, 10, 15, maximum_graph_degree=4)
  print(e.root_interval(bits=80))
  print(e.exclusion_certificate(F(99,100)))
  print(e.delivery_upper(F(1,10000)))

Read the model contract before applying that example. The graph mode requires
physical on-site Z noise; the product mode requires the corresponding X-noise
law. The generic Hamiltonian/jump norm conversion is safe under conjugation.
Tighter supplied local block bounds must be valid in the actual target frame.
The invariant_target flag is a premise about every allowed auxiliary state,
not a request for the compiler to establish invariance.

No experiment, new apparatus, historical-priority result, formal-kernel proof,
optimal general coherent controller, universal energy price or P=NP result
is asserted. Complete physical-output/reference and source/native contracts,
including continuing resources and output holding, remain governing.
