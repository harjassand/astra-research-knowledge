"""Finite exact arithmetic checks for clipping and integer streaming; not a proof audit."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import random

BASE = Path(__file__).parent
RNG = random.Random(9382)


def norm2(vector):
    return sum(x * x for x in vector)


def clip_round(w, n, p):
    h = F(1, 2**p)
    r2 = F(3, n)
    w2 = norm2(w)
    values = []
    for wa in w:
        lo, hi = 0, 2**p + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            feasible = (mid * h)**2 <= wa**2 if w2 <= r2 else (mid * h)**2 * w2 <= wa**2 * r2
            if feasible:
                lo = mid
            else:
                hi = mid
        values.append((1 if wa >= 0 else -1) * lo * h)
    return values


def main():
    count = 0
    clipping_count = 0
    for n in (4, 6, 8, 13, 50, 101):
        for a in (4, 8, 12):
            epsilon = F(1, 2**(2*a))
            p = 0
            while 2**(2*p) < 12 * n / epsilon:
                p += 1
            for _ in range(24):
                w = [F(RNG.randint(-100, 100), 100) for _ in range(3)]
                v = clip_round(w, n, p)
                assert norm2(v) <= F(3, n)
                w_float = [float(x) for x in w]
                scale = min(1, math.sqrt(3/n / float(norm2(w)))) if norm2(w) else 1
                y = [x * scale for x in w_float]
                assert sum((float(va) - ya)**2 for va, ya in zip(v, y)) <= 3 * 2**(-2*p) * (1 + 1e-9)
                clipping_count += 1
                for r in (2, n//2):
                    va = [int(x * 2**p) for x in v]
                    c = F(n * (r-1), n-1)
                    d = F(r * (r-1), n * (n-1)) * (n + n*n*norm2(v))
                    for axis in range(3):
                        for x in range(-r, r+1, 2):
                            t = (3*x*x - 3*r - 6*c*v[axis]*x + d)/r
                            numerator = (
                                3*n*(n-1)*r*2**(2*p)*(x*x-r)
                                - 6*n*n*r*(r-1)*2**p*va[axis]*x
                                + r*r*(r-1)*(n*2**(2*p)+n*n*sum(z*z for z in va))
                            )
                            denominator = n*(n-1)*r*r*2**(2*p)
                            assert F(numerator, denominator) == t
                            count += 1
    result = {
        "status": "FINITE_EXACT_ARITHMETIC_DIAGNOSTIC_ONLY",
        "integer_score_equalities": count,
        "clipping_cases": clipping_count,
        "seed": 9382,
        "scope": "Named finite rational examples. Confidence and mixture soundness remain analytic statements.",
    }
    (BASE / "calibration_diagnostic_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
