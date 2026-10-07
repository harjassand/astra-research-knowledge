"""Finite diagnostic for the energy-to-commutator inequality on a qubit cloner."""
import numpy as np

rng = np.random.default_rng(20261007)
lam = 2.0 / 3.0

def hermitian_contraction():
    z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    h = (z + z.conj().T) / 2
    return h / np.linalg.norm(h, 2)

def phi(a):
    return lam * a + (1.0 - lam) * np.trace(a).real * np.eye(2) / 2

def tau(a):
    return np.trace(a).real / 2

def hsn(a):
    return np.sqrt(max(0.0, tau(a.conj().T @ a)))

def energy(a):
    return tau(a @ (a - phi(a)))

constant = 2.0 + np.sqrt(2.0)
worst_ratio = 0.0
for _ in range(2000):
    a, b = hermitian_contraction(), hermitian_contraction()
    ea, eb = energy(a), energy(b)
    lhs = hsn(a @ b - b @ a)
    rhs = constant * (np.sqrt(max(ea, 0.0)) + np.sqrt(max(eb, 0.0)))
    worst_ratio = max(worst_ratio, lhs / max(rhs, 1e-15))
    assert lhs <= rhs + 2e-12, (lhs, rhs, ea, eb)
print({"seed": 20261007, "fixtures": 2000, "channel": "qubit universal cloner marginal, lambda=2/3", "max_lhs_over_rhs": worst_ratio, "passed": True})
