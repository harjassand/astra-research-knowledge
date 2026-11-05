CAUSAL RECOVERY FROM A HOMOGENEOUS WEAK QUANTUM STREAM
Research construction, proofs, and reproducibility package -- 5 November 2026

STATUS
The selected full endpoint remains unresolved. No causal sublinear-memory
decoder with the required joint angle/error/count and processing guarantees
is constructed. The new general lower bound is Omega_theta(N/log N) at the
benchmark count with theta fixed; it is not a matching Omega(N) result and
is not uniform in the weak-angle limit.

MAIN DELIVERABLE
output/pdf/causal_recovery_research_note.pdf
The report gives the model, prior benchmark, general instrument witness,
complete crossing/interpolation proof, asymptotic consequence, finite-memory
floors, exact carrier-erasure theorem, source attribution, and limitations.

PROOF MAP
operational_constructor/crossing_gap_proof.md
  All-prefix singular gap and its memory consequence. Partial transpose and
  analytic continuation occur in a converse, not in a physical receiver.
channel_constructor/crossing_gap_audit.txt
  Independent check of crossing, normalizations, interpolation and asymptotics.
channel_constructor/sharp_profile_and_gap_audit.txt
  Full refined-instrument witness, sharp Petz energy, branch tails, and exact
  two-/three-carrier coefficient analysis; includes erasure audit.
algebra_constructor/renes_profile_audit.txt
  Separate self-contained check of the sharp recovery inequality and cap.
root_analysis/erasure_theorem.txt
  Exact retained-carrier recurrence, physical decoder, all-decoder bound,
  iid loss threshold, and untouched-subset budget. These restricted erasures
  are not interchangeable with arbitrary coherent receiver compression.
operational_constructor/pauli_completion_obstruction.md
  Exact irreversible loss for a specified attempted receiver instrument.

FAST REPRODUCTION (Python 3, from the unpacked top-level directory)
python3 root_analysis/erasure_check.py
python3 operational_constructor/check_crossing_gap.py
python3 channel_constructor/leading_gap.py
python3 operational_constructor/check_pauli_completion_floor.py
python3 root_analysis/pauli_completion_check.py

The first, second, fourth and fifth commands write JSON receipts beside their
scripts. leading_gap.py prints an exact SymPy matrix/eigenvalue certificate.
The numerical checks are finite floating-point corroboration, not proofs.
The analytic proofs do not depend on extrapolating numerical spectra.

OPTIONAL EXPLORATORY CALCULATIONS
python3 root_analysis/spectrum.py
python3 root_analysis/invariant_spectrum.py
The first covers full operator spaces only through four carriers. The second
covers the SU(2)-scalar sector only through seven carriers. Its second singular
value is not automatically the second singular value on the entire space.
Neither establishes a large-prefix asymptotic by numerical fitting.

REBUILD THE REPORT
python3 root_analysis/make_loss_figure.py
Then, from output/pdf, run twice:
pdflatex -interaction=nonstopmode -halt-on-error causal_recovery_research_note.tex
The report source includes crossing_section.tex. The plotted large-count
quantities evaluate exact formulas; no 43,462-qubit density matrix was simulated.

DEPENDENCIES
NumPy is used by the dense checks; SciPy by exploratory singular-value code;
SymPy by the exact coefficient certificate; Matplotlib by the scientific plot.
tested_runtime.json records the actual versions used in this session.
PDF creation used pdfTeX/TeX Live 2023 with standard LaTeX packages.

PRIOR SOURCES AND ATTRIBUTION
root_analysis/inputs holds retrieved Astra governing sources and a text
extraction of the earlier general-memory note. These are prior work and are
not new derivations from this run. source_manifest.json gives exact identities
and primary research links. The report separates the established Petz and
R-matrix machinery from the bounds derived here. No exhaustive priority claim
or peer-review certification is made.

CHECKSUMS
CHECKSUMS.sha256 identifies every included file other than itself. Rendered
page images, transient build logs, caches, and abandoned progress notes are
excluded from the deliverable.
