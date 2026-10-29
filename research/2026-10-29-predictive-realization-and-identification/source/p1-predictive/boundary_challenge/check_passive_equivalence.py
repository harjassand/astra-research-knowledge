#!/usr/bin/env python3
"""Exact supplied-source controls for passive mean equivalence.

No source sampling, measurement, or physical preparation. All arithmetic
underlying assertions is rational. Timings are wall time, not source time.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path
import time

F = Fraction


class Matrix:
    """Small independent exact matrix implementation used by these controls."""
    def __init__(self, values, rows=None, cols=None):
        if rows is not None:
            self.rows, self.cols = rows, cols
            self.a = [[F(0) for _ in range(cols)] for _ in range(rows)]
        else:
            values = list(values)
            if values and not isinstance(values[0], (list, tuple)):
                values = [[x] for x in values]
            self.rows = len(values)
            self.cols = len(values[0]) if values else 0
            self.a = [[F(x) for x in row] for row in values]

    def __len__(self):
        return self.rows * self.cols

    def __iter__(self):
        return (x for row in self.a for x in row)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.a[item // self.cols][item % self.cols]
        r, c = item
        if isinstance(r, int) and isinstance(c, int):
            return self.a[r][c]
        rr = list(range(self.rows))[r] if isinstance(r, slice) else [r]
        cc = list(range(self.cols))[c] if isinstance(c, slice) else [c]
        return self.extract(rr, cc)

    def __setitem__(self, item, value):
        if isinstance(item, int):
            self.a[item // self.cols][item % self.cols] = F(value)
            return
        r, c = item
        if isinstance(r, int) and isinstance(c, int):
            self.a[r][c] = F(value)
            return
        rr = list(range(self.rows))[r] if isinstance(r, slice) else [r]
        cc = list(range(self.cols))[c] if isinstance(c, slice) else [c]
        assert isinstance(value, Matrix) and (value.rows, value.cols) == (len(rr), len(cc))
        for i, ri in enumerate(rr):
            for j, cj in enumerate(cc):
                self.a[ri][cj] = value[i, j]

    def extract(self, rows, cols):
        out = Matrix([], len(rows), len(cols))
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                out[i, j] = self[r, c]
        return out

    def copy(self):
        return self.extract(list(range(self.rows)), list(range(self.cols)))

    @property
    def T(self):
        out = Matrix([], self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                out[j, i] = self[i, j]
        return out

    def __eq__(self, other):
        return isinstance(other, Matrix) and (self.rows, self.cols, self.a) == (other.rows, other.cols, other.a)

    def __add__(self, other):
        assert (self.rows, self.cols) == (other.rows, other.cols)
        out = self.copy()
        for i in range(self.rows):
            for j in range(self.cols):
                out[i, j] += other[i, j]
        return out

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            out = self.copy()
            for i in range(self.rows):
                for j in range(self.cols):
                    out[i, j] *= F(other)
            return out
        assert self.cols == other.rows
        out = Matrix([], self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                out[i, j] = sum((self[i, k] * other[k, j] for k in range(self.cols)), F(0))
        return out

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (F(1) / scalar)

    def inv(self):
        assert self.rows == self.cols
        n = self.rows
        a = [self.a[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
        for k in range(n):
            pivot = next(i for i in range(k, n) if a[i][k])
            a[k], a[pivot] = a[pivot], a[k]
            divisor = a[k][k]
            a[k] = [x / divisor for x in a[k]]
            for i in range(n):
                if i != k and a[i][k]:
                    factor = a[i][k]
                    a[i] = [x - factor * y for x, y in zip(a[i], a[k])]
        return Matrix([row[n:] for row in a])


class Exact:
    Matrix = Matrix
    MatrixBase = Matrix

    @staticmethod
    def zeros(rows, cols=None):
        return Matrix([], rows, rows if cols is None else cols)

    @staticmethod
    def ones(rows, cols):
        return Matrix([[1] * cols for _ in range(rows)])

    @staticmethod
    def eye(n):
        return Matrix([[int(i == j) for j in range(n)] for i in range(n)])

    @staticmethod
    def diag(*values):
        return Matrix([[values[i] if i == j else 0 for j in range(len(values))] for i in range(len(values))])


sp = Exact()


def matrix_block(M, rows, cols):
    return M.extract(list(rows), list(cols))


def laplacian(n, edges):
    L = sp.zeros(n)
    for u, v, g in edges:
        g = F(g)
        assert g > 0 and u != v
        L[u, u] += g
        L[v, v] += g
        L[u, v] -= g
        L[v, u] -= g
    assert L * sp.ones(n, 1) == sp.zeros(n, 1)
    return L


def record(L, w, B):
    B = list(B)
    I = [i for i in range(len(w)) if i not in B]
    G = matrix_block(L, I, I)
    J = matrix_block(L, I, B)
    wi = matrix_block(w, I, [0])
    wb = matrix_block(w, B, [0])
    if I:
        H = -G.inv() * J
        S = matrix_block(L, B, B) + J.T * H
        b = wb + H.T * wi
        c = (wi.T * G.inv() * wi)[0]
        assert H * sp.ones(len(B), 1) == sp.ones(len(I), 1)
        assert all(v >= 0 for v in H)
    else:
        H = sp.zeros(0, len(B))
        S, b, c = L.copy(), w.copy(), F(0)
    assert S * sp.ones(len(B), 1) == sp.zeros(len(B), 1)
    assert sum(b) == sum(w)
    assert all(v > 0 for v in b)
    return S, b, c, sum(w), H


def killed_mean(L, w, target):
    C = [i for i in range(len(w)) if i not in target]
    A = matrix_block(L, C, C)
    wc = matrix_block(w, C, [0])
    h = A.inv() * wc
    assert A * h == wc
    return (wc.T * h)[0] / sum(wc)


def passive_mean(L, w, B, t, z, g):
    """Build real pendant nodes and ground shunts; perform full solve."""
    active = [i for i, zi in enumerate(z) if zi]
    n = len(w)
    A = sp.zeros(n + len(active))
    A[:n, :n] = L
    ww = sp.Matrix(list(w) + [z[i] for i in active])
    for port in B:
        A[port, port] += t
    for j, i in enumerate(active):
        port, leaf = B[i], n + j
        A[port, port] += g[i]
        A[leaf, leaf] += g[i]
        A[port, leaf] -= g[i]
        A[leaf, port] -= g[i]
    h = A.inv() * ww
    assert A * h == ww
    return (ww.T * h)[0] / sum(ww)


def encode(x):
    if isinstance(x, sp.MatrixBase):
        return [[str(x[i, j]) for j in range(x.cols)] for i in range(x.rows)]
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def main():
    started = time.perf_counter()
    recovered = []
    passive_calls = 0
    boundary_target_checks = 0
    for case, n in enumerate([5, 6, 7, 8]):
        edges = [(i, i + 1, F(i + 2, case + 2)) for i in range(n - 1)]
        edges += [(0, n - 1, F(case + 1, 3)), (1, n - 2, F(2, 5))]
        L = laplacian(n, edges)
        w = sp.Matrix([F(i + 1, n + case + 1) for i in range(n)])
        B = [0, 2, n - 1]
        S, b, c, mu, _ = record(L, w, B)
        k, t = len(B), F(2, 3)
        g = [F(1), F(2), F(3)]
        cache = {}

        def observe(z):
            nonlocal passive_calls
            z = tuple(z)
            if z not in cache:
                T = passive_mean(L, w, B, t, z, g)
                cache[z] = (mu + sum(z)) * T - sum(zi * zi / gi for zi, gi in zip(z, g))
                passive_calls += 1
            return cache[z]

        zero = [F(0)] * k
        f0 = observe(zero)
        M, d = sp.zeros(k), sp.zeros(k, 1)
        singles = []
        for i in range(k):
            z = zero.copy()
            z[i] = 1
            f1 = observe(z)
            singles.append(f1)
            z[i] = 2
            f2 = observe(z)
            M[i, i] = (f2 - 2 * f1 + f0) / 2
            d[i] = f1 - f0 - M[i, i]
        for i in range(k):
            for j in range(i + 1, k):
                z = zero.copy()
                z[i] = z[j] = 1
                M[i, j] = M[j, i] = (observe(z) - singles[i] - singles[j] + f0) / 2
        Sr = M.inv() - t * sp.eye(k)
        br = M.inv() * d / 2
        cr = f0 - (br.T * M * br)[0]
        assert Sr == S and br == b and cr == c
        assert len(cache) == (k + 1) * (k + 2) // 2
        for size in range(1, k + 1):
            for a in itertools.combinations(range(k), size):
                R = [j for j in range(k) if j not in a]
                numerator = c
                if R:
                    bb = matrix_block(b, R, [0])
                    numerator += (bb.T * matrix_block(S, R, R).inv() * bb)[0]
                T = numerator / (mu - sum(w[B[j]] for j in a))
                assert T == killed_mean(L, w, {B[j] for j in a})
                boundary_target_checks += 1
        recovered.append({"states": n, "boundary": B, "passive_queries": len(cache), "S": S, "b": b, "c": c})

    # Entire first jet fixed but the equilibrium residual is unbounded.
    trap_checks = []
    for exponent in [0, 4, 16, 64]:
        d = F(1, 2**exponent)
        L = laplacian(3, [(0, 1, 1), (0, 2, d)])
        w = sp.ones(3, 1)
        S, b, c, mu, H = record(L, w, [0, 1])
        Kprime = sp.eye(2) + H.T * H
        assert S == sp.Matrix([[1, -1], [-1, 1]])
        assert b == sp.Matrix([2, 1]) and c == 1 / d
        assert Kprime == sp.diag(2, 1)
        T = killed_mean(L, w, {1})
        assert T == 2 + 1 / (2 * d)
        # Boundary-started Poisson fields remain fixed at 2 and 1.
        for target, start, expected in [(1, 0, 2), (0, 1, 1)]:
            C = [i for i in range(3) if i != target]
            h = matrix_block(L, C, C).inv() * sp.ones(2, 1)
            assert h[C.index(start)] == expected
        trap_checks.append({"d": d, "c": c, "mean_to_1": T})

    # Equal complete mean record, different memory and survival law.
    modules = [
        (laplacian(2, [(0, 1, 1)]), sp.Matrix([1, 1])),
        (laplacian(3, [(0, 1, 1), (0, 2, F(1, 3))]), sp.Matrix([1, F(1, 2), F(1, 2)])),
    ]
    pair_results = []
    for L, w in modules:
        S, b, c, mu, _ = record(L, w, [0])
        assert S == sp.zeros(1) and b == sp.Matrix([2]) and c == 1 and mu == 2
        I = list(range(1, len(w)))
        D = sp.diag(*list(w))
        Ginv = matrix_block(L, I, I).inv()
        J = matrix_block(L, I, [0])
        Di = matrix_block(D, I, I)
        power = Ginv * J
        jet = [S[0]]
        for j in range(1, 4):
            power = Ginv * Di * power
            coefficient = (-1) ** (j + 1) * (J.T * power)[0]
            if j == 1:
                coefficient += w[0]
            jet.append(coefficient)
        A = L.copy()
        A[0, 0] += 1
        h = A.inv() * w
        mean = (w.T * h)[0] / sum(w)
        second = 2 * (h.T * D * h)[0] / sum(w)
        laplace_survival_at_one = (w.T * (A + D).inv() * w)[0] / sum(w)
        pair_results.append({"states": len(w), "jet_coefficients_0_to_3": jet, "mean": mean, "second_moment": second, "laplace_survival_at_1": laplace_survival_at_one})
    assert pair_results[0]["jet_coefficients_0_to_3"] == [0, 2, -1, 1]
    assert pair_results[1]["jet_coefficients_0_to_3"] == [0, 2, -1, F(5, 4)]
    assert [x["mean"] for x in pair_results] == [F(5, 2)] * 2
    assert [x["second_moment"] for x in pair_results] == [13, F(53, 4)]
    assert pair_results[0]["laplace_survival_at_1"] != pair_results[1]["laplace_survival_at_1"]
    pair_passive_checks = 0
    for t, z in itertools.product([F(1, 2), F(1), F(2), F(7)], [F(0), F(1, 2), F(3)]):
        values = [passive_mean(L, w, [0], t, [z], [F(2)]) for L, w in modules]
        predicted = (1 + z * z / 2 + (2 + z) ** 2 / t) / (2 + z)
        assert values == [predicted, predicted]
        pair_passive_checks += 1

    # Same S,b,c does not compile the same native killing hazard without w_B.
    native_hazard_boundary = []
    for x in [F(1), F(1, 2)]:
        w = sp.Matrix([x, 2 - x])
        L = laplacian(2, [(0, 1, (2 - x) ** 2)])
        S, b, c, mu, _ = record(L, w, [0])
        assert S == sp.zeros(1) and b == sp.Matrix([2]) and c == 1 and mu == 2
        A = L.copy()
        A[0, 0] += x  # Same native killing rate 1, different conductance.
        h = A.inv() * w
        mean = (w.T * h)[0] / sum(w)
        assert mean == F(1, 2) + 2 / x
        native_hazard_boundary.append({"port_mass": x, "native_hazard": 1, "mean": mean})

    # All whole-module target unions on a nontrivial physical assembly.
    local = []
    for j in range(4):
        edges = [(0, 2, F(j + 1, 2)), (2, 3, F(j + 2, 3)), (3, 1, F(j + 3, 5)), (0, 1, F(1, j + 4))]
        w = sp.Matrix([F(j + i + 1, 5) for i in range(4)])
        L = laplacian(4, edges)
        local.append((L, w, record(L, w, [0, 1])))
    global_L, global_w = sp.zeros(16), sp.zeros(16, 1)
    for j, (L, w, _) in enumerate(local):
        global_L[4 * j:4 * j + 4, 4 * j:4 * j + 4] = L
        global_w[4 * j:4 * j + 4, 0] = w
    cross = [((j, 1), ((j + 1) % 4, 0), F(j + 1, 7)) for j in range(4)]
    cross += [((0, 0), (2, 1), F(2, 9)), ((1, 1), (3, 0), F(3, 8))]
    for (j, p), (k, q), g in cross:
        u, v = 4 * j + p, 4 * k + q
        global_L[u, u] += g
        global_L[v, v] += g
        global_L[u, v] -= g
        global_L[v, u] -= g
    assembly = []
    for size in range(1, 4):
        for target_modules in itertools.combinations(range(4), size):
            live = [j for j in range(4) if j not in target_modules]
            ports = [(j, p) for j in live for p in [0, 1]]
            idx = {v: i for i, v in enumerate(ports)}
            K, bb, cc, mass = sp.zeros(len(ports)), sp.zeros(len(ports), 1), F(0), F(0)
            for j in live:
                S, b, c, mu, _ = local[j][2]
                slots = [idx[(j, 0)], idx[(j, 1)]]
                for p in range(2):
                    bb[slots[p]] = b[p]
                    for q in range(2):
                        K[slots[p], slots[q]] += S[p, q]
                cc += c
                mass += mu
            for u, v, g in cross:
                if u in idx:
                    K[idx[u], idx[u]] += g
                if v in idx:
                    K[idx[v], idx[v]] += g
                if u in idx and v in idx:
                    K[idx[u], idx[v]] -= g
                    K[idx[v], idx[u]] -= g
            reduced_energy = (bb.T * K.inv() * bb)[0]
            predicted = (cc + reduced_energy) / mass
            target = {4 * j + i for j in target_modules for i in range(4)}
            direct = killed_mean(global_L, global_w, target)
            assert predicted == direct
            assert cc > 0
            assembly.append({"target_modules": list(target_modules), "full_live_states": 16 - len(target), "retained_live_ports": len(ports), "mean": predicted, "relative_error_if_residual_omitted": cc / (cc + reduced_energy)})

    result = {
        "status": "PASS",
        "arithmetic": "exact fractions.Fraction with independent small-matrix elimination; no floating assertions",
        "source_access": "supplied finite matrices only; zero statistical/physical assays",
        "passive_identifiability_full_solve_queries": passive_calls,
        "boundary_target_mean_checks": boundary_target_checks,
        "passive_recovered_records": recovered,
        "first_jet_trap_checks": trap_checks,
        "same_record_different_survival": pair_results,
        "same_record_passive_attachment_checks": pair_passive_checks,
        "native_hazard_requires_boundary_mass": native_hazard_boundary,
        "whole_region_union_checks": len(assembly),
        "assembly": assembly,
        "wall_seconds": time.perf_counter() - started,
        "claims_not_established": ["efficient source acquisition", "unknown boundary discovery", "speed superiority over equally informed direct elimination", "all-survival-law equivalence", "historical novelty"],
    }
    destination = Path(__file__).with_name("PASSIVE_EQUIVALENCE_CHECKS.json")
    destination.write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps({"status": result["status"], "passive_queries": passive_calls, "boundary_targets": boundary_target_checks, "region_unions": len(assembly), "pair_second_moments": [str(x["second_moment"]) for x in pair_results], "wall_seconds": result["wall_seconds"], "output": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
