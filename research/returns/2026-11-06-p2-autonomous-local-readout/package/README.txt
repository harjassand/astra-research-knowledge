A TIMING COST OF LOCAL QUANTUM READOUT IN AUTONOMOUS NOISY DYNAMICS
Research continuation and complete proof package
5 November 2026

MAIN RESULT
For finite-dimensional, bounded-strength, time-independent local Lindblad
dynamics, a robust unknown-qubit output at a fixed compact port at a public
time T requires N = Omega(T) registers, at fixed positive permitted burst
intensity. This allows the known-controller startup. It does not invoke
arbitrary-junk restart. The derived all-register-time bound is Omega(T^2).

The proof includes an exact admissible assignment from the original Poisson
burst process, a conditional-information budget, a Poisson smoothness bound,
and a local Choi-positivity argument that includes coherent Hamiltonian
terms. It is a new derivation relative to the supplied record, without an
independent review or literature-priority claim.

STATUS AND LIMITS
The accepted synchronous sparse and reusable constructions are preserved.
The positive autonomous acquisition/computation/delivery construction is
not completed. A matching upper bound is not claimed. The new lower bound
concerns a fixed-time compact-port output; a causal random-completion
interface is different and remains unconstructed here.

FILES
- autonomous_local_readout_bound.pdf: full statement, proof, scope and sources.
- autonomous_local_readout_bound.tex: editable mathematical source.
- check_readout_bound.py: finite matrix/inequality diagnostics.
- finite_checks.json: complete diagnostic results.
- retained_failures_and_scope.txt: invalid inferences and the open operation.
- accepted_sparse_report.txt: exact pinned predecessor proof record.
- accepted_reusable_report.tex: exact pinned reusable construction.
- MANIFEST.json: hashes and source provenance.

VALIDATION
Run python check_readout_bound.py (Python, NumPy and SciPy).
The diagnostics include 54 local uniformization cases, 12 exact qubit
positivity-boundary cases, 100 information-drain cases, 18 Poisson
smoothness cases, and the Bell-witness operator identity. They do not
simulate an autonomous fault-tolerant processor or estimate a threshold.
The PDF was compiled with pdflatex and every page visually inspected.

ACCEPTED CAPITAL
Repository: harjassand/astra-research-knowledge
Commit: 6113f5274d937b751f632a82e03e7f63bf0d234a
Directory: research/returns/2026-11-05-p2-sparse-autonomous-processor/package
report.txt Git blob: cc603fc1209aa8b247cc01adac3b34b39b2902bd
accepted_reusable_report.tex Git blob:
5135cc7292968fb22225d88b16766cbf168f3f9e
Both included predecessor files were checked against those exact blob hashes.

GOVERNING LITERATURE
Dunnweber, Styliaris and Trivedi, arXiv:2601.20818v3, II.2 and VII.
Brandao, Christandl and Yard, arXiv:1010.1750v5, corrected one-way-LOCC
conditional-information theorem.
Prech et al., arXiv:2406.19450v2, clock-uncertainty context.
Demkowicz-Dobrzanski et al., arXiv:1704.06280v3, noisy-metrology context.
Full references and precise import boundaries are in the report.
