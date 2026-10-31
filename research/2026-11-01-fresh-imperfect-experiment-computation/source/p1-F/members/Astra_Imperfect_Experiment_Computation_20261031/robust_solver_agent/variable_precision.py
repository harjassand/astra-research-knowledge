"""Variable-precision acquisition of a reusable one-mode resolvent.

This experiment is a numerical illustration, not an interval proof.
The source is a full-rank symmetric matrix represented as an unknown
rank-one mode plus a generic fixed tail.  The learner only receives
source products at requested error tolerances.  Errors are adversarially
directed to reduce the top-mode overlap and increase the tail component.

Run: python3 variable_precision.py --output results.json
"""

from __future__ import annotations
import argparse
import json
import math
import numpy as np


class Source:
    def __init__(self, n, eps, seed):
        self.n, self.eps = n, eps
        rng = np.random.default_rng(seed)
        self.u = rng.normal(size=n)
        self.u /= np.linalg.norm(self.u)
        self.lam = 1.4
        self.beta = eps / 8
        # P diag(d) P is generically full rank on u^perp, with norm <= beta.
        self.diag = rng.uniform(-self.beta, self.beta, n)
        self.work = 0.0
        self.calls = 0
        self.tolerances = []
        self.trace = []

    def exact(self, v):
        tail = v - self.u * (self.u @ v)
        tail = self.diag * tail
        tail -= self.u * (self.u @ tail)
        return self.lam * self.u * (self.u @ v) + tail

    def noisy(self, v, tau, phase):
        self.work += tau ** -2
        self.calls += 1
        self.tolerances.append(tau)
        a = self.u @ v
        tail = v - self.u * a
        tailnorm = np.linalg.norm(tail)
        if tailnorm <= 1e-15:
            tail = np.roll(self.u, 1)
            tail -= self.u * (self.u @ tail)
            tailnorm = np.linalg.norm(tail)
        tail /= tailnorm
        # Total error norm is exactly tau*||v|| (up to rounding).
        error = (-math.copysign(1.0, a) * self.u + tail) / math.sqrt(2)
        error *= tau * np.linalg.norm(v)
        out = self.exact(v) + error
        self.trace.append({"phase": phase, "tau": float(tau),
                           "sin_angle_before": float(math.sqrt(max(0.0, 1-a*a)))})
        return out


def acquire(source, eps, seed=20, delta=0.01, fixed_precision=False):
    rng = np.random.default_rng(seed)
    n = source.n
    alpha, beta_bound = 1 / 32, 1 / 4
    max_attempts = math.ceil(math.log(delta) / math.log(13 / 16))
    q = None
    attempts = 0
    # Strong fixed-precision baseline: the minimum tolerance required anywhere
    # by this schedule.  Standard noisy-power conditions use the minimum of
    # discovery and final accuracy; they do not require their product.
    fixed_tau = min(alpha / math.sqrt(1+4*n), 1/128, eps)
    planned_T = 2.0
    while planned_T > eps/8:
        fixed_tau = min(fixed_tau, planned_T / (16*math.sqrt(1+planned_T**2)))
        planned_T /= 2
    def call(v, tau, phase):
        return source.noisy(v, fixed_tau if fixed_precision else tau, phase)
    for attempt in range(max_attempts):
        attempts += 1
        v = rng.normal(size=n)
        v /= np.linalg.norm(v)
        T = 2 * math.sqrt(n)
        while T > 1 / 8:
            tau = alpha / math.sqrt(1 + T*T)
            y = call(v, tau, "discovery")
            norm_y = np.linalg.norm(y)
            if norm_y <= 1e-100:
                break
            v = y / norm_y
            T = (beta_bound*T + alpha) / (1-alpha)
        score = float(v @ call(v, 1/128, "test"))
        if score >= 3/4:
            q = v
            break
    if q is None:
        return {"success": False, "calls": source.calls, "work": source.work}
    T = 2.0
    while T > eps/8:
        tau = T / (16 * math.sqrt(1+T*T))
        y = call(q, tau, "refine")
        q = y / np.linalg.norm(y)
        T /= 2
    lamhat = float(np.clip(q @ call(q, eps, "eigenvalue"), 1, 2))
    angle = math.sqrt(max(0.0, 1-(q@source.u)**2))
    # A rigorous expression from the proof; uses class constants.
    lamerr_bound = eps + (9/4)*(eps/8)**2
    inverse_bound = (4/3)*source.beta + (2/3)*(eps/8) + lamerr_bound/4
    # Direct spectral-norm check at mu=1 on moderate dimensions.
    eye = np.eye(n)
    B = np.column_stack([source.exact(eye[:,i]) for i in range(n)])
    true_inv = np.linalg.inv(eye+B)
    learned_inv = eye-(lamhat/(1+lamhat))*np.outer(q,q)
    actual_op_error = np.linalg.norm(true_inv-learned_inv,ord=2)
    return {"success": True, "n": n, "epsilon": eps,
            "attempts": attempts, "calls": source.calls,
            "precision_work": source.work,
            "minimum_tolerance": min(source.tolerances),
            "top_mode_angle": angle, "lambda_error": abs(lamhat-source.lam),
            "actual_inverse_error_mu_1": float(actual_op_error),
            "theorem_inverse_bound": float(inverse_bound),
            "finite_check_pass": bool(actual_op_error <= inverse_bound),
            "source_tail_bound": source.beta,
            "fixed_precision": fixed_precision,
            "source_tolerances": source.tolerances}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="results.json")
    args=parser.parse_args()
    results=[]
    for n,eps in [(64,.1),(128,.1),(256,.1),(128,.03),(128,.01)]:
        for fixed in [False,True]:
            source=Source(n,eps,seed=100+n)
            result=acquire(source,eps,seed=20+n,fixed_precision=fixed)
            results.append(result)
            print(json.dumps({k:v for k,v in result.items() if k!="source_tolerances"}))
    with open(args.output,"w") as f:
        json.dump({"description":"Numerical illustration; class promise is supplied, directions are acquired.",
                   "results":results},f,indent=2)
    assert all(r["success"] and r["finite_check_pass"] for r in results)


if __name__=="__main__":
    main()
