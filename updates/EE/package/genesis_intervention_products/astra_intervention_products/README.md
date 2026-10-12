# Intervention-product completion

Research candidate: no independent review or established historical priority.

- `proof_note.md`: assumptions, proofs, observable certificate, nonstationary acquisition, feedback bounds, access obstructions, and resource accounting.
- `verify.py`: exact rational finite-model falsification checks and six separately labeled floating finite-time diagnostics. Requires Python, SymPy, NumPy, SciPy.
- `verification_results.json`: executed check results, exact example, fitted coefficients, and counterexamples.
- `verification_summary.txt`: compact execution output.
- `sources.json`: selective primary-source/dependency record.

Run `python verify.py` to regenerate the results. The exact example fits the control coefficients using only observable moment matrices, then separately checks the hidden operator identity. The general statistical experiment and budgeted noisy optimizer are theorems/protocols, not implemented laboratory software. No physical samples were acquired.

The crucial access distinction: a product control is a setting with multiplied microscopic rate gains, not a sequence of two control pulses. Sequential pulses are used separately to measure mixed-time derivatives. Selective mode requires unchanged within-label off-diagonal transitions. Activity-complete mode replaces that requirement with a microscopic-event counter that need not identify the states.
