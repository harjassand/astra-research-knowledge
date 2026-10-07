"""Independent diagnostics for the critical separability candidate, not proof."""
from pathlib import Path
import json
import math
import numpy as np
import mpmath as mp


def spin(j):
    m = np.arange(-j, j + 1, dtype=float)
    z = np.diag(m).astype(complex)
    p = np.zeros_like(z)
    for k, v in enumerate(m[:-1]):
        p[k + 1, k] = math.sqrt((j - v) * (j + v + 1))
    return [(p + p.T) / 2, (p - p.T) / (2j), z]


def exp_h(a):
    w, u = np.linalg.eigh((a + a.conj().T) / 2)
    return (u * np.exp(w)) @ u.conj().T


def trace_norm(a):
    return float(np.abs(np.linalg.eigvalsh((a + a.conj().T) / 2)).sum())


def sector_check(n, a, b):
    bound = float(np.linalg.norm(a, ord=2))
    s = n ** .75
    c = a + bound * np.eye(3)
    lam, vec = np.linalg.eigh(c)
    sectors = []
    zg = zw = defect = 0.
    min_eig = math.inf
    for twice_j in range(n % 2, n + 1, 2):
        j = twice_j / 2
        d = twice_j + 1
        js = spin(j)
        eye = np.eye(d)
        h = sum(c[i, k] * (js[i] @ js[k] + js[k] @ js[i]) / 2
                for i in range(3) for k in range(3)) / n ** 1.5
        field = sum(b[i] * js[i] for i in range(3)) / s
        h += field
        ll = (np.kron(eye, field) + np.kron(field.T, eye)) / 2
        for k in range(3):
            f = sum(vec[i, k] * js[i] for i in range(3))
            f2 = f @ f
            ll += lam[k] / (4 * n ** 1.5) * (
                np.kron(eye, f2) + 2 * np.kron(f.T, f) + np.kron(f2.T, eye))
        y = (exp_h(ll) @ eye.reshape(-1, order='F')).reshape((d, d), order='F')
        g = exp_h(h)
        min_eig = min(min_eig, float(np.linalg.eigvalsh(y).min()))
        multiplicity = math.comb(n, int(n / 2 - j)) * d / (n / 2 + j + 1)
        scale = multiplicity * math.exp((2 / n - bound / n ** 1.5) * j * (j + 1))
        zg += scale * float(np.trace(g).real)
        zw += scale * float(np.trace(y).real)
        defect += scale * trace_norm(y - g)
        sectors.append((scale, y, g))
    actual = sum(scale * trace_norm(y / zw - g / zg) / 2 for scale, y, g in sectors)
    certificate = moment_ratio(n, bound, float(np.linalg.norm(b)))['certificate']
    assert actual <= certificate + 1e-10
    assert min_eig > -1e-10
    return dict(N=n, M=bound, B=float(np.linalg.norm(b)), trace_distance=actual,
                certificate=certificate, raw_error_over_target_Z=defect / zg,
                N_to_1p5_times_error=actual * n ** 1.5, min_Y_eigenvalue=min_eig)


def moment_ratio(n, bound, field):
    j = np.arange(n % 2 / 2, n / 2 + .25, 1.)
    logs = np.array([math.lgamma(n + 1) - math.lgamma(n / 2 - v + 1)
                     - math.lgamma(n / 2 + v + 1)
                     + 2 * math.log(2 * v + 1) - math.log(n / 2 + v + 1)
                     + 2 * v * (v + 1) / n - n * math.log(2) for v in j])
    x = j * (j + 1) / n ** 1.5
    ell = j / n ** .75
    p = 2 * bound * x + field * ell / 2 + (2 * bound * x + field * ell) ** 2 / 3
    ld = logs - bound * x
    lu = logs + bound * x + field * ell
    zd = math.exp(float(ld.max())) * float(np.exp(ld - ld.max()).sum())
    zu = math.exp(float(lu.max())) * float((np.exp(lu - lu.max()) * p).sum())
    return dict(N=n, ratio=zu / zd, D_over_2N_Np75=zd / n ** .75,
                certificate=1.5 * bound / n ** 1.5 * zu / zd)


def envelope_check(n):
    j = np.arange(n % 2 / 2, n / 2 + .25, 1.)
    logs = np.array([math.lgamma(n + 1) - math.lgamma(n / 2 - v + 1)
                     - math.lgamma(n / 2 + v + 1)
                     + 2 * math.log(2 * v + 1) - math.log(n / 2 + v + 1)
                     + 2 * v * (v + 1) / n - n * math.log(2) for v in j])
    upper = math.log(64) + 2 * np.log(2 * j + 1) - 1.5 * math.log(n) - 2 / 3 * j ** 4 / n ** 3
    residual = float((logs - upper).max())
    assert residual <= 1e-9
    return dict(N=n, max_log_a_minus_log_envelope=residual)


def heat_check(t, j):
    mp.mp.dps = 45
    k = mp.mpf(j) + mp.mpf('.5')
    c = (4 * mp.pi * t) ** (-mp.mpf('1.5')) * mp.exp(-t / 4) * 8 * mp.pi / (2 * j + 1)
    got = c * mp.quad(lambda r: r * mp.exp(-r*r/(4*t)) * mp.sinh(k*r), [0, mp.inf])
    expected = mp.exp(t*j*(j+1))
    return dict(t=t, j=j, relative_error=float(abs(got / expected - 1)))


def main():
    a1 = np.diag([.8, -.5, .1])
    a2 = np.array([[.3, .21, -.12], [.21, -.4, .16], [-.12, .16, .2]])
    out = {
        'status': 'Finite diagnostics only; none proves separability or asymptotics.',
        'sectors': [sector_check(n, a, b) for n in [2, 3, 4, 6, 8, 12]
                    for a, b in [(a1, np.array([.7, -.3, .4])),
                                 (a2, np.array([-.2, .8, .3])),
                                 (np.zeros((3, 3)), np.array([.7, .5, -.1]))]],
        'moments': [moment_ratio(n, m, b) for m, b in [(1., 1.), (2., 3.), (0.5, 0.)]
                    for n in [256, 1024, 4096, 16384]],
        'envelopes': [envelope_check(n) for n in [256, 257, 1024, 1025, 4096, 16384]],
        'heat': [heat_check(t, j) for t in [.02, .2, 1., 2.] for j in [0., .5, 1., 2., 3.]],
    }
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'sector_cases': len(out['sectors']),
                      'max_heat_relative_error': max(v['relative_error'] for v in out['heat']),
                      'max_error_over_certificate': max(v['trace_distance']/v['certificate']
                           for v in out['sectors'] if v['certificate'] > 0),
                      'max_Np1p5_error': max(v['N_to_1p5_times_error'] for v in out['sectors']),
                      'path': str(target)}, indent=2))


if __name__ == '__main__':
    main()
