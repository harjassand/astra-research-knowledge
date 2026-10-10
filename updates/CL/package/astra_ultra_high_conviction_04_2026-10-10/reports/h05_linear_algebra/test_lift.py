"""Reproduce GMRES stagnation versus symmetric-dilation residuals.

Uses only NumPy. Full Arnoldi least-squares is used for both systems; on the
Hermitian dilation this computes the MINRES residual minimization problem, with
more storage than a production three-term MINRES implementation.
"""
import numpy as np


def arnoldi_residual_history(apply, rhs, max_steps, tol=1e-12):
    beta = np.linalg.norm(rhs)
    q = rhs / beta
    Q = [q]
    H = np.zeros((max_steps + 1, max_steps), dtype=float)
    history = []
    e1 = np.zeros(max_steps + 1)
    e1[0] = beta
    for j in range(max_steps):
        v = apply(Q[j])
        for _ in range(2):
            for i in range(j + 1):
                hij = np.dot(Q[i], v)
                H[i, j] += hij
                v -= hij * Q[i]
        H[j + 1, j] = np.linalg.norm(v)
        if H[j + 1, j] > 10 * np.finfo(float).eps:
            Q.append(v / H[j + 1, j])
        y, *_ = np.linalg.lstsq(H[: j + 2, : j + 1], e1[: j + 2], rcond=None)
        residual = np.linalg.norm(e1[: j + 2] - H[: j + 2, : j + 1] @ y)
        history.append(residual / beta)
        if residual <= tol * beta:
            break
        if H[j + 1, j] <= 10 * np.finfo(float).eps:
            break
    return np.asarray(history)


def make_matrix(n, gamma):
    A = np.zeros((n, n))
    for j in range(n - 1):
        A[j + 1, j] = 1.0
    A[0, n - 1] = 1.0
    A[n - 1, n - 1] = gamma
    return A


def main():
    gamma = 0.05
    print("n, gmres_iterations_to_1e-8, last_preterminal_residual, lift_iterations_to_1e-8")
    for n in (24, 64, 128):
        A = make_matrix(n, gamma)
        b = np.zeros(n)
        b[0] = 1.0
        gmres = arnoldi_residual_history(lambda x: A @ x, b, n, tol=1e-8)
        # K [u; v] = [A v; A^T u], symmetric and dimension 2n.
        def apply_K(z):
            u, v = z[:n], z[n:]
            return np.concatenate((A @ v, A.T @ u))
        f = np.concatenate((b, np.zeros(n)))
        lifted = arnoldi_residual_history(apply_K, f, min(2 * n, 40), tol=1e-8)
        print(f"{n}, {len(gmres)}, {gmres[-2] if len(gmres) > 1 else float('nan'):.3e}, {len(lifted)}")
        assert np.allclose(gmres[: n - 1], 1.0, atol=1e-12, rtol=0.0)
        assert lifted[-1] < 1e-8


if __name__ == "__main__":
    main()
