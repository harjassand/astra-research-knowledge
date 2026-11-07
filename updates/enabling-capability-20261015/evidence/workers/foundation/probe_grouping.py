"""Probe a proposed grouping step; floating point is discovery evidence only.

The single-site co-Choi domination is source-derived from Wu--Zou,
arXiv:2608.02647v1, Lemma 7.4. Here we test its grouped analogue.
No random search is a positivity certificate.
"""
from itertools import combinations
import json
from pathlib import Path
import numpy as np


def ptrace(x, dims, keep):
    keep = tuple(keep)
    current = list(range(len(dims)))
    y = x.reshape(tuple(dims) * 2)
    for i in reversed(range(len(dims))):
        if i not in keep:
            p = current.index(i)
            y = np.trace(y, axis1=p, axis2=p + len(current))
            current.pop(p)
    n = int(np.prod([dims[i] for i in keep]))
    return y.reshape(n, n)


def embed(x, dims, keep):
    keep = list(keep)
    other = [i for i in range(len(dims)) if i not in keep]
    order = keep + other
    y = np.kron(x, np.eye(int(np.prod([dims[i] for i in other]))))
    y = y.reshape(tuple(dims[i] for i in order) * 2)
    perm = [order.index(i) for i in range(len(dims))]
    return y.transpose(perm + [i + len(dims) for i in perm]).reshape(int(np.prod(dims)), -1)


def lam(x, dims):
    y = np.zeros_like(x, dtype=complex)
    for n in range(len(dims) + 1):
        for keep in combinations(range(len(dims)), n):
            y += (-.5) ** n * embed(ptrace(x, dims, keep), dims, keep)
    return y


def cochoi_and_switched(u, dims):
    n = len(u)
    basis = np.eye(n)
    a = lam(np.outer(u, u.conj()), dims)
    a_inv = np.linalg.inv(a)
    ell = [lam(np.outer(basis[j], u.conj()), dims) for j in range(n)]
    c = np.zeros((n*n, n*n), complex)
    s = np.zeros_like(c)
    for j in range(n):
        for k in range(n):
            c[k*n:(k+1)*n,j*n:(j+1)*n] = lam(np.outer(basis[j],basis[k]), dims)
            s[k*n:(k+1)*n,j*n:(j+1)*n] = ell[j] @ a_inv @ ell[k].conj().T
    return c, s, a


def probe(u, dims):
    u = u / np.linalg.norm(u)
    c, s, a = cochoi_and_switched(u, dims)
    low, v = np.linalg.eigh(c-s)
    hi = np.linalg.eigvalsh(c+s)
    return {
        "dims": list(dims), "A_min_eigenvalue": float(np.linalg.eigvalsh(a)[0]),
        "C_min_eigenvalue": float(np.linalg.eigvalsh(c)[0]),
        "C_minus_S_min_eigenvalue": float(low[0]),
        "C_plus_S_min_eigenvalue": float(hi[0]),
        "Hermitian_residual_C": float(np.linalg.norm(c-c.conj().T)),
        "Hermitian_residual_S": float(np.linalg.norm(s-s.conj().T)),
        "negative_vector_real": v[:,0].real.tolist(),
        "negative_vector_imag": v[:,0].imag.tolist(),
    }


def main():
    rng = np.random.default_rng(20261015)
    out = {"status": "NUMERICAL_PROBE_ONLY", "seed": 20261015, "rows": []}
    for d in [2,3,4]:
        product = np.zeros(d*d); product[0] = 1
        bell = np.eye(d).reshape(-1) / np.sqrt(d)
        for label,u in [("product",product),("maximally_entangled",bell)]:
            row = probe(u,(d,d)); row["reference"] = label
            out["rows"].append(row)
        u = rng.normal(size=d*d)+1j*rng.normal(size=d*d)
        row=probe(u,(d,d));row["reference"]="seeded_generic"
        out["rows"].append(row)
    p=Path(__file__).with_name("grouping_probe.json")
    p.write_text(json.dumps(out,indent=2)+"\n")
    for row in out["rows"]:
        print({k:row[k] for k in ["dims","reference","C_minus_S_min_eigenvalue","C_plus_S_min_eigenvalue"]})


if __name__ == "__main__":
    main()
