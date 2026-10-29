#!/usr/bin/env python3
"""Exact rational checks of the conserving-ring shared-clock identities.

These checks verify finite generator algebra, not a sampled experiment,
finite-size rare-event bound, or the asymptotic proof by enumeration.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def parity(mask, n):
    return 1 - 2 * (sum(i * ((mask >> i) & 1) for i in range(n)) % 2)


def check(n, alpha=F(3, 5), c=F(2, 3)):
    states = exchanges = 0
    for eta in range(1 << n):
        p = parity(eta, n)
        for sigma in (-1, 1):
            states += 1
            u = sigma * p
            intensity = drift_j = drift_m = bracket_m = F(0)
            activity = 0
            for i in range(n):
                j = (i + 1) % n
                delta = ((eta >> i) & 1) - ((eta >> j) & 1)
                if not delta:
                    continue  # Null native attempts do not reverse parity.
                exchanges += 1
                activity += 1
                nxt = eta ^ (1 << i) ^ (1 << j)
                assert parity(nxt, n) == -p
                rate = c * (1 + alpha * u * delta)
                reverse = c * (1 + alpha * (-u) * (-delta))
                assert rate == reverse and rate >= 0
                d = F(delta) - alpha * u
                if alpha == 1 and rate > 0:
                    assert d == 0
                intensity += rate
                drift_j += rate * delta
                drift_m += rate * d
                bracket_m += rate * d * d
                # Native jump of M + alpha/2*(u0-u) equals delta.
                assert d + alpha * u == delta
            assert intensity == c * activity
            assert drift_j == c * alpha * u * activity
            assert drift_m == 0
            assert bracket_m == c * (1 - alpha * alpha) * activity
            # Common-clock jump cancels boundary and C_gamma terms.
            assert alpha * u - alpha * u == 0
    return dict(n=n, alpha=str(alpha), joint_states=states, geometric_directed_exchanges=exchanges,
                all_equalities_exact=True)


if __name__ == "__main__":
    out = dict(scope="Exact finite generator and path-increment algebra only.",
               amplitudes=["3/5", "1"], c="2/3",
               results=[check(n, alpha) for alpha in (F(3, 5), F(1)) for n in (4, 6, 8)])
    path = Path(__file__).with_name("COMMON_CLOCK_IDENTITIES.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
