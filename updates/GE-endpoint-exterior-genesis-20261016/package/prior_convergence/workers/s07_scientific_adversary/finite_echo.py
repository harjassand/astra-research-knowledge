"""Finite positive-duration pulse-grid replay; no derivatives are estimated."""

import numpy as np


def matrix_function(A, scalar_function):
    values, vectors = np.linalg.eig(A)
    output = vectors @ np.diag(scalar_function(values)) @ np.linalg.inv(vectors)
    return np.real_if_close(output, tol=10000).real


def run(delta, tau):
    A = np.array([[-3., 1., 2.], [2., -5., 1.], [1., 4., -3.]])
    D = np.diag([2., 3., 5.])
    b = np.array([1., 0., 0.])
    c = np.ones(3)
    n = len(b)
    P = matrix_function((A-D)*delta, np.exp)
    Q = matrix_function(A*tau, np.exp)
    P2 = matrix_function((A-D)*(delta*np.sqrt(2)), np.exp)
    Q2 = matrix_function(A*(tau*np.sqrt(3)), np.exp)
    moments = np.array([c @ np.linalg.matrix_power(P, k) @ b
                        for k in range(2*n)])
    H = np.array([[moments[i+j] for j in range(n)] for i in range(n)])
    Hshift = np.array([[moments[i+j+1] for j in range(n)] for i in range(n)])
    K = np.array([[c @ np.linalg.matrix_power(P, i) @ Q
                   @ np.linalg.matrix_power(P, j) @ b
                   for j in range(n)] for i in range(n)])
    Hshift2 = np.array([[c @ np.linalg.matrix_power(P, i) @ P2
                         @ np.linalg.matrix_power(P, j) @ b
                         for j in range(n)] for i in range(n)])
    K2 = np.array([[c @ np.linalg.matrix_power(P, i) @ Q2
                    @ np.linalg.matrix_power(P, j) @ b
                    for j in range(n)] for i in range(n)])
    Ph = np.linalg.solve(H, Hshift)
    Qh = np.linalg.solve(H, K)
    P2h = np.linalg.solve(H, Hshift2)
    Q2h = np.linalg.solve(H, K2)
    C = np.column_stack([np.linalg.matrix_power(P, j) @ b for j in range(n)])
    pair_errors = (np.linalg.norm(P2h - np.linalg.solve(C, P2 @ C)),
                   np.linalg.norm(Q2h - np.linalg.solve(C, Q2 @ C)))
    Mh = matrix_function(Ph, np.log) / delta
    Ah = matrix_function(Qh, np.log) / tau
    Dh = Ah-Mh
    eigenvalues, E = np.linalg.eig(Dh)
    order = np.argsort(eigenvalues.real)
    E = np.real_if_close(E[:, order]).real
    ch = moments[:n]
    E = E / (ch @ E)
    recovered_A = np.linalg.solve(E, Ah @ E)
    recovered_D = np.linalg.solve(E, Dh @ E)
    recovered_b = np.linalg.solve(E, np.linalg.solve(H, moments[:n]))
    errors = (np.linalg.norm(recovered_A-A),
              np.linalg.norm(recovered_D-D),
              np.linalg.norm(recovered_b-b))
    return np.linalg.cond(H), errors, pair_errors


if __name__ == '__main__':
    for delta, tau in ((0.25, 0.4), (0.05, 0.05), (0.5, 0.5)):
        condition, errors, pair_errors = run(delta, tau)
        print('delta,tau=', delta, tau, 'cond(H)=', condition,
              'absolute errors (A,D,b)=', errors,
              'second-grid same-basis errors=', pair_errors)
        assert all(err < 1e-4 for err in errors)
        assert all(err < 1e-8 for err in pair_errors)
