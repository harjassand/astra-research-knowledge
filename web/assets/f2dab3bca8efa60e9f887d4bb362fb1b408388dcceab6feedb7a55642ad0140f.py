#!/usr/bin/env python3
"""Finite Decimal check of the center Chernoff-product envelope."""
from decimal import Decimal, getcontext

getcontext().prec = 90
D = Decimal

def center_chernoff(n: int) -> Decimal:
    N = D(n)
    # e^(s a) prod lambda/(lambda+s), s=N^2/4, a=1/N.
    value = (N / D(4)).exp()
    for r in range(1, 2*n + 1):
        lam = (D(r) + N/D(2))**2
        value *= lam / (lam + N*N/D(4))
    return value

def main() -> None:
    for n in range(1, 401):
        N = D(n)
        exact_bound = D(2) * (-N/D(40)).exp()
        value = center_chernoff(n)
        if value > exact_bound:
            raise SystemExit(f"failed at N={n}: {value} > {exact_bound}")
    print("PASS: center finite-product Chernoff bound <= 2 exp(-N/40), N=1..400")
    print("FINITE-EVIDENCE only; universal inequality follows from RESULT.txt proof.")

if __name__ == "__main__":
    main()
