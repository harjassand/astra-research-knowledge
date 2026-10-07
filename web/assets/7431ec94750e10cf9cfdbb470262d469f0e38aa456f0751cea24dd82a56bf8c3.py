"""Finite checks for the mixed bosonic orbit; not an optimality certificate."""
from collections import Counter
from itertools import product
from math import comb, log, sqrt
from pathlib import Path
import json
import numpy as np


def occupations(k, d):
    if d == 1:
        return [(k,)]
    return [(r,) + rest for r in range(k + 1)
            for rest in occupations(k - r, d - 1)]


def embedding(k, d):
    basis = occupations(k, d)
    index = {v: j for j, v in enumerate(basis)}
    vectors = np.zeros((d**k, len(basis)), dtype=complex)
    strings = list(product(range(d), repeat=k))
    counts = Counter(tuple(s.count(a) for a in range(d)) for s in strings)
    for i, s in enumerate(strings):
        count = tuple(s.count(a) for a in range(d))
        vectors[i, index[count]] = 1 / sqrt(counts[count])
    return vectors, basis


def number_operator(psi, k, d, basis):
    index = {v: j for j, v in enumerate(basis)}
    ans = np.zeros((len(basis), len(basis)), dtype=complex)
    for col, occ in enumerate(basis):
        for a in range(d):
            for b in range(d):
                if occ[b] == 0:
                    continue
                temp = list(occ)
                temp[b] -= 1
                coeff = sqrt(occ[b]) * sqrt(temp[a] + 1)
                temp[a] += 1
                ans[index[tuple(temp)], col] += psi[a] * psi[b].conjugate() * coeff
    return ans


def partial_trace_last(matrix, first_dim, last_dim):
    return np.einsum('abcb->ac', matrix.reshape(first_dim, last_dim, first_dim, last_dim))


def distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a - b)).sum() / 2)


def orbit_stats(k, d):
    probs = [((d - 1) / (k + d - 1))]
    for r in range(k):
        probs.append(probs[-1] * (k - r) / (k - r + d - 2))
    ratios = [d * r / k for r in range(k + 1)]
    capacity = sum(p * x * log(x) for p, x in zip(probs, ratios) if x > 0)
    separation = sum(p * abs(x - 1) for p, x in zip(probs, ratios)) / 2
    return {"capacity": capacity, "distance_to_reference": separation,
            "EB_error": d / (k + d) * separation,
            "b2": d / (2 * (k + d)) * separation}


def main():
    rng = np.random.default_rng(736109)
    cases = []
    residuals = []
    for d, k, receivers in [(2, 1, 2), (2, 2, 2), (2, 3, 2),
                            (2, 1, 3), (2, 2, 3), (3, 1, 2),
                            (3, 2, 2), (3, 1, 3), (3, 2, 3)]:
        m = receivers * k
        uk, basis = embedding(k, d)
        um, _ = embedding(m, d)
        psi = rng.normal(size=d) + 1j * rng.normal(size=d)
        psi /= np.linalg.norm(psi)
        dk, dm = uk.shape[1], um.shape[1]
        rho = d * number_operator(psi, k, d, basis) / (k * dk)
        omega = np.eye(dk) / dk
        joint = (dk / dm) * um.conj().T @ np.kron(uk @ rho @ uk.conj().T,
                                                np.eye(d**(m - k))) @ um
        marginal = uk.conj().T @ partial_trace_last(um @ joint @ um.conj().T,
                                                   d**k, d**(m - k)) @ uk
        eta = (m + d) / (receivers * (k + d))
        expected = eta * rho + (1 - eta) * omega
        cloning_residual = float(np.linalg.norm(marginal - expected))

        # Exact Haar moment for the covariant measure/prepare output.
        uplus, _ = embedding(k + 1, d)
        pplus = uplus @ uplus.conj().T
        ppsi = np.outer(psi, psi.conjugate())
        mp = d / uplus.shape[1] * partial_trace_last(
            np.kron(np.eye(d**k), ppsi) @ pplus, d**k, d)
        mp = uk.conj().T @ mp @ uk
        expected_mp = k / (k + d) * rho + d / (k + d) * omega
        moment_residual = float(np.linalg.norm(mp - expected_mp))
        trace_residual = float(abs(np.trace(joint) - 1))
        minimum_eigenvalue = float(np.linalg.eigvalsh(joint).min())
        residuals.extend([cloning_residual, moment_residual, trace_residual])
        cases.append({"d": d, "k": k, "receivers": receivers,
                      "cloning_residual": cloning_residual,
                      "moment_residual": moment_residual,
                      "trace_residual": trace_residual,
                      "minimum_joint_eigenvalue": minimum_eigenvalue,
                      "broadcast_error": distance(marginal, rho),
                      "predicted_broadcast_error": (1 - eta) * distance(rho, omega),
                      "MP_error": distance(mp, rho),
                      "predicted_MP_error": d / (k + d) * distance(rho, omega)})
    stats = [{"d": d, "k": k, **orbit_stats(k, d)}
             for d, k in [(2, 2), (4, 4), (16, 16), (64, 64),
                          (256, 256), (16, 64), (16, 256)]]
    capacity_checks = []
    for d in [2, 3, 4, 8, 16, 32, 64]:
        for k in [d, 2*d, 4*d, 16*d]:
            st = orbit_stats(k, d)
            lower = log(1 + (d - 1)/k)
            upper = log(d * (2*k + d - 1) / (k * (d + 1)))
            assert lower - 1e-12 <= st['capacity'] <= upper + 1e-12
            assert st['capacity'] <= log(3) + 1e-12
            capacity_checks.append({"d": d, "k": k, "capacity": st['capacity'],
                                    "lower": lower, "upper": upper})
    assert max(residuals) < 1e-12
    assert min(c['minimum_joint_eigenvalue'] for c in cases) > -1e-12
    output = {"status": "passed", "seed": 736109,
              "max_formula_residual": max(residuals),
              "dense_cases": cases, "orbit_stats": stats,
              "capacity_checks": capacity_checks,
              "scope": "Finite formula/normalization checks only; optimality is mathematical."}
    destination = Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({"status": output['status'], "dense_cases": len(cases),
                      "capacity_cases": len(capacity_checks),
                      "max_formula_residual": max(residuals),
                      "orbit_stats": stats}, indent=2))


if __name__ == '__main__':
    main()
