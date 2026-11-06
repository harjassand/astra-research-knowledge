"""Certified acquisition and composition of finite static quadratic port laws.

The source contract is explicit: calibrated scalar port-energy records and a
warranted positive lower spectral scale in fixed port coordinates. The compiler
uses only the acquired intervals. It does not identify microscopic coefficients.
All matrix computations use exact rational arithmetic. No physical experiment
is performed by this file. See RESEARCH_REPORT.txt for proofs and resource costs.
"""
from fractions import Fraction as Q


def qtree(obj):
    if isinstance(obj, Q):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): qtree(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [qtree(v) for v in obj]
    return obj


class Arithmetic:
    """Counts arithmetic in the explicitly instrumented matrix kernels only."""
    def __init__(self):
        self.counts = dict(add=0, sub=0, mul=0, div=0)
        self.maximum_fraction_bits = 1

    def observe(self, value):
        if isinstance(value, (list, tuple)):
            for item in value:
                self.observe(item)
        else:
            value = Q(value)
            self.maximum_fraction_bits = max(self.maximum_fraction_bits,
                abs(value.numerator).bit_length(), value.denominator.bit_length())
        return value

    def add(self, a, b):
        self.counts['add'] += 1
        return self.observe(a+b)

    def sub(self, a, b):
        self.counts['sub'] += 1
        return self.observe(a-b)

    def mul(self, a, b):
        self.counts['mul'] += 1
        return self.observe(a*b)

    def div(self, a, b):
        self.counts['div'] += 1
        return self.observe(a/b)

    def record(self):
        return dict(operations=self.counts.copy(),
                    total_operations=sum(self.counts.values()),
                    maximum_fraction_bits=self.maximum_fraction_bits,
                    scope='instrumented rational matrix kernels; not all Python instructions')


def zeros(n, m=None):
    m = n if m is None else m
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rational_matrix(a):
    return [list(map(Q, row)) for row in a]


def add(a, b, meter=None):
    meter = meter or Arithmetic()
    return [[meter.add(x, y) for x, y in zip(r, s)] for r, s in zip(a, b)]


def sub(a, b, meter=None):
    meter = meter or Arithmetic()
    return [[meter.sub(x, y) for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(c, a, meter=None):
    meter = meter or Arithmetic()
    return [[meter.mul(Q(c), x) for x in row] for row in a]


def matmul(a, b, meter=None):
    meter = meter or Arithmetic()
    if not a:
        return []
    if not b:
        raise ValueError('Use an explicit zero matrix for empty products')
    assert len(a[0]) == len(b)
    out = zeros(len(a), len(b[0]))
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                out[i][j] = meter.add(out[i][j], meter.mul(a[i][k], b[k][j]))
    return out


def quadratic(a, v, meter=None):
    meter = meter or Arithmetic()
    s = Q(0)
    for i in range(len(v)):
        for j in range(len(v)):
            s = meter.add(s, meter.mul(meter.mul(Q(v[i]), a[i][j]), Q(v[j])))
    return s


def outer(v, weight=Q(1), meter=None):
    meter = meter or Arithmetic()
    return [[meter.mul(Q(weight), meter.mul(Q(x), Q(y))) for y in v] for x in v]


def psd_certificate(a, strict=False, meter=None):
    """Exact symmetric pivoted elimination, including singular PSD matrices."""
    meter = meter or Arithmetic()
    a = rational_matrix(a)
    n = len(a)
    assert all(len(row) == n for row in a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError('Matrix must be symmetric')
    meter.observe(a)
    labels = list(range(n)); pivots = []
    while a:
        if any(a[j][j] < 0 for j in range(len(a))):
            raise ValueError('Matrix is not positive semidefinite')
        p = next((j for j in range(len(a)) if a[j][j] > 0), None)
        if p is None:
            if any(x for row in a for x in row):
                raise ValueError('Nonzero matrix with zero PSD diagonal')
            break
        pivot = a[p][p]
        pivots.append(dict(coordinate=labels[p], pivot=pivot))
        keep = [j for j in range(len(a)) if j != p]
        a = [[meter.sub(a[i][j], meter.div(meter.mul(a[i][p], a[p][j]), pivot))
              for j in keep] for i in keep]
        labels = [labels[j] for j in keep]
    if strict and len(pivots) != n:
        raise ValueError('Matrix is not positive definite')
    return dict(dimension=n, rank=len(pivots), positive_definite=len(pivots) == n,
                pivots=pivots, residual_zero_coordinates=labels)


def solve_consistent(a, rhs, meter=None):
    """Rational RREF; free coordinates are set to zero. Multiple RHS allowed."""
    meter = meter or Arithmetic()
    a = rational_matrix(a); rhs = rational_matrix(rhs)
    n = len(a)
    if not n:
        return []
    assert len(rhs) == n
    cols = len(a[0]); rcols = len(rhs[0])
    aug = [row + r for row, r in zip(a, rhs)]
    meter.observe(aug)
    rank = 0; pivots = []
    for col in range(cols):
        pivot = next((i for i in range(rank, n) if aug[i][col]), None)
        if pivot is None:
            continue
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        v = aug[rank][col]
        aug[rank] = [meter.div(x, v) for x in aug[rank]]
        for i in range(n):
            if i != rank and aug[i][col]:
                v = aug[i][col]
                aug[i] = [meter.sub(x, meter.mul(v, y))
                          for x, y in zip(aug[i], aug[rank])]
        pivots.append(col); rank += 1
        if rank == n:
            break
    if any(any(row[cols:]) for row in aug[rank:]):
        raise ValueError('Inconsistent linear equations')
    solution = zeros(cols, rcols)
    for i, col in enumerate(pivots):
        solution[col] = aug[i][cols:]
    return solution


def schur_psd(a, ports, meter=None, verify=True):
    """Return exact port law and a linear minimizing lift, no inverse oracle."""
    meter = meter or Arithmetic()
    a = rational_matrix(a); n = len(a); p = int(ports)
    assert 1 <= p <= n
    if verify:
        psd_certificate(a, meter=meter)
    upper = [row[:p] for row in a[:p]]
    if p == n:
        return upper, []
    h = [row[p:] for row in a[p:]]
    b = [row[:p] for row in a[p:]]
    x = solve_consistent(h, b, meter)
    law = sub(upper, matmul(transpose(b), x, meter), meter)
    lift = scale(-1, x, meter)
    return law, lift


def infinity_norm(a):
    return max((sum(abs(x) for x in row) for row in a), default=Q(0))


def acquire_law(reader, ports, alpha, delta):
    """Exactly p(p+1)/2 calibrated scalar energy queries; alpha is a promise."""
    p = int(ports); alpha = Q(alpha); delta = Q(delta)
    assert p >= 1 and alpha > 0 and 0 < delta <= 1
    eps = delta*alpha/(2*(1+delta))
    radius = eps/(2*p)
    k = zeros(p); entries = zeros(p); records = []
    diagonal = []
    for i in range(p):
        v = [Q(int(i == j)) for j in range(p)]
        r = reader(v, radius)
        assert 0 <= r['error'] <= radius
        records.append(r); diagonal.append(r)
        k[i][i] = r['mid']; entries[i][i] = r['error']
    for i in range(p):
        for j in range(i+1, p):
            v = [Q(int(h == i or h == j)) for h in range(p)]
            r = reader(v, radius)
            assert 0 <= r['error'] <= radius
            records.append(r)
            k[i][j] = k[j][i] = (r['mid']-diagonal[i]['mid']-diagonal[j]['mid'])/2
            entries[i][j] = entries[j][i] = (r['error']+diagonal[i]['error']+diagonal[j]['error'])/2
    actual_op_bound = infinity_norm(entries)
    assert actual_op_bound <= eps
    lower = sub(k, scale(eps, eye(p)))
    upper = add(k, scale(eps, eye(p)))
    cert_l = psd_certificate(lower, strict=True)
    cert_width = psd_certificate(sub(scale(1+delta, lower), upper))
    return dict(ports=p, alpha=alpha, delta=delta, gamma=1+delta,
                matrix_padding=eps, requested_scalar_radius=radius,
                reconstructed=k, entry_error_bounds=entries,
                operator_error_bound=actual_op_bound, lower=lower, upper=upper,
                lower_positive_certificate=cert_l,
                relative_width_certificate=cert_width, records=records)


def assemble(laws, placements, known, meter=None):
    """known + sum(T_a^T K_type(a) T_a); complete explicit maps are input."""
    meter = meter or Arithmetic()
    out = rational_matrix(known); n = len(out)
    psd_certificate(out, meter=meter)
    for item in placements:
        law = laws[item['type']]
        t = rational_matrix(item['map'])
        assert len(t) == len(law) and all(len(row) == n for row in t)
        out = add(out, matmul(transpose(t), matmul(law, t, meter), meter), meter)
    return out


def compile_interval(library, placements, known, ports, meter=None):
    meter = meter or Arithmetic()
    lower = assemble({key: item['lower'] for key, item in library.items()},
                     placements, known, meter)
    upper = assemble({key: item['upper'] for key, item in library.items()},
                     placements, known, meter)
    gamma = max((library[item['type']]['gamma'] for item in placements), default=Q(1))
    fl, yl = schur_psd(lower, ports, meter)
    fu, yu = schur_psd(upper, ports, meter)
    cert_order = psd_certificate(sub(fu, fl, meter), meter=meter)
    cert_width = psd_certificate(sub(scale(gamma, fl, meter), fu, meter), meter=meter)
    return dict(lower_matrix=lower, upper_matrix=upper, lower_response=fl,
                upper_response=fu, lower_minimizing_lift=yl,
                upper_minimizing_lift=yu, gamma=gamma,
                order_certificate=cert_order, relative_width_certificate=cert_width)


def robust_design(lower_base, directions, ports, loading, vertices, epsilon,
                  price=None):
    """Normalize NEW passive directions, then use unchanged accepted solver.

    Input vertices are explicit and nonnegative. The lower baseline is SPD.
    The output solves the worst-case problem for the declared Loewner rectangle.
    All ensuing scalar calls are constructed finite digital computations.
    """
    from predecessor_intervention import ellipsoid_design, finite_quadratic_reader
    base = rational_matrix(lower_base); n = len(base)
    psd_certificate(base, strict=True)
    directions = [rational_matrix(c) for c in directions]
    k = len(directions)
    assert k >= 1
    for c in directions:
        assert len(c) == n and all(len(row) == n for row in c)
        psd_certificate(c)
    vertices = [list(map(Q, v)) for v in vertices]
    assert vertices and all(len(v) == k and min(v) >= 0 for v in vertices)
    price = list(map(Q, price or [0]*k))
    assert len(price) == k
    loading = list(map(Q, loading)); assert len(loading) == ports
    total = zeros(n)
    for c in directions:
        total = add(total, c)
    largest_setting = max(x for v in vertices for x in v)
    w = infinity_norm(total)
    if not w or not largest_setting:
        u = min(vertices, key=lambda v: sum(c*x for c, x in zip(price, v)))
        f, lift = schur_psd(base, ports)
        value = quadratic(f, loading)-sum(c*x for c, x in zip(price, u))
        return dict(actuation=u, gap_upper=Q(0), value_interval=[value, value],
                    optimum_interval=[value, value], model_evaluations=0,
                    trivial=True)
    inv = solve_consistent(base, eye(n))
    mu = 1/infinity_norm(inv)
    t = max(Q(1), w/mu)
    b = largest_setting/2 + 1/t
    r = largest_setting/(2*b)
    center = add(base, scale(largest_setting/2, total))
    scaled = [scale(b, c) for c in directions]
    psd_certificate(sub(center, scale(b, total)))
    theta_vertices = [[(x-largest_setting/2)/b for x in v] for v in vertices]
    upper_energy = quadratic([row[:ports] for row in center[:ports]], loading)
    reader, model_records = finite_quadratic_reader(center, scaled, ports)
    cert = ellipsoid_design(reader, theta_vertices, loading, r, upper_energy,
                            Q(epsilon), price=[b*x for x in price])
    u = [largest_setting/2 + b*x for x in cert['theta']]
    offset = largest_setting*sum(price)/2
    task_bound = max(quadratic([row[:ports] for row in add(base,
                      sum_matrices([scale(x, c) for x, c in zip(v, directions)], n))[:ports]],
                      loading) for v in vertices)
    return dict(actuation=u, gap_upper=cert['gap_upper'],
                value_interval=[x-offset for x in cert['value_interval']],
                optimum_interval=[x-offset for x in cert['optimum_interval']],
                lower_energy_task_bound=task_bound, normalization=dict(mu=mu, W=w,
                    T=t, R=largest_setting, b=b, r=r, objective_offset=offset),
                model_evaluations=len(model_records), source_experiments=0,
                solver_certificate=cert, model_records=model_records)


def sum_matrices(matrices, n):
    out = zeros(n)
    for m in matrices:
        out = add(out, m)
    return out
