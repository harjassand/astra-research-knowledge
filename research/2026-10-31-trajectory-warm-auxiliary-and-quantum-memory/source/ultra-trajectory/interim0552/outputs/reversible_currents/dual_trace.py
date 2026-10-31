#!/usr/bin/env python3
"""Verify a frozen predictive-flow dual and evaluate one dependent record.

The certificate must be fixed before seeing the record, or selected from a
predetermined family with an appropriate allocation of alpha. See
PREDICTIVE_DUAL_PROOF.txt. No generating chain or mixing bound is an input.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import json
import math
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "predictive_flow"))
from flow_grid import geometry, prefix, word_feature
from currents import fraction_json, log_bounds


def load_certificate(path, max_states=1000):
    data = json.loads(Path(path).read_text())
    s, L, k = data["alphabet_size"], data["depth"], data["mesh"]
    leaves, nodes, descriptors, words = geometry(s, L, k, max_states)
    n, d = len(nodes), len(descriptors)
    y = list(map(Q, data["row_duals"]))
    dc = list(map(Q, data["data_duals"]))
    z = Q(data["normalization_dual"])
    if len(y) != n*d or len(dc) != 2*len(words) or any(v > 0 for v in y):
        raise ValueError("invalid dual shape or row signs")
    c = [dc[2*j]-dc[2*j+1] for j in range(len(words))]
    H = [-z-v for v in c]
    if H != list(map(Q, data["word_statistic"])):
        raise ValueError("word statistic disagrees with dual")
    rdata = [sum((v*word_feature(node, word, leaves, L, k)
                  for v, word in zip(c, words)), Q(0)) for node in nodes]
    active = [[(v, desc) for v, desc in zip(y[i*d:(i+1)*d], descriptors) if v]
              for i in range(n)]
    cache = {}
    for i, node in enumerate(nodes):
        for side, b, w, sign in descriptors:
            cache[i, side, w] = prefix(node, side, w, leaves, k)
            cache[i, side, (b,)+w] = prefix(node, side, (b,)+w, leaves, k)

    def endpoint(i, j):
        result = rdata[i]
        for v, (side, b, w, sign) in active[i]:
            result += v*(sign*((cache[j, side, w] if nodes[j][0] == b else 0)
                               -cache[i, side, (b,)+w])-Q(1, k))
        return result

    worst = None
    columns = 0
    for i in range(n):
        for j in range(i, n):
            lhs = z+(endpoint(i, j)+endpoint(j, i))/2
            if lhs > 0:
                raise ValueError(f"invalid exact flow column {(i, j)}: {lhs}")
            worst = lhs if worst is None else max(worst, lhs)
            columns += 1
    B = Q(0)
    B_loose = Q(0)
    for i in range(n):
        combined = {}
        for v, (_, b, w, sign) in active[i]:
            combined[b, w] = combined.get((b, w), Q(0))+sign*v
        B = max(B, sum(map(abs, combined.values()), Q(0)))
        B_loose = max(B_loose, sum((abs(v) for v, _ in active[i]), Q(0)))
    R = max(H)-min(H)
    ceil_root = math.isqrt(L)
    if ceil_root*ceil_root < L:
        ceil_root += 1
    return {"alphabet": s, "depth": L, "mesh": k, "nodes": nodes,
        "descriptors": descriptors, "leaves": leaves, "words": words,
        "y": y, "c": c, "z": z, "H": H, "B": B, "B_loose": B_loose,
        "R": R, "C": B/2+ceil_root*R, "columns_checked": columns,
        "maximum_column_lhs": worst}


def trace_statistic(cert, record):
    s, L = cert["alphabet"], cert["depth"]
    if any(not isinstance(a, int) or not 0 <= a < s for a in record):
        raise ValueError("record contains an invalid symbol")
    n = len(record)-2*L
    if n < 1:
        raise ValueError("record too short")
    lookup = dict(zip(cert["words"], cert["H"]))
    T = sum((lookup[tuple(record[t:t+2*L+1])] for t in range(n)), Q(0))
    excess = max(Q(0), -T-cert["R"]/2)
    C = cert["C"]
    exponent = excess**2/(2*n*C*C) if C else Q(0)
    return n, T, exponent


def rate_lower(exponent, transitions, alpha):
    # D11; use an UPPER enclosure on binary entropy and round downward.
    a_lo, a_hi = log_bounds(alpha)
    b_lo, b_hi = log_bounds(1-alpha)
    entropy_upper = -alpha*a_lo-(1-alpha)*b_lo
    lower = max(Q(0), Q(4, transitions)*(alpha*exponent-entropy_upper))
    scale = 2**96
    scaled = lower*scale
    return Q(scaled.numerator//scaled.denominator, scale)


def evaluate(cert, record, alpha=Q(1, 40)):
    alpha = Q(alpha)
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie between zero and one")
    n, T, exponent = trace_statistic(cert, record)
    loglo, loghi = log_bounds(1/alpha)
    lower = rate_lower(exponent, len(record)-1, alpha)
    return {"observations": len(record), "transitions": len(record)-1,
        "overlapping_windows": n, "stationary_preparations_assumed": 1,
        "statistic_sum": str(T), "B": str(cert["B"]), "R": str(cert["R"]),
        "C_rational_upper": str(cert["C"]),
        "null_tail_exponent": fraction_json(exponent),
        "null_tail_bound": "exp(-null_tail_exponent)",
        "reject_reversible": exponent >= loghi,
        "decision_unresolved_by_log_precision": loglo <= exponent < loghi,
        "alpha": fraction_json(alpha), "rate_lower_bound": fraction_json(lower),
        "rate_preview": float(lower), "units": "nats per discrete step",
        "contract": "frozen certificate; one stationary record; fixed horizon"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("certificate", type=Path)
    p.add_argument("record", type=Path, help="JSON list of observed integer symbols")
    p.add_argument("--alpha", default="1/40")
    args = p.parse_args()
    cert = load_certificate(args.certificate)
    result = evaluate(cert, json.loads(args.record.read_text()), Q(args.alpha))
    result["exact_flow_columns_checked"] = cert["columns_checked"]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
