#!/usr/bin/env python3
"""Bounded independent checks for PROOFS.md; no physical data or optimizer oracle.

Requires NumPy. Writes only the explicitly requested output file. Fractions check
the two finite coexistence constructions exactly; numerical identities and dual
certificates check stated conditional models, not material validity or novelty.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
import platform

import numpy as np


def sym(a):
    return (a + a.T) / 2


def root(a, inverse=False):
    d, v = np.linalg.eigh(sym(a))
    assert min(d) > 0
    return (v * (1 / np.sqrt(d) if inverse else np.sqrt(d))) @ v.T


def positive_projector(a):
    d, v = np.linalg.eigh(sym(a))
    return (v * (d > 0)) @ v.T


def frac_shift(qdiag, a, a0):
    return sum(q * (x*x-y*y) / 2 for q, x, y in zip(qdiag, a, a0))


def fraction_constructions():
    a0 = [F(1), F(0)]
    q = [F(1, 2), F(2, 5)]
    spring = [x/(1-x) for x in q]
    shifts = [frac_shift(q, a, a0) for a in
              ([F(0), F(1)], [F(1, 2), F(1)], [F(1, 2), F(-1)])]
    assert spring == [F(1), F(2, 3)]
    assert shifts == [F(-1, 20), F(1, 80), F(1, 80)]
    # Analytic rank-one exclusion in PROOFS.md: useful |z|<1; both
    # damage signs imply |z|>3/2. These strict rational intervals are disjoint.
    assert F(1) < F(3, 2)
    q2 = [F(2, 5), F(3, 5)]
    s2 = [x/(1-x) for x in q2]
    useful = -frac_shift(q2, [F(0), F(0)], a0)
    safety = frac_shift(q2, [F(0), F(1)], a0)
    assert (useful, safety) == (F(1, 5), F(1, 10))
    assert sum(q2) == 1 and max(q2) < 1
    assert s2 == [F(2, 3), F(3, 2)]
    # Full-PSD feasibility is not actual diagonal-catalog accessibility.
    qcross = [[F(1,4),F(1,4)],[F(1,4),F(1,4)]]
    benefit_matrix = [[F(0),F(1)],[F(1),F(0)]]
    cross_benefit = sum(qcross[i][j]*benefit_matrix[j][i]
                        for i in range(2) for j in range(2))
    assert cross_benefit == F(1,2)
    assert all(benefit_matrix[i][i] == 0 for i in range(2))
    return {
        "three_sign_Q_diagonal": list(map(str, q)),
        "three_sign_S_diagonal": list(map(str, spring)),
        "three_exact_barrier_shifts": list(map(str, shifts)),
        "rank_one_exclusion": "|z|<1 and |z|>3/2 impossible; see analytic proof",
        "two_target_Q_diagonal": list(map(str, q2)),
        "two_target_S_diagonal": list(map(str, s2)),
        "two_target_benefits": [str(useful), str(safety)],
        "finite_rank_one_exclusion": "trace(Q)>=1 required; finite rank-one Q<I has trace<1",
        "inaccessible_cross_spring_full_PSD_benefit":str(cross_benefit),
        "actual_diagonal_catalog_benefit":"0 for every diagonal Q",
    }


def direct_free_energy_change(h, u, s, force, kt):
    hp = h + u @ s @ u.T
    return (force @ (np.linalg.solve(h, force)-np.linalg.solve(hp, force)) / 2
            + kt * (np.linalg.slogdet(hp)[1]-np.linalg.slogdet(h)[1]) / 2)


def common_host_checks(rng, ntests=80):
    errors = {k: 0.0 for k in ("free_energy", "inverse_S", "barrier", "dQ",
                              "finite_cap", "cap_support_optimality", "cap_dual_gap")}
    sampled_points = 0
    for _ in range(ntests):
        n, r = 5, 3
        m = rng.normal(size=(n, n))
        h = m @ m.T + np.eye(n)
        u = rng.normal(size=(n, r))
        g = u.T @ np.linalg.solve(h, u)
        gs, gi = root(g), root(g, inverse=True)
        m = rng.normal(size=(r, r))
        s = m @ m.T / 3
        l = gs @ s @ gs
        q = sym(np.eye(r)-np.linalg.inv(np.eye(r)+l))
        assert np.linalg.eigvalsh(q).min() >= -1e-12
        assert np.linalg.eigvalsh(q).max() < 1
        sinv = gi @ (np.linalg.inv(np.eye(r)-q)-np.eye(r)) @ gi
        errors["inverse_S"] = max(errors["inverse_S"], np.linalg.norm(s-sinv))
        kt = 0.7
        forces = [rng.normal(size=n), rng.normal(size=n)]
        a = [gi @ (u.T @ np.linalg.solve(h, f)) for f in forces]
        expected = [x @ q @ x / 2-kt*np.linalg.slogdet(np.eye(r)-q)[1]/2 for x in a]
        direct = [direct_free_energy_change(h, u, s, f, kt) for f in forces]
        errors["free_energy"] = max(errors["free_energy"], max(abs(x-y) for x,y in zip(expected,direct)))
        c = (np.outer(a[1],a[1])-np.outer(a[0],a[0]))/2
        errors["barrier"] = max(errors["barrier"], abs(np.trace(q@c)-(direct[1]-direct[0])))
        d = rng.normal(size=(r, r)); ds = d @ d.T / 4
        inv = np.linalg.inv(np.eye(r)+l)
        exact_dq = inv @ gs @ ds @ gs @ inv
        eps = 1e-5
        qp = np.eye(r)-np.linalg.inv(np.eye(r)+gs@(s+eps*ds)@gs)
        qm = np.eye(r)-np.linalg.inv(np.eye(r)+gs@(s-eps*ds)@gs)
        errors["dQ"] = max(errors["dQ"], np.linalg.norm((qp-qm)/(2*eps)-exact_dq))
        # A finite, full-PSD Loewner hardware cap. Its optimum is attained.
        smax = s + np.eye(r)
        qmax = sym(np.eye(r)-np.linalg.inv(np.eye(r)+gs@smax@gs))
        qms = root(qmax)
        w = sym(rng.normal(size=(r, r)))
        compressed = sym(qms @ w @ qms)
        qopt = qms @ positive_projector(compressed) @ qms
        optimum = np.maximum(np.linalg.eigvalsh(compressed), 0).sum()
        errors["cap_dual_gap"] = max(errors["cap_dual_gap"], abs(np.trace(w@qopt)-optimum))
        ss = gi @ (np.linalg.inv(np.eye(r)-qopt)-np.eye(r)) @ gi
        cap_violation = max(0.0, -np.linalg.eigvalsh(sym(smax-ss)).min())
        errors["finite_cap"] = max(errors["finite_cap"], cap_violation)
        for __ in range(25):
            _, v = np.linalg.eigh(sym(rng.normal(size=(r, r))))
            z = (v * rng.uniform(size=r)) @ v.T
            feasible = qms @ z @ qms
            violation = max(0.0, np.trace(w@feasible)-optimum)
            errors["cap_support_optimality"] = max(errors["cap_support_optimality"], violation)
            sampled_points += 1
    assert errors["free_energy"] < 2e-11
    assert errors["inverse_S"] < 2e-10
    assert errors["barrier"] < 2e-11
    assert errors["dQ"] < 2e-8
    assert errors["finite_cap"] < 1e-9
    assert errors["cap_dual_gap"] < 1e-10
    assert errors["cap_support_optimality"] < 1e-10
    return {"cases": ntests, "cap_feasible_samples": sampled_points, "max_absolute_errors": errors}


def energy_optimum(w, pa, kt, budget):
    def candidate(lam):
        d, v = np.linalg.eigh(sym(w-lam*pa))
        q = np.zeros_like(d)
        use = d > lam*kt/2
        q[use] = 1-lam*kt/(2*d[use])
        mat = (v*q)@v.T
        cost = np.trace(pa@mat)-kt*np.log1p(-q).sum()/2
        return mat, float(cost), d, q
    lo, hi = 1e-12, 1.0
    while candidate(hi)[1] > budget:
        hi *= 2
    for _ in range(100):
        mid = (lo+hi)/2
        if candidate(mid)[1] > budget:
            lo = mid
        else:
            hi = mid
    lam = hi
    q, cost, d, eig = candidate(lam)
    objective = float(np.trace(w@q))
    lag_max = float(d@eig + lam*kt*np.log1p(-eig).sum()/2)
    dual = lam*budget+lag_max
    return q, {"lambda": lam, "cost": cost, "budget": budget,
               "objective": objective, "dual_upper_bound": dual,
               "primal_dual_gap": dual-objective,
               "max_Q_eigenvalue": float(max(eig))}


def stiffness_optimum(w, budget):
    d, v = np.linalg.eigh(sym(w))
    def candidate(lam):
        q = np.zeros_like(d)
        use = d > lam
        q[use] = 1-np.sqrt(lam/d[use])
        return q, float((q/(1-q)).sum())
    lo, hi = 1e-12, max(float(max(d)), 1.0)
    for _ in range(100):
        mid = (lo+hi)/2
        if candidate(mid)[1] > budget:
            lo = mid
        else:
            hi = mid
    eig, cost = candidate(hi)
    q = (v*eig)@v.T
    obj = float(d@eig)
    dual = hi*budget+float(d@eig-hi*(eig/(1-eig)).sum())
    return q, {"lambda": hi, "cost": cost, "budget": budget,
               "objective": obj, "dual_upper_bound": dual,
               "primal_dual_gap": dual-obj,
               "max_Q_eigenvalue": float(max(eig))}


def resource_checks(rng):
    # Nondiagonal A-establishment cost: its optimum need not commute with W.
    w = np.array([[2.1, .45, -.2],[.45, .8, .25],[-.2,.25,-.7]])
    aa = np.array([1.2,-.5,.7]); pa = np.outer(aa,aa)/2
    q, energy = energy_optimum(w, pa, kt=.8, budget=.9)
    qs, stiffness = stiffness_optimum(w, budget=2.3)
    max_energy_excess = max_stiff_excess = 0.0
    for _ in range(500):
        m = rng.normal(size=(3,3)); s = m@m.T
        s *= rng.uniform(.05,1.0)*2.3/np.trace(s)
        trial = np.eye(3)-np.linalg.inv(np.eye(3)+s)
        max_stiff_excess = max(max_stiff_excess, float(np.trace(w@trial))-stiffness["objective"])
        # Independently find a feasible scalar rescaling under energy budget.
        def ec(t):
            x = t*trial
            return float(np.trace(pa@x)-.8*np.linalg.slogdet(np.eye(3)-x)[1]/2)
        lo, hi = 0.0, 1.0
        if ec(hi) > .9:
            for __ in range(60):
                mid = (lo+hi)/2
                if ec(mid) > .9: hi=mid
                else: lo=mid
            scale = lo
        else: scale=1.0
        max_energy_excess = max(max_energy_excess, float(np.trace(w@(scale*trial)))-energy["objective"])
    for receipt in (energy, stiffness):
        assert abs(receipt["cost"]-receipt["budget"]) < 1e-10
        assert abs(receipt["primal_dual_gap"]) < 1e-10
        assert 0 <= receipt["max_Q_eigenvalue"] < 1
    assert max_energy_excess < 1e-10 and max_stiff_excess < 1e-10
    energy["noncommutation_norm_Q_W"] = float(np.linalg.norm(q@w-w@q))
    energy["random_feasible_objective_excess_max"] = max_energy_excess
    stiffness["random_feasible_objective_excess_max"] = max_stiff_excess
    return {"energy_budget": energy, "normalized_stiffness_budget": stiffness,
            "random_comparators": 500}


def finite_temperature_checks():
    bu = math.log(5/8)/2
    bh = math.log(5/2)/2
    def shift(k):
        return 4.5*(.25-1/(4+k))+.5*math.log((1+k/4)/(1+k))
    eps=1e-5
    deriv=(shift(eps)-shift(-eps))/(2*eps)
    assert bu < 0 < bh
    assert abs(deriv+3/32) < 1e-10
    assert shift(1) < 0 < shift(3)
    return {"entropy_only_useful_shift_in_kBT": bu,
            "entropy_only_damage_shift_in_kBT": bh,
            "reversal_derivative_exact": "-3/32",
            "reversal_derivative_finite_difference": deriv,
            "reversal_shift_kappa_1": shift(1),
            "reversal_shift_kappa_3": shift(3)}


def poisson_information_check():
    delta, mp, mm = F(1,10), F(3), F(5)
    itt = mp+mm
    its = delta*(mp-mm)
    iss = delta**2*(mp+mm)
    schur = iss-its**2/itt
    direct = 4*delta**2*mp*mm/(mp+mm)
    assert schur == direct == F(3,40)
    e, k = F(100), F(1,5)
    mp = mm = e*k/2
    balanced = 4*delta**2*mp*mm/(mp+mm)
    assert balanced == delta**2*k*e == F(1,5)
    return {"profiled_information_exact":str(schur),
            "balanced_information_exact":str(balanced),
            "scope":"independent homogeneous Poisson channel, exact exponential response, nuisance log baseline, regular CR premises"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args=parser.parse_args()
    rng=np.random.default_rng(20261015)
    out={"scope":"conditional exact constructions and bounded numerical identities; no physical validation",
         "python":platform.python_version(),"numpy":np.__version__,"seed":20261015,
         "exact_constructions":fraction_constructions(),
         "common_host_and_cap":common_host_checks(rng),
         "resource_optimization":resource_checks(rng),
         "finite_temperature_counterexamples":finite_temperature_checks(),
         "acquisition_information":poisson_information_check(),
         "status":"PASS"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps(out,indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
