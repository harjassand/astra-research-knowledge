"""Exact static score transfer for the raw all-order dual alternative.

The two-parity 3x3 products can be an augmented balanced-tree aggregate.
This file audits the transfer identity itself; it is not a fast raw sampler.
"""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path


def alpha_transfer(state, n):
    t = F(n-1, n+1)
    gaps = [state[i+1]-state[i] for i in range(len(state)-1)]
    gaps += [n+state[0]-state[-1]]
    exponent = sum(gaps[1::2])
    x, y, z = t**exponent, t**(n-exponent), F(0)
    for parity, gap in enumerate(gaps):
        q = t**gap
        r = t**(1-gap)*(1-q)
        if parity % 2 == 0:
            x, y, z = q*x, y/q, z+(1-q)*x+r*y
        else:
            x, y, z = x/q, q*y, z+r*x+(1-q)*y
    return z/((1+t)*(1-t**n))


def audit():
    source = Path(__file__).resolve().parents[1]/"root"/"all_order_response.py"
    spec = importlib.util.spec_from_file_location("root_positive_score", source)
    root = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(root)
    count = 0
    for n in range(4, 11):
        for mask in range(1, 1 << n):
            if mask.bit_count() % 2 == 0:
                continue
            state = [i for i in range(n) if mask >> i & 1]
            exact = alpha_transfer(state, n)
            lower, upper, scale = root.alpha_interval(state, n, 100)
            assert F(lower, scale) <= exact <= F(upper, scale)
            count += 1
    return {"odd_subsets_checked": count, "rings": list(range(4, 11)),
            "method": "Exact rational 3x3 gap transfer versus outward positive gap sum",
            "passed": True}


if __name__ == "__main__":
    result = audit()
    Path(__file__).with_name("raw_dual_transfer_audit.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))
