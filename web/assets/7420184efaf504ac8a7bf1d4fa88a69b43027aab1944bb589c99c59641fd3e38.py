#!/usr/bin/env python3
"""Owned exact fixtures and lightweight Schur-sector diagnostics.

No peer code is imported. Exact rational fixtures supplement the analytic
all-N proofs in PHASE2_DEEP_ATTACK.txt; floating limits are not certificates.
"""
from fractions import Fraction as F
from math import comb, erf, exp, lgamma, log, pi, sqrt
from pathlib import Path
import json
import time
import sympy as sp


def multiplicity(N, twice_j):
    k = (N - twice_j) // 2
    return comb(N, k) - (comb(N, k - 1) if k else 0)


def sector_iid(N, r):
    lp, lm = (1 + r) / 2, (1 - r) / 2
    out = []
    for tj in range(N % 2, N + 1, 2):
        detpower = (N - tj) // 2
        trrep = sum((lp ** k) * (lm ** (tj - k)) for k in range(tj + 1))
        out.append(multiplicity(N, tj) * (lp * lm) ** detpower * trrep)
    return out


def exact_checks():
    x, y, z, rr, nn = sp.symbols("x y z rr nn", real=True)
    m = sp.Matrix([x, y, z])
    n = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0])
    u = (n.T * m)[0]
    v, rot = n - u * m, n.cross(m)
    coords = sp.Matrix([x, y, z])
    directional_v = v.jacobian(coords) * v
    directional_rot = rot.jacobian(coords) * rot
    per_axis = sp.simplify(directional_v - directional_rot + 2 * u * v)
    checks = {
        "noncoordinate_axis_drift_simplification": per_axis == sp.zeros(3, 1),
        "constant_ball_PSD_margin_3777_over_4096":
            (1 - F(1, 64)) ** 2 - 3 * F(1, 64) == F(3777, 4096),
    }
    C = sp.diag(1, 1, 3)
    mm = sp.Matrix([rr, 0, 0])
    cross = sp.Matrix([[0, 0, 0], [0, 0, -rr], [0, rr, 0]])
    P = sp.eye(3) - mm * mm.T
    D = sp.expand(P * C * P - cross * C * cross.T)
    checks["outer_ball_indefinite_exact"] = sp.simplify(
        D - sp.diag((1 - rr**2)**2, 1 - 3*rr**2, 3 - rr**2)) == sp.zeros(3)
    checks["physical_r_3_over_4_negative_diffusion"] = D.subs(rr, F(3, 4))[1, 1] == -F(11, 16)
    total_cdf, total_optimizer = 0, 0
    for N in range(2, 19):
        q = sector_iid(N, F(0))
        assert sum(q) == 1
        # exp[-4 log(2) J^2] has rational weights for either parity.
        unnormalized = [a * F(1, 2) ** (tj * (tj + 2))
                        for a, tj in zip(q, range(N % 2, N + 1, 2))]
        Z = sum(unnormalized)
        p = [a / Z for a in unnormalized]
        cut = max(i for i, (a, b) in enumerate(zip(p, q)) if a >= b)
        target_T = sum(abs(a - b) for a, b in zip(p, q)) / 2
        assert sum(p[:cut+1]) - sum(q[:cut+1]) == target_T
        for r in [F(0), F(1, 7), F(1, 3), F(3, 4), F(1)]:
            v = sector_iid(N, r)
            assert sum(v) == 1
            for i in range(len(v)):
                assert sum(v[:i+1]) <= sum(q[:i+1])
                total_cdf += 1
            witness_gap = sum(p[:cut+1]) - sum(v[:cut+1])
            assert witness_gap >= target_T
            total_optimizer += 1
    checks["rational_sector_CDF_fixtures"] = True
    checks["rational_antiferro_optimizer_witness_fixtures"] = True
    assert all(checks.values()), checks
    return {"checks": checks, "CDF_fixture_count": total_cdf,
            "optimizer_fixture_count": total_optimizer,
            "proof_scope": "Finite exact transcription fixtures, not all-N theorem validation."}


def sector_base(N):
    ns = []
    log_weights = []
    for tj in range(N % 2, N + 1, 2):
        j = tj / 2
        k = (N - tj) // 2
        # m_j = (2j+1)/(N/2+j+1) binom(N,N/2-j).
        lw = (2*log(tj+1) - log(N/2+j+1) + lgamma(N+1)
              - lgamma(k+1) - lgamma(N-k+1) - N*log(2))
        ns.append(j)
        log_weights.append(lw)
    ws = [exp(v) for v in log_weights]
    norm = sum(ws)
    return ns, [v/norm for v in ws]


def maxwell_CDF(alpha, x):
    u = sqrt(alpha)*x
    return erf(u) - 2*u/sqrt(pi)*exp(-u*u)


def probes():
    out = []
    for N in [32, 128, 512, 2048, 8192]:
        js, q = sector_base(N)
        for kappa in [0.25, 2, 10]:
            raw = [v*exp(-kappa*j*(j+1)/N) for j,v in zip(js,q)]
            norm = sum(raw)
            p = [v/norm for v in raw]
            distance = sum(abs(a-b) for a,b in zip(p,q))/2
            expected_J2_over_N = sum(v*j*(j+1)/N for j,v in zip(js,p))
            a = sqrt(1.5*log(1+kappa/2)/kappa)
            limit = maxwell_CDF(2+kappa,a)-maxwell_CDF(2,a)
            out.append({"N":N,"kappa":kappa,"exact_optimizer_distance_float":distance,
                        "analytic_limit_float":limit,"E_J2_over_N_float":expected_J2_over_N,
                        "analytic_E_J2_over_N_limit":3/(2*(2+kappa))})
    strong=[]
    for N in [32,128,512,2048,8192]:
        js,q=sector_base(N)
        raw=[v*exp(-j*(j+1)) for j,v in zip(js,q)]
        norm=sum(raw);p=[v/norm for v in raw]
        strong.append({"N":N,"a":1,"optimizer_distance_float":sum(abs(a-b) for a,b in zip(p,q))/2})
    return {"critical_boundary_probes":out,"strong_antiferro_probes":strong,
            "status":"FLOATING_DIAGNOSTICS_ONLY", "memory":"O(N) scalar sectors, no 2^N operators"}


if __name__ == "__main__":
    start = time.monotonic()
    result = {"exact":exact_checks(),"floating":probes()}
    result["elapsed_seconds"] = time.monotonic()-start
    path = Path(__file__).with_name("phase2_spin_checks.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"exact_checks":result["exact"],"elapsed_seconds":result["elapsed_seconds"],
                      "output":str(path)},indent=2))
