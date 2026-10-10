"""Reproducible exact and numerical checks for the rejected repair primitive."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def scale(t, a):
    return [[t * x for x in row] for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def apply(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


rho = F(1, 2)
P = [[F(0), -rho], [F(0), F(1)]]
Q = [[F(1), F(0)], [-rho, F(0)]]
H = [[F(1), rho], [rho, F(1)]]
PQP = matmul(matmul(P, Q), P)
QPQ = matmul(matmul(Q, P), Q)
assert matmul(P, P) == P and matmul(Q, Q) == Q
assert matmul(transpose(P), H) == matmul(H, P)
assert matmul(transpose(Q), H) == matmul(H, Q)
assert PQP == scale(rho * rho, P)
assert QPQ == scale(rho * rho, Q)
assert PQP != QPQ
example = apply(PQP, [F(0), F(1)])
other_example = apply(QPQ, [F(0), F(1)])
assert example == [F(-1, 8), F(1, 4)]
assert other_example == [F(0), F(0)]
x, y = example
energy = (x*x + 2*rho*x*y + y*y)/2
assert energy == F(3, 128)

word_count = 0
for length in range(1, 13):
    for word in product((P, Q), repeat=length):
        v = [F(1), F(1)]
        for repair in word:
            v = apply(repair, v)
        assert all(component != 0 for component in v)
        word_count += 1

angle_checks = []
for theta in (0.1, 0.01, 0.001, 0.0001):
    c, s = math.cos(theta), math.sin(theta)
    p = [[1., 0.], [0., 0.]]
    q = [[c*c, c*s], [c*s, s*s]]
    pqp = matmul(matmul(p, q), p)
    qpq = matmul(matmul(q, p), q)
    difference = [[pqp[i][j] - qpq[i][j] for j in range(2)]
                  for i in range(2)]
    # The symmetric traceless difference has eigenvalues +/-sqrt(a²+b²).
    measured_defect = math.hypot(difference[0][0], difference[0][1])
    predicted_defect = c*c*s
    assert math.isclose(measured_defect, predicted_defect, rel_tol=1e-9)
    output = apply(pqp, [1., 0.])
    repaired = apply(q, output)
    residual = math.dist(output, repaired)
    assert math.isclose(residual, predicted_defect, rel_tol=1e-9)
    v = [c, s]
    for _ in range(100):
        v = apply(q, apply(p, v))
    predicted_after_100 = c**200
    measured_after_100 = math.hypot(*v)
    assert math.isclose(measured_after_100, predicted_after_100, rel_tol=1e-11)
    angle_checks.append({
        'theta': theta,
        'braid_defect': measured_defect,
        'distance_after_three_step_sweep': math.hypot(*output),
        'maximum_local_residual': residual,
        'distance_after_100_pairs': measured_after_100,
    })

result = {
    'status': 'PASS: proposed general finite-repair capability falsified',
    'exact_quadratic_checks': True,
    'rho': str(rho),
    'RSR_0_1': [str(x) for x in example],
    'SRS_0_1': [str(x) for x in other_example],
    'energy_after_RSR': str(energy),
    'nonterminating_words_tested_through_length_12': word_count,
    'small_angle_checks': angle_checks,
    'novelty_claim': False,
}
out = Path(__file__).with_name('verification.json')
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
