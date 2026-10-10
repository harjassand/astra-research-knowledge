"""Exact iid edge-failure baseline for K_10 with p=1/47."""
from fractions import Fraction
from math import comb

p = Fraction(1, 47)
connected = [Fraction(0), Fraction(1)]
for n in range(2, 11):
    connected.append(
        Fraction(1)
        - sum(
            Fraction(comb(n - 1, j - 1))
            * connected[j]
            * p ** (j * (n - j))
            for j in range(1, n)
        )
    )

independent_outage = 1 - connected[10]
polynomial_outage = p**2
print("iid outage, exact:", independent_outage)
print("iid outage, decimal:", float(independent_outage))
print("polynomial-law outage:", polynomial_outage, float(polynomial_outage))
print("outage ratio:", float(polynomial_outage / independent_outage))
