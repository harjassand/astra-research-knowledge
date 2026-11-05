#!/usr/bin/env python3
"""Narrow deterministic checks of two marking kernels and the score identity.

The common bounded outcome is Y=tanh(P), with P a standard Gaussian. This is
an algebraic example, not execution of a thermal apparatus or campaign.
"""
from pathlib import Path
import json
import math
from scipy.integrate import quad


def expect(fn):
    split = [-12.0, -math.pi / 2, -1.0, 0.0, 1.0, math.pi / 2, 12.0]
    return sum(quad(lambda z: fn(z) * math.exp(-z*z/2) / math.sqrt(2*math.pi),
                    a, b, epsabs=2e-12, epsrel=2e-12, limit=200)[0]
               for a, b in zip(split[:-1], split[1:]))


def xlogx(x):
    return 0.0 if x <= 0 else x * math.log(x)


def kernel_record(name, s, mean_exact):
    signal = expect(lambda z: z*s(z))
    mutual_info = expect(lambda z: (xlogx(1+s(z))+xlogx(1-s(z)))/2)
    score_mean = 2*expect(lambda z: s(z)*math.tanh(z))
    arm_var = 4*expect(lambda z: math.tanh(z)**2)-score_mean**2
    weighted_var = 4*expect(lambda z: s(z)**2*math.tanh(z)**2)-score_mean**2
    gap_direct = 4*expect(lambda z: (1-s(z)**2)*math.tanh(z)**2)
    residual = abs(arm_var-weighted_var-gap_direct)
    assert abs(signal-mean_exact) < 1e-10
    assert residual < 1e-10
    assert weighted_var <= arm_var + 1e-12
    return {"kernel": name, "positive_arm_momentum_mean": signal,
            "analytic_momentum_mean": mean_exact,
            "mean_energy_difference": expect(lambda z: z*z*s(z)),
            "arm_momentum_mutual_information_nats": mutual_info,
            "bounded_outcome": "tanh(P)",
            "contrast": score_mean, "arm_score_variance": arm_var,
            "weighted_score_variance": weighted_var,
            "rao_blackwell_variance_gap": gap_direct,
            "variance_identity_residual": residual}


def main():
    out = {"scope": "Gaussian integral checks; no thermal apparatus or campaign executed.",
           "sigma": 1.0, "marking_Lipschitz_constant": 1.0,
           "records": [
               kernel_record("sine", math.sin, math.exp(-0.5)),
               kernel_record("clipped_linear", lambda z: max(-1., min(1., z)),
                             math.erf(1/math.sqrt(2)))],
           "tail_note": "Integrals are over [-12,12]; omitted Gaussian tail is below 4e-33."}
    path = Path(__file__).with_name("weighted_score_checks.json")
    path.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
