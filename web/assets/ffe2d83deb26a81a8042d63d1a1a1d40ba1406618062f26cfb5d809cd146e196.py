"""Finite diagnostics only; proofs are in RESULTS.md. No asymptotic certification."""
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(714190)

def exp_hermitian(x):
    v, u = np.linalg.eigh(x)
    return (u * np.exp(v)) @ u.conj().T

def log_hermitian(x):
    v, u = np.linalg.eigh(x)
    return (u * np.log(v)) @ u.conj().T

def hermitian(n):
    z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return (z + z.conj().T) / 2

def gibbs(logw, a):
    x = exp_hermitian(logw + a)
    return x / np.trace(x).real

stats = {"fixtures": 0, "max_wy_bound_ratio": 0., "max_central_kl_bound_ratio": 0.}
for n in [2, 3, 7, 16]:
    for _ in range(100):
        e = rng.uniform(-4, 4, n)
        beta = rng.uniform(.1, 2)
        p = np.exp(-beta * e)
        p /= p.sum()
        w = np.diag(p)
        a = hermitian(n)
        comm_s = np.sqrt(p)[:, None] * a - a * np.sqrt(p)[None, :]
        comm_h = e[:, None] * a - a * e[None, :]
        lhs = np.vdot(comm_s, comm_s).real
        rhs = beta**2 / 4 * np.trace(w @ comm_h.conj().T @ comm_h).real
        assert lhs <= rhs + 1e-10
        stats["max_wy_bound_ratio"] = max(stats["max_wy_bound_ratio"], lhs / rhs)

        c = rng.uniform(.2, 2)
        a *= c / max(abs(np.linalg.eigvalsh(a)))
        b = np.diag(rng.uniform(-c, c, n))
        d = a-b
        ra, rb = gibbs(np.diag(np.log(p)), a), gibbs(np.diag(np.log(p)), b)
        kl = np.trace(rb @ (log_hermitian(rb)-log_hermitian(ra))).real
        eps = np.trace(w @ d @ d).real
        kc = np.expm1(2*c)/(4*c*c) - 1/(2*c)
        bound = np.exp(2*c) * kc * eps
        assert kl <= bound + 1e-9
        stats["max_central_kl_bound_ratio"] = max(stats["max_central_kl_bound_ratio"], kl/bound)
        stats["fixtures"] += 1

stats["scope"] = "Random finite fixtures check constants and matrix conventions only."
out = Path(__file__).with_name("bridge_diagnostics.json")
out.write_text(json.dumps(stats, indent=2)+"\n")
print(json.dumps(stats, indent=2))
