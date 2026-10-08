"""Monte Carlo sanity check for the Haar fourth-moment contraction identity.

The derivation in CYCLE2_REPORT.md is the proof; this script is only a finite
diagnostic on random trace-zero Hermitian operators supported on Sym^2(C^d).
"""
import numpy as np


def symmetric_embedding(d):
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    V = np.zeros((d * d, len(pairs)), dtype=complex)
    for k, (i, j) in enumerate(pairs):
        if i == j:
            V[i * d + j, k] = 1
        else:
            V[i * d + j, k] = V[j * d + i, k] = 1 / np.sqrt(2)
    return V


def check_dimension(d, samples=120_000, seed=4000):
    rng = np.random.default_rng(seed + d)
    V = symmetric_embedding(d)
    n_sym = V.shape[1]
    Z = rng.normal(size=(n_sym, n_sym)) + 1j * rng.normal(size=(n_sym, n_sym))
    H = (Z + Z.conj().T) / 2
    H -= np.trace(H).real / n_sym * np.eye(n_sym)
    D = V @ H @ V.conj().T
    D4 = D.reshape(d, d, d, d)
    partial = np.einsum("ij kj->ik", D4, optimize=True)
    denominator = d * (d + 1) * (d + 2) * (d + 3)
    rhs = (4 * np.linalg.norm(D, "fro") ** 2 + 16 * np.linalg.norm(partial, "fro") ** 2) / denominator

    X = rng.normal(size=(samples, d)) + 1j * rng.normal(size=(samples, d))
    X /= np.linalg.norm(X, axis=1)[:, None]
    q = np.einsum(
        "ni,nj,ijkl,nk,nl->n",
        X.conj(), X.conj(), D4, X, X,
        optimize=True,
    )
    lhs = np.mean(np.real(q) ** 2)
    return lhs, rhs, lhs / rhs


if __name__ == "__main__":
    for dimension in (2, 3, 4):
        lhs, rhs, ratio = check_dimension(dimension)
        print(
            f"d={dimension}: Haar_MC={lhs:.8g}, contraction={rhs:.8g}, "
            f"ratio={ratio:.6f}"
        )
