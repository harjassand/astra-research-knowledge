"""Finite exhaustive checks for the principal's soft XOR quadratization.

These checks audit small truth tables; the uniform proof is in researcher_b.txt.
"""
from itertools import product
from math import exp, prod
from pathlib import Path
import json


def gate_penalty(a, b, c, d):
    return (c - a - b + 2*d)**2 + a*b - 2*a*d - 2*b*d + 3*d


def quadratic_penalty(a, b, c, d):
    return (c + a + b + 7*d - 2*c*a - 2*c*b + 4*c*d
            + 3*a*b - 6*a*d - 6*b*d)


gate_cases = 0
for a, b, c, d in product((0, 1), repeat=4):
    penalty = gate_penalty(a, b, c, d)
    assert penalty == quadratic_penalty(a, b, c, d)
    assert penalty >= 0
    assert (penalty == 0) == (d == a*b and c == (a ^ b))
    gate_cases += 1

Jc, M = 3, 30
all_aux_assignments = 0
port_inputs = 0
max_relative_excess = 0.0
per_q = []
for q in range(2, 7):
    R = 2*(q-1)
    qmax = 0.0
    for ports in product((0, 1), repeat=q):
        parity = sum(ports) % 2
        zeros = 0
        partition = 0.0
        for aux in product((0, 1), repeat=R):
            previous = ports[0]
            penalty = 0
            for i, next_port in enumerate(ports[1:]):
                c, d = aux[2*i:2*i+2]
                penalty += gate_penalty(previous, next_port, c, d)
                previous = c
            if penalty == 0:
                zeros += 1
                assert previous == parity
            else:
                assert penalty >= 1
            partition += exp(-2*Jc*previous - M*penalty)
            all_aux_assignments += 1
        assert zeros == 1
        ideal = exp(-2*Jc*parity)
        excess = partition/ideal - 1
        bound = (2**R - 1)*exp(2*Jc-M)
        assert excess >= -1e-13
        assert excess <= bound + 1e-12
        qmax = max(qmax, excess)
        max_relative_excess = max(max_relative_excess, excess)
        port_inputs += 1
    per_q.append({"q": q, "R": R,
                  "max_relative_excess": qmax,
                  "uniform_bound": (2**R - 1)*exp(2*Jc-M)})

# A positive weighted sum and then a product preserve the checkwise bracket.
positive_sum_checks = 0
epsilon = 0.01
for m in range(1, 7):
    weights = [1 + i*i for i in range(1, 2**m + 1)]
    relative = [prod(1 + epsilon*((i >> j) & 1) for j in range(m))
                for i in range(2**m)]
    ratio = sum(w*f for w, f in zip(weights, relative))/sum(weights)
    assert 1 <= ratio <= (1+epsilon)**m + 1e-12
    positive_sum_checks += 1

result = {"gate_truth_table_cases": gate_cases,
          "port_inputs": port_inputs,
          "auxiliary_assignments": all_aux_assignments,
          "Jc": Jc, "M": M,
          "maximum_relative_excess": max_relative_excess,
          "per_q": per_q,
          "positive_sum_checks": positive_sum_checks,
          "status": "all assertions passed"}
out = Path(__file__).with_name("pairwise_gadget_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
