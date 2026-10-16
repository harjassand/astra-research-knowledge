"""Local same-information precision check on 180 two-pulse schedules, n=3.

It is a fixed, unoptimized rich timing grid, not a global design bound.
Eleven unknowns include six transition rates, three loss rates, and two
initial-mixture logits. All observations are Bernoulli total-survival counts.
"""

import numpy as np


A_TRUE = np.array([[-3., 1., 2.], [2., -5., 1.], [1., 4., -3.]])
B_TRUE = np.array([.5, .3, .2])
EDGES = [(i, j) for j in range(3) for i in range(3) if i != j]
DARK = (.03, .1, .3, .7, 1.5)


def expm(B, t):
    values, vectors = np.linalg.eig(B)
    return np.real_if_close(vectors @ np.diag(np.exp(values*t))
                            @ np.linalg.inv(vectors)).real


def observations(z, on_times):
    rates = np.exp(z[:6])
    losses = np.exp(z[6:9])
    if len(z) == 9:
        b = np.array([1., 0., 0.])  # Separately supplied pure-state prep.
    else:
        raw_b = np.exp(np.r_[z[9:11], 0.])
        b = raw_b / raw_b.sum()
    A = np.zeros((3, 3))
    for rate, (i, j) in zip(rates, EDGES):
        A[i, j] = rate
        A[j, j] -= rate
    M = A - np.diag(losses)
    p = {t: expm(M, t) for t in on_times}
    q = {t: expm(A, t) for t in DARK}
    c = np.ones(3)
    return np.array([c @ p[t2] @ q[tau] @ p[t1] @ b
                     for t1 in on_times for tau in DARK for t2 in on_times])


def audit(losses, on_times, pure_prep=False):
    z = np.r_[np.log([A_TRUE[i, j] for i, j in EDGES]),
              np.log(losses)]
    if not pure_prep:
        z = np.r_[z, np.log(B_TRUE[:2] / B_TRUE[2])]
    y = observations(z, on_times)
    h = 1e-4
    J = np.empty((len(y), len(z)))
    for k in range(len(z)):
        delta = np.zeros(len(z))
        delta[k] = h
        J[:, k] = (observations(z + delta, on_times)
                   - observations(z - delta, on_times)) / (2*h)
    WJ = J / np.sqrt(y * (1-y))[:, None]
    singular = np.linalg.svd(WJ, compute_uv=False)
    cov_10k = np.linalg.inv(WJ.T @ WJ * 10000)
    print("losses:", losses, "pure prep:", pure_prep,
          "settings:", len(y))
    print("  survival range:", (float(y.min()), float(y.max())))
    print("  min weighted singular:", singular[-1])
    print("  weighted condition:", singular[0] / singular[-1])
    print("  outcomes/setting for 0.1 local sigma, weak direction:",
          1 / (.1 * singular[-1])**2)
    print("  max marginal local sigma at 10000/setting:",
          np.max(np.sqrt(np.diag(cov_10k))))


if __name__ == "__main__":
    audit((2., 3., 5.), (.03, .08, .15, .3, .5, .8))
    audit((.2, 3., 15.), (.005, .02, .05, .1, .2, .4))
    audit((.2, 3., 15.), (.005, .02, .05, .1, .2, .4), pure_prep=True)
