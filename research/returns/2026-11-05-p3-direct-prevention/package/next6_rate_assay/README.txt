FINITE GROUPED-WAIT OPERATING RATE ASSAY
Astra research construction, 5 November 2026

This module supplies the local physical-statistical interface for a separate
first-event intervention decision. It acquires the arithmetic mean of the
actual requested-context boundary exit rates, without learning a rate table.
It does not by itself identify a boundary flux with a first-event lifetime.
The proof of that global decision reduction belongs to the parent endpoint.

READ
  finite_rate_assay.pdf       Complete eight-page proof and execution account.
  rate_assay_body.tex         Integrable body; no documentclass, unique ra labels
                             and RA-prefixed macros, with definitions provided.
  finite_rate_assay.tex       Standalone wrapper, sources and execution table.
  STATUS.txt                 Exact earned operation and conditions.
  DEVELOPMENT.txt            Preserved improvements and superseded valid route.
  PRIMARY_SOURCES.json        Original sources and the scope of their use.
  EXECUTION_RECEIPT.json      What was executed, costs, limits and checksums.
  MANIFEST.json              SHA256 hashes of all deliverable files except itself.

REPRODUCE
  python3 audit_rate_assay.py
  pdflatex -interaction=nonstopmode -halt-on-error finite_rate_assay.tex
  pdflatex -interaction=nonstopmode -halt-on-error finite_rate_assay.tex

The canonical audit uses Python 3.12.14, NumPy 2.3.5, and mpmath 1.3.0.
It writes rate_assay_execution.json. Numerical random seeds, finite service,
exact quotient and rational interval arithmetic are defined in the program.
Recorded CPU durations can vary when rerun; all inference is based on stated
analytic guarantees, not on an empirical confidence claim from this one run.
The synthetic latent exponential waits are not actual apparatus measurements.

The historical audit_rate_assay_initial_mom.py and its separately named JSON
preserve the earlier valid, larger contrast-squared median-of-means schedule.
They are not the final recommended schedule. The earlier uniform-bit
lower-bound example in that historical record is superseded for the main
endpoint by the reliable q_star <= 1/4 hard pair in the final theorem.

Packaging may omit tmp/, __pycache__/, compile_stdout.txt and LaTeX auxiliary,
log and out files. The final source and PDF are sufficient to rebuild the
report. The saved receipt records clean compilation and visual inspection.
No prior package or independent continuum artifact was altered.
