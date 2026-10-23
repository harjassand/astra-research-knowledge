#!/usr/bin/env python3
"""Exact rational candidate plus high-precision entropy diagnostic.

The rigorous certificate is analytic, in two_call_entropy.md, not this finite
evaluation. Uses the Python standard library only. No bath truncation is used.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
import argparse
import json
import platform
import resource
import time


def run():
    started = time.perf_counter()
    beta = F(1, 512)
    b = beta * beta
    delta = b*b/512
    c = -b/128
    q = F(1, 2)-delta
    x, y, z = q*q, q*(1-q)/2, (1-q)*(1-q)/4
    eigenvalues = [x] + [z]*4 + [y+c]*2 + [y-c]*2
    assert sum(eigenvalues) == 1
    assert all(F(1, 16) <= e <= F(1, 4) for e in eigenvalues)
    assert x+4*y+4*z == 1 and y > abs(c)
    drift = (1-b)*(4*delta+2*b*c)
    assert drift == -(1-b)*b*b/128 < 0
    certificate = 2*delta-28*c*c-7*delta*delta
    uniform_certificate = F(569, 262144)*b*b
    simple_certificate = b*b/512
    assert certificate >= uniform_certificate > simple_certificate > 0
    with localcontext() as ctx:
        ctx.prec = 110
        def d(f):
            return Decimal(f.numerator)/Decimal(f.denominator)
        ln2 = Decimal(2).ln()
        entropy = -sum(d(e)*d(e).ln()/ln2 for e in eigenvalues)
        excess = entropy-3
        output = {
            "status": "candidate_exact_arithmetic_passed",
            "beta": str(beta), "b_beta_squared": str(b),
            "delta": str(delta), "c": str(c),
            "q": str(q), "x": str(x), "y": str(y), "z": str(z),
            "bulk_drift_exact_conditional_on_separate_map_identity": str(drift),
            "bulk_drift_decimal": str(d(drift)),
            "entropy_decimal_observed": str(entropy),
            "entropy_excess_decimal_observed": str(excess),
            "formal_entropy_excess_lower_bound_exact": str(certificate),
            "uniform_lower_bound_exact": str(uniform_certificate),
            "simpler_strict_lower_bound_exact": str(simple_certificate),
            "formal_entropy_excess_lower_bound_decimal": str(d(certificate)),
            "rate_bits_per_forward_use_observed_if_coding_obligation_met": str(entropy/2),
            "spectral_min_exact": str(min(eigenvalues)),
            "spectral_max_exact": str(max(eigenvalues)),
            "decimal_precision": ctx.prec,
            "diagnostic_not_interval_certificate": True,
            "bath_cutoff_used": False,
            "proof_source": "two_call_entropy.md, inequalities C3-C4",
        }
    output.update({"wall_seconds": time.perf_counter()-started,
                   "max_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   "python": platform.python_version(), "platform": platform.platform()})
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2)+"\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")
