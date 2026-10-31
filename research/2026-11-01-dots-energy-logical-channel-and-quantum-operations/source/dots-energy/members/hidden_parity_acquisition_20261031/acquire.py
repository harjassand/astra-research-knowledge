"""Acquire edgewise parity gauges from local task spans, over Q.

The acquisition input contains graph incidences and observed local tensors only.
The hidden gauges used to make test data are never passed to acquire().
"""
import itertools
import json
import math
import random
import time
from pathlib import Path
import sympy as sp

I = sp.eye(2)
Z = sp.diag(1, -1)
X = sp.Matrix([[0, 1], [1, 0]])
EVEN = [0, 3, 5, 6]


def kron(ms):
    out = sp.Matrix([[1]])
    for m in ms:
        out = sp.kronecker_product(out, m)
    return out


def preserver_axis(basis, leg):
    """Return rational involution from a four-dimensional local parity space."""
    if basis.shape != (8, 4) or basis.rank() != 4:
        raise ValueError('need four independent local directions')
    annihilator = sp.Matrix.vstack(*[v.T for v in basis.T.nullspace()])
    columns = []
    for r in range(2):
        for c in range(2):
            elementary = sp.zeros(2)
            elementary[r, c] = 1
            matrices = [I, I, I]
            matrices[leg] = elementary
            columns.append(sp.Matrix(annihilator*kron(matrices)*basis).reshape(16, 1))
    constraints = sp.Matrix.hstack(*columns)
    null = constraints.nullspace()
    if len(null) != 2:
        raise ValueError('local leg-preserver algebra is not two-dimensional')
    a, b = [sp.Matrix(2, 2, list(v)) for v in null]
    j = sp.trace(b)*a-sp.trace(a)*b
    if j == sp.zeros(2):
        raise ValueError('no nonzero traceless generator')
    lam = -j.det()
    root = sp.sqrt(lam)
    if not root.is_Rational or root == 0:
        raise ValueError('parity axis does not split over Q')
    j /= root
    assert j*j == I and sp.trace(j) == 0
    return j


def local_parity(transformed_basis):
    nonzero_rows = [i for i in range(8) if any(transformed_basis.row(i))]
    ps = {i.bit_count() % 2 for i in nonzero_rows}
    if len(ps) != 1:
        raise ValueError('learned subspace is not a pure parity space')
    return ps.pop()


def validate_graph(incidence, edges):
    expected = [[] for _ in incidence]
    for e, pair in enumerate(edges):
        if len(pair) != 2:
            raise ValueError('each edge needs two endpoints')
        u, v = pair
        if not (0 <= u < len(incidence) and 0 <= v < len(incidence)) or u == v:
            raise ValueError('bad endpoint or unsupported self-loop')
        expected[u].append(e)
        expected[v].append(e)
    if any(len(es) != 3 or sorted(es) != sorted(expected[v]) for v, es in enumerate(incidence)):
        raise ValueError('each vertex needs exactly three correctly recorded ports')


def acquire(incidence, edges, observations):
    start = time.perf_counter()
    validate_graph(incidence, edges)
    n = len(incidence)
    bases, axes = {}, {}
    for v in range(n):
        cols = sp.Matrix.hstack(*[obs[v] for obs in observations]).columnspace()
        if len(cols) != 4:
            raise ValueError(f'vertex {v}: observed dimension is {len(cols)}, not four')
        basis = sp.Matrix.hstack(*cols)
        bases[v] = basis
        axes[v] = [preserver_axis(basis, leg) for leg in range(3)]
    certificate = assemble_certificate(incidence, edges, axes, bases)
    certificate.update(acquired_seconds=time.perf_counter()-start,
                       observed_tasks=len(observations), vertices=n,
                       local_linear_systems=3*n, edge_checks=len(edges))
    return certificate


def assemble_certificate(incidence, edges, axes, bases):
    n = len(incidence)
    gauges = [[None]*3 for _ in range(n)]
    for e, (u, v) in enumerate(edges):
        iu, iv = incidence[u].index(e), incidence[v].index(e)
        ju, jv = axes[u][iu], axes[v][iv]
        if jv != ju.T and jv != -ju.T:
            raise ValueError(f'edge {e}: endpoint parity axes are incompatible')
        plus = (ju-I).nullspace()[0]
        minus = (ju+I).nullspace()[0]
        g = sp.Matrix.hstack(plus, minus)
        gauges[u][iu], gauges[v][iv] = g, g.inv().T
    transforms = [kron([g.inv() for g in gs]) for gs in gauges]
    parity = [local_parity(transforms[v]*bases[v]) for v in range(n)]
    # Swap edge eigenvectors to make every vertex even, when total parity allows.
    seen, flips = set(), []
    for root in range(n):
        if root in seen:
            continue
        parent = {root: None}
        order = [root]
        seen.add(root)
        for u in order:
            for e in incidence[u]:
                a, b = edges[e]
                v = b if a == u else a
                if v not in seen:
                    seen.add(v)
                    parent[v] = (u, e)
                    order.append(v)
        for v in reversed(order[1:]):
            if parity[v]:
                u, e = parent[v]
                flips.append(e)
                parity[v] ^= 1
                parity[u] ^= 1
        if parity[root]:
            raise ValueError('component has globally odd parity; contraction is identically zero')
    for e in flips:
        u, v = edges[e]
        for w in (u, v):
            j = incidence[w].index(e)
            gauges[w][j] = gauges[w][j]*X
    transforms = [kron([g.inv() for g in gs]) for gs in gauges]
    for v in range(n):
        assert local_parity(transforms[v]*bases[v]) == 0
    for e, (u, v) in enumerate(edges):
        assert gauges[u][incidence[u].index(e)].T*gauges[v][incidence[v].index(e)] == I
    return dict(gauges=gauges, transforms=transforms)


def apply_certificate(certificate, tensors):
    if len(tensors) != len(certificate['transforms']):
        raise ValueError('wrong number of query tensors')
    result = []
    for v, tensor in enumerate(tensors):
        if tensor.shape != (8, 1):
            raise ValueError('each query tensor must have eight coefficients')
        x = certificate['transforms'][v]*tensor
        if any(x[i] != 0 for i in range(8) if i not in EVEN):
            raise ValueError(f'query tensor at vertex {v} lies outside certified family')
        result.append(x)
    return result


def save_certificate(certificate, incidence, edges, path):
    payload = dict(schema='paired-rational-parity-chart-v1', incidence=incidence,
                   edges=edges,
                   gauges=[[[str(x) for x in g] for g in gs]
                           for gs in certificate['gauges']])
    Path(path).write_text(json.dumps(payload, indent=2)+'\n')


def load_certificate(path, incidence, edges):
    from fractions import Fraction
    validate_graph(incidence, edges)
    payload = json.loads(Path(path).read_text())
    if (payload.get('schema') != 'paired-rational-parity-chart-v1' or
        payload.get('incidence') != incidence or
        payload.get('edges') != [list(e) for e in edges]):
        raise ValueError('stored certificate has a different graph or schema')
    raw = payload['gauges']
    if len(raw) != len(incidence) or any(len(gs) != 3 for gs in raw):
        raise ValueError('wrong chart size')
    gauges = []
    for gs in raw:
        row = []
        for entries in gs:
            if len(entries) != 4:
                raise ValueError('bad matrix size')
            vals = [Fraction(x) for x in entries]
            g = sp.Matrix(2, 2, [sp.Rational(x.numerator, x.denominator) for x in vals])
            if not g.det():
                raise ValueError('stored gauge is singular')
            row.append(g)
        gauges.append(row)
    for e, (u, v) in enumerate(edges):
        if gauges[u][incidence[u].index(e)].T*gauges[v][incidence[v].index(e)] != I:
            raise ValueError('stored edge duality failed')
    return dict(gauges=gauges, transforms=[kron([g.inv() for g in gs]) for gs in gauges])


def cube_graph():
    # A planar nested-square drawing; incidences are in counterclockwise order.
    points = [(-2, -2), (2, -2), (2, 2), (-2, 2),
              (-1, -1), (1, -1), (1, 1), (-1, 1)]
    edges = [(i, (i+1) % 4) for i in range(4)]
    edges += [(i+4, (i+1) % 4+4) for i in range(4)]
    edges += [(i, i+4) for i in range(4)]
    incidence = [[] for _ in points]
    for e, (a, b) in enumerate(edges):
        incidence[a].append(e)
        incidence[b].append(e)
    for u in range(len(points)):
        def angle(e):
            a, b = edges[e]
            v = b if a == u else a
            return math.atan2(points[v][1]-points[u][1], points[v][0]-points[u][0])
        incidence[u].sort(key=angle)
    return incidence, edges, points


def make_hidden(incidence, edges, seed=17):
    rng = random.Random(seed)
    gauges = [[None]*3 for _ in incidence]
    for e, (u, v) in enumerate(edges):
        # Rational unimodular matrices, densely mixing the edge coordinates.
        a, b, c = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)]
        g = sp.Matrix([[1, a], [0, 1]])*sp.Matrix([[1, 0], [b, 1]])*sp.Matrix([[1, c], [0, 1]])
        gauges[u][incidence[u].index(e)] = g
        gauges[v][incidence[v].index(e)] = g.inv().T
    return [kron(gs) for gs in gauges]


def generate_task(hidden_transforms, rng):
    raw, canonical = [], []
    for trans in hidden_transforms:
        x = sp.zeros(8, 1)
        for i in EVEN:
            x[i] = rng.randint(1, 9)
        canonical.append(x)
        raw.append(trans*x)
    return raw, canonical


def brute_contract(tensors, incidence, edges):
    answer = 0
    for assignment in range(1 << len(edges)):
        term = 1
        for v, es in enumerate(incidence):
            local = 0
            for e in es:
                local = 2*local+((assignment >> e) & 1)
            term *= tensors[v][local]
            if term == 0:
                break
        answer += term
    return answer


def main():
    incidence, edges, points = cube_graph()
    hidden = make_hidden(incidence, edges)
    rng = random.Random(110)
    observations = [generate_task(hidden, rng)[0] for _ in range(4)]
    certificate = acquire(incidence, edges, observations)
    save_certificate(certificate, incidence, edges, 'acquired_chart.json')
    results = []
    for _ in range(3):
        raw, canonical = generate_task(hidden, rng)
        acquired = apply_certificate(certificate, raw)
        zraw = brute_contract(raw, incidence, edges)
        zcanonical = brute_contract(canonical, incidence, edges)
        zacquired = brute_contract(acquired, incidence, edges)
        assert zraw == zcanonical == zacquired
        results.append(str(zraw))
    tampered = [sp.MutableDenseMatrix(t) for t in raw]
    tampered[0][0] += 1
    try:
        apply_certificate(certificate, tampered)
        raise AssertionError('tampered task was wrongly accepted')
    except ValueError:
        pass
    summary = {k:v for k,v in certificate.items() if k not in ('gauges','transforms')}
    summary.update(exact_new_task_partition_sums=results, tampered_query_rejected=True,
                   hidden_gauges_supplied_to_acquisition=False)
    Path('acquisition_results.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
