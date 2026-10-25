"""Exact finite charge-algebra checks and a separate cutoff diagnostic.

The normal/host cutoff is NOT a cold-transport or infinite-bath proof.
"""

import json
import numpy as np


def charge_operators(cutoff):
    charges = np.arange(-cutoff, cutoff + 2)
    size = len(charges)
    reflection = np.zeros((size, size), dtype=np.int64)
    for i, n in enumerate(charges):
        reflection[int(1 - n - charges[0]), i] = 1
    force = np.diag(np.ones(size - 1, dtype=np.int64), 1)
    force += force.T
    translation = np.diag([1 if n % 2 == 0 else -1 for n in charges])
    return charges, reflection, force, translation


def exact_checks():
    for cutoff in range(1, 13):
        n, j, q, t = charge_operators(cutoff)
        ident = np.eye(len(n), dtype=np.int64)
        kinetic4 = np.diag((2 * n - 1) ** 2)
        eta_plus256 = np.diag((16 * n - 9) ** 2)
        eta_minus256 = np.diag((16 * n - 7) ** 2)
        assert np.array_equal(j @ j, ident)
        assert np.array_equal(j @ kinetic4, kinetic4 @ j)
        assert np.array_equal(j @ q, q @ j)
        assert np.array_equal(t @ q @ t, -q)
        assert np.array_equal(t @ j @ t, -j)
        assert np.array_equal(j @ eta_plus256 @ j, eta_minus256)
    return {"integer_charge_algebra": "PASS", "charge_cutoffs": [1, 12]}


def diagnostic(cutoff, host=16, recoil=128.0, coupling=0.4, beta=10.0):
    n, j, q, t = charge_operators(cutoff)
    a = np.diag(np.sqrt(np.arange(1, host)), 1)
    x = (a + a.T) / np.sqrt(2)
    p = 1j * (a.T - a) / np.sqrt(2)
    hg = np.diag(np.arange(host) + 0.5)
    ih = np.eye(host)
    parity = np.diag([1 if k % 2 == 0 else -1 for k in range(host)])
    rotor = recoil * np.diag((n - 0.5) ** 2)
    h = np.kron(hg, np.eye(len(n))) + np.kron(ih, rotor) - coupling * np.kron(x, q)
    jf = np.kron(ih, j)
    cf = np.kron(parity, t)
    eigenvalues = np.linalg.eigvalsh(h)

    # Exact J+ restriction; ALL retained normal levels remain.
    embedding = np.zeros((len(n), cutoff + 1))
    for k in range(cutoff + 1):
        embedding[int(-k - n[0]), k] = 1 / np.sqrt(2)
        embedding[int(1 + k - n[0]), k] = 1 / np.sqrt(2)
    qplus = embedding.T @ q @ embedding
    expected = np.diag(np.ones(cutoff), 1) + np.diag(np.ones(cutoff), -1)
    expected[0, 0] = 1
    assert np.max(abs(qplus - expected)) < 1e-14
    hp = np.kron(hg, np.eye(cutoff + 1)) + np.kron(ih, embedding.T @ rotor @ embedding)
    hp -= coupling * np.kron(x, qplus)
    values, vectors = np.linalg.eigh(hp)
    weights = np.exp(-beta * (values - values[0]))
    weights /= weights.sum()

    def mean(op):
        return float(np.real(weights @ np.diag(vectors.conj().T @ op @ vectors)))

    ymean = mean(np.kron(x, np.eye(cutoff + 1)))
    qmean = mean(np.kron(ih, qplus))
    normal_exc = np.eye(cutoff + 1)
    normal_exc[0, 0] = 0
    pvariance = mean(np.kron(p @ p, np.eye(cutoff + 1)))
    return {
        "rotor_charge_cutoff": cutoff,
        "host_oscillator_cutoff": host,
        "max_J_commutator": float(np.max(abs(h @ jf - jf @ h))),
        "max_C_commutator": float(np.max(abs(h @ cf - cf @ h))),
        "largest_eigenvalue_pair_gap": float(np.max(abs(eigenvalues[1::2] - eigenvalues[::2]))),
        "sector_force_mean": qmean,
        "sector_port_mean": ymean,
        "mean_force_balance_residual": abs(ymean - coupling * qmean),
        "free_normal_excited_probability": mean(np.kron(ih, normal_exc)),
        "actual_host_momentum_variance": pvariance,
        "free_host_momentum_variance": float(0.5 / np.tanh(beta / 2)),
    }


if __name__ == "__main__":
    rows = [diagnostic(n) for n in [2, 3, 4]]
    for row in rows:
        assert row["max_J_commutator"] < 1e-12
        assert row["max_C_commutator"] < 1e-12
        assert row["largest_eigenvalue_pair_gap"] < 1e-8
        assert row["sector_force_mean"] > 0.5
        assert row["mean_force_balance_residual"] < 1e-8
        assert row["actual_host_momentum_variance"] <= row["free_host_momentum_variance"] + 1e-8
    print(json.dumps({"exact": exact_checks(), "finite_diagnostics": rows}, indent=2))
