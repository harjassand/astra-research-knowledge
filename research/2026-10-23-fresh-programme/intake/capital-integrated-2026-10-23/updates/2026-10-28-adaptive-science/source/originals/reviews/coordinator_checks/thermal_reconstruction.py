"""Independent physical-coordinate check; not an all-network proof."""
from fractions import Fraction as Q
from pathlib import Path
import json
import mpmath as mp

mp.mp.dps = 80

def real(q):
    q = Q(q)
    return mp.mpf(q.numerator) / q.denominator

def check(name, masses, springs):
    masses, springs = list(map(Q, masses)), list(map(Q, springs))
    n = len(masses) + 1
    d0 = mp.matrix(n)
    for i, (m, k) in enumerate(zip(masses, springs), 1):
        d0[0, 0] += real(k)
        d0[i, i] = real(k / m)
        d0[0, i] = d0[i, 0] = -real(k) / mp.sqrt(real(m))
    dpi = d0.copy()
    dpi[0, 0] += 4
    alpha = list(mp.eigsy(d0, eigvals_only=True))
    beta = list(mp.eigsy(dpi, eigvals_only=True))
    assert abs(alpha[0]) < mp.mpf('1e-65')
    alpha[0] = mp.mpf(0)
    assert all(alpha[i] < beta[i] for i in range(n))
    assert all(beta[i] < alpha[i + 1] for i in range(n - 1))
    bands = [(mp.sqrt(a), mp.sqrt(b)) for a, b in zip(alpha, beta)]
    def bose(w):
        return (w / mp.sinh(w)) ** 2 if w else mp.mpf(1)
    conductance = sum(mp.quad(bose, [a, b]) for a, b in bands)
    compliance = sum((m * m / k for m, k in zip(masses, springs)), Q(0))
    trace = sum(beta) - sum(alpha)
    product = mp.fprod(beta) / mp.fprod(alpha[1:])
    moment = (sum(1 / b for b in beta) - sum(1 / a for a in alpha[1:]) - mp.mpf(1)/2) / 2
    assert abs(trace - 4) < mp.mpf('1e-65')
    assert abs(product - 2) < mp.mpf('1e-65')
    assert abs(moment - real(compliance) / 4) < mp.mpf('1e-65')
    return {
        'name': name,
        'total_mass_exact': str(1 + sum(masses, Q(0))),
        'total_internal_spring_exact': str(sum(springs, Q(0))),
        'compliance_exact': str(compliance),
        'bands': [[mp.nstr(x, 55) for x in p] for p in bands],
        'conductance': mp.nstr(conductance, 55),
        'trace_residual': mp.nstr(abs(trace - 4), 5),
        'log_moment_product_residual': mp.nstr(abs(product - 2), 5),
        'negative_cubic_moment_residual': mp.nstr(abs(moment - real(compliance)/4), 5),
    }

cases = [
    check('requested_cap_pendant', [Q(1)], [Q(4)]),
    check('severe_cap_pendant', [Q(1)], [Q(20)]),
    check('severe_cap_positive_two_pendant', [Q(1,20), Q(19,20)], [Q(5), Q(1805,99)]),
]
out = {
    'method': 'independent original-coordinate mass-normalized matrices, full eigenvalues and separate Bose quadrature',
    'precision_decimal_digits': mp.mp.dps,
    'cases': cases,
    'severe_cap_improvement': mp.nstr(mp.mpf(cases[1]['conductance']) - mp.mpf(cases[2]['conductance']), 50),
    'scope': 'high-precision floating reconstruction; not intervals, a global optimum proof, device validation or priority',
}
target = Path(__file__).with_name('thermal_reconstruction.json')
target.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
