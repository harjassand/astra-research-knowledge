"""Finite convention checks. These diagnostics do not prove the theorems."""
import json
import math
from pathlib import Path


def z(s, r):
    return s + 1 if r == 1 else (1 - r ** (s + 1)) / (1 - r)


def spin_weights(k, delta):
    if delta == 1:
        return {k: 1.0}
    pp, pm = (1 + delta) / 2, (1 - delta) / 2
    r = pm / pp
    result = {}
    for ell in range(k % 2, k + 1, 2):
        q = (k - ell) // 2
        mul = math.comb(k, q) - (math.comb(k, q - 1) if q else 0)
        lp = math.log(mul) + ((k + ell) / 2) * math.log(pp)
        lp += ((k - ell) / 2) * math.log(pm)
        result[ell] = math.exp(lp) * z(ell, r)
    return result


def thin_weights(n, w, delta):
    result = [0.0] * (n + 1)
    for k in range(n + 1):
        bk = math.comb(n, k) * w ** k * (1 - w) ** (n - k)
        for ell, p in spin_weights(k, delta).items():
            result[ell] += bk * p
    return result


def master_bound(p, delta, cutoff):
    r = (1 - delta) / (1 + delta)
    good = [ell for ell in range(len(p)) if ell <= cutoff]
    c = max((ell + 1) / z(ell, r) for ell in good)
    numerator = 0.0
    min_gap = 1.0
    for ell in good:
        tl = (ell + 1) / z(ell, r)
        gl = z(ell, r * r) / z(ell, r)
        gl -= (ell + 1) * z(2 * ell, r) / ((2 * ell + 1) * z(ell, r))
        min_gap = min(min_gap, gl)
        numerator += p[ell] * tl * gl
    tail = sum(p[ell] for ell in range(len(p)) if ell > cutoff)
    return (2 / 3) * (numerator / c - tail), min_gap


fixtures = []
for n, w, delta in [(3, .65, 1 / 13), (20, .4, .7), (80, .65, .3),
                    (180, .8, .8), (80, .1, 1), (120, .6, .5)]:
    p = thin_weights(n, w, delta)
    g, kappa = w * delta, n * w * delta ** 2
    casimir = sum(prob * ell * (ell + 2) for ell, prob in enumerate(p))
    exact = 3 * n * w + n * (n - 1) * g ** 2
    centered = sum(prob * (ell - n * g) ** 2 for ell, prob in enumerate(p))
    mb, min_gap = master_bound(p, delta, 2 * n * g)
    assert abs(sum(p) - 1) < 2e-12
    assert abs(casimir - exact) < 2e-9
    assert centered <= 3 * n * w + 2e-9
    assert min_gap >= -2e-14
    simple = delta / 20 - 2 / kappa if kappa >= 64 else None
    if simple is not None:
        assert mb + 2e-12 >= simple
    fixtures.append(dict(n=n, w=w, delta=delta, kappa=kappa,
                         mass=sum(p), casimir_error=casimir-exact,
                         centered_second_moment=centered,
                         moment_upper=3*n*w, exact_master_bound=mb,
                         simplified_bound=simple))

r, t = .5, 1.0
a, s = math.atanh(r), math.hypot(math.atanh(r), t)
x, zz = t * math.tanh(s) / s, a * math.tanh(s) / s
qubit = dict(r=r, t=t, x=x, z=zz,
             error_lower=1 / (2 / x + 4 / (r-zz)))

# Audit the scalar log-bin inequality, including tiny and huge modular gaps.
max_ratio = 0.0
for j in range(1, 1501):
    gap = 10 ** (-7 + j * 10 / 1500)
    skew_fraction = 1 - 1 / math.cosh(gap / 2) if gap < 100 else 1.0
    # Cancellation-free evaluation near zero.
    if gap < 1e-3:
        skew_fraction = 2 * math.sinh(gap / 4) ** 2 / math.cosh(gap / 2)
    for width in [.01, .1, .7, 1.0]:
        ratio = min(1, gap / width) * width / math.sqrt(skew_fraction)
        max_ratio = max(max_ratio, ratio)
        assert ratio <= 4.0000001

# A common-width exponent check: after j pinches, exponent is
# (1-(2**j-1)*a)/2**j, and at j=k-1 this equals a.
recursion = []
for k in range(1, 9):
    aa = 1 / (2 ** k - 1)
    final = (1-(2 ** (k-1)-1)*aa) / (2 ** (k-1))
    assert abs(final-aa) < 1e-14
    recursion.append(dict(k=k, exponent=aa,
                          inherited_iteration=1/(3**(k-1))))

out = dict(status='finite diagnostics only', spin=fixtures,
           noncommuting_reference_witness=qubit,
           maximum_scalar_ratio=max_ratio, recursion=recursion)
Path(__file__).with_name('diagnostics.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
