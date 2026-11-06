"""Exact rational reference implementation for the periodic certificate theorem.

The mathematical input includes a valid L1 Cauchy name and an exponential
moment bound. This program does NOT decide whether those promises are true.
All matrices and fields returned by a name are explicitly expanded. The
implementation is intentionally elementary, with no claim of fast scaling.
See RESEARCH_REPORT.txt for the convergence proof and resource contract.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product, permutations
from math import factorial


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def eye(d):
    return [[Q(i == j) for j in range(d)] for i in range(d)]


def inverse(a):
    """Exact elimination, including row pivoting. No numerical tolerances."""
    d = len(a)
    b = [[Q(x) for x in a[i]] + eye(d)[i] for i in range(d)]
    for j in range(d):
        p = next((i for i in range(j, d) if b[i][j]), None)
        if p is None:
            raise ValueError('Singular rational matrix')
        b[j], b[p] = b[p], b[j]
        q = b[j][j]
        b[j] = [x/q for x in b[j]]
        for i in range(d):
            if i != j and b[i][j]:
                q = b[i][j]
                b[i] = [x-q*y for x, y in zip(b[i], b[j])]
    return [row[d:] for row in b]


def is_spd(a):
    """Exact symmetric LDL test; the empty matrix is positive definite."""
    n = len(a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    l, diag = [[Q(0)]*n for _ in range(n)], []
    for j in range(n):
        z = a[j][j] - sum((l[j][k]**2*diag[k] for k in range(j)), Q(0))
        if z <= 0:
            return False
        diag.append(z)
        l[j][j] = Q(1)
        for i in range(j+1, n):
            l[i][j] = (a[i][j]-sum((l[i][k]*l[j][k]*diag[k]
                                    for k in range(j)), Q(0)))/z
    return True


class StepField:
    """An explicit rational box field on the uniform dyadic periodic grid.

    values[cube] is either a d-vector or a d by d matrix.
    error is a promised L1 operator-norm error (zero for exact finite data).
    """
    def __init__(self, d, level, values, error=Q(0)):
        self.d, self.level, self.values = d, level, values
        self.error = Q(error)
        if self.error < 0:
            raise ValueError('An error bound must be nonnegative')
        expected = set(product(range(2**level), repeat=d))
        if set(values) != expected:
            raise ValueError('All dyadic boxes must be explicitly supplied')

    def at(self, x):
        k = tuple(int(t*2**self.level) % (2**self.level) for t in x)
        return self.values[k]


def zero_source(d):
    return StepField(d, 0, {(0,)*d: [Q(0)]*d})


def symmetrize(a):
    vals = {box: [[(Q(v[i][j])+Q(v[j][i]))/2 for j in range(a.d)]
                  for i in range(a.d)] for box, v in a.values.items()}
    return StepField(a.d, a.level, vals, a.error)


def inverse_parameters(n, tau, moment):
    """Only integer/rational tests are used to allocate the three errors."""
    tau, moment = Q(tau), Q(moment)
    if tau <= 0 or moment <= 0:
        raise ValueError('Positive rational tau and moment are required')
    r = 1
    while True:
        radius = max(Q(1), Q(2*r)/tau)
        tail = moment*(radius+1/tau)*Q(1, 2**(2*r))
        if tail <= Q(1, 2**(n+2)):
            break
        r += 1
    k = 1
    while radius*Q(1, 2**k) > Q(1, 2**(n+2)):
        k += 1
    lipschitz = Q(k*(k+3), 4)*radius**2
    s = n
    while lipschitz*Q(1, 2**s) > Q(1, 2**(n+1)):
        s += 1
    return dict(n=n, r=r, radius=radius, k=k, source_precision=s,
                lipschitz=lipschitz, tail=tail,
                spectral_error=radius*Q(1, 2**k))


def rational_inverse_filter(s, radius, k):
    """R^2 S sum_{j=1}^k (I+R^2 S^2)^(-j), valid for symmetric S."""
    d = len(s)
    if any(s[i][j] != s[j][i] for i in range(d) for j in range(d)):
        raise ValueError('Symmetric matrix required')
    if all(s[i][j] == 0 for i in range(d) for j in range(d) if i != j):
        c = [[Q(0)]*d for _ in range(d)]
        for i in range(d):
            a = s[i][i]
            t = 1/(1+radius**2*a**2)
            c[i][i] = Q(0) if a == 0 else (1-t**k)/a
        return c
    square = mm(s, s)
    t = inverse([[Q(i == j)+radius**2*square[i][j]
                  for j in range(d)] for i in range(d)])
    power, total = eye(d), [[Q(0)]*d for _ in range(d)]
    for _ in range(k):
        power = mm(power, t)
        total = [[total[i][j]+power[i][j] for j in range(d)] for i in range(d)]
    return [[radius**2*v for v in row] for row in mm(s, total)]


def inverse_name(name, n, tau, moment):
    pars = inverse_parameters(n, tau, moment)
    a = name(pars['source_precision'])
    if a.error > Q(1, 2**pars['source_precision']):
        raise ValueError('Name did not return the requested error bound')
    vals = {}
    for box, raw in a.values.items():
        s = [[(Q(raw[i][j])+Q(raw[j][i]))/2 for j in range(a.d)]
             for i in range(a.d)]
        vals[box] = rational_inverse_filter(s, pars['radius'], pars['k'])
    err = pars['lipschitz']*a.error + pars['spectral_error']+pars['tail']
    assert err <= Q(1, 2**n)
    return StepField(a.d, a.level, vals, err), pars


@lru_cache(None)
def mesh(d, level):
    n = 2**level
    cells = []
    for cube in product(range(n), repeat=d):
        for perm in permutations(range(d)):
            v = list(cube)
            vertices = [tuple(v)]
            for axis in perm:
                v = v.copy()
                v[axis] = (v[axis]+1) % n
                vertices.append(tuple(v))
            frac = [Q(0)]*d
            for j, axis in enumerate(perm):
                frac[axis] = Q(d-j, d+1)
            centre = tuple((Q(cube[i])+frac[i])/n for i in range(d))
            cells.append((cube, perm, tuple(vertices), centre))
    return tuple(cells)


@lru_cache(None)
def mesh_index(d, level):
    return {(c, p): i for i, (c, p, _, _) in enumerate(mesh(d, level))}


def locate(x, d, level):
    n = 2**level
    cube = tuple(int(t*n) % n for t in x)
    frac = tuple(t*n-int(t*n) for t in x)
    perm = tuple(sorted(range(d), key=lambda i: (-frac[i], i)))
    return mesh_index(d, level)[(cube, perm)]


def independent_columns(columns):
    """Select original columns, preserving their small rational entries."""
    pivots, selected = {}, []
    for index, col in enumerate(columns):
        v = list(col)
        for p, basis in sorted(pivots.items()):
            z = v[p]
            if z:
                v = [a-z*b for a, b in zip(v, basis)]
        p = next((j for j, a in enumerate(v) if a), None)
        if p is not None:
            z = v[p]
            pivots[p] = [a/z for a in v]
            selected.append(index)
    return selected


@lru_cache(None)
def bases(d, level):
    n = 2**level
    nodes = tuple(product(range(n), repeat=d))
    gradients = []
    for node in nodes:
        field = []
        for _, perm, vertices, _ in mesh(d, level):
            g = [Q(0)]*d
            for j, axis in enumerate(perm):
                g[axis] = Q(n*(int(vertices[j+1] == node)-int(vertices[j] == node)))
            field.append(tuple(g))
        gradients.append(tuple(field))
    primal = tuple(gradients[1:])  # fix one nodal value, removing constants
    dual, ids = [], []
    for axis in range(d):
        dual.append(tuple(tuple(Q(i == axis) for i in range(d))
                          for _ in mesh(d, level)))
        ids.append(('constant', axis))
    for i in range(d):
        for j in range(i+1, d):
            for node, grad in zip(nodes, gradients):
                field = []
                for g in grad:
                    h = [Q(0)]*d
                    h[i], h[j] = g[j], -g[i]
                    field.append(tuple(h))
                dual.append(tuple(field))
                ids.append(('curl', i, j, node))
    columns = [[a for v in field for a in v] for field in dual]
    chosen = independent_columns(columns)
    return primal, tuple(dual[i] for i in chosen), tuple(ids[i] for i in chosen)


def assemble(basis, level, coefficient, source, e, dual=False):
    d, count = coefficient.d, len(basis)
    fine = max(level, coefficient.level, source.level)
    volume = Q(1, factorial(d)*2**(fine*d))
    gram = [[Q(0)]*count for _ in range(count)]
    linear = [Q(0)]*count
    for _, _, _, x in mesh(d, fine):
        index = locate(x, d, level)
        vectors = [list(field[index]) for field in basis]
        a, f = coefficient.at(x), source.at(x)
        transformed = [mv(a, v) for v in vectors]
        target = ([e[i]-mv(a, f)[i] for i in range(d)] if dual else
                  [mv(a, e)[i]-f[i] for i in range(d)])
        for i in range(count):
            linear[i] += volume*dot(vectors[i], target)
            for j in range(i+1):
                gram[i][j] += volume*dot(vectors[i], transformed[j])
    for i in range(count):
        for j in range(i):
            gram[j][i] = gram[i][j]
    return gram, linear


def combine(basis, coefficients, baseline, cell_count):
    d = len(baseline)
    return [tuple(baseline[j]+sum((c*field[i][j]
                   for c, field in zip(coefficients, basis)), Q(0))
                  for j in range(d)) for i in range(cell_count)]


def certificate(a, c, source, e, level, electric, conserved_flux):
    """Exact finite arithmetic; the two named L1 error promises are paid."""
    d = a.d
    fine = max(level, a.level, c.level, source.level)
    vol = Q(1, factorial(d)*2**(fine*d))
    primal, dual = Q(0), Q(0)
    max_e2, max_q2 = Q(0), Q(0)
    mean_b = [Q(0)]*d
    for _, _, _, x in mesh(d, fine):
        index = locate(x, d, level)
        ef, bf = electric[index], conserved_flux[index]
        f = source.at(x)
        q = [bf[i]+f[i] for i in range(d)]
        primal += vol*(dot(ef, mv(a.at(x), ef))-2*dot(f, ef))
        dual += vol*(2*dot(e, bf)-dot(q, mv(c.at(x), q)))
        max_e2, max_q2 = max(max_e2, dot(ef, ef)), max(max_q2, dot(q, q))
        mean_b = [mean_b[i]+vol*bf[i] for i in range(d)]
    upper, lower = primal+a.error*max_e2, dual-c.error*max_q2
    return dict(upper=upper, lower=lower, gap=upper-lower,
                approximate_primal=primal, approximate_dual=dual,
                coefficient_error=a.error, inverse_error=c.error,
                max_e_squared=max_e2, max_flux_plus_source_squared=max_q2,
                mean_conserved_flux=mean_b)


def solve_level(a, c, source, e, level):
    d = a.d
    g, h, ids = bases(d, level)
    ga, b = assemble(g, level, a, source, e)
    hc, v = assemble(h, level, c, source, e, dual=True)
    if not is_spd(ga) or not is_spd(hc):
        return None
    z = [-q for q in mv(inverse(ga), b)] if g else []
    y = mv(inverse(hc), v)
    ef = combine(g, z, e, len(mesh(d, level)))
    bf = combine(h, y, [Q(0)]*d, len(mesh(d, level)))
    cert = certificate(a, c, source, e, level, ef, bf)
    cert.update(dimension=d, mesh_level=level, potential_coefficients=z,
                flux_coefficients=y, flux_basis_ids=ids,
                electric_field=ef, conserved_flux=bf,
                primal_dimension=len(g), dual_dimension=len(h))
    return cert


def certified_solve(name, tau, moment, e, epsilon, source=None, max_stages=None):
    """Uniform deterministic loop on VALID names; theorem proves halting.

    max_stages is only an optional caller-imposed resource limit. Reaching it
    reports failure to certify, not nonexistence or a lower bound.
    """
    e, epsilon = [Q(x) for x in e], Q(epsilon)
    d = len(e)
    source = source or zero_source(d)
    if epsilon <= 0:
        raise ValueError('Positive error tolerance required')
    n = 1
    while max_stages is None or n <= max_stages:
        a = symmetrize(name(n))
        if a.d != d or source.d != d or source.error:
            raise ValueError('Dimension mismatch or inexact source representation')
        if a.error > Q(1, 2**n):
            raise ValueError('Invalid advertised error from coefficient name')
        c, pars = inverse_name(name, n, tau, moment)
        max_level = (n+1).bit_length()-1
        for level in range(max_level+1):
            result = solve_level(a, c, source, e, level)
            if result is not None and result['gap'] <= epsilon**2:
                if result['gap'] < 0:
                    raise ValueError('Negative bound gap: inconsistent supplied promises')
                result.update(stage=n, inverse_parameters=pars, epsilon=epsilon)
                return result
        n += 1
    raise RuntimeError('Resource limit reached without a certificate')


def serializable(obj):
    if isinstance(obj, Q):
        return f'{obj.numerator}/{obj.denominator}'
    if isinstance(obj, dict):
        return {str(k): serializable(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serializable(v) for v in obj]
    return obj
