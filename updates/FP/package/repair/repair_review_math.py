"""Exact first-step review of the proposed two-template repair CTMC.

Run: python3 repair_review_math.py
This is a hypothetical state model, not fitted enzyme kinetics.
"""

from fractions import Fraction as F
import json


def mean_patch_lifetime(damage, repair, eligible):
    """0 -> R at 2*lambda*p, 0 -> I at 2*lambda*(1-p).

    R -> 0 at mu, R -> F at lambda; I -> F at lambda.
    F is absorbing. I represents a permanently ineligible single-copy lesion.
    """
    lam, mu, p = F(damage), F(repair), F(eligible)
    assert lam > 0 and mu >= 0 and 0 <= p <= 1
    return ((3 - 2 * p) * mu + 3 * lam) / (2 * lam * ((1 - p) * mu + lam))


def fast_repair_limit(damage, eligible):
    lam, p = F(damage), F(eligible)
    assert lam > 0 and 0 <= p <= 1
    return None if p == 1 else (3 - 2 * p) / (2 * lam * (1 - p))


def check():
    lam, mu = F(1), F(1000)
    cases = [F(1), F(999, 1000), F(99, 100), F(9, 10), F(0)]
    assert mean_patch_lifetime(lam, mu, F(1)) == (mu + 3 * lam) / (2 * lam * lam)
    assert mean_patch_lifetime(lam, mu, F(0)) == F(3, 2) / lam
    out = []
    for p in cases:
        value = mean_patch_lifetime(lam, mu, p)
        limit = fast_repair_limit(lam, p)
        if limit is not None:
            assert value <= limit
        out.append({
            "damage_rate": str(lam),
            "repair_rate": str(mu),
            "eligible_fraction": str(p),
            "mean_patch_lifetime": str(value),
            "infinite_repair_rate_limit": "unbounded" if limit is None else str(limit),
        })
    return out


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
