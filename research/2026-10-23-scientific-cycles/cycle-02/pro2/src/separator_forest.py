"""Exact direct recovery on a graph whose supplied separator leaves a forest.

Rows of the query seed are coordinate vectors, so every row has energy one.
This module has no numerical solver and does not find a minimum separator.
The caller supplies the support and the separator; construction validates them.
All arithmetic can be fractions.Fraction.  No dense n-by-n matrix is needed.
"""
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Design:
    n: int
    edges: tuple
    separator: tuple
    colors: tuple
    parents: tuple
    q: int


def design(n, edges, separator=()):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    sep = tuple(sorted(separator))
    if len(set(sep)) != len(sep) or any(not isinstance(v, int) or not 0 <= v < n for v in sep):
        raise ValueError("invalid separator")
    S = set(sep)
    canonical = set()
    adj = [[] for _ in range(n)]
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("edges must have two endpoints")
        i, j = edge
        if not isinstance(i, int) or not isinstance(j, int) or not 0 <= i < n or not 0 <= j < n or i == j:
            raise ValueError("invalid off-diagonal edge")
        i, j = min(i, j), max(i, j)
        if (i, j) in canonical:
            raise ValueError("duplicate edge")
        canonical.add((i, j))
        if i not in S and j not in S:
            adj[i].append(j)
            adj[j].append(i)
    colors = [-1] * n
    parents = [-1] * n
    for c, v in enumerate(sep):
        colors[v] = c
    s = len(sep)
    for root in range(n):
        if colors[root] != -1:
            continue
        colors[root] = s
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if w == parents[v]:
                    continue
                if colors[w] != -1:
                    raise ValueError("removing separator does not leave a forest")
                parents[w] = v
                colors[w] = s + (colors[v] - s + 1) % 3
                queue.append(w)
    return Design(n, tuple(sorted(canonical)), sep, tuple(colors), tuple(parents), s + 3)


def seed(plan, one=1, zero=0):
    """Optional explicit n-by-q seed. The colors are its O(n) encoding."""
    return [[one if c == plan.colors[i] else zero for c in range(plan.q)] for i in range(plan.n)]


def action(plan, coefficients):
    """Simulated exact D X for an explicitly supplied sparse D (test utility).

    coefficients maps upper-triangle (i,j), including diagonals, to values.
    This is actual action work, not a replacement for oracle action charges.
    """
    allowed = set(plan.edges) | {(i, i) for i in range(plan.n)}
    if any(key not in allowed for key in coefficients):
        raise ValueError("coefficient outside support")
    Y = [[0 for _ in range(plan.q)] for _ in range(plan.n)]
    for (i, j), value in coefficients.items():
        Y[i][plan.colors[j]] += value
        if i != j:
            Y[j][plan.colors[i]] += value
    return Y


def selected_cells(plan):
    """Map each coefficient to its one selected cell, or two averaged cells."""
    S = set(plan.separator)
    cells = {(i, i): ((i, plan.colors[i]),) for i in range(plan.n)}
    for i, j in plan.edges:
        if i in S and j in S:
            cells[(i, j)] = ((i, plan.colors[j]), (j, plan.colors[i]))
        elif i in S:
            cells[(i, j)] = ((j, plan.colors[i]),)
        elif j in S:
            cells[(i, j)] = ((i, plan.colors[j]),)
        elif plan.parents[i] == j:
            cells[(i, j)] = ((i, plan.colors[j]),)
        elif plan.parents[j] == i:
            cells[(i, j)] = ((j, plan.colors[i]),)
        else:
            raise AssertionError("forest orientation inconsistency")
    return cells


def decode(plan, measured):
    """Sparse symmetric recovery; arbitrary action error is permitted.

    ||error||F <= sqrt(2)||E||F.
    ||error||2 <= sqrt(3/2)||E||F if s=0, else sqrt(5/3)||E||F.
    The operator constants are sharp for this specified decoder over the class.
    """
    if len(measured) != plan.n or any(len(row) != plan.q for row in measured):
        raise ValueError("action shape mismatch")
    ans = {}
    for key, cells in selected_cells(plan).items():
        values = [measured[i][j] for i, j in cells]
        ans[key] = values[0] if len(values) == 1 else (values[0] + values[1]) / 2
    return ans


def frobenius_squared(coefficients):
    return sum((1 if i == j else 2) * value * value for (i, j), value in coefficients.items())
