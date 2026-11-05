"""Exact rational certificate for the strong-convexity/local-error boundary.

The physical time is log(2), so exp(-T)=1/2 and exp(-2T)=1/4.
There is no floating ODE integration in this certificate.  It verifies the
rank-one spectral projector algebra for small instances and records exact
large-dimension consequences of the analytically specified family.
"""

from fractions import Fraction as Q
import json
from pathlib import Path


def rank_matrix(s):
    n = s*s+1
    return [[Q(1, 2) if i == j == 0 else
             Q(1, 2*s) if i == 0 or j == 0 else Q(1, 2*s*s)
             for j in range(n)] for i in range(n)]


def exact_check(s):
    p = rank_matrix(s)
    n = len(p)
    for i in range(n):
        for j in range(n):
            assert sum((p[i][k]*p[k][j] for k in range(n)), Q(0)) == p[i][j]
    assert sum(p[i][i] for i in range(n)) == 1
    r = [Q(1)]+[Q(-1)]*(n-1)
    pr = [sum((p[i][j]*r[j] for j in range(n)), Q(0)) for i in range(n)]
    e = [r[i]/2-pr[i]/8 for i in range(n)]
    assert e[0] == Q(s+7, 16)
    assert max(abs(t) for t in e) == e[0]
    return {"s": s, "dimension": n, "projector_idempotence": True,
            "visible_hessian_eigenvalues": [1, 2],
            "per_coordinate_force_error": 1,
            "physical_time": "log(2)",
            "max_coordinate_error_exact": str(e[0])}


def main():
    checked = [exact_check(s) for s in (1,2,4)]
    family = [{"s": s, "dimension": s*s+1,
               "max_coordinate_error_exact": str(Q(s+7,16)),
               "max_coordinate_error": float(Q(s+7,16))}
              for s in (1,2,4,8,9,16,32,64,128,256,1024)]
    data = {
        "status": "exact algebraic verification of an explicit boundary family",
        "checked_projector_instances": checked,
        "analytic_family_consequences": family,
        "theorem": "The Hessian obeys I <= H <= 2I, while fixed-time node error grows as sqrt(n)/16 under unit node-force uncertainty.",
        "scope": "No hidden memory and no acquisition are needed for the counterexample. It excludes dimension-free max-node robustness from strong convexity alone, not Euclidean robustness."
    }
    target = Path(__file__).with_name("exact_network_boundary.json")
    target.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
