"""Exact finite gradient interpolation and a rational global potential.

The interpolation theorem and conjugate construction are due to Taylor,
Hendrickx and Glineur (2017). This is a small exact reference implementation.
No claim of a new interpolation theorem is made.
"""
from fractions import Fraction as Q
from itertools import combinations


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def norm2(x):
    return dot(x, x)


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def weight(xi, gi, xj, gj, mu, upper):
    beta = upper-mu
    assert beta > 0
    dx = sub(xi, xj)
    ds = tuple(a-b-mu*c for a, b, c in zip(gi, gj, dx))
    return dot(gj, dx)+mu*norm2(dx)/2+norm2(ds)/(2*beta)


def check_values(points, gradients, values, mu, upper):
    n = len(points)
    if not (n == len(gradients) == len(values) and n > 0 and upper > mu):
        raise ValueError('Invalid interpolation dimensions or curvature interval')
    d = len(points[0])
    if d < 1 or any(len(x) != d for x in list(points)+list(gradients)):
        raise ValueError('Interpolation dimension mismatch')
    slacks = []
    for i in range(n):
        for j in range(n):
            slack = values[i]-values[j]-weight(
                points[i], gradients[i], points[j], gradients[j], mu, upper)
            if slack < 0:
                return False, {'pair': (i, j), 'slack': slack}
            slacks.append(slack)
    return True, {'checked': n*n, 'minimum_slack': min(slacks)}


def complete_values(points, gradients, mu, upper):
    """Find compatible values, or return an exact positive-cycle witness.

    Inequalities are f[i] >= f[j]+weight(i,j). Bellman--Ford is run
    with the sign reversed and a zero-cost super-source.
    """
    n = len(points)
    if not (n > 0 and n == len(gradients) and upper > mu):
        raise ValueError('Invalid interpolation dimensions or curvature interval')
    d = len(points[0])
    if d < 1 or any(len(x) != d for x in list(points)+list(gradients)):
        raise ValueError('Interpolation dimension mismatch')
    weights = [[weight(points[i], gradients[i], points[j], gradients[j],
                       mu, upper) for j in range(n)] for i in range(n)]
    values = [Q(0)]*n
    parent = [-1]*n
    last = -1
    for iteration in range(n):
        last = -1
        for j in range(n):
            for i in range(n):
                candidate = values[j]+weights[i][j]
                if candidate > values[i]:
                    values[i] = candidate
                    parent[i] = j
                    last = i
        if last == -1:
            anchor = values[0]
            values = [v-anchor for v in values]
            ok, certificate = check_values(points, gradients, values, mu, upper)
            assert ok
            return {'feasible': True, 'values': values, 'certificate': certificate}
    v = last
    for _ in range(n):
        v = parent[v]
        assert v >= 0
    backwards = [v]
    u = parent[v]
    while u != v:
        backwards.append(u)
        u = parent[u]
        assert len(backwards) <= n+1
    backwards.append(v)
    cycle = list(reversed(backwards))
    total = sum((weights[j][i] for i, j in zip(cycle, cycle[1:])), Q(0))
    assert total > 0
    return {'feasible': False, 'cycle': cycle, 'cycle_weight': total}


def solve_unique(matrix, rhs):
    n = len(rhs)
    work = [list(map(Q, row))+[Q(y)] for row, y in zip(matrix, rhs)]
    for j in range(n):
        pivots = [i for i in range(j, n) if work[i][j]]
        if not pivots:
            return None
        i = pivots[0]
        work[i], work[j] = work[j], work[i]
        pivot = work[j][j]
        work[j] = [x/pivot for x in work[j]]
        for i in range(n):
            if i != j and work[i][j]:
                c = work[i][j]
                work[i] = [x-c*y for x, y in zip(work[i], work[j])]
    return [row[-1] for row in work]


class RationalPotential:
    """Global C^(1,1) interpolant; values and gradients at rational x are exact.

    h* = |s|^2/(2 beta) + max_i(a_i.s+b_i), V=h+mu |x|^2/2.
    Evaluating h uses finite active-face enumeration. Cost can be
    combinatorial in dimension and data size; it is not a free QP oracle.
    """
    def __init__(self, points, gradients, values, mu, upper):
        self.x = [tuple(map(Q, x)) for x in points]
        self.g = [tuple(map(Q, g)) for g in gradients]
        self.f = list(map(Q, values))
        self.mu, self.upper = Q(mu), Q(upper)
        self.beta = self.upper-self.mu
        if self.beta <= 0:
            raise ValueError('This evaluator requires a nondegenerate curvature interval')
        ok, _ = check_values(self.x, self.g, self.f, self.mu, self.upper)
        if not ok:
            raise ValueError('Inconsistent interpolation data')
        self.dimension = len(self.x[0])
        self.a, self.b = [], []
        for x, g, f in zip(self.x, self.g, self.f):
            si = tuple(u-self.mu*v for u, v in zip(g, x))
            hi = f-self.mu*norm2(x)/2
            self.a.append(tuple(v-u/self.beta for v, u in zip(x, si)))
            self.b.append(norm2(si)/(2*self.beta)-hi)

    def evaluate(self, x):
        x = tuple(map(Q, x))
        if len(x) != self.dimension:
            raise ValueError('Query dimension mismatch')
        n = len(self.x)
        attempts = 0
        for k in range(1, min(n, self.dimension+1)+1):
            for support in combinations(range(n), k):
                attempts += 1
                matrix = [[self.beta*dot(self.a[i], self.a[j]) for j in support]
                          + [Q(1)] for i in support]
                matrix.append([Q(1)]*k+[Q(0)])
                rhs = [self.beta*dot(self.a[i], x)+self.b[i] for i in support]+[Q(1)]
                answer = solve_unique(matrix, rhs)
                if answer is None:
                    continue
                alpha = answer[:k]
                if min(alpha) < 0:
                    continue
                mean_a = tuple(sum((alpha[j]*self.a[i][ell]
                                    for j, i in enumerate(support)), Q(0))
                               for ell in range(self.dimension))
                s = tuple(self.beta*(u-v) for u, v in zip(x, mean_a))
                heights = [dot(ai, s)+bi for ai, bi in zip(self.a, self.b)]
                maximum = max(heights)
                if any(heights[i] != maximum for j, i in enumerate(support)
                       if alpha[j]):
                    continue
                value = dot(x, s)-norm2(s)/(2*self.beta)-maximum+self.mu*norm2(x)/2
                gradient = tuple(u+self.mu*v for u, v in zip(s, x))
                return value, gradient, {
                    'support': support, 'weights': alpha, 'faces_tried': attempts}
        raise AssertionError('A convex-conjugate active face must exist')
