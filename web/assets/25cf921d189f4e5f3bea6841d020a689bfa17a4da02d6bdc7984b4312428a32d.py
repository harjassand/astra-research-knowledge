"""Finite diagnostics for the all-matrix near-full theorem, not a proof.

No optimizer is numerically identified. Full matrices are deliberately tiny;
the larger radial tests use one-dimensional layer arrays only.
"""
import json
import math
import pathlib
from fractions import Fraction

import numpy as np
from verify_operational import occupations, generators, lift, energy


def dim(n, s):
    return math.comb(n + s, s)


def a_constant(s):
    return 2 * s ** (s - 1) * (s + 1) ** s / (math.factorial(s - 1) * math.factorial(s))


def constants(s):
    if s == 1:
        return 2 / 7, 6 * (1 + math.log(9))
    a = a_constant(s)
    b = math.factorial(s) ** (1 / s) + 1
    small = 4 * s * (s + 2) ** s * b ** (s - 1) / math.factorial(s)
    small *= math.factorial(s) ** (1 / s)
    moderate = s * (s + 2) * 2 ** (1 / s) * 16 ** (s - 1)
    return 1 / (a + 1 + 1 / (s + 1)), max(small, moderate)


def matrix_checks(n, m):
    s = m - 1
    basis = list(occupations(n, m))
    d = len(basis)
    ts = [lift(t, basis) for t in generators(m)]
    identity = np.eye(d)
    comms = [np.kron(identity, t) - np.kron(t.T, identity) for t in ts]
    lap = sum(c @ c for c in comms)
    eigenvalues, eigenvectors = np.linalg.eigh(lap)
    shells = []
    spectrum_residual = 0.0
    for j in range(n + 1):
        c_j = j * (j + s)
        mask = np.abs(eigenvalues - c_j) < 1e-8
        b_j = math.comb(j + s, s) ** 2 - (math.comb(j + s - 1, s) ** 2 if j else 0)
        assert int(mask.sum()) == b_j
        spectrum_residual = max(spectrum_residual, float(np.max(np.abs(eigenvalues[mask] - c_j))))
        shells.append(eigenvectors[:, mask])
    rng = np.random.default_rng(20261008 + 100 * m + n)
    cases = []
    max_identity_residual = spectrum_residual
    for k in range(1, d):
        for sample in range(2):
            unitary, _ = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
            p = unitary[:, :k] @ unitary[:, :k].conj().T
            vecp = p.reshape(-1, order='F')
            masses = [float(np.linalg.norm(shell.conj().T @ vecp) ** 2) for shell in shells]
            assert abs(masses[0] - k * k / d) < 1e-9
            assert abs(sum(masses) - k) < 1e-9
            for j in range(1, n + 1):
                b_j = shells[j].shape[1]
                assert masses[j] <= k * k * b_j / d + 1e-9
            green = sum(masses[j] / (j * (j + s)) for j in range(1, n + 1))
            r = (d / k) ** (1 / (2 * s))
            cutoff = min(n, math.floor(r))
            low = (k * k / d) * sum(shells[j].shape[1] / (j * (j + s))
                                       for j in range(1, cutoff + 1))
            tail = k / ((cutoff + 1) * (cutoff + 1 + s)) if cutoff < n else 0
            assert green <= low + tail + 1e-9
            if s == 1:
                universal_green = k * k / d * (3 + math.log(d / k))
                universal_energy = 1 / (3.5 + math.log(d / k))
            else:
                universal_green = (a_constant(s) + 1) * k ** (1 + 1 / s) / d ** (1 / s)
                universal_energy = constants(s)[0] * (k / d) ** ((s - 1) / s)
            assert green <= universal_green + 1e-9
            weights = np.arange(1, d - k + 1, dtype=float)
            weights /= np.linalg.norm(weights)
            support = unitary[:, k:]
            f = (support * weights) @ support.conj().T
            e = energy(f, ts)
            mean = float(np.trace(f).real / d)
            assert np.linalg.norm(f @ p) < 1e-10
            assert k * k * mean * mean <= e * green + 1e-9
            kernel_lower = 1 / (d * green / (k * k) + 1 / m)
            assert e >= kernel_lower - 1e-9
            assert e >= universal_energy - 1e-9
            x = f - mean * identity
            max_identity_residual = max(max_identity_residual,
                abs(np.linalg.norm(f) ** 2 - d * mean * mean - np.linalg.norm(x) ** 2))
            cases.append(dict(k=k, sample=sample, green=green,
                              energy=e, exact_kernel_lower=kernel_lower))
    return dict(N=n, m=m, dimension=d, projections=len(cases),
                max_identity_residual=max_identity_residual,
                min_energy_to_kernel_lower=min(c['energy'] / c['exact_kernel_lower'] for c in cases))


def ceil_integer_root(value, s):
    lo, hi = 0, 1
    while hi ** s < value:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** s >= value:
            hi = mid
        else:
            lo = mid
    return hi


def radial_trial(n, s, r, b):
    d = dim(n, s)
    conductances = [s * (n - j) * math.comb(j + s, s) for j in range(r - 1, b)]
    resistance = sum((Fraction(1, c) for c in conductances), Fraction())
    values = [Fraction(0) for _ in range(r)]
    cumulative = Fraction()
    for c in conductances:
        cumulative += Fraction(1, c)
        values.append(cumulative / resistance)
    assert len(values) == b + 1 and values[-1] == 1
    direct_energy = sum(Fraction(s * (n - j) * math.comb(j + s, s)) *
                        (values[j + 1] - values[j]) ** 2 for j in range(b))
    assert direct_energy == 1 / resistance
    norm = sum(math.comb(j + s - 1, s - 1) * values[j] ** 2 for j in range(b))
    norm += d - math.comb(b - 1 + s, s)
    holes = math.comb(r - 1 + s, s)
    return direct_energy / norm, holes, resistance, norm


def cap_energy(n, s, q):
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if math.comb(mid + s, s) <= q:
            lo = mid
        else:
            hi = mid - 1
    r = lo
    assert r < n
    z = math.comb(r + s + 2, s + 2) + math.comb(r + s + 1, s + 2)
    w = n * s * math.comb(r + s + 1, s + 1) - s * (s + 1) * math.comb(r + s + 1, s + 2)
    return Fraction(w, z), r


def comparator_controls():
    records = []
    for s in range(1, 5):
        for n in [8, 16, 32, 64]:
            d = dim(n, s)
            threshold = n ** s // (math.factorial(s) * 8 ** s)
            choices = {1, 2, max(1, threshold), max(1, threshold + 1), max(1, d // 4), (d - 1) // 2}
            for k in sorted(choices):
                q = d - k
                if not (1 <= k and q > d / 2):
                    continue
                if s == 1 and k <= n // 8:
                    trial, holes, resistance, norm = radial_trial(n, s, k, n // 2)
                    category = 'harmonic'
                    assert holes == k and norm >= Fraction(d, 2)
                    assert float(resistance) >= math.log(math.e * d / k) / (4 * n) - 1e-12
                elif s >= 2 and k <= threshold:
                    r = ceil_integer_root(math.factorial(s) * k, s)
                    b = 2 * r
                    assert r <= n / 4 and b <= n / 2
                    trial, holes, resistance, norm = radial_trial(n, s, r, b)
                    category = 'harmonic'
                    assert holes >= k and norm >= Fraction(d, 4)
                    lower_resistance = Fraction(math.factorial(s), s * n * (s + 2) ** s * r ** (s - 1))
                    assert resistance >= lower_resistance
                else:
                    trial, r = cap_energy(n, s, q)
                    holes = d - math.comb(r + s, s)
                    category = 'cap'
                assert d - holes <= q
                profile = 1 / math.log(math.e * d / k) if s == 1 else (k / d) ** ((s - 1) / s)
                assert float(trial) <= constants(s)[1] * profile + 1e-10
                records.append(dict(N=n, m=s + 1, dimension=d, deficit=k,
                                    actual_holes=holes, category=category,
                                    energy=float(trial), profile=profile))
    return records


def spin_asymptotic_controls():
    records = []
    for n in [32, 128, 512, 2048, 8192, 32768]:
        for k in [1, math.ceil(math.sqrt(n))]:
            scale = math.log(n / k)
            b = math.floor(n / scale)
            assert k <= b < n
            edges = np.arange(k - 1, b, dtype=float)
            cumulative = np.cumsum(1 / ((n - edges) * (edges + 1)))
            resistance = cumulative[-1]
            internal_values = cumulative[:-1] / resistance
            norm = float(np.sum(internal_values ** 2)) + (n + 1 - b)
            rayleigh = 1 / (resistance * norm)
            assert rayleigh >= 1 / (3.5 + math.log((n + 1) / k)) - 1e-12
            records.append(dict(N=n, k=k, B=b, energy=rayleigh,
                                energy_times_log_d_over_k=rayleigh * math.log((n + 1) / k)))
    return records


def main():
    matrices = [matrix_checks(n, m) for n, m in
                [(2, 2), (5, 2), (1, 3), (2, 3), (3, 3), (2, 4)]]
    comparators = comparator_controls()
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  arbitrary_kernel_matrix_cases=matrices,
                  arbitrary_kernel_projections=sum(c['projections'] for c in matrices),
                  exact_radial_and_cap_comparators=len(comparators),
                  comparator_details=comparators,
                  spin_asymptotic_diagnostics=spin_asymptotic_controls(),
                  optimizer_search_performed=False,
                  max_matrix_identity_residual=max(c['max_identity_residual'] for c in matrices),
                  theorem_file='near_full.txt')
    path = pathlib.Path(__file__).with_name('NEAR_FULL_CHECKS.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'arbitrary_kernel_projections',
          'exact_radial_and_cap_comparators', 'max_matrix_identity_residual']}))


if __name__ == '__main__':
    main()
