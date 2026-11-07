COMPLETE CLASSICAL MEDIATION FOR NONCOMMUTING SPIN NETWORKS

Read REPORT.md for the full theorem, proof, assumptions and cost contract.
ENDPOINT.json records the exact scope. PREDECESSORS.json preserves earlier archives and statuses.

Executable files:
  mediation.py          Standard-library rational binary trajectory kernel and conservative step budget.
  exact_matrix.py       Exact rational-complex matrices, primal/dual checks and constructive PSD separation.
  validate_mediation.py Exact identities and explicitly separate small floating diagnostics.

Run: python validate_mediation.py
The validation uses NumPy and SciPy; the rational trajectory kernel itself does not.
The supplied seeded RNG is a smoke check. The sampling theorem requires independent uniform random bits.

REFERENCE_WITNESS.json contains the exact physical Pauli settings and a conservative paid acquisition bound.
VALIDATION.json records what was executed. The very large full compiler and physical witness budgets were not executed.

The package does not include a new general SDP implementation. The report supplies the constructive reduction, PSD separator, radii and bit contract for established rational convex optimization.
No physical experiment, outside communication, new worker, infrastructure or spend occurred.
