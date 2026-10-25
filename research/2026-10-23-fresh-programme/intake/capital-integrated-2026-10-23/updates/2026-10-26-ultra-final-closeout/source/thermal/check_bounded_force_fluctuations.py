"""Finite oscillator-cutoff diagnostics for the exact all-mode identities.

The proof is in BOUNDED_FORCE_FLUCTUATION_PRINCIPLE.md. These finite matrices
test normalization, signs, noncommuting internal dynamics and cutoff drift;
they do not certify an infinite bath, cold limit, current, or hardware.
"""

import json
import numpy as np


def annihilator(n):
    return np.diag(np.sqrt(np.arange(1, n)), 1)


def thermal_case(n, internal, beta=2.5, coupling=0.8):
    masses = np.array([1.2, 0.8])
    spring = np.array([[2.0, -0.5], [-0.5, 1.0]])
    port = np.array([1.0, -1.0])
    mhalf = np.diag(np.sqrt(masses))
    mi = np.diag(1 / np.sqrt(masses))
    eig, modes = np.linalg.eigh(mi @ spring @ mi)
    omega = np.sqrt(eig)
    an = annihilator(n)
    ident = np.eye(n)
    a = [np.kron(an, ident), np.kron(ident, an)]
    qn = [(x + x.T) / np.sqrt(2 * w) for x, w in zip(a, omega)]
    pn = [1j * np.sqrt(w / 2) * (x.T - x) for x, w in zip(a, omega)]
    q = [sum((mi @ modes)[i, j] * qn[j] for j in range(2)) for i in range(2)]
    p = [sum((mhalf @ modes)[i, j] * pn[j] for j in range(2)) for i in range(2)]
    hg = sum(w * (x.T @ x + np.eye(n * n) / 2) for x, w in zip(a, omega))
    sx = np.array([[0.0, 1.0], [1.0, 0.0]])
    sy = np.array([[0.0, -1j], [1j, 0.0]])
    sz = np.diag([1.0, -1.0])
    ha = 0.7 * sx + 0.2 * sy + 0.3 * sz if internal == "noncommuting" else 0.3 * sz
    y = port[0] * q[0] + port[1] * q[1]
    h = np.kron(hg, np.eye(2)) + np.kron(np.eye(n * n), ha) - coupling * np.kron(y, sz)
    energy, vec = np.linalg.eigh(h)
    weights = np.exp(-beta * (energy - energy[0]))
    weights /= weights.sum()

    def mean(op):
        return float(np.real(np.dot(weights, np.diag(vec.conj().T @ op @ vec))))

    q = [np.kron(x, np.eye(2)) for x in q]
    p = [np.kron(x, np.eye(2)) for x in p]
    qmean = np.array([mean(x) for x in q])
    qcov = np.array([[mean((x @ z + z @ x) / 2) for z in q] for x in q]) - np.outer(qmean, qmean)
    pcov = np.array([[mean((x @ z + z @ x) / 2) for z in p] for x in p])
    coth = 1 / np.tanh(beta * omega / 2)
    qfree = mi @ modes @ np.diag(coth / (2 * omega)) @ modes.T @ mi
    pfree = mhalf @ modes @ np.diag(omega * coth / 2) @ modes.T @ mhalf
    free_t = float(np.sum(omega * coth / 4))
    total_v = float(np.trace(spring @ (qcov + np.outer(qmean, qmean))) / 2)
    total_t = float(np.trace(np.diag(1 / masses) @ pcov) / 2)
    compliance = float(port @ np.linalg.solve(spring, port))
    reorganisation = coupling**2 * compliance / 2

    def matsubara(op, index):
        transformed = vec.conj().T @ op @ vec
        i, j = np.triu_indices(len(energy), 1)
        gap = energy[j] - energy[i]
        nu = 2 * np.pi * index / beta
        positive = gap > 1e-11
        total = np.sum(2 * (weights[i[positive]] - weights[j[positive]]) * gap[positive]
                       * abs(transformed[i[positive], j[positive]])**2
                       / (gap[positive]**2 + nu**2))
        if index == 0:
            diagonal = np.real(np.diag(transformed))
            total += beta * (np.dot(weights, diagonal**2) - np.dot(weights, diagonal)**2)
            degenerate = ~positive
            total += np.sum(2 * beta * weights[i[degenerate]]
                            * abs(transformed[i[degenerate], j[degenerate]])**2)
        return float(np.real(total))

    yfull = port[0] * q[0] + port[1] * q[1]
    qaux = np.kron(np.eye(n * n), sz)
    residual = []
    for index in [0, 1, 2, 7]:
        nu = 2 * np.pi * index / beta
        c = float(port @ np.linalg.solve(spring + nu**2 * np.diag(masses), port))
        actual = matsubara(yfull, index)
        predicted = c + coupling**2 * c**2 * matsubara(qaux, index)
        residual.append(abs(actual - predicted))
    return {
        "cutoff_per_oscillator": n,
        "internal": internal,
        "max_matsubara_identity_residual": max(residual),
        "min_position_covariance_increment_eigenvalue": float(np.linalg.eigvalsh(qcov - qfree)[0]),
        "min_momentum_covariance_reduction_eigenvalue": float(np.linalg.eigvalsh(pfree - pcov)[0]),
        "max_momentum_covariance_difference": float(np.max(abs(pfree - pcov))),
        "total_spring_energy_increase": total_v - free_t,
        "total_kinetic_energy_decrease": free_t - total_t,
        "reorganisation_energy_bound": reorganisation,
        "kinetic_decrease_bound": reorganisation / 4,
        "port_variance": float(port @ qcov @ port),
        "physical_momentum_variances": np.diag(pcov).tolist(),
    }


if __name__ == "__main__":
    results = [thermal_case(n, "noncommuting") for n in [8, 12, 16]]
    results.append(thermal_case(16, "commuting"))
    last = results[2]
    assert last["max_matsubara_identity_residual"] < 1e-7
    assert last["min_position_covariance_increment_eigenvalue"] > -1e-8
    assert last["min_momentum_covariance_reduction_eigenvalue"] > -1e-8
    assert 0 <= last["total_spring_energy_increase"] <= last["reorganisation_energy_bound"]
    assert 0 <= last["total_kinetic_energy_decrease"] <= last["kinetic_decrease_bound"]
    assert results[-1]["max_momentum_covariance_difference"] < 1e-7
    print(json.dumps(results, indent=2))
