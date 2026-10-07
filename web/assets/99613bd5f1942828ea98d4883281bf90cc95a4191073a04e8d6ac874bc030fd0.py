"""Finite diagnostics for the sparse universal-lift volume lemma.

These checks are examples and algebra checks, not theorem or novelty validation.
The proof is in quantum_complexity.txt. Uses NumPy only; deterministic seed.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, exp, log, sqrt
import json
import numpy as np


def cap_cdf(d, s, t):
    # Squared distance from a Haar complex unit vector to a fixed s-plane.
    return sum(Fraction(comb(d - 1, k)) * t**k * (1 - t)**(d - 1 - k)
               for k in range(d - s, d))


def lower_bound(d, n, s):
    a = comb(n, s) * comb(d - 1, s - 1)
    return (d - s) / (d - s + 1) * exp(-log(a) / (d - s))


def complex_normal(rng, shape):
    return rng.normal(size=shape) + 1j * rng.normal(size=shape)


def haar_unitary(rng, d):
    q, r = np.linalg.qr(complex_normal(rng, (d, d)))
    diag = np.diag(r)
    return q @ np.diag(diag / np.abs(diag))


def row_spans(v, s):
    spans = []
    for ix in combinations(range(len(v)), s):
        r = v[list(ix), :]
        _, singular, vh = np.linalg.svd(r, full_matrices=False)
        rank = int(np.sum(singular > 1e-12))
        basis = vh[:rank, :]
        spans.append((ix, r, basis.conj().T @ basis))
    return spans


def best_row_sparse(v, u, spans):
    targets = v @ u
    m = np.zeros((len(v), len(v)), dtype=complex)
    row_loss = 0.0
    for j, target in enumerate(targets):
        best = None
        for ix, rows, p in spans:
            loss = float(np.linalg.norm(target - target @ p)**2)
            if best is None or loss < best[0]:
                best = (loss, ix, rows)
        loss, ix, rows = best
        m[j, list(ix)] = target @ np.linalg.pinv(rows)
        row_loss += loss
    residual = m @ v - targets
    return row_loss / v.shape[1], np.linalg.norm(residual, "fro")**2 / v.shape[1], \
        np.linalg.norm(residual, 2)**2


def main():
    out = {"scope": "Finite diagnostics only; proof and priority are separate."}
    rational_caps = 0
    for d in range(2, 14):
        for s in range(1, d):
            for k in range(21):
                t = Fraction(k, 20)
                assert cap_cdf(d, s, t) <= comb(d - 1, s - 1) * t**(d - s)
                rational_caps += 1
    out["exact_rational_cap_checks"] = rational_caps

    # For the coordinate frame, E max_j |psi_j|^2 = H_d/d.
    basis = []
    for d in range(2, 17):
        harmonic = sum(Fraction(1, j) for j in range(1, d + 1))
        exact = 1 - harmonic / d
        bound = lower_bound(d, d, 1)
        assert float(exact) >= bound - 1e-14
        basis.append({"d": d, "exact_mean_distortion": str(exact),
                      "volume_lower_bound": bound})
    assert basis[0]["exact_mean_distortion"] == "1/4"
    out["coordinate_frame_checks"] = basis

    rng = np.random.default_rng(7102026)
    fixtures = []
    for d, n, s in [(3, 8, 1), (4, 7, 2), (5, 9, 2)]:
        v, _ = np.linalg.qr(complex_normal(rng, (n, d)))
        assert np.linalg.norm(v.conj().T @ v - np.eye(d), 2) < 1e-12
        spans = row_spans(v, s)
        weights = np.sum(np.abs(v)**2, axis=1) / d
        # Deliberately nonuniform frame weights, unlike the first draft's premise.
        assert weights.max() - weights.min() > 1e-3
        losses, operators = [], []
        for _ in range(160):
            u = haar_unitary(rng, d)
            a, b, c = best_row_sparse(v, u, spans)
            assert abs(a - b) < 2e-12
            assert c + 2e-12 >= b
            losses.append(a)
            operators.append(c)
        mean = float(np.mean(losses))
        bound = lower_bound(d, n, s)
        assert mean >= bound
        fixtures.append({"d": d, "N": n, "s": s, "unitaries": len(losses),
                         "frame_weight_min": float(weights.min()),
                         "frame_weight_max": float(weights.max()),
                         "mean_optimal_row_LS_frobenius_squared_over_d": mean,
                         "mean_operator_error_squared": float(np.mean(operators)),
                         "volume_lower_bound": bound})
    out["nonuniform_frame_fixtures"] = fixtures

    # Exact-rational 1-local counterexample: each site's two projectors have
    # distinct kernels, so every state violates at least half of all terms.
    rational_hamiltonians = []
    for bits in [1, 8, 64, 256]:
        r = Fraction(1, 2**bits)
        h00 = r*r / (2*(1 + r*r))
        h01 = r / (2*(1 + r*r))
        h11 = Fraction(1, 2) + Fraction(1, 2*(1 + r*r))
        det = h00*h11 - h01*h01
        assert h00 + h11 == 1
        assert det == r*r / (4*(1 + r*r))
        assert det > 0
        assert det <= r*r/4
        # The characteristic polynomial is decreasing on [0,1/2]. Its signs
        # at these exact rational bounds sandwich the smaller eigenvalue.
        lo, hi = det, r*r/4
        assert 0 < lo <= hi < Fraction(1, 2)
        assert lo*lo - lo + det >= 0
        assert hi*hi - hi + det <= 0
        rational_hamiltonians.append({"B": bits, "exact_determinant": str(det),
                                      "spectral_energy_upper_bound": str(r*r/4),
                                      "combinatorial_energy": "1/2"})
    out["rational_combinatorial_gap_counterexamples"] = rational_hamiltonians

    # A stable upper bound on log A avoids constructing astronomic N.
    scaling = []
    for n_qubits in [8, 16, 32, 64]:
        d = 2**n_qubits
        s = n_qubits**2
        if s >= d:
            continue
        log_n = n_qubits**2 * log(2)
        log_a_upper = s * (1 + log_n - log(s))
        if s > 1:
            log_a_upper += (s - 1) * (1 + log(d - 1) - log(s - 1))
        eps_lower = sqrt((d - s)/(d - s + 1) * exp(-log_a_upper/(d - s)))
        scaling.append({"logical_qubits": n_qubits, "physical_bits": n_qubits**2,
                        "row_sparsity": s, "universal_operator_error_lower_bound": eps_lower})
    out["polynomial_label_and_row_scaling"] = scaling
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
