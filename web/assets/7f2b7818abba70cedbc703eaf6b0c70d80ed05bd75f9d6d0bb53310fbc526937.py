"""Small floating-point audit of the proposed weighted wall count.

This is intentionally diagnostic, not a proof of a uniform spectral bound.
It constructs the carriers through the local contraction-kernel checker,
forms L_w on HS(V), and prints D_w(x/N^2) for x<=N.
"""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[5]
CHECKER = ROOT / "outputs/research/sol_semiclassical_memory/regular_su3/verify_regular_su3.py"
spec = importlib.util.spec_from_file_location("regular_su3_checker", CHECKER)
su3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(su3)


def spectrum_case(a: int, b: int) -> dict:
    ts, _ambient = su3.harmonic_carrier(a, b)
    d = ts[0].shape[0]
    n = a + b
    B = b + 1
    C2 = (a * a + a * b + b * b + 3 * a + 3 * b) / 3
    C3 = (a - b) * (2 * a + b + 3) * (a + 2 * b + 3) / 18
    alpha = C3 / C2
    C_S = (C2 * (C2 / 3 + 0.25) - C3 * C3 / C2) / n**2
    D_ops = [
        sum(su3.d_symbol[k, i, j] * ts[i] @ ts[j]
            for i in range(8) for j in range(8))
        for k in range(8)
    ]
    ss = [(D_ops[k] - alpha * ts[k]) / n for k in range(8)]

    # For column-major vectorization, vec([G,A])=(I kron G-G^T kron I)vec(A).
    eye = np.eye(d)
    L_w = np.zeros((d * d, d * d), dtype=complex)
    for T_A, S_A in zip(ts, ss):
        ad_T = np.kron(eye, T_A) - np.kron(T_A.T, eye)
        ad_S = np.kron(eye, S_A) - np.kron(S_A.T, eye)
        L_w += ad_T @ ad_T / n**2
        L_w += ad_S @ ad_S / (n * math.sqrt(C_S))
    eigenvalues = np.linalg.eigvalsh(L_w)

    records = []
    for x in range(1, n + 1):
        t = x / n**2
        count = int(np.count_nonzero(eigenvalues <= t + 1e-9)) - 1
        denominator = d * ((n * n / B) * t * t + n**3 * t**3)
        records.append({
            "x": x,
            "D_w_minus_1": count,
            "ratio_to_H_rhs_without_C": count / denominator if denominator else 0.0,
        })

    return {
        "a": a,
        "b": b,
        "N": n,
        "B": B,
        "d": d,
        "gap": float(eigenvalues[1]),
        "records_at_t=x_over_N2": records,
    }


def main() -> None:
    # These intentionally small carriers are outside H's large-b scope.
    cases = [(2, 1), (3, 1), (4, 1), (2, 2), (3, 2)]
    print(json.dumps({"status": "finite-diagnostic-only",
                      "cases": [spectrum_case(a, b) for a, b in cases]}, indent=2))


if __name__ == "__main__":
    main()
