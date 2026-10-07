"""Small exact-interface diagnostics for the Koenig et al. locking ensemble.

Checks Pauli tensor identities and finite-dimensional state distances for q<=3.
It does not compute accessible information; that upper bound is imported from
arXiv:quant-ph/0512021, Lemma 2.
"""
from itertools import product
import numpy as np

I2 = np.eye(2, dtype=complex)
PAULI = {
    1: np.array([[0, 1], [1, 0]], dtype=complex),
    2: np.array([[0, -1j], [1j, 0]], dtype=complex),
    3: np.array([[1, 0], [0, -1]], dtype=complex),
}

def string_op(y):
    out = np.array([[1]], dtype=complex)
    for a in y:
        out = np.kron(out, PAULI[a])
    return out

def trace_distance(a, b):
    return float(np.sum(np.linalg.svd(a-b, compute_uv=False).real) / 2)

def root_fidelity(a, b):
    ea, va = np.linalg.eigh(a)
    sa = (va * np.sqrt(np.maximum(ea, 0))) @ va.conj().T
    vals = np.linalg.eigvalsh(sa @ b @ sa)
    return float(np.sum(np.sqrt(np.maximum(vals, 0))))

for q in range(1, 4):
    D = 2**q
    labels = []
    states = []
    for y in product((1, 2, 3), repeat=q):
        G = string_op(y)
        assert np.allclose(G @ G, np.eye(D))
        assert abs(np.trace(G)) < 1e-9
        for sign in (-1, 1):
            labels.append((sign, y))
            states.append((np.eye(D) + sign * G) / D)
    mean = sum(states) / len(states)
    assert np.allclose(mean, np.eye(D) / D)
    assert all(np.allclose(np.linalg.eigvalsh(s),
                           np.r_[np.zeros(D//2), np.full(D//2, 2/D)])
               for s in states)
    assert all(abs(trace_distance(s, mean) - 0.5) < 1e-9 for s in states)
    min_pair = min(trace_distance(states[i], states[j])
                   for i in range(len(states)) for j in range(i))
    assert min_pair >= 0.5 - 1e-9
    if q >= 2:
        assert abs(min_pair - 0.5) < 1e-9

    if q >= 1:
        # q=1, X and Z observables anticommute; choose the + eigenspaces.
        a = states[labels.index((1, (1,) + (1,)*(q-1)))]
        b = states[labels.index((1, (3,) + (1,)*(q-1)))]
        # For q>1 these strings differ at exactly one site and anticommute.
        F = root_fidelity(a, b)
        # Affinity is Tr(sqrt(a) sqrt(b)); each state is 2P/D.
        Pa = (np.eye(D) + string_op((1,) + (1,)*(q-1))) / 2
        Pb = (np.eye(D) + string_op((3,) + (1,)*(q-1))) / 2
        A = float((2/D) * np.trace(Pa @ Pb).real)
        assert abs(F - 1/np.sqrt(2)) < 1e-8
        assert abs(A - 0.5) < 1e-8
        assert abs(F - A - (1/np.sqrt(2) - 0.5)) < 1e-8
    print({"q": q, "dimension": D, "labels": len(states),
           "mean_trace_distance": 0.5, "minimum_pair_distance": min_pair,
           "anticommuting_pair_gap": 1/np.sqrt(2)-0.5})
