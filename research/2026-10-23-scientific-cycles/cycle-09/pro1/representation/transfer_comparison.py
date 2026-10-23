#!/usr/bin/env python3
"""Evaluate proved formulas, retained comparators and existence constants.

No bath cutoff, matrix extrapolation, code compiler or physical simulation.
Uses Python's standard-library Decimal for reproducible rounded observations.
The all-parameter inequalities are proved in SPECTRAL_CLIPPING_CAPACITY.tex.
"""
import argparse
from decimal import Decimal, localcontext
from math import comb
from pathlib import Path
import hashlib
import json
import resource
import time


def collision_v(k, D=Decimal):
    n = (k - 2) // 2
    a = D(comb(2*n, n)) / D(4**n)
    collision = (2*n+1) * a * (D(k-1) - D(2*n)/3)
    v = D(k*(k-1))/8 - collision/8
    return collision, v


def run(denominators=(16, 64, 256, 512, 2048)):
    started = time.perf_counter()
    rows = []
    with localcontext() as ctx:
        ctx.prec = 100
        D = Decimal
        ell = D(2).ln()
        log10 = D(10).ln()
        for den in denominators:
            beta = D(1)/den
            b = beta*beta
            T = 1-b.ln()
            k = int(1/(16*b*T))
            r = b*k
            c, v = collision_v(k)
            B = ell*v*b*b
            epsilon_upper = 8*ell*r/3 * (-1/(2*ell*r)).exp()
            epsilon_budget = B/(256*k)
            kappa = B*(1-b)/128
            lyapunov_t = kappa/(2*k*k)
            gap = kappa*kappa/(4*k*k)
            new_uniform = ell*b/(65536*T)
            new_exact_v = B/(64*k)
            k8 = int(1/(4*beta))
            _, v8 = collision_v(k8)
            old_uniform = ell*beta**3/8192
            old_exact_v = ell*v8*b*b/(32*k8)
            delta = b*b/512
            q = D("0.5")-delta
            cc = -b/128
            x, y, z = q*q, q*(1-q)/2, (1-q)**2/4
            def entropy(ps):
                return -sum(p*p.ln()/ell for p in ps if p)
            h2 = lambda p: entropy([p, 1-p])
            pair = entropy([x]+[z]*4+[y+cc]*2+[y-cc]*2)/2
            four = pair+x*y*(1-h2((1+cc/y)/2))/2
            repair_free_witness = 1-ell*b*c/16
            log10_rank_bound = D(k)*D(3).ln()/log10
            assert k >= 2 and r < D(1)/64
            assert epsilon_upper <= epsilon_budget
            assert new_exact_v >= new_uniform
            rows.append({
                "beta_denominator": den,
                "beta": str(beta), "b": str(b), "k": k,
                "T_ln_e_over_b": str(T), "bk": str(r),
                "C_k": str(c), "v_k": str(v),
                "epsilon_upper": str(epsilon_upper),
                "epsilon_budget": str(epsilon_budget),
                "all_stated_scalar_margins_pass": True,
                "new_uniform_excess_lower": str(new_uniform),
                "new_exact_v_excess_lower": str(new_exact_v),
                "cycle8_k": k8,
                "cycle8_uniform_excess_lower": str(old_uniform),
                "cycle8_exact_v_excess_lower": str(old_exact_v),
                "new_exact_v_over_cycle8_exact_v": str(new_exact_v/old_exact_v),
                "pair_actual_entropy_excess": str(pair-D("1.5")),
                "nonscalar_four_call_actual_entropy_excess": str(four-D("1.5")),
                "best_retained_certified_excess": str(max(
                    new_exact_v, old_exact_v, pair-D("1.5"), four-D("1.5"))),
                "input_rank": "rank(B_plus), unknown; at most 3^k",
                "log10_input_dimension_upper": str(log10_rank_bound),
                "kappa": str(kappa), "lyapunov_t": str(lyapunov_t),
                "one_minus_lambda": str(gap),
                "log10_C_lyapunov": str((2*k*lyapunov_t-gap.ln())/log10),
                "log10_type_cutoff_coefficient_upper_3k_over_t":
                    str(log10_rank_bound-lyapunov_t.ln()/log10),
                "affine_relative_density_witness_expectation": str(repair_free_witness),
                "affine_witness_scope":
                    "Negative proves the smaller-coefficient un-clipped affine input is not positive at this angle/length. Positive does not prove positivity.",
            })
        counterexamples = {
            "mislabelled_endpoint_k4": {
                "actual_second_moment": 72, "invalid_claimed_bound": 48},
            "unpinched_Dicke_reference_k4_q2": {
                "eigenvalue": 8, "second_moment": 64, "invalid_claimed_bound": 48},
            "unpinched_Dicke_reference_k8_q4": {
                "exponential_moment": str(D(1).exp()), "invalid_claimed_bound": str(D(8)/3)},
        }
    return {
        "precision_decimal_digits": 100,
        "exact_input_beta_denominators": list(denominators),
        "observations": rows, "omitted_premise_counterexamples": counterexamples,
        "scope": "Rounded evaluations of closed, analytically proved formulas. No finite check proves the all-length theorem; no capacity optimization or code compilation.",
        "wall_seconds": time.perf_counter()-started,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "discovery_inference_review_total": "Unknown",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({
        "rows": [{key:r[key] for key in [
            "beta_denominator", "k", "new_exact_v_excess_lower",
            "cycle8_exact_v_excess_lower", "new_exact_v_over_cycle8_exact_v",
            "affine_relative_density_witness_expectation"]} for r in result["observations"]],
        "wall_seconds": result["wall_seconds"],
        "peak_rss_kib_linux": result["peak_rss_kib_linux"]
    }, indent=2))
