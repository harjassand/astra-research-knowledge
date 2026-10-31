"""Exact-rational checks for the 4-state common-stationary construction."""
from fractions import Fraction as F
from itertools import product
import json


def matmul(A, B):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*B)] for row in A]


def build(weights):
    B = [[F(1),F(0),F(0)], [F(0),F(1),F(0)],
         [F(0),F(0),F(1)], [F(-1),F(-1),F(-1)]]
    C = [[F(3,4),F(-1,4),F(-1,4),F(-1,4)],
         [F(-1,4),F(3,4),F(-1,4),F(-1,4)],
         [F(-1,4),F(-1,4),F(3,4),F(-1,4)]]
    raw = {}
    for i, a in enumerate(weights):
        for sign in (-1,1):
            b = sign*a
            A = [[F(1),F(0),F(0)], [F(b),F(1),F(0)],
                 [F(b*b),F(2*b),F(1)]]
            raw[i,sign] = matmul(matmul(B,A), C)
    M = max(F(1), max(abs(x) for A in raw.values() for row in A for x in row))
    alpha = F(1)/(16*M)
    matrices = {key: [[F(1,4)+alpha*x for x in row] for row in A]
                for key,A in raw.items()}
    for P in matrices.values():
        assert all(sum(row)==1 for row in P)
        assert all(sum(col)==1 for col in zip(*P))
        assert min(x for row in P for x in row) >= F(3,16)
    return matrices,alpha


def check(weights):
    matrices,alpha = build(weights)
    beta = F(1,8)
    observations = []
    for signs in product((-1,1), repeat=len(weights)):
        p = [[F(3,8)],[F(1,4)],[F(1,4)],[F(1,8)]]
        for i,sign in enumerate(signs):
            p = matmul(matrices[i,sign],p)
        assert all(x[0]>=0 for x in p)
        assert sum(x[0] for x in p)==1
        reward = p[0][0]+p[1][0]+p[3][0]
        S = sum(s*a for s,a in zip(signs,weights))
        expected = F(3,4)-beta*alpha**len(weights)*S*S
        assert reward==expected
        observations.append((reward,S))
    best = max(r for r,s in observations)
    yes = any(s==0 for r,s in observations)
    assert (best==F(3,4))==yes
    return {"weights": weights,"sequences_checked":len(observations),
            "partition_exists":yes,"alpha":str(alpha),
            "best_reward":str(best),"minimum_nonzero_gap_bound":str(beta*alpha**len(weights))}


if __name__ == "__main__":
    results = [check(w) for w in ([1,2,3],[1,2,4],[3,5,6,8],[3,5,6,9],[2,7,11,18],[101,103,107,311])]
    print(json.dumps({"status":"all_exact_rational_checks_passed","results":results},indent=2))
