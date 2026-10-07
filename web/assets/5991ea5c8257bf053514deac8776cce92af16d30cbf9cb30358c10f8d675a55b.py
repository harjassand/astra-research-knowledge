"""Finite spectral diagnostics for the flagged-clique Choi witness.

This checks explicit matrices, not a channel SDP or asymptotic construction.
Run with the locally available NumPy. No files outside this worker's scope.
"""

import json
import math
import numpy as np


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron_all(factors):
    out = np.ones((1, 1), dtype=complex)
    for factor in factors:
        out = np.kron(out, factor)
    return out


def clifford(r):
    m = r // 2
    generators = []
    for j in range(m):
        for pauli in (X, Y):
            generators.append(kron_all([Z] * j + [pauli] + [I2] * (m-j-1)))
    if r % 2:
        generators.append(kron_all([Z] * m))
    ident = np.eye(2**m)
    defect = 0.0
    for i, a in enumerate(generators):
        for j, b in enumerate(generators):
            defect = max(defect, float(np.max(np.abs(a@b+b@a-(2*ident if i == j else 0)))))
    assert defect < 1e-12
    return generators


def witness(a, b, c):
    dim = a[0].shape[0]
    ident = np.eye(dim)
    result = np.zeros((dim**3, dim**3), dtype=complex)
    for aa, bb, cc in zip(a, b, c):
        result += np.kron(np.kron(aa.T, bb), ident)
        result += np.kron(np.kron(aa.T, ident), cc)
    return result


def spectral_record(k, analytical_bound):
    eigenvalues = np.linalg.eigvalsh(k)
    opnorm = float(np.max(np.abs(eigenvalues)))
    assert opnorm <= analytical_bound + 1e-9
    return {
        "matrix_dimension": k.shape[0],
        "largest_eigenvalue": float(eigenvalues[-1]),
        "operator_norm": opnorm,
        "analytical_bound": analytical_bound,
        "slack": analytical_bound-opnorm,
    }


def affine_flag_operators(q):
    # This diagnostic uses prime q only. The proof also covers prime powers.
    points = [(x, y) for x in range(q) for y in range(q)]
    point_index = {point: index for index, point in enumerate(points)}
    directions = [(0, 1)] + [(1, slope) for slope in range(q)]
    gamma = clifford(q)
    h = gamma[0].shape[0]
    result = []
    partitions = []
    for vx, vy in directions:
        lines = sorted({tuple(sorted(point_index[((x+t*vx) % q, (y+t*vy) % q)]
                                     for t in range(q))) for x, y in points})
        assert len(lines) == q
        assert sorted(i for line in lines for i in line) == list(range(q*q))
        operators = [None] * (q*q)
        for line_index, line in enumerate(lines):
            for coordinate, point in enumerate(line):
                factors = [np.eye(h)] * q
                factors[line_index] = gamma[coordinate]
                operators[point] = kron_all(factors)
        partitions.append(lines)
        result.append(operators)
    for p, left in enumerate(partitions):
        for right in partitions[p+1:]:
            assert max(len(set(a) & set(b)) for a in left for b in right) == 1
    return result


records = {"numpy_version": np.__version__, "local_aligned": [], "affine_flags": [], "random_pair_sos": []}
for r in range(2, 8):
    gamma = clifford(r)
    k = witness(gamma, gamma, gamma)
    record = {"r": r, **spectral_record(k, r*math.sqrt(2))}
    record["observed_formula_diagnostic_only"] = r+1 if r % 2 else math.sqrt(r*(r+2))
    records["local_aligned"].append(record)
    print(json.dumps({"local": record}), flush=True)

for q in (2, 3):
    flags = affine_flag_operators(q)
    cases = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2)]
    for p, b, c in cases:
        bound = q*q*math.sqrt(2)
        k = witness(flags[p], flags[b], flags[c])
        record = {"q": q, "n": q*q, "flags": [p, b, c], **spectral_record(k, bound)}
        records["affine_flags"].append(record)
        print(json.dumps({"affine": record}), flush=True)

rng = np.random.default_rng(20261007)
def random_involution(dim):
    raw = rng.normal(size=(dim, dim))+1j*rng.normal(size=(dim, dim))
    unitary, _ = np.linalg.qr(raw)
    return unitary@np.diag([1]*(dim//2)+[-1]*(dim-dim//2))@unitary.conj().T

for trial in range(30):
    dim = 2 if trial < 15 else 4
    b1, b2, c1, c2 = [random_involution(dim) for _ in range(4)]
    b1 = kron_all([I2, b1, np.eye(dim)])
    b2 = kron_all([I2, b2, np.eye(dim)])
    c1 = kron_all([I2, np.eye(dim), c1])
    c2 = kron_all([I2, np.eye(dim), c2])
    g1 = kron_all([X, np.eye(dim), np.eye(dim)])
    g2 = kron_all([Y, np.eye(dim), np.eye(dim)])
    f = 1j*g1@g2
    k = g1@(b1+c1)+g2@(b2+c2)
    m = b1-c1+1j*f@(b2-c2)
    residual = 8*np.eye(k.shape[0])-k@k-m.conj().T@m
    defect = float(np.max(np.abs(residual)))
    assert defect < 1e-10
    record = {"trial": trial, "receiver_dimension": dim, "sos_residual_max_abs": defect,
              **spectral_record(k, 2*math.sqrt(2))}
    records["random_pair_sos"].append(record)

print(json.dumps({"pair_sos_trials": len(records["random_pair_sos"]),
                  "max_sos_residual": max(x["sos_residual_max_abs"] for x in records["random_pair_sos"])}))

records["status"] = "All finite operator bounds passed; no channel optimization was performed."
with open("work/cycle3/clifford_broadcast_check.json", "w") as output:
    json.dump(records, output, indent=2)
