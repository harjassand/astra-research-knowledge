"""Exact rational primitives for implicit-energy trajectory certificates.

This module constructs and checks the convex quadratic program derived in
proof_note.md. It does NOT implement a general polynomial-time QP solver.
Only rational arithmetic from Python's standard library is used.

Representation:
    F(x) = min { 1/2 y^T H y + g^T y : A y <= b, y[:d] = x }.
H must be symmetric positive semidefinite. Boundedness and minimizer facts
are verified separately using supplied rational KKT certificates.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from math import lcm
from typing import Sequence

Vector = list[Q]
Matrix = list[Vector]


def dot(x: Sequence[Q], y: Sequence[Q]) -> Q:
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")
    return sum((a*b for a, b in zip(x, y)), Q(0))


def mv(A: Sequence[Sequence[Q]], x: Sequence[Q]) -> Vector:
    return [dot(row, x) for row in A]


def quad(A: Matrix, x: Vector) -> Q:
    return dot(x, mv(A, x))


def norm2(x: Sequence[Q]) -> Q:
    return dot(x, x)


def sub(x: Sequence[Q], y: Sequence[Q]) -> Vector:
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")
    return [a-b for a, b in zip(x, y)]


def is_psd(A: Matrix) -> bool:
    """Exact rational LDL elimination, including zero-pivot checks."""
    n = len(A)
    if any(len(row) != n for row in A):
        return False
    if any(A[i][j] != A[j][i] for i in range(n) for j in range(n)):
        return False
    M = [row.copy() for row in A]
    for k in range(n):
        p = M[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(M[k][j] != 0 for j in range(k+1, n)):
                return False
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                value = M[i][j] - M[i][k]*M[k][j]/p
                M[i][j] = M[j][i] = value
    return True


@dataclass
class EnergyQP:
    H: Matrix
    g: Vector
    A: Matrix
    b: Vector
    d: int

    def __post_init__(self) -> None:
        D = len(self.g)
        if not 1 <= self.d <= D:
            raise ValueError("Invalid observed dimension")
        if len(self.H) != D or any(len(row) != D for row in self.H):
            raise ValueError("H dimensions do not match g")
        if len(self.A) != len(self.b) or any(len(row) != D for row in self.A):
            raise ValueError("Constraint dimensions do not match")
        if not is_psd(self.H):
            raise ValueError("H is not rational symmetric PSD")

    @property
    def D(self) -> int:
        return len(self.g)

    @property
    def m(self) -> int:
        return len(self.b)

    def q(self, y: Vector) -> Q:
        return quad(self.H, y)/2 + dot(self.g, y)

    def feasible(self, y: Vector) -> bool:
        return len(y) == self.D and all(v <= b for v, b in zip(mv(self.A, y), self.b))

    def verify_minimizer(self, y: Vector, lam: Vector) -> bool:
        if not self.feasible(y) or len(lam) != self.m or any(v < 0 for v in lam):
            return False
        slack = sub(self.b, mv(self.A, y))
        if any(a*s != 0 for a, s in zip(lam, slack)):
            return False
        grad = [v+g for v, g in zip(mv(self.H, y), self.g)]
        return all(grad[j] + sum((self.A[r][j]*lam[r] for r in range(self.m)), Q(0)) == 0
                   for j in range(self.D))

    def tail_growth_constant(self, ystar: Vector, lamstar: Vector, E: Q) -> Q:
        """Return explicit rational C^2 with dist(x,S)^2 <= C^2 (F(x)-min F)
        on energy gaps <= E. The bound is crude, not the optimal Hoffman constant.
        """
        if E <= 0 or not self.verify_minimizer(ystar, lamstar):
            raise ValueError("Need positive E and a valid global KKT certificate")
        weighted = [sum((lamstar[r]*self.A[r][j] for r in range(self.m)), Q(0))
                    for j in range(self.D)]
        B = [row.copy() for row in self.A] + [row.copy() for row in self.H]
        B += [[-v for v in row] for row in self.H] + [weighted, [-v for v in weighted]]
        den = 1
        for row in B:
            for a in row:
                den = lcm(den, a.denominator)
        U = max([1] + [abs(int(a*den)) for row in B for a in row])
        K = Q(den * (self.D*U)**(self.D-1))
        qbar = sum((abs(a) for row in self.H for a in row), Q(0))
        return K*K*(2*qbar+E)


def geometric_mesh(E: Q, R2: Q, eta: Q, T: Q, max_steps: int = 1_000_000) -> Vector:
    if E <= 0 or R2 <= 0 or not 0 < eta < 1 or T <= 0:
        raise ValueError("Require E,R2,T>0 and 0<eta<1")
    a = R2/(2*E)
    times = [Q(0)]
    while times[-1] < T:
        if len(times) > max_steps:
            raise RuntimeError("Explicit step cap exceeded")
        t = times[-1]
        times.append(t + min(eta*(a+t), T-t))
    return times


@dataclass
class Certificate:
    times: Vector
    primal: list[Vector]  # includes initial feasible lift y_0
    dual_w: list[Vector]
    dual_lambda: list[Vector]


def certificate_action(model: EnergyQP, c: Certificate) -> Q:
    """Check all exact feasibility constraints and return a rigorous action upper bound."""
    N = len(c.times)-1
    if N < 1 or c.times[0] != 0 or len(c.primal) != N+1:
        raise ValueError("Malformed mesh or primal path")
    if len(c.dual_w) != N or len(c.dual_lambda) != N:
        raise ValueError("Malformed dual path")
    if not all(model.feasible(y) for y in c.primal):
        raise ValueError("Primal lift is infeasible")
    action = (norm2(c.primal[-1][:model.d])-norm2(c.primal[0][:model.d]))/2
    for i in range(1, N+1):
        h = c.times[i]-c.times[i-1]
        if h <= 0:
            raise ValueError("Times must strictly increase")
        yp, y = c.primal[i-1], c.primal[i]
        w, lam = c.dual_w[i-1], c.dual_lambda[i-1]
        if len(w) != model.D or len(lam) != model.m or any(v < 0 for v in lam):
            raise ValueError("Invalid dual variables")
        velocity = [(yp[j]-y[j])/h for j in range(model.d)] + [Q(0)]*(model.D-model.d)
        Hw = mv(model.H, w)
        for j in range(model.D):
            lhs = Hw[j] + model.g[j] + sum((model.A[r][j]*lam[r] for r in range(model.m)), Q(0))
            if lhs != velocity[j]:
                raise ValueError(f"Dual equality fails in cell {i}, coordinate {j}")
        dual = quad(model.H, w)/2 + dot(model.b, lam)
        action += h*((model.q(yp)+model.q(y))/2+dual)
    if action < 0:
        raise ArithmeticError("A feasible certificate cannot have negative action")
    return action


@dataclass
class SparseQP:
    """Objective 1/2 z^T Q z + c^T z + constant; full symmetric COO Q."""
    n: int
    Qentries: dict[tuple[int, int], Q]
    linear: dict[int, Q]
    constant: Q
    inequalities: list[tuple[dict[int, Q], Q]]
    equalities: list[tuple[dict[int, Q], Q]]

    def evaluate_feasible(self, z: Vector) -> Q:
        if len(z) != self.n:
            raise ValueError("Wrong candidate dimension")
        def ev(row: dict[int, Q]) -> Q:
            return sum((a*z[j] for j, a in row.items()), Q(0))
        if any(ev(row) > rhs for row, rhs in self.inequalities):
            raise ValueError("QP inequality violation")
        if any(ev(row) != rhs for row, rhs in self.equalities):
            raise ValueError("QP equality violation")
        return self.constant + ev(self.linear) + sum((a*z[i]*z[j]/2 for (i,j), a in self.Qentries.items()), Q(0))


def compile_action_qp(model: EnergyQP, times: Vector, y0: Vector) -> SparseQP:
    """Construct the exact global QP. No active-region enumeration is performed."""
    if not model.feasible(y0) or not times or times[0] != 0:
        raise ValueError("Invalid initial lift or mesh")
    h = [times[i+1]-times[i] for i in range(len(times)-1)]
    if not h or any(t <= 0 for t in h):
        raise ValueError("Invalid mesh")
    N, D, m = len(h), model.D, model.m
    stride = 2*D+m
    matrix: dict[tuple[int,int], Q] = {}
    linear: dict[int, Q] = {}
    le: list[tuple[dict[int,Q], Q]] = []
    eq: list[tuple[dict[int,Q], Q]] = []
    def put(table: dict, key, val: Q) -> None:
        if val:
            table[key] = table.get(key, Q(0)) + val
            if table[key] == 0:
                del table[key]
    for i in range(N):
        off, hi = i*stride, h[i]
        hn = h[i+1] if i+1 < N else Q(0)
        for j in range(D):
            put(linear, off+j, (hi+hn)*model.g[j]/2)
            for k in range(D):
                put(matrix, (off+j,off+k), (hi+hn)*model.H[j][k]/2)
                put(matrix, (off+D+j,off+D+k), hi*model.H[j][k])
        if i == N-1:
            for j in range(model.d):
                put(matrix, (off+j,off+j), Q(1))
        for r in range(m):
            put(linear, off+2*D+r, hi*model.b[r])
            le.append(({off+j:a for j,a in enumerate(model.A[r]) if a}, model.b[r]))
            le.append(({off+2*D+r:Q(-1)}, Q(0)))
        for j in range(D):
            row: dict[int,Q] = {}
            for k in range(D):
                put(row, off+D+k, hi*model.H[j][k])
            for r in range(m):
                put(row, off+2*D+r, hi*model.A[r][j])
            rhs = -hi*model.g[j]
            if j < model.d:
                put(row, off+j, Q(1))
                if i:
                    put(row, off-stride+j, Q(-1))
                else:
                    rhs += y0[j]
            eq.append((row,rhs))
    constant = h[0]*model.q(y0)/2 - norm2(y0[:model.d])/2
    return SparseQP(N*stride, matrix, linear, constant, le, eq)


def certificate_vector(c: Certificate) -> Vector:
    z: Vector = []
    for i in range(1,len(c.times)):
        z += c.primal[i] + c.dual_w[i-1] + c.dual_lambda[i-1]
    return z
