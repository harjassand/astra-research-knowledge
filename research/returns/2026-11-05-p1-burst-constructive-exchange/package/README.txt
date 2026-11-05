A SHARP TAIL BOUNDARY FOR RECOVERABLE INFORMATION
Constructive question-level exchange, 5 November 2026

START HERE

Read burst_recoverability_exchange_20261105.pdf for the integrated result,
proof, comparison and resource accounting. Its LaTeX source is
exchange_report.tex. All paths below are relative to this package directory.

COMPLETED MAIN RESULT

For instantaneous Poisson cube bursts in ambient dimension d with strict
Pareto radius tail Pr(R>r)=r^(-alpha), alpha>d, the fixed-finite-seed,
horizon-uniform classical-bit recovery operation is achievable at sufficiently
small positive intensity if and only if alpha>d+1. The positive construction
uses bounded binary registers, density, degree, range, speed and gate rate.
Every mutable register is corruptible. Immutable gate laws and an
input-independent horizon-specific schedule are granted under the producer's
final refinement. Initialization, growth, transport, waiting, local decoding
and delivery exposure are included.

For a fixed family with z=log(U)/log(B) in (1,alpha-d), active mutable cells
are O(T^(1/z)), delivery is O(T), and local work is O(T^(1+1/z)). This approaches
the necessary spatial-extent exponent, not a universal full-hardware optimum.

Proof order:
  p3_construction.md
  p3_compiler_lemma.md
  p3_independent_audit.md

The two-round gadget supersedes the earlier redundant three-round version.
Finite checkers verify the semantic core; they do not simulate or prove the
entire hierarchy. The hierarchy proof uses the explicit deterministic support
projection, actual marked-Poisson independence, staged prewarming and local
scale-conversion interfaces.

COMPANION RESULTS AND GOVERNING ORDER

P2: p2_bypass.md gives finite Gaussian replacement and direct preparation of
the original sine family at a chosen fixed strength eta=1/2, independently of
an unknown constant force and arbitrary old reference, within the affine
Langevin class. Fine meter records and dither seeds must be isolated/disposed
of before reuse. The hidden marginal is the contemporary prepared marginal.

p2_c1_meter_completion.md is the final smooth-meter version and governs over
older rectangular and piecewise-linear switching entries. Its 100-piece
directed interval certificate covers 0<=k/(M gamma^2)<=1/4. Nominal 1.1/gamma
means the specified measurement-and-force schedule. Causal ADC/computation
latency, added readout noise, calibration acquisition, cold-pointer preparation,
finite range, overflow, record disposal and reuse are not supplied by that
number. No total-resource optimum or universal nonlinear campaign interface
is claimed. Point-fixture force actions and the interval candidate controller
are distinguished in the final note.

P1: p1_comparator.md proves an extensive direct-sum Fano minor for the actual
BDL physical Z-check matroid, at every fixed allowed subdivision parameter.
It excludes the regular-matroid route and both logarithmic graphic/cographic
defect guarantees of Code Swendsen-Wang. It does not prove slow mixing,
sampling hardness or a practical advantage. The prior accepted loading
compiler, equilibrium-inference and quantum results are unchanged.

REPRODUCTION

The main checks use Python 3.12. Recorded numerical environment:
  numpy 2.3.5
  scipy 1.17.0
  mpmath 1.3.0

Run from this directory. The independent P1 and P3 checkers use Python's
standard library and require no CMR executable or external repository.

  python3 p3_gadget_check.py
  python3 p3_two_round_check.py
  python3 verify_wheel_packing.py
  python3 bdl_subdivision_check.py

P2 point fixtures and independent full-state validation:

  python3 p2_general_reset.py
  python3 p2_c1_direct_sine_arm.py
  python3 p2_smooth_meter_validation.py

Continuum interval certificates (slower than point fixtures):

  python3 p2_general_reset.py --interval --pieces 100
  python3 p2_c1_direct_sine_arm.py --interval --pieces 100

The .json receipts are included. Their numerical inequalities, not rounded
summary values, are the certificate data. The uniform proof uses directed
intervals and exact decimal candidate weights; floating-point point optima
and ODE cross-checks are corroboration only.

The older no-pin rectangular and piecewise-linear variants and the earlier
pin-based probe are retained as development evidence. They are superseded
where the final C1 note says so. Some exploratory matroid helper scripts are
included for provenance; their optional CMR export/analysis entry points are
not required by the reproduction commands above. No CMR binaries are bundled.

To compile the report with a standard TeX Live installation, run twice:

  pdflatex -interaction=nonstopmode -halt-on-error exchange_report.tex

This produces exchange_report.pdf, equivalent in content to the named report.

SOURCE PROVENANCE

sources/p2_return.txt, p2_readme.md and p2_conditions.md are exact fetched
copies of the user-specified P2 opening at immutable Git commit:
  e9bd2054d8e396d82dc89d59b9851f1827fc55ef
Repository path:
  research/returns/2026-11-05-p2-intervention-stream-opening/

sources/p2_governing.md is the earlier local thermal intervention theorem at:
  3629d4ca14f495fb6999d2cd9bdd89a2be8c34ba
Path:
  research/returns/2026-11-05-p2-local-thermal-trials/package/thermal/
  LOCAL_THERMAL_INTERVENTION_THEOREM.md

sources/p3_return.txt, p3_report.txt and p3_refinement.md are exact fetched
copies of the user-specified P3 opening at:
  d0365eab6f9a362b526f4801db9cb950841e5d5d
Repository path:
  research/returns/2026-11-05-p3-burst-recoverability-opening/
The final uniform-horizon refinement governs earlier quantifiers.

The repository is https://github.com/harjassand/astra-research-knowledge .
The report includes all precise primary references. The extract of the
Balasubramanian-Davydova-Lake 2026 paper retains its CC BY 4.0 attribution.

EVIDENCE AND LIMITS

There were zero hardware trials. This package supplies a mathematical theorem,
explicit model constructions and reproducible certificates. It does not
establish historical priority, autonomous reliable control, damaged-gate
recovery, passive quantum burst memory, a positive information-density
theorem, the general finite-(d+1)-moment endpoint, or a laboratory intervention
apparatus. Those are not silently included in the completed strict-Pareto
classification.

MANIFEST.json records SHA-256 hashes of the packaged files. The manifest is
an integrity aid, not a proof. Numerical receipts are results of the checks
listed above; proof scope is explained in the corresponding notes.
