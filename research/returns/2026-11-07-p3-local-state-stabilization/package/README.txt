P3 LOCAL STATE STABILIZATION — PACKAGE GUIDE

Read P3_LOCAL_STATE_STABILIZATION_20261107_RETURN.txt for the full theorem,
proofs, endpoint, resource contracts, source credit, limitations and findings.

local_stabilizer.py:
  Symbolic compiler from a supplied one/two-qubit unitary circuit to a fixed
  random-scan local process. Integer resource bounds use exact Fractions.
  Native synthesis and physical implementation are separate. Dense audit
  helpers are intentionally exponential and only used on small examples.

run_audits.py:
  Recreates the Bell and noncommuting two-qubit thermal examples, exact clock
  resource certificates, complete-channel diagnostics, perturbation audit,
  exhaustive small-clock structural audit, and rational Curie–Weiss barriers.

make_figure.py:
  Creates PRECISION_AND_LOCAL_RESTORATION.png from the recorded outputs.

Run in this directory with Python, NumPy, SciPy, Matplotlib and threadpoolctl:
  python run_audits.py
  python make_figure.py

Emit a different logical process:
  python local_stabilizer.py BELL_SOURCE.json process.json --duty 1/64 --mixing-error 1/100

Input source contract:
  work_qubits: positive integer q
  output_qubits: chosen subset of work qubits
  input_state: zero
  gates: ordered list, each with one/two distinct work-qubit labels

Named H, X, S, CNOT, RY and RZ gates have their usual ideal unitary meanings.
The numerical matrix fixtures have binary64 entries and a reported unitarity
residual; they are diagnostics for ideal unitary targets, not exact finite-bit
physical gates. The mathematical theorem requires exact source unitaries or
a separately supplied source/implementation error budget. A controller must
implement the source gates' known adjoints, reset, and independent randomness.

Main records:
  BELL_SOURCE.json / BELL_LOCAL_PROCESS.json
  THERMAL_SOURCE.json / THERMAL_LOCAL_PROCESS.json
  FULL_CHANNEL_AUDIT.json / THERMAL_STATE_AUDIT.json
  CLOCK_STRUCTURE_AUDIT.json
  BOTTLENECK_CERTIFICATES.json
  ACCURACY_RESOURCE_TABLE.json / RUN_SUMMARY.json
  SOURCE_ACCESS_NOTES.txt

Full-state restoration is approximate on the physical output because the
stationary process includes intermediate clock states. It does not retain an
exact hard-window support guarantee or imply natural-bath thermalization.
No physical experiment was performed.
