#!/usr/bin/env python3
"""Exact affine Stein-inverse identities; no oracle or sampler claim."""
from fractions import Fraction
import json
import math
from pathlib import Path


def exact_check(n, lam=Fraction(3, 5), a=Fraction(4, 5)):
    assert lam * lam + a * a == 1
    r = lam / a
    # Input He_n(G), output sum b_q He_(n-q)(G) He_q(Z).
    b = [(-r) ** q * math.comb(n, q) / (a * (q + 1) * (q + 2))
         for q in range(n + 1)]
    for q in range(n + 1):
        lhs = a * (q + 2) * b[q]
        if q:
            lhs += lam * (n - q + 1) * b[q - 1]
        assert lhs == (1 if q == 0 else 0), (n, q, lhs)
    j2 = sum(b[q] ** 2 / math.comb(n, q) for q in range(n + 1))
    j2_formula = sum(r ** (2 * q) * math.comb(n, q)
                     / (a * a * (q + 1) ** 2 * (q + 2) ** 2)
                     for q in range(n + 1))
    assert j2 == j2_formula
    # Parent-supplied source-adjoint gauge, checked in every scalar bidegree.
    for p in range(n + 1):
        m = n - p
        # u=-He_p He_(m+1)/(n+2), J_G=p He_(p-1)He_(m+1)/(n+2),
        # J_Z=-(p+1)He_p He_m/(n+2). Divergence coefficient:
        assert Fraction(p - (p + 1), n + 2) == -Fraction(1, n + 2)
        # D_Gu+J_G=0 and D_Zu+J_Z=-R, exactly.
        assert -Fraction(m + 1, n + 2) - Fraction(p + 1, n + 2) == -1
    return {"n": n, "exact_identities": True, "J_norm": math.sqrt(float(j2))}


def logsumexp(values):
    top = max(values)
    return top + math.log(sum(math.exp(v - top) for v in values))


def log_norms(n, lam=0.6):
    a = math.sqrt(1.0 - lam * lam)
    r = abs(lam / a)
    logs = []
    for q in range(n + 1):
        choose = (math.lgamma(n + 1) - math.lgamma(q + 1)
                  - math.lgamma(n - q + 1))
        logs.append(2 * q * math.log(r) + choose - 2 * math.log(a)
                    - 2 * math.log(q + 1) - 2 * math.log(q + 2))
    j = 0.5 * logsumexp(logs)
    u = 0.5 * logsumexp([v + math.log(q + 1) for q, v in enumerate(logs)])
    dzu = 0.5 * logsumexp([v + 2 * math.log(q + 1) for q, v in enumerate(logs)])
    dgu = (0.5 * logsumexp([logs[q] + math.log(n - q) + math.log(q + 1)
                            for q in range(n)]) if n else -math.inf)
    lower = (-(n + 1) * math.log(a) - math.log(n * lam * lam + 1)
             - math.log(n * lam * lam + 2))
    upper = (-(n + 1) * math.log(a)
             + math.log(min(0.5, 1 / ((1 - a) ** 2 * (n + 1) * (n + 2)))))
    assert lower <= j + 2e-10
    assert j <= upper + 2e-10
    return {"n": n, "lambda": lam, "a": a,
            "log10_J": j / math.log(10), "log10_u": u / math.log(10),
            "log10_DZu": dzu / math.log(10),
            "log10_DGu": (dgu / math.log(10) if n else None),
            "log10_J_lower": lower / math.log(10),
            "log10_operator_upper": upper / math.log(10)}


def main():
    exact = [exact_check(n) for n in [0, 1, 2, 5, 10, 25, 50, 100]]
    table = [log_norms(n, lam) for lam in [0.1, 0.3, 0.6]
             for n in [0, 10, 100, 1000, 10000]]
    result = {"exact_checks": exact, "log10_norm_table": table,
              "scope": "Affine Gaussian analytic identities only; no sampler."}
    dest = Path(__file__).with_name("affine_hermite_results.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print("Exact rational identities passed for n=0,1,2,5,10,25,50,100.")
    print("lambda    n      log10 ||J||    log10 ||u||    log10 ||D_Zu||")
    for row in table:
        print(f"{row['lambda']:4.1f} {row['n']:6d} "
              f"{row['log10_J']:15.6f} {row['log10_u']:15.6f} "
              f"{row['log10_DZu']:18.6f}")
    print(f"Saved {dest}")


if __name__ == "__main__":
    main()
