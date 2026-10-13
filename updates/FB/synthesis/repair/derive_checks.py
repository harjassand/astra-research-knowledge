"""Independent finite qualification checks; no material simulator or fitted rates.

All chain examples are synthetic rational Markov reward systems. The optical
numbers are recalculated from the preserved source's approximate theoretical
inputs; exact arithmetic does not make those physical inputs exact.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math


def solve(a, b):
    n = len(b)
    m = [[F(x) for x in row] + [F(b[i])] for i, row in enumerate(a)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k])
        m[k], m[p] = m[p], m[k]
        z = m[k][k]
        m[k] = [x / z for x in m[k]]
        for i in range(n):
            if i != k:
                z = m[i][k]
                m[i] = [x - z*y for x, y in zip(m[i], m[k])]
    return [row[-1] for row in m]


def mv(p, v):
    return [sum((x*y for x, y in zip(row, v)), F(0)) for row in p]


def value(p, r):
    return solve([[F(int(i == j))-p[i][j] for j in range(len(p))]
                  for i in range(len(p))], r)


def stringify(v):
    return [str(x) for x in v]


def main():
    eta = F(100) / (F(100) + 1/F(24, 10**10))
    photon = F(453, 100) * F(1602176634, 10**28)
    assert eta == F(3, 12500003)
    assert 1 / eta == F(12500003, 3)
    p = [[F(1,4), F(1,4), F(0)],
         [F(0), F(1,2), F(1,4)],
         [F(1,8), F(0), F(1,4)]]
    r, d, c = [F(1,2), F(2,3), F(1,3)], [F(1,10), F(1,20), F(1,8)], [F(1), F(2), F(3)]
    g, damage, cost = value(p,r), value(p,d), value(p,c)
    assert all(0 <= d[i] <= 1-sum(p[i]) for i in range(3))
    assert all(g[i] == r[i] + mv(p,g)[i] for i in range(3))
    assert all(damage[i] == d[i]+mv(p,damage)[i] for i in range(3))
    assert all(cost[i] == c[i]+mv(p,cost)[i] for i in range(3))
    delta = min(1-sum(row) for row in p)
    assert max(g) <= max(r)/delta
    ratio_cap = max(r[i]/d[i] for i in range(3))
    assert all(g[i] <= ratio_cap*damage[i] for i in range(3))
    assert all(g[i] <= F(1,2)*cost[i] for i in range(3))
    # Exact tail truncation and a uniform upper remainder certificate.
    partial, term = [F(0)]*3, r[:]
    for _ in range(80):
        partial = [x+y for x,y in zip(partial,term)]
        term = mv(p,term)
    tail_cap = max(r)*(1-delta)**80/delta
    assert all(0 <= g[i]-partial[i] <= tail_cap for i in range(3))
    # Same repaired endpoint, different survivor dynamics: no composition from q.
    one_shot = value([[F(0)]], [F(1)])[0]
    long_chain = value([[F(999,1000)]], [F(1)])[0]
    assert one_shot == 1 and long_chain == 1000
    # Same first-step repair/survival probabilities, different outgoing type.
    good = value([[F(9,10),F(0)],[F(0),F(0)]], [F(9,10),F(0)])[0]
    bad = value([[F(0),F(9,10)],[F(0),F(0)]], [F(9,10),F(0)])[0]
    assert good == 9 and bad == F(9,10)
    # Uniform gain certificate valid under every adaptive action sequence.
    actions = [([[F(1,4),F(1,4)],[F(1,8),F(1,4)]],[F(1,3),F(1,2)]),
               ([[F(1,8),F(1,4)],[F(1,4),F(1,4)]],[F(1,2),F(1,4)])]
    v = [F(1), F(1)]
    assert all(all(rew[i]+mv(kernel,v)[i] <= v[i] for i in range(2))
               for kernel,rew in actions)
    stationary_values = []
    for a in (0,1):
        for b in (0,1):
            kernel = [actions[a][0][0],actions[b][0][1]]
            rew = [actions[a][1][0],actions[b][1][1]]
            ans = value(kernel,rew)
            assert all(x <= 1 for x in ans)
            stationary_values.append(stringify(ans))
    # Finite distinct-defect cap: even perfect repair/survival cannot beat M.
    caps = []
    for m in (1,10,1000,10**6,4166667,4166668):
        phi = eta*m
        caps.append({"distinct_defects":m,"ideal_phi":str(phi),"exceeds_one":phi>1})
    assert not caps[-2]["exceeds_one"] and caps[-1]["exceeds_one"]
    # Exact zero-termination confidence formula; rounding is checked on both sides.
    ef = float(eta)
    n_min = math.floor(math.log(.05)/math.log1p(-ef))+1
    up_prev = -math.expm1(math.log(.05)/(n_min-1))
    up = -math.expm1(math.log(.05)/n_min)
    assert up < ef <= up_prev
    # Large mean with unbounded tail; an expected gain is not a hard completion cap.
    assert F(999,1000)**10000 > 0
    out = {
        "status":"Internal exact synthetic checks and conditional optical arithmetic only",
        "not_established":["material mechanism","physical coefficients","novel mathematics","safe retained manufacturing advantage"],
        "optical": {"eta":str(eta),"photons_per_loaded_triplet":str(1/eta),
                    "absorbed_energy_J_per_loaded_triplet":float(photon/eta),
                    "uniform_termination_necessary_for_phi_above_one":str(eta),
                    "all_success_independent_transfer_trials_to_certify_delta_below_eta_at_95_percent":n_min,
                    "confidence_qualifier":"Sufficient homogeneous per-transfer zero-loss assay, not universal acquisition lower bound; independence and type uniformity must be acquired"},
        "three_type_fixture":{"P":[stringify(x) for x in p],"r":stringify(r),"d":stringify(d),"c":stringify(c),
                              "gain":stringify(g),"expected_damage":stringify(damage),"expected_cost":stringify(cost),
                              "termination_floor":str(delta),"ratio_cap":str(ratio_cap),
                              "eighty_step_tail_upper_bound":float(tail_cap)},
        "countermodels":{"scope":"Finite rational type models with unlimited fresh-defect supply; finite specimen needs depletion state and finite supply cap",
                          "same_endpoint_q_one_survivor_gain":str(one_shot),"same_endpoint_q_long_survivor_gain":str(long_chain),
                          "same_first_marginals_good_type_gain":str(good),"same_first_marginals_bad_type_gain":str(bad)},
        "adaptive_certificate":{"v":stringify(v),"all_action_inequalities":True,"stationary_policy_values":stationary_values},
        "finite_defect_caps":caps,
        "all_assertions_passed":True,
    }
    dest=Path(__file__).with_name("derived_results.json")
    dest.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__ == "__main__":
    main()
