#!/usr/bin/env python3
"""Scalar-only control-map acquisition. Synthetic checks, not apparatus data.

The estimator sees only (u, scalar_response) queries, never the plant matrix.
Run: python3 check_scalar_acquisition.py
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np


def response(f0, a, H, u):
    u = np.asarray(u)
    z = np.linalg.solve(np.eye(len(u)) + H * u[None, :], np.ones(len(u)))
    return f0 - np.dot(a * u, z)


class ScalarOracle:
    def __init__(self, f0, a, H, noise=0.0, seed=0):
        self.f0, self.a, self.H = f0, a, H
        self.noise = noise
        self.rng = np.random.default_rng(seed)
        self.records = []

    def __call__(self, u):
        value = float(response(self.f0, self.a, self.H, u))
        measured = value + self.noise * self.rng.normal()
        self.records.append((np.asarray(u).copy(), measured))
        return measured


def acquire(m, oracle, t1=0.5, t2=1.5, t3=1.0):
    """Fixed-anchor algorithm. Rejects no data silently; reports nonreal pairs."""
    zero = np.zeros(m)
    f0 = oracle(zero)
    a = np.zeros(m, dtype=complex)
    H = np.zeros((m, m), dtype=complex)
    pair = {}
    nonreal = 0
    margins = []
    for i in range(m):
        deltas = []
        for t in (t1, t2):
            u = zero.copy(); u[i] = t
            deltas.append(f0 - oracle(u))
        d1, d2 = deltas
        H[i, i] = (d2 / t2 - d1 / t1) / (d1 - d2)
        a[i] = d1 * (1 + H[i, i] * t1) / t1
    for i, j in itertools.combinations(range(m), 2):
        ds, rs = [], []
        for t in (t1, t2):
            u = zero.copy(); u[i] = u[j] = t
            delta = f0 - oracle(u)
            den0 = (1 + H[i, i] * t) * (1 + H[j, j] * t)
            num0 = (a[i] + a[j]) * t + (a[i] * H[j, j] + a[j] * H[i, i]) * t*t
            ds.append(delta); rs.append((num0 - delta * den0) / (t*t))
        p = (rs[1] - rs[0]) / (ds[0] - ds[1])
        q = rs[0] + ds[0] * p
        roots = np.roots([a[i], -q, a[j] * p])
        choices = [(x, (q - a[i] * x) / a[j]) for x in roots]
        if max(abs(x.imag) + abs(y.imag) for x, y in choices) > 1e-7:
            nonreal += 1
        pair[i, j] = choices

    def setpair(K, i, j, choice):
        K[i, j], K[j, i] = choice

    def probe_triangle(indices, candidates):
        idx = np.array(indices)
        u = zero.copy(); u[idx] = t3
        observed = oracle(u)
        preds = [response(f0, a[idx], K[np.ix_(idx, idx)], np.full(3, t3)) for K in candidates]
        residuals = [abs(p - observed) for p in preds]
        order = np.argsort(residuals)
        margins.append(float(abs(preds[order[1]] - preds[order[0]])))
        return candidates[order[0]]

    if m >= 2:
        setpair(H, 0, 1, pair[0, 1][0])
    for k in range(2, m):
        candidates = []
        for ci, cj in itertools.product(range(2), repeat=2):
            K = H.copy()
            setpair(K, 0, k, pair[0, k][ci])
            setpair(K, 1, k, pair[1, k][cj])
            candidates.append(K)
        H = probe_triangle((0, 1, k), candidates)
    for i, j in itertools.combinations(range(2, m), 2):
        candidates = []
        for choice in pair[i, j]:
            K = H.copy(); setpair(K, i, j, choice); candidates.append(K)
        H = probe_triangle((0, i, j), candidates)
    return f0, a, H, {"queries": len(oracle.records), "nonreal_pairs": nonreal,
                       "minimum_triangle_candidate_separation": min(margins) if margins else None}


def dissipative_plant(m, seed):
    """A real strictly dissipative one-port plant, n=m+1 hidden/observed states.

    Build its inverse G. The estimator receives only a scalar one-port oracle.
    Full symmetric part of G is positive definite, hence so is that of A=G^-1.
    The hidden block is dense and nonreciprocal.
    """
    rng = np.random.default_rng(seed)
    H = 2 * np.eye(m) + rng.normal(size=(m, m)) * 0.30 / np.sqrt(m)
    np.fill_diagonal(H, 2 + rng.uniform(-0.2, 0.2, m))
    w = rng.uniform(1.0, 2.0, m) / np.sqrt(m)
    v = rng.uniform(1.0, 2.0, m) / np.sqrt(m)
    f0 = 4.0
    G = np.block([[np.array([[f0]]), v[None, :]], [w[:, None], H]])
    minimum = np.linalg.eigvalsh((G + G.T) / 2).min()
    if minimum <= 0:
        raise RuntimeError("generated plant not dissipative")
    # Diagonal gauge w -> 1; a_i = v_i*w_i.
    Hg = H * w[None, :] / w[:, None]
    return f0, v*w, Hg, {"min_symmetric_inverse_eigenvalue": float(minimum),
                          "plant_condition_number": float(np.linalg.cond(G))}


def run_trials():
    results = []
    for m in (3, 8, 16, 32):
        for noise in (0.0, 1e-10, 1e-8, 1e-6, 1e-4):
            errs, relative_changes, nonreal, margins, ranking = [], [], [], [], []
            for seed in range(8):
                f0, a, H, physical = dissipative_plant(m, seed)
                oracle = ScalarOracle(f0, a, H, noise, 1000 + seed)
                fh, ah, Hh, info = acquire(m, oracle)
                rng = np.random.default_rng(10000 + seed)
                us = rng.uniform(0, 2, (100, m))
                truth = np.array([response(f0, a, H, u) for u in us])
                pred = np.array([response(fh, ah, Hh, u) for u in us])
                errs.append(float(np.sqrt(np.mean(abs(pred-truth)**2))))
                relative_changes.append(float(np.linalg.norm(pred-truth) / np.linalg.norm(truth-f0)))
                nonreal.append(info["nonreal_pairs"])
                if info["minimum_triangle_candidate_separation"] is not None:
                    margins.append(info["minimum_triangle_candidate_separation"])
                tdiff = truth[:50] - truth[50:]
                pdiff = pred[:50].real - pred[50:].real
                ranking.append(float(np.mean(tdiff * pdiff > 0)))
            results.append({"m": m, "absolute_response_noise_sd": noise,
                "queries_per_run": info["queries"],
                "expected_queries": (3*m*m-m+4)//2,
                "runs": 8, "heldout_configurations_per_run": 100,
                "median_heldout_rms_absolute_error": float(np.median(errs)),
                "maximum_heldout_rms_absolute_error": float(np.max(errs)),
                "median_error_relative_to_control_induced_response": float(np.median(relative_changes)),
                "median_pairwise_prediction_order_accuracy": float(np.median(ranking)),
                "total_nonreal_pair_estimates": int(sum(nonreal)),
                "median_minimum_triangle_separation": float(np.median(margins))})
    return results


def exact_counterexamples():
    import sympy as s
    a = s.Matrix([1, 2, 3])
    H = s.Matrix([[10, s.Rational(1,5), s.Rational(1,2)],
                  [s.Rational(3,10), 10, s.Rational(11,10)],
                  [s.Rational(7,10), s.Rational(13,10), 10]])
    K = H.copy()
    K[0,2], K[2,0] = 3*H[2,0], H[0,2]/3
    def exact(M, u):
        D = s.diag(*u)
        return s.Integer(10) - (a.T * D * (s.eye(3)+M*D).inv() * s.ones(3,1))[0]
    u1,u2,u3 = s.symbols("u1 u2 u3")
    pair_equal = []
    for i,j in itertools.combinations(range(3), 2):
        u=[0,0,0]; u[i]=u1; u[j]=u2
        pair_equal.append(s.cancel(exact(H,u)-exact(K,u)) == 0)
    full_values = [exact(M,[1,1,1]) for M in (H,K)]
    generic_values=[]
    for bits in itertools.product([0,1], repeat=2):
        M=H.copy()
        for bit,(i,j) in zip(bits, [(0,2),(1,2)]):
            if bit: M[i,j],M[j,i]=a[j]/a[i]*M[j,i],a[i]/a[j]*M[i,j]
        generic_values.append(exact(M,[1,1,1]))
    # A fixed-anchor schedule never probes 3 interior nodes at once.
    # At epsilon=0, anchors 0,1 are disconnected in H from interior 2,3,4.
    # Every scheduled datum is identical; the interior triple still differs.
    weak=[]
    for eps in (0.0,1e-6,1e-4,1e-2):
        H5=np.zeros((5,5)); K5=np.zeros((5,5))
        H5[:2,:2]=np.array([[10,.2],[.3,10]])
        K5[:2,:2]=H5[:2,:2]
        H5[2:,2:]=np.array(H,float); K5[2:,2:]=np.array(K,float)
        for i in range(2):
            for j in range(2,5):
                H5[i,j]=K5[i,j]=eps*(1+i+j)
                H5[j,i]=K5[j,i]=eps*(2+2*i+j)
        a5=np.array([1.,2.,1.,2.,3.])
        o=ScalarOracle(10.,a5,H5)
        acquire(5,o)
        differences=[abs(response(10.,a5,H5,u)-response(10.,a5,K5,u)) for u,y in o.records]
        future=np.array([0.,0.,1.,1.,1.])
        weak.append({"epsilon":eps,"maximum_difference_on_all_scheduled_queries":float(max(differences)),
                     "difference_on_unqueried_interior_triple":float(abs(response(10.,a5,H5,future)-response(10.,a5,K5,future)))})
    return {"single_and_pair_response_functions_identical":all(pair_equal),
            "triple_responses_exact":list(map(str,full_values)),
            "triple_response_difference_exact":str(full_values[0]-full_values[1]),
            "four_anchor_orientation_predictions_exact":list(map(str,generic_values)),
            "four_anchor_orientation_predictions_distinct":len(set(generic_values))==4,
            "weak_anchor_counterexample":weak}


def direct_plant_check():
    m=12
    f0,a,H,physical=dissipative_plant(m,43)
    G=np.block([[np.array([[f0]]),a[None,:]],[np.ones((m,1)),H]])
    # This diagonal gauge need not preserve a Euclidean dissipation metric;
    # physical dissipativity was checked before gauge normalization above.
    A=np.linalg.inv(G); b=np.eye(m+1)[0]
    rng=np.random.default_rng(44)
    errors=[]
    for _ in range(50):
        u=rng.uniform(0,2,m)
        loaded=A+np.diag(np.r_[0.,u])
        errors.append(abs(np.linalg.solve(loaded,b)[0]-response(f0,a,H,u)))
    return {"maximum_direct_loaded_plant_error":float(max(errors)),**physical}


if __name__ == "__main__":
    output={"status":"synthetic_mathematical_check_only",
            "direct_plant":direct_plant_check(),
            "exact_counterexamples":exact_counterexamples(),
            "noise_trials":run_trials()}
    path=Path(__file__).with_name("scalar_acquisition_results.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
