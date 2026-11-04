WHEN THE CONTROL RECORD ARRIVES
A finite-error memory law for one quantum payload
Research return, 5 November 2026

START HERE
==========

causal_payload_memory.pdf is the complete, self-contained paper. Its LaTeX
source is causal_payload_memory.tex. RESULT_SUMMARY.txt is the portable factual
handoff; SELECTION_RECORD.txt records the independent selection and the
questions that remain open. sources.json identifies primary prior machinery
and the pinned governing Astra packages. SHA256SUMS.txt covers every packaged
file except itself.

The main result is a proved conditional theorem and a complete ideal quantum
operation with a finite physical implementation contract. It is not a
laboratory demonstration, formal proof-assistant certificate, exhaustive
priority determination, or realised civilisation-scale technology.
Independent audits here are by separately tasked collaborating agents;
they are not external peer review.

The homogeneous weak partial-SWAP stream's low-memory, near-linear general
receiver remains unresolved. This package resolves a distinct foundational
question: whether small payload/source dimension alone bounds the quantum
memory of causal recovery from mixed physical outputs. It does not. A short
record's arrival time is an explicit additional resource in the constructed
family. The complete early-record reader uses actual output measurements,
not an inaccessible bath purification or a return link.

KEY CONVENTIONS
===============

All channel errors are HALF diamond distance, ||A-B||_diamond/2. Numerical
Choi residuals are normalized-Choi half trace distances, not numerical diamond
norm evaluations.

Memory dimension is counted per dephased classical branch. Classical records
may be unlimited. Every coherent register, delay line, entanglement half and
ancilla crossing the relevant cut counts. "Whole-qubit capacity" is the maximum
over branches; it is not occupancy on every branch. The paper separately
proves bounds on actual expected retained qubits and qubit-time under the
maximally mixed payload / marginal of a Bell input.

The fixed emitter does not accept receiver feedback that changes its future
encoding or record schedule. The physical gate, factory, record, timing,
precision, routing, reset, calibration and protection resources are declared.
In particular, the new programmed source uses strong finite controlled gates
and a final full SWAP. It is not a weak-action replacement for the warm reader.

MAIN PACKAGE MAP
================

proofs/late_selector_theorem.txt
  Concise algebraic proof: selector-dependent decoders -> common analytic Petz
  witness -> commutator gap -> Kraus-rank memory bound.

proofs/small_bias_instantiation.txt
  Complete finite-field family, physical source/receiver, every-prefix and
  variable-branch expectation refinements, finite costs, initialization,
  calibration, and n=1000 analytic point.

proofs/local_expander_instantiation.txt
  Separate five-bit record / fixed-register source, imported 16-generator
  local expander, actual generator list and fixed-order routing. Its small
  certified error threshold must not be exchanged with the small-bias gap.

proofs/late_selector_independent_audit.txt
  Independent proof and interface audit, including the essential Z anchor,
  variable-branch rank calculation and header timing caveat.

proofs/emission_error_refinement.txt
  Actual noisy-emission capacity and expected-occupancy bounds. Includes the
  separate branch-probability correction and the required fixed timing.

proofs/prior_addendum.txt
  Closest comparator: Ioannou et al. (2022), common compression followed by
  setting-dependent measurements. Its all-projective-measurement bounds
  differ from the finite binary-probe score premise used here.

proofs/verify_payload_memory.py and payload_memory_verification.json
  Executed full quantum-channel checks, commutator spectra, hybrid-memory
  tests, singular baseline cases and a specified one-qubit-discard baseline.

proofs/small_bias_checks.py and small_bias_execution.json
  Exact finite-field/character calculations, small arbitrary-reference
  decoder checks, and one generated n=1000 classical program.

figures/
  Publication figure in PDF, SVG and PNG; generating script, caption and
  memory_resources.json. These show analytic theorem bounds and arithmetic.
  No large quantum state or device is simulated by that figure.

INDEPENDENT COMPANIONS
=====================

companions/scalar_receiver/
  Complete restricted no-go for one tracial receiver qubit using predetermined
  partial-SWAP encounters. The scope excludes general instruments, feedback,
  pure ancillas, larger memories and block compression. Its arbitrary final
  decoder is included. A three-dimensional recurrence is checked against
  direct three-qubit matrices.

companions/thermal_pulse/
  Complete finite thermal pulse identification for a declared observable
  all-even OU system, with unknown drift and diffusion, calibrated common
  diffusion-scaling access, no hidden state reset, and explicit conditioning
  and sampling costs. The million-cycle demonstration's conservative bound
  does not certify its displayed point accuracy.

companions/image_force/
  Translational force query from raw blurred images under a specified radial
  PSF and particle-pair contract. Includes the exact moment correction, Stokes
  virtual field, reciprocal force identity and finite-lag costs. Executed
  symbolic/quadrature evidence is not an optical experiment.

PRESERVED WARM RESULTS
=====================

warm/tracial_acquisition_research_package.zip is the complete prior mixed-bath
acquisition package, copied unchanged. Its SHA-256 is
355131cf35f48c97a71daea24037392847af50ddcd90a9578c96ec0e817a8fab

warm/rare_failure_research_package.zip preserves the previous rare-failure
work. warm/RESULT_SUMMARY.txt, WARM_RESULTS.txt and SELECTION_RECORD.txt are
unchanged prior records, not summaries of the new result.

warm/active_port_nonidentifiability.txt and
warm/local_rules_prediction_obstacle.txt preserve both earlier nonquantum
companions. The new thermal construction adds a new physical port; it does
not invalidate the earlier identical-transcript result under force-only
access.

Preserved premises include the universal fourth-order action law under
genuine classical feedback and a pathwise budget, exact acquired partial-SWAP
channel and factor-two recovery guarantee, independent-module collective
decoder theorem, source forgetting versus physical acquisition, finite
collision/factory interfaces, rare-failure local reach/backbone/start-mass/
precision costs, and the unresolved pure-port weak-export route. The paper
states these scopes; the unchanged archives and pinned public sources govern
the full original results.

REPRODUCING THE EXECUTED CALCULATIONS
===================================

Use a writable COPY of this directory: scripts overwrite the JSON receipt
beside the script. Rerunning therefore changes the checksum manifest.
No command below requires the original absolute workspace path.

Python 3.10 or later with NumPy, SciPy, SymPy and Matplotlib is sufficient
for the supplied scripts. The executed root environment is recorded in
runtime_versions.json. A separate temporary SymPy installation used for
the original force calculation is not required if SymPy is installed normally.

From this directory:

    python3 -m pip install -r requirements.txt
    python3 proofs/verify_payload_memory.py
    python3 proofs/small_bias_checks.py
    python3 companions/scalar_receiver/verify_scalar_receiver.py
    python3 companions/thermal_pulse/heat_pulse_demo.py
    python3 companions/image_force/force_query.py
    python3 figures/make_memory_figure.py

These are independent entry points; running all is not needed to read or
apply the theorem. Parameters and seeds are in the scripts. They have no
command-line parameter parser. In particular, the thermal script performs
1,000,000 cycles with seed 913. Do not redirect stdout to the receipt path:
the scripts themselves write full JSON and print a shorter summary.

Receipt destinations:

  proofs/verify_payload_memory.py
    -> proofs/payload_memory_verification.json
  proofs/small_bias_checks.py
    -> proofs/small_bias_execution.json
  companions/scalar_receiver/verify_scalar_receiver.py
    -> companions/scalar_receiver/scalar_receiver_verification.json
  companions/thermal_pulse/heat_pulse_demo.py
    -> companions/thermal_pulse/heat_pulse_execution.json
  companions/image_force/force_query.py
    -> companions/image_force/receipt.json
  figures/make_memory_figure.py
    -> figures/causal_memory_bounds.{pdf,svg,png},
       figures/memory_resources.json, figures/figure_caption.txt

With a LaTeX installation containing the packages in the preamble:

    pdflatex -interaction=nonstopmode -halt-on-error causal_payload_memory.tex
    pdflatex -interaction=nonstopmode -halt-on-error causal_payload_memory.tex

The final PDF was compiled and visually inspected. Recompilation can change
PDF timestamps and byte hashes without changing the mathematical content.
Historical execution notes inside companions may name the original staging
paths; the relative commands above are the portable entry points.

SCOPE OF THE NUMERICAL EVIDENCE
===============================

The proofs establish asymptotic and arbitrary-reference statements.
Finite examples check formula translation and implementation. They do not
replace the proofs. No 1000-qubit density matrix, noisy factory, protected
quantum bank, timing controller, large calibration campaign or optical
experiment was run. The 25-bit record, 1001-qubit capacity, 901.901-qubit
expected-memory bound and 450950.228340645*tau pre-record expected exposure
are analytic consequences for the declared exact emission. Imperfect emission
needs the separate expected-occupancy correction in the error refinement.

Extra header-delay exposure is charged only while NO selector information has
reached the receiver. A progressively revealed serial header requires a
conditional-ensemble analysis after each informative bit. The base plotted
exposure does not include that unproved extension.
