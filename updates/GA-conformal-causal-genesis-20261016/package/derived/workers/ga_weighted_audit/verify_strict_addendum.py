#!/usr/bin/env python3
"""Exact algebra checks for the strict-weight compactness audit."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import verify_weighted_audit as v


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]


def main():
    allocations = 0
    for m in range(3, 9):
        for twice_alpha in range(1, 2 * m + 1):
            alpha = F(twice_alpha, 2)
            for u, b, w, z in v.exponents(m, 4):
                beta = F(u, 2) + w + z
                if beta <= alpha:
                    continue
                theta = alpha / beta
                m_power = b + theta * u / 2
                r_power = (1 - theta) * (u + w + z)
                v.require(theta * beta == alpha, "strict defect exponent")
                v.require(r_power > 0, "strict residual exponent positive")
                v.require(m_power >= 0, "bounded full-gradient exponent nonnegative")
                v.require(m_power + r_power == m - alpha, "strict amplitude balance")
                allocations += 1

    for m in range(3, 9):
        v.require(
            sum(v.weight(e) <= 2 for e in v.exponents(m, 4)) == 5,
            f"strict alpha-one excludes exactly five monomials degree={m}",
        )

    psi = v.add(v.add(v.cosine(1, 1, -1), v.cosine(0, 1, -1)), v.cosine(1, 2, F(-1, 2)))
    sigma = F(2)
    for N in (1, 2, 7, 31):
        a, b, c, d, q = v.compatible_components(psi, {}, sigma, N)
        signed = v.average(v.multiply(b, v.determinant(a, b, c, d)))
        e_squared = v.average(v.power(q, 2)) + v.average(v.power(c, 2))
        v.require(e_squared > 0, f"boundary defect nonzero N={N}")
        v.require(
            signed * signed / e_squared == F(9, 10),
            f"UI boundary witness exact squared quotient N={N}",
        )

    sources = [
        CAMPAIGN / "root/STRICT_WEIGHT_COMPACTNESS_THEOREM.md",
        CAMPAIGN / "workers/ga_polynomial_genesis/CORE_THEOREM_v1.md",
    ]
    receipt = {
        "status": "PASS_FINITE_ALGEBRA_ONLY",
        "checks": len(v.CHECKS),
        "strict_monomial_allocations_checked": allocations,
        "boundary_witness": {
            "polynomial": "b det Dphi",
            "m": 3,
            "alpha": 1,
            "p": 2,
            "s": 4,
            "least_weight": 2,
            "signed_quotient_squared": "9/10",
            "full_gradients": "uniformly bounded in L-infinity by the explicit family",
        },
        "source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "scope": "Exact residual-exponent algebra and the declared boundary field; Vitali convergence and the general null-polynomial proof are analytic arguments in the audit, not machine formalization.",
    }
    destination = HERE / "STRICT_VERIFICATION_RECEIPT.json"
    destination.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: {len(v.CHECKS)} exact checks, {allocations} strict allocations; {destination}")


if __name__ == "__main__":
    main()
