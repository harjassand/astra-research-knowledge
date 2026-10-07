"""Finite exact checks for the release-reset deductions, not release proofs."""
import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp


def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2


checks = {}
t, theta = sp.symbols("t theta", real=True)
radial = sp.Matrix([2, -1, -1])
transverse = sp.Matrix([0, 1, -1])
P = sp.eye(3) - sp.ones(3) / 3
K = theta * sp.eye(3) + (1 - theta) * sp.ones(3) / 3
variables = sp.symbols("h0:3", real=True)
field = sp.Matrix(variables)
exp_field = field.applyfunc(sp.exp)
psi = P * (K * exp_field).applyfunc(sp.log)
B = P * psi.jacobian(field) * P
B0 = sp.simplify(B.subs({v: 0 for v in variables}))
B_line = B.subs({v: t * radial[i] for i, v in enumerate(variables)})
Bprime = sp.simplify(B_line.diff(t).subs(t, 0))
expected = theta * (1 - theta) * P * sp.diag(*radial) * P
assert sp.simplify(B0 - theta * P) == sp.zeros(3)
assert sp.simplify(Bprime - expected) == sp.zeros(3)
assert sp.simplify(Bprime * radial - theta * (1 - theta) * radial) == sp.zeros(3, 1)
assert sp.simplify(Bprime * transverse + theta * (1 - theta) * transverse) == sp.zeros(3, 1)
gram_prime = sp.simplify((Bprime.T * B0 + B0.T * Bprime) / theta**2)
assert sp.simplify(gram_prime - 2 * (1 - theta) * P * sp.diag(*radial) * P) == sp.zeros(3)
checks["potts_q3_exact"] = {
    "B_at_zero": str(B0),
    "B_first_variation": str(Bprime),
    "radial_first_variation": str(theta * (1 - theta)),
    "transverse_first_variation": str(-theta * (1 - theta)),
    "normalized_gram_first_variation_at_theta_half": str(gram_prime.subs(theta, sp.Rational(1, 2))),
}

# Softmax posterior coordinates exactly linearize an individual Potts edge.
weights = sp.Matrix(sp.symbols("y0:3", positive=True))
partition = sum(weights)
posterior = weights / partition
new_weights = K * weights
new_posterior = new_weights / sum(new_weights)
assert sp.simplify(new_posterior - (sp.ones(3, 1) / 3 + theta * (posterior - sp.ones(3, 1) / 3))) == sp.zeros(3, 1)
J = sp.diag(*posterior) - posterior * posterior.T
Jnew = sp.diag(*new_posterior) - new_posterior * new_posterior.T
B_rational = P * sp.diag(*(1 / z for z in new_weights)) * K * sp.diag(*weights) * P
transported_jacobian = (Jnew * B_rational).applyfunc(sp.cancel)
assert (transported_jacobian - theta * J).applyfunc(sp.cancel) == sp.zeros(3)
# Factor through the already computed Jacobian rather than expanding a large
# unsimplified rational metric product. The direct expansion was interrupted.
metric_defect = (9 * transported_jacobian.T * transported_jacobian - theta**2 * 9 * J.T * J).applyfunc(sp.cancel)
assert metric_defect == sp.zeros(3)
F = 3 * (exp_field / sum(exp_field) - sp.ones(3, 1) / 3)
mixed_hessian = sp.Matrix([
    sum(sp.diff(F[i], variables[j], variables[k]).subs({v: 0 for v in variables}) * radial[j] * transverse[k]
        for j in range(3) for k in range(3))
    for i in range(3)
])
assert mixed_hessian == P * sp.diag(*radial) * transverse
assert mixed_hessian == -transverse
checks["posterior_coordinate_repair"] = {
    "exact_edge_conjugacy": True,
    "exact_pullback_metric_identity": True,
    "mixed_fusion_hessian_q3": str(mixed_hessian),
    "simultaneous_edge_and_fusion_flatness": False,
}

dimension_checks = []
for q in range(2, 9):
    Pq = sp.eye(q) - sp.ones(q) / q
    hq = sp.Matrix([q - 1] + [-1] * (q - 1))
    Aq = Pq * sp.diag(*hq) * Pq
    is_zero = Aq == sp.zeros(q)
    assert is_zero == (q == 2)
    dimension_checks.append({"q": q, "first_variation_zero": is_zero, "rank": Aq.rank()})
checks["potts_dimensions"] = dimension_checks

parity_checks = []
for n in range(4, 8):
    permutations = list(itertools.permutations(range(n)))
    even = [p for p in permutations if parity(p) == 0]
    for omitted in (2, 3):
        keep = tuple(range(n - omitted))
        all_images = Counter(tuple(p[i] for i in keep) for p in permutations)
        even_images = Counter(tuple(p[i] for i in keep) for p in even)
        assert all_images.keys() == even_images.keys()
        assert all(2 * even_images[k] == all_images[k] for k in all_images)
        parity_checks.append({
            "n": n, "omitted": omitted,
            "tuple_count": len(all_images), "full_TV": "1/2", "marginal_TV": "0",
        })
checks["parity_blind_complements"] = parity_checks

even4 = [p for p in itertools.permutations(range(4)) if parity(p) == 0]
compositions = Counter(tuple(p[q[i]] for i in range(4)) for p in even4 for q in even4)
assert set(compositions) == set(even4)
assert set(compositions.values()) == {len(even4)}
checks["A4_convolution_stationarity"] = True

output = Path(__file__).with_name("release_reset_check_results.json")
output.write_text(json.dumps(checks, indent=2) + "\n")
print(json.dumps({"symbolic_dimension_cases": 7, "posterior_conjugacy_and_metric": True, "parity_marginal_checks": len(parity_checks), "convolution_check": True, "output": str(output)}))
