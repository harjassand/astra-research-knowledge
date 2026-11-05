"""Floating diagnostics of a proved identity, not an interval or laboratory proof."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent


def mechanical_matrix(gamma, mu, mass, bath, coupling):
    n = len(coupling)
    mat = np.zeros((2 + n, 2 + n))
    mat[0, 1] = np.sqrt(mu / mass)
    mat[1, 0] = -np.sqrt(mu / mass)
    mat[1, 1] = -gamma / mass
    mat[1, 2:] = -coupling / np.sqrt(mass)
    mat[2:, 1] = coupling / np.sqrt(mass)
    mat[2:, 2:] = bath
    inp = np.zeros(2 + n); inp[1] = 1 / np.sqrt(mass)
    out = np.zeros(2 + n); out[0] = 1 / np.sqrt(mu)
    return mat, inp, out


def check(mat, inp, out, gamma, mu, times):
    ident = np.eye(len(inp))
    def step(t):
        return float(out @ np.linalg.solve(mat, (expm(t * mat) - ident) @ inp))
    def impulse(t):
        return float(out @ expm(t * mat) @ inp)
    rows = np.array([out @ expm(t * mat) for t in times])
    actual = rows @ rows.T
    maximum = np.empty_like(actual)
    for i, t in enumerate(times):
        for j, s in enumerate(times):
            integral, _ = quad(lambda u: impulse(t-u) * impulse(s-u),
                               0., min(t, s), epsabs=2e-13, epsrel=2e-13)
            maximum[i, j] = 1 / mu - step(abs(t-s)) - 2 * gamma * integral
    return {
        "actual_gram_eigenvalues": np.linalg.eigvalsh(actual).tolist(),
        "maximum_gram_eigenvalues": np.linalg.eigvalsh(maximum).tolist(),
        "difference_eigenvalues": np.linalg.eigvalsh(maximum-actual).tolist(),
        "max_entry_difference": float(np.max(abs(maximum-actual))),
        "actual_gram": actual.tolist(),
        "maximum_gram": maximum.tolist(),
    }


def main():
    gamma, mu, mass = 1., 1., 1.
    times = np.array([.05, .2, .4, .7, 1.1, 1.6, 2.2, 3.])
    conservative = np.array([[0., -1.3, 0., 0.], [1.3, 0., 0., 0.],
                             [0., 0., 0., -2.7], [0., 0., 2.7, 0.]])
    mat, inp, out = mechanical_matrix(gamma, mu, mass, conservative,
                                      np.array([.6, .2, .4, -.1]))
    finite = check(mat, inp, out, gamma, mu, times)
    mat, inp, out = mechanical_matrix(gamma, mu, mass, np.array([[-.7]]),
                                      np.array([np.sqrt(.8)]))
    maxwell = check(mat, inp, out, gamma, mu, times)
    assert finite["max_entry_difference"] < 2e-11
    assert min(maxwell["difference_eigenvalues"]) > -2e-11
    assert min(maxwell["maximum_gram_eigenvalues"]) > 1e-10
    result = {
        "scope": "Floating finite-matrix diagnostic, not interval verification or physical data.",
        "times": times.tolist(),
        "finite_conservative_bath_full_dimension": 6,
        "conservative_completion_identity": finite,
        "one_dissipative_bath_actual_full_dimension": 3,
        "same_response_maximum_preparation": maxwell,
        "interpretation": "The finite conservative case agrees with its response-derived kernel. The third-order dissipative response has a larger, full-rank eight-time preparation kernel over its conservative completion class.",
    }
    (ROOT / "completion_kernel_checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"conservative_max_identity_error": finite["max_entry_difference"],
                      "maximum_kernel_min_eigenvalue": min(maxwell["maximum_gram_eigenvalues"]),
                      "dominance_min_eigenvalue": min(maxwell["difference_eigenvalues"])}, indent=2))


if __name__ == "__main__":
    main()
