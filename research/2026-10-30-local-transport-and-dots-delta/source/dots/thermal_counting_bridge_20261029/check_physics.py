"""Dense-matrix sanity checks of PHYSICS_THEOREM.md; not a substitute for proof."""
import csv
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.special import logsumexp

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261029)


def embed(a, support, n):
    out = np.zeros((2**n, 2**n), dtype=complex)
    for col in range(2**n):
        b = [(col >> (n - 1 - j)) & 1 for j in range(n)]
        lc = sum(b[s] << (len(support) - 1 - j) for j, s in enumerate(support))
        for lr in range(2**len(support)):
            bb = b.copy()
            for j, s in enumerate(support):
                bb[s] = (lr >> (len(support) - 1 - j)) & 1
            row = sum(bb[j] << (n - 1 - j) for j in range(n))
            out[row, col] += a[lr, lc]
    return out


def random_term(support, n):
    d = 2**len(support)
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    a = (a + a.conj().T) / 2
    a /= np.linalg.norm(a, 2)
    return embed(a, support, n)


def opnorm(a):
    return float(np.linalg.norm(a, 2))


def herm(a):
    return (a + a.conj().T) / 2


rows = []
cases = [
    (2, [(0, 1)], "edge"),
    (4, [(a, b) for a in range(4) for b in range(a + 1, 4)], "K4"),
    (6, [(a, b) for a in range(3) for b in range(3, 6)], "K3_3"),
]
for n, edges, label in cases:
    supports = [tuple(e) for e in edges] + [(i,) for i in range(n)]
    local = [random_term(s, n) for s in supports]
    m = len(local)
    D = max(sum(i in s for s in supports) for i in range(n))
    colors = []
    for s in supports:
        banned = {colors[j] for j, old in enumerate(supports[:len(colors)]) if set(s) & set(old)}
        c = 0
        while c in banned:
            c += 1
        colors.append(c)
    q = max(colors) + 1
    assert q <= 2 * (D - 1) + 1
    Hs = [sum((local[j] for j in range(m) if colors[j] == c), np.zeros_like(local[0])) for c in range(q)]
    for c in range(q):
        ss = [set(supports[j]) for j in range(m) if colors[j] == c]
        assert all(not (a & b) for j, a in enumerate(ss) for b in ss[j+1:])
    H = sum(Hs)
    evalH = np.linalg.eigvalsh(H)
    M = sum(2**ell for ell in range(1, q + 1))
    for beta in [0.7, 4.0]:
        logZ = logsumexp(-beta * evalH)
        for r in [16, 32, 64, 128]:
            delta = beta / r
            Es = [expm(-delta * hj / 2) for hj in Hs]
            Q = np.eye(2**n, dtype=complex)
            for e in Es:
                Q = e @ Q
            P = herm(Q.conj().T @ Q)
            evalP, vecP = np.linalg.eigh(P)
            assert min(evalP) > 0
            logP = herm((vecP * np.log(evalP)) @ vecP.conj().T)
            effective_error = opnorm(logP + delta * H)
            x = M * delta  # J = 1
            step_bound = 2 * m / M * (np.sinh(x) - x)
            logZr = logsumexp(r * np.log(evalP))
            density_error = abs(logZr - logZ) / n
            density_bound = 2 * D * r / M * (np.sinh(x) - x)
            # Check the actual relative sandwich too, not just its conclusion.
            R = Q @ expm(delta * H / 2)
            evS = np.linalg.eigvalsh(herm(R.conj().T @ R))
            relative_log_error = max(abs(np.log(evS)))
            assert relative_log_error <= step_bound + 1e-10
            assert effective_error <= step_bound + 1e-10
            assert density_error <= density_bound + 1e-10
            rows.append(dict(n=n, graph=label, m=m, D=D, q=q, M=M, beta=beta, r=r,
                             step_error=effective_error, step_bound=step_bound,
                             relative_log_error=float(relative_log_error),
                             log_density_error=float(density_error), log_density_bound=float(density_bound)))

with (OUT / "physics_checks.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
summary = {
    "status": "PASS",
    "cases": len(rows),
    "seed": 20261029,
    "maximum_step_error_over_bound": max(r["step_error"] / r["step_bound"] for r in rows),
    "maximum_log_density_error_over_bound": max(r["log_density_error"] / r["log_density_bound"] for r in rows),
    "scope": "Small complex Hermitian, generally non-stoquastic dense-matrix checks; proof is analytic, not numerical.",
}
(OUT / "physics_checks_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
