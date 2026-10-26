#!/usr/local/bin/python3
"""Stage 2 held-out compression and witness-construction diagnostics.

Reads no sibling data and does not modify stage1. New random seed and alphabet
sizes are frozen here. The theorem is analytic; finite checks cannot prove it.
"""
from pathlib import Path
import json
import math
import warnings
import numpy as np
from scipy.linalg import eigh, qr

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(9827410626)


def mm(a, b):
    return np.einsum('ik,kj->ij', a, b, optimize=False)


def mv(a, v):
    return np.einsum('ij,j->i', a, v, optimize=False)


def adj(a): return a.conj().T


def root(a, exponent):
    e, v = np.linalg.eigh(a)
    assert min(e) > 0
    return mm(v * e ** exponent, adj(v))


def pd(d, floor=0.1):
    a = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    return mm(a, adj(a)) / d + floor * np.eye(d)


def povm(n, d):
    raw = [pd(d) for _ in range(n)]
    inv = root(sum(raw), -0.5)
    return [mm(mm(inv, a), inv) for a in raw]


def stochastic(m, n):
    a = RNG.gamma(0.7, 1, size=(m, n)) + 0.03
    return a / a.sum(axis=0)


def outputs(k, q, u):
    ww = [sum(row[i] * q[i] for i in range(len(q))) for row in k]
    vv = [sum(row[i] * u[i] for i in range(len(q))) for row in k]
    return ww, vv


def free_form(k, q, u, subtract_marginal=False):
    ww, vv = outputs(k, q, u)
    val = sum(np.vdot(v, np.linalg.solve(w, v)).real for w, v in zip(ww, vv))
    if subtract_marginal: val -= np.vdot(sum(u), sum(u)).real
    return float(val)


def compress(q, u, k, l):
    wk, vk = outputs(k, q, u)
    wl, vl = outputs(l, q, u)
    vectors = u + [np.linalg.solve(w, v) for w, v in zip(wk, vk)] + [
        np.linalg.solve(w, v) for w, v in zip(wl, vl)]
    # SVD gives an orthonormal basis for the stated finite span, not a fitted
    # lower-dimensional surrogate. All discarded singular values are logged.
    mat = np.stack(vectors, axis=1)
    basis, singular, _ = np.linalg.svd(mat, full_matrices=False)
    keep = singular > singular[0] * 1e-11
    basis = basis[:, keep]
    qp = [mm(mm(adj(basis), a), basis) for a in q]
    up = [mv(adj(basis), a) for a in u]
    return qp, up, singular.tolist(), basis


def bkm(a, h):
    e, v = np.linalg.eigh(a)
    assert min(e) > 0
    x = mm(mm(adj(v), h), v)
    out = 0.0
    for i, ei in enumerate(e):
        for j, ej in enumerate(e):
            coeff = 2 / (ei + ej) if abs(ei - ej) < 1e-10 * max(ei, ej) else (
                math.log(ei) - math.log(ej)) / (ei - ej)
            out += abs(x[i, j]) ** 2 * coeff
    return float(out)


def rel(a, b):
    ea, va = np.linalg.eigh(a)
    eb, vb = np.linalg.eigh(b)
    assert min(ea) > 0 and min(eb) > 0
    la = mm(va * np.log(ea), adj(va))
    lb = mm(vb * np.log(eb), adj(vb))
    return float(np.trace(mm(a, la - lb)).real)


def block_outputs(k, aa):
    return [sum(row[i] * aa[i] for i in range(len(aa))) for row in k]


def vacuum_blocks(q, u, eps):
    n, d = len(q), len(q[0])
    ss, hh = [], []
    for a, vector in zip(q, u):
        s = np.zeros((d + 1, d + 1), complex)
        s[:d, :d] = (1 - eps) * a / d
        s[-1, -1] = eps / n
        h = np.zeros_like(s)
        h[:d, -1] = vector
        h[-1, :d] = vector.conj()
        ss.append(s)
        hh.append(h)
    return ss, hh


def vacuum_test(q, u, k, l):
    target = free_form(k, q, u) / free_form(l, q, u)
    rows = []
    for eps in [1e-2, 1e-4, 1e-8]:
        ss, hh = vacuum_blocks(q, u, eps)
        sk, hk = block_outputs(k, ss), block_outputs(k, hh)
        sl, hl = block_outputs(l, ss), block_outputs(l, hh)
        metric = sum(bkm(s, h) for s, h in zip(sk, hk)) / sum(bkm(s, h) for s, h in zip(sl, hl))
        row = {'epsilon': eps, 'metric_ratio': metric, 'absolute_error_from_free_ratio': abs(metric - target)}
        rate_checks = []
        for channel, ss_out, hh_out in [(k, sk, hk), (l, sl, hl)]:
            ww, _ = outputs(channel, q, u)
            eigenvalues = np.concatenate([np.linalg.eigvalsh(w) for w in ww])
            wmin, wmax = min(eigenvalues), max(eigenvalues)
            out_prob = channel.sum(axis=1) / len(q)
            delta = max(eps * (1 + len(q[0]) * prob / wmin) for prob in out_prob)
            bconst = math.log(2) + max(abs(math.log(w / (len(q[0]) * prob)))
                                      for w in [wmin, wmax] for prob in out_prob)
            expected = free_form(channel, q, u)
            scaled = sum(bkm(s, h) for s, h in zip(ss_out, hh_out)) / (
                2 * len(q[0]) * math.log(1 / eps))
            actual = abs(scaled - expected) / expected
            bound = (delta + bconst / math.log(1 / eps)) / (1 - delta) if delta < 1 else None
            if bound is not None: assert actual <= bound + 1e-9
            rate_checks.append({'delta': delta, 'logarithmic_constant_B': bconst,
                                'actual_scaled_metric_relative_error': actual,
                                'proved_relative_error_bound': bound})
        row['explicit_convergence_bound_K_L'] = rate_checks
        if eps == 1e-2:
            # Guaranteed positivity: ||S^-1/2 H S^-1/2|| * t <= 0.01.
            radii = []
            for s, h in zip(ss, hh):
                r = root(s, -0.5)
                radii.append(np.linalg.norm(mm(mm(r, h), r), ord=2))
            step = 0.01 / max(radii)
            rr = [s + step * h for s, h in zip(ss, hh)]
            assert min(np.linalg.eigvalsh(a)[0] for a in rr) > 0
            kr, lr = block_outputs(k, rr), block_outputs(l, rr)
            finite = sum(rel(a, b) for a, b in zip(kr, sk)) / sum(rel(a, b) for a, b in zip(lr, sl))
            row.update({'finite_step': step, 'finite_relative_entropy_ratio': finite,
                        'reference_marginal_difference_norm': float(np.linalg.norm(sum(rr) - sum(ss)))})
            assert abs(finite - metric) < 2e-4
        rows.append(row)
    assert rows[-1]['absolute_error_from_free_ratio'] < rows[0]['absolute_error_from_free_ratio'] + 1e-10
    return {'free_ratio': target, 'reference_dimension': len(q[0]) + 1, 'rows': rows}


def general_checks():
    results = []
    # n,mK,mL are withheld from stage1's binary construction, and original
    # dimension exceeds the proved compressed bound in every case.
    for n, mk, ml in [(3, 4, 3), (4, 3, 5), (6, 7, 4), (8, 5, 6)]:
        bound = n - 1 + mk + ml
        d = bound + 11
        for repeat in range(8):
            q = povm(n, d)
            a = [RNG.normal(size=d) + 1j * RNG.normal(size=d) for _ in range(n)]
            v = sum(a)
            u = [ai - mv(qi, v) for ai, qi in zip(a, q)]
            k, l = stochastic(mk, n), stochastic(ml, n)
            fk, fl = free_form(k, q, u), free_form(l, q, u)
            gauge_errors = [abs(free_form(ch, q, a, True) - free_form(ch, q, u))
                            for ch in [k, l]]
            qp, up, singular, basis = compress(q, u, k, l)
            cp = len(qp[0])
            compression_errors = [abs(free_form(ch, qp, up) - free_form(ch, q, u))
                                  / max(1, abs(free_form(ch, q, u))) for ch in [k, l]]
            assert cp <= bound
            assert max(gauge_errors) < 1e-8
            assert max(compression_errors) < 1e-10
            assert np.linalg.norm(sum(qp) - np.eye(cp)) < 1e-10
            assert np.linalg.norm(sum(up)) < 1e-9
            row = {'input_size': n, 'outputs_K': mk, 'outputs_L': ml,
                   'repeat': repeat, 'original_dimension': d,
                   'proved_compression_bound': bound, 'actual_compressed_dimension': cp,
                   'gauge_absolute_error_max': max(gauge_errors),
                   'compression_relative_error_max': max(compression_errors),
                   'uncompressed_ratio': fk / fl,
                   'compressed_ratio': free_form(k, qp, up) / free_form(l, qp, up),
                   'span_singular_values': singular,
                   'max_commutator_norm': max(float(np.linalg.norm(mm(qp[i], qp[j]) - mm(qp[j], qp[i])))
                                              for i in range(n) for j in range(i))}
            if repeat == 0:
                row['explicit_equal_marginal_state_construction'] = vacuum_test(qp, up, k, l)
            results.append(row)
    return results


def uniform_simplex_control(n, lam=0.5):
    # n vectors of a regular simplex in an (n-1)-dimensional real subspace.
    centered = np.eye(n) - np.ones((n, n)) / n
    basis = np.linalg.eigh(centered)[1][:, 1:]
    vectors = [math.sqrt(n / (n - 1)) * basis[i] for i in range(n)]
    lam_q = 1e-5
    q = [(1 - lam_q) * (n - 1) / n * np.outer(v, v) + lam_q * np.eye(n - 1) / n
         for v in vectors]
    k = lam * np.eye(n) + (1 - lam) * np.ones((n, n)) / n
    l = np.eye(n)
    ratio = free_form(k, q, vectors) / free_form(l, q, vectors)
    known = (n - 1) * lam ** 2 / (1 + (n - 2) * lam)
    ordinary = lam ** 2 / (lam + 2 * (1 - lam) / n)
    assert ordinary < ratio <= known + 1e-10
    return {'input_size': n, 'scalar_ordinary_exact': ordinary,
            'existing_complete_exact': known, 'constructed_free_ratio': ratio,
            'povm_regularizer': lam_q,
            'vacuum_state_test': vacuum_test(q, vectors, k, l)}


def direct_bkm_map_checks():
    rows = []
    for n, r, mk, ml in [(3, 5, 4, 3), (4, 6, 3, 5)]:
        blocks = [pd(r) for _ in range(n)]
        total_trace = np.trace(sum(blocks)).real
        blocks = [a / total_trace for a in blocks]
        tangent = []
        for _ in range(n):
            z = RNG.normal(size=(r, r)) + 1j * RNG.normal(size=(r, r))
            tangent.append(z + adj(z))
        correction = np.trace(sum(tangent)).real / (n * r)
        tangent = [h - correction * np.eye(r) for h in tangent]
        k, l = stochastic(mk, n), stochastic(ml, n)
        m, h = sum(blocks), sum(tangent)
        assert np.linalg.norm(h) > 1  # Changing reference marginal is deliberate.
        direct = []
        for channel in [k, l]:
            aa, hh = block_outputs(channel, blocks), block_outputs(channel, tangent)
            direct.append(sum(bkm(a, x) for a, x in zip(aa, hh)) - bkm(m, h))
        points, weights = np.polynomial.legendre.leggauss(64)
        integrals = [0.0, 0.0]
        compression_error = 0.0
        max_d = 0
        for point, weight in zip(points, weights):
            s = (point + 1) / 2
            ts = lambda a: s * np.kron(np.eye(r), a) + (1 - s) * np.kron(a.T, np.eye(r))
            invroot = root(ts(m), -0.5)
            q = [mm(mm(invroot, ts(a)), invroot) for a in blocks]
            av = [mv(invroot, x.reshape(r * r, order='F')) for x in tangent]
            v = sum(av)
            u = [a - mv(qi, v) for a, qi in zip(av, q)]
            qp, up, _, _ = compress(q, u, k, l)
            max_d = max(max_d, len(qp[0]))
            for j, channel in enumerate([k, l]):
                full, compressed = free_form(channel, q, u), free_form(channel, qp, up)
                compression_error = max(compression_error, abs(full - compressed) / max(1, abs(full)))
                integrals[j] += weight / 2 * compressed
        errors = [abs(a - b) / max(1, abs(a)) for a, b in zip(direct, integrals)]
        assert max(errors) < 1e-10, errors
        assert compression_error < 1e-10
        assert max_d <= n - 1 + mk + ml
        rows.append({'input_size': n, 'original_reference_dimension': r,
                     'original_Hilbert_Schmidt_dimension': r * r,
                     'maximum_compressed_dimension': max_d,
                     'proved_bound': n - 1 + mk + ml,
                     'reference_marginal_tangent_norm': float(np.linalg.norm(h)),
                     'direct_conditional_BKM_values_K_L': direct,
                     'compressed_quadrature_values_K_L': integrals,
                     'relative_error_max': max(errors),
                     'pointwise_compression_error_max': compression_error})
    return rows


def main():
    warnings.simplefilter('error')
    general = general_checks()
    uniform = [uniform_simplex_control(n) for n in [3, 4, 5]]
    bkm_checks = direct_bkm_map_checks()
    result = {'seed': 9827410626, 'assertions': 'PASS',
              'meaning': 'finite withheld diagnostics supplement the all-domain proof',
              'random_noncommuting_witnesses': general,
              'known_uniform_controls': uniform,
              'direct_unequal_reference_BKM_checks': bkm_checks}
    (HERE / 'stress_results.json').write_text(json.dumps(result, indent=2) + '\n')
    report = ['# Stage 2 executed stress tests', '',
              'All assertions passed with warnings treated as errors. A new frozen seed and nonbinary alphabets were used; stage1 was not modified.', '',
              f'{len(general)} noncommuting operator witnesses were compressed from dimensions exceeding the theorem bound.',
              f"Largest relative compression error: {max(r['compression_relative_error_max'] for r in general):.3g}.",
              f"Largest absolute gauge-identity error: {max(r['gauge_absolute_error_max'] for r in general):.3g}.",
              'The spans were computed from the exact listed witness vectors, with a 1e-11 relative singular-value threshold recorded in the code and full singular values saved in the data.', '',
              'Four random compressed witnesses and three known uniform-reset controls were converted into explicit faithful equal-reference-marginal state pairs. Both local BKM and finite relative-entropy ratios were evaluated; convergence trajectories are saved rather than assuming a favorable rate.', '',
              'Two further nonbinary cases start from changing reference marginals. Their exact spectral BKM Hessians agree with 64-point quadrature over compressed free witnesses to relative error below 1e-10.', '',
              '| Input labels | Exact ordinary scalar coefficient | Existing complete coefficient | Constructed free ratio |',
              '|---:|---:|---:|---:|']
    for row in uniform:
        report.append(f"| {row['input_size']} | {row['scalar_ordinary_exact']:.12g} | {row['existing_complete_exact']:.12g} | {row['constructed_free_ratio']:.12g} |")
    report += ['', 'The uniform values and simplex construction are existing controls from stage1/N967, not novelty claims.',
               'No random search maximum is claimed to be a certified global optimum.', '',
               'Run: `/usr/local/bin/python3 stress_finite_reference.py`', '']
    (HERE / 'STRESS_TESTS.md').write_text('\n'.join(report))
    print('\n'.join(report))


if __name__ == '__main__': main()
