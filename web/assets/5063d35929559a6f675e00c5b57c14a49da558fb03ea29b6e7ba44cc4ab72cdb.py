"""Finite diagnostics for polynomial normalization and counterexample legality."""
from fractions import Fraction
from math import ceil, comb, exp, factorial, log, log1p, sqrt
from pathlib import Path
import json


def unshifted_coefficients(n, h, maximum):
    values = [Fraction(1)]
    if maximum:
        values.append(Fraction(h))
    for k in range(1, maximum):
        values.append((h*values[k]-(n-k+1)*values[k-1])/(k+1))
    return values


exact_checks = 0
circle_checks = 0
for n in range(1, 65):
    maximum = min(n, 6)
    for h in range(-n, n+1, 2):
        positive, negative = (n+h)//2, (n-h)//2
        unshifted = unshifted_coefficients(n, h, maximum)
        for k in range(1, maximum+1):
            for beta in [Fraction(-1, 2), Fraction(0), Fraction(1, 2)]:
                coefficient = sum(
                    comb(positive, ell)*comb(negative, k-ell)
                    * (1-beta)**ell * (-1-beta)**(k-ell)
                    for ell in range(max(0, k-negative), min(k, positive)+1)
                )
                normalized = coefficient/comb(n, k)
                expanded = sum(Fraction(comb(k, ell), comb(n, ell))
                               * (-beta)**(k-ell) * unshifted[ell]
                               for ell in range(k+1))
                assert normalized == expanded
                exact_checks += 1
                radius = min(0.25, sqrt(k/(4.5*n)))
                circle_bound = (radius**(-k)/comb(n, k)
                                * exp((abs(h)+n*abs(float(beta)))*radius
                                      + 2.25*n*radius**2))
                assert abs(float(normalized)) <= circle_bound*(1+1e-12)
                circle_checks += 1

# Exact mean Casimir and bounded baseline spin for every N tested.
for n in range(1, 257):
    epsilon = Fraction(1, 4*n)
    rare_casimir = Fraction(n*(n+2), 4)
    target = (Fraction(3*n, 4)-epsilon*rare_casimir)/(1-epsilon)
    sectors = [(m, Fraction(m*(m+2), 4)) for m in range(n % 2, n+1, 2)]
    below = max((entry for entry in sectors if entry[1] <= target), key=lambda x: x[1])
    above = min((entry for entry in sectors if entry[1] >= target), key=lambda x: x[1])
    if below == above:
        baseline = below[1]
    else:
        upper_weight = (target-below[1])/(above[1]-below[1])
        assert 0 <= upper_weight <= 1
        baseline = (1-upper_weight)*below[1]+upper_weight*above[1]
    assert (1-epsilon)*baseline+epsilon*rare_casimir == Fraction(3*n, 4)
    assert above[0]**2 <= 16*n
    exact_checks += 3

x = Fraction(1, 4)
series = sum((2*k+1)*x**k for k in range(2, 101))
closed = x**2*(5-3*x)/(1-x)**2
assert series <= closed <= 9*x**2
exact_checks += 1

counterexamples = []
for n in [100, 10000, 1000000]:
    log_epsilon = min(-sqrt(n), -log(4*n))
    epsilon = exp(log_epsilon)  # Underflow only discards a negligible log1p correction.
    r = ceil(3*sqrt(n)/log(2))
    assert r <= n
    log_lower_plus_one = 2*log_epsilon+r*(log(2)-log1p(epsilon))
    assert log_lower_plus_one >= 0.99*sqrt(n)
    counterexamples.append({"N":n,"r":r,"r_over_N":r/n,
                            "log_rare_weight":log_epsilon,
                            "log_one_plus_chi_lower":log_lower_plus_one})

result = {"exact_checks":exact_checks,"circle_bound_checks":circle_checks,
          "counterexample_diagnostics":counterexamples,
          "scope":"Finite normalization/legality diagnostics, not theorem validation"}
Path(__file__).with_name('verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
