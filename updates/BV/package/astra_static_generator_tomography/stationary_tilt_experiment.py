"""Independent Astra research probe: finite-intervention stationary-tilt tomography.

Exact i.i.d. rejection sampling from nonlinear quartic equilibria, discriminative
ratio learning (logistic regression), and a Gaussian-moment linear-response baseline.
All observations are labelled stationary positions; no trajectories or gradients.

Requires numpy scipy scikit-learn. Run:
    python stationary_tilt_experiment.py --reps 12 --sizes 500 2000 8000
"""
from __future__ import annotations
import argparse
import json
import time
import warnings
import numpy as np
from sklearn.linear_model import LogisticRegression

H = np.array([[1.5, 0.35, -0.1], [0.35, 1.8, 0.25], [-0.1, 0.25, 1.2]], dtype=float)
QUARTIC = 0.35
D = np.array([[0.6, 0.08, -0.04], [0.08, 0.7, 0.07], [-0.04, 0.07, 0.5]], dtype=float)
K = np.array([[0, -0.45, 0.2], [0.45, 0, -0.3], [-0.2, 0.3, 0]], dtype=float)
B = D + K
DIM = len(D)
FORCE = 0.9
U = FORCE * np.eye(DIM)
A_TRUE = np.linalg.solve(B, U)
COV_GAUSS = np.linalg.inv(H)
CHOLESKY = np.linalg.cholesky(COV_GAUSS)


def sample_exact(n: int, a: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, int]:
    """Exact independent proposals Gaussian N(H^-1 a,H^-1); quartic accept-reject.

    Acceptance weight exp(-lambda/4 * sum(x^4)) <= 1; the accepted law is
    p_a(x) proportional to exp(-x H x/2 -lambda sum(x^4)/4 + a x).
    """
    mean = COV_GAUSS @ a
    result = np.empty((n, DIM))
    count = 0
    attempts = 0
    while count < n:
        batch = max(128, int((n-count)*1.4))
        x = mean + rng.normal(size=(batch, DIM)) @ CHOLESKY.T
        lweight = -(QUARTIC/4) * np.sum(x**4, axis=1)
        take = np.log(rng.random(batch)) < lweight
        accepted = x[take]
        k = min(len(accepted), n-count)
        result[count:count+k] = accepted[:k]
        count += k
        attempts += batch
    return result, attempts


def estimate_ratio(x0: np.ndarray, x1: np.ndarray) -> np.ndarray:
    x = np.vstack((x0, x1))
    y = np.concatenate((np.zeros(len(x0)), np.ones(len(x1))))
    model = LogisticRegression(C=np.inf, fit_intercept=True, solver="lbfgs", max_iter=450,
                               tol=1e-9)
    # scikit-learn >=1.8 emits a benign warning when infinite C requests
    # an unpenalized logistic fit; retain the exact estimator and silence
    # only that known warning. All other warnings still surface.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Setting penalty=None will ignore the C and l1_ratio parameters", category=UserWarning)
        model.fit(x, y)
    return model.coef_.ravel()


def run_once(n: int, rng: np.random.Generator) -> dict:
    t0 = time.perf_counter()
    x0, calls = sample_exact(n, np.zeros(DIM), rng)
    A_hat = np.empty((DIM, DIM))
    C0 = np.cov(x0.T)
    m0 = x0.mean(axis=0)
    A_moment = np.empty_like(A_hat)
    for i in range(DIM):
        xi, work = sample_exact(n, A_TRUE[:, i], rng)
        calls += work
        A_hat[:, i] = estimate_ratio(x0, xi)
        A_moment[:, i] = np.linalg.solve(C0, xi.mean(axis=0) - m0)
    fit_time = time.perf_counter() - t0
    try:
        B_hat = U @ np.linalg.inv(A_hat)
        B_mom = U @ np.linalg.inv(A_moment)
    except np.linalg.LinAlgError:
        return {"failed": True}
    D_hat = (B_hat + B_hat.T)/2
    K_hat = (B_hat - B_hat.T)/2
    D_mom = (B_mom + B_mom.T)/2
    # Measure recovery of the actual noise, circulation, and total generator mobility.
    # Estimating the potential/score is a separate problem (not silently included here).
    return {
        "failed": False,
        "n_per_condition": n,
        "stationary_samples": (DIM+1)*n,
        "proposals": calls,
        "acceptance_efficiency": (DIM+1)*n / calls,
        "seconds_sampling_and_fitting": fit_time,
        "matrix_rel_error": np.linalg.norm(B_hat-B, 'fro')/np.linalg.norm(B,'fro'),
        "D_rel_error": np.linalg.norm(D_hat-D,'fro')/np.linalg.norm(D,'fro'),
        "K_rel_error": np.linalg.norm(K_hat-K,'fro')/np.linalg.norm(K,'fro'),
        "moment_D_rel_error": np.linalg.norm(D_mom-D,'fro')/np.linalg.norm(D,'fro'),
        "moment_matrix_rel_error": np.linalg.norm(B_mom-B,'fro')/np.linalg.norm(B,'fro'),
        "D_positive": bool(np.linalg.eigvalsh(D_hat).min() > 0),
        "ratio_matrix_rel_error": np.linalg.norm(A_hat-A_TRUE,'fro')/np.linalg.norm(A_TRUE,'fro'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sizes', type=int, nargs='+', default=[500, 2000, 8000])
    ap.add_argument('--reps', type=int, default=12)
    ap.add_argument('--seed', type=int, default=25016)
    ap.add_argument('--output', default='results.json')
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    summary = {
        "seed": args.seed, "reps": args.reps, "sizes": args.sizes,
        "model": {"dim": DIM,"D": D.tolist(), "K": K.tolist(), "B": B.tolist(),
                  "quartic_coefficient": QUARTIC, "quadratic": H.tolist(),
                  "forcing": U.tolist(), "true_log_ratio_slopes": A_TRUE.tolist(),
                  "condition_A": float(np.linalg.cond(A_TRUE))},
        "rows":[], "aggregate": [],
    }
    for n in args.sizes:
        rows = []
        for r in range(args.reps):
            row = run_once(n, rng)
            row['rep'] = r
            summary['rows'].append(row)
            if not row['failed']:
                rows.append(row)
        aggregate = {"n_per_condition": n, "successes":len(rows)}
        for key in ['matrix_rel_error','D_rel_error','K_rel_error',
                    'moment_matrix_rel_error','moment_D_rel_error',
                    'acceptance_efficiency','seconds_sampling_and_fitting','proposals']:
            vals = np.array([v[key] for v in rows])
            aggregate[key+'_mean'] = float(vals.mean())
            aggregate[key+'_std'] = float(vals.std(ddof=1)) if len(vals) > 1 else 0.
            aggregate[key+'_median'] = float(np.median(vals))
        summary['aggregate'].append(aggregate)
        print(json.dumps(aggregate, indent=2))
    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(summary,f,indent=2)
    print('Saved',args.output)

if __name__=='__main__':
    main()
