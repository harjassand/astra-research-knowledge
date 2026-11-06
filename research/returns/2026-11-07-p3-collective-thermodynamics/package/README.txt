P3 COLLECTIVE THERMODYNAMICS — 2026-11-07

Read RESEARCH_REPORT.txt for the theorem, proofs, governing conditions,
costs and interpretation of the evidence. This directory contains only
new work for this return. No predecessor originals are included.

DELIVERED EVIDENCE

RECORDS.json: finite calibrated digital source record, 3840 scalar values.
AUDIT_TRUTH.json: separated source truth, used only for the subsequent audit.
ACQUISITION_CERTIFICATE.json: learned model, uniform coefficient error and
  explicit hypothetical physical sampling cost. No physical shots were taken.
DECISION_GROUND.json and DECISION_FINITE_TEMPERATURE.json: rational feasible
  commands, global objective bounds, mixture probabilities/responses and
  complete uncertainty-aware phase covers for the declared model class.
FINITE_N_CERTIFICATE.json: all-sector 64-spin rational eigenvalue intervals,
  finite-temperature free-energy interval and mixture-deficit certificate.
SCHUR_DIAGNOSTIC.json: separate binary64 generic-block validation.
VALIDATION.json: focused exact checks and labeled floating-point diagnostics.
RESULTS.png: scientific illustration; the JSON certificates govern numbers.
MANIFEST.json: hashes of these new deliverables and code.

REPRODUCTION

The code uses the existing Python environment, NumPy, SciPy, Matplotlib and
threadpoolctl. It creates no remote jobs and performs no network operations.
requirements.txt records the observed versions; it is not an instruction to
install infrastructure or acquire hardware.

Run in this directory, in order:

  python acquire_model.py
  python global_decision.py
  python schur_diagnostic.py
  python finite_size_certificate.py
  python verify_result.py
  python make_figure.py

On the session's existing runtime these steps took approximately 42 seconds
in total. Times vary. The recorded exact rational values, uncertainty
budgets and certificate inequalities are the substantive outputs.

CORE MODULES

polynomial_tools.py: rational polynomial operations and explicit probe inverse.
probe_schedule.py: rational positive-time schedule and derivative bounds.
calibrated_source.py: exact rational small-N source with Taylor error bounds.
entropy_bounds.py: outward scalar exp/log/entropy and square-root bounds.
certified_thermodynamics.py: global rational state bounds and all-phase covers.
global_decision.py: LP proposals with rational primal/dual certification.
finite_size_certificate.py: specialized exact Sturm finite-size certificate.
schur_diagnostic.py: generic all-sector compiler, binary64 diagnostic only.
verify_result.py: checks normalization, records, decisions and finite-N evidence.

The mathematical construction has the scope stated in the report. The code
does not provide an unknown physical apparatus, a generally calibrated
actuator, a generic finite-N exact-inertia implementation or an economical
physical acquisition schedule. The finite-size Sturm emitter explicitly
requires the displayed quartic X/Z model. No source-access or transfer hold
is relaxed by this new package.
