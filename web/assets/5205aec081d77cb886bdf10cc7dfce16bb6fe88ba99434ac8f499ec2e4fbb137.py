#!/usr/bin/env python3
"""Exact rational checks for N129's page-4 constant-budget step.

The universal proof is given in RESULT.txt. This grid is a reproducible
diagnostic over exact fractions, not a substitute for that proof.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


OUT = Path(__file__).resolve().parent
SOURCE = (
    Path(__file__).resolve().parents[5]
    / "work/astra_prior/web/assets/"
    / "b0bef324a423b447a13b85ce392717f37ab3347cb2eb70843703c6add8b4842e.pdf"
)


def ceil_fraction(x: Fraction) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


epsilons = [Fraction(1, 4), Fraction(1, 7), Fraction(1, 64), Fraction(1, 1000)]
extras = [0, 1, 37]
cases = 0
for eps in epsilons:
    assert 0 < eps <= Fraction(1, 4)
    for d0 in range(129):
        threshold = max(3, ceil_fraction(Fraction(96 * d0, 1) / eps))
        for extra in extras:
            u = threshold + extra
            eta = min(Fraction(1, 32 * u), eps / (64 * u))

            # The two load-bearing constant inequalities, checked exactly.
            assert Fraction(3 * d0, u) <= eps / 32
            assert eta * u <= eps / 64

            # Exact downstream worst-case budgets (normalized by H).
            appended = Fraction(3 * d0, u)
            separator_loss = eta * u
            unpaired = eps / 64 + separator_loss + appended
            assert appended <= eps / 32
            assert separator_loss <= eps / 64
            assert unpaired <= eps / 16

            bad_unpaired_mass = unpaired / eps
            bad_comparison_mass = Fraction(12, 192)
            assert bad_unpaired_mass <= Fraction(1, 16)
            assert bad_comparison_mass == Fraction(1, 16)
            remaining_mass = Fraction(63, 64) - bad_unpaired_mass - bad_comparison_mass
            assert remaining_mass >= Fraction(55, 64)
            cases += 1

pdf_hash = sha256(SOURCE.read_bytes()).hexdigest()
checks = {
    "status": "PASS_EXACT_RATIONAL_GRID",
    "source_pdf_sha256": pdf_hash,
    "source_pdf_bytes": SOURCE.stat().st_size,
    "epsilon_values": [f"{x.numerator}/{x.denominator}" for x in epsilons],
    "D0_values": "all integers 0..128 inclusive",
    "U_values": "max(3, ceil(96*D0/epsilon)) plus offsets 0, 1, 37",
    "cases": cases,
    "arithmetic": "fractions.Fraction only; no floating point",
    "results": {
        "appended_over_H": "<= epsilon/32",
        "separator_loss_over_H": "<= epsilon/64",
        "unpaired_sum_over_H": "<= epsilon/16",
        "bad_unpaired_cluster_mass_over_H": "<= 1/16",
        "bad_comparison_cluster_mass_over_H": "= 1/16",
        "remaining_cluster_mass_over_H": ">= 55/64",
    },
    "scope": "Finite diagnostics only; RESULT.txt contains the all-parameter algebraic proof.",
}
(OUT / "CHECKS.json").write_text(json.dumps(checks, indent=2) + "\n")
print(json.dumps(checks, indent=2))
