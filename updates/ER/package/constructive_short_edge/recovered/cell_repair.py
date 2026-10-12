"""Exact enclosing-cell repair for explicitly described rational polytopes.

This is an executable implementation of the precision-repair operation, not
of the full spectral rounding algorithm. The explicit-H implementation uses
exact rational boundary pushes to a vertex of the clipped slice (at most n
face drops). The oracle-model construction uses polynomial-bit rational LP.

Artificial cell facets are NEVER carried into the next original-face model.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import sympy as sp

RationalLike = int | sp.Rational

def q(value: RationalLike) -> sp.Rational:
    if isinstance(value, float):
        raise TypeError("Use exact rational input, not binary floats.")
    return sp.Rational(value)

def dot(a, b):
    return sum((q(x) * q(y) for x, y in zip(a, b)), sp.Rational(0))

def independent_equations(rows, rhs, n):
    if not rows:
        return [], []
    matrix = sp.Matrix(rows)
    _, pivots = matrix.T.rref()
    selected = list(pivots)
    return [list(matrix.row(i)) for i in selected], [rhs[i] for i in selected]

def original_face_dimension(point, inequalities, upper, equalities, targets):
    n = len(point)
    rows = [list(row) for row in equalities]
    rows += [list(row) for row, bound in zip(inequalities, upper)
             if dot(row, point) == q(bound)]
    return n - (sp.Matrix(rows).rank() if rows else 0)

def max_coordinate_bits(point):
    return max((max(abs(int(q(t).p)).bit_length(), int(q(t).q).bit_length())
                for t in point), default=0)

@dataclass
class RepairResult:
    point: list[sp.Rational]
    input_bits: int
    output_bits: int
    mesh_bits: int
    face_dimension_before: int
    face_dimension_after: int
    boundary_pushes: int


def enclosing_cell_repair(
    point: Sequence[RationalLike],
    inequalities: Sequence[Sequence[RationalLike]],
    upper: Sequence[RationalLike],
    equalities: Sequence[Sequence[RationalLike]] = (),
    targets: Sequence[RationalLike] = (),
    fixed_equations: Sequence[Sequence[RationalLike]] = (),
    fixed_targets: Sequence[RationalLike] = (),
    mesh_bits: int = 16,
) -> RepairResult:
    """Repair inside the minimal ORIGINAL face and the prescribed affine slice.

    P={z: inequalities*z <= upper, equalities*z == targets}.
    All fixed slice targets must be part of the original encoded problem,
    rather than unbounded-denominator expressions stored from prior moves.
    The returned point may be in a smaller original face.  Cell facets are
    deliberately not reported as original face constraints.
    """
    x = [q(t) for t in point]
    n = len(x)
    if n == 0 or not isinstance(mesh_bits, int) or mesh_bits < 0:
        raise ValueError("Require nonempty point and nonnegative integer mesh_bits.")
    A = [[q(t) for t in row] for row in inequalities]
    b = [q(t) for t in upper]
    E = [[q(t) for t in row] for row in equalities]
    f = [q(t) for t in targets]
    C = [[q(t) for t in row] for row in fixed_equations]
    d = [q(t) for t in fixed_targets]
    if len(A) != len(b) or len(E) != len(f) or len(C) != len(d):
        raise ValueError("Constraint/right-hand-side counts do not match.")
    if any(len(row) != n for row in A + E + C):
        raise ValueError("Incorrect constraint dimension.")
    if any(dot(row, x) > bound for row, bound in zip(A, b)):
        raise ValueError("Input point is not in the original polytope.")
    if any(dot(row, x) != target for row, target in zip(E + C, f + d)):
        raise ValueError("Input point violates an exact equation.")

    face_rows = E + [row for row, bound in zip(A, b) if dot(row, x) == bound]
    face_rhs = f + [bound for row, bound in zip(A, b) if dot(row, x) == bound]
    eq, eqrhs = independent_equations(face_rows + C, face_rhs + d, n)
    denominator = 1 << mesh_bits
    lower = [sp.Rational(sp.floor(t * denominator), denominator) for t in x]
    upper_cell = [t + sp.Rational(1, denominator) for t in lower]
    bounds = list(zip(lower, upper_cell))

    # Vertex extraction for an explicit H-polytope: move along a nullspace
    # direction until a new ORIGINAL-OR-CELL inequality binds. Each push adds
    # an independent normal, so no more than n pushes are possible. The cell
    # inequalities are temporary and are never included in the returned
    # original-face dimension. All computations are exact rational.
    all_rows = [row[:] for row in A]
    all_rhs = b[:]
    for j in range(n):
        unit = [sp.Rational(int(i == j)) for i in range(n)]
        all_rows += [unit, [-t for t in unit]]
        all_rhs += [upper_cell[j], -lower[j]]
    y = x[:]
    calls = 0
    while True:
        active = eq + [row for row, bound in zip(all_rows, all_rhs)
                       if dot(row, y) == bound]
        if active:
            kernel = sp.Matrix(active).nullspace()
        else:
            kernel = [sp.eye(n).col(0)]
        if not kernel:
            break
        direction = list(kernel[0])
        candidates = [(bound - dot(row, y)) / dot(row, direction)
                      for row, bound in zip(all_rows, all_rhs)
                      if dot(row, direction) > 0]
        if not candidates:
            raise AssertionError("Bounded enclosing cell cannot have a recession ray.")
        step = min(candidates)
        if step <= 0:
            raise AssertionError("Direction must have a positive feasible step.")
        y = [t + step * h for t, h in zip(y, direction)]
        calls += 1
        if calls > n:
            raise AssertionError("Every push must strictly lower clipped-face dimension.")
    if any(dot(row, y) > bound for row, bound in zip(A, b)):
        raise AssertionError("LP result failed exact original feasibility.")
    if any(dot(row, y) != target for row, target in zip(face_rows + C, face_rhs + d)):
        raise AssertionError("LP result failed exact face/slice preservation.")
    if any(not (lo <= t <= hi) for t, (lo, hi) in zip(y, bounds)):
        raise AssertionError("LP result failed exact cell containment.")
    if any(abs(t-s) > sp.Rational(1, denominator) for t, s in zip(x, y)):
        raise AssertionError("LP result exceeded repair movement budget.")
    before = original_face_dimension(x, A, b, E, f)
    after = original_face_dimension(y, A, b, E, f)
    assert after <= before
    return RepairResult(y, max_coordinate_bits(x), max_coordinate_bits(y),
                        mesh_bits, before, after, calls)
