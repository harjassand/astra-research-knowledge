"""Finite-dimensional diagnostics for an energy-descent completion.

These are numerical checks, not a proof of general correctness, historical
novelty, physical implementability, or efficient ground-state preparation.
The spectral basis used here is a verification device, NOT an assumed input
to the proposed time-domain construction.

Requirements: Python 3.10+, numpy, scipy.
Run: python verify_energy_descent.py
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy.linalg import expm

Matrix = NDArray[np.complex128]


def dstar(jump: Matrix, observable: Matrix) -> Matrix:
    r = jump.conj().T @ jump
    return jump.conj().T @ observable @ jump - (r @ observable + observable @ r) / 2


def completion(energies: NDArray[np.float64], jump: Matrix) -> tuple[Matrix, Matrix]:
    """Return Hermitian G and C for D[B]^*(H)+i[G,H] = -C^*C.

    The supplied B must contain strictly downward matrix elements only.
    """
    energies = np.asarray(energies, dtype=float)
    jump = np.asarray(jump, dtype=complex)
    d = len(energies)
    if jump.shape != (d, d):
        raise ValueError("Inconsistent dimensions")
    drops = energies[None, :] - energies[:, None]
    if np.linalg.norm(jump[drops <= 0]) > 1e-11:
        raise ValueError("Jump includes zero-energy or upward matrix elements")
    roots = np.sqrt(np.maximum(drops, 0))
    c = roots * jump
    g = np.zeros_like(jump)
    for m in range(d):
        active = np.flatnonzero(drops[m] > 0)
        for n in active:
            for p in active:
                x, y = roots[m, n], roots[m, p]
                g[n, p] += 0.5j * (x-y)/(x+y) * jump[m, n].conjugate() * jump[m, p]
    return g, c


def cauchy_drift(energies: NDArray[np.float64], b: Matrix,
                 cutoff: float | None = None) -> Matrix:
    """Exact dual energy drift of int_0^cutoff D[e^{sH} B e^{-sH}] ds."""
    d = len(energies)
    result = np.zeros_like(b)
    for m in range(d):
        for n in range(d):
            x = energies[n]-energies[m]
            if x <= 0:
                continue
            for p in range(d):
                y = energies[p]-energies[m]
                if y <= 0:
                    continue
                factor = 1.0 if cutoff is None else -np.expm1(-cutoff*(x+y))
                result[n, p] -= 0.5*factor*b[m, n].conjugate()*b[m, p]
    return result


def full_generator(h: Matrix, g: Matrix, b: Matrix) -> Matrix:
    """Column-major vectorization of -i[H+G,rho]+D[B](rho)."""
    d = h.shape[0]
    eye = np.eye(d)
    a = h+g
    r = b.conj().T @ b
    return (-1j*(np.kron(eye, a)-np.kron(a.T, eye))
            + np.kron(b.conjugate(), b)
            - 0.5*(np.kron(eye, r)+np.kron(r.T, eye)))


def kron_all(items: list[Matrix]) -> Matrix:
    out = np.ones((1, 1), dtype=complex)
    for item in items:
        out = np.kron(out, item)
    return out


def main() -> None:
    rng = np.random.default_rng(20261013)
    report: dict[str, object] = {
        "status": "finite numerical diagnostics only; no physical experiment or priority clearance",
        "seed": 20261013,
    }
    worst_identity = 0.0
    worst_hermiticity = 0.0
    worst_cauchy = 0.0
    worst_truncation = 0.0
    tests = 0
    for d in (2, 3, 4, 6, 8, 12):
        for repetition in range(30):
            e = np.sort(rng.uniform(-2.0, 3.0, d))
            if repetition % 3 == 0 and d >= 3:
                e[1] = e[0]  # include exact degeneracies
            drop = e[None, :]-e[:, None]
            b = (rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)))*(drop > 0)
            b /= max(1.0, np.linalg.norm(b, 2))
            h = np.diag(e)
            g, c = completion(e, b)
            drift = dstar(b, h)+1j*(g@h-h@g)
            error = float(np.linalg.norm(drift+c.conj().T@c, 2))
            worst_identity = max(worst_identity, error)
            worst_hermiticity = max(worst_hermiticity, float(np.linalg.norm(g-g.conj().T, 2)))
            assert error < 5e-12
            assert np.linalg.eigvalsh(drift).max() < 5e-12
            err_c = np.linalg.norm(cauchy_drift(e, b)+b.conj().T@b/2, 2)
            worst_cauchy = max(worst_cauchy, float(err_c))
            cutoff = 0.7
            bs = b*np.exp(-cutoff*np.maximum(drop, 0))
            err_s = np.linalg.norm(cauchy_drift(e, b, cutoff)
                                   +b.conj().T@b/2-bs.conj().T@bs/2, 2)
            worst_truncation = max(worst_truncation, float(err_s))
            assert err_c < 5e-12 and err_s < 5e-12
            tests += 1
    report["random_matrix_cases"] = tests
    report["max_completion_identity_operator_norm_error"] = worst_identity
    report["max_G_hermiticity_error"] = worst_hermiticity
    report["max_cauchy_identity_error"] = worst_cauchy
    report["max_finite_cutoff_identity_error"] = worst_truncation

    # Exact-rational fixture (floating evaluation of displayed exact values).
    e = np.array([0., 1., 4.])
    h = np.diag(e)
    b = np.array([[0, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=complex)
    g, c = completion(e, b)
    psi = np.array([0, -3, 1], dtype=complex)/np.sqrt(10)
    naive = float(np.vdot(psi, dstar(b, h)@psi).real)
    repaired = float(np.vdot(psi, (dstar(b, h)+1j*(g@h-h@g))@psi).real)
    assert np.isclose(naive, 1/5) and np.isclose(repaired, -1/10)
    assert np.isclose(g[1, 2], -1j/6)
    report["three_level_fixture"] = {
        "energies": e.tolist(), "state": "(-3|1>+|2>)/sqrt(10)",
        "naive_energy_derivative": naive,
        "completed_energy_derivative": repaired,
        "exact_G_12": "-i/6",
        "independent_downward_channels_derivative": -1.3,
    }
    # Confirm dynamics, trace preservation, positivity, and nonincreasing energy.
    liouv = full_generator(h, g, b)
    rho0 = np.outer(psi, psi.conjugate()).reshape(-1, order='F')
    energies_run = []
    min_density_eigenvalue = 1.0
    for t in np.linspace(0, 12, 121):
        rho = (expm(t*liouv)@rho0).reshape((3, 3), order='F')
        energies_run.append(float(np.trace(h@rho).real))
        min_density_eigenvalue = min(min_density_eigenvalue, float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min()))
        assert abs(np.trace(rho)-1) < 1e-11
    assert np.diff(energies_run).max() < 1e-11
    report["three_level_evolution"] = {
        "sampled_times": 121, "initial_energy": energies_run[0],
        "final_energy_at_t12": energies_run[-1],
        "minimum_density_eigenvalue_roundoff": min_density_eigenvalue,
    }

    # Optimal reservoir coherence and the PSD energy-dissipation kernel.
    max_kernel_error = 0.0
    for size in (2, 4, 8, 12):
        w = np.geomspace(0.1, 7.0, size)
        k = 2*np.sqrt(w[:, None]*w[None, :])/(w[:, None]+w[None, :])
        ck = (w[:, None]+w[None, :])*k/2
        max_kernel_error = max(max_kernel_error, float(np.linalg.norm(ck-np.sqrt(w[:, None]*w[None, :]), 2)))
        assert np.linalg.eigvalsh(k).min() > -1e-12
        assert np.linalg.eigvalsh(ck).min() > -1e-12
    report["max_cauchy_kernel_factorization_error"] = max_kernel_error

    # Slow near-degenerate excited pair: no-jump survival exponents.
    slow_cases = []
    for delta in (0.1, 0.03, 0.01, 0.003, 0.001):
        e = np.array([0., 1., 1.+delta])
        g, _ = completion(e, b)
        m = -1j*(np.diag(e)[1:, 1:]+g[1:, 1:])-b.conj().T[1:]@b[:, 1:]/2
        actual = -2*np.linalg.eigvals(m).real.max()
        q = delta/(2*(np.sqrt(1+delta)+1)**2)  # stable root-ratio evaluation
        radicand = delta**2+4*q*q
        predicted = radicand/(1+np.sqrt(1-radicand))
        r = 2*np.sqrt(1+delta)/(2+delta)
        cauchy_rad = delta**2+delta**2/(2+delta)**2
        cauchy_rate = cauchy_rad/(1+np.sqrt(1-cauchy_rad))
        assert abs(actual-predicted) < 3e-14
        slow_cases.append({"delta": delta, "completed_population_decay_exponent": float(actual),
                           "completed_rate_over_delta_squared": float(actual/delta**2),
                           "cauchy_population_decay_exponent": float(cauchy_rate)})
    report["near_degenerate_slowing"] = slow_cases
    report["asymptotic_completed_decay_exponent"] = "(17/32)*delta^2 + O(delta^3), rates and lower excitation energy fixed at 1"

    # Classical metastability defeats every <=2-local Pauli seed on six spins.
    pauli = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex),
             np.array([[0, -1j], [1j, 0]], complex), np.diag([1., -1.]).astype(complex)]
    n, local_limit, field = 6, 2, 0.2
    es = []
    for bitstring in itertools.product((0, 1), repeat=n):
        z = 1-2*np.array(bitstring)
        es.append(-float(sum(z[i]*z[(i+1)%n] for i in range(n)))-field*float(sum(z)))
    es = np.asarray(es)
    trapped = (1<<n)-1
    seed_count = 0
    max_dark = 0.0
    for labels in itertools.product(range(4), repeat=n):
        if not 1 <= sum(label != 0 for label in labels) <= local_limit:
            continue
        a = kron_all([pauli[label] for label in labels])
        filtered = a*((es[None, :]-es[:, None]) > 1e-10)
        max_dark = max(max_dark, float(np.linalg.norm(filtered[:, trapped])))
        # Since a column is zero, the completion G has zero corresponding row/column.
        assert np.linalg.norm(filtered[:, trapped]) == 0
        seed_count += 1
    report["six_spin_metastable_fixture"] = {
        "J": 1, "h": field, "locality_limit": local_limit,
        "all_down_energy": float(es[trapped]), "ground_energy": float(es.min()),
        "energy_excess": float(es[trapped]-es.min()), "seeds_checked": seed_count,
        "max_lowering_seed_action_on_trap": max_dark,
        "minimum_energy_cost_of_nonempty_at_most_k_spin_flip_bound": 4-2*field*local_limit,
    }

    # Unknown-H inverse construction: finite Pauli averaging identity.
    n = 3
    strings = list(itertools.product(range(4), repeat=n))
    support = [s for s in strings if 1 <= sum(x != 0 for x in s) <= 2]
    matrices = [kron_all([pauli[x] for x in s]) for s in strings]
    sm = [kron_all([pauli[x] for x in s]) for s in support]
    coeff = rng.normal(size=len(support))
    hu = sum(c*p for c, p in zip(coeff, sm))
    avg = np.zeros_like(hu)
    probs = []
    for label, p in zip(strings, matrices):
        characters = [(-1)**sum(a != 0 and c != 0 and a != c for a, c in zip(label, q)) for q in support]
        prob = (1-sum(characters)/len(support))/(4**n)
        probs.append(prob)
        avg += prob*(p@hu@p)
    err_inv = float(np.linalg.norm(avg+hu/len(support), 2))
    assert min(probs) >= -1e-14 and abs(sum(probs)-1) < 1e-13 and err_inv < 1e-12
    report["Pauli_inverse_average_fixture"] = {
        "qubits": n, "candidate_terms_K": len(support),
        "minimum_probability": float(min(probs)), "probability_sum": float(sum(probs)),
        "average_identity_error": err_inv,
        "scope": "verifies algebra only; no finite pulse circuit or lab experiment executed",
    }
    out = Path(__file__).with_name("diagnostics.json")
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
