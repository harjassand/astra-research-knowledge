"""Rebuild and audit one selected d=5 compatibility-kernel primal point."""
from __future__ import annotations

import argparse
import json
import numpy as np
from weyl_sdp import compatibility_sdp, line_system, line_cover, data


def encode_complex(a):
    return [[[float(z.real), float(z.imag)] for z in row] for row in a]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--eps", type=float, default=1e-9)
    ap.add_argument("--mix-depolarizing", type=float, default=0.01)
    args = ap.parse_args()
    source = json.load(open(args.candidate))
    d = source["dimension"]
    selection = source["best"]["selection"]
    points, index, qv, lamv, solve = compatibility_sdp(d, eps=args.eps,
                                                       max_iters=400000)
    lines = line_system(d)
    direction = np.zeros(d*d)
    active = 0
    for line, k in zip(lines, selection):
        if k is not None:
            direction[line[k-1]] += 2
            active += 1
    raw = solve(direction)
    X0, q0, lam0 = raw["X"], raw["q"], raw["lambda"]
    a = args.mix_depolarizing
    q = (1-a)*q0 + a/(d*d)
    X = (1-a)*X0 + a*np.eye(d*d)/(d*d)
    lam = np.real(data(d)[3] @ q)
    F = data(d)[2]
    q_compat = np.array([np.real(np.sum(F[:,:,r]*X))/(d*d)
                         for r in range(d*d)])
    beta = X / np.sqrt(np.outer(q, q))
    cover, peaks, terms = line_cover(lam, lines)
    payload = {
        "dimension": d,
        "selection": selection,
        "solver": raw["solver_stats"],
        "solver_status": raw["status"],
        "mix_with_depolarizing_fraction": a,
        "q": q.tolist(),
        "lambda": lam.tolist(),
        "line_cover_budget": cover,
        "line_peaks": peaks,
        "line_terms": terms,
        "X_real_imag": encode_complex(X),
        "beta_real_imag": encode_complex(beta),
        "diagnostics": {
            "q_min": float(q.min()),
            "q_sum_error": float(abs(q.sum()-1)),
            "diag_X_q_max_error": float(np.max(np.abs(np.diag(X).real-q))),
            "compatibility_qprime_q_max_error": float(np.max(np.abs(q_compat-q))),
            "X_hermitian_max_error": float(np.max(np.abs(X-X.conj().T))),
            "X_min_eigenvalue": float(np.linalg.eigvalsh((X+X.conj().T)/2).min()),
            "beta_diag_max_error": float(np.max(np.abs(np.diag(beta)-1))),
            "beta_min_eigenvalue": float(np.linalg.eigvalsh((beta+beta.conj().T)/2).min()),
            "lambda_min": float(lam.min()),
            "target_clipped_sum": float(np.maximum(2*lam-1,0)[1:].sum()),
        },
        "scope": "floating-point primal reconstruction and residual audit; no exact algebraic/rational certificate",
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(json.dumps({k: payload[k] for k in (
        "line_cover_budget", "line_peaks", "line_terms", "diagnostics",
        "solver_status", "solver")}, indent=2))


if __name__ == "__main__":
    main()

