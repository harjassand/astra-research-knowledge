#!/usr/bin/env python3
"""Exact SU(2) checks of the coherent first-bias normalization.

For spin j=n/2, the highest Dynkin label is n and the complementary-root
shift is the positive root alpha. In the physical J_z coordinate the
coherent symbol of alpha is the Bloch coordinate z. The exact beta integral
computes Tcal(z) and checks Delta(J_z)=Tcal(z)=J_z/(j+1). This is a finite
normalization check only; the all-face proof is analytic and in RESULT.txt.
"""

from fractions import Fraction
from math import comb, factorial
import json
from pathlib import Path


def beta_int(a: int, b: int) -> Fraction:
    """Integral_0^1 u^(a-1)(1-u)^(b-1) du, for positive integers."""
    return Fraction(factorial(a - 1) * factorial(b - 1), factorial(a + b - 1))


def diagonal_tcal_z(n: int, k: int) -> Fraction:
    """Diagonal <m|Tcal(z)|m> for spin n/2, m=k-n/2."""
    # |<j,m|z,phi>|^2 = binom(n,k) u^k(1-u)^(n-k),
    # with u=cos^2(theta/2) uniform on [0,1], z=2u-1 and d=n+1.
    weight = comb(n, k)
    i0 = weight * beta_int(k + 1, n - k + 1)
    i1 = weight * beta_int(k + 2, n - k + 1)
    return Fraction(n + 1) * (2 * i1 - i0)


def main() -> None:
    records = []
    for n in range(1, 41):
        j = Fraction(n, 2)
        for k in range(n + 1):
            m = Fraction(2 * k - n, 2)
            observed = diagonal_tcal_z(n, k)
            expected = m / (j + 1)
            assert observed == expected
            psi_jz = m - observed
            assert psi_jz == j / (j + 1) * m
            records.append({
                "dynkin_label": n,
                "magnetic_weight_twice": 2 * k - n,
                "Tcal_root_symbol": str(observed),
                "Delta_Jz": str(m - psi_jz),
                "expected_Delta_Jz": str(expected),
            })

    out = {
        "status": "FINITE-EXACT-SU2-CHECK",
        "scope": "Exact beta-integral verification of the spin-j first-bias sign and normalization for labels 1 through 40; not a proof for other groups.",
        "cases": len(records),
        "identity": "Tcal(z)=J_z/(j+1), Psi(J_z)=j J_z/(j+1), Delta(J_z)=J_z/(j+1)",
        "records": records,
    }
    path = Path(__file__).with_name("su2_first_bias_check.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({key: value for key, value in out.items() if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
