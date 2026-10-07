#!/usr/bin/env python3
"""Independent small exact fixture for the root-origin projection posterior DP.

Scientific arithmetic is Fraction, integer and rational complex pairs only.
Direct local symmetrization is by averaging all computational strings of each
weight, not by importing the claimed combinatorial amplitude formula. Global
color assignment and density matrices are separately enumerated for M6.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import time

ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def conjugate(a):
    return a[0], -a[1]


def scale(a, b):
    return a[0]*b, a[1]*b


def phase(exponent):
    return (ONE, (Q(0), Q(1)), (Q(-1), Q(0)), (Q(0), Q(-1)))[exponent % 4]


def norm(vector):
    return sum((a*a+b*b for a, b in vector.values()), Q(0))


def direct_projection(colors, amplitude0, amplitude1, phase_quarters):
    m = len(colors)
    weight_sums = [ZERO for _ in range(m + 1)]
    for bits in product((0, 1), repeat=m):
        value = ONE
        for color, bit in zip(colors, bits):
            if color == 0:  # coherent latent color
                local = (amplitude0, Q(0)) if not bit else scale(phase(phase_quarters), amplitude1)
            elif color == 1:
                local = ONE if bit else ZERO
            else:
                local = ONE if not bit else ZERO
            value = mul(value, local)
        weight_sums[sum(bits)] = add(weight_sums[sum(bits)], value)
    result = {}
    for index in range(1 << m):
        ell = index.bit_count()
        value = scale(weight_sums[ell], Q(1, comb(m, ell)))
        if value != ZERO:
            result[index] = value
    return result


def analytic_projection(m, r, b, amplitude0, amplitude1, phase_quarters):
    result = {}
    for index in range(1 << m):
        ell = index.bit_count()
        t = ell - b
        if 0 <= t <= r:
            real = Q(comb(r, t), comb(m, ell)) * amplitude1**t * amplitude0**(r-t)
            value = scale(phase(t * phase_quarters), real)
            if value != ZERO:
                result[index] = value
    return result


def z_formula(m, r, b, x):
    return sum((Q(comb(r, t)**2, comb(m, b+t))*x**t*(1-x)**(r-t) for t in range(r+1)), Q(0))


def options(m, x):
    return [(r, b, comb(m, r)*comb(m-r, b), z_formula(m, r, b, x))
            for r in range(m+1) for b in range(m-r+1)]


def dp(groups, x):
    layers = [{(0, 0): Q(1)}]
    for m in groups:
        new = {}
        for (R, B), value in layers[-1].items():
            for r, b, count, z in options(m, x):
                key = (R+r, B+b)
                new[key] = new.get(key, Q(0)) + value * count * z
        layers.append(new)
    return layers


def quantize(probs, bits):
    assert probs and sum(probs, Q(0)) == 1 and all(p >= 0 for p in probs)
    D = 1 << bits
    weights = [p.numerator*D // p.denominator for p in probs[:-1]]
    weights.append(D - sum(weights))
    q = [Q(w, D) for w in weights]
    assert sum(q, Q(0)) == 1 and all(v >= 0 for v in q)
    TV = sum((abs(a-b) for a, b in zip(probs, q)), Q(0)) / 2
    assert TV <= Q(len(probs)-1, D)
    return q


def posterior(groups, x, layers, k, u, bits=None):
    result = {}
    def recurse(i, R, B, chosen, mass):
        if i == 0:
            assert R == B == 0
            result[tuple(reversed(chosen))] = mass
            return
        branch = []
        for r, b, count, z in options(groups[i-1], x):
            previous = layers[i-1].get((R-r, B-b), Q(0))
            if previous:
                branch.append(((r, b), count*z*previous/layers[i][R, B]))
        probabilities = [p for _, p in branch]
        assert sum(probabilities, Q(0)) == 1
        if bits is not None:
            probabilities = quantize(probabilities, bits)
        for ((r, b), _), p in zip(branch, probabilities):
            recurse(i-1, R-r, B-b, chosen+[(r, b)], mass*p)
    recurse(len(groups), k, u, [], Q(1))
    assert sum(result.values(), Q(0)) == 1
    return result


def tensor_vectors(vectors, groups):
    total = {0: ONE}
    for vector, m in zip(vectors, groups):
        total = {(i << m) | j: mul(a, b) for i, a in total.items() for j, b in vector.items()}
    return total


def rank_add(matrix, vector, weight):
    for i, a in vector.items():
        for j, b in vector.items():
            matrix[i, j] = add(matrix.get((i, j), ZERO), scale(mul(a, conjugate(b)), weight))


def matrix_equal(a, b):
    return all(a.get(key, ZERO) == b.get(key, ZERO) for key in set(a) | set(b))


def main():
    start = time.perf_counter()
    local_count = 0
    amplitudes = [(Q(1), Q(0)), (Q(0), Q(1)), (Q(3, 5), Q(4, 5)), (Q(5, 13), Q(12, 13))]
    for a0, a1 in amplitudes:
        assert a0*a0+a1*a1 == 1
        x = a1*a1
        for m in range(1, 5):
            for colors in product(range(3), repeat=m):
                r, b = colors.count(0), colors.count(1)
                z = z_formula(m, r, b, x)
                assert Q(1, comb(m, m//2)) <= z <= 1
                for quarter in (0, 1):
                    direct = direct_projection(colors, a0, a1, quarter)
                    assert direct == analytic_projection(m, r, b, a0, a1, quarter)
                    assert norm(direct) == z
                    local_count += 1
    groups, M = (2, 3, 1), 6
    DP_cases = posterior_paths = 0
    tables = {}
    for a0, a1 in amplitudes:
        x = a1*a1
        layers = dp(groups, x);tables[x] = layers
        brute = {}
        for colors in product(range(3), repeat=M):
            counts, offset, mass = [], 0, Q(1)
            for m in groups:
                local = colors[offset:offset+m];offset += m
                r, b = local.count(0), local.count(1);counts.append((r, b))
                mass *= z_formula(m, r, b, x)
            key = colors.count(0), colors.count(1)
            brute[key] = brute.get(key, Q(0)) + mass
        assert brute == layers[-1]
        for (k, u), W in layers[-1].items():
            s = W / (comb(M, k)*comb(M-k, u))
            assert Q(1, 1 << M) <= s <= 1
            post = posterior(groups, x, layers, k, u)
            for counts, p in post.items():
                exact = Q(1)
                for m, (r, b) in zip(groups, counts):
                    exact *= comb(m, r)*comb(m-r, b)*z_formula(m, r, b, x)
                assert p == exact/W
                posterior_paths += 1
            DP_cases += 1
    # Exact global density comparison against all ordered color assignments.
    density_reports = []
    a0, a1 = Q(3, 5), Q(4, 5);x = a1*a1;k,u = 2,2
    normalization = comb(M,k)*comb(M-k,u)
    for quarter in (0, 1):
        direct, grouped = {}, {}
        assignments = 0
        for colors in product(range(3), repeat=M):
            if colors.count(0) != k or colors.count(1) != u:
                continue
            offset, vectors = 0, []
            for m in groups:
                vectors.append(direct_projection(colors[offset:offset+m], a0, a1, quarter));offset += m
            rank_add(direct, tensor_vectors(vectors, groups), Q(1, normalization));assignments += 1
        for counts, p in posterior(groups, x, tables[x], k, u).items():
            vectors, mass = [], Q(1)
            for m,(r,b) in zip(groups, counts):
                colors=(0,)*r+(1,)*b+(2,)*(m-r-b)
                vectors.append(direct_projection(colors,a0,a1,quarter))
                mass *= comb(m,r)*comb(m-r,b)
            rank_add(grouped, tensor_vectors(vectors,groups), mass/normalization)
        assert assignments == normalization and matrix_equal(direct,grouped)
        trace = sum((direct.get((i,i),ZERO)[0] for i in range(1<<M)),Q(0))
        expected = tables[x][-1][k,u]/normalization
        assert trace == expected
        canonical = [(i,j,str(v[0]),str(v[1])) for (i,j),v in sorted(direct.items())]
        density_reports.append({'phase_quarters':quarter,'ordered_assignments':assignments,
                                'matrix_dimension':1<<M,'nonzero_entries':sum(v!=ZERO for v in direct.values()),
                                'projected_trace':str(trace),'exact_density_sha256':sha256(json.dumps(canonical).encode()).hexdigest()})
    # Finite-bit categorical output is approximate, with an executed exact TV bound.
    outer=[(Q(2,7),2,1,Q(16,25)),(Q(3,7),0,3,Q(0)),(Q(2,7),6,0,Q(144,169))]
    weights=[a*tables[x][-1][k,u]/(comb(M,k)*comb(M-k,u)) for a,k,u,x in outer]
    total=sum(weights,Q(0));assert total>=Q(1,1<<M)
    exact_outer=[w/total for w in weights];bits=16
    rounded_outer=quantize(exact_outer,bits)
    TV=Q(0)
    for exact_p,approx_p,(_,k,u,x) in zip(exact_outer,rounded_outer,outer):
        exact=posterior(groups,x,tables[x],k,u)
        approx=posterior(groups,x,tables[x],k,u,bits=bits)
        for counts in exact:
            TV+=abs(exact_p*exact[counts]-approx_p*approx[counts])/2
    bound=Q(len(outer)+sum((m+1)*(m+2)//2 for m in groups),1<<bits)
    assert TV<=bound
    result={'status':'PASS independent bounded exact projection/DP/output-distribution fixture',
            'utc':datetime.now(timezone.utc).isoformat(),'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'local_direct_projection_checks':local_count,'groups':groups,'M':M,
            'DP_cases':DP_cases,'posterior_paths_verified':posterior_paths,
            'global_density_reports':density_reports,'finite_bit_categorical_bits_per_decision':bits,
            'finite_bit_joint_TV_exact':str(TV),'finite_bit_joint_TV_bound':str(bound),
            'projection_rejection_attempts':0,
            'scope':'finite fixture; general proof, outer acquisition and native state preparation separate',
            'wall_seconds':time.perf_counter()-start}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','local_direct_projection_checks','DP_cases','posterior_paths_verified','finite_bit_joint_TV_bound','wall_seconds']},indent=2))


if __name__=='__main__':main()
