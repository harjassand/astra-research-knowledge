"""Independent finite-bit Erlang/resolvent enclosure of the receiving Duhamel bound.

No source packet module is imported or executed. Standard library only.
All acceptance quantities are exact rational integers. Floating values display only.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import math
import resource
import time


def pair_matrix(n, edges, rates):
    if not isinstance(n, int) or n < 2 or len(edges) != len(rates):
        raise ValueError("invalid graph size or edge/rate lengths")
    edge_rates = {}
    for e, r in zip(edges, rates):
        if len(e) != 2 or any(not isinstance(x, int) or x < 0 or x >= n for x in e) or e[0] == e[1]:
            raise ValueError("invalid edge")
        e = tuple(sorted(e))
        r = F(r)
        if e in edge_rates or r < 0 or r.denominator != 1:
            raise ValueError("duplicate edge or noninteger/nonnegative rate")
        edge_rates[e] = int(r)
    neighbors = [[] for _ in range(n)]
    for (x, y), r in edge_rates.items():
        neighbors[x].append((y, r))
        neighbors[y].append((x, r))
    pairs = list(combinations(range(n), 2))
    index = {e: i for i, e in enumerate(pairs)}
    rows = []
    for i, (x, y) in enumerate(pairs):
        row = {i: 2 * edge_rates.get((x, y), 0)}
        for a, b in ((x, y), (y, x)):
            for z, r in neighbors[a]:
                if z == b or not r:
                    continue
                j = index[tuple(sorted((z, b)))]
                row[i] += r
                row[j] = row.get(j, 0) - r
        row = {j: x for j, x in row.items() if x}
        if sum(row.values()) < 0 or any(x > 0 for j, x in row.items() if j != i):
            raise ArithmeticError("invalid killed M-matrix")
        rows.append(row)
    if any(rows[j].get(i, 0) != a for i, row in enumerate(rows) for j, a in row.items()):
        raise ArithmeticError("pair matrix is not symmetric")
    return rows, [index[tuple(sorted(e))] for e in edges]


class ExactSparseLDL:
    """Natural-order sparse rational LDL; fill and bit lengths are reported.

    This is a proposer only. The certificate checker uses integer residuals,
    independent of whether factorization/solve code is correct.
    """
    def __init__(self, rows, shift):
        if not isinstance(shift, int) or shift <= 0:
            raise ValueError("shift must be a positive integer")
        self.shift = shift
        self.rows = rows
        d = len(rows)
        a = [{j: F(x) for j, x in row.items() if j >= i} for i, row in enumerate(rows)]
        for i in range(d):
            a[i][i] = a[i].get(i, F(0)) + shift
        self.columns = []
        self.diagonal = []
        self.schur_updates = 0
        self.maximum_factor_bits = 0
        begin = time.perf_counter()
        for i in range(d):
            pivot = a[i][i]
            if pivot <= 0:
                raise ArithmeticError("nonpositive exact LDL pivot")
            self.diagonal.append(pivot)
            ns = sorted(j for j, v in a[i].items() if j > i and v)
            col = {j: a[i][j] / pivot for j in ns}
            self.columns.append(col)
            for pos, j in enumerate(ns):
                for ell in ns[pos:]:
                    v = a[j].get(ell, F(0)) - col[j] * a[i][ell]
                    self.schur_updates += 1
                    if v:
                        a[j][ell] = v
                    else:
                        a[j].pop(ell, None)
            for v in [pivot, *col.values()]:
                self.maximum_factor_bits = max(self.maximum_factor_bits, abs(v.numerator).bit_length(), v.denominator.bit_length())
            a[i].clear()
        self.factor_seconds = time.perf_counter() - begin
        self.factor_entries = d + sum(len(c) for c in self.columns)
        self.solves = 0
        self.solve_seconds = 0.0

    def apply_scaled_and_floor(self, z):
        begin = time.perf_counter()
        d = len(z)
        # Solve (H+sI)y = s z exactly, then floor y onto the input grid.
        u = [F(self.shift * x) for x in z]
        for i, col in enumerate(self.columns):
            for j, lij in col.items():
                u[j] -= lij * u[i]
        y = [u[i] / self.diagonal[i] for i in range(d)]
        for i in range(d - 1, -1, -1):
            y[i] -= sum((lij * y[j] for j, lij in self.columns[i].items()), F(0))
        proposal = [x.numerator // x.denominator for x in y]
        # Exact integer residual, against original H rather than the factors.
        residual = max(abs(self.shift * z[i] - self.shift * proposal[i] - sum(a * proposal[j] for j, a in row.items())) for i, row in enumerate(self.rows))
        self.solves += 1
        self.solve_seconds += time.perf_counter() - begin
        return proposal, residual

    def receipt(self):
        return dict(proposer="exact rational LDL", shift=self.shift, dimension=len(self.rows), input_nnz=sum(len(r) for r in self.rows),
                    factor_entries=self.factor_entries, schur_updates=self.schur_updates,
                    maximum_factor_integer_bits=self.maximum_factor_bits,
                    factor_seconds=self.factor_seconds, solves=self.solves, solve_seconds=self.solve_seconds)


class CheckedFixedSparseLDL:
    """Fixed-point sparse LDL proposer, accepted solely through exact residuals.

    There is deliberately no claim that a rounded factor is an exact factor.
    A failed/nonpositive pivot rejects this proposer. If its roundoff is large,
    the residual enclosure grows and the final certificate fails closed.
    """
    def __init__(self, rows, shift, precision):
        if not isinstance(shift, int) or shift <= 0:
            raise ValueError("shift must be a positive integer")
        self.shift = shift
        self.rows = rows
        self.scale = 1 << precision
        scale = self.scale
        d = len(rows)
        a = [{j: x * scale for j, x in row.items() if j >= i} for i, row in enumerate(rows)]
        for i in range(d):
            a[i][i] = a[i].get(i, 0) + shift * scale
        self.columns = []
        self.reciprocal_diagonal = []
        self.schur_updates = 0
        self.maximum_factor_bits = 0
        begin = time.perf_counter()
        for i in range(d):
            pivot = a[i][i]
            if pivot <= 0:
                raise ArithmeticError("nonpositive rounded LDL pivot; increase precision")
            self.reciprocal_diagonal.append((scale * scale) // pivot)
            ns = sorted(j for j, v in a[i].items() if j > i and v)
            col = {j: (a[i][j] * scale) // pivot for j in ns}
            self.columns.append(col)
            for pos, j in enumerate(ns):
                for ell in ns[pos:]:
                    v = a[j].get(ell, 0) - (a[i][j] * a[i][ell]) // pivot
                    self.schur_updates += 1
                    if v:
                        a[j][ell] = v
                    else:
                        a[j].pop(ell, None)
            for v in [pivot, *col.values()]:
                self.maximum_factor_bits = max(self.maximum_factor_bits, abs(v).bit_length())
            a[i].clear()
        self.factor_seconds = time.perf_counter() - begin
        self.factor_entries = d + sum(len(c) for c in self.columns)
        self.solves = 0
        self.solve_seconds = 0.0

    def apply_scaled_and_floor(self, z):
        begin = time.perf_counter()
        d = len(z)
        scale = self.scale
        u = [self.shift * x for x in z]
        for i, col in enumerate(self.columns):
            for j, lij in col.items():
                u[j] -= (lij * u[i]) // scale
        proposal = [(u[i] * self.reciprocal_diagonal[i]) // scale for i in range(d)]
        for i in range(d - 1, -1, -1):
            proposal[i] -= sum((lij * proposal[j]) // scale for j, lij in self.columns[i].items())
        residual = max(abs(self.shift * z[i] - self.shift * proposal[i] - sum(a * proposal[j] for j, a in row.items())) for i, row in enumerate(self.rows))
        self.solves += 1
        self.solve_seconds += time.perf_counter() - begin
        return proposal, residual

    def receipt(self):
        return dict(proposer="fixed-point sparse LDL with exact integer residual acceptance", shift=self.shift,
                    dimension=len(self.rows), input_nnz=sum(len(r) for r in self.rows),
                    factor_entries=self.factor_entries, schur_updates=self.schur_updates,
                    maximum_factor_integer_bits=self.maximum_factor_bits,
                    factor_seconds=self.factor_seconds, solves=self.solves, solve_seconds=self.solve_seconds)


def gamma_cdf_lower(shape, x, terms=None):
    """P[Gamma(shape,rate=x) <= 1] lower bound from exp(x) Taylor lower sum."""
    if shape < 2 or x <= 0:
        raise ValueError("invalid Erlang parameters")
    x = F(x)
    terms = max(4 * shape, math.ceil(2 * x)) if terms is None else terms
    term = F(1)
    lower_exp = F(1)
    tail_poly = F(1)
    for j in range(1, terms + 1):
        term *= x / j
        lower_exp += term
        if j < shape:
            tail_poly += term
    lower = 1 - tail_poly / lower_exp
    if lower <= 0:
        raise ArithmeticError("CDF lower bound did not become positive")
    return lower, terms


def solve_history(rows, edge_indices, shape, shift, precision, exact_proposer=False):
    q = 1 << precision
    z = [q] * len(rows)
    factor = ExactSparseLDL(rows, shift) if exact_proposer else CheckedFixedSparseLDL(rows, shift, precision)
    error = F(0)
    hist = []
    residuals = []
    witnesses = []
    for j in range(1, shape):
        z, residual = factor.apply_scaled_and_floor(z)
        # (H+sI)^{-1} has infinity norm <= 1/s; P=s(H+sI)^{-1}
        # is positive substochastic. All past action errors therefore contract.
        error += F(residual, shift * q)
        lo = [max(F(0), F(z[e], q) - error) for e in edge_indices]
        hi = [min(F(1), F(z[e], q) + error) for e in edge_indices]
        if any(a > b for a, b in zip(lo, hi)):
            raise ArithmeticError("invalid residual enclosure")
        hist.append((lo, hi))
        witnesses.append(z.copy())
        residuals.append(dict(power=j, residual_numerator=residual,
                              grid_denominator_bits=precision, accumulated_error_exact=str(error)))
    return hist, factor.receipt(), residuals, witnesses


def certify(n, edges, r, q, shape=8, shift=None, precision=None, tolerance=F(1, 20), exact_proposer=False):
    """Certifies finite r->q endpoint TV only; separate averaging/sampler costs remain."""
    if shape < 2:
        raise ValueError("shape must be >=2")
    shift = 2 * shape if shift is None else shift
    before = time.perf_counter()
    rh, ei = pair_matrix(n, edges, r)
    qh, eq = pair_matrix(n, edges, q)
    assert ei == eq
    delta = [abs(a - b) for a, b in zip(r, q)]
    weight = sum(delta)
    largest = max((row.get(i, 0) for h in [rh, qh] for i, row in enumerate(h)), default=0)
    # Residual after grid rounding is O(Lambda/Q). Charge rate-change weight too.
    precision = max(64, largest.bit_length() + max(1, weight.bit_length()) + 60 + shape.bit_length()) if precision is None else precision
    matrix_seconds = time.perf_counter() - before
    hr, rr, er, wr = solve_history(rh, ei, shape, shift, precision, exact_proposer)
    hq, rq, eqr, wq = solve_history(qh, ei, shape, shift, precision, exact_proposer)
    gl, terms = gamma_cdf_lower(shape, shift)
    lower_average = F(0)
    upper_average = F(0)
    for j in range(1, shape):
        lr, ur = hr[j - 1]
        lq, uq = hq[shape - j - 1]
        lower_average += sum(d * a * b for d, a, b in zip(delta, lr, lq))
        upper_average += sum(d * a * b for d, a, b in zip(delta, ur, uq))
    lower_average /= shape - 1
    upper_average /= shape - 1
    bound = upper_average / gl
    return dict(method="quadrature-free positive Erlang-resolvent Duhamel enclosure",
                graph=dict(n=n, edges=edges, original_rates=r, comparison_rates=q),
                horizon_exact="1", pair_states=len(rh), shape=shape, shift=shift,
                precision_bits=precision, gamma_cdf_lower_exact=str(gl), gamma_cdf_taylor_terms=terms,
                averaged_b_lower_exact=str(lower_average), averaged_b_upper_exact=str(upper_average),
                Duhamel_upper_exact=str(bound), Duhamel_upper_float=float(bound),
                tolerance_exact=str(tolerance), finite_generator_certified=bound <= tolerance,
                factor_receipts=[rr, rq], residual_receipts=[er, eqr],
                dyadic_solve_witnesses=[wr, wq],
                matrix_setup_seconds=matrix_seconds,
                wall_seconds=time.perf_counter() - before,
                peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                full_permutation_enumeration=False, survival_queries=0, time_quadrature_intervals=0,
                retained_history_scalars=2 * (shape - 1) * len(edges),
                delivered_witness_scalars=2 * (shape - 1) * len(rh),
                certificate_scope="finite original-to-comparison full endpoint TV, uniform initial permutation and color projections; averaging and finite-bit sampler errors additional")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--case", choices=["source20", "branch6", "ungapped6"], default="source20")
    p.add_argument("--shape", type=int, default=8)
    p.add_argument("--shift", type=int)
    p.add_argument("--exact-proposer", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.case == "source20":
        n = 20
        edges = [(j, j + 1) for j in range(n - 1)]
        r = [10 ** j for j in range(n - 1)]
        q = [1, 10] + [10 ** n] * (n - 3)
    else:
        n = 6
        edges = [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5)]
        r = [1, 10, 100, 1000, 10000] if a.case == "branch6" else [1] * 5
        q = r[:2] + [1000000] * 3
    result = certify(n, edges, r, q, a.shape, a.shift, exact_proposer=a.exact_proposer)
    result["case"] = a.case
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ["case", "pair_states", "shape", "Duhamel_upper_float", "finite_generator_certified", "wall_seconds", "peak_RSS_bytes"]}), flush=True)


if __name__ == "__main__":
    main()
