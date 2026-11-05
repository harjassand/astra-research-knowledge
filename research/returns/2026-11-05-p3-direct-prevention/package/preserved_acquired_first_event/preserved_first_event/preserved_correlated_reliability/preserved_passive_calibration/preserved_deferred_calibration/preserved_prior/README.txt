A CONTROL-SPEED LAW FOR READING UNENCODED QUANTUM SYSTEMS
Research return — 5 November 2026

START HERE

Read Astra_Control_Speed_Law.pdf for the complete final theorem, proof,
matching constructions, resource accounting, comparison, and limitations.
control_speed_law.tex is the editable source. The result is a mathematical
construction with internal collaborative proof checks and numerical
diagnostics. It has not been experimentally demonstrated, externally peer
reviewed, or certified historically novel.

WHAT WAS RESOLVED

For initially unencoded n-qubit sources with actual independent inaccessible
Markov Z dephasing, bounded k-site source commutation support, and summed
per-site term-norm control budget Omega, the acquired high-weight transverse
channel is exponentially suppressed for EVERY fixed finite Omega/lambda.
Free operations must be covariant at full retained-instrument scope.

The main bound includes genuine classical feedback with budgets imposed in
each classical branch:

  ||N P_R||_diamond <= q_k^|R|,
  q_k = exp[-lambda/(k Omega)]
        + (1-exp[-lambda/(k Omega)]) 2^(-1/k) < 1.

It is uniform in eventual acquisition time, quantum memory, references,
collective processing, and heralding with all consumed specimens counted.
The global-decomposition model has a sharper coefficient in Appendix A.
Do not silently give that sharper coefficient to branchwise-only budgets.

At fixed k and Omega/lambda >= 1, the full-weight known-parity promise at
fixed contrast, and the GHZ-versus-diagonal-mixture promise, have

  log(1+M_opt) = Theta_k(1+n lambda/Omega).

Polynomial specimen cost has the necessary and achievable scale
Omega/lambda >= order n/log n. A zero-start summed slew cap K, imposed at
EACH specimen's arrival, additionally requires K/lambda^2 >= order
(n/log n)^2. Bounded specimen cost replaces n/log n by n in both scales.
The exact local-meter and finite-slew pulse constructions attain these
orders with actual ports and protected meters supplied as premises.

This is NOT a universal purity upper bound, a zero-capacity theorem,
an all-growing-k sharp law, or a general continuous-Hamiltonian pure-port
recovery algorithm. Universal purity only receives the stated worst-case
lower bound. All physical model assumptions remain substantive.

PACKAGE MAP

  Astra_Control_Speed_Law.pdf     Final proof report.
  control_speed_law.tex           Editable report source.
  CONTINUATION.txt                Concise factual handoff and open limits.
  SOURCES.json                   Pinned governing source revision and primary literature.
  environment_versions.txt       Recorded software versions.
  SHA256SUMS.txt                  Content hashes, excluding itself.

  derivations/ALL_STRENGTH_ACCESS_PROOF.md
      Detailed derivation with the corrected global/CQ distinction.
  derivations/independent_quantum_proof_check.md
      Separate collaborator's proof check, including the feedback issue.

  checks/check_coverage.py
  checks/coverage_checks.json
      120 selected-operator fixed-noise-trajectory checks and seven
      constant-pulse ODE checks. These do NOT evaluate a general diamond
      norm and do NOT exhaust feedback, references, or controls.

  compute_resource_law.py
  resource_law.json
  resource_law.pdf
  resource_law.png
      Analytic resource curves, 33 numerical rows, and 18 finite-slew
      ODE checks (6 triangles and 12 trapezoids). The wide figure is
      suitable for separate viewing. It plots bounds, not exact optima.

  render_report_figure.py
  resource_law_report.pdf
  resource_law_report.png
      Same analytic curves in a portrait layout for the report.

  companion/effusion_companion.md
  companion/check_effusion_companion.py
  companion/effusion_diagnostic.json
      Separate exact finite-temperature transport/intervention
      construction. It is not used by the quantum theorem. Its physical
      ports, geometric shell promise, finite flight/clearing costs,
      systematic errors, and remaining exponential exposure are explicit.

REPRODUCTION

Use Python 3 with NumPy, SciPy, and Matplotlib. The programs use no network.
Run from the extracted package directory:

  python3 checks/check_coverage.py
  python3 compute_resource_law.py
  python3 render_report_figure.py
  python3 companion/check_effusion_companion.py

Each program writes its JSON or figures beside the program, except the
resource program also accepts --output-dir. Copy the recorded JSON first
if you want to retain the original execution alongside a new execution.
Floating-point values can differ slightly between numerical libraries.
Runtime metadata and PDF creation dates are not bit-reproducible.

To rebuild the report with a normal TeX Live installation, from this folder:

  pdflatex -interaction=nonstopmode -halt-on-error control_speed_law.tex
  pdflatex -interaction=nonstopmode -halt-on-error control_speed_law.tex

This generates control_speed_law.pdf. The supplied named final PDF is the
same report. Packages used are listed in the source preamble.

EVIDENCE AND ERRORS

The finite-trajectory maximum tested norm/bound ratio was 0.20881396899958496.
All 18 finite-slew ODE checks satisfied beta >= 1-2 lambda T; maximum pulse
area error was 4.45e-16 and maximum noiseless transfer error 1.82e-13.
These are error-finding diagnostics. The analytic proof supports the
theorem; neither finite simulation nor a reviewer assertion replaces it.

The final report additionally gives complete local binary-POVM calibration
using six trusted Pauli eigenstates per site. The total reference cost is
O(n^3 epsilon^-2 beta^(-2n) log(n/delta)) at the stated bias tolerance.
It is polynomial in the polynomial-contrast regime. It does not certify
cross-site independence, lack of common causes, Markovianity, or stationarity.
Calibration failure delta and discrimination error must share the error budget.

GOVERNING HANDOFF

The inherited Astra packages are accepted premises pinned to Git revision
5cfc803599d9f95cfa0a55896fb580e77567e162 in
https://github.com/harjassand/astra-research-knowledge .
See SOURCES.json for exact paths. No changes to that repository or external
publication were made as part of this return.
