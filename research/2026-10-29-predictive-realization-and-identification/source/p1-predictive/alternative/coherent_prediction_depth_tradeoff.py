#!/usr/bin/env python3
"""Exact core/control checks plus a small, individually sampled binary fixture.

No laboratory, GPU, remote job, acquisition-search solver, or source hardware.
The proof is COHERENT_PREDICTION_DEPTH_TRADEOFF.md. Floating checks are labelled.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import random
import time

ROOT = Path(__file__).resolve().parent


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F())
             for j in range(len(b[0]))] for i in range(len(a))]


def norminf(a):
    return max(sum(abs(x) for x in row) for row in a)


def fs(x):
    return str(x.numerator) + "/" + str(x.denominator)


def probability(k, theta):
    return (1 - math.cos(k * theta)) / 2


def inverse3(a):
    aug = [[F(x) for x in row] + [F(i == j) for j in range(3)]
           for i, row in enumerate(a)]
    for k in range(3):
        pivot = next(i for i in range(k, 3) if aug[i][k])
        aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [x/scale for x in aug[k]]
        for i in range(3):
            if i != k:
                scale = aug[i][k]
                aug[i] = [x-scale*y for x,y in zip(aug[i],aug[k])]
    return [row[3:] for row in aug]


def arctan_bounds(x, terms):
    a = sum(((-1)**j * x**(2*j+1) / (2*j+1)
             for j in range(terms)), F())
    b = a + (-1)**terms * x**(2*terms+1)/(2*terms+1)
    return min(a,b), max(a,b)


def sine_bounds(x, terms=15):
    assert 0 <= x <= 1
    a = sum(((-1)**j * x**(2*j+1) / math.factorial(2*j+1)
             for j in range(terms)), F())
    b = a + (-1)**terms*x**(2*terms+1)/math.factorial(2*terms+1)
    return min(a,b),max(a,b)


def main():
    started = time.perf_counter()
    a0 = [[F(1), F(1), F(1)], [F(0), F(1,2), F(1)],
          [F(1,2), F(1), F(1,2)]]
    inv = [[F(3,2), F(-1), F(-1)], [F(-1), F(0), F(2)],
           [F(1,2), F(1), F(-1)]]
    ident = [[F(i == j) for j in range(3)] for i in range(3)]
    assert matmul(a0, inv) == ident == matmul(inv, a0)
    assert norminf(inv) == F(7,2)
    neumann = F(7,2) / (1-F(33,128))
    assert neumann == F(448,95)

    # Exact finite Taylor lower bound, not floating acceptance: e^7 >1000.
    exp7_lower = sum((F(7)**j / math.factorial(j) for j in range(31)), F())
    assert exp7_lower > 1000
    alpha = F(1,1000)
    pi_upper = F(22,7)
    grid = []
    affinity_checks = 0
    for horizon in [128, 256, 1024, 65536, 2**32]:
        assert horizon % 4 == 0
        # H theta0=2pi*(H/4), H theta1=2pi*(H/4)+pi: exact target proof.
        theta0 = math.pi/2
        theta1 = theta0 + math.pi/horizon
        amat = [[1,1,1],
                          [probability(j,theta1) for j in range(3)],
                          [probability(j+1,theta1) for j in range(3)]]
        inverse_norm = norminf(inverse3(amat))
        assert inverse_norm < neumann
        for depth_cap in [1,3,15,31,63]:
            if 4*depth_cap > horizon:
                continue
            k = depth_cap if depth_cap % 2 else depth_cap-1
            lower_q = 4*(1-2*alpha)**2*F(horizon**2,1)/(pi_upper**2*depth_cap**2)
            upper_q = math.ceil(F(16*horizon**2, k*k))
            # A lower pi-free rate gives a conservative integer-usable bill.
            assert lower_q > 0
            for tested in range(depth_cap+1):
                p0 = probability(tested,theta0)
                p1 = probability(tested,theta1)
                p0 = max(0.0,min(1.0,p0))
                p1 = max(0.0,min(1.0,p1))
                affinity = math.sqrt(p0*p1)+math.sqrt((1-p0)*(1-p1))
                lower = 1-(math.pi*tested/horizon)**2/8
                assert affinity + 1e-12 >= lower
                affinity_checks += 1
            gap = abs(probability(k,theta1)-probability(k,theta0))
            assert gap >= k/horizon - 1e-12
            grid.append({"H":horizon,"L":depth_cap,
                         "rank":3,"target_probabilities_exact":[0,1],
                         "inverse_inf_diagnostic":float(inverse_norm),
                         "certified_inverse_inf_upper":fs(neumann),
                         "Q_lower_using_pi_upper":fs(lower_q),
                         "ordinary_Q_upper_at_alpha_0_001":upper_q})

    # Actual individual bit generation, one small fixture. The ideal source
    # probability is rounded down to a 53-bit threshold; include that cost.
    horizon, cap = 128, 15
    k = cap
    shots = math.ceil(F(16*horizon*horizon,k*k))
    # Machin's formula and alternating rational series rigorously enclose pi.
    a_lo,a_hi=arctan_bounds(F(1,5),25)
    b_lo,b_hi=arctan_bounds(F(1,239),5)
    pi_lo,pi_hi=16*a_lo-4*b_hi,16*a_hi-4*b_lo
    assert F(3)<pi_lo<pi_hi<F(22,7)
    x_lo,x_hi=F(k,horizon)*pi_lo,F(k,horizon)*pi_hi
    sin_lo=sine_bounds(x_lo)[0]
    sin_hi=sine_bounds(x_hi)[1]
    # k=15: p1=(1-sin(k*pi/H))/2; monotonicity holds on [0,pi/4].
    assert k%4 == 3
    probability_bands=[(F(1,2),F(1,2)),((1-sin_hi)/2,(1-sin_lo)/2)]
    precision = 1 << 53
    thresholds=[]
    for lo,hi in probability_bands:
        low_floor=(lo*precision).__floor__()
        high_floor=(hi*precision).__floor__()
        assert low_floor == high_floor
        thresholds.append(low_floor)
    native_probs = [F(t,precision) for t in thresholds]
    # midpoint and classification are exact rational operations on the
    # explicitly known two-hypothesis source family.
    midpoint = (native_probs[0]+native_probs[1])/2
    gap_exact = abs(native_probs[1]-native_probs[0])
    conservative_gap = F(k,horizon)-F(1,2**52)
    assert gap_exact >= conservative_gap > 0
    exponent_lower = F(shots,2)*conservative_gap**2
    assert exponent_lower > 7
    records=[]
    rng = random.Random(202610290119)
    for hypothesis, threshold in enumerate(thresholds):
        bits = bytes(int(rng.getrandbits(53)<threshold) for _ in range(shots))
        ones=sum(bits)
        mean=F(ones,shots)
        if native_probs[1] > native_probs[0]:
            decision=int(mean>midpoint)
        else:
            decision=int(mean<midpoint)
        assert decision == hypothesis
        name=f"phase_hypothesis_{hypothesis}_raw_bits.bin"
        (ROOT/name).write_bytes(bits)
        records.append({"hypothesis":hypothesis,"shots":shots,"ones":ones,
                        "decision":decision,
                        "actual_binary_outcomes_generated":shots,
                        "charged_independent_starts":shots,
                        "charged_native_rotation_calls":shots*k,
                        "probability_53bit":fs(native_probs[hypothesis]),
                        "raw_bits_file":name,
                        "raw_bits_sha256":hashlib.sha256(bits).hexdigest()})
    result={
        "status":"PASS",
        "scope":"Ordinary theorem with exact rational core/budget checks; float diagnostic grid and small synthetic individually generated outcomes. Exact rational Machin/sine intervals certify each fixture Bernoulli threshold. No physical operation or external source acquisition.",
        "source_model":"one-qubit y rotation; independently reset episodes; terminal Z test",
        "core_inverse_exact":[[fs(x) for x in row] for row in inv],
        "uniform_inverse_inf_upper":fs(neumann),
        "affinity_diagnostic_checks":affinity_checks,
        "diagnostic_only_float_tolerance":1e-12,
        "grid":grid,
        "fixture":{"H":horizon,"L":cap,"Q_per_hypothesis":shots,
                   "alpha_per_hypothesis":fs(alpha),
                   "total_actual_binary_outcomes":2*shots,
                   "total_charged_starts":2*shots,
                   "total_charged_native_calls":2*shots*k,
                   "probability_argument_error_bound":"1/9007199254740992",
                   "exact_hoeffding_exponent_lower":fs(exponent_lower),
                   "failure_bound":"exp(-exponent_lower) < exp(-7) < 1/1000",
                   "PRNG":"Python random.Random(202610290119); ideal independence is a theorem assumption, not established by replay",
                   "records":records,
                   "long_legal_episode_alternative":"If depth H is legal, one H-call terminal experiment separates the two hypotheses exactly under the ideal source law; zero such physical experiments executed."},
        "wall_seconds":time.perf_counter()-started}
    out=ROOT/"COHERENT_PREDICTION_DEPTH_RESULTS.json"
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"grid_cases":len(grid),
                      "affinity_checks":affinity_checks,
                      "fixture":result["fixture"],
                      "wall_seconds":result["wall_seconds"]},indent=2))


if __name__ == "__main__":
    main()
