TWO CLOCKS FOR QUANTUM INFORMATION
Finite action law and output-only recovery through mixed collision baths
Research construction package, 5 November 2026

Start with tracial_acquisition.pdf. The note includes theorems, proofs, a finite
physical interface, all paid costs, primary/Astra comparisons, and limitations.

MAIN COMPLETED RESULT
A fresh, independent, maximally mixed collision bath exports source information
only at fourth order in weak interaction action. A weighted operator norm gives
a finite law for all retained outputs and their correlations, arbitrary receiver
processing, classical feedback, and bounded stopping with a pathwise action
budget. Its all-decoder lower bound is matched in scaling by an exact partial-
SWAP model whose receiver replaces the discarded source by a mixed dummy and
reverses the known collision circuit. It receives no bath purifiers.

Source forgetting has a quadratic weak-collision clock; output-only recovery
has a quartic clock. Identical exact source depolarizing dynamics on a sampled
time grid can therefore hide different physical output acquisition costs.

ERROR CONVENTION
The manuscript and proof supplements use HALF diamond distance, in [0,1].
Raw diagnostic fields explicitly named trace_distance or full_diamond are
unhalved; their field names and comparisons preserve that convention.

FILES
tracial_acquisition.pdf / .tex : Full research note and editable source.
theory_converse.txt           : Complete adaptive/pathwise theorem and proofs.
partial_swap_theory.txt       : Exact acquired channel, decoder and clocks.
physical_interface.txt        : Finite local schedule, calibration and errors.
prior_art_comparison.txt      : Strongest applicable primary/Astra alternatives.
sources.json                 : Source ledger and precise roles.
check_hot_bath.py             : Full finite-matrix channel/decoder diagnostics.
hot_bath_checks.json          : Executed small-system results and formula rows.
resource_analysis.py          : Exact resource calculations and figure generator.
resource_counts.json          : Necessary/sufficient finite resource counts.
figures/                     : Scientific plots, PDF and PNG.
SELECTION_RECORD.txt         : Independent question selection and decisive gaps.
WARM_RESULTS.txt              : Accepted prior results with retained conditions.
RESULT_SUMMARY.txt            : Portable factual research handoff.
runtime_versions.json         : Numerical runtime versions.
companions/                  : Other independently constructed openings.
SHA256SUMS.txt                : Hashes of delivered files, excluding itself.

REPRODUCTION
Run these commands from the extracted tracial_acquisition directory:
  python3 check_hot_bath.py
  python3 resource_analysis.py
  pdflatex -interaction=nonstopmode -halt-on-error tracial_acquisition.tex
Run pdflatex twice for references. Dependencies: Python 3, NumPy, SciPy,
Matplotlib, and a LaTeX installation with the packages in the source preamble.

Finite diagnostics retain all bath correlations and apply the source-discarded
dummy decoder. They cover 48 qubit partial-SWAP cases (N<=6), five d=3/4 cases
with entangled references, 80 generic-Hamiltonian transfer checks, and 12
measured-output feedback chains. No large-bath simulation, semidefinite optimum,
formal proof assistant, or hardware experiment is claimed. Large N values and
plots are evaluations of proved finite formulas.

The necessary-count rows in hot_bath_checks.json use the simpler valid bound
epsilon >= (1-d^-2) r/2. resource_counts.json uses the stronger centered
Renes bound and is the source of the manuscript's tighter resource table.
Their slightly different lower counts are different valid bounds, not two
different simulations of an optimum.

RESOURCES AND SCOPE
The input is arbitrary and can be entangled with an inaccessible reference.
Every incoming bath register is independent and maximally mixed, conditional
on the classical history. Initial purifiers and preparation keys are unavailable.
No emitted register returns to the actual source; no receiver quantum memory
couples back coherently. Arbitrary receiver instruments and genuine classical
feedback are allowed in the converse. The explicit decoder uses a known
collision circuit and N coherent stored outputs per source module.

The product-register law allows arbitrary collective final decoding and
arbitrarily entangled inputs, but assumes independent emission channels.
Cross-module active controls that destroy product emission are outside that law.

A full source SWAP is a simpler operation when available. Fixed-action collision
counts do not include free routing, calibration, hidden precision, idle
protection, or memory factories. The finite supplement pays these costs.
Exact traciality and local coupling reach are architecture assumptions, not
facts certified by short source-only observations.

Pure coherent ports, bath preparation labels, returning particles, nontracial
probes, and coherent feedback are different supplied resources. No arbitrary
finite-temperature bosonic bath or general many-body noisy hardware theorem
is asserted. The fixed-rate continuous limit requires increasing peak coupling;
the bounded-strength finite clock is stated separately.

STATUS AND PROVENANCE
This is a completed in-session mathematical construction with explicit finite
operations and finite-matrix evidence. It uses established recovery machinery
and accepted Astra results. It is not an exhaustive historical-priority search
or a demonstrated civilization-changing technology. No external repository
was modified and no external scientific publication was submitted.

Governing Astra revision for accepted baselines and warm results:
324acb589443002bf8d529cc15e160129c5e36d2.
