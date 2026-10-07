"""Exact finite checks for representation-valued filter kernels.

Own script, no peer execution. N is the number of physical sites, ell the
symmetric-power representation degree. The all-N argument is analytic.
"""
from pathlib import Path
import itertools
import json
import math
import time
import sympy as s

started = time.monotonic()
xs = s.symbols('x y z', real=True)
x, y, z = xs
pauli = [s.Matrix([[0, 1], [1, 0]]),
         s.Matrix([[0, -s.I], [s.I, 0]]),
         s.diag(1, -1)]
fund = [t / 2 for t in pauli]
r = (s.eye(2) + sum((m * t for m, t in zip(xs, pauli)), s.zeros(2))) / 2
point = dict(zip(xs, (s.Rational(1, 7), s.Rational(2, 9), s.Rational(1, 11))))
mp = s.Matrix([point[u] for u in xs])


def kron_all(vs):
    out = s.ones(1, 1)
    for v in vs:
        out = s.kronecker_product(out, v)
    return out


def collective(t, n):
    return sum((kron_all([t if i == j else s.eye(t.rows) for i in range(n)])
                for j in range(n)), s.zeros(t.rows ** n))


def first(rho, h, n):
    return sum((kron_all([h if i == j else rho for i in range(n)])
                for j in range(n)), s.zeros(rho.rows ** n))


def second(rho, h, n):
    return sum((2 * kron_all([h if i in (j, k) else rho for i in range(n)])
                for j in range(n) for k in range(j + 1, n)),
               s.zeros(rho.rows ** n))


def zero(a):
    return all(s.simplify(v) == 0 for v in a)


rows = []
for ell in (2, 3):
    p = ell + 1
    sym = s.zeros(2 ** ell, p)
    for word in itertools.product((0, 1), repeat=ell):
        j = sum(word)
        index = sum(bit * 2 ** (ell - 1 - i) for i, bit in enumerate(word))
        sym[index, j] = 1 / s.sqrt(math.comb(ell, j))
    raw = sym.H * kron_all([r] * ell) * sym
    rho_func = raw / s.trace(raw)
    rho = rho_func.subs(point).applyfunc(s.simplify)
    grads = [rho_func.diff(u).subs(point).applyfunc(s.simplify) for u in xs]
    hess = [[rho_func.diff(u, v).subs(point).applyfunc(s.simplify)
             for v in xs] for u in xs]
    reps = [sym.H * collective(t, ell) * sym for t in fund]
    for axis in (s.Matrix([0, 0, 1]),
                 s.Matrix([s.Rational(2, 3), s.Rational(1, 3), s.Rational(2, 3)])):
        t = sum((a * g for a, g in zip(axis, reps)), s.zeros(p))
        u0 = (axis.T * mp)[0]
        vf = axis - u0 * mp
        rf = -axis.cross(mp)
        # Derivatives of the fundamental-coordinate vector fields.
        dvv = -((axis.T * vf)[0] * mp + u0 * vf)
        drr = -axis.cross(rf)
        d_sigma_v = sum((a * g for a, g in zip(vf, grads)), s.zeros(p))
        d_sigma_r = sum((a * g for a, g in zip(rf, grads)), s.zeros(p))
        h_sigma_vv = sum((vf[i] * vf[j] * hess[i][j]
                          for i in range(3) for j in range(3)), s.zeros(p))
        h_sigma_rr = sum((rf[i] * rf[j] * hess[i][j]
                          for i in range(3) for j in range(3)), s.zeros(p))
        d_sigma_dvv = sum((a * g for a, g in zip(dvv, grads)), s.zeros(p))
        d_sigma_drr = sum((a * g for a, g in zip(drr, grads)), s.zeros(p))
        mu = s.trace(t * rho)
        for n in (1, 2):
            k = kron_all([rho] * n)
            j = collective(t, n)
            ell0 = 2 * n * mu
            dell0 = 2 * n * s.trace(t * d_sigma_v)
            grad_v = first(rho, d_sigma_v, n)
            grad_r = first(rho, d_sigma_r, n)
            v2 = (first(rho, h_sigma_vv + d_sigma_dvv, n)
                  + second(rho, d_sigma_v, n))
            r2 = (first(rho, h_sigma_rr + d_sigma_drr, n)
                  + second(rho, d_sigma_r, n))
            b2 = ((ell0 ** 2 + dell0) * k + 2 * ell0 * grad_v + v2)
            tests = {
                'representation_filter': zero(ell0 * k + grad_v - j * k - k * j),
                'representation_rotation': zero(grad_r - s.I * (j * k - k * j)),
                'representation_quadratic_signed_identity': zero(
                    b2 - r2 - 2 * (j ** 2 * k + k * j ** 2)),
            }
            assert all(tests.values()), (ell, n, axis, tests)
            rows.append({'spin': str(s.Rational(ell, 2)), 'physical_dimension': p,
                         'N': n, 'axis': [str(v) for v in axis], **tests})

result = {'status': 'PASS_FINITE_TRANSCRIPTION_CHECKS', 'fixtures': rows,
          'scope': 'Higher-spin local kernels in fundamental SU(2) coordinates; no asymptotic proof by finite tests.',
          'elapsed_seconds': time.monotonic() - started, 'peer_scripts_executed': False}
Path(__file__).with_name('higher_spin_filter_checks.json').write_text(
    json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'fixtures': len(rows),
                  'elapsed_seconds': result['elapsed_seconds']}, indent=2))
