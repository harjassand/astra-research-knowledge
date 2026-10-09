#!/usr/bin/env python3
"""Recompute amplitude spot checks at 80 digits; this is not interval rounding."""
import json
from pathlib import Path

import mpmath as mp

from amplifier_search import amplitude

mp.mp.dps = 80
worst = 0.0
count = 0
for gain in [1.1, 1.5, 2.0, 3.0]:
    for m in range(4):
        for n in range(4):
            for p in [0, 1, 2, 3, 8, 20, 40, 80, 119]:
                q = p - m + n
                if q < 0:
                    continue
                shift = p - m
                gg = mp.mpf(str(gain))
                t = mp.sqrt((gg - 1) / gg)
                sech = 1 / mp.sqrt(gg)
                pref = mp.sqrt(mp.factorial(m) * mp.factorial(n)
                               * mp.factorial(p) * mp.factorial(q))
                result = mp.mpf("0")
                for ell in range(max(0, -shift), min(m, n) + 1):
                    result += ((-1) ** ell * t ** (shift + 2 * ell)
                               * sech ** (m + n - 2 * ell + 1) * pref
                               / (mp.factorial(ell) * mp.factorial(shift + ell)
                                  * mp.factorial(m - ell) * mp.factorial(n - ell)))
                worst = max(worst, abs(amplitude(p, q, m, n, gain) - float(result)))
                count += 1
data = {"mpmath_digits": 80, "amplitude_spotcheck_count": count,
        "maximum_absolute_amplitude_error": worst, "rounding_certification": False}
(Path(__file__).parent / "verification.json").write_text(json.dumps(data, indent=2))
print(json.dumps(data))
