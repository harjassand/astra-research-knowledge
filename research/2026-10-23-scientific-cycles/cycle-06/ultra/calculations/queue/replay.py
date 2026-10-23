#!/usr/bin/env python3
"""Bounded exact/classical admission checks; no E_F optimization or matrix search."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import json
import math
import time


def entropy(probs):
    return -sum(float(p) * math.log(float(p)) for p in probs if p)


def labels(k, n, alphabet):
    # Conditional output Bell-label law; for computational readout use alphabet D.
    used = min(k, n)
    w = F(1, alphabet ** (n - used))
    for tail in product(range(alphabet), repeat=n - used):
        yield (0,) * used + tail, w


def mixture(l, n, alphabet):
    out = defaultdict(F)
    joint = defaultdict(F)
    for k in range(1, l + 1):
        for z, p in labels(k, n, alphabet):
            out[z] += p / l
            joint[k, z] += p / l
    assert sum(out.values()) == 1
    return out, joint


def truncated_entropy(q, s):
    den = sum(q ** g for g in range(s))
    return entropy(q ** g / den for g in range(s))


def posterior_formula(q, l):
    return (
        sum(float((1 - q ** s) / l) * truncated_entropy(q, s)
            for s in range(1, l))
        + float((1 - q ** l) / (l * (1 - q))) * truncated_entropy(q, l)
    )


def check(d, l, n):
    alphabet = d * d
    q = F(1, alphabet)
    m = math.log(d)
    delta = (1 - q ** l) / l
    assert (1 / delta).__ceil__() == l + 1

    # Full classical flag plus product Bell-label diagonal memory distributions.
    initial = defaultdict(F)
    returned = defaultdict(F)
    for k in range(1, l + 1):
        for z, p in labels(k, l, alphabet):
            initial[k, z] += p / l
        j = k - 1 if k > 1 else l
        for z, p in labels(k - 1, l, alphabet):
            returned[j, z] += p / l
    actual_delta = sum(abs(initial[x] - returned[x])
                       for x in initial.keys() | returned.keys()) / 2
    assert actual_delta == delta

    out, joint = mixture(l, n, alphabet)
    for i in range(1, n + 1):
        actual_prefix = sum(p for z, p in out.items() if all(t == 0 for t in z[:i]))
        formula_prefix = (max(l - i + 1, 0) + sum(q ** (i-k)
                          for k in range(1, min(l, i - 1) + 1))) / l
        assert actual_prefix == formula_prefix
        assert actual_prefix >= max(F(0), 1 - (i - 1) * delta)

    noise_slots = sum(F(max(n-k, 0), l) for k in range(1, l + 1))
    formula_noise = F(n * (n-1), 2*l) if n <= l else F(2*n-l-1, 2)
    assert noise_slots == formula_noise
    # This is an explicit READOUT upper, not optimized quantum uncertainty.
    bob_conditional, _ = mixture(l, n, d)
    readout_q = entropy(bob_conditional.values())
    genie_lower = float(noise_slots) * m
    assert genie_lower - 1e-12 <= readout_q <= genie_lower + math.log(l) + 1e-12

    row = dict(D=d, L=l, N=n, exact_delta=str(delta),
               exact_expected_Bell_D_pairs=str(F(l+1, 2)),
               exact_mean_private_noise_slots=str(noise_slots),
               optimized_Q_lower_per_complementary_copy=genie_lower,
               explicit_computational_readout_Q=readout_q,
               exact_prefix_probabilities=[str(sum(p for z, p in out.items()
                   if all(t == 0 for t in z[:i]))) for i in range(1, n+1)])
    if n >= l:
        hz = entropy(out.values())
        h_joint = entropy(joint.values())
        h_post = h_joint - hz
        hg = -math.log(1-float(q)) - float(q/(1-q))*math.log(float(q))
        h_formula = posterior_formula(q, l)
        conditional = (2*n-l-1)*m
        assert abs(hz - (conditional + math.log(l) - h_post)) < 1e-11
        assert abs(h_post - h_formula) < 1e-11
        assert -1e-12 <= h_post <= hg + 1e-12
        row.update(output_entropy=hz, exact_posterior_entropy_numeric=h_post,
                   geometric_entropy_upper=hg,
                   subsumed_coherent_information_lower=hz-n*m)
    return row


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    cases = [(2, 1, 1), (2, 1, 2), (2, 2, 2), (2, 2, 3),
             (2, 3, 3), (2, 3, 4), (2, 4, 2), (2, 4, 4), (2, 4, 5),
             (3, 1, 2), (3, 2, 2), (3, 2, 3), (3, 3, 3)]
    rows = [check(*c) for c in cases]
    result = dict(status="PASS", scope="bounded classical diagonal admission checks",
                  no_claims=["E_F optimization", "reservoir supply saving", "historical novelty",
                             "physical validation", "full discovery cost"],
                  cases=rows, case_count=len(cases),
                  measured_replay_cpu_seconds=time.process_time()-cpu,
                  measured_replay_wall_seconds=time.perf_counter()-wall)
    Path(__file__).with_name("RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "scope", "case_count",
          "measured_replay_cpu_seconds", "measured_replay_wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
