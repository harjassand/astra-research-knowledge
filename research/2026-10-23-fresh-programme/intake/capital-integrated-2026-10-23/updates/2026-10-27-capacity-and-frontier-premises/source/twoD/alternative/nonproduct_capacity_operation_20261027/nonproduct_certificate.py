"""Exact, local Galerkin certificates for a finite nonproduct Gibbs source.

Only graph balls reached by powers of the full BACKWARD generator are built.
All residual neighbors are retained. No 2**N source-state enumeration occurs.
This is an application of ordinary reversible potential theory and Galerkin
residual bounds, with no priority or computational-advantage claim.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True


def exact(x):
    if type(x) not in (int, F):
        raise TypeError("Only exact integer or Fraction inputs are accepted")
    return F(x)


def box(x):
    x = F(x)
    try:
        approximate = float(x)
    except OverflowError:
        approximate = None
    return {"numerator": str(x.numerator), "denominator": str(x.denominator),
            "numerator_bits": abs(x.numerator).bit_length(),
            "denominator_bits": x.denominator.bit_length(), "approx": approximate}


def unbox(x):
    return F(int(x["numerator"]), int(x["denominator"]))


def square_edges(width, height, periodic=True):
    if min(width, height) < (3 if periodic else 2):
        raise ValueError("Periodic sides >= 3; open sides >= 2 required")
    edges = set()
    for y in range(height):
        for x in range(width):
            i = y * width + x
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = x + dx, y + dy
                if periodic:
                    xx, yy = xx % width, yy % height
                if xx < width and yy < height:
                    j = yy * width + xx
                    assert i != j
                    edges.add(tuple(sorted((i, j))))
    return tuple(sorted(edges))


class GibbsOperator:
    def __init__(self, width=8, height=8, periodic=True,
                 theta=F(1, 4), kappa=F(9, 8)):
        self.theta, self.kappa = exact(theta), exact(kappa)
        if not 0 < self.theta < 1 or not self.kappa >= 1:
            raise ValueError("This fixture requires 0 < theta < 1, kappa >= 1")
        self.width, self.height, self.periodic = width, height, periodic
        self.n = width * height
        self.edges = square_edges(width, height, periodic)
        self.neighbors = [0] * self.n
        for i, j in self.edges:
            self.neighbors[i] |= 1 << j
            self.neighbors[j] |= 1 << i
        self.degree = max(m.bit_count() for m in self.neighbors)
        self.a, self.b = 0, (1 << self.n) - 1
        ratios = [self.theta * self.kappa**k for k in range(self.degree + 1)]
        self.birth = [r / (1 + r) for r in ratios]
        self.death = [1 / (1 + r) for r in ratios]
        self.D = math.lcm(*(p.denominator for p in self.birth + self.death))
        self.birth_int = [int(self.D * p) for p in self.birth]
        self.death_int = [int(self.D * p) for p in self.death]
        assert all(self.birth_int[k] + self.death_int[k] == self.D
                   for k in range(self.degree + 1))
        self.B = (self.theta.denominator**self.n *
                  self.kappa.denominator**len(self.edges))
        self.rho = self.theta**self.n * self.kappa**len(self.edges)
        self.N = self.B * self.rho
        assert self.N.denominator == 1
        self.N = int(self.N)
        if not 0 < self.rho <= 1:
            raise ValueError("Endpoint weight ratio must be in (0, 1]")
        self.influence = max((self.birth[k + 1] - self.birth[k]
                              for k in range(self.degree)), default=F(0))
        self.gap = 1 - self.degree * self.influence
        if self.gap <= 0:
            raise ValueError("The common-uniform coupling bound is nonpositive")
        self.Ra = self.n * self.birth[0]
        self.Rstar = F(self.n)  # Unit heatbath clocks; all flip rates <= 1.
        self.weights = {self.a: self.B, self.b: self.N}
        self.row_evaluations = 0
        self.neighbor_evaluations = 0

    def direct_weight(self, x):
        """Independent direct expression, used on controls and endpoints."""
        occupied_edges = sum(bool(x >> i & 1) and bool(x >> j & 1)
                             for i, j in self.edges)
        value = self.B * self.theta**x.bit_count() * self.kappa**occupied_edges
        assert value.denominator == 1
        return int(value)

    def rows(self, x):
        self.row_evaluations += 1
        self.neighbor_evaluations += self.n
        for i, mask in enumerate(self.neighbors):
            k = (x & mask).bit_count()
            if x >> i & 1:
                forward, reverse = self.death_int[k], self.birth_int[k]
            else:
                forward, reverse = self.birth_int[k], self.death_int[k]
            yield x ^ (1 << i), forward, reverse

    def apply_A(self, vector):
        """A=D*(-Q_backward); propagation uses q(y,x), not q(x,y)."""
        out = {}
        for x, value in vector.items():
            wx = self.weights[x]
            diagonal = 0
            for y, forward, reverse in self.rows(x):
                diagonal += forward
                wy, remainder = divmod(wx * forward, reverse)
                assert remainder == 0
                if y in self.weights:
                    assert self.weights[y] == wy
                else:
                    self.weights[y] = wy
                out[y] = out.get(y, 0) - reverse * value
            out[x] = out.get(x, 0) + diagonal * value
        out = {x: value for x, value in out.items() if value}
        assert sum(self.weights[x] * value for x, value in out.items()) == 0
        return out

    def inner(self, x, y):
        if len(x) > len(y):
            x, y = y, x
        return sum(self.weights[s] * value * y.get(s, 0)
                   for s, value in x.items())

    def support_receipt(self, vector, degree):
        counts_a = [0] * (degree + 1)
        counts_b = [0] * (degree + 1)
        overlap = 0
        for x in vector:
            da, db = x.bit_count(), self.n - x.bit_count()
            assert min(da, db) <= degree
            if da <= degree:
                counts_a[da] += 1
            if db <= degree:
                counts_b[db] += 1
            overlap += da <= degree and db <= degree
        return {"degree": degree, "nonzeros": len(vector),
                "distance_counts_a": counts_a, "distance_counts_b": counts_b,
                "overlap": overlap,
                "max_entry_bits": max(abs(v).bit_length() for v in vector.values())}


def solve_small(matrix, rhs):
    """Exact elimination; intended only for the tiny Galerkin system."""
    n = len(rhs)
    rows = [[F(x) for x in row] + [F(rhs[i])]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            raise ArithmeticError("Dependent Krylov vectors: no singular inverse")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    answer = [row[-1] for row in rows]
    assert all(sum(a * b for a, b in zip(row, answer)) == target
               for row, target in zip(matrix, rhs))
    return answer


def galerkin(op, vectors, degree, gram):
    # z=sum alpha_j A**j (B*u); y=(D/B)*z.
    matrix = [[gram[i][j + 1] for j in range(degree)]
              for i in range(degree)]
    assert all(matrix[i][j] == matrix[j][i]
               for i in range(degree) for j in range(degree))
    rhs = [gram[i][0] for i in range(degree)]
    alpha = solve_small(matrix, rhs)
    energy = sum((a * b for a, b in zip(alpha, rhs)), F(0))
    beta = [F(1)] + [-a for a in alpha]
    residual_norm = sum((beta[i] * beta[j] * gram[i][j]
                         for i in range(degree + 1)
                         for j in range(degree + 1)), F(0))
    assert energy > 0 and residual_norm >= 0
    scale = op.B**2 * op.N
    lower = op.D * energy / scale
    upper = lower + residual_norm / (scale * op.gap)
    return lower, upper, alpha, residual_norm


def certify(width=8, height=8, periodic=True, max_degree=3,
            epsilon=F(1, 1000), progress=False, return_internal=False):
    epsilon = exact(epsilon)
    if not 0 < epsilon < 1 or type(max_degree) is not int or max_degree < 1:
        raise ValueError("Positive integer degree and epsilon in (0,1) required")
    started = time.perf_counter()
    op = GibbsOperator(width, height, periodic)
    vectors = [{op.a: op.N, op.b: -op.B}]
    assert sum(op.weights[x] * v for x, v in vectors[0].items()) == 0
    lower = (1 + op.rho) / (2 * op.Rstar)
    upper = (1 + op.rho) / op.gap
    records = []
    for k in range(1, max_degree + 1):
        apply_started = time.perf_counter()
        vectors.append(op.apply_A(vectors[-1]))
        apply_seconds = time.perf_counter() - apply_started
        gram_started = time.perf_counter()
        gram = [[op.inner(v, w) for w in vectors] for v in vectors]
        assert all(gram[i][j] == gram[j][i]
                   for i in range(k + 1) for j in range(k + 1))
        gram_seconds = time.perf_counter() - gram_started
        lo, hi, alpha, norm = galerkin(op, vectors, k, gram)
        lower, upper = max(lower, lo), min(upper, hi)
        assert 0 < lower <= upper
        p_lower = op.rho / (op.Ra * upper)
        p_upper = op.rho / (op.Ra * lower)
        record = {"degree": k, "I_lower": box(lower), "I_upper": box(upper),
                  "raw_Galerkin_lower": box(lo), "raw_residual_upper": box(hi),
                  "p_lower": box(p_lower), "p_upper": box(p_upper),
                  "relative_width": float(upper / lower - 1),
                  "support": op.support_receipt(vectors[-1], k),
                  "coefficient_alpha": [box(a) for a in alpha],
                  "residual_norm_integer_weight": box(norm),
                  "moment_max_bits": max(abs(x).bit_length()
                                         for row in gram for x in row),
                  "row_evaluations_total": op.row_evaluations,
                  "neighbor_evaluations_total": op.neighbor_evaluations,
                  "apply_seconds": apply_seconds, "gram_seconds": gram_seconds,
                  "elapsed_seconds": time.perf_counter() - started}
        records.append(record)
        if progress:
            print("degree", k, "relative width", record["relative_width"],
                  "residual support", len(vectors[-1]), "seconds",
                  record["elapsed_seconds"], flush=True)
        if upper / lower <= 1 + epsilon:
            break
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "status": "TARGET_MET" if upper / lower <= 1 + epsilon else
                  "CERTIFIED_BUT_TARGET_NOT_MET",
        "method": "ordinary exact local Galerkin, full backward residual",
        "width": width, "height": height, "periodic": periodic,
        "sites": op.n, "edges": len(op.edges), "full_state_count": 1 << op.n,
        "theta": str(op.theta), "kappa": str(op.kappa),
        "epsilon": str(epsilon), "degree_cap": max_degree, "degree": k,
        "rho": box(op.rho), "R_a": box(op.Ra),
        "max_exit_rate_upper": box(op.Rstar),
        "birth_probabilities": [box(p) for p in op.birth],
        "influence_max": box(op.influence), "gap_lower": box(op.gap),
        "rate_denominator": str(op.D), "rate_denominator_bits": op.D.bit_length(),
        "weight_scale": str(op.B), "weight_scale_bits": op.B.bit_length(),
        "p_lower": box(p_lower), "p_upper": box(p_upper),
        "I_lower": box(lower), "I_upper": box(upper),
        "relative_width": float(upper / lower - 1), "degrees": records,
        "final_moment_matrix": [[str(g) for g in row] for row in gram],
        "visited_weight_states": len(op.weights),
        "row_evaluations_total": op.row_evaluations,
        "neighbor_evaluations_total": op.neighbor_evaluations,
        "peak_process_RSS_bytes": rss if platform.system() == "Darwin" else 1024 * rss,
        "elapsed_seconds": time.perf_counter() - started,
        "python": sys.version, "platform": platform.platform(),
        "scope": "Exact supplied finite Gibbs model and analytic gap; no physical acquisition, priority, generic low-degree, or advantage claim."
    }
    return (result, (op, vectors, gram, alpha)) if return_internal else result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CERTIFICATE_8x8.json")
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--height", type=int, default=8)
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--degree", type=int, default=3)
    parser.add_argument("--epsilon", default="1/1000")
    args = parser.parse_args()
    result = certify(args.width, args.height, not args.open, args.degree,
                     F(args.epsilon), progress=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"], "p in", result["p_lower"]["approx"],
          result["p_upper"]["approx"], flush=True)
