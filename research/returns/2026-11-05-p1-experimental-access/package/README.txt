ASTRA P1 — QUANTUM EXPERIMENTAL ACCESS
Scientific return dated 5 November 2026, Australia/Brisbane

START HERE

Astra_P1_Quantum_Experimental_Access.pdf is the main, self-contained report.
It includes the exact access model, analytic diamond-norm proof, copy lower
bounds, explicit finite-slew meters, costs, comparison with ordinary methods,
validation, primary references, and remaining limits.

The completed result is a theoretical access hierarchy for initially unencoded
quantum experiments under independent hidden Z dephasing and a charged,
locality-resolved Hamiltonian budget. It is not a demonstrated device, a proof
of historical priority, or an impossibility theorem for every control regime.

CONTENTS

1. Astra_P1_Quantum_Experimental_Access.pdf — main report.
2. Astra_P1_Quantum_Experimental_Access.tex — complete editable LaTeX source.
3. verify_access.py — finite-model numerical falsification checks and figure.
4. verification_results.json — stored results from the checks.
5. access_scaling.png — illustrative copy-budget figure used in the report.
6. proof_audit.txt — important proof boundaries and resolved audit issues.
7. continuation_handoff.txt — compact scientific handoff and governing links.
8. causal_reset_decoder.txt — independent structured-receiver companion note.
9. expander_mixed_bath_companion.txt — independent mixed-output companion note.
10. environment_versions.txt — versions used for numerical checks/build.
11. SHA256SUMS.txt — hashes of the packaged files other than this manifest.

The two companion notes pursue different questions. They are preserved as
independent research constructions, not prerequisites or experimental
validation of the main theorem. Their separate assumptions and limitations
must be retained if their results are reused.

REPRODUCE

Requirements: Python 3 with NumPy, SciPy and Matplotlib; a LaTeX installation
with the packages imported in the source; pdflatex for the report.

In this directory:

    python3 verify_access.py
    pdflatex -interaction=nonstopmode -halt-on-error Astra_P1_Quantum_Experimental_Access.tex
    pdflatex -interaction=nonstopmode -halt-on-error Astra_P1_Quantum_Experimental_Access.tex

The Python script regenerates verification_results.json and access_scaling.png.
It checks 24 finite-slew meter cases, 60 shared-receiver evolutions, and records
16 constant-drive scalar optima. The finite examples do not test the full
diamond norm and do not replace the analytic proof. They are not interval
certificates. Small numerical or rendered differences across versions are
possible.

SOURCE AND CLAIM STATUS

The main theorem and explicit meter calculations are derived in the report.
Existing shadow statistics, noisy-learning results and fault-tolerant I/O are
credited in the bibliography. Governing Astra packets were inspected through
the GitHub connector at revision:

    8457e1084a3bcf3c4f8e3c7e4da9e0f5045a6570

The predecessor acquisition law and prepare-entanglement-first protocol were
accepted from the user's explicit factual handoff. Their private conversation
links are preserved in continuation_handoff.txt; this package does not claim
to reproduce those complete conversations.

No laboratory source, native many-body coupling, strict hard-bandwidth pulse
implementation, device economics or universal strong-control theorem is
supplied by this return.
