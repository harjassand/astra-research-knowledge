#!/usr/local/bin/python3
"""Reproducible numerical stress checks for binary_channel_proof.md.

These are finite diagnostics, not a substitute for its dimension-uniform proof.
Only NumPy, SciPy and the standard library are used. No network, API or other
trial files are accessed. Output is written alongside this script.
"""
from pathlib import Path
import json
import math
import platform
import numpy as np
import scipy
from scipy.linalg import block_diag
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(2026102628)


def hermitian_basis(d):
    out = []
    for i in range(d):
        x = np.zeros((d, d), complex)
        x[i, i] = 1
        out.append(x)
    for i in range(d):
        for j in range(i):
            x = np.zeros((d, d), complex)
            x[i, j] = x[j, i] = 1 / math.sqrt(2)
            out.append(x)
            x = np.zeros((d, d), complex)
            x[i, j] = 1j / math.sqrt(2)
            x[j, i] = -1j / math.sqrt(2)
            out.append(x)
    return np.array(out)


def random_pd(d, floor=0.01):
    z = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    a = z @ z.conj().T + floor * np.eye(d)
    return a / np.trace(a).real


def random_cq(d, equal_marginal=None):
    if equal_marginal is None:
        q = RNG.uniform(0.02, 0.98)
        return [q * random_pd(d), (1 - q) * random_pd(d)]
    m = equal_marginal
    vals, vecs = np.linalg.eigh(m)
    root = (vecs * np.sqrt(vals)) @ vecs.conj().T
    u = random_pd(d)
    uv, uu = np.linalg.eigh(u)
    u = (uu * RNG.uniform(0.03, 0.97, size=d)) @ uu.conj().T
    a = root @ u @ root
    return [a, m - a]


def apply_channel(k, blocks):
    return [k[y, 0] * blocks[0] + k[y, 1] * blocks[1]
            for y in range(len(k))]


def logm_pd(a):
    e, v = np.linalg.eigh(a)
    assert np.min(e) > 0
    return (v * np.log(e)) @ v.conj().T


def relative_entropy(a, b):
    return float(np.trace(a @ (logm_pd(a) - logm_pd(b))).real)


def conditional_divergence(k, rho, sigma):
    rr, ss = apply_channel(k, rho), apply_channel(k, sigma)
    return (sum(relative_entropy(a, b) for a, b in zip(rr, ss))
            - relative_entropy(sum(rho), sum(sigma)))


def metric_matrix(a, basis):
    """BKM Hessian by eigenvalue divided differences, not operator identity (4)."""
    e, v = np.linalg.eigh(a)
    assert np.min(e) > 0
    coeff = np.empty((len(e), len(e)))
    for i, x in enumerate(e):
        for j, y in enumerate(e):
            if abs(x - y) <= 1e-10 * max(x, y):
                coeff[i, j] = 2 / (x + y)
            else:
                coeff[i, j] = (np.log(x) - np.log(y)) / (x - y)
    bb = np.array([v.conj().T @ b @ v for b in basis]).reshape(len(basis), -1)
    # Explicit contraction avoids the BLAS path that emitted status warnings.
    # Check the actual entries rather than suppressing floating-point errors.
    ans = np.einsum('ik,jk->ij', bb.conj() * coeff.ravel(), bb,
                    optimize=False).real
    assert np.all(np.isfinite(ans))
    return (ans + ans.T) / 2


def conditional_hessian(k, blocks, basis):
    n = len(basis)
    answer = np.zeros((2 * n, 2 * n))
    for row, block in zip(k, apply_channel(k, blocks)):
        h = metric_matrix(block, basis)
        answer += np.kron(np.outer(row, row), h)
    hm = metric_matrix(sum(blocks), basis)
    answer -= np.kron(np.ones((2, 2)), hm)
    return (answer + answer.T) / 2


def scalar_g(k, t):
    delta = k[:, 0] - k[:, 1]
    # Convex-combination form avoids cancellation near a deterministic endpoint.
    return float(np.sum(delta ** 2 / ((1 - t) * k[:, 1] + t * k[:, 0])))


def scalar_relative(k, l):
    """Numerical ordinary incumbent: sample, then refine every grid maximum."""
    f = lambda t: scalar_g(k, t) / scalar_g(l, t)
    grid = np.linspace(1e-9, 1 - 1e-9, 2001)
    values = np.array([f(t) for t in grid])
    candidates = [(values[0], grid[0]), (values[-1], grid[-1])]
    for i in range(1, len(grid) - 1):
        if values[i] >= values[i - 1] and values[i] >= values[i + 1]:
            opt = minimize_scalar(lambda t: -f(t),
                                  bounds=(grid[i - 1], grid[i + 1]),
                                  method='bounded',
                                  options={'xatol': 1e-14})
            candidates.append((-opt.fun, opt.x))
    return max(candidates)


def binary_coefficient(a, b):
    return (math.sqrt(a * (1 - b)) - math.sqrt(b * (1 - a))) ** 2


def max_generalized(hk, hl):
    ev, vec = np.linalg.eigh(hl)
    keep = ev > max(1e-9, np.max(ev) * 1e-10)
    assert np.any(keep)
    whitening = vec[:, keep] / np.sqrt(ev[keep])
    ans = np.einsum('ia,ij,jb->ab', whitening, hk, whitening, optimize=False)
    assert np.all(np.isfinite(ans))
    return float(np.linalg.eigvalsh((ans + ans.T) / 2)[-1])


def bkm_value(a, h):
    e, u = np.linalg.eigh(a)
    hh = u.conj().T @ h @ u
    val = 0.0
    for i, x in enumerate(e):
        for j, y in enumerate(e):
            c = 2 / (x + y) if abs(x - y) < 1e-10 * max(x, y) else (
                np.log(x) - np.log(y)) / (x - y)
            val += abs(hh[i, j]) ** 2 * c
    return float(val)


def check_ternary_boundary():
    """Existing N967 simplex witness: a necessary negative control, not new."""
    c, lam, d = 3, 0.5, 3
    k = lam * np.eye(c) + (1 - lam) * np.ones((c, c)) / c
    eye = np.eye(d)
    vacuum = eye[:, 0]
    vectors = [np.array([0, math.cos(2 * math.pi * j / c),
                         math.sin(2 * math.pi * j / c)]) for j in range(c)]
    tangent = [(np.outer(v, vacuum) + np.outer(vacuum, v)) / c for v in vectors]
    rows = []
    finite_witness = None
    for eps in [1e-2, 1e-4, 1e-8, 1e-16, 1e-24, 1e-40]:
        baseline = [((1 - eps) * np.outer(v, v) + eps * eye / c) / c
                    for v in vectors]
        # Compute the metric by exact block eigenspaces. Extreme eps can lose
        # positive definiteness in generic eigenvalue routines, so retain the
        # analytic quotient at those eps rather than fabricating a matrix test.
        cf = lam + (1 - lam) / (c - 1)
        analytic = lam ** 2 / cf * math.log1p(c * (1 - eps) * cf / eps) / math.log1p(c * (1 - eps) / eps)
        measured = None
        if eps >= 1e-8:
            out_s, out_h = apply_multilabel(k, baseline), apply_multilabel(k, tangent)
            measured = sum(bkm_value(s, h) for s, h in zip(out_s, out_h)) / sum(
                bkm_value(s, h) for s, h in zip(baseline, tangent))
            assert abs(measured - analytic) < 1e-7
            if eps == 1e-2:
                step = 1e-3
                rho = [s + step * h for s, h in zip(baseline, tangent)]
                assert min(np.linalg.eigvalsh(s)[0] for s in rho) > 0
                out_rho = apply_multilabel(k, rho)
                finite_ratio = sum(relative_entropy(a, b) for a, b in zip(out_rho, out_s)) / sum(
                    relative_entropy(a, b) for a, b in zip(rho, baseline))
                assert finite_ratio > 0.3
                finite_witness = {'epsilon': eps, 'step': step,
                                  'relative_entropy_ratio': finite_ratio,
                                  'reference_marginal_difference_norm': float(np.linalg.norm(sum(rho) - sum(baseline)))}
        rows.append({'epsilon': eps, 'analytic_metric_ratio': analytic,
                     'matrix_metric_ratio': measured})
    # Ordinary ternary uniform reset coefficient (known sharp classical value).
    ordinary = lam ** 2 / (lam + 2 * (1 - lam) / c)
    assert rows[-1]['analytic_metric_ratio'] > ordinary
    assert 895 ** 10 > 4 ** 10 * 298 ** 9
    return {'ordinary_classical_coefficient': ordinary,
            'known_complete_limit': (c - 1) * lam ** 2 / (1 + (c - 2) * lam),
            'finite_relative_entropy_witness': finite_witness,
            'exact_epsilon_001_metric_separation_certificate': '895^10 > 4^10 * 298^9',
            'simplex_rows': rows}


def apply_multilabel(k, blocks):
    return [sum(k[y, i] * blocks[i] for i in range(len(blocks))) for y in range(len(k))]


def main():
    # identity, biased binary reset, BSC, binary erasure, asymmetric 3-output.
    ident = np.eye(2)
    biased = np.array([[5 / 8, 1 / 8], [3 / 8, 7 / 8]])
    bsc = np.array([[0.83, 0.17], [0.17, 0.83]])
    bec = np.array([[0.72, 0], [0, 0.72], [0.28, 0.28]])
    asymmetric = np.array([[0.62, 0.12], [0.23, 0.41], [0.15, 0.47]])
    comparisons = [
        ('biased_reset_vs_identity', biased, ident),
        ('BSC_vs_identity', bsc, ident),
        ('BEC_vs_identity', bec, ident),
        ('asymmetric_3output_vs_identity', asymmetric, ident),
        ('biased_reset_vs_BSC', biased, bsc),
        ('asymmetric_3output_vs_BEC', asymmetric, bec),
        ('BSC_vs_asymmetric_3output', bsc, asymmetric),
    ]
    results = []
    for label, k, l in comparisons:
        c, tstar = scalar_relative(k, l)
        row = {'comparison': label, 'ordinary_scalar_optimum': c,
               'scalar_witness_t': tstar, 'K': k.tolist(), 'L': l.tolist(),
               'dimension_checks': []}
        for d in [1, 2, 3, 5, 8]:
            ratios = []
            commutators = []
            for equal in [False, True]:
                for _ in range(40):
                    m = random_pd(d) if equal else None
                    rho = random_cq(d, m)
                    sigma = random_cq(d, m)
                    den = conditional_divergence(l, rho, sigma)
                    num = conditional_divergence(k, rho, sigma)
                    assert den > 1e-10
                    ratio = num / den
                    assert ratio <= c + 2e-9, (label, d, ratio, c)
                    assert num > -1e-10
                    ratios.append(ratio)
                    commutators.append(float(np.linalg.norm(sigma[0] @ sigma[1] - sigma[1] @ sigma[0])))
            hessian_max = None
            if d <= 5:
                basis = hermitian_basis(d)
                maxima = []
                for _ in range(6):
                    blocks = random_cq(d)
                    hk = conditional_hessian(k, blocks, basis)
                    hl = conditional_hessian(l, blocks, basis)
                    val = max_generalized(hk, hl)
                    assert val <= c + 2e-7, (label, d, 'hessian', val, c)
                    maxima.append(val)
                hessian_max = max(maxima)
            row['dimension_checks'].append({
                'reference_dimension': d, 'finite_pair_count': len(ratios),
                'finite_ratio_max': max(ratios),
                'noncommutator_norm_max': max(commutators),
                'all_tangents_hessian_max_over_6_baselines': hessian_max})
        results.append(row)

    exact = binary_coefficient(5 / 8, 1 / 8)
    root = math.sqrt((1 / 8) * (7 / 8) / ((5 / 8) * (3 / 8)))
    tstar = root / (1 + root)
    scalar_witnesses = []
    for step in [1e-2, 1e-3, 1e-4, 1e-5]:
        rho = [np.array([[tstar + step]]), np.array([[1 - tstar - step]])]
        sigma = [np.array([[tstar]]), np.array([[1 - tstar]])]
        val = conditional_divergence(biased, rho, sigma) / conditional_divergence(ident, rho, sigma)
        scalar_witnesses.append({'step': step, 'relative_entropy_ratio': val})
        assert abs(val - exact) < step
    assert abs(results[0]['ordinary_scalar_optimum'] - exact) < 1e-10

    output = {
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                        'scipy': scipy.__version__, 'seed': 2026102628},
        'meaning': 'finite numerical diagnostics; the all-reference theorem is analytic',
        'comparisons': results,
        'biased_reset': {'exact_expression': '(19-sqrt(105))/32',
                         'exact_coefficient': exact, 'index_transplant': 3 / 8,
                         'scalar_tstar': tstar, 'sharpness_witnesses': scalar_witnesses},
        'ternary_negative_control': check_ternary_boundary(),
        'assertions': 'PASS',
    }
    path = HERE / 'numerical_results.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    report = [
        '# Numerical verification', '',
        'All checks passed. These finite diagnostics supplement the analytic proof; they do not prove its quantifiers.', '',
        '| Comparison | Ordinary numerical optimum | Largest finite-state ratio | Largest local tangent ratio |',
        '|---|---:|---:|---:|',
    ]
    for row in results:
        finite = max(x['finite_ratio_max'] for x in row['dimension_checks'])
        local = max(x['all_tangents_hessian_max_over_6_baselines'] for x in row['dimension_checks']
                    if x['all_tangents_hessian_max_over_6_baselines'] is not None)
        report.append(f"| {row['comparison']} | {row['ordinary_scalar_optimum']:.12g} | {finite:.12g} | {local:.12g} |")
    report.extend(['', f'Biased reset exact coefficient: {exact:.15g}; false index transplant: 0.375.',
                   f'Scalar optimizing input: t={tstar:.15g}.',
                   'Reference dimensions: 1, 2, 3, 5, 8. Both equal and unequal marginals were tested.',
                   'Each comparison used 400 finite pairs and 24 full tangent-space Hessian optimizations.',
                   'The Hessian ratios use the numerically positive comparison subspace; eigenvalues at most max(1e-9, 1e-10 times the largest eigenvalue) are omitted as numerical null directions.',
                   'The scalar search uses a 2,001-point grid and refines each grid maximum. Its general-channel optima are numerical estimates; exact rational upper bounds are supplied separately.',
                   'All comparison constants came from competent ordinary scalar optimization over the same channels.',
                   'The ternary negative control recovers an existing quantum-reference separation, preventing an invalid extension beyond binary input.',
                   '', 'Run: `/usr/local/bin/python3 verify_binary_channels.py`', ''])
    (HERE / 'NUMERICAL_VERIFICATION.md').write_text('\n'.join(report))
    print('\n'.join(report))


if __name__ == '__main__':
    main()
