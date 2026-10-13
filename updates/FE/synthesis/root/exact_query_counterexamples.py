"""Independent rational verification of two failed endpoint transfers.

The search provenance belongs to the hidden-gate worker. This implementation
uses a directly inverted two-by-two grounded matrix and Python Fraction only.
It checks explicit counterexamples, not an exhaustive class or a new algorithm.
Run with --output-dir to keep evidence writes in a new owned directory.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse, json, platform


def F(c, m=(Q(1), Q(1))):
    a, b, c = c
    x, y = m
    return (b*x*x+a*y*y+c*(x+y)**2)/(a*b+a*c+b*c)


def ratio(lo, hi, m):
    return F(lo, m)/F(hi, m)


def one_step(lo, hi, m, excluded):
    candidates = {}
    for e in range(3):
        if e in excluded:
            continue
        vals = []
        for t in [lo[e], hi[e]]:
            ll, hh = list(lo), list(hi)
            ll[e] = hh[e] = t
            vals.append(ratio(ll, hh, m))
        candidates[e] = max(vals)
    return min(candidates.values()), candidates


def record(q):
    return {"exact": str(q), "approximate": float(q)}


def main(out):
    lo = [Q(1, 4), Q(8), Q(1, 8)]
    hi = [Q(33, 4), Q(72), Q(5, 8)]
    m = [Q(1), Q(1)]
    rows = []
    for t in [lo[0], Q(5, 4), hi[0]]:
        ll, hh = lo.copy(), hi.copy()
        ll[0] = hh[0] = t
        value, options = one_step(ll, hh, m, {0})
        rows.append({"answer_a": str(t), "value": record(value),
                     "second_query_scores": {str(k): record(v) for k, v in options.items()}})
    peak = Q(rows[1]["value"]["exact"])
    endpoint = max(Q(rows[0]["value"]["exact"]), Q(rows[2]["value"]["exact"]))
    assert peak > endpoint
    # This is the value AFTER the fixed first query; do not claim that this
    # particular first query is optimal among initial choices.
    initial_endpoint_values = {}
    for first in range(3):
        scores = []
        for t in [lo[first], hi[first]]:
            ll, hh = lo.copy(), hi.copy()
            ll[first] = hh[first] = t
            scores.append(one_step(ll, hh, m, {first})[0])
        initial_endpoint_values[str(first)] = record(max(scores))
    endpoint_dp = min(Q(r["exact"]) for r in initial_endpoint_values.values())
    real_lower = min(peak, Q(initial_endpoint_values["1"]["exact"]),
                     Q(initial_endpoint_values["2"]["exact"]))
    assert real_lower > endpoint_dp

    lo2 = [Q(1, 8), Q(2), Q(4)]
    hi2 = [Q(1025, 8), Q(10), Q(6)]
    m2 = [Q(1, 2), Q(4)]
    joint_rows = []
    for t in [Q(0), Q(1, 4), Q(1)]:
        a, b = Q(1, 8)+128*t, 2+8*t
        rr = F([a,b,lo2[2]],m2)/F([a,b,hi2[2]],m2)
        joint_rows.append({"parameter": str(t), "ratio": record(rr)})
    assert Q(joint_rows[1]["ratio"]["exact"]) > max(
        Q(joint_rows[0]["ratio"]["exact"]), Q(joint_rows[2]["ratio"]["exact"]))
    assert all(x > 0 for x in lo+lo2)
    relative_rows=[]
    for t in [Q(1,8),Q(6),Q(513,32)]:
        rr=F([Q(1),t,Q(8)],[Q(2),Q(8)])/F([Q(2),4*t,Q(10)],[Q(2),Q(8)])
        formula=2*(t+216)*(12*t+5)/((2*t+141)*(9*t+8))
        assert rr == formula
        relative_rows.append({"interval": [str(t),str(4*t)],"ratio":record(rr)})
    assert Q(relative_rows[1]["ratio"]["exact"])>max(
        Q(relative_rows[0]["ratio"]["exact"]),Q(relative_rows[2]["ratio"]["exact"]))
    report = dict(status="PASS", runtime=platform.python_version(), arithmetic="exact fractions",
        matrix="[[a+c,-c],[-c,b+c]]", edges=["0-ground","1-ground","0-1"],
        first_fixed_adaptive=dict(lower=list(map(str,lo)),upper=list(map(str,hi)),masses=list(map(str,m)),
            rows=rows,interior_excess=record(peak-endpoint),
            endpoint_only_initial_scores=initial_endpoint_values,
            endpoint_only_two_query_minimax=record(endpoint_dp),
            true_two_query_minimax_lower_bound=record(real_lower),
            scope="Endpoint-only dynamic programming strictly underestimates deterministic two-query minimax ratio. Exact global optimum is not computed; randomized or average-case policies are not addressed."),
        joint_rank_two=dict(lower=list(map(str,lo2)),upper=list(map(str,hi2)),masses=list(map(str,m2)),
            update="a=1/8+128t,b=2+8t,c unresolved in [4,6],t in [0,1]", rows=joint_rows,
            scope="Refutes a common-scalar rank-two extension; independent-coordinate fixed batches retain their vertex theorem."),
        relative_precision=dict(lower=["1","1/8","8"],upper=["2","513/8","10"],masses=["2","8"],
            queried_edge="1-ground", legal_intervals="[a,4a], a in [1/8,513/32]",rows=relative_rows,
            scope="An interior relative-error interval is worse than both end intervals; the bounded additive-width endpoint theorem remains intact."),
        universal_proof_checked=False, historical_priority="UNKNOWN")
    out.mkdir(parents=True,exist_ok=True)
    (out/"EXACT_QUERY_COUNTEREXAMPLES.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("--output-dir",type=Path,required=True)
    main(p.parse_args().output_dir)
