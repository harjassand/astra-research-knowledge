#!/usr/bin/env python3
"""Exact normalization/cost checks and small Weyl diagnostics; not an asymptotic proof.

Run from any directory: python replay_frontier.py --output replay_frontier.json
No old recurrence/tree-capacity replay is invoked.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path
import numpy as np


def dyck_dimension(m: int) -> int:
    return math.comb(2*m, m) // (m+1) * 2**m


def least_length(k: int) -> tuple[int, int]:
    m = 1
    while dyck_dimension(m) < k:
        m += 1
    assert m == 1 or dyck_dimension(m-1) < k
    return 2*m, dyck_dimension(m)


def fraction_string(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def run() -> dict:
    start = time.perf_counter()
    bounds = []
    for bits in (8, 16, 64, 256, 1024, 4096):
        k = 2**bits
        n, dim = least_length(k)
        for f in (Fraction(1,4), Fraction(1,2), Fraction(9,10), Fraction(1)):
            p = (f-Fraction(1,k*k))/(1-Fraction(1,k*k))
            fe = p+(1-p)/k**2
            half_error = (1-p)*(1-Fraction(1,k*k))
            assert 0 <= p <= 1 and fe == f and half_error == 1-f
            upper = p*n
            best_lower, best_l = Fraction(0), 0
            # M_l=floor(sqrt(8**l)), exactly, without floating point.
            for ell in range(n+1):
                m_l = math.isqrt(8**ell)
                lower = max(Fraction(0), (ell+1)*(f-Fraction(m_l,k)))
                if lower > best_lower:
                    best_lower, best_l = lower, ell
            assert best_lower <= upper
            bounds.append({"logical_bits":bits,"fidelity":fraction_string(f),
                "exact_code_calls":n,"code_dimension_at_least_K":dim>=k,
                "best_tested_cutoff":best_l,
                "lower_cost_per_log2K":float(best_lower/bits),
                "achieved_cost_per_log2K":float(upper/bits),
                "theorem_limit":float(f/Fraction(3,2))})

    weyl = []
    for k in (2,3,5,7):
        phi = np.eye(k,dtype=complex).reshape(-1)/math.sqrt(k)
        j_id = np.outer(phi,phi.conj())
        states=[]
        for a in range(k):
            for b in range(k):
                w=np.zeros((k,k),complex)
                for col in range(k):
                    w[(col+a)%k,col]=np.exp(2j*np.pi*b*col/k)
                v=np.kron(np.eye(k),w)@phi
                states.append(v)
        mat=np.column_stack(states)
        gram_error=float(np.linalg.norm(mat.conj().T@mat-np.eye(k*k)))
        j_depol=sum(np.outer(v,v.conj()) for v in states)/(k*k)
        depol_error=float(np.linalg.norm(j_depol-np.eye(k*k)/(k*k)))
        bell_half=float(np.abs(np.linalg.eigvalsh(j_id-j_depol)).sum()/2)
        assert gram_error<1e-11 and depol_error<1e-12
        assert abs(bell_half-(1-1/k**2))<1e-12
        for p in (0.0,0.25,0.5,1.0):
            j=p*j_id+(1-p)*j_depol
            fe=float(np.real(phi.conj()@j@phi))
            half=float(np.abs(np.linalg.eigvalsh(j_id-j)).sum()/2)
            assert abs(fe-(p+(1-p)/k**2))<1e-12
            assert abs(half-(1-fe))<1e-12
        weyl.append({"K":k,"gram_error":gram_error,"depolarizing_Choi_error":depol_error,
                     "Bell_witness_half_trace_distance":bell_half,
                     "full_trace_distance":2*bell_half})

    # Exact integer certificates for the coherent-history numerical constants.
    # h2(1/100)<0.0808 iff 100**2500 < 2**202 * 99**2475.
    arithmetic={
        "h2_one_percent_lt_0.0808":100**2500 < 2**202*99**2475,
        "log2_3_lt_1.585":3**200 < 2**317,
        "log2_3_gt_1.5849":3**10000 > 2**15849,
        "q_above_binomial_peak_for_beta_le_1_over_512":100**2 < 512**2-1,
    }
    assert all(arithmetic.values())
    q=0.01
    entropy= -q*math.log2(q)-(1-q)*math.log2(1-q)
    arithmetic["rank_exponent_approx"]=1.5+entropy+q*(math.log2(3)-1.5)
    arithmetic["exact_rational_rank_exponent_upper"]="1.58165"
    arithmetic["exact_rational_tail_exponent_upper"]="-0.0092"
    # A concrete failure of unbounded-expectation continuity.
    mean_counterexample=[]
    for m in (10,100,1000):
        tv=Fraction(1,m)
        mean_difference=tv*m*m
        assert mean_difference==m
        mean_counterexample.append({"half_trace_distance":fraction_string(tv),
            "N_on_rare_event":m*m,"expectation_difference":int(mean_difference)})

    return {"status":"finite_diagnostics_passed","scope":"normalization, exact cost brackets, Weyl witness, and exact numerical inequalities; no universal theorem inferred from samples",
        "cost_bounds_not_exact_finite_K_optima":bounds,"weyl_diagnostics":weyl,
        "history_exponent_arithmetic_certificates":arithmetic,
        "unbounded_expectation_continuity_counterexample":mean_counterexample,
        "resources":{"wall_seconds":time.perf_counter()-start,
                     "max_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     "python":sys.version.split()[0],"numpy":np.__version__,
                     "machine":platform.machine()}}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="replay_frontier.json")
    args=parser.parse_args()
    receipt=run()
    Path(args.output).write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":receipt["status"],"output":args.output,
                      "resources":receipt["resources"]},indent=2))
