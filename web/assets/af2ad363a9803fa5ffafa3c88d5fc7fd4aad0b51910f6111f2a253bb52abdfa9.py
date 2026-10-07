"""Exact acquired enumeration for a balanced, calibrated one-pair no-go.

Uses the earlier own determinant implementation. Does not read peer outputs.
The entire state space has only 45 candidate two-line sets.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys
import json
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from initial_checks import det, det_permutation, holes


def family(t):
    return [[0,t,t,1],[0,0,t,1],[0,0,0,1],[0,0,0,0]]


def line_system(t, sigma):
    f = family(t)
    lines = [(tuple(Q(j==i) for j in range(4)),tuple(Q(x) for x in f[i]),Q(1),f"o{i+1}") for i in range(4)]
    for i,j in combinations(range(4),2):
        lines.append((tuple(Q(k==i) for k in range(4)),tuple(Q(k==j) for k in range(4)),sigma,f"c{i+1}{j+1}"))
    return lines


def weights(t, sigma):
    lines = line_system(t,sigma)
    result = {}
    for a,b in combinations(range(len(lines)),2):
        v,w,activity,_ = lines[a]
        vp,wp,activityp,_ = lines[b]
        matrix = [[v[j],w[j],vp[j],wp[j]] for j in range(4)]
        d = det(matrix)
        assert d == det_permutation(matrix)
        result[(a,b)] = activity*activityp*d*d
    return result


def main():
    started = time.perf_counter()
    sigma = Q(1,10**8*5**4)
    lines = line_system(Q(1),sigma)
    polynomial = {}
    values = [weights(Q(t),sigma) for t in (0,1,2)]
    for state in values[0]:
        a0,a1,a2 = [d[state] for d in values]
        quadratic = (a2-2*a1+a0)/2
        linear = a1-a0-quadratic
        assert linear == 0
        polynomial[state] = (quadratic,a0)
    high = {s for s,(a,c) in polynomial.items() if a}
    low = {s for s,(a,c) in polynomial.items() if not a and c}
    assert len(high) == 4 and len(low) == 6
    for s in high:
        assert polynomial[s][1] == 0
    expected_high = {frozenset(("o1","o3")),frozenset(("o1","c24")),frozenset(("o1","c34")),frozenset(("o2","c14"))}
    assert {frozenset(lines[i][3] for i in s) for s in high} == expected_high
    for x in high:
        for y in high:
            if (0 in x) != (0 in y):
                assert not (set(x)&set(y))
            if len(set(x)-set(y)) <= 1:
                assert (0 in x) == (0 in y)
    # Union-preserving moves preserve the additive indicator for all tuples.
    positive = high|low
    fibers = {}
    for x in positive:
        for y in positive:
            union = tuple(sorted(x+y))
            value = int(0 in x)+int(0 in y)
            if union in fibers:
                assert fibers[union] == value
            fibers[union] = value
    fixtures = []
    for length in [2,10,50,100]:
        t = Q(2**length)
        w = weights(t,sigma)
        z = sum(w.values(),Q(0))
        assert z == t*t*(1+3*sigma)+3*sigma*(1+sigma)
        b = sum((w[s] for s in low),Q(0))/z
        assert b == 3*sigma*(1+sigma)/z
        p = sum((ws for s,ws in w.items() if 0 in s),Q(0))/z
        assert p == (t*t*(1+2*sigma)+sigma)/z
        eta = 2*b-b*b
        lower_bound = p*(1-p)/(4*eta)
        assert lower_bound >= t*t/240
        f = family(t)
        z0 = holes(f,[])
        assert z0 == t*t
        maxima = [max(holes(f,{i,j})/z0 for j in range(4) if i!=j) for i in range(4)]
        assert maxima == [1,1,1,1]
        # Cheap two-line crossing explicitly exists; no two-line no-go is claimed.
        source = next(s for s in high if frozenset(lines[i][3] for i in s) == frozenset(("o1","o3")))
        target = next(s for s in high if frozenset(lines[i][3] for i in s) == frozenset(("o2","c14")))
        assert len(set(source)-set(target)) == 2
        assert w[target]/w[source] == sigma
        fixtures.append({"L":length,"t":str(t),"Z":str(z),"rare_mass":str(b),"one_layer_indicator_probability":str(p),"variance":str(p*(1-p)),"comparison_lower_bound":str(lower_bound),"simple_lower_bound":str(t*t/240),"hole_maxima":maxima})
    result = {"status":"PASS","arithmetic":"exact rational; determinant cross-check by permutation expansion", "sigma":str(sigma),"candidate_line_sets":45,"high_states":[{"lines":[lines[i][3] for i in s],"quadratic_weight_coefficient":str(polynomial[s][0])} for s in sorted(high)],"low_states":[{"lines":[lines[i][3] for i in s],"weight":str(polynomial[s][1])} for s in sorted(low)],"fixtures":fixtures,"boundary":"Blocks <=1 line replacement per layer plus arbitrary union-preserving moves; explicit two-line crossing has ratio sigma and evades the obstruction", "scope":"Exact finite state acquisition and proof bookkeeping, not a general mixing implementation", "wall_seconds":time.perf_counter()-started}
    destination = Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(result,default=str,indent=2)+'\n')
    print(json.dumps({"status":"PASS","high_states":len(high),"low_states":len(low),"fixtures":len(fixtures),"wall_seconds":result['wall_seconds'],"result_path":str(destination)}))


if __name__ == '__main__':
    main()
