"""Exact arithmetic checks for the broad EB-branch/Petz-square obstruction."""

import json
from pathlib import Path
import sympy as sp

d = sp.symbols("d", positive=True, integer=True)
lambda_clone = (d + 2) / (2 * (d + 1))
lambda_cap = (1 + 1 / sp.sqrt(d + 1)) ** 2 / 4
gap = sp.simplify(lambda_clone - lambda_cap)
claimed_gap = (sp.sqrt(d + 1) - 1) ** 2 / (4 * (d + 1))
assert sp.simplify(gap - claimed_gap) == 0

fixtures = []
for dim in range(2, 13):
    clone = sp.Rational(dim + 2, 2 * (dim + 1))
    cap = sp.simplify((1 + 1 / sp.sqrt(dim + 1)) ** 2 / 4)
    exact_gap = sp.simplify(clone - cap)
    assert exact_gap > 0
    fixtures.append({
        "dimension": dim,
        "clone_lambda": str(clone),
        "branch_square_cap": str(cap),
        "strict_gap": str(exact_gap),
    })

assert sp.Rational(5, 8) - sp.Rational(9, 16) == sp.Rational(1, 16)
record = {
    "status": "PASS_EXACT_SYMBOLIC_AND_DIMENSION_FIXTURES",
    "symbolic_gap_identity": sp.sstr(sp.factor(gap)),
    "fixtures": fixtures,
    "scope": "representation obstruction only; no EB-rounding counterexample",
}
Path(__file__).with_name("broad_branch_square_cap.json").write_text(
    json.dumps(record, indent=2) + "\n"
)
print(json.dumps({"status": record["status"], "qutrit_gap": "1/16", "fixtures": len(fixtures)}, indent=2))
