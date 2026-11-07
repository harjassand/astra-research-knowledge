P3 NOISY THERMAL CONTROL — 7 NOVEMBER 2026

Start with P3_NOISY_THERMAL_CONTROL_20261107_RETURN.txt. It contains the full
question, governing premises, proofs, finite compilation and resource contracts.

Reproduce the mathematical audits with:
  python3 run_audits.py
  python3 make_figure.py

Dependencies: Python 3, NumPy, SciPy; Matplotlib for the figure. No network,
hardware, additional worker, paid resource or physical source is used by the
scripts. Run from this directory or invoke them by absolute path.

gain_certificate.py: exact Python Fraction arithmetic; reachable positive
repair-loop criterion, minimal rates, capacities and nonnegative linear price.

thermal_controller.py: binary64 finite-matrix emitter for Gaussian CKG jump
maps and KMS completions, retaining cross-frequency terms. It is not a rigorous
finite-bit/gate compiler or an acquired physical native primitive.

resource_bounds.py: binary64 evaluations of the report's analytic bounds.
Operational schedule examples need a supplied justified mixing-rate lower
bound. The alpha=0.1 examples are explicitly illustrative and uncalibrated.

EXACT_GAIN_CERTIFICATES.json: exact rational results and scope counterexample.
FINITE_QUANTUM_DIAGNOSTIC.json: noncommuting three-qubit native-law fixture,
stationarity residuals and a retained entangled-reference trajectory.
LOCALITY_DIAGNOSTIC.json: six-site operator-localization checks and independent
Gaussian quadrature checks of the cross-frequency kernel.
RESOURCE_SCENARIOS.json: conservative local-window costs; these are explicitly
not a practical commissioning demonstration.
FINITE_CONTROLLER_BINARY64.npz: actual finite Hamiltonian, state and emitted
generator matrices for inspection. All data are synthetic mathematical inputs.
RUN_SUMMARY.json: completed audit record.
NOISY_THERMAL_CONTROL.png/.svg: one analytic rate law and one numerical fixture.
SOURCE_ACCESS_NOTES.txt: new source checks plus complete inherited notes verbatim.

The complete structural result does not close the larger programme of economical
repeatable physical many-body state control. Physical installation, acquisition,
rate calibration, residual precision and continuing resources remain paid.
