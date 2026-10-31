"""Exact checks of a task-first endpoint/record separation.

Own four-state fixture; no producer scientific source code is executed.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def action(A, x):
    return [dot(r, x) for r in A]


def source(c, sigma):
    f = [F(1), F(1), F(-1), F(-1)]
    v = [F(1), F(-1), F(0), F(0)] if sigma == 1 else [F(0), F(0), F(1), F(-1)]
    K = [[F(1,4)+c*(f[i]*v[j]+v[i]*f[j]) for j in range(4)] for i in range(4)]
    return K, f, v


def record_probability(K, f, ys):
    alpha = [F(1,4)*int(f[i] == ys[0]) for i in range(4)]
    for y in ys[1:]:
        alpha = [sum(alpha[i]*K[i][j] for i in range(4))*int(f[j] == y) for j in range(4)]
    return sum(alpha)


def filtered(K, f, v, ys):
    alpha = [F(1,4)*int(f[i] == ys[0]) for i in range(4)]
    total = sum(alpha)
    alpha = [a/total for a in alpha]
    for y in ys[1:]:
        alpha = [sum(alpha[i]*K[i][j] for i in range(4))*int(f[j] == y) for j in range(4)]
        total = sum(alpha)
        alpha = [a/total for a in alpha]
    G = dot(alpha, v)
    p = sum(alpha[i]*sum(K[i][j] for j in range(4) if f[j] == 1) for i in range(4))
    return G, p


def bern_kl(p, q):
    p, q = float(p), float(q)
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))


rows = []
for c in [F(1,10), F(1,16), F(1,32)]:
    worlds = {s: source(c,s) for s in [1,-1]}
    report = {"c":str(c), "worlds":{}}
    for sigma, (K,f,v) in worlds.items():
        assert min(min(r) for r in K) > 0
        assert all(sum(r)==1 for r in K)
        assert all(K[i][j] == K[j][i] for i in range(4) for j in range(4))
        assert action(K, f) == [4*c*x for x in v]
        assert action(K, v) == [2*c*x for x in f]
        assert [f[i]*v[i] for i in range(4)] == [sigma*x for x in v]
        correlations = []
        w = f
        for lag in range(25):
            mu = dot(f,w)/4
            assert mu == ((8*c*c)**(lag//2) if lag%2==0 else 0)
            correlations.append(str(mu))
            w = action(K,w)
        triple = sum(F(ys[0]*ys[1]*ys[2])*record_probability(K,f,ys)
                     for ys in product([1,-1],repeat=3))
        p3 = record_probability(K,f,(1,1,1))
        assert triple == sigma*8*c*c
        assert p3 == F(1,8)+(1+sigma)*c*c
        report["worlds"][str(sigma)] = {"K":[[str(x) for x in r] for r in K],
            "triple":str(triple), "all_plus_three":str(p3),
            "correlations_0_to_8":correlations[:9]}

    max_kl_per_c4 = 0.0
    for length in range(1,9):
        for ys in product([1,-1],repeat=length):
            ps = {}
            for sigma, (K,f,v) in worlds.items():
                G,p = filtered(K,f,v,ys)
                assert abs(G) <= 8*c
                assert p == F(1,2)+2*c*G
                if ys[-1] != sigma:
                    assert G == 0
                    assert p == F(1,2)
                if length >= 2:
                    oldG,_ = filtered(K,f,v,ys[:-1])
                    expected = F(0) if ys[-1]!=sigma else 4*c*ys[-2]/(1+4*c*sigma*oldG)
                    assert G == expected
                ps[sigma] = p
            assert abs(ps[1]-ps[-1]) <= 16*c*c
            for sigma in [1,-1]:
                ratio = bern_kl(ps[sigma],ps[-sigma])/float(c**4)
                max_kl_per_c4 = max(max_kl_per_c4,ratio)
                assert ratio < 2048
    report["max_one_step_KL_over_c4_through_history_length_8"] = max_kl_per_c4
    rows.append(report)

output = {"status":"all exact identities and filter checks passed", "fixtures":rows,
          "scope":"Exact finite checks supplement the analytic proof; no physical samples acquired."}
path = Path(__file__).with_name("task_alternative_checks.json")
path.write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({"status":output["status"], "output":str(path),
                  "maximum_observed_KL_ratio":max(r["max_one_step_KL_over_c4_through_history_length_8"] for r in rows)}))
