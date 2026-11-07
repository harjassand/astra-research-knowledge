P3 LOCAL NOISE ABSORPTION — 7 November 2026

Start with P3_NOISE_ABSORPTION_20261107_RETURN.txt. It contains the complete
mathematical arguments, input and output contracts, acquisition and operating
costs, source credits, and unfinished programme status.

The programme endpoint remains repeatable many-body state control with all
physical and information costs paid. This package resolves a supplied-model
noise-completion and native-menu operation. It does not certify an acquired
apparatus, a generic hardware threshold, or economical unknown commissioning.

REPRODUCTION (existing Python + NumPy + SciPy + Matplotlib + threadpoolctl)

  python3 run_audits.py
  python3 operating_regime.py
  python3 make_figure.py

No network access, installation, physical device, worker, or external message
is needed. Dense full-system checks are deliberately restricted to small audits.
The general algorithms in noise_absorption.py and native_menu.py operate on
supplied finite local blocks. Generic matrix cost is exponential in block size.

CODE

noise_absorption.py: complex local positive Choi completion; projected-Choi
optimal reset rate as a numerical diagnostic; KMS modular completion including
its coherent term; Clifford light-cone transformation; physical-output bounds.

native_menu.py: sparse local full-generator and stationarity representations;
binary64 LP for an ACTUALLY SUPPLIED affine generator menu and rate caps.

rational_certificates.py: independent exact Fraction witnesses for the biased
qubit reset rate, positive LDL, and native-menu feasibility distinctions.

operating_regime.py: exact noisy-actuator rate/floor decisions; complete mixing
formula; finite-time population inversion; rational whole-state parameter-box
certificate; binomial global-versus-local calibration separation.

run_audits.py: independent small complex, locality, entangled-state/reference,
overlapping-menu, and exact-rational checks. Numeric checks are not substitutes
for the proofs and are not experimental data.

KEY OUTPUTS

GRAPH_STATE_CONTROLLER_BINARY64.json is computed logical-generator data,
not a native hardware command file or a rigorous interval gate synthesis.

EXACT_RATIONAL_CERTIFICATES.json and EXACT_GLOBAL_PARAMETER_CERTIFICATE.json
are exact arithmetic certificates at their specific rational-input contracts.
The latter's confidence intervals are DECLARED, not experimentally acquired.

FINITE_TIME_ACQUISITION_AUDIT.json uses synthetic model probabilities. Its
illustrative sampling count at population-probability error 0.001 does not
establish the much tighter simultaneous parameter intervals used in the
million-factor global certificate. All actual preparation/readout/timing and
model-validation costs remain paid and unperformed.

RUN_SUMMARY.json summarizes run_audits.py. The operating-regime and calibration
checks have their separate JSON records. NATIVE_MENU_AUDIT.json includes an
infeasible reset embedding with a feasible stationary target, preventing an
overbroad interpretation of LP infeasibility.

NOISE_ACTIVITY_AND_CALIBRATION.png and .svg plot exact declared-model formulas.
The right panel is full physical trace distance, preserved by a common unitary
dressing; the one-factor error stays 0.002 while the whole-state distance tends
to one. It is not a simulation of a physical laboratory.

SOURCE_ACCESS_NOTES.txt preserves all prior notes and records new holds. Held
originals were not retried or reconstructed. The report credits established
GKSL, KMS, optimization, reset, state-synthesis, and statistical machinery.
No historical-priority claim is made.

MANIFEST_SHA256.json records package file hashes. It excludes itself.
