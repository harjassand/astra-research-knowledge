"""Independent, non-interval-certified quadrature for the thermal mixture tail.

For s>0, the Euler law has survival
  P(S>s)=2 sum_{n>=1} (-1)^(n+1) exp(-pi^2 n^2 s).
The corresponding density series is absolutely convergent away from zero.
Changing y=pi^2 n^2(s-c^2) keeps each quadrature on a fixed interval.
This script supplies a numeric check; REPORT.txt's theorem uses the elementary
exponential-moment tail bound and does not depend on these numbers.
"""

import json
import math


def simpson(function, left, right, steps):
    width = (right - left) / steps
    odd = sum(function(left + index * width) for index in range(1, steps, 2))
    even = sum(function(left + index * width) for index in range(2, steps, 2))
    return width / 3 * (function(left) + function(right) + 4 * odd + 2 * even)


def tail(c, steps):
    b = 1 / c
    cutoff = c * c

    def weight(s):
        coefficient = s * b * b
        return (1 + coefficient / 2) ** (-1.5) * math.exp(
            b * b / (8 + 4 * coefficient)
        )

    terms = []
    for n in range(1, 5):
        rate = math.pi**2 * n * n
        integral = simpson(
            lambda y: math.exp(-y) * weight(cutoff + y / rate), 0, 48, steps
        )
        terms.append(2 * (-1) ** (n + 1) * math.exp(-rate * cutoff) * integral)
    return sum(terms), terms


if __name__ == "__main__":
    checks = []
    for resolution in [1000, 2000, 4000, 8000, 16000]:
        value, terms = tail(1, resolution)
        checks.append({"steps": resolution, "delta_c1": value})
    print(
        json.dumps(
            {
                "status": "finite-tested; not interval-certified",
                "checks": checks,
                "terms_at_finest_resolution": terms,
                "analytic_upper_c1": 2
                * (2 / 3) ** 1.5
                * math.exp(-math.pi**2 + 1 / 12),
            },
            indent=2,
        )
    )
