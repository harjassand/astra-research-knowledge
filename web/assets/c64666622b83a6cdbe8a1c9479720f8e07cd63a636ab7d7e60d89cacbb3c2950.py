"""Small exact checks of the SU(q) stopped-filter extension.

No peer script is executed. These check transcription, not asymptotic proof.
"""
from pathlib import Path
import json
import time
import sympy as s

OUT = Path(__file__).with_name('su_q_generator_checks.json')
started = time.monotonic()


def kron_all(xs):
    z = s.ones(1, 1)
    for x in xs:
        z = s.kronecker_product(z, x)
    return z


def collective(t, n):
    eye = s.eye(t.rows)
    return sum((kron_all([t if i == j else eye for i in range(n)])
                for j in range(n)), s.zeros(t.rows ** n))


def first(rho, v, n):
    return sum((kron_all([v if i == j else rho for i in range(n)])
                for j in range(n)), s.zeros(rho.rows ** n))


def second(rho, v, n):
    return sum((2 * kron_all([v if i in (j, k) else rho
                             for i in range(n)])
                for j in range(n) for k in range(j + 1, n)),
               s.zeros(rho.rows ** n))


def zero(x):
    return all(s.expand(y) == 0 for y in x)


def generators(q):
    ts = []
    for i in range(q):
        for j in range(i + 1, q):
            x = s.zeros(q)
            x[i, j] = x[j, i] = s.Rational(1, 2)
            ts.append(x)
            y = s.zeros(q)
            y[i, j], y[j, i] = -s.I / 2, s.I / 2
            ts.append(y)
    for k in range(1, q):
        z = s.zeros(q)
        for i in range(k):
            z[i, i] = 1
        z[k, k] = -k
        ts.append(z / s.sqrt(2 * k * (k + 1)))
    return ts


rows = []
for q in (2, 3, 4):
    rho = s.eye(q) / q
    rho[0, 0] += s.Rational(1, 10 * q)
    rho[-1, -1] -= s.Rational(1, 10 * q)
    rho[0, 1] = rho[1, 0] = s.Rational(1, 20 * q)
    # Non-coordinate Hermitian axes also test imaginary and diagonal terms.
    t0 = s.zeros(q)
    t0[0, 1] = s.Rational(2, 7) + s.I / 11
    t0[1, 0] = s.conjugate(t0[0, 1])
    t0[0, 0], t0[-1, -1] = s.Rational(1, 5), -s.Rational(1, 5)
    t1 = s.zeros(q)
    t1[0, -1] = t1[-1, 0] = s.Rational(3, 13)
    t1[0, 0], t1[-1, -1] = s.Rational(2, 9), -s.Rational(2, 9)
    for n in (1, 2):
        for axis, t in enumerate((t0, t1)):
            mu = s.trace(t * rho)
            v = t * rho + rho * t - 2 * mu * rho
            r = s.I * (t * rho - rho * t)
            dvv = (t * v + v * t - 2 * s.trace(t * v) * rho
                   - 2 * mu * v)
            drr = s.I * (t * r - r * t)
            ell = 2 * n * mu
            dell = 2 * n * s.trace(t * v)
            k = kron_all([rho] * n)
            j = collective(t, n)
            bk = ell * k + first(rho, v, n)
            rk = first(rho, r, n)
            b2 = ((ell ** 2 + dell) * k + 2 * ell * first(rho, v, n)
                  + first(rho, dvv, n) + second(rho, v, n))
            r2 = first(rho, drr, n) + second(rho, r, n)
            tests = {
                'anticommutator': zero(bk - j * k - k * j),
                'rotation': zero(rk - s.I * (j * k - k * j)),
                'quadratic_signed_identity': zero(
                    b2 - r2 - 2 * (j * j * k + k * j * j)),
            }
            assert all(tests.values()), (q, n, axis, tests)
            rows.append({'q': q, 'N': n, 'axis': axis, **tests})

covariance = []
casimir = []
for q in (2, 3, 4):
    ts = generators(q)
    rho = s.diag(*[s.Rational(2 ** i, 2 ** q - 1) for i in range(q)])
    y = s.zeros(q)
    y[0, 1] = s.Rational(3, 7) + s.I / 5
    y[1, 0] = s.conjugate(y[0, 1])
    y[0, 0], y[-1, -1] = s.Rational(2, 3), -s.Rational(2, 3)
    z0 = s.trace(rho * y)
    cov = 0
    for t in ts:
        mu = s.trace(t * rho)
        v = t * rho + rho * t - 2 * mu * rho
        r = s.I * (t * rho - rho * t)
        cov += s.trace(y * v) ** 2 - s.trace(y * r) ** 2
    target = 2 * s.trace(rho * (y - z0 * s.eye(q))
                         * rho * (y - z0 * s.eye(q)))
    assert s.simplify(cov - target) == 0
    eta = min(rho.diagonal())
    margin = s.simplify(cov - 2 * eta ** 2 * s.trace(y * y))
    assert margin >= 0
    covariance.append({'q': q, 'form_identity': True,
                       'margin_above_2eta_squared': str(margin)})
    c2 = sum((collective(t, 2) ** 2 for t in ts), s.zeros(q ** 2))
    swap = s.zeros(q ** 2)
    for i in range(q):
        for j in range(q):
            swap[i * q + j, j * q + i] = 1
    cfund = s.Rational(q * q - 1, 2 * q)
    pair = 2 * cfund * s.eye(q ** 2) + swap - s.eye(q ** 2) / q
    assert zero(c2 - pair)
    casimir.append({'q': q, 'N': 2, 'swap_identity': True,
                    'maximum_eigenvalue_formula': str(s.Rational((q - 1) * (q + 2), q))})

# Exact negative boundary: anisotropic signed covariance is not globally PSD.
q = 3
ts = generators(q)
pure = s.diag(1, 0, 0)
y = s.sqrt(2) * ts[1]
negative = 0
for a, t in enumerate(ts):
    mu = s.trace(t * pure)
    v = t * pure + pure * t - 2 * mu * pure
    r = s.I * (t * pure - pure * t)
    coefficient = 2 if a == 0 else 1
    negative += coefficient * (s.trace(y * v) ** 2 - s.trace(y * r) ** 2)
negative = s.simplify(negative)
assert negative == -s.Rational(1, 2)

result = {
    'status': 'PASS_FINITE_TRANSCRIPTION_CHECKS',
    'scope': 'Exact small fixtures only; all-N theorem is analytic, not certified by checks.',
    'generator_fixtures': rows,
    'isotropic_covariance_fixtures': covariance,
    'casimir_fixtures': casimir,
    'anisotropic_global_psd_counterfixture': {'q': 3, 'quadratic_form': str(negative)},
    'elapsed_seconds': time.monotonic() - started,
    'peer_scripts_executed': False,
}
OUT.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('status', 'elapsed_seconds',
                                       'anisotropic_global_psd_counterfixture')}, indent=2))
