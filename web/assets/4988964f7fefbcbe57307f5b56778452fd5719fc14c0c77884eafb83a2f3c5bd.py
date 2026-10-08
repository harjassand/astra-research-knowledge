#!/usr/bin/env python3
"""Independent arbitrary-precision recurrence check at mu=1000.

Uses mpmath and the unscaled coefficient recurrence (rather than the
log-domain double-precision implementation in exact_cp_audit.py). The
finite cutoff is far into the Chernoff tail; outputs are diagnostic, not
formal interval bounds.
"""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

RATES = ((1, 1, 4, 0), (0, 4, 1, 1))
MU = 1000
CUTOFF = 19150


def coefficients(mu: mp.mpf, rates: tuple[int, ...]) -> list[mp.mpf]:
    q = [mp.mpf(0)] * (CUTOFF + 1)
    q[0] = mp.mpf(1)
    for n in range(1, CUTOFF + 1):
        q[n] = (mu / n) * mp.fsum(
            j * rates[j - 1] * q[n - j]
            for j in range(1, min(len(rates), n) + 1)
            if rates[j - 1]
        )
    return q


def main() -> None:
    mp.mp.dps = 50
    mu = mp.mpf(MU)
    qs = [coefficients(mu, rates) for rates in RATES]
    p0 = [mp.exp(-6 * mu) * value for value in qs[0]]
    p1 = [mp.exp(-6 * mu) * value for value in qs[1]]
    h2 = mp.fsum((mp.sqrt(a) - mp.sqrt(b)) ** 2 for a, b in zip(p0, p1))
    d10 = mp.fsum(
        p1[n] * mp.log(qs[1][n] / qs[0][n])
        for n in range(2, CUTOFF + 1)
        if p1[n]
    )
    result = {
        "mu": MU,
        "cutoff": CUTOFF,
        "mpmath_dps": mp.mp.dps,
        "mass0_truncated": mp.nstr(mp.fsum(p0), 30),
        "mass1_truncated": mp.nstr(mp.fsum(p1), 30),
        "mu_H2": mp.nstr(mu * h2, 30),
        "target_mu_H2": mp.nstr(mp.mpf(3) / (2 * 41**3), 30),
        "mu_KL_1_to_0": mp.nstr(mu * d10, 30),
        "target_mu_KL": mp.nstr(mp.mpf(3) / 41**3, 30),
        "scope": "arbitrary-precision finite recurrence with truncation; diagnostic only, not interval-certified",
    }
    out = Path(__file__).with_name("high_precision_cp_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
