#!/usr/local/bin/python3
"""Independent local diagnostics for Q28; no source-trial files are modified.

The analytic audit is in DERIVATION.md. Finite checks are diagnostics, not proof.
"""
from pathlib import Path
import json
import math
import warnings
import numpy as np
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(2610262807)


def mm(a, b):
    return np.einsum('ij,jk->ik', a, b, optimize=False)


def mv(a, v):
    return np.einsum('ij,j->i', a, v, optimize=False)


def out(ch, blocks):
    return [sum((c * x for c, x in zip(row, blocks)), np.zeros_like(blocks[0])) for row in ch]


def ff(ch, q, u):
    return float(sum(np.vdot(v, np.linalg.solve(w, v)).real for w, v in zip(out(ch, q), out(ch, u))))


def exact_rational_check():
    # Rational-complex positive matrices in dimension 9; the exact span has
    # dimension at most 3-1+2+2=6. No SVD truncation enters this check.
    d = 9
    eye = sp.eye(d)
    h1, h2 = sp.zeros(d), sp.diag(*[(-1) ** j for j in range(d)])
    for j in range(d - 1):
        h1[j, j + 1] = h1[j + 1, j] = 1
    for j in range(d - 2):
        h2[j, j + 2], h2[j + 2, j] = sp.I, -sp.I
    q = [eye / 3 + h1 / 100, eye / 3 + h2 / 120]
    q.append(eye - q[0] - q[1])
    assert q[0] * q[1] != q[1] * q[0]
    assert all(x == x.H for x in q)
    assert all(x[j, j] > sum(abs(x[j, k]) for k in range(d) if k != j)
               for x in q for j in range(d))  # Strict Hermitian diagonal dominance.
    u1, u2 = eye[:, 0] + sp.I * eye[:, 2], eye[:, 1] + eye[:, 8] / 2
    u = [u1, u2, -u1 - u2]
    k = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 5)],
                   [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(4, 5)]])
    l = sp.Matrix([[sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)],
                   [sp.Rational(3, 4), sp.Rational(1, 2), sp.Rational(1, 4)]])

    def terms(ch, vecs):
        ww = [sum((ch[y, i] * q[i] for i in range(3)), sp.zeros(d)) for y in range(ch.rows)]
        vv = [sum((ch[y, i] * vecs[i] for i in range(3)), sp.zeros(d, 1)) for y in range(ch.rows)]
        xx = [w.inv() * v for w, v in zip(ww, vv)]
        return ww, vv, xx

    data = [terms(ch, u) for ch in (k, l)]
    basis_cols = sp.Matrix.hstack(*(u + data[0][2] + data[1][2])).columnspace()
    b = sp.Matrix.hstack(*basis_cols)
    assert b.cols <= 6
    # With a nonorthonormal basis B, the orthogonal-compression quadratic is
    # (B* v)* (B* W B)^-1 (B* v); Gram factors cancel exactly.
    preserved = []
    for ww, vv, xx in data:
        for w, v, x in zip(ww, vv, xx):
            full = (v.H * x)[0]
            bv = b.H * v
            compressed = (bv.H * (b.H * w * b).inv() * bv)[0]
            assert sp.simplify(full - compressed) == 0
        preserved.append(True)
    marginal = sp.Matrix([j + 1 + sp.I * j for j in range(d)])
    aa = [ui + qi * marginal for ui, qi in zip(u, q)]
    assert sum(aa, sp.zeros(d, 1)) == marginal
    for ch, (_, vv, xx) in zip((k, l), data):
        _, av, ax = terms(ch, aa)
        lhs = sum((v.H * x)[0] for v, x in zip(av, ax)) - (marginal.H * marginal)[0]
        rhs = sum((v.H * x)[0] for v, x in zip(vv, xx))
        assert sp.simplify(lhs - rhs) == 0
    return {'arithmetic': 'exact rational-complex SymPy', 'original_dimension': d,
            'span_dimension': b.cols, 'bound': 6, 'both_forms_preserved_exactly': preserved,
            'both_gauge_identities_exact': True, 'positive_definiteness': 'strict diagonal dominance'}


def exact_binary_algebraic_check():
    t, c = sp.symbols('t c', real=True)
    # Columns of K are (1/5,4/5),(2/5,3/5); columns of L are
    # (1/5,4/5),(3/5,2/5). Binary spectral calculus is exact here.
    k = sp.Matrix([[sp.Rational(1, 5), sp.Rational(2, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    l = sp.Matrix([[sp.Rational(1, 5), sp.Rational(3, 5)],
                   [sp.Rational(4, 5), sp.Rational(2, 5)]])
    def fisher(ch):
        return sum((ch[y, 0] - ch[y, 1]) ** 2 /
                   (ch[y, 0] * t + ch[y, 1] * (1 - t)) for y in range(ch.rows))
    ratio = sp.cancel(fisher(k) / fisher(l))
    numerator, denominator = sp.fraction(ratio)
    derivative_num = sp.factor(sp.together(sp.diff(ratio, t)).as_numer_denom()[0])
    critical = sp.solve(derivative_num, t)
    inside = [r for r in critical if r.is_real and 0 < r < 1]
    assert inside == [3 - sp.sqrt(6)]
    value = sp.simplify(ratio.subs(t, inside[0]))
    assert value > ratio.subs(t, 0) and value > ratio.subs(t, 1)
    assert sp.simplify(100 * value ** 2 - 116 * value + 25) == 0
    assert sp.Poly(denominator, t).count_roots(0, 1) == 0
    # An exact threshold check: c D-N <=0 because D is negative on [0,1].
    assert sp.simplify(value - (sp.Rational(29, 50) - 3 * sp.sqrt(6) / 25)) == 0
    identity_to_bsc = sp.factor((1 / t + 1 / (1 - t)) /
        (sp.Rational(1, 4) * (1 / (sp.Rational(1, 4) + t / 2) +
                               1 / (sp.Rational(3, 4) - t / 2))))
    assert sp.simplify(identity_to_bsc - (1 + 3 / (4 * t * (1 - t)))) == 0
    assert sp.limit(identity_to_bsc, t, 0, dir='+') == sp.oo
    return {'K': str(k), 'L': str(l), 'ratio': str(ratio),
            'critical_points': [str(r) for r in critical], 'maximizing_t': str(inside[0]),
            'exact_coefficient': str(value), 'decimal': float(value),
            'minimal_polynomial': '100*c^2 - 116*c + 25',
            'global_check': 'all stationary points and both boundary limits compared exactly',
            'infinite_without_exact_kernel_witness': {
                'K': 'identity', 'L': 'invertible BSC(1/4)',
                'free_ratio': str(identity_to_bsc), 'limit_at_t_zero': 'infinity',
                'F_L_strictly_positive_for_every_nonzero_zero_sum_tangent': True}}


def random_povm(n, d):
    raw = []
    for _ in range(n):
        z = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
        raw.append(mm(z, z.conj().T) / d + np.eye(d) / 3)
    e, v = np.linalg.eigh(sum(raw))
    inv = mm(v * e ** -0.5, v.conj().T)
    return [mm(mm(inv, x), inv) for x in raw]


def sparse_and_zero_checks():
    errors, postprocessing_excess, erasure_errors, numerator_compression_gain = [], [], [], []
    for n, d in [(3, 17), (5, 20), (7, 23)]:
        for _ in range(5):
            q = random_povm(n, d)
            u = [RNG.normal(size=d) + 1j * RNG.normal(size=d) for _ in range(n - 1)]
            u.append(-sum(u))
            raw = RNG.uniform(size=(n + 1, n))
            raw[RNG.uniform(size=raw.shape) < 0.45] = 0
            raw[:n] += np.eye(n)  # No zero columns or first n rows.
            if not raw[-1].any():
                raw[-1, 0] = 1
            l = raw / raw.sum(axis=0)
            post = RNG.uniform(size=(3, n + 1))
            post /= post.sum(axis=0)
            k = mm(post, l)
            f_l, f_k = ff(l, q, u), ff(k, q, u)
            assert f_k <= f_l * (1 + 1e-12)
            postprocessing_excess.append((f_k - f_l) / f_l)
            wk, vk = out(k, q), out(k, u)
            wl, vl = out(l, q), out(l, u)
            vectors = u + [np.linalg.solve(w, v) for w, v in zip(wk, vk)]
            # Independent refinement only: preserve numerator; denominator may
            # decrease under compression. Not needed to validate Q28's bound.
            b, singular, _ = np.linalg.svd(np.column_stack(vectors), full_matrices=False)
            b = b[:, singular > singular[0] * 1e-11]
            assert b.shape[1] <= n - 1 + len(k)
            qp = [mm(mm(b.conj().T, x), b) for x in q]
            up = [mv(b.conj().T, x) for x in u]
            cfk, cfl = ff(k, qp, up), ff(l, qp, up)
            assert abs(cfk - f_k) < 1e-10 * max(1, f_k)
            assert cfl <= f_l * (1 + 1e-11)
            numerator_compression_gain.append(cfk / cfl - f_k / f_l)
            errors.append(abs(cfk - f_k) / max(1, f_k))
            ident = np.eye(n)
            erase = lambda a: np.vstack([a * ident, (1 - a) * np.ones((1, n))])
            id_form = ff(ident, q, u)
            for a in [0.0, 1/7, 0.5, 1.0]:
                ch = erase(a)
                ch = ch[np.any(ch, axis=1)]  # The theorem drops zero output rows.
                err = abs(ff(ch, q, u) - a * id_form) / max(1, id_form)
                erasure_errors.append(err)
                assert err < 1e-12
    # Exact scalar L=discard, K=identity, u=(1,-1). F_L=0,F_K=4.
    q = [np.array([[0.5]]), np.array([[0.5]])]
    u = [np.array([1.0]), np.array([-1.0])]
    assert ff(np.ones((1, 2)), q, u) == 0
    assert ff(np.eye(2), q, u) == 4
    return {'sparse_postprocessing_cases': 15, 'maximum_relative_numerator_compression_error': max(errors),
            'maximum_postprocessing_excess': max(postprocessing_excess),
            'maximum_erasure_identity_error': max(erasure_errors),
            'numerator_only_compression_ratio_gains_range': [min(numerator_compression_gain), max(numerator_compression_gain)],
            'exact_zero_denominator': {'F_discard': 0, 'F_identity': 4},
            'both_discard_coefficient': 0}


def mp_rel(a, b):
    ea, va = mp.eighe(a)
    eb, vb = mp.eighe(b)
    def xl(x):
        return x * mp.log(x) if x > 0 else mp.mpf('0')
    # tr a log b via b's eigenbasis. All b in these tests are faithful.
    rotated = vb.H * a * vb
    return mp.re(sum(xl(ea[i]) for i in range(a.rows)) -
                  sum(rotated[i, i] * mp.log(eb[i]) for i in range(a.rows)))


def mp_out(ch, blocks):
    return [sum((ch[y, i] * blocks[i] for i in range(ch.cols)), mp.zeros(blocks[0].rows))
            for y in range(ch.rows)]


def vacuum_and_boundary_checks():
    mp.mp.dps = 100
    q = [mp.matrix([[mp.mpf('0.45'), 0], [0, mp.mpf('0.05')]]),
         mp.matrix([[mp.mpf('0.2'), mp.j / 20], [-mp.j / 20, mp.mpf('0.3')]])]
    q.append(mp.eye(2) - q[0] - q[1])
    u = [mp.matrix([1 + mp.j / 3, mp.mpf('0.2')]), mp.matrix([mp.mpf('-0.4'), mp.j / 2])]
    u.append(-u[0] - u[1])
    p = [mp.mpf(1) / 7, mp.mpf(2) / 7, mp.mpf(4) / 7]
    k = mp.matrix([[1, 0, mp.mpf(1) / 2], [0, 1, mp.mpf(1) / 2]])
    l = mp.matrix([[mp.mpf(1) / 2, mp.mpf(1) / 4, 0],
                   [mp.mpf(1) / 2, mp.mpf(3) / 4, 1]])

    def free(ch):
        return mp.re(sum((v.H * (w ** -1) * v)[0] for w, v in
                        zip(mp_out(ch, q), [sum((ch[y, i] * u[i] for i in range(3)), mp.zeros(2, 1))
                                           for y in range(ch.rows)])))

    def offdiag_metric(ch, eps):
        ans = mp.mpf('0')
        for y, w in enumerate(mp_out(ch, q)):
            v = sum((ch[y, i] * u[i] for i in range(3)), mp.zeros(2, 1))
            e, basis = mp.eighe(w)
            z = basis.H * v
            prob = sum(ch[y, i] * p[i] for i in range(3))
            vacuum = eps * prob
            for j in range(2):
                active = (1 - eps) * e[j] / 2
                divided = (mp.log(active) - mp.log(vacuum)) / (active - vacuum)
                ans += 2 * abs(z[j]) ** 2 * divided
        return mp.re(ans)

    def construct(eps):
        blocks, tangents, radius = [], [], mp.inf
        for qi, ui, pi in zip(q, u, p):
            s, h = mp.zeros(3), mp.zeros(3)
            for i in range(2):
                for j in range(2):
                    s[i, j] = (1 - eps) * qi[i, j] / 2
                h[i, 2], h[2, i] = ui[i], mp.conj(ui[i])
            s[2, 2] = eps * pi
            r = mp.sqrt(eps * pi * (1 - eps) / (2 * (ui.H * qi ** -1 * ui)[0]))
            radius = min(radius, mp.re(r))
            blocks.append(s)
            tangents.append(h)
        return blocks, tangents, radius

    fk, fl = free(k), free(l)
    trajectory = []
    for exponent in [2, 6, 20, 80]:
        eps = mp.mpf(10) ** -exponent
        actual = []
        for ch, expected in [(k, fk), (l, fl)]:
            ww = mp_out(ch, q)
            eigen = [ev for w in ww for ev in mp.eighe(w, eigvals_only=True)]
            wmin, wmax = min(eigen), max(eigen)
            probs = [sum(ch[y, i] * p[i] for i in range(3)) for y in range(ch.rows)]
            delta = max(eps * (1 + 2 * py / wmin) for py in probs)
            bc = mp.log(2) + max(abs(mp.log(w / (2 * py))) for w in [wmin, wmax] for py in probs)
            scaled = offdiag_metric(ch, eps) / (4 * mp.log(1 / eps))
            error = abs(scaled - expected) / expected
            bound = (delta + bc / mp.log(1 / eps)) / (1 - delta)
            assert delta < 1 and error <= bound
            actual.append({'relative_error': float(error), 'proved_bound': float(bound)})
        trajectory.append({'epsilon': f'1e-{exponent}',
                           'metric_ratio': float(offdiag_metric(k, eps) / offdiag_metric(l, eps)),
                           'scaled_metric_errors_K_L': actual})
    eps = mp.mpf('1e-6')
    ss, hh, radius = construct(eps)
    finite = []
    metric_ratio = offdiag_metric(k, eps) / offdiag_metric(l, eps)
    for fraction in [mp.mpf('0.5'), mp.mpf('0.01'), mp.mpf('0.0001')]:
        rr = [s + fraction * radius * h for s, h in zip(ss, hh)]
        assert all(min(mp.eighe(r, eigvals_only=True)) > 0 for r in rr)
        assert mp.norm(sum(rr, mp.zeros(3)) - sum(ss, mp.zeros(3))) < mp.mpf('1e-95')
        ds = [sum(mp_rel(r, s) for r, s in zip(mp_out(ch, rr), mp_out(ch, ss))) for ch in (k, l)]
        finite.append({'step_fraction_of_exact_radius': float(fraction), 'ratio': float(ds[0] / ds[1]),
                       'error_from_fixed_epsilon_metric': float(abs(ds[0] / ds[1] - metric_ratio))})
    assert finite[-1]['error_from_fixed_epsilon_metric'] < finite[0]['error_from_fixed_epsilon_metric']

    # Singular input hypotheses: input D is infinite, but all output and
    # reference terms are finite. The regularization must still work.
    zero = mp.zeros(2)
    plus = mp.matrix([[1, 1], [1, 1]]) / 2
    phase = mp.matrix([[1, -mp.j], [mp.j, 1]]) / 2
    sigma = [mp.matrix([[mp.mpf('0.5'), 0], [0, 0]]),
             mp.matrix([[0, 0], [0, mp.mpf('0.5')]]), zero]
    rho = [mp.mpf('0.6') * plus, zero, mp.mpf('0.4') * phase]
    # Strictly positive stochastic output rows on all input labels.
    ch = mp.matrix([[mp.mpf(1)/5, mp.mpf(3)/5, mp.mpf(2)/5],
                    [mp.mpf(4)/5, mp.mpf(2)/5, mp.mpf(3)/5]])
    def conditional(rr, ss):
        return sum(mp_rel(a, b) for a, b in zip(mp_out(ch, rr), mp_out(ch, ss))) - \
            mp_rel(sum(rr, mp.zeros(2)), sum(ss, mp.zeros(2)))
    target = conditional(rho, sigma)
    regularized = []
    for exponent in [2, 8, 20, 40]:
        eta = mp.mpf(10) ** -exponent
        rr = [(1 - eta) * a + eta * mp.eye(2) / 6 for a in rho]
        ss = [(1 - eta) * a + eta * mp.eye(2) / 6 for a in sigma]
        actual = conditional(rr, ss)
        regularized.append({'mixture': f'1e-{exponent}', 'error': float(abs(actual - target))})
    assert regularized[-1]['error'] < 1e-38
    # An actual faithful pair with a zero denominator, not just a free form.
    base = mp.matrix([[mp.mpf('0.4'), 0], [0, mp.mpf('0.1')]])
    perturb = mp.matrix([[0, mp.mpf('0.1')], [mp.mpf('0.1'), 0]])
    rzero = [base + perturb, base - perturb]
    assert all(min(mp.eighe(r, eigvals_only=True)) > 0 for r in rzero)
    assert sum(rzero, mp.zeros(2)) == 2 * base
    positive_numerator = sum(mp_rel(r, base) for r in rzero)
    assert positive_numerator > 0
    return {'precision_decimal_digits': 100, 'nonuniform_p_sparse_channels': True,
            'free_ratio': float(fk/fl), 'vacuum_trajectory': trajectory,
            'finite_state_trajectory': finite,
            'actual_faithful_zero_denominator_pair': {
                'sigma_blocks': ['diag(0.4,0.1)', 'diag(0.4,0.1)'],
                'rho_blocks': ['[[0.4,0.1],[0.1,0.1]]', '[[0.4,-0.1],[-0.1,0.1]]'],
                'J_identity': float(positive_numerator), 'J_discard': 0,
                'equal_reference_marginals': True},
            'singular_input_D_infinite_output_terms_finite': {'conditional_value': float(target),
                                                            'regularization_errors': regularized}}


def main():
    warnings.simplefilter('error')
    result = {'status': 'PASS', 'meaning': 'diagnostics supplement the independent analytic derivation',
              'exact_rational_noncommuting': exact_rational_check(),
              'exact_binary_algebraic': exact_binary_algebraic_check(),
              'sparse_and_zero_cases': sparse_and_zero_checks(),
              'vacuum_and_support_boundary': vacuum_and_boundary_checks()}
    (HERE / 'independent_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
