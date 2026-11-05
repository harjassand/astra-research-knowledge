THE COST OF INFERRING EQUILIBRIUM BEFORE RELAXATION
Research report and reproducibility package, 5 November 2026

START HERE

Read equilibrium_inference_20261105.pdf for the model, complete central
proof, attaining operation, physical resource accounting, source comparison
and limitations. The separate notes record the independent construction
routes and internal audit. The numerical checks are finite checks, not
formal verification, external peer review or physical measurements.

The programme establishes a logarithmic minimax resource law in a specified
scalar-port experiment class. It does not establish worldwide priority,
civilisation-changing impact, a practical speed advantage over optimal
ordinary extrapolation, or the earlier unrestricted quantum memory law.

MAIN RESULT

For x'=-A x+b u, y=b^T x, A symmetric with mu I<=A<=Lambda I, ||b||=1,
unknown dimension and spectrum, the target is S=mu b^T A^-1 b. Each trial
starts at zero, has maximum transient age T and independent Gaussian
sensor readout dY=y dt+sigma dW. Causal feedback and unlimited computation
are allowed. Total squared-drive effort is E=sum integral u^2 dt and its
normalization is B=E/(sigma^2 mu^2); it is not thermodynamic port work.

For 0<s=mu T<=1/64, 16<=kappa=Lambda/mu<=infinity, 0<epsilon<=1/16,
and success probability 3/4, the proved scale is

  log(1+B_star) = Theta(Phi),
  Phi = sqrt(kappa) L log(1+L/(s sqrt(kappa))), L=log(1/epsilon).

For unbounded kappa take Phi=L^2/s. Constants in the logarithm are
universal; the exact optimal leading constant is not determined.

The upper construction uses a bounded monotone ramp, a plateau, finitely
integrated readouts, Chebyshev weights and repetitions. The lower bound
uses positive finite moment-matched spectra and covers all permitted
adaptive inputs. Rate bounds and normalization are supplied information.
Reset time, detector bandwidth, systematic error, physical work, parallel
copies and total serial elapsed time remain separately charged.

FILES

equilibrium_inference_20261105.pdf    Main 13-page report.
equilibrium_inference_20261105.tex    Editable LaTeX source.
sources.json                        Primary references and pinned inputs.
environment.json                    Recorded execution environment.
SHA256SUMS.txt                       Integrity hashes of delivered files.

passive_programme/
  bandwidth_accuracy_theorem.md      Independent approximation proof.
  physical_operation.md              Acquisition and resource derivation.
  independent_audit.md               Internal review and scope cautions.
  response_compiler.py               Exact rational experiment compiler.
  response_certificate.json          Default exact finite certificate.
  verify_compiler.py                 Exact and finite-spectrum checks.
  compiler_checks.json               Executed compiler-check record.
  check_bandwidth_witnesses.py        Positive witness construction/checks.
  moment_witness_checks.json         High-precision witness record/spectra.
  saved_witness_checks.json          Reload verification of saved spectra.
  audit_grid.py                      Independent scalar-formula challenge.
  audit_grid.json                    Executed 120-case challenge record.
  make_figures.py                    Analytic scientific-plot source.
  resource_crossover.{pdf,png}        Main scaling-law figure.
  simple_witness.{pdf,png}            Simple positive spectral ambiguity.

quantum_companion/
  theorem.md                         Scoped scrambling/collision extension.
  verify.py                          Dense finite-circuit and group checks.
  verification.json                 Executed quantum checking record.

REPRODUCTION

The compiler itself uses only Python's standard library (Fraction).
The other checks require numpy and mpmath; figures require matplotlib.
The environment record lists versions used, not a claim that only those
versions work. LaTeX rebuilding needs pdflatex and the packages declared
in the .tex preamble. Run commands from the extracted package root.

  python3 passive_programme/response_compiler.py \
    --mu 1 --upper 16 --horizon 1/10 --epsilon 1/16 \
    --alpha 1/20 --output response_certificate.json

  python3 passive_programme/verify_compiler.py
  python3 passive_programme/check_bandwidth_witnesses.py
  python3 passive_programme/audit_grid.py
  python3 quantum_companion/verify.py
  python3 passive_programme/make_figures.py
  pdflatex -interaction=nonstopmode -halt-on-error equilibrium_inference_20261105.tex
  pdflatex -interaction=nonstopmode -halt-on-error equilibrium_inference_20261105.tex

Some verification scripts overwrite their own adjacent JSON output. Keep
the original package if comparing records. High-precision witness checks
can take longer than the standard-library compiler example. The saved
reload check is an executed audit record; it is not a separate CLI tool.

The compiler takes finite rational Lambda. The main theorem also covers
an unbounded upper-rate class, using a=0 in its analytic recipe. The
compiler's max-degree is a software limit, not an impossibility theorem.

INTERPRETING FINITE CERTIFICATES

The default example has mu=1, Lambda=16, T=0.1, epsilon=1/16, sigma=U=1
and confidence 0.95. This T is outside the narrower range chosen for the
asymptotic theorem, but the exact finite certificate remains valid. The
compiler returns degree 10, 11 bins, bias bound 0.012239727214128027,
log10 amplification 18.3946217056 and log10 sufficient repetitions
43.1362787277. These enormous costs are sufficient for this estimator;
they are not an evaluated optimum or a performed laboratory experiment.

The compiler allocates epsilon/4 each to bias, random readout error and
digitization, leaving epsilon/4 for other arithmetic/control/preparation
errors. Its rational upper enclosure avoids uncertain exponential
endpoint evaluation. It does not remove hardware calibration errors.

The independent moment-witness script uses an ideal-step/bin upper check,
exact exponential endpoints evaluated numerically and its own allocation.
Its finite upper counts and the rational ramp compiler's counts are not
interchangeable. For the lower witnesses, interpolation proves moment
equality. Tiny floating-point residuals do not prove the uniform bound;
the analytical Taylor remainder does. The report distinguishes the
uniform bound from smaller sampled discrepancies.

Only the sensor-noise model has matching upper and adaptive lower bounds.
The extra thermal model has an upper variance calculation and an explicit
Theta T/sigma^2 factor; its parameter-dependent covariance requires a
different lower-bound analysis.

The quantum companion is explicitly compared with the 2023 radiative
random-circuit paper. It pays for source control, outputs, inverse gates,
memory, routing, key records and error protection. It does not solve the
preserved optimal joint receiver memory/processing problem.

PROVENANCE

The authors of the cited prior research receive credit for their results.
The present proof and code were constructed and checked within this
session using independent mathematical routes. All checks in the JSON
records were actually executed; no physical trials were performed. The
pinned Astra inputs and preserved earlier reports are referenced in
sources.json but are not copied wholesale into this package. No external
repository was modified or paper submitted.
