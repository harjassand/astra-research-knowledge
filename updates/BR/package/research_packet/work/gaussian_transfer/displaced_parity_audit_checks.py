"""Finite diagnostics for the separate parity audit; not a uniform proof."""
from fractions import Fraction as Q
import json
import math
import mpmath as mp


def exact_h(n, a, c):
    return sum((a / 2) ** j * c ** (n - 2 * j)
               / (math.factorial(j) * math.factorial(n - 2 * j))
               for j in range(n // 2 + 1))


def main():
    vals = [Q(0), Q(1, 100), Q(1, 4), Q(7, 2)]
    coefficient_checks = 0
    aggregate_checks = 0
    for a in vals:
        for c in vals:
            hs = [exact_h(n, a, c) for n in range(43)]
            for n in range(2, 41):
                assert hs[n] ** 2 >= hs[n - 2] * hs[n + 2]
                coefficient_checks += 1
            for b in vals:
                for h in [2, 7, 16, 40]:
                    ws = [b ** k * hs[h - k] ** 2 / math.factorial(k)
                          for k in range(h + 1)]
                    for k in range(2, h - 1):
                        assert ws[k] ** 2 >= ws[k - 2] * ws[k + 2]
                        aggregate_checks += 1

    mp.mp.dps = 90
    integral_checks = []
    for n, astr, cstr in [(1, '.25', '.01'), (7, '.25', '1e-20'),
                          (16, '2', '3'), (25, '.01', '20')]:
        a, c = mp.mpf(astr), mp.mpf(cstr)
        d = c / mp.sqrt(a)
        m = (d + mp.sqrt(d * d + 4 * n)) / 2
        b = (lambda t: -mp.expm1(-2 * d * t)) if n % 2 else (
            lambda t: 1 + mp.exp(-2 * d * t))
        def integrand(t):
            if not t:
                return mp.mpf(0)
            x = t - m
            return mp.exp(n * (mp.log1p(x / m) - x / m) - x * x / 2) * b(t) / b(m)
        integral = mp.quad(integrand, [0, m, m + 1, m + 10, mp.inf])
        estimate = (a ** (mp.mpf(n) / 2) * m ** n
                    * mp.exp(-(n / m) ** 2 / 2) * b(m) * integral
                    / (mp.factorial(n) * mp.sqrt(2 * mp.pi)))
        exact = mp.fsum((a / 2) ** j * c ** (n - 2 * j)
                        / (mp.factorial(j) * mp.factorial(n - 2 * j))
                        for j in range(n // 2 + 1))
        rel = abs(estimate / exact - 1)
        assert rel < mp.mpf('1e-60')
        integral_checks.append(dict(n=n, a=astr, c=cstr,
                                    relative_error=mp.nstr(rel, 8),
                                    normalized_integral=mp.nstr(integral, 20)))
    result = dict(status='PASS_FINITE_DIAGNOSTICS_ONLY',
                  exact_parity_logconcavity_checks=coefficient_checks,
                  exact_aggregate_parity_logconcavity_checks=aggregate_checks,
                  gaussian_moment_integral_checks=integral_checks)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
