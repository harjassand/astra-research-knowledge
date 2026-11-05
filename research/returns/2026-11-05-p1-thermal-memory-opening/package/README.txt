THERMAL QUANTUM MEMORY: INDEPENDENT SELECTION AND CONSTRUCTIVE OPENING
5 November 2026

Primary deliverable
  thermal_memory_selection_20261105.pdf
  selection_brief.tex

The report nominates one full question: efficient, reference-preserving
write/passive-hold/read access to the proved random-embedding BDL 3D memory
family, with its physical assumptions and resource bill retained.

The central construction compiles multiscale syndrome histories into a
bounded-degree local constraint model. A self-contained polymer sampler,
an exact TV-to-diamond loading identity, and a source-conditional
instantiation are proved in the report. The full base-validity factor
removes the earlier conditioning floor. This is not a practical hardware
implementation or an established priority claim over existing samplers.

Exact reproducible checks (Python 3, standard library only)
  python3 history_polymer_example.py
  python3 verify_matroid_obstruction.py

Their JSON output files are included. They check synthetic finite algebraic
examples, not the full BDL code or a physical experiment.

Independent working notes
  quantum_new.md               Central construction and physical scope
  learning_challenge.md        Independent proof audit and comparator tests
  csw_bdl_comparison.md        Current Code SW and regular-matroid comparison
  learning_new.md              Preserved strict-AT sampling alternative
  independent.md              Preserved SK/thermal-filter selection audit
  conditional_thermal_repair.tex  Root's unselected conditional transport note

The report is the consolidated statement. Working notes preserve the
selection process and their own explicit scope qualifications. The thermal
repair note did not receive the same independent audit as the selected
polymer construction. No rival participant's new proposal was consulted.

Source and claim record
  source_audit.json
  manifest_sha256.json

The source audit distinguishes full primary text from abstract-only access.
Code Swendsen-Wang applicability and regularity of the actual BDL physical
check matroids are unresolved. Full-Gibbs logical randomization is not a
reason to exclude a competing sampler: syndrome sampling followed by fresh
logical injection suffices.

Preserved prior work
The completed equilibrium_inference_20261105.pdf and its package, the
quantum companion, and the original joint_recovery_continuation material
remain unchanged. Their accepted scope is summarized in the report.
The unrestricted partial-SWAP joint memory/processing law remains open.

Build the report
  pdflatex -interaction=nonstopmode -halt-on-error selection_brief.tex
Run twice to resolve references. Dependencies are standard LaTeX packages.

All runtime and temperature statements fix the code-family structural
parameters first. Their very large constants are not suppressed as an
engineering advantage. Bath, control, calibration, initialization, routing,
reset and holding-time resources must be interpreted as stated in the report.
