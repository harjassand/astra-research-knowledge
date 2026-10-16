"""Local Bernoulli-information audit of the minimal n=3 time grid.

Eleven coordinates: six log transition rates, three log effective losses,
and two logits for the initially unknown state distribution.
"""

import numpy as np


N = 3
H = .2
ELL = .2
EDGES = [(i, j) for j in range(N) for i in range(N) if i != j]


def expm(B):
    values, vectors = np.linalg.eig(B)
    return np.real_if_close(vectors @ np.diag(np.exp(values))
                            @ np.linalg.inv(vectors)).real


def observations(z):
    rates = np.exp(z[:6])
    losses = np.exp(z[6:9])
    raw_b = np.exp(np.r_[z[9:11], 0.])
    b = raw_b / raw_b.sum()
    A = np.zeros((N, N))
    for rate, (i, j) in zip(rates, EDGES):
        A[i, j] = rate
        A[j, j] -= rate
    P = expm((A - np.diag(losses)) * H)
    Q = expm(A * ELL)
    c = np.ones(N)
    one = [c @ np.linalg.matrix_power(P, k) @ b
           for k in range(1, 2*N)]
    echo = [c @ np.linalg.matrix_power(P, i) @ Q
            @ np.linalg.matrix_power(P, j) @ b
            for i in range(1, N) for j in range(N)]
    return np.array(one + echo)


def main():
    A = np.array([[-3., 1., 2.], [2., -5., 1.], [1., 4., -3.]])
    b = np.array([.5, .3, .2])
    z = np.r_[np.log([A[i, j] for i, j in EDGES]),
              np.log([2., 3., 5.]), np.log(b[:2] / b[2])]
    y = observations(z)
    step = 1e-4
    J = np.empty((len(y), len(z)))
    for k in range(len(z)):
        delta = np.zeros(len(z))
        delta[k] = step
        J[:, k] = (observations(z + delta)
                   - observations(z - delta)) / (2 * step)
    weighted = J / np.sqrt(y * (1-y))[:, None]
    singular = np.linalg.svd(weighted, compute_uv=False)
    print("settings:", len(y))
    print("per-setting Bernoulli weighted min sensitivity:", singular[-1])
    print("weighted condition:", singular[0] / singular[-1])
    print("independent outcomes per setting for 0.1 local 1-sigma"
          " along weakest log-parameter direction:",
          1 / (.1 * singular[-1])**2)


if __name__ == "__main__":
    main()
