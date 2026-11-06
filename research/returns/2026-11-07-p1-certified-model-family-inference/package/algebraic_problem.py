"""Emit the exact finite polynomial problem for a shared potential.

This module constructs and evaluates rational constraints. It does not
implement general real-algebraic quantifier elimination. The complete
algorithm in GENERAL_THEOREM.txt uses the standard charged CAD algorithm.
"""
from fractions import Fraction as Q


def const(x):
    return {(): Q(x)} if x else {}


def var(i):
    return {(i,): Q(1)}


def add(a, b):
    out = a.copy()
    for key, value in b.items():
        out[key] = out.get(key, Q(0))+value
        if out[key] == 0:
            del out[key]
    return out


def scale(a, value):
    return {k: v*value for k, v in a.items() if v*value}


def subtract(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = {}
    for i, v in a.items():
        for j, w in b.items():
            key = tuple(sorted(i+j))
            out[key] = out.get(key, Q(0))+v*w
    return {k: v for k, v in out.items() if v}


def dot(a, b):
    out = {}
    for x, y in zip(a, b):
        out = add(out, mul(x, y))
    return out


def linear_map(matrix, vector):
    out = []
    for row in matrix:
        p = {}
        for c, x in zip(row, vector):
            p = add(p, scale(x, Q(c)))
        out.append(p)
    return out


def evaluate(poly, assignment):
    result = Q(0)
    for indices, coefficient in poly.items():
        term = coefficient
        for i in indices:
            term *= assignment[i]
        result += term
    return result


class Problem:
    def __init__(self):
        self.names, self.constraints = [], []

    def variable(self, name):
        self.names.append(name)
        return var(len(self.names)-1)

    def vector(self, prefix, n):
        return [self.variable(prefix+'_'+str(i)) for i in range(n)]

    def ge(self, poly, name):
        self.constraints.append(('ge', poly, name))

    def eq(self, poly, name):
        self.constraints.append(('eq', poly, name))

    def interval(self, poly, lower, upper, name):
        self.ge(subtract(poly, const(lower)), name+'_lower')
        self.ge(subtract(const(upper), poly), name+'_upper')

    def verify_assignment(self, values):
        assignment = [Q(values[name]) for name in self.names]
        for sense, p, name in self.constraints:
            value = evaluate(p, assignment)
            if not (value == 0 if sense == 'eq' else value >= 0):
                raise ValueError((name, value))
        return True

    def document(self):
        return {
            'variables': self.names,
            'constraints': [
                {'sense': sense, 'name': name,
                 'polynomial': [{'indices': list(k), 'coefficient': str(v)}
                                for k, v in sorted(p.items())]}
                for sense, p, name in self.constraints],
            'maximum_degree': max((len(k) for _, p, _ in self.constraints
                                   for k in p), default=0),
            'solver_executed': False}


def compile_euler(A, B, C, mu, upper, initial_box, anchor_gradient_bound,
                  calibrations, steps, forcing):
    """Calibration rows are (x, gradient-box, value-box or None).

    One potential is used by all rows and all Euler nodes. steps is a
    list of positive rational step lengths; forcing lists one vector
    per step. The potential is gauged by V(0)=0.
    """
    mu, upper = Q(mu), Q(upper)
    if upper <= mu:
        raise ValueError('This compiler requires upper > mu')
    beta = upper-mu
    n, d = len(A), len(C)
    if not (n > 0 and d > 0 and len(B) == n and len(initial_box) == n
            and all(len(row) == n for row in A)
            and all(len(row) == d for row in B)
            and all(len(row) == n for row in C)
            and len(forcing) == len(steps)
            and all(len(row) == n for row in forcing)
            and all(Q(h) > 0 for h in steps)
            and Q(anchor_gradient_bound) >= 0):
        raise ValueError('Invalid dimensions, mesh, or anchor bound')
    if any(len(x) != d or len(gbox) != d for x, gbox, _ in calibrations):
        raise ValueError('Calibration dimension mismatch')
    anchor_gradient_bound = Q(anchor_gradient_bound)
    P = Problem()
    anchor_g = P.vector('anchor_g', d)
    samples = [([{} for _ in range(d)], anchor_g, {})]
    for j, g in enumerate(anchor_g):
        P.interval(g, -anchor_gradient_bound, anchor_gradient_bound, 'anchor_'+str(j))
    for i, (x, gbox, fbox) in enumerate(calibrations):
        gs = P.vector('cal_'+str(i)+'_g', d)
        fs = P.variable('cal_'+str(i)+'_f')
        for j, (g, limits) in enumerate(zip(gs, gbox)):
            P.interval(g, *map(Q, limits), 'cal_g_'+str(i)+'_'+str(j))
        if fbox is not None:
            P.interval(fs, *map(Q, fbox), 'cal_f_'+str(i))
        samples.append(([const(Q(a)) for a in x], gs, fs))
    states = [P.vector('z_'+str(k), n) for k in range(len(steps)+1)]
    for j, limits in enumerate(initial_box):
        P.interval(states[0][j], *map(Q, limits), 'initial_'+str(j))
    gradients = []
    for k, z in enumerate(states):
        gs = P.vector('node_'+str(k)+'_g', d)
        fs = P.variable('node_'+str(k)+'_f')
        gradients.append(gs)
        samples.append((linear_map(C, z), gs, fs))
    for k, h in enumerate(steps):
        az, bg = linear_map(A, states[k]), linear_map(B, gradients[k])
        for j in range(n):
            rhs = add(add(az[j], bg[j]), const(Q(forcing[k][j])))
            P.eq(subtract(subtract(states[k+1][j], states[k][j]), scale(rhs, Q(h))),
                 'euler_'+str(k)+'_'+str(j))
    for i, (xi, gi, fi) in enumerate(samples):
        for j, (xj, gj, fj) in enumerate(samples):
            if i == j:
                continue
            dx = [subtract(x, y) for x, y in zip(xi, xj)]
            ds = [subtract(subtract(x, y), scale(z, mu))
                  for x, y, z in zip(gi, gj, dx)]
            p = subtract(subtract(fi, fj), dot(gj, dx))
            p = subtract(p, scale(dot(dx, dx), mu/2))
            p = subtract(p, scale(dot(ds, ds), 1/(2*beta)))
            P.ge(p, 'shared_potential_'+str(i)+'_'+str(j))
    return P
