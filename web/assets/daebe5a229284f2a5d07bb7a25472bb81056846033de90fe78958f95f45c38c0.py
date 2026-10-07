"""Finite diagnostics for the analytical POVM/Luders Dirichlet theorem.

These fixtures do not prove the unrestricted broadcasting conjecture.
Only NumPy is used; no optimization solver is called.
"""

import json
import platform
import sys

import numpy as np


rng = np.random.default_rng(701471523)


def hermitian_basis(d):
    out = []
    for i in range(d):
        x = np.zeros((d, d), dtype=complex)
        x[i, i] = np.sqrt(d)
        out.append(x)
    for i in range(d):
        for j in range(i + 1, d):
            x = np.zeros((d, d), dtype=complex)
            x[i, j] = x[j, i] = np.sqrt(d / 2)
            out.append(x)
            x = np.zeros((d, d), dtype=complex)
            x[i, j] = -1j * np.sqrt(d / 2)
            x[j, i] = 1j * np.sqrt(d / 2)
            out.append(x)
    return out


def sqrt_psd(x):
    ev, u = np.linalg.eigh(x)
    return (u * np.sqrt(np.maximum(ev, 0))) @ u.conj().T


def norm1(x):
    return float(np.sum(np.abs(np.linalg.eigvalsh((x + x.conj().T) / 2))))


def partial_trace(x, d, keep):
    a = x.reshape(d, d, d, d)
    return np.einsum("abcb->ac", a) if keep == 0 else np.einsum("abad->bd", a)


def povm(d, outcomes):
    raw = []
    for _ in range(outcomes):
        z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        raw.append(z.conj().T @ z)
    ev, u = np.linalg.eigh(sum(raw))
    inv = (u * (ev ** -0.5)) @ u.conj().T
    return [inv @ g @ inv for g in raw]


def superoperator(f, basis, d):
    return np.array([[np.trace(a @ f(b)).real / d for b in basis] for a in basis])


records = {
    "python_version": sys.version,
    "platform": platform.platform(),
    "numpy_version": np.__version__,
    "seed": 701471523,
    "solver": None,
    "povm_fixtures": [],
    "tensor_fixtures": [],
}
saved = []

for d in range(2, 9):
    for trial in range(4):
        effects = povm(d, 2 + trial)
        roots = [sqrt_psd(m) for m in effects]
        basis = hermitian_basis(d)

        def luders(a):
            return sum(k @ a @ k for k in roots)

        def measure_prepare(a):
            return sum(np.trace(m @ a) * m / np.trace(m) for m in effects)

        def s_map(a):
            return (luders(a) + measure_prepare(a)) / 2

        l = superoperator(luders, basis, d)
        p = superoperator(measure_prepare, basis, d)
        s = (l + p) / 2
        ident = np.eye(d * d)
        lower = min(np.linalg.eigvalsh(p)[0], np.linalg.eigvalsh(l - p)[0],
                    np.linalg.eigvalsh(ident - l)[0],
                    np.linalg.eigvalsh(2 * (ident - s) - (ident - p))[0])
        assert lower > -2e-12
        assert np.max(np.abs(l - l.T)) < 2e-12
        assert np.max(np.abs(p - p.T)) < 2e-12

        a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        a = (a + a.conj().T) / 2
        a -= np.trace(a) * np.eye(d) / d
        a /= np.max(np.abs(np.linalg.eigvalsh(a)))
        theta = 0.5
        h = theta * a
        rho = (np.eye(d) + h) / d
        joint = sum(np.kron(k @ rho @ k, m / np.trace(m))
                    for k, m in zip(roots, effects))
        swapped = joint.reshape(d, d, d, d).transpose(1, 0, 3, 2).reshape(d*d, d*d)
        symmetric_joint = (joint + swapped) / 2
        target = s_map(rho)
        marginal_defect = max(np.max(np.abs(partial_trace(symmetric_joint, d, j) - target))
                              for j in (0, 1))
        r = norm1(target - rho)
        error = norm1(measure_prepare(rho) - rho) / 2
        bound = np.sqrt(2 * theta * r) / 2
        assert error <= bound + 1e-12
        assert marginal_defect < 2e-12
        assert np.linalg.eigvalsh(symmetric_joint)[0] > -2e-12
        assert abs(np.trace(symmetric_joint) - 1) < 2e-12
        assert np.max(np.abs(s_map(np.eye(d)) - np.eye(d))) < 2e-12

        record = {
            "d": d,
            "outcomes": len(effects),
            "loewner_min_eigenvalue": float(lower),
            "joint_marginal_max_abs_error": float(marginal_defect),
            "residual_full_trace": r,
            "EB_error_half_trace": error,
            "analytical_bound": float(bound),
            "local_L_Psi_commutator_2": float(np.linalg.norm(l @ p - p @ l)),
        }
        records["povm_fixtures"].append(record)
        if d <= 3:
            saved.append((d, s, p))

for j in range(0, len(saved), 2):
    da, sa, pa = saved[j]
    db, sb, pb = saved[(j + 1) % len(saved)]
    st = np.kron(sa, sb)
    pt = np.kron(pa, pb)
    ident = np.eye((da * db) ** 2)
    lower = min(np.linalg.eigvalsh(st - pt)[0],
                np.linalg.eigvalsh(2 * (ident - st) - (ident - pt))[0])
    assert lower > -5e-12
    records["tensor_fixtures"].append({
        "dimensions": [da, db],
        "loewner_min_eigenvalue": float(lower),
    })

records["status"] = "PASS: finite POVM/Luders and tensor diagnostics; unrestricted theorem unproved."
with open("work/cycle4/luders_dirichlet_checks.json", "w") as f:
    json.dump(records, f, indent=2)
print(json.dumps({
    "status": records["status"],
    "python_version": platform.python_version(),
    "numpy_version": np.__version__,
    "povm_fixtures": len(records["povm_fixtures"]),
    "tensor_fixtures": len(records["tensor_fixtures"]),
    "worst_marginal_error": max(x["joint_marginal_max_abs_error"] for x in records["povm_fixtures"]),
    "smallest_Loewner_eigenvalue": min(x["loewner_min_eigenvalue"] for x in records["povm_fixtures"] + records["tensor_fixtures"]),
    "maximum_local_L_Psi_commutator_2": max(x["local_L_Psi_commutator_2"] for x in records["povm_fixtures"]),
}, indent=2))
