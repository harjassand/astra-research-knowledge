#!/usr/bin/env python3
"""Exact checks for the all-n r=0 spinor recoupling identity."""

from math import comb
import sympy as sp


def swap_sign(n: int, j: int) -> int:
    return (-1) ** (((n - j) * (n - j + 1)) // 2)


def recoupling(n: int) -> sp.Matrix:
    N, d = 2 * n + 1, 2**n
    ds = [comb(N, j) for j in range(n + 1)]
    out = sp.zeros(n + 1)
    for j in range(n + 1):
        for k in range(n + 1):
            total = sum(
                (-1) ** (j * k - ell)
                * comb(j, ell)
                * comb(N - j, k - ell)
                for ell in range(min(j, k) + 1)
            )
            out[j, k] = (
                sp.Rational(comb(N, j) * total, d)
                * sp.sqrt(sp.Rational(1, ds[j] * ds[k]))
            )
    return out


def main() -> None:
    for n in range(1, 9):
        F = recoupling(n)
        assert F == F.T, f"n={n}: not symmetric"
        assert F * F == sp.eye(n + 1), f"n={n}: not an involution"
        plus = sum(swap_sign(n, j) == 1 for j in range(n + 1))
        minus = n + 1 - plus
        evals = F.eigenvals()
        assert evals.get(1, 0) == plus, (n, evals, plus, minus)
        assert evals.get(-1, 0) == minus, (n, evals, plus, minus)
        print(
            f"n={n} d={2**n} size={n+1} "
            f"exact-symmetric/involutive; +/-=({plus},{minus})"
        )
    print("PASS: exact r=0 recoupling checks for n=1..8")


if __name__ == "__main__":
    main()
