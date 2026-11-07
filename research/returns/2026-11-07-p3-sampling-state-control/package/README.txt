P3 SOURCE-DRIVEN MANY-BODY STATE CONTROL — 7 November 2026

Read P3_SAMPLING_STATE_CONTROL_20261107_RETURN.txt for the complete result,
proofs, native interface, repeated-output conditions, full costs and limits.

This is a mathematical research package and a logical controller implementation.
It is not an acquired apparatus, hardware driver, physical experiment, or a
generic noise-correction theorem. All predecessor artifacts remain unchanged.

FILES

sampling_control.py
  Pure-Python integer/Fraction finite-budget compiler and controller.
  source_count(cell, arm, n) must supply n fresh measured source outcomes.
  Its return value is the number of ones, not an uncharged binomial oracle.
  getbits(cell, n) supplies paid fair bits, or use
  bounded_commands_with_source_bits to extract bits from additional source calls.
  The rational target is in calibrated observation coordinates; contrast converts
  population error to physical-state error. Actual populations are never passed
  to the runtime controller. The executable uses a common target coordinate and
  uniform bounds; sites may have distinct unknown populations.

exact_factory.py
  Exact rational Huber-based emitter with almost-sure finite termination and
  the cited expected source-query guarantee. No hard runtime or expected bit-work
  guarantee is asserted. Do not replace the bounded emitter's contract with it.

run_audits.py
  Exact rational calculations, finite distribution enumeration, cost certificates,
  a small binary64 quantum-reference calculation, and seeded sampling fixtures.
  Uses already available NumPy, SciPy and threadpoolctl. No dependency installation
  or network access is part of the audit. Run: python3 run_audits.py
  Million-slot certificates are computed, not their physical/source calls.

make_figure.py
  Standard Matplotlib figure from compiler counts and the algebraic calibration
  obstruction. Run: python3 make_figure.py

The JSON records distinguish exact arithmetic, analytic bounds and synthetic
fixtures. SOURCE_ACCESS_NOTES.txt preserves the complete predecessor notes and
records one newly unavailable governing-original path. MANIFEST_SHA256.json
records package file hashes. No primary-paper bytes or held predecessor archive
are included. No physical source, role, worker, purchase or outreach was created.

The main implementation refinements are exact probability sampling, a finite
global or per-site cap, explicit timeout fallback, noisy calibrated observations,
source-derived fair bits, and a complete source/reference error budget. Correct
one-copy marginals do not license label reuse across outputs. Modeled native
noise is distinct from unknown residual error and from output holding resources.
