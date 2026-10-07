"""Small exact fixtures for the independent microscopic-energy attack.

No sampler or FPRAS is implemented. All arithmetic used for acceptance
assertions is rational. The dense four-site family is a universal proof
fixture; the six-site coordinate-cycle sums are finite diagnostics.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path
import time


def det(a):
    n = len(a)
    if n == 0:
        return Q(1)
    a = [[Q(x) for x in row] for row in a]
    answer = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            answer = -answer
        d = a[j][j]
        answer *= d
        for i in range(j + 1, n):
            r = a[i][j] / d
            for k in range(j + 1, n):
                a[i][k] -= r * a[j][k]
            a[i][j] = Q(0)
    return answer


def det_permutation(a):
    result = Q(0)
    for p in permutations(range(len(a))):
        term = Q(1)
        for i, j in enumerate(p):
            term *= a[i][j]
        inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
        result += term * (-1 if inv % 2 else 1)
    return result


def minor(f, a, b):
    matrix = [[f[i][j] for j in sorted(b)] for i in sorted(a)]
    result = det(matrix)
    assert result == det_permutation(matrix)
    return result


def holes(f, u):
    r = set(range(len(f))) - set(u)
    if len(r) % 2:
        return Q(0)
    return sum((minor(f, a, r - set(a)) ** 2 for a in combinations(sorted(r), len(r)//2)), Q(0))


def dense_family(delta):
    return [[Q(0), 1+delta, Q(1), Q(1)],
            [1+delta, Q(0), Q(1), Q(2)],
            [Q(1), Q(1), Q(0), Q(1)],
            [Q(1), Q(2), Q(1), Q(0)]]


def paired_columns(f, a):
    n = len(f)
    columns = []
    for i in sorted(a):
        columns.append([Q(j == i) for j in range(n)])
        columns.append(list(f[i]))
    return [[column[j] for column in columns] for j in range(n)]


def matchings(vertices):
    if not vertices:
        yield []
        return
    a, *rest = vertices
    for b in rest:
        remaining = [i for i in rest if i != b]
        for tail in matchings(remaining):
            yield [(a, b)] + tail


def cycle_states(q, epsilon):
    """Exactly enumerate colored coordinate perfect matchings; n<=6 here."""
    n = 2*q
    original = {tuple(sorted((i, (i+1) % n))): i for i in range(n)}
    states = []
    for m in matchings(list(range(n))):
        cycle_positions = [j for j, edge in enumerate(m) if edge in original]
        for mask in range(1 << len(cycle_positions)):
            active = {cycle_positions[j] for j in range(len(cycle_positions)) if mask & (1 << j)}
            original_lines = frozenset(original[edge] for j, edge in enumerate(m) if j in active)
            coordinate_lines = tuple(edge for j, edge in enumerate(m) if j not in active)
            weight = epsilon ** len(coordinate_lines)
            states.append((original_lines, coordinate_lines, weight))
    return states


def encode(x):
    if isinstance(x, Q):
        return str(x)
    raise TypeError(type(x).__name__)


def main():
    started = time.perf_counter()
    dense = []
    for length in [2, 3, 10, 40, 100]:
        delta = Q(1, 2**length)
        f = dense_family(delta)
        a, b, ap, bp = [{0,1}, {2,3}, {0,2}, {1,3}]
        amplitudes = [minor(f, s, set(range(4))-s) for s in (a, b, ap, bp)]
        assert amplitudes == [1, 1, delta, delta]
        for s, amplitude in zip((a,b,ap,bp), amplitudes):
            assert det(paired_columns(f, s)) ** 2 == amplitude ** 2
        ratio = amplitudes[2]**2 * amplitudes[3]**2 / (amplitudes[0]**2 * amplitudes[1]**2)
        assert ratio == Q(1, 2**(4*length))
        z = holes(f, [])
        assert z == 4*(1-delta+delta**2)
        g = {str(u): holes(f, u)/z for u in combinations(range(4),2)}
        assert all(Q(1,2) <= x <= Q(32,13) for x in g.values())
        r = [max(holes(f, {i,j})/z for j in range(4) if j != i) for i in range(4)]
        assert all(Q(1,8) <= x <= 4 for x in r)
        # Arbitrary rational pair fields cancel since both tuples use every line once.
        fields = [Q(2), Q(3,5), Q(7), Q(11,13)]
        def field_weight(s):
            value = Q(1)
            for i in s:
                value *= fields[i]
            return value
        field_ratio = ratio * field_weight(ap)*field_weight(bp)/(field_weight(a)*field_weight(b))
        assert field_ratio == ratio
        # An explicit nonscalar ambient preconditioner also cancels exactly.
        G = [[Q(i==j)*(i+2) + Q(j==i+1) for j in range(4)] for i in range(4)]
        transformed = []
        for s in (a,b,ap,bp):
            V = paired_columns(f, s)
            GV = [[sum(G[i][k]*V[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
            transformed.append(det(GV)**2)
        assert transformed[2]*transformed[3]/(transformed[0]*transformed[1]) == ratio
        dense.append({"L": length, "delta": delta, "product_ratio": ratio, "Z": z, "hole_ratios": g, "row_maxima": r})
    F0 = dense_family(Q(0))
    inv0 = [[-1,Q(1,2),0,Q(1,2)], [Q(1,2),Q(-1,2),Q(1,2),0],
            [0,Q(1,2),-1,Q(1,2)], [Q(1,2),0,Q(1,2),Q(-1,2)]]
    assert [[sum(F0[i][k]*inv0[k][j] for k in range(4)) for j in range(4)] for i in range(4)] == [[Q(i==j) for j in range(4)] for i in range(4)]
    assert max(sum(abs(x) for x in row) for row in inv0) == 2
    cycles = []
    for q in [2,3]:
        n = 2*q
        M = n + n*(n-1)//2
        for length in [1,8,30]:
            epsilon = Q(1,2**(M+length))
            states = cycle_states(q, epsilon)
            ordinary = [s for s in states if not s[1]]
            assert len(ordinary) == 2 and all(s[2] == 1 for s in ordinary)
            odd = frozenset(range(0,n,2)); even = frozenset(range(1,n,2))
            assert {s[0] for s in ordinary} == {odd,even}
            z = sum((s[2] for s in states),Q(0))
            beta = (z-2)/z
            assert beta <= epsilon*2**M/2 <= Q(1,2**(length+1))
            eta = 2*beta-beta**2
            variance = (1-beta**2)/4
            universal_energy_bound = 4*eta
            forced_L_lower_bound = variance/universal_energy_bound
            for x in ordinary:
                for y in ordinary:
                    original_union = {i: int(i in x[0])+int(i in y[0]) for i in range(n)}
                    fxy = int(x[0] == odd)+int(y[0] == odd)
                    for xp in ordinary:
                        for yp in ordinary:
                            target_union = {i: int(i in xp[0])+int(i in yp[0]) for i in range(n)}
                            if original_union == target_union:
                                assert fxy == int(xp[0] == odd)+int(yp[0] == odd)
                            if x[0] != xp[0]:
                                assert len(x[0]-xp[0]) == q
            cycles.append({"q":q,"L":length,"epsilon":epsilon,"colored_states":len(states),"Z":z,"beta":beta,"rare_pair_mass":eta,"variance":variance,"energy_upper_bound":universal_energy_bound,"comparison_lower_bound":forced_L_lower_bound})
    result = {"status":"PASS","arithmetic":"exact Fraction; every small determinant cross-checked by permutation expansion", "dense_family":dense,"coordinate_cycle_fixtures":cycles,"condition_number_certificate":"||F0^-1||2<=2; delta<=1/4 gives ||Fdelta^-1||2<=4, ||Fdelta||2<=17/4, hence kappa2<=17", "scope":"No mixing computation, FPRAS, or microscopic energy compiler; finite bookkeeping only", "wall_seconds":time.perf_counter()-started}
    target = Path(__file__).with_name("initial_checks.json")
    target.write_text(json.dumps(result,default=encode,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"dense_cases":len(dense),"cycle_cases":len(cycles),"wall_seconds":result["wall_seconds"],"result_path":str(target)}))


if __name__ == "__main__":
    main()
