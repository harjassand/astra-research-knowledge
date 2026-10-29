"""Population-model checks for factors, ordering and failure mechanisms.

These calculations do not establish a theorem, data-acquisition confidence,
or an apparatus. Run from any directory; output is adjacent to this file.
"""
from pathlib import Path
from itertools import combinations, product
import json
import math
import numpy as np
from scipy.linalg import eigh, expm

ROOT = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261029)


def norm(a):
    return float(np.linalg.norm(a, 2))


def spectral(a):
    vals, vecs = eigh((a + a.T) / 2)
    assert vals.min() >= -2e-11 * max(1, norm(a))
    return np.maximum(vals, 0), vecs


def evolution(spec, t):
    vals, vecs = spec
    return (vecs * np.exp(-t * vals)) @ vecs.T


def block_model(gap, eta):
    rot, _ = np.linalg.qr(RNG.normal(size=(3, 3)))
    aval = np.array([gap, .7, 1.8])
    a = np.zeros((4, 4))
    ahalf = np.zeros((4, 4))
    a[1:, 1:] = (rot * aval) @ rot.T
    ahalf[1:, 1:] = (rot * np.sqrt(aval)) @ rot.T
    crot, _ = np.linalg.qr(RNG.normal(size=(3, 3)))
    cv = np.array([.4, 1.4, 2.5])
    c = (crot * cv) @ crot.T
    chalf = (crot * np.sqrt(cv)) @ crot.T
    contraction = RNG.normal(size=(3, 4))
    contraction /= norm(contraction)
    b = eta * chalf @ contraction @ ahalf
    full = np.block([[a, b.T], [b, c]])
    return full, a


def abstract_checks():
    rows = []
    for gap, eta in product([1., 1e-4, 1e-8], [.1, .3, .7]):
        full, a = block_model(gap, eta)
        fs, vs = spectral(full), spectral(a)
        bound = eta**2 / (2 * math.sqrt(1 - eta**2))
        worst = 0.
        for t in np.r_[0., np.geomspace(1e-4, 20 / gap, 120)]:
            err = norm(evolution(fs, t)[:4, :4] - evolution(vs, t))
            worst = max(worst, err)
        assert worst <= bound + 2e-6
        # Different instantaneous eigenspaces challenge propagator ordering.
        full2, a2 = block_model(gap, eta)
        f2s, v2s = spectral(full2), spectral(a2)
        uf, uv = np.eye(7), np.eye(4)
        switched = 0.
        for j, dt in enumerate(np.geomspace(.001, 100., 23)):
            uf = evolution(fs if j % 2 else f2s, dt) @ uf
            uv = evolution(vs if j % 2 else v2s, dt) @ uv
            switched = max(switched, norm(uf[:4, :4] - uv))
        assert switched <= bound + 2e-8
        rows.append(dict(gap=gap, eta=eta, bound=bound,
                         largest_sampled_error=worst,
                         largest_switched_error=switched))
    return rows


def exclusion_model(n, particles, s, amplitudes, kappa, context=False):
    configs = []
    for occupied in combinations(range(n), particles):
        y = tuple(int(j in occupied) for j in range(n))
        configs.append(y)
    yi = {y: i for i, y in enumerate(configs)}
    signs = list(product([-1, 1], repeat=n))
    hi = {h: i for i, h in enumerate(signs)}
    ny, nh = len(configs), len(signs)
    full = np.zeros((ny * nh, ny * nh))
    native = np.zeros_like(full)
    terms = []
    for bond in range(n):
        ai = np.zeros((ny, ny))
        for i, y in enumerate(configs):
            j = (bond + 1) % n
            if y[bond] != y[j]:
                yp = list(y)
                yp[bond], yp[j] = yp[j], yp[bond]
                ai[i, i] += .5
                ai[i, yi[tuple(yp)]] -= .5
        assert norm(ai @ ai - ai) < 1e-13
        terms.append(ai)
    for iy, y in enumerate(configs):
        for ih, h in enumerate(signs):
            row = iy * nh + ih
            for bond in range(n):
                j = (bond + 1) % n
                if y[bond] != y[j]:
                    yp = list(y)
                    yp[bond], yp[j] = yp[j], yp[bond]
                    col = yi[tuple(yp)] * nh + ih
                    context_sign = 2*y[(bond+2) % n]-1 if context else 1
                    rate = s * (1 + amplitudes[bond] * context_sign * h[bond]) / 2
                    native[row, row] += rate
                    native[row, col] -= rate
                hp = list(h)
                hp[bond] *= -1
                col = iy * nh + hi[tuple(hp)]
                full[row, row] += kappa / 2  # hidden centered gap kappa
                full[row, col] -= kappa / 2
    full += native
    embed = np.kron(np.eye(ny), np.ones((nh, 1)) / math.sqrt(nh))
    a = s * sum(terms)
    assert norm(full - full.T) < 1e-12
    assert norm(embed.T @ full @ embed - a) < 2e-12
    b = native @ embed - embed @ a
    expected = sum(s*s*amplitudes[i]**2 * terms[i] for i in range(n))
    orthogonality_error = norm(b.T @ b - expected)
    assert orthogonality_error < 2e-12
    m = s * max(amplitudes**2)
    assert eigh(m * a - b.T @ b, eigvals_only=True).min() > -2e-12
    return configs, full, a, embed, m, orthogonality_error


def physical_checks():
    rows = []
    for n, kappa in product([3, 4, 5], [2.5, 10.]):
        s = 1.3
        amps = np.linspace(.2, .7, n)
        configs, full, a, embed, m, ortho = exclusion_model(
            n, n // 2, s, amps, kappa)
        fs, vs = spectral(full), spectral(a)
        r = m / kappa
        bound = r / (2 * math.sqrt(1-r))
        q = 2 * math.pi / n
        f = np.array([sum(y[j] * np.exp(1j*q*j) for j in range(n))
                      for y in configs])
        f /= np.linalg.norm(f)
        eig = s * (1-math.cos(q))
        assert np.linalg.norm(a @ f - eig*f) < 1e-12
        transformed = embed.T @ fs[1]
        worst = worst_mode = 0.
        for t in np.r_[0., np.geomspace(.0001, 100*n*n/s, 100)]:
            compressed = (transformed * np.exp(-t*fs[0])) @ transformed.T
            reference = evolution(vs, t)
            worst = max(worst, norm(compressed - reference))
            worst_mode = max(worst_mode, float(abs(
                np.vdot(f, compressed @ f) - np.exp(-eig*t))))
        assert worst <= bound + 1e-9
        rows.append(dict(sites=n, microscopic_states=len(full), kappa=kappa,
                         local_variance_to_mean=m, bound=bound,
                         largest_sampled_operator_error=worst,
                         largest_sampled_density_mode_error=worst_mode,
                         orthogonality_error=ortho))
    return rows


def failures():
    alpha, kappa = .8, 2.
    target = math.exp(-1) * (math.cosh(alpha)-1)
    rows = []
    for n in [1, 10, 100, 1000, 10000]:
        # Exact tilted generator for parity coupled to one common telegraph sign.
        q = np.array([[-kappa/2, kappa/2], [kappa/2, -kappa/2]])
        tilted = q - np.diag(n * np.array([1-alpha, 1+alpha]))
        correlation = np.array([.5, .5]) @ expm(tilted/n) @ np.ones(2)
        rows.append(dict(sites=n, error=float(correlation-math.exp(-1))))
    assert abs(rows[-1]['error'] - target) < 2e-5
    slow_rows = [dict(s=s, time=1/s, additive_defect=s*alpha,
                      exact_error=target) for s in [1., 1e-4, 1e-8]]
    return dict(shared_phase=rows, shared_phase_limit=target,
                absolute_defect=slow_rows,
                frozen_mean_error_at_time_one=(math.exp(-.5)+math.exp(-1.5))/2
                    -math.exp(-1))


def collective_response_checks():
    # Context-dependent modulation destroys actual one-particle closure.
    n, s = 5, 1.3
    amps = np.linspace(.2, .7, n)
    rows = []
    previous_tau = float('inf')
    for kappa in [2.5, 5., 10.]:
        configs, full, a, embed, m, ortho = exclusion_model(
            n, 2, s, amps, kappa, context=True)
        vals, vecs = spectral(full)
        av, au = spectral(a)
        evecs = embed.T @ vecs
        q = 2*math.pi/n
        f = np.array([sum(y[j]*np.exp(1j*q*j) for j in range(n))
                      for y in configs])
        f /= np.linalg.norm(f)
        coeffs = vecs.T @ (embed @ f)
        positive = vals > 1e-10
        assert np.linalg.norm(coeffs[~positive]) < 1e-10
        tau = float(np.sum(abs(coeffs[positive])**2 / vals[positive]))
        omega = s*(1-math.cos(q))
        r = m/kappa
        assert 1/omega - 1e-10 <= tau <= 1/((1-r)*omega) + 1e-10
        assert tau <= previous_tau + 1e-10
        previous_tau = tau
        min_margin = float('inf')
        centered = np.eye(len(a))-np.ones_like(a)/len(a)
        null_roundoff = 0.
        # The constant mode is exactly shared analytically. A numerical
        # eigenvalue around 1e-14 spuriously changes its 1/z resolvent by
        # about 1e-8 at z=.001. Test order on the orthogonal sector, and
        # retain the raw diagnostic rather than relaxing the assertion.
        assert np.linalg.norm(full @ np.ones(len(full))) < 2e-12
        for z in [.001, .1, 1., 10.]:
            actual = (evecs/(z+vals)) @ evecs.T
            lower = (au/(z+av)) @ au.T
            upper = (au/(z+(1-r)*av)) @ au.T
            null_roundoff = max(null_roundoff,
                                float(abs(np.ones(len(a)) @ (actual-lower)
                                          @ np.ones(len(a))/len(a))))
            min_margin = min(min_margin,
                float(eigh(centered@(actual-lower)@centered, eigvals_only=True).min()),
                float(eigh(centered@(upper-actual)@centered, eigvals_only=True).min()))
        assert min_margin >= -2e-9
        # Fix one phase sector to expose the nonlinear visible action.
        nh = 2**n
        indices = np.arange(len(configs))*nh
        fixed_native = full[np.ix_(indices, indices)] - (n*kappa/2)*np.eye(len(configs))
        centered_y = np.asarray(configs, float)-2/n
        u, singular, _ = np.linalg.svd(centered_y, full_matrices=False)
        linear = u[:, singular > 1e-10]
        density_leak = norm(fixed_native@linear-linear@(linear.T@fixed_native@linear))
        assert density_leak > .01
        rows.append(dict(kappa=kappa, r=r, tau=tau, reference_tau=1/omega,
                         certified_upper_tau=1/((1-r)*omega),
                         defined_response_coefficient=1/((1-math.cos(q))*tau),
                         smallest_resolvent_order_margin=min_margin,
                         raw_shared_constant_resolvent_roundoff=null_roundoff,
                         actual_density_sector_leakage=density_leak,
                         orthogonality_error=ortho))
    return rows


def main():
    result = dict(status='PASS', interpretation='population-model checks only',
                  abstract=abstract_checks(), physical=physical_checks(),
                  preserved_failures=failures(),
                  collective_response=collective_response_checks())
    path = ROOT / 'SELECTIVE_AVERAGING_CHECKS.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
