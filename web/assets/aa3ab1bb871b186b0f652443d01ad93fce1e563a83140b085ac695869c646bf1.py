"""Exact-mean dyadic rounding for bipartite perfect matchings.

The polynomial-time version supplies Li's rational Komlos signing algorithm
as ``signer``.  This file implements the remaining exact rational compiler.
``exhaustive_signer`` is a small-instance fallback only; it is exponential.

Vertices are labelled 0..n-1 on each shore.  Edge (i,j) joins left i to right
j.  Feature rows are indexed first and edges second.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt
from typing import Callable, Iterable, Sequence


Q = Fraction
Edge = tuple[int, int]
Point = tuple[Q, ...]
CycleColumn = tuple[Q, ...]
Signer = Callable[[Sequence[CycleColumn]], Sequence[int]]


@dataclass(frozen=True)
class Atom:
    probability: Q
    matching: tuple[int, ...]  # edge indices in the input edge list


def _floor(x: Q) -> int:
    return x.numerator // x.denominator


def _ceil_sqrt(x: Q) -> int:
    """Exact least integer at least sqrt(x), for nonnegative rational x."""
    if x < 0:
        raise ValueError("square-root input must be nonnegative")
    root = isqrt(x.numerator // x.denominator)
    if root * root * x.denominator < x.numerator:
        root += 1
    return root


def _other_endpoint(edge: Edge, vertex: int, n: int) -> int:
    left, right = edge
    right_vertex = n + right
    if vertex == left:
        return right_vertex
    if vertex == right_vertex:
        return left
    raise ValueError("vertex is not incident to edge")


def _support_perfect_matching(
    n: int, edges: Sequence[Edge], residual: Sequence[Q]
) -> tuple[int, ...] | None:
    """Find a perfect matching using only positive residual edges."""
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for eid, ((left, right), value) in enumerate(zip(edges, residual)):
        if value > 0:
            adjacency[left].append(eid)

    match_left: list[int | None] = [None] * n  # right endpoint
    match_right: list[int | None] = [None] * n  # left endpoint
    match_edge: list[int | None] = [None] * n

    # Successive augmenting paths; each search is a BFS in the alternating
    # graph and all choices follow the input edge order.
    for start in range(n):
        if match_left[start] is not None:
            continue
        parent_right: list[tuple[int, int] | None] = [None] * n
        seen_left = [False] * n
        seen_left[start] = True
        queue = [start]
        qpos = 0
        free_right: int | None = None
        while qpos < len(queue) and free_right is None:
            left = queue[qpos]
            qpos += 1
            for eid in adjacency[left]:
                _, right = edges[eid]
                if match_left[left] == right or parent_right[right] is not None:
                    continue
                parent_right[right] = (left, eid)
                matched_left = match_right[right]
                if matched_left is None:
                    free_right = right
                    break
                if not seen_left[matched_left]:
                    seen_left[matched_left] = True
                    queue.append(matched_left)

        if free_right is None:
            continue

        right = free_right
        while True:
            predecessor = parent_right[right]
            if predecessor is None:
                raise ArithmeticError("broken augmenting path")
            left, eid = predecessor
            old_right = match_left[left]
            match_left[left] = right
            match_right[right] = left
            match_edge[left] = eid
            if old_right is None:
                break
            right = old_right

    if any(right is None for right in match_left):
        return None
    if any(eid is None for eid in match_edge):
        return None
    result = tuple(int(eid) for eid in match_edge)
    if len(set(edges[eid][1] for eid in result)) != n:
        raise ArithmeticError("matching routine returned repeated right endpoint")
    return result


def _validate_input(
    n: int, edges: Sequence[Edge], x: Sequence[Q], feature_rows: Sequence[Sequence[Q]]
) -> tuple[tuple[Edge, ...], tuple[Q, ...], tuple[tuple[Q, ...], ...]]:
    if n < 1:
        raise ValueError("n must be positive")
    edge_tuple = tuple((int(left), int(right)) for left, right in edges)
    x_tuple = tuple(Q(value) for value in x)
    A = tuple(tuple(Q(value) for value in row) for row in feature_rows)
    if len(edge_tuple) != len(x_tuple):
        raise ValueError("one marginal is required for each labelled edge")
    if any(not (0 <= left < n and 0 <= right < n) for left, right in edge_tuple):
        raise ValueError("edge endpoint outside the labelled shores")
    if any(value < 0 for value in x_tuple):
        raise ValueError("marginals must be nonnegative")
    if any(len(row) != len(edge_tuple) for row in A):
        raise ValueError("each feature row must have one entry per edge")

    left_sums = [Q(0) for _ in range(n)]
    right_sums = [Q(0) for _ in range(n)]
    for (left, right), value in zip(edge_tuple, x_tuple):
        left_sums[left] += value
        right_sums[right] += value
    if any(value != 1 for value in left_sums + right_sums):
        raise ValueError("x must have degree sum one at every vertex")
    if _support_perfect_matching(n, edge_tuple, x_tuple) is None:
        raise ValueError("positive support has no perfect matching")
    return edge_tuple, x_tuple, A


def _birkhoff_decomposition(
    n: int, edges: Sequence[Edge], x: Sequence[Q]
) -> list[tuple[Q, tuple[int, ...]]]:
    """Exact network-flow decomposition into at most |E| matchings."""
    residual = list(x)
    result: list[tuple[Q, tuple[int, ...]]] = []
    while any(value > 0 for value in residual):
        matching = _support_perfect_matching(n, edges, residual)
        if matching is None:
            raise ArithmeticError("feasible residual lost a perfect matching")
        theta = min(residual[eid] for eid in matching)
        if theta <= 0:
            raise ArithmeticError("nonpositive network-flow subtraction")
        result.append((theta, matching))
        for eid in matching:
            residual[eid] -= theta
            if residual[eid] < 0:
                raise ArithmeticError("negative residual after exact subtraction")
        if len(result) > len(edges):
            raise ArithmeticError("support did not shrink under flow subtraction")
    if sum((weight for weight, _ in result), Q(0)) != 1:
        raise ArithmeticError("matching weights do not sum to one")
    return result


def _matching_point(edge_count: int, matching: Iterable[int]) -> Point:
    values = [Q(0) for _ in range(edge_count)]
    for eid in matching:
        values[eid] += 1
    return tuple(values)


def _initial_dyadic_law(
    edge_count: int,
    decomposition: Sequence[tuple[Q, tuple[int, ...]]],
    K: int,
) -> list[tuple[Q, Point]]:
    """Systematically round decomposition weights to denominator 2**K."""
    scale = 1 << K
    weights = [weight for weight, _ in decomposition]
    floors = [_floor(scale * weight) for weight in weights]
    fractions = [scale * weight - floor for weight, floor in zip(weights, floors)]
    total_fraction = sum(fractions, Q(0))
    if total_fraction.denominator != 1:
        raise ArithmeticError("fractional remainders do not sum to an integer")
    required_ones = int(total_fraction)

    cumulative = [Q(0)]
    for value in fractions:
        cumulative.append(cumulative[-1] + value)

    breaks = {Q(0), Q(1)}
    for value in cumulative[1:-1]:
        breaks.add(value - _floor(value))
    ordered = sorted(breaks)

    law_by_point: dict[Point, Q] = {}
    for low, high in zip(ordered, ordered[1:]):
        if low == high:
            continue
        U = (low + high) / 2
        bits = [
            _floor(cumulative[i + 1] - U) - _floor(cumulative[i] - U)
            for i in range(len(weights))
        ]
        if any(bit not in (0, 1) for bit in bits) or sum(bits) != required_ones:
            raise ArithmeticError("systematic rounding violated its cardinality")
        point_values = [Q(0) for _ in range(edge_count)]
        for i, (_, matching) in enumerate(decomposition):
            coefficient = Q(floors[i] + bits[i], scale)
            for eid in matching:
                point_values[eid] += coefficient
        point = tuple(point_values)
        law_by_point[point] = law_by_point.get(point, Q(0)) + (high - low)

    law = [(probability, point) for point, probability in law_by_point.items() if probability]
    if sum((probability for probability, _ in law), Q(0)) != 1:
        raise ArithmeticError("initial dyadic law has wrong total mass")
    return law


def _null_relation(points: Sequence[Point]) -> tuple[Q, ...]:
    """Return nonzero c with sum c_i=0 and sum c_i points[i]=0."""
    columns = len(points)
    rows = 1 + (len(points[0]) if points else 0)
    matrix = [[Q(1) for _ in range(columns)]]
    matrix.extend([[points[col][row] for col in range(columns)] for row in range(rows - 1)])

    pivot_columns: list[int] = []
    pivot_row = 0
    for col in range(columns):
        pivot = next((r for r in range(pivot_row, rows) if matrix[r][col] != 0), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for r in range(rows):
            if r == pivot_row or matrix[r][col] == 0:
                continue
            factor = matrix[r][col]
            matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break

    free = next((col for col in range(columns) if col not in pivot_columns), None)
    if free is None:
        raise ArithmeticError("expected affine dependence was absent")
    relation = [Q(0) for _ in range(columns)]
    relation[free] = Q(1)
    for r, pivot_col in enumerate(pivot_columns):
        relation[pivot_col] = -matrix[r][free]
    if not any(relation) or sum(relation, Q(0)) != 0:
        raise ArithmeticError("invalid affine dependence")
    for coordinate in range(rows - 1):
        if sum((relation[i] * points[i][coordinate] for i in range(columns)), Q(0)) != 0:
            raise ArithmeticError("dependence does not preserve the barycenter")
    return tuple(relation)


def _compress_law(law: Sequence[tuple[Q, Point]], edge_count: int) -> list[tuple[Q, Point]]:
    """Exact Caratheodory compression using existing atoms only."""
    merged: dict[Point, Q] = {}
    for probability, point in law:
        if probability > 0:
            merged[point] = merged.get(point, Q(0)) + probability
    current = [(probability, point) for point, probability in merged.items() if probability]
    while len(current) > edge_count + 1:
        points = [point for _, point in current]
        relation = _null_relation(points)
        positive = [i for i, value in enumerate(relation) if value > 0]
        if not positive:
            raise ArithmeticError("affine relation lacks a positive coefficient")
        step = min(current[i][0] / relation[i] for i in positive)
        updated = [
            (probability - step * coefficient, point)
            for (probability, point), coefficient in zip(current, relation)
        ]
        if any(probability < 0 for probability, _ in updated):
            raise ArithmeticError("compression made a negative weight")
        current = [(probability, point) for probability, point in updated if probability > 0]
    if sum((probability for probability, _ in current), Q(0)) != 1:
        raise ArithmeticError("compression changed total probability")
    return current


def _even_cycle_decomposition(
    n: int, edges: Sequence[Edge], odd_edge_ids: Sequence[int]
) -> list[tuple[tuple[int, int], ...]]:
    """Partition an even-degree bipartite multigraph into simple cycles.

    Each returned cycle is an ordered tuple of ``(edge_id, alternating_sign)``
    pairs.  The alternating signs cancel at every incident vertex.
    """
    adjacency: list[list[int]] = [[] for _ in range(2 * n)]
    degree = [0] * (2 * n)
    for eid in odd_edge_ids:
        left, right = edges[eid]
        v_right = n + right
        adjacency[left].append(eid)
        adjacency[v_right].append(eid)
        degree[left] += 1
        degree[v_right] += 1
    if any(value % 2 for value in degree):
        raise ValueError("odd-numerator support is not Eulerian")

    remaining = set(odd_edge_ids)
    cycles: list[tuple[tuple[int, int], ...]] = []

    while remaining:
        first_edge = min(remaining)
        start = edges[first_edge][0]
        vertices_stack = [start]
        edge_stack: list[int] = []
        circuit_vertices: list[int] = []
        circuit_edges: list[int] = []
        cursor = [0] * (2 * n)

        while vertices_stack:
            vertex = vertices_stack[-1]
            while cursor[vertex] < len(adjacency[vertex]) and adjacency[vertex][cursor[vertex]] not in remaining:
                cursor[vertex] += 1
            if cursor[vertex] < len(adjacency[vertex]):
                eid = adjacency[vertex][cursor[vertex]]
                cursor[vertex] += 1
                if eid not in remaining:
                    continue
                remaining.remove(eid)
                other = _other_endpoint(edges[eid], vertex, n)
                vertices_stack.append(other)
                edge_stack.append(eid)
            else:
                circuit_vertices.append(vertices_stack.pop())
                if edge_stack:
                    circuit_edges.append(edge_stack.pop())

        circuit_vertices.reverse()
        circuit_edges.reverse()
        if len(circuit_vertices) != len(circuit_edges) + 1 or circuit_vertices[0] != circuit_vertices[-1]:
            raise ArithmeticError("Euler tour reconstruction failed")

        # Split repeated vertices from the closed Euler walk until every piece
        # is a simple cycle. Removing a closed subwalk leaves a closed walk.
        while circuit_edges:
            seen: dict[int, int] = {}
            repeated: tuple[int, int] | None = None
            for j, vertex in enumerate(circuit_vertices[:-1]):
                if vertex in seen:
                    repeated = (seen[vertex], j)
                    break
                seen[vertex] = j
            if repeated is None:
                cycle_ids = circuit_edges
                if len(cycle_ids) % 2:
                    raise ArithmeticError("odd cycle in bipartite graph")
                cycles.append(tuple((eid, 1 if i % 2 == 0 else -1) for i, eid in enumerate(cycle_ids)))
                break

            i, j = repeated
            cycle_ids = circuit_edges[i:j]
            if len(cycle_ids) < 2 or len(cycle_ids) % 2:
                raise ArithmeticError("Euler walk did not split into an even simple cycle")
            cycles.append(tuple((eid, 1 if h % 2 == 0 else -1) for h, eid in enumerate(cycle_ids)))
            circuit_edges = circuit_edges[:i] + circuit_edges[j:]
            circuit_vertices = circuit_vertices[: i + 1] + circuit_vertices[j + 1 :]

    return cycles


def exhaustive_signer(columns: Sequence[CycleColumn]) -> tuple[int, ...]:
    """Exponential exact fallback for small inputs; not a polynomial backend."""
    count = len(columns)
    if count > 24:
        raise ValueError("exhaustive_signer is restricted to at most 24 columns")
    if count == 0:
        return ()
    rows = len(columns[0])
    for signs in product((-1, 1), repeat=count):
        discrepancy = [
            sum((signs[i] * columns[i][row] for i in range(count)), Q(0))
            for row in range(rows)
        ]
        if all(abs(value) < 99 for value in discrepancy):
            return tuple(signs)
    raise ArithmeticError("no <99 signing found; input may violate the unit-column premise")


def compile_matching_law(
    n: int,
    edges: Sequence[Edge],
    marginals: Sequence[Q],
    feature_rows: Sequence[Sequence[Q]],
    signer: Signer,
) -> tuple[Q, list[Atom], Q]:
    """Compile exact marginals into a law with every feature error < 100 B.

    ``signer`` must implement deterministic rational Komlos signing: on columns
    with Euclidean norm at most one it returns signs whose infinity discrepancy
    is strictly below 99.  The function verifies this premise and conclusion
    exactly on each call.  It returns ``(B, atoms, verified_max_error)``. Here
    ``B=min(B0, 2*n*max_e ceil(||A_e||_2))``; both terms are exact rational
    upper bounds on every simple cycle feature norm, and no cycle-norm oracle
    is needed.
    """
    edge_tuple, x, A = _validate_input(n, edges, marginals, feature_rows)
    edge_count = len(edge_tuple)
    B0 = sum((abs(value) for row in A for value in row), Q(0))
    column_norm_bounds = [
        _ceil_sqrt(sum((row[eid] * row[eid] for row in A), Q(0)))
        for eid in range(edge_count)
    ]
    B = min(B0, Q(2 * n * max(column_norm_bounds, default=0)))
    decomposition = _birkhoff_decomposition(n, edge_tuple, x)

    if B == 0:
        atoms = [Atom(weight, matching) for weight, matching in decomposition]
        return B, atoms, Q(0)

    support_size = len(decomposition)
    D_target = 2 * support_size * n
    K = 0
    while (1 << K) < D_target:
        K += 1
    law = _initial_dyadic_law(edge_count, decomposition, K)
    law = _compress_law(law, edge_count)

    for k in range(K, 0, -1):
        denominator = 1 << k
        child_law: list[tuple[Q, Point]] = []
        for probability, point in law:
            numerators: list[int] = []
            for value in point:
                scaled = value * denominator
                if scaled.denominator != 1:
                    raise ArithmeticError("point is off the expected dyadic grid")
                numerators.append(int(scaled))

            odd_edges = [eid for eid, value in enumerate(numerators) if value % 2]
            cycles = _even_cycle_decomposition(n, edge_tuple, odd_edges)
            if not cycles:
                child_law.append((probability, point))
                continue

            columns: list[CycleColumn] = []
            for cycle in cycles:
                col = []
                for row in A:
                    col.append(sum((row[eid] * sign for eid, sign in cycle), Q(0)))
                columns.append(tuple(col))
            normalized = tuple(tuple(value / B for value in col) for col in columns)
            for col in normalized:
                if sum((value * value for value in col), Q(0)) > 1:
                    raise ArithmeticError("cycle feature column exceeds the Li norm premise")

            signs = tuple(int(value) for value in signer(normalized))
            if len(signs) != len(cycles) or any(value not in (-1, 1) for value in signs):
                raise ValueError("signer must return one +/-1 sign per cycle")
            signing_error = [
                sum((signs[i] * normalized[i][row] for i in range(len(cycles))), Q(0))
                for row in range(len(A))
            ]
            if any(abs(value) >= 99 for value in signing_error):
                raise ValueError("signer failed the exact <99 discrepancy check")

            signed_direction = [0] * edge_count
            for cycle, cycle_sign in zip(cycles, signs):
                for eid, alternating_sign in cycle:
                    signed_direction[eid] = cycle_sign * alternating_sign

            plus = tuple(point[eid] + Q(signed_direction[eid], denominator) for eid in range(edge_count))
            minus = tuple(point[eid] - Q(signed_direction[eid], denominator) for eid in range(edge_count))
            for child in (plus, minus):
                if any(not 0 <= value <= 1 for value in child):
                    raise ArithmeticError("cycle halving left the unit cube")
                for left in range(n):
                    if sum((child[eid] for eid, (u, _) in enumerate(edge_tuple) if u == left), Q(0)) != 1:
                        raise ArithmeticError("cycle halving changed a left degree")
                for right in range(n):
                    if sum((child[eid] for eid, (_, v) in enumerate(edge_tuple) if v == right), Q(0)) != 1:
                        raise ArithmeticError("cycle halving changed a right degree")
            child_law.extend(((probability / 2, plus), (probability / 2, minus)))

        law = _compress_law(child_law, edge_count)

    atoms: list[Atom] = []
    max_error = Q(0)
    output_mean = [Q(0) for _ in range(edge_count)]
    for probability, point in law:
        matching = tuple(eid for eid, value in enumerate(point) if value == 1)
        if len(matching) != n or any(value not in (0, 1) for value in point):
            raise ArithmeticError("terminal point is not integral of matching size")
        for left in range(n):
            if sum(1 for eid in matching if edge_tuple[eid][0] == left) != 1:
                raise ArithmeticError("terminal point misses a left vertex")
        for right in range(n):
            if sum(1 for eid in matching if edge_tuple[eid][1] == right) != 1:
                raise ArithmeticError("terminal point misses a right vertex")
        error = [
            sum((row[eid] * (point[eid] - x[eid]) for eid in range(edge_count)), Q(0))
            for row in A
        ]
        max_error = max(max_error, *(abs(value) for value in error)) if error else max_error
        if max_error >= 100 * B:
            raise ArithmeticError("terminal feature discrepancy exceeded the theorem bound")
        for eid, value in enumerate(point):
            output_mean[eid] += probability * value
        atoms.append(Atom(probability, matching))

    if len(atoms) > edge_count + 1:
        raise ArithmeticError("support compression bound was violated")
    if sum((atom.probability for atom in atoms), Q(0)) != 1:
        raise ArithmeticError("output weights do not sum to one")
    if tuple(output_mean) != x:
        raise ArithmeticError("output law does not preserve every edge marginal")
    return B, atoms, max_error
