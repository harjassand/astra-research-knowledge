# Exact evidence and portable replay

Python uses the standard library. From the package root:

    python contributions/four_call_representation.py --output /tmp/pro1_cycle5_representation.json
    python contributions/four_call_nonscalar_witness.py
    python contributions/four_call_susceptibility_replay.py --max-n 6 --output /tmp/pro1_cycle5_susceptibility.json

The witness script reads the packaged exact matrix and replaces its own
local JSON receipt. Preserve a source copy if comparing original resource costs.
The first script derives the complete polynomial from infinite-tree path
rules, checking Gram identity, diagonal drift, parity and the top-color
counterexample. Four calls inspect only a finite prefix; this is not a
reflecting-bath approximation.
The second verifies the owner rho4 drift for all b by exact polynomial algebra.
The third computes only uniform-prefix susceptibility, not operator negativity
or a large-k law. The proof, not finite check count, establishes asymptotics.

Build the proof with: python build_pdf.py (pdflatex required).
Run python verify_package.py for manifest and unchanged-parent identity.
Integrity checks are not mathematical certification.
