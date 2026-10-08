"""Finite interface checks only; this is not validation of the asymptotic theorem."""
import itertools
import json
from pathlib import Path

import numpy as np


def kron_all(items):
    out = np.array([[1.0 + 0j]])
    for item in items:
        out = np.kron(out, item)
    return out


def partial_trace_last(rho, d, n, r):
    shaped = rho.reshape(d**r, d ** (n - r), d**r, d ** (n - r))
    return np.einsum("abcb->ac", shaped)


def local_basis(tau):
    d = tau.shape[0]
    candidates = [np.eye(d, dtype=complex)]
    for a, b in itertools.product(range(d), repeat=2):
        item = np.zeros((d, d), dtype=complex)
        item[a, b] = 1
        candidates.append(item)
    basis = []
    for item in candidates:
        item = item.copy()
        for old in basis:
            item -= old * np.trace(tau @ old.conj().T @ item)
        norm2 = np.trace(tau @ item.conj().T @ item).real
        if norm2 > 1e-20:
            basis.append(item / np.sqrt(norm2))
    assert len(basis) == d * d
    return basis


def weighted_parseval(rho, tau, r):
    basis = local_basis(tau)
    invsigma = kron_all([np.linalg.inv(tau)] * r)
    sigma = kron_all([tau] * r)
    chi = (np.trace(rho @ rho @ invsigma) - 1).real
    total = 0.0
    first_order = 0.0
    for index in itertools.product(range(len(basis)), repeat=r):
        active = sum(a != 0 for a in index)
        coefficient = np.trace(rho @ kron_all([basis[a].conj().T for a in index]))
        if active:
            total += abs(coefficient) ** 2
        if active == 1:
            first_order += abs(coefficient) ** 2
    commutator = np.linalg.norm(rho @ sigma - sigma @ rho)
    assert abs(chi - total) < 1e-10
    assert first_order < 1e-20
    return {"chi": chi, "parseval": total, "first_order_squared_norm": first_order,
            "commutator_frobenius_norm": float(commutator)}


def collective(local, n):
    d = local.shape[0]
    return sum(kron_all([local if j == i else np.eye(d) for j in range(n)])
               for i in range(n))


def spin_one_state(n):
    sx = np.array([[0, 1], [1, 0]], dtype=complex) / 2
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2
    sz = np.diag([1.0, -1.0]) / 2
    jx, jy, jz = [collective(x, n) for x in (sx, sy, sz)]
    casimir = jx @ jx + jy @ jy + jz @ jz
    values, vectors = np.linalg.eigh(casimir)
    block = vectors[:, np.abs(values - 2) < 1e-9]
    projector = block @ block.conj().T
    h = 0.6 * jz + 0.25 * (jx @ jz + jz @ jx) + 0.12 * (jy @ jy)
    hv, hu = np.linalg.eigh(h)
    exponential = (hu * np.exp(hv)) @ hu.conj().T
    rho = projector @ exponential @ projector
    rho /= np.trace(rho)
    return rho


def main():
    # lambda=(3,1) at N=4 removes one determinant column and leaves mu=(2,0).
    # The same polynomial of collective generators gives the same arbitrary
    # spin-one irrep density, with identity on physical multiplicities.
    rho4 = spin_one_state(4)
    rho_mu = spin_one_state(2)
    tau4 = partial_trace_last(rho4, 2, 4, 1)
    tau_mu = partial_trace_last(rho_mu, 2, 2, 1)
    marginal_error = np.linalg.norm(tau4 - (np.eye(2) + 2 * tau_mu) / 4)
    assert marginal_error < 1e-10
    x = np.array([[0.3 + 0.2j, 0.4 - 0.1j], [-0.2 + 0.35j, -0.1j]])
    g = np.eye(2) + 0.23 * x
    actual = np.trace(rho4 @ kron_all([g] * 4))
    predicted = np.linalg.det(g) * np.trace(rho_mu @ kron_all([g] * 2))
    character_error = abs(actual - predicted)
    assert character_error < 1e-10
    rho2 = partial_trace_last(rho4, 2, 4, 2)
    qubit_parseval = weighted_parseval(rho2, tau4, 2)
    assert qubit_parseval["commutator_frobenius_norm"] > 1e-5

    # Independent d=3 check of the complex weighted basis on a noncommuting,
    # permutation-invariant two-site state. No tail or asymptotic claim is tested.
    rng = np.random.default_rng(975531)
    matrix = rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))
    rho = matrix @ matrix.conj().T
    rho /= np.trace(rho)
    swap = np.array([3 * b + a for a, b in itertools.product(range(3), repeat=2)])
    rho = (rho + rho[np.ix_(swap, swap)]) / 2
    tau = partial_trace_last(rho, 3, 2, 1)
    qutrit_parseval = weighted_parseval(rho, tau, 2)
    assert qutrit_parseval["commutator_frobenius_norm"] > 1e-5

    result = {"scope": "finite interface diagnostics only, not asymptotic theorem validation",
              "qubit_determinant_twist_absolute_error": float(character_error),
              "qubit_marginal_identity_frobenius_error": float(marginal_error),
              "qubit_noncommuting_parseval": qubit_parseval,
              "qutrit_noncommuting_parseval": qutrit_parseval}
    target = Path(__file__).with_name("interface_checks.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
