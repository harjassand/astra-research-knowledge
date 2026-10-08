"""Dyadic + cycle-signing sampler for rational bipartite PM marginals.

This exact-rational wrapper implements the graph, residual-rounding, and
dyadic-coarsening steps.  `signer` is the deterministic rational Li signing
algorithm from arXiv:2609.30044v1: on columns of Euclidean norm at most one,
it must return signs with infinity discrepancy < 99.  The wrapper checks the
returned signing's discrepancy exactly.  It does not embed or reimplement Li's
published signing procedure.

Input edges are labelled by indices into `edges`; each edge is `(left,right)`.
`feature_columns[e]` is the rational feature vector attached to that actual
edge and must have Euclidean norm at most one.

The output is a single perfect matching sampled from a finite rational law.
The law's exact marginal is the supplied vector; its pathwise feature error is
bounded by `|E|*2^-T + 99*sum_t 2^-t U_t` for that run's cycle scales U_t.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Callable, Sequence


Edge = tuple[int, int]
Vector = tuple[Fraction, ...]
RandBelow = Callable[[int], int]
Signer = Callable[[Sequence[Vector]], Sequence[int]]
GetRandBits = Callable[[int], int]


@dataclass(frozen=True)
class Cycle2Sample:
    matching_edge_ids: tuple[int, ...]
    feature_error: Vector
    initial_residual_bound: Fraction
    cycle_scales: tuple[tuple[int, int], ...]  # (dyadic level t, U_t)
    path_bound: Fraction


def fair_bit_randbelow(bound: int, getrandbits: GetRandBits) -> int:
    """Exact uniform integer in [0,bound), using rejection from fair bits."""
    if bound < 1:
        raise ValueError("bound must be positive")
    if bound == 1:
        return 0
    nbits = (bound - 1).bit_length()
    while True:
        value = getrandbits(nbits)
        if 0 <= value < bound:
            return value


def _bernoulli(probability: Fraction, randbelow: RandBelow) -> int:
    if not 0 <= probability <= 1:
        raise ValueError("probability must lie in [0,1]")
    q = probability.denominator
    draw = randbelow(q)
    if not 0 <= draw < q:
        raise ValueError("randbelow(q) must return an integer in [0,q)")
    return int(draw < probability.numerator)


def _global_endpoints(n_left: int, edge: Edge) -> tuple[int, int]:
    left, right = edge
    return left, n_left + right


def _find_cycle(
    n_vertices: int,
    n_left: int,
    edges: Sequence[Edge],
    active_edge_ids: Sequence[int],
) -> tuple[int, ...] | None:
    """Find one simple undirected cycle, returning edge IDs in cyclic order."""
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n_vertices)]
    for edge_id in active_edge_ids:
        u, v = _global_endpoints(n_left, edges[edge_id])
        adjacency[u].append((edge_id, v))
        adjacency[v].append((edge_id, u))
    for row in adjacency:
        row.sort()

    state = [0] * n_vertices  # 0 unseen, 1 active DFS stack, 2 finished
    parent = [-1] * n_vertices
    parent_edge = [-1] * n_vertices
    for root in range(n_vertices):
        if state[root]:
            continue
        state[root] = 1
        stack: list[tuple[int, int]] = [(root, 0)]
        while stack:
            u, offset = stack[-1]
            if offset >= len(adjacency[u]):
                state[u] = 2
                stack.pop()
                continue
            edge_id, v = adjacency[u][offset]
            stack[-1] = (u, offset + 1)
            if edge_id == parent_edge[u]:
                continue
            if state[v] == 0:
                parent[v] = u
                parent_edge[v] = edge_id
                state[v] = 1
                stack.append((v, 0))
            elif state[v] == 1:
                # In undirected DFS, a non-parent active neighbor is an ancestor.
                path: list[int] = []
                current = u
                while current != v:
                    if current < 0 or parent[current] < 0:
                        raise ArithmeticError("DFS back edge did not close a cycle")
                    path.append(parent_edge[current])
                    current = parent[current]
                return tuple(list(reversed(path)) + [edge_id])
    return None


def _cycle_interval(
    residual: Sequence[Fraction], cycle: Sequence[int]
) -> tuple[Fraction, Fraction, tuple[int, ...]]:
    if len(cycle) % 2:
        raise ArithmeticError("a bipartite cycle must have even length")
    signs = tuple(1 if i % 2 == 0 else -1 for i in range(len(cycle)))
    lower: Fraction | None = None
    upper: Fraction | None = None
    for edge_id, direction in zip(cycle, signs):
        value = residual[edge_id]
        if not 0 < value < 1:
            raise ArithmeticError("cycle rounding received an integral edge")
        if direction > 0:
            lo, hi = -value, 1 - value
        else:
            lo, hi = value - 1, value
        lower = lo if lower is None else max(lower, lo)
        upper = hi if upper is None else min(upper, hi)
    if lower is None or upper is None or not lower < 0 < upper:
        raise ArithmeticError("fractional cycle has no two-sided feasible move")
    return lower, upper, signs


def _initial_residual_bmatching(
    n_left: int,
    n_right: int,
    edges: Sequence[Edge],
    x: Sequence[Fraction],
    level: int,
    randbelow: RandBelow,
) -> tuple[int, ...]:
    """Sample integer degree-2^level b-matchings with exact mean 2^level*x.

    First floor each scaled edge value.  The remaining fractional values have
    integer degrees.  Alternating-cycle endpoint moves round this residual
    fractional b-matching to an integral one, preserving every edge mean.
    """
    n_vertices = n_left + n_right
    b = 1 << level
    scaled = tuple(value * b for value in x)
    floors = [value.numerator // value.denominator for value in scaled]
    residual = [value - floor for value, floor in zip(scaled, floors)]

    while True:
        fractional = [e for e, value in enumerate(residual) if 0 < value < 1]
        if not fractional:
            break
        cycle = _find_cycle(n_vertices, n_left, edges, fractional)
        if cycle is None:
            raise ArithmeticError("integer residual degrees imply a cycle, but none was found")
        lower, upper, directions = _cycle_interval(residual, cycle)
        width = upper - lower
        probability_lower = upper / width
        step = lower if _bernoulli(probability_lower, randbelow) else upper
        for edge_id, direction in zip(cycle, directions):
            residual[edge_id] += step * direction
            if not 0 <= residual[edge_id] <= 1:
                raise ArithmeticError("cycle endpoint move left [0,1]")

    if any(value not in (0, 1) for value in residual):
        raise ArithmeticError("initial cycle rounder did not become integral")
    y = tuple(floor + int(value) for floor, value in zip(floors, residual))
    if not _has_degrees(n_left, n_right, edges, y, b):
        raise ArithmeticError("initial rounded b-matching has incorrect degrees")
    return y


def _has_degrees(
    n_left: int,
    n_right: int,
    edges: Sequence[Edge],
    multiplicities: Sequence[int],
    target: int,
) -> bool:
    degree = [0] * (n_left + n_right)
    for (left, right), value in zip(edges, multiplicities):
        if value < 0:
            return False
        degree[left] += value
        degree[n_left + right] += value
    return all(value == target for value in degree)


def _decompose_into_cycles(
    n_left: int,
    n_right: int,
    edges: Sequence[Edge],
    active_edge_ids: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Decompose an Eulerian bipartite edge set into edge-disjoint cycles."""
    active = set(active_edge_ids)
    cycles: list[tuple[int, ...]] = []
    while active:
        cycle = _find_cycle(n_left + n_right, n_left, edges, tuple(sorted(active)))
        if cycle is None:
            raise ArithmeticError("nonempty Eulerian edge set has no cycle")
        if len(cycle) % 2:
            raise ArithmeticError("odd cycle found in a bipartite graph")
        cycles.append(cycle)
        active.difference_update(cycle)
    return tuple(cycles)


def _ceil_sqrt_fraction(value: Fraction) -> int:
    if value < 0:
        raise ValueError("squared norm must be nonnegative")
    u = isqrt(value.numerator // value.denominator)
    if u * u * value.denominator < value.numerator:
        u += 1
    return u


def _coarsen_one_level(
    n_left: int,
    n_right: int,
    edges: Sequence[Edge],
    y: Sequence[int],
    level: int,
    feature_columns: Sequence[Vector],
    randbelow: RandBelow,
    signer: Signer,
) -> tuple[tuple[int, ...], int]:
    """Coarsen a degree-2^level b-matching to degree 2^(level-1)."""
    odd_edges = [edge_id for edge_id, value in enumerate(y) if value % 2]
    cycles = _decompose_into_cycles(n_left, n_right, edges, odd_edges)
    if not cycles:
        half = tuple(value // 2 for value in y)
        if not _has_degrees(n_left, n_right, edges, half, 1 << (level - 1)):
            raise ArithmeticError("even numerator halving changed the degrees")
        return half, 0

    cycle_vectors: list[Vector] = []
    for cycle in cycles:
        row = [Fraction(0)] * (len(feature_columns[0]) if feature_columns else 0)
        for position, edge_id in enumerate(cycle):
            direction = 1 if position % 2 == 0 else -1
            for coordinate, entry in enumerate(feature_columns[edge_id]):
                row[coordinate] += direction * entry
        cycle_vectors.append(tuple(row))

    max_sq_norm = max(
        (sum((entry * entry for entry in column), Fraction(0)) for column in cycle_vectors),
        default=Fraction(0),
    )
    scale = _ceil_sqrt_fraction(max_sq_norm)
    if scale == 0:
        signs = (1,) * len(cycles)
    else:
        normalized = tuple(
            tuple(entry / scale for entry in column) for column in cycle_vectors
        )
        signs = tuple(signer(normalized))
        if len(signs) != len(cycles) or any(sign not in (-1, 1) for sign in signs):
            raise ValueError("signer must return one +/-1 sign per cycle")
        signed_sum = tuple(
            sum((sign * column[j] for sign, column in zip(signs, cycle_vectors)), Fraction(0))
            for j in range(len(cycle_vectors[0]))
        )
        if any(abs(value) > 99 * scale for value in signed_sum):
            raise ValueError("signer failed the required infinity-discrepancy bound")

    orientation = 1 if _bernoulli(Fraction(1, 2), randbelow) else -1
    updated = list(y)
    for sign, cycle in zip(signs, cycles):
        for position, edge_id in enumerate(cycle):
            delta = 1 if position % 2 == 0 else -1
            updated[edge_id] += orientation * sign * delta
    if any(value < 0 or value % 2 for value in updated):
        raise ArithmeticError("cycle signing failed to produce nonnegative even numerators")
    half = tuple(value // 2 for value in updated)
    if not _has_degrees(n_left, n_right, edges, half, 1 << (level - 1)):
        raise ArithmeticError("cycle coarsening changed the b-matching degrees")
    return half, scale


def sample_bipartite_perfect_matching(
    n_left: int,
    n_right: int,
    edges: Sequence[Edge],
    marginals: Sequence[Fraction],
    feature_columns: Sequence[Sequence[Fraction]],
    level: int,
    randbelow: RandBelow,
    signer: Signer,
) -> Cycle2Sample:
    """Sample a PM with exact rational marginals and a pathwise feature bound.

    Preconditions: the graph is bipartite with equal shore sizes, all listed
    edges are actual labelled graph edges, the supplied marginals are feasible,
    the feature columns are rational Euclidean unit vectors, and `signer` is
    Li's deterministic rational signing algorithm with its <99 guarantee.
    """
    if n_left != n_right or n_left < 1:
        raise ValueError("a nonempty bipartite perfect-matching instance needs equal shores")
    if len(edges) != len(marginals) or len(edges) != len(feature_columns):
        raise ValueError("edges, marginals, and feature columns must have equal length")
    if level < 0:
        raise ValueError("dyadic level must be nonnegative")
    x = tuple(Fraction(value) for value in marginals)
    A = tuple(tuple(Fraction(value) for value in column) for column in feature_columns)
    d = len(A[0]) if A else 0
    if any(len(column) != d for column in A):
        raise ValueError("feature columns must have a common dimension")
    if any(not 0 <= value <= 1 for value in x):
        raise ValueError("edge marginals must lie in [0,1]")
    if any(sum((q * q for q in column), Fraction(0)) > 1 for column in A):
        raise ValueError("each feature column must have Euclidean norm at most one")
    for left, right in edges:
        if not 0 <= left < n_left or not 0 <= right < n_right:
            raise ValueError("edge endpoint lies outside its bipartition shore")

    degree = [Fraction(0)] * (n_left + n_right)
    for (left, right), value in zip(edges, x):
        degree[left] += value
        degree[n_left + right] += value
    if any(value != 1 for value in degree):
        raise ValueError("marginals must satisfy every perfect-matching degree equation")

    y = _initial_residual_bmatching(n_left, n_right, edges, x, level, randbelow)
    scales: dict[int, int] = {}
    for t in range(level, 0, -1):
        y, scales[t] = _coarsen_one_level(
            n_left, n_right, edges, y, t, A, randbelow, signer
        )
    if any(value not in (0, 1) for value in y) or not _has_degrees(
        n_left, n_right, edges, y, 1
    ):
        raise ArithmeticError("final coarsening did not produce a perfect matching")

    error = tuple(
        sum((A[e][j] * (y[e] - x[e]) for e in range(len(edges))), Fraction(0))
        for j in range(d)
    )
    residual_bound = Fraction(len(edges), 1 << level)
    path_bound = residual_bound + 99 * sum(
        (Fraction(scales[t], 1 << t) for t in range(1, level + 1)), Fraction(0)
    )
    if max((abs(value) for value in error), default=Fraction(0)) > path_bound:
        raise ArithmeticError("sample exceeded its certified pathwise feature bound")
    return Cycle2Sample(
        matching_edge_ids=tuple(edge_id for edge_id, value in enumerate(y) if value),
        feature_error=error,
        initial_residual_bound=residual_bound,
        cycle_scales=tuple((t, scales[t]) for t in range(level, 0, -1)),
        path_bound=path_bound,
    )
