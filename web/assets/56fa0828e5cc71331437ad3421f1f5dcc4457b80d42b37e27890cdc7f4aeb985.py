"""Finite precision Choi-rank diagnostic for transverse-noise sensing channel.

This is a numerical cross-check of the trajectory-span proof in REPORT.md,
not a proof of full rank or a verification of the cited papers.
"""
import mpmath as mp


def kron(a, b):
    out = mp.matrix(a.rows * b.rows, a.cols * b.cols)
    for i in range(a.rows):
        for j in range(a.cols):
            for k in range(b.rows):
                for ell in range(b.cols):
                    out[i * b.rows + k, j * b.cols + ell] = a[i, j] * b[k, ell]
    return out


def channel_choi(omega, gamma, tau, dps=70):
    mp.mp.dps = dps
    I = mp.eye(2)
    X = mp.matrix([[0, 1], [1, 0]])
    Z = mp.matrix([[1, 0], [0, -1]])
    eye4 = mp.eye(4)
    # vec(A rho B) = (B^T kron A) vec(rho), column-major convention.
    L = (-1j * omega) * (kron(I, Z) - kron(Z.T, I))
    L += gamma * (kron(X.T, X) - eye4)
    S = mp.expm(tau * L)

    J = mp.matrix(4, 4)
    for i in range(2):
        for j in range(2):
            # vec(|i><j|) has its one at row i + 2*j.
            e = mp.matrix(4, 1)
            e[i + 2 * j] = 1
            outvec = S * e
            out = mp.matrix(2, 2)
            for k in range(2):
                for ell in range(2):
                    out[k, ell] = outvec[k + 2 * ell]
            for k in range(2):
                for ell in range(2):
                    J[2 * i + k, 2 * j + ell] = out[k, ell]
    J = (J + J.H) / 2
    return J


if __name__ == "__main__":
    mp.mp.dps = 80
    gamma, tau = mp.mpf("0.1"), mp.mpf("0.1")
    for omega in (mp.mpf("3"), mp.mpf("0.1"), mp.mpf("0")):
        J = channel_choi(omega, gamma, tau)
        # Realification of a Hermitian matrix duplicates each eigenvalue.
        R = mp.matrix(8, 8)
        for i in range(4):
            for j in range(4):
                R[i, j] = mp.re(J[i, j])
                R[i, j + 4] = -mp.im(J[i, j])
                R[i + 4, j] = mp.im(J[i, j])
                R[i + 4, j + 4] = mp.re(J[i, j])
        vals = mp.eigsy(R, eigvals_only=True)
        vals = vals[::2]
        print(f"omega={omega}, gamma={gamma}, tau={tau}")
        print("normalized-Choi eigenvalues:")
        print(" ".join(mp.nstr(x / 2, 15) for x in vals))
