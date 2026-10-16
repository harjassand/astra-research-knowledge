"""Noiseless finite-time sampled loss-echo reconstruction, n=3.

Uses an eigendecomposition implementation of exp/log valid for this fixture.
The general finite-time theorem requires a nonaliasing spectral strip.
"""

import numpy as np


def matrix_function(B, scalar_function):
    values, vectors = np.linalg.eig(B)
    result = vectors @ np.diag(scalar_function(values)) @ np.linalg.inv(vectors)
    return np.real_if_close(result).real


def main():
    A = np.array([[-3., 1., 2.], [2., -5., 1.], [1., 4., -3.]])
    D = np.diag([2., 3., 5.])
    b = np.array([1., 0., 0.])
    c = np.ones(3)
    h = .2
    ell = .2
    P = matrix_function((A - D) * h, np.exp)
    Q = matrix_function(A * ell, np.exp)
    n = 3

    v = np.array([c @ np.linalg.matrix_power(P, k) @ b
                  for k in range(2*n)])
    H = np.array([[v[i+j] for j in range(n)] for i in range(n)])
    HP = np.array([[v[i+j+1] for j in range(n)] for i in range(n)])
    K = np.array([[c @ np.linalg.matrix_power(P, i) @ Q
                   @ np.linalg.matrix_power(P, j) @ b
                   for j in range(n)] for i in range(n)])
    assert np.allclose(K[0, :], v[:n])  # Dark interval alone is invisible.

    Ph = np.linalg.solve(H, HP)
    Qh = np.linalg.solve(H, K)
    Mh = matrix_function(Ph, np.log) / h
    Ah = matrix_function(Qh, np.log) / ell
    Dh = Ah - Mh

    C = np.column_stack([np.linalg.matrix_power(P, j) @ b
                         for j in range(n)])
    ch = c @ C
    bh = np.linalg.solve(H, v[:n])
    eigvals, eigvecs = np.linalg.eig(Dh)
    order = np.argsort(eigvals.real)
    E = eigvecs[:, order]
    E = E / (ch @ E)[None, :]
    Ar = np.linalg.inv(E) @ Ah @ E
    Dr = np.linalg.inv(E) @ Dh @ E
    br = np.linalg.inv(E) @ bh
    assert np.max(np.abs(Ar - A)) < 1e-8
    assert np.max(np.abs(Dr - D)) < 1e-8
    assert np.max(np.abs(br - b)) < 1e-8
    print("one-pulse nonzero time settings:", 2*n-1)
    print("new two-pulse time settings:", n*(n-1))
    print("H condition:", np.linalg.cond(H))
    print("maximum A,D,b absolute error:",
          max(np.max(np.abs(Ar-A)), np.max(np.abs(Dr-D)),
              np.max(np.abs(br-b))))


if __name__ == "__main__":
    main()
