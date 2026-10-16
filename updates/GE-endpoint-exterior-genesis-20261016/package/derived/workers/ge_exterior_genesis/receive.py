#!/usr/bin/env python3
"""Replay a certified full sorted-endpoint receiver on an executed finite input."""
import argparse
import json
from pathlib import Path
import secrets
import time
from checks import heat_rows, laplacian, cover_laplacian, PrefixMass
from sampler import sample_sorted_endpoints


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, default=3)
    parser.add_argument("--samples", type=int, default=100)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    cert = json.loads((here / "checks_receipt.json").read_text())
    case = cert["finite_bit_count_cases"][args.case]
    if int(case["survival_lower_bound"]["numerator"]) <= 0:
        raise ValueError("positive certified survival lower bound required")
    n, k = case["n"], case["k"]
    edges, potential = case["edge_rates"], case["site_killing_rates"]
    negative = [(0, n - 1)] if case["cycle"] and k % 2 == 0 else []
    c = (cover_laplacian(n, edges, potential, negative) if negative
         else laplacian(n, edges, potential))
    begin = time.perf_counter()
    rows, scale, epsilon = heat_rows(c, case["start"], case["m"], case["p"])
    if negative:
        rows = [[row[y] - row[y + n] for y in range(n)] for row in rows]
    oracle = PrefixMass(rows)
    setup_elapsed = time.perf_counter() - begin
    begin = time.perf_counter()
    draws = [sample_sorted_endpoints(n, k, oracle, secrets.randbits, attempts=32)
             for _ in range(args.samples)]
    sample_elapsed = time.perf_counter() - begin
    assert all(len(x["endpoint"]) == k and len(set(x["endpoint"])) == k
               and x["endpoint"] == sorted(x["endpoint"])
               and all(0 <= y < n for y in x["endpoint"])
               and x["decisions"] <= case["full_endpoint_decision_bound"] for x in draws)
    out = {"status": "PASS", "case": case["name"], "samples": args.samples,
           "output": "sorted occupied endpoint sites conditional on no prior collision/death",
           "certificate_TV_bound": case["full_endpoint_sampler_TV_bound"],
           "assumption": "independent fair bits; secrets execution is a software diagnostic",
           "first_ten_endpoints": [x["endpoint"] for x in draws[:10]],
           "fair_bits_consumed": sum(x["fair_bits"] for x in draws),
           "maximum_decisions_observed": max((x["decisions"] for x in draws), default=0),
           "maximum_prefix_queries_observed": max((x["distinct_prefix_mass_queries"] for x in draws), default=0),
           "rejection_fallbacks": sum(x["rejection_fallbacks"] for x in draws),
           "zero_mass_fallbacks": sum(x["zero_mass_fallbacks"] for x in draws),
           "heat_squaring_integer_products": case["heat_squaring_scalar_integer_products"],
           "setup_elapsed_seconds_diagnostic": setup_elapsed,
           "sampling_elapsed_seconds_diagnostic": sample_elapsed,
           "inference_time_seconds": "UNKNOWN", "model_token_usage": "UNKNOWN"}
    (here / "full_endpoint_receiver_receipt.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
