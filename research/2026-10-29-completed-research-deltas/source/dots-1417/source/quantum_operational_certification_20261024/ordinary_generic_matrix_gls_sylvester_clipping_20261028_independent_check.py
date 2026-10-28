#!/usr/bin/env python3
"""Independent finite-moment tests for clipped Sylvester GLS, not quantum sampling.

The covariance calculations below sum finite-support distributions exactly up to
floating-point matrix arithmetic.  In particular, they do not assume Gaussian
tails.  Mathematical proof and separately received physical imports are required.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = 'ordinary_generic_matrix_gls_sylvester_clipping_20261028'
FROZEN_SOURCE_SHA256 = '9454b204df34d302bf315bfe20afddc6ea5f109a8205bbd20f61b4de22c22c21'
rng = np.random.default_rng(281226)


def herm_basis(d):
    out = []
    for i in range(d):
        h = np.zeros((d, d), complex)
        h[i, i] = 1
        out.append(h)
    for i in range(d):
        for j in range(i + 1, d):
            h = np.zeros((d, d), complex)
            h[i, j] = h[j, i] = 1 / math.sqrt(2)
            out.append(h)
            h = np.zeros((d, d), complex)
            h[i, j], h[j, i] = 1j / math.sqrt(2), -1j / math.sqrt(2)
            out.append(h)
    return np.array(out)


def haar(d):
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    return np.linalg.qr(z)[0]


def hn(a):
    return float(np.linalg.norm(a, 2))


def hpart(a):
    return (a + a.conj().T) / 2


def hfun(a, f):
    w, v = np.linalg.eigh(hpart(a))
    return (v * f(w)) @ v.conj().T


def dilation(z):
    d = z.shape[0]
    return np.block([[np.zeros((d, d)), z], [z.conj().T, np.zeros((d, d))]])


def vec(a, basis):
    return np.einsum('qij,ji->q', basis, a).real


def sylvester(u, a):
    w, v = np.linalg.eigh(u)
    middle = v.conj().T @ a @ v
    return v @ (middle / (w[:, None] + w[None, :])) @ v.conj().T


def clip(a, t):
    return hfun(a, lambda w: np.clip(w, -t, t))


def ceil_log2(x):
    x = Q(x)
    numerator, denominator = x.numerator, x.denominator
    k = numerator.bit_length() - denominator.bit_length()
    if k >= 0:
        return k + (numerator > denominator * (1 << k))
    return k + (numerator * (1 << -k) > denominator)


results = {
    'basis_transform_cases': 0,
    'finite_distribution_cases': 0,
    'clipping_cases': 0,
    'rational_schedule_cases': 0,
    'exact_full_bank_cap_cases': 0,
    'nonquadratic_envelope_design_cases': 0,
    'nonquadratic_design_updates': 0,
    'max_extremal_reference_second_moment_over_bound': 0.0,
    'max_left_second_moment_over_sigma_squared': 0.0,
    'max_right_second_moment_over_sigma_squared': 0.0,
    'max_biased_mean_over_sigma': 0.0,
    'max_clipping_bias_over_v_over_t': 0.0,
    'max_clipped_variance_over_v': 0.0,
    'max_reconstruction_relative_error': 0.0,
    'max_reference_covariance_formula_error': 0.0,
    'min_factor_sandwich_slack': 1.0,
    'max_realized_raw_bank_sum_over_cap': 0.0,
}

for d in [2, 3, 5, 7]:
    basis = herm_basis(d)
    p = d * d
    for eta in [0.2, 0.01, 1e-4]:
        # Noncommuting positive envelope and nonsymmetric rational factor.
        w = eta + 3 * rng.random(d)
        w[0] = eta
        q = haar(d)
        u = (q * w) @ q.conj().T
        root = hfun(1.5 * u, np.sqrt)
        rotation = haar(d)
        b0 = root @ rotation
        mesh = eta / (1000 * d)
        b = np.round(b0.real / mesh) * mesh + 1j * np.round(b0.imag / mesh) * mesh
        ub = b @ b.conj().T
        low = np.linalg.eigvalsh(ub - u)[0]
        high = np.linalg.eigvalsh(2 * u - ub)[0]
        assert min(low, high) > 0
        results['min_factor_sandwich_slack'] = min(results['min_factor_sandwich_slack'], float(min(low, high)))
        # Independently test the source's specific rational Cholesky scaling.
        chol = np.linalg.cholesky(u)
        chol = np.round(chol.real / mesh) * mesh + 1j * np.round(chol.imag / mesh) * mesh
        assert hn(chol @ chol.conj().T - u) <= eta / 10
        bc = 1.1 * chol
        assert np.linalg.eigvalsh(bc @ bc.conj().T - u)[0] > 0
        assert np.linalg.eigvalsh(2 * u - bc @ bc.conj().T)[0] > 0

        ku = np.array([vec((u @ a + a @ u) / 2, basis) for a in basis]).T
        kub = np.array([vec((ub @ a + a @ ub) / 2, basis) for a in basis]).T
        ks = hfun(ku, np.sqrt).real
        zz = np.array([b.conj().T @ sylvester(ub, a) for a in basis])
        # A covariance reference, not the assumed law of any physical estimator.
        zleft = np.einsum('ab,aij,bkj->ik', kub, zz, zz.conj())
        zright = np.einsum('ab,aji,bjk->ik', kub, zz.conj(), zz)
        lam, ev = np.linalg.eigh(ub)
        us = hfun(ub, np.sqrt)
        unitary = np.linalg.solve(us, b)
        predicted_left = unitary.conj().T @ ev @ np.diag(0.5 * (lam[:, None] / (lam[:, None] + lam[None, :])).sum(axis=1)) @ ev.conj().T @ unitary
        predicted_right = ev @ np.diag(0.5 * (lam[:, None] / (lam[:, None] + lam[None, :])).sum(axis=0)) @ ev.conj().T
        reference_error = max(hn(zleft - predicted_left), hn(zright - predicted_right))
        assert reference_error < 2e-10
        results['max_reference_covariance_formula_error'] = max(results['max_reference_covariance_formula_error'], reference_error)
        results['basis_transform_cases'] += 1

        # Random correlated full real-HS second moment M <= K(u).
        a = rng.normal(size=(p, p))
        orth = np.linalg.qr(a)[0]
        frac = 0.1 + 0.9 * rng.random(p)
        m = ks @ (orth * frac) @ orth.T @ ks
        ms = hfun(m, np.sqrt).real
        mean = 0.25 * ms[:, 0]
        covariance_factor = ms @ np.diag([math.sqrt(15 / 16)] + [1] * (p - 1))
        assert np.linalg.eigvalsh(ku - m)[0] > -1e-10
        # A valid state T <= u to check reconstruction and the center radius.
        usmall = hfun(u, np.sqrt)
        v0 = haar(d)
        ttrue = usmall @ (v0 * rng.uniform(0, 0.5, d)) @ v0.conj().T @ usmall
        rtrue = sylvester(ub, ttrue)
        ztrue = b.conj().T @ rtrue
        reconstructed = b @ ztrue + ztrue.conj().T @ b.conj().T
        recerr = hn(reconstructed - ttrue) / max(hn(ttrue), 1e-30)
        assert recerr < 2e-11
        assert np.linalg.eigvalsh(rtrue)[0] >= -1e-11
        assert np.linalg.eigvalsh(0.5 * np.eye(d) - rtrue)[0] >= -1e-11
        assert hn(ztrue) <= math.sqrt(38) / 2 + 1e-11
        results['max_reconstruction_relative_error'] = max(results['max_reconstruction_relative_error'], recerr)

        for rare in [0.5, 0.01, 1e-6]:
            # Biased finite-support law with rare large atoms; E ee^T = M.
            coords = []
            probs = []
            for col in covariance_factor.T:
                # Strong skew prevents cancellation of the clipping bias.
                coords.extend([mean + math.sqrt(p * (1 - rare) / rare) * col,
                               mean - math.sqrt(p * rare / (1 - rare)) * col])
                probs.extend([rare / p, (1 - rare) / p])
            probs = np.array(probs)
            coords = np.array(coords)
            actual_m = np.einsum('s,sa,sb->ab', probs, coords, coords)
            assert np.allclose(actual_m, m, atol=1e-10)
            errors = np.einsum('sa,aij->sij', coords, basis)
            dzs = np.array([b.conj().T @ sylvester(ub, e) for e in errors])
            left = np.einsum('s,sij,skj->ik', probs, dzs, dzs.conj())
            right = np.einsum('s,sji,sjk->ik', probs, dzs.conj(), dzs)
            sigma2 = d / 2
            assert np.linalg.eigvalsh(sigma2 * np.eye(d) - left)[0] > -1e-10
            assert np.linalg.eigvalsh(sigma2 * np.eye(d) - right)[0] > -1e-10
            mean_dz = np.einsum('s,sij->ij', probs, dzs)
            results['max_left_second_moment_over_sigma_squared'] = max(results['max_left_second_moment_over_sigma_squared'], hn(left) / sigma2)
            results['max_right_second_moment_over_sigma_squared'] = max(results['max_right_second_moment_over_sigma_squared'], hn(right) / sigma2)
            results['max_biased_mean_over_sigma'] = max(results['max_biased_mean_over_sigma'], hn(mean_dz) / math.sqrt(sigma2))
            results['finite_distribution_cases'] += 1

            for delta in [0, 0.25, 4.0]:
                off = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
                off *= delta / max(hn(off), 1e-30)
                shift = dilation(off)
                xs = np.array([dilation(z) + shift for z in dzs])
                ex = np.einsum('s,sij->ij', probs, xs)
                ex2 = np.einsum('s,sij,sjk->ik', probs, xs, xs)
                v = 2 * (sigma2 + delta * delta)
                assert np.linalg.eigvalsh(v * np.eye(2 * d) - ex2)[0] > -1e-9
                # h/b=1/2^16 is exactly the manuscript's round ratio.
                for factor in [1.0, 1.5, 2.0]:
                    threshold = factor * math.sqrt(v * 2**16)
                    ys = np.array([clip(x, threshold) for x in xs])
                    ey = np.einsum('s,sij->ij', probs, ys)
                    ycent = ys - ey
                    variance = np.einsum('s,sij,sjk->ik', probs, ycent, ycent)
                    bias = hn(ey - ex)
                    assert bias <= v / threshold + 1e-9
                    assert np.linalg.eigvalsh(v * np.eye(2 * d) - variance)[0] > -1e-9
                    assert max(hn(y) for y in ycent) <= 2 * threshold + 1e-8
                    # Off-diagonal dilation structure survives odd clipping.
                    assert np.max(np.abs(ys[:, :d, :d])) < 1e-8
                    assert np.max(np.abs(ys[:, d:, d:])) < 1e-8
                    results['max_clipping_bias_over_v_over_t'] = max(results['max_clipping_bias_over_v_over_t'], bias / (v / threshold))
                    results['max_clipped_variance_over_v'] = max(results['max_clipped_variance_over_v'], hn(variance) / v)
                    results['clipping_cases'] += 1

# Reference spectra approach the constant d/2 from both sides of the dilation.
for d in [2, 5, 11]:
    for flip in [False, True]:
        lam = np.array([19.0] + [1e-8] * (d - 1))
        if flip:
            lam = 19.0 + 1e-8 - lam
        ratio_matrix = lam[:, None] / (lam[:, None] + lam[None, :])
        ratio = max(ratio_matrix.sum(0).max(), ratio_matrix.sum(1).max()) / d
        assert ratio < 1
        results['max_extremal_reference_second_moment_over_bound'] = max(results['max_extremal_reference_second_moment_over_bound'], float(ratio))

# The learned envelope need not lie in the ten-feature model.
d = 2
basis = herm_basis(d)
p, D, L = d * d, 10 * d * d, 80 * d * d
anchors = list(np.eye(4))
for i in range(4):
    for j in range(i + 1, 4):
        x = np.zeros(4)
        x[i] = x[j] = 1 / math.sqrt(2)
        anchors.append(x)
grid = anchors[:]
for _ in range(14):
    x = rng.normal(size=4)
    grid.append(x / np.linalg.norm(x))
features = np.array([[x[i]**2 for i in range(4)] + [2 * x[i] * x[j] for i in range(4) for j in range(i + 1, 4)] for x in grid])
fs = np.array([np.kron(a[:, None], np.eye(p)) for a in features])
for eta in [0.1, 0.001, 1e-5]:
    us = []
    for index in range(len(grid)):
        rotation = haar(d)
        eigen = np.array([eta, 2.0]) if index >= 10 else np.array([1.5, 2.0])
        us.append((rotation * eigen) @ rotation.conj().T)
    table = np.array([vec(u, basis) for u in us])
    fitted = features @ np.linalg.lstsq(features, table, rcond=None)[0]
    assert np.linalg.norm(table - fitted) > 0.1
    ks = np.array([np.array([vec((u @ a + a @ u) / 2, basis) for a in basis]).T for u in us])
    kis = np.linalg.inv(ks)
    blocks = np.array([f @ ki @ f.T for f, ki in zip(fs, kis)])
    weights = np.array([0.1] * 10 + [0.0] * 14)
    max_updates = 10 + D * (ceil_log2(Q(4) / Q(str(eta))) + 20) + 1
    updates = 0
    while True:
        vv = np.einsum('x,xij->ij', weights, blocks)
        vi = np.linalg.inv(vv)
        leverage = np.einsum('ij,xji->x', vi, blocks)
        index = int(np.argmax(leverage))
        if leverage[index] <= L:
            break
        previous_det = np.linalg.slogdet(vv)[1]
        weights *= 1 - 1 / D
        weights[index] += 1 / D
        next_v = np.einsum('x,xij->ij', weights, blocks)
        assert np.linalg.slogdet(next_v)[1] - previous_det > math.log(2) - 1e-8
        updates += 1
        assert updates <= max_updates
    for f, ki in zip(fs, ks):
        lhs = f.T @ vi @ f
        assert np.linalg.eigvalsh(L * ki - lhs)[0] > -1e-7
    nn = math.ceil(2**28 * d * L / eta)
    ms = np.array([math.ceil(nn * weight) + math.ceil(2 + d / eta) for weight in weights])
    inner = np.einsum('x,xij->ij', weights**2 / ms, blocks)
    covariance = 100 * vi @ inner @ vi
    vs = hfun(vv, np.sqrt).real
    assert np.linalg.eigvalsh(nn * vs @ covariance @ vs / 100).max() <= 1 + 1e-7
    results['nonquadratic_envelope_design_cases'] += 1
    results['nonquadratic_design_updates'] += updates

# Exact arithmetic for Bernstein, all scales, floors, and deterministic caps.
assert Q(16, 1) / (2 * (1 + Q(16, 3))) == Q(24, 19) > 1
assert Q(101, 2**29) <= Q(1, 2**22)
assert 5 * math.sqrt(2) / 256 < 0.25
assert 5 * math.sqrt(2) / 256 + 1 + 0.25 < 2
assert 8 * math.sqrt(2) / 256 < 1 / 16
assert 17 / 16 + 1 / 4 < 2
assert 1 + math.sqrt(2) + 8 / 3 < 8
for d in [2, 6, 20]:
    D, L, r = 10 * d * d, 80 * d * d, d
    for j in [1, 2, 3, 10, 31, 80]:
        eta = Q(1, 2**j)
        n = math.ceil(Q(2**28 * d * L, 1) / eta)
        alpha = Q(101 * L, n)
        sigma2 = alpha * d / 2
        sbar = Q(1, 2**(11 + j // 2))
        assert sigma2 <= sbar * sbar
        assert sbar * sbar <= 2 * eta / 2**22
        rounds = math.ceil(Q(13 + j // 2, 2))
        radius = Q(4)
        for _ in range(rounds):
            radius = radius / 4 + 2 * sbar
        assert radius <= 4 * sbar
        # Squared form of 8 sqrt(2) sbar <= sqrt(eta)/128.
        assert 128 * sbar * sbar <= eta / 128**2
        floor = math.ceil(2 + Q(r, 1) / eta)
        mbar = n + floor + 1
        zeta = min(eta / (10**6 * D * n), Q(1, mbar * mbar))
        assert zeta <= Q(1, mbar * mbar)
        assert zeta * zeta / eta <= Q(1, n)
        support = 10 + D * (j + 22) + 1
        assert support == 10 + math.ceil(D * math.log2((4 / float(eta)) / 2**-20)) + 1
        # Worst-case realized bank sum, including all ceilings.
        weights = [Q(1, 10)] * 10
        mi = [math.ceil(n * w) + floor for w in weights]
        assert max(mi) <= mbar
        assert sum(mi) <= n + support * (floor + 1)
        results['rational_schedule_cases'] += 1
        Dp = d * r
        Dplus = 2**ceil_log2(Dp)
        Lz = 2 + ceil_log2(1 / zeta)
        lbar = mbar + Lz
        betabar = zeta / (1000 * lbar**2 * Dp**2 * mbar**2)
        n0bar = 320 * Dplus * ceil_log2(12 * Dplus / betabar) + 1
        for size in [1, 10, 37]:
            positive = [int(i) for i in rng.integers(1, 1001, size)]
            pi = [Q(i, sum(positive)) for i in positive]
            realized = 0
            for weight in pi:
                mm = math.ceil(n * weight) + floor
                li = max(mm, (ceil_log2(4 / zeta) + 1) // 2)
                beta_i = zeta / (1000 * li**2 * Dp**2 * mm**2)
                assert li <= mm + Lz <= lbar
                assert beta_i >= betabar
                n0_i = 320 * Dplus * ceil_log2(12 * Dplus / beta_i)
                raw = n0_i + mm + li
                assert raw <= n0bar + 2 * mm + Lz
                realized += raw
            cap = 2 * n + support * (2 * (floor + 1) + n0bar + Lz)
            assert realized <= cap
            # Exact fixed h and all-round multiplication, never expected stopping.
            M, J, tmax, beta = 10**4, 100, 33, Q(1, 3200)
            h = ceil_log2(Q(8 * d * M * J * tmax, 1) / beta)
            batch = 2**16 * h
            assert batch * rounds * realized <= batch * rounds * cap
            results['max_realized_raw_bank_sum_over_cap'] = max(results['max_realized_raw_bank_sum_over_cap'], float(Q(realized, cap)))
            results['exact_full_bank_cap_cases'] += 1

source = ROOT / (STEM + '.md')
assert hashlib.sha256(source.read_bytes()).hexdigest() == FROZEN_SOURCE_SHA256, 'Source changed: this independent receipt does not transfer automatically.'
results.update({
    'status': 'PASS_INDEPENDENT_SYLVESTER_COVARIANCE_CLIPPING_AND_SCHEDULE_CHECKS',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'bernstein_exponent_over_h_at_four_root_threshold': '24/19',
    'scope': 'Exact finite-distribution moments evaluated numerically, noncommuting envelope factors, correlated biased heavy-tail errors, deterministic scalar schedule algebra. Not quantum-bank sampling, actual tomography, certified matrix arithmetic, compiler execution, or hardware validation.',
})
output = ROOT / (STEM + '_independent_check.json')
output.write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
