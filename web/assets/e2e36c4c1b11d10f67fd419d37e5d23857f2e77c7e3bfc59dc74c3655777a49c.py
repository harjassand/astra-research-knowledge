from fractions import Fraction as Q
import json

# Exact qubit frame calculation for diagonal covariance matrices K.
# H_i = a_i . sigma and K = sum_i p_i a_i a_i^T.
# A rank-one POVM is an antipodal Bloch ensemble; its covariance has trace 1.
examples = [
    [Q(1), Q(0), Q(0)],
    [Q(1, 3), Q(2, 3), Q(1, 6)],
    [Q(0), Q(3, 5), Q(1, 5)],
]
# Compatible positive qubit channel eigenvalues; mu_i=(2 lambda_i-1)_+ sums to 1/2.
lambdas = [Q(3, 4), Q(1, 2), Q(1, 4)]
mu = [max(Q(0), 2*x-Q(1)) for x in lambdas]
assert sum(mu) <= 1
records = []
for diagK in examples:
    # q(p)=min_frame average joint variance = Tr(K)-lambda_max(K).
    qval = sum(diagK)-max(diagK)
    # Dirichlet energy of the diagonal channel on this frame.
    energy = sum(k*(1-lam) for k,lam in zip(diagK,lambdas))
    assert qval <= 2*energy
    # Choi/separable identity: for antipodal states +/-e_j, cost=TrK-K_jj.
    costs = [sum(diagK)-diagK[j] for j in range(3)]
    assert min(costs) == qval
    records.append({
        "K_diagonal": [str(x) for x in diagK],
        "q_exact": str(qval),
        "canonical_axis_costs": [str(x) for x in costs],
        "Dirichlet_energy": str(energy),
        "q_le_2_energy": True,
    })
print(json.dumps({
    "scope": "exact diagonal qubit frame checks only",
    "lambda": [str(x) for x in lambdas],
    "positive_part_2lambda_minus_1": [str(x) for x in mu],
    "records": records,
    "does_not_establish": "the higher-dimensional selfcompatible-channel inequality",
}, indent=2))
