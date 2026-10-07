#!/usr/bin/env python3
"""Evaluate the exact origin Fisher-information constant for the quartic law.

This is a numeric check of the gamma-integral evaluation in INITIAL.txt; it is
not evidence about the finite-N quantum Fisher information or channel theorem.
"""

import math


def origin_fisher_information() -> float:
    # p(x) is proportional to exp(-a |x|^4), with a = 4/3. By isotropy,
    # Cov(X) = E[|X|^2] I_3 / 3, and the radial integrals are gamma integrals.
    a = 4.0 / 3.0
    return a ** (-0.5) * math.gamma(1.25) / (3.0 * math.gamma(0.75))


if __name__ == "__main__":
    information = origin_fisher_information()
    print(f"I_b(0,0) diagonal entry = {information:.12f}")
    print(f"asymptotic standard-error coefficient = {1 / math.sqrt(information):.12f}")
