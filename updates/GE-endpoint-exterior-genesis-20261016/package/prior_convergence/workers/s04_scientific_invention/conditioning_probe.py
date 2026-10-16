"""Finite-sample conditioning of selective-sink tomography.

The noise is a Gaussian approximation to N independent absorption times per
assay. Its covariance is computed from the exact phase-type Laplace transform.
The matched comparator fits the very same 18 noisy Laplace means, with all
positive rates and sink efficiencies jointly free. It sees no hidden truth.
"""

import argparse
import numpy as np


TRUE_A = np.array([[-3., 3., 1.], [2., -4., 4.], [1., 1., -5.]])
TRUE_K = np.array([2., 3., 5.])
N = 3
S = np.array([1., 2., 3.])
DOSES = (1., 2.)
B = np.array([1., 0., 0.])
EDGES = [(i, j) for j in range(N) for i in range(N) if i != j]


def from_log_parameters(z):
    rates = np.exp(z[:len(EDGES)])
    k = np.exp(z[len(EDGES):])
    a = np.zeros((N, N))
    for rate, (i, j) in zip(rates, EDGES):
        a[i, j] = rate
        a[j, j] -= rate
    return a, k


def phi(a, k, i, u, s):
    sink = np.zeros((N, N))
    sink[i, i] = u * k[i]
    y = np.sum(np.linalg.solve(s * np.eye(N) - a + sink, B))
    return 1. - s * y


def phi_array(a, k):
    return np.array([[[phi(a, k, i, u, s) for s in S]
                      for u in DOSES] for i in range(N)])


def gaussian_laplace_sample(a, k, population, rng):
    obs = np.zeros((N, 2, N))
    for i in range(N):
        for d, u in enumerate(DOSES):
            means = np.array([phi(a, k, i, u, s) for s in S])
            cov = np.array([[phi(a, k, i, u, s + t) - means[j] * means[l]
                             for l, t in enumerate(S)] for j, s in enumerate(S)])
            cov = (cov + cov.T) / 2
            obs[i, d] = rng.multivariate_normal(means, cov / population,
                                                 check_valid="raise")
    return obs


def algebraic_reconstruct(obs):
    u1, u2 = DOSES
    p1, p2 = obs[:, 0, :], obs[:, 1, :]
    f = (u2 - u1) * p1 * p2 / (u1 * u2 * (p2 - p1))
    w = np.linalg.solve(f.T, 1. / S)
    k = 1. / w
    x = w[:, None] * f
    a = (x * S[None, :] - B[:, None]) @ np.linalg.inv(x)
    return a, k, np.linalg.cond(f), np.linalg.cond(x)


def model_vector(z):
    a, k = from_log_parameters(z)
    return phi_array(a, k).ravel()


def joint_fit(obs, starts):
    target = obs.ravel()
    best = None
    for z0 in starts:
        z = z0.copy()
        lam = 1e-3
        for _ in range(90):
            predicted = model_vector(z)
            residual = predicted - target
            loss = residual @ residual
            h = 1e-5
            jac = np.column_stack([(model_vector(z + h * np.eye(len(z))[j]) - predicted) / h
                                   for j in range(len(z))])
            try:
                step = np.linalg.solve(jac.T @ jac + lam * np.eye(len(z)),
                                       -jac.T @ residual)
            except np.linalg.LinAlgError:
                break
            trial = np.clip(z + step, -8, 8)
            tr = model_vector(trial) - target
            trial_loss = tr @ tr
            if trial_loss < loss:
                z = trial
                lam = max(lam / 3, 1e-10)
                if np.linalg.norm(step) < 1e-9:
                    break
            else:
                lam = min(lam * 5, 1e8)
                if lam >= 1e8:
                    break
        final_resid = model_vector(z) - target
        final_loss = final_resid @ final_resid
        if best is None or final_loss < best[0]:
            best = (final_loss, *from_log_parameters(z))
    return best


def errors(a, k):
    return np.linalg.norm(a - TRUE_A) / np.linalg.norm(TRUE_A), \
           np.linalg.norm(k - TRUE_K) / np.linalg.norm(TRUE_K)


def main():
    global TRUE_A, S, DOSES
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("stress", "separated"), default="stress")
    args = parser.parse_args()
    if args.scenario == "separated":
        TRUE_A = np.array([[-3., 1., 2.], [2., -5., 1.], [1., 4., -3.]])
        S = np.array([1., 3., 20.])
        DOSES = (.3, 3.)
    print("scenario:", args.scenario, "frequencies:", S.tolist(), "doses:", DOSES)
    true_obs = phi_array(TRUE_A, TRUE_K)
    a0, k0, cond_f, cond_x = algebraic_reconstruct(true_obs)
    assert np.allclose(a0, TRUE_A, atol=1e-9)
    assert np.allclose(k0, TRUE_K, atol=1e-9)
    print("exact cond(F):", round(cond_f, 2), "cond(X):", round(cond_x, 2))
    print("exact sink dose contrast min(phi_2-phi_1):",
          round(float(np.min(true_obs[:, 1, :] - true_obs[:, 0, :])), 6))

    rng = np.random.default_rng(20261016)
    starts = [np.zeros(9), np.log(np.array([.5, 1., 2., .5, 1., 2., 2., 2., 2.])),
              np.log(np.array([2., 2., .5, 2., 2., .5, 3., 3., 3.]))]
    for population in (10_000, 1_000_000):
        algebraic = []
        joint = []
        physical = 0
        fail = 0
        for rep in range(12):
            obs = gaussian_laplace_sample(TRUE_A, TRUE_K, population, rng)
            try:
                a, k, _, _ = algebraic_reconstruct(obs)
                err = errors(a, k)
                algebraic.append(err)
                physical += int(np.all(k > 0) and
                                all(a[i, j] > 0 for i, j in EDGES))
            except np.linalg.LinAlgError:
                fail += 1
            _, ja, jk = joint_fit(obs, starts)
            joint.append(errors(ja, jk))
        print("N per assay:", population, "replicates:", len(joint))
        print("algebraic med relative errors (A,k):",
              np.round(np.median(algebraic, axis=0), 3),
              "physical fits:", physical, "singular failures:", fail)
        print("matched joint-fit med relative errors (A,k):",
              np.round(np.median(joint, axis=0), 3))


if __name__ == "__main__":
    main()
