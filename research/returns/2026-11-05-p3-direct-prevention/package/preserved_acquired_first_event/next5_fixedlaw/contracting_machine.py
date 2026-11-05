"""Exact finite compiler for the contraction/reachability boundary.

All arithmetic uses fractions.Fraction.  This is a constructive diagnostic,
not a proof assistant or an efficient simulator for arbitrary counter programs.
See FOUNDATIONAL_CONTRACTION_BOUNDARY.md for the global proof and scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import permutations, product
from typing import Iterable, Sequence


Vector = tuple[F, ...]


def vec(values: Iterable[int | F]) -> Vector:
    return tuple(F(v) for v in values)


def dot(a: Sequence[F], b: Sequence[F]) -> F:
    return sum((u * v for u, v in zip(a, b)), F(0))


def sqnorm(a: Sequence[F]) -> F:
    return dot(a, a)


def sub(a: Sequence[F], b: Sequence[F]) -> Vector:
    return tuple(u - v for u, v in zip(a, b))


def scale(c: F, a: Sequence[F]) -> Vector:
    return tuple(c * u for u in a)


@dataclass(frozen=True)
class Instruction:
    """Counters are 0/1; state labels are 1,...,m, with m the sole halt."""

    kind: str
    counter: int = 0
    next_state: int | None = None
    zero_state: int | None = None
    positive_state: int | None = None

    @staticmethod
    def inc(counter: int, target: int) -> "Instruction":
        return Instruction("inc", counter, next_state=target)

    @staticmethod
    def decjz(counter: int, zero: int, positive: int) -> "Instruction":
        return Instruction("decjz", counter, zero_state=zero, positive_state=positive)

    @staticmethod
    def halt() -> "Instruction":
        return Instruction("halt")


class CounterMachine:
    def __init__(self, program: Sequence[Instruction]):
        self.program = tuple(program)
        self.m = len(program)
        if self.m < 2 or self.program[-1].kind != "halt":
            raise ValueError("Require m>=2 and a final HALT instruction")
        for index, instruction in enumerate(self.program, start=1):
            if instruction.kind == "halt":
                if index != self.m:
                    raise ValueError("Only the final label may be HALT")
                continue
            if instruction.counter not in (0, 1):
                raise ValueError("Exactly two counters, numbered 0 and 1")
            if instruction.kind == "inc":
                targets = (instruction.next_state,)
            elif instruction.kind == "decjz":
                targets = (instruction.zero_state, instruction.positive_state)
            else:
                raise ValueError("Unknown instruction")
            if any(t is None or not 1 <= t <= self.m for t in targets):
                raise ValueError("Invalid target label")

    def step(self, configuration: tuple[int, int, int]) -> tuple[int, int, int] | None:
        label, *counters = configuration
        if not 1 <= label <= self.m or min(counters) < 0:
            raise ValueError("Invalid machine configuration")
        instruction = self.program[label - 1]
        if instruction.kind == "halt":
            return None
        counter = instruction.counter
        if instruction.kind == "inc":
            counters[counter] += 1
            target = instruction.next_state
        elif counters[counter] == 0:
            target = instruction.zero_state
        else:
            counters[counter] -= 1
            target = instruction.positive_state
        assert target is not None
        return (target, counters[0], counters[1])


def project_cone(x: Sequence[F]) -> Vector:
    """Exact Euclidean projection onto t>=0, 0<=y_j<=t.

    There are at most eight active subsets.  Every candidate is affine over
    its rational polyhedral validity region.  Boundary ties agree uniquely.
    """

    t0, *coordinates = vec(x)
    if len(coordinates) != 3:
        raise ValueError("The ambient state has dimension four")
    if t0 + sum((max(F(0), c) for c in coordinates), F(0)) <= 0:
        return vec((0, 0, 0, 0))
    for active_bits in product((False, True), repeat=3):
        active = [j for j, bit in enumerate(active_bits) if bit]
        t = (t0 + sum((coordinates[j] for j in active), F(0))) / (1 + len(active))
        if t < 0:
            continue
        if all(
            (coordinates[j] >= t if active_bits[j] else coordinates[j] <= t)
            for j in range(3)
        ):
            clipped = tuple(min(t, max(F(0), c)) for c in coordinates)
            return (t, *clipped)
    raise AssertionError("Projection active-set enumeration must cover every input")


def projection_regions() -> list[dict]:
    """35 explicit rational conical cells, including boundary overlaps.

    A region is {x: h.x >= 0 for each h in inequalities}.  Cells may be
    redundant or lower-dimensional; equal boundary values make this harmless.
    """

    basis = [tuple(F(i == j) for j in range(4)) for i in range(4)]
    zero_matrix = tuple(vec((0, 0, 0, 0)) for _ in range(4))
    records = []
    for positive_bits in product((False, True), repeat=3):
        inequalities = [
            scale(F(1 if positive_bits[j] else -1), basis[j + 1]) for j in range(3)
        ]
        last = list(scale(F(-1), basis[0]))
        for j, positive in enumerate(positive_bits):
            if positive:
                last[j + 1] -= 1
        inequalities.append(tuple(last))
        records.append({
            "kind": "zero",
            "status": positive_bits,
            "matrix": zero_matrix,
            "inequalities": tuple(inequalities),
        })
    for statuses in product(("low", "middle", "upper"), repeat=3):
        upper = [j for j, status in enumerate(statuses) if status == "upper"]
        trow = [F(1, 1 + len(upper)), F(0), F(0), F(0)]
        for j in upper:
            trow[j + 1] = trow[0]
        trow = tuple(trow)
        matrix = [trow]
        inequalities = [trow]
        for j, status in enumerate(statuses):
            if status == "low":
                matrix.append(vec((0, 0, 0, 0)))
                inequalities.append(scale(F(-1), basis[j + 1]))
            elif status == "middle":
                matrix.append(basis[j + 1])
                inequalities.extend((basis[j + 1], sub(trow, basis[j + 1])))
            else:
                matrix.append(trow)
                inequalities.append(sub(basis[j + 1], trow))
        records.append({
            "kind": "positive",
            "status": statuses,
            "matrix": tuple(matrix),
            "inequalities": tuple(inequalities),
        })
    return records


class ContractingCompiler:
    counter_grid = (F(0), F(1, 2), F(3, 4), F(1))

    def __init__(self, machine: CounterMachine):
        self.machine = machine
        m = machine.m
        self.labels = (F(0),) + tuple(F(i, 2 * m) for i in range(1, m)) + (F(1),)
        self.grids = (self.labels, self.counter_grid, self.counter_grid)
        self.C = 16 * m + 68
        self.a = F(1, 2 * self.C)
        self._vertices: dict[tuple[int, int, int], Vector] = {}
        for indices in product(range(m + 1), range(4), range(4)):
            plane, i, j = indices
            label = max(1, plane)
            self._vertices[indices] = self.plane_map(
                label, self.counter_grid[i], self.counter_grid[j]
            )

    def label_value(self, label: int) -> F:
        return self.labels[label]

    def plane_map(self, label: int, z0: F, z1: F) -> Vector:
        instruction = self.machine.program[label - 1]
        if instruction.kind == "halt":
            return vec((0, 0, 0, 0))
        counters = [F(z0), F(z1)]
        counter = instruction.counter
        if instruction.kind == "inc":
            counters[counter] /= 2
            assert instruction.next_state is not None
            q = self.label_value(instruction.next_state)
        else:
            z = counters[counter]
            assert instruction.zero_state is not None
            assert instruction.positive_state is not None
            positive_q = self.label_value(instruction.positive_state)
            zero_q = self.label_value(instruction.zero_state)
            if z <= F(1, 2):
                counters[counter] = 2 * z
                q = positive_q
            elif z >= F(3, 4):
                counters[counter] = F(1)
                q = zero_q
            else:
                u = 4 * z - 2
                counters[counter] = F(1)
                q = (1 - u) * positive_q + u * zero_q
        return (F(1), q, counters[0], counters[1])

    @staticmethod
    def _interval(grid: Sequence[F], coordinate: F, t: F) -> int:
        if coordinate < 0 or coordinate > t:
            raise ValueError("Cone coordinate out of range")
        for i in range(len(grid) - 1):
            if coordinate <= grid[i + 1] * t:
                return i
        raise AssertionError("Grid covers the unit interval")

    def cone_map(self, x: Sequence[F]) -> Vector:
        """Homogenized interpolation, with no division by the state scale t."""

        t, *coordinates = vec(x)
        if t == 0:
            if any(coordinates):
                raise ValueError("Only the origin of this cone has t=0")
            return vec((0, 0, 0, 0))
        if t < 0:
            raise ValueError("Negative cone scale")
        lower = [
            self._interval(grid, c, t) for grid, c in zip(self.grids, coordinates)
        ]
        v = [
            (coordinates[j] - self.grids[j][lower[j]] * t)
            / (self.grids[j][lower[j] + 1] - self.grids[j][lower[j]])
            for j in range(3)
        ]
        order = sorted(range(3), key=lambda j: (-v[j], j))
        weights = (
            t - v[order[0]],
            v[order[0]] - v[order[1]],
            v[order[1]] - v[order[2]],
            v[order[2]],
        )
        assert min(weights) >= 0 and sum(weights) == t
        indices = list(lower)
        output = [F(0)] * 4
        for j in range(4):
            w = self._vertices[tuple(indices)]
            for k in range(4):
                output[k] += weights[j] * w[k]
            if j < 3:
                indices[order[j]] += 1
        return tuple(output)

    def cube_map(self, z: Sequence[F]) -> Vector:
        if len(z) != 3:
            raise ValueError("Cube state has dimension three")
        return self.cone_map((F(1), *z))

    def __call__(self, x: Sequence[F]) -> Vector:
        return scale(self.a, self.cone_map(project_cone(x)))

    def encode(self, configuration: tuple[int, int, int]) -> Vector:
        label, counter0, counter1 = configuration
        if min(counter0, counter1) < 0:
            raise ValueError("Counters must be nonnegative")
        return (F(1), self.label_value(label), F(1, 2**counter0), F(1, 2**counter1))

    def matrices(self) -> list[dict]:
        """Compile the 54*m cone matrices and their defining simplices.

        Matrices act on (t,x_q,x_0,x_1); each is [b | A] for cube map Az+b.
        The projection stage has its own fixed, exact active-set specification.
        """

        records = []
        for lower in product(range(self.machine.m), range(3), range(3)):
            lower_point = tuple(self.grids[j][lower[j]] for j in range(3))
            widths = tuple(
                self.grids[j][lower[j] + 1] - self.grids[j][lower[j]]
                for j in range(3)
            )
            for order in permutations(range(3)):
                indices = list(lower)
                outputs = [self._vertices[tuple(indices)]]
                vertices = [lower_point]
                for axis in order:
                    indices[axis] += 1
                    outputs.append(self._vertices[tuple(indices)])
                    vertices.append(tuple(self.grids[j][indices[j]] for j in range(3)))
                A = [[F(0)] * 3 for _ in range(4)]
                for step, axis in enumerate(order):
                    for row in range(4):
                        A[row][axis] = (outputs[step + 1][row] - outputs[step][row]) / widths[axis]
                b = [outputs[0][row] - dot(A[row], lower_point) for row in range(4)]
                matrix = tuple((b[row], *A[row]) for row in range(4))
                inequalities = [vec((1, 0, 0, 0))]
                normalized_rows = []
                for axis in range(3):
                    lo = [F(0)] * 4
                    hi = [F(0)] * 4
                    lo[0] = -lower_point[axis]
                    lo[axis + 1] = F(1)
                    hi[0] = lower_point[axis] + widths[axis]
                    hi[axis + 1] = F(-1)
                    inequalities.extend((tuple(lo), tuple(hi)))
                    normalized_rows.append(scale(1 / widths[axis], lo))
                inequalities.extend((
                    sub(normalized_rows[order[0]], normalized_rows[order[1]]),
                    sub(normalized_rows[order[1]], normalized_rows[order[2]]),
                ))
                records.append({
                    "lower_indices": lower,
                    "order": order,
                    "vertices": tuple(vertices),
                    "outputs": tuple(outputs),
                    "matrix": matrix,
                    "inequalities": tuple(inequalities),
                    "entry_absolute_sum": sum((abs(e) for row in matrix for e in row), F(0)),
                })
        return records

    def global_regions(self):
        """Yield an explicit complete global CPWL representation, <=1890*m cells.

        No feasibility oracle is hidden here: redundant/empty cells are kept.
        All coefficients are exact rational numbers.  The total cover and
        boundary consistency follow by composition of the two proved covers.
        """

        cone_regions = self.matrices()
        for projection in projection_regions():
            P = projection["matrix"]
            for region in cone_regions:
                M = region["matrix"]
                matrix = tuple(
                    tuple(self.a * sum((M[i][k] * P[k][j] for k in range(4)), F(0))
                          for j in range(4))
                    for i in range(4)
                )
                inequalities = list(projection["inequalities"])
                inequalities.extend(
                    tuple(sum((h[k] * P[k][j] for k in range(4)), F(0)) for j in range(4))
                    for h in region["inequalities"]
                )
                yield {"matrix": matrix, "inequalities": tuple(inequalities)}


def flag(x: Sequence[F]) -> F:
    return x[1] - F(3, 4) * x[0]


def countdown_machine() -> CounterMachine:
    return CounterMachine([
        Instruction.decjz(0, zero=3, positive=2),
        Instruction.inc(1, target=1),
        Instruction.halt(),
    ])


def nonhalting_machine() -> CounterMachine:
    return CounterMachine([
        Instruction.inc(0, target=1),
        Instruction.halt(),
    ])
