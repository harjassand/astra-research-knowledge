#!/usr/bin/env python3
"""Mass-carrying quotient, tree residual output certificate, independent checks.

No package installation or repository mutations. NumPy/SciPy is used only for
trial potentials. Decimal directed arithmetic independently verifies arbitrary
trial potentials against exact supplied float coefficients or coefficient bands.
"""
from __future__ import annotations
import argparse
import dataclasses
import decimal
from decimal import Decimal as D
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy import sparse
from scipy.sparse import csgraph
from scipy.sparse.linalg import splu


@dataclasses.dataclass
class Graph:
    n: int
    u: np.ndarray
    v: np.ndarray
    c: np.ndarray
    w: np.ndarray
    s: int = 0
    t: int = 1
    c_bounds: list | None = None
    w_bounds: list | None = None


class DSU:
    def __init__(self, n, s=-1, t=-1):
        self.p = np.arange(n)
        self.sz = np.ones(n, dtype=np.int64)
        self.tag = np.zeros(n, dtype=np.int8)
        if s >= 0:
            self.tag[s] = 1
        if t >= 0:
            self.tag[t] = 2

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return int(x)

    def join(self, x, y, protect=True):
        x, y = self.find(x), self.find(y)
        if x == y or (protect and (self.tag[x] | self.tag[y]) == 3):
            return False
        if self.sz[x] < self.sz[y]:
            x, y = y, x
        self.p[y] = x
        self.sz[x] += self.sz[y]
        self.tag[x] |= self.tag[y]
        return True


def select_partition(g: Graph, k: int, prune_leaves=True):
    """Terminal-protected maximum-conductance contractions and tree receipt."""
    d = DSU(g.n, g.s, g.t)
    chosen = []
    if prune_leaves:
        adj = [[] for _ in range(g.n)]
        for e, (i, j) in enumerate(zip(g.u, g.v)):
            adj[int(i)].append((int(j), e))
            adj[int(j)].append((int(i), e))
        deg = np.array([len(a) for a in adj])
        removed = np.zeros(g.n, dtype=bool)
        queue = [i for i in range(g.n) if deg[i] == 1 and i not in (g.s, g.t)]
        for i in queue:
            if removed[i]:
                continue
            for j, e in adj[i]:
                if not removed[j]:
                    if d.join(i, j):
                        chosen.append(e)
                    removed[i] = True
                    deg[j] -= 1
                    if deg[j] == 1 and j not in (g.s, g.t):
                        queue.append(j)
                    break
    k = max(2, min(k, g.n - len(chosen)))
    order = np.argsort(-g.c, kind="stable")
    for e in order:
        if g.n - len(chosen) <= k:
            break
        if d.join(int(g.u[e]), int(g.v[e])):
            chosen.append(int(e))
    roots = np.array([d.find(i) for i in range(g.n)])
    _, part = np.unique(roots, return_inverse=True)
    # Add a tree of intercluster edges: arbitrary coarse solver errors can drain.
    fulltree = list(chosen)
    for e in order:
        if d.join(int(g.u[e]), int(g.v[e]), protect=False):
            fulltree.append(int(e))
    if len(fulltree) != g.n - 1:
        raise ValueError("Graph is disconnected")
    return part, np.asarray(fulltree, dtype=np.int64), len(chosen)


def grounded_matrix(g: Graph, part=None, keep=None):
    if part is None:
        part = np.arange(g.n)
    k = int(part.max()) + 1
    if keep is None:
        keep = np.ones(len(g.c), dtype=bool)
    u, v = part[g.u[keep]], part[g.v[keep]]
    c = g.c[keep]
    good = u != v
    u, v, c = u[good], v[good], c[good]
    adj = sparse.coo_matrix((np.r_[c, c], (np.r_[u, v], np.r_[v, u])), shape=(k, k)).tocsr()
    adj.sum_duplicates()
    A = sparse.diags(np.ravel(adj.sum(axis=1))) - adj
    target = int(part[g.t])
    mask = np.arange(k) != target
    A = A.tocsc()[mask][:, mask]
    w = np.bincount(part, weights=g.w, minlength=k)[mask]
    a = np.zeros(k)
    a[part[g.s]] = 1
    return A, a[mask], w, mask, adj.nnz // 2


def trial_solve(g: Graph, part=None, keep=None):
    A, a, w, mask, mcore = grounded_matrix(g, part, keep)
    t0 = time.perf_counter()
    diag = A.diagonal()
    if np.any(diag <= 0) or not np.all(np.isfinite(diag)):
        raise ArithmeticError("Invalid coarse matrix diagonal")
    d = 1.0 / np.sqrt(diag)
    Ae = sparse.diags(d).dot(A).dot(sparse.diags(d)).tocsc()
    lu = splu(Ae, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0)
    rhs = np.column_stack((a, w))
    ans = d[:, None] * lu.solve(d[:, None] * rhs)
    full = np.zeros((len(mask), 2))
    full[mask] = ans
    if part is not None:
        full = full[part]
    if not np.all(np.isfinite(full)):
        raise ArithmeticError("Nonfinite trial solve")
    return full[:, 0], full[:, 1], dict(
        solve_seconds=time.perf_counter() - t0,
        core_states=len(mask), core_edges=mcore,
        lu_nnz=int(lu.L.nnz + lu.U.nnz),
        approximate_mfpt=float(full[g.s, 1]),
        minimum_trial_value=float(full.min()),
    )


def root_tree(g: Graph, tree):
    adj = [[] for _ in range(g.n)]
    for e in tree:
        i, j = int(g.u[e]), int(g.v[e])
        adj[i].append((j, int(e)))
        adj[j].append((i, int(e)))
    parent = np.full(g.n, -1, dtype=np.int64)
    pedge = np.full(g.n, -1, dtype=np.int64)
    order = [g.t]
    parent[g.t] = g.t
    for i in order:
        for j, e in adj[i]:
            if parent[j] < 0:
                parent[j], pedge[j] = i, e
                order.append(j)
    if len(order) != g.n:
        raise ValueError("Routing tree is not spanning")
    return parent, pedge, order


def cycle_blocks(g: Graph):
    """Iterative Tarjan edge blocks; handles parallel edges by edge identity.

    Every cycle is wholly within one block. Thus the edge-space orthogonal
    projector onto the cycle space, and its complement P, are block diagonal.
    One-edge blocks are bridges with P=I exactly.
    """
    adj = [[] for _ in range(g.n)]
    for e, (i, j) in enumerate(zip(g.u, g.v)):
        i, j = int(i), int(j)
        adj[i].append((j, e))
        adj[j].append((i, e))
    disc = np.full(g.n, -1, dtype=np.int64)
    low = np.full(g.n, -1, dtype=np.int64)
    parent = np.full(g.n, -1, dtype=np.int64)
    pe = np.full(g.n, -1, dtype=np.int64)
    edgeblock = np.full(len(g.c), -1, dtype=np.int64)
    estack = []
    counter = blocks = 0
    for root in range(g.n):
        if disc[root] >= 0:
            continue
        disc[root] = low[root] = counter
        counter += 1
        stack = [[root, 0]]
        while stack:
            i, ix = stack[-1]
            if ix < len(adj[i]):
                j, e = adj[i][ix]
                stack[-1][1] += 1
                if disc[j] < 0:
                    parent[j], pe[j] = i, e
                    disc[j] = low[j] = counter
                    counter += 1
                    estack.append(e)
                    stack.append([j, 0])
                elif e != pe[i] and disc[j] < disc[i]:
                    low[i] = min(low[i], disc[j])
                    estack.append(e)
            else:
                stack.pop()
                p = int(parent[i])
                if p >= 0:
                    low[p] = min(low[p], low[i])
                    if low[i] >= disc[p]:
                        while True:
                            e = estack.pop()
                            edgeblock[e] = blocks
                            if e == pe[i]:
                                break
                        blocks += 1
    if np.any(edgeblock < 0):
        raise AssertionError("Unassigned edge block")
    return edgeblock, np.bincount(edgeblock, minlength=blocks)


def diagnostic_certificate(g: Graph, x, y, tree, blocks=None):
    """Long-double diagnostic only, not advertised as a rounding certificate."""
    typ = np.longdouble
    x, y, c = x.astype(typ), y.astype(typ), g.c.astype(typ)
    ra = np.zeros(g.n, dtype=typ)
    ra[g.s] = 1
    rb = g.w.astype(typ).copy()
    rb[g.t] = 0
    for z, r in ((x, ra), (y, rb)):
        f = c * (z[g.u] - z[g.v])
        np.add.at(r, g.u, -f)
        np.add.at(r, g.v, f)
    t0 = y[g.s] + np.sum(x * rb, dtype=typ)
    parent, pedge, order = root_tree(g, tree)
    fa, fb = ra.copy(), rb.copy()
    edgeblock, sizes = cycle_blocks(g) if blocks is None else blocks
    ea, eb, jvals = (np.zeros(len(sizes), dtype=typ) for _ in range(3))
    local = []
    for i in reversed(order[1:]):
        e = pedge[i]
        bid = edgeblock[e]
        a, b = fa[i], fb[i]
        ea[bid] += a * a / c[e]
        eb[bid] += b * b / c[e]
        jvals[bid] += a * b / c[e]
        local.append((float(abs(a * b / c[e])), int(e)))
        fa[parent[i]] += a
        fb[parent[i]] += b
    bridge = sizes == 1
    rad = np.sqrt(ea[~bridge] * eb[~bridge]).sum() / 2
    mid = t0 + jvals[bridge].sum() + jvals[~bridge].sum() / 2
    lo, hi = max(typ(0), mid - rad), mid + rad
    return dict(lower=float(lo), upper=float(hi), center=float(mid),
                relative_width=float(hi / lo - 1) if lo > 0 else None,
                E_source=str(ea.sum()), E_mass=str(eb.sum()), J=str(jvals.sum()),
                cycle_blocks=len(sizes), bridge_blocks=int(bridge.sum()),
                global_product_radius=str(np.sqrt(ea.sum() * eb.sum()) / 2),
                blockwise_radius=str(rad),
                top_local_mixed_edges=sorted(local, reverse=True)[:8],
                status="longdouble_diagnostic_not_rounding_certified")


def forest_partition(g, edges):
    d = DSU(g.n)
    for e in edges:
        d.join(int(g.u[e]), int(g.v[e]), protect=False)
    roots = np.array([d.find(i) for i in range(g.n)])
    return np.unique(roots, return_inverse=True)[1]


def refinement_scores(g, x, y, tree, blocks):
    typ = np.longdouble
    x, y, c = x.astype(typ), y.astype(typ), g.c.astype(typ)
    ra = np.zeros(g.n, dtype=typ)
    ra[g.s] = 1
    rb = g.w.astype(typ).copy()
    rb[g.t] = 0
    for pot, res in ((x, ra), (y, rb)):
        f = c * (pot[g.u] - pot[g.v])
        np.add.at(res, g.u, -f)
        np.add.at(res, g.v, f)
    parent, pedge, order = root_tree(g, tree)
    ea, eb = np.zeros(len(c), dtype=typ), np.zeros(len(c), dtype=typ)
    for i in reversed(order[1:]):
        e = pedge[i]
        ea[e], eb[e] = ra[i] * ra[i] / c[e], rb[i] * rb[i] / c[e]
        ra[parent[i]] += ra[i]
        rb[parent[i]] += rb[i]
    bids, sizes = blocks
    a = np.bincount(bids, weights=ea.astype(float), minlength=len(sizes)).astype(typ)
    b = np.bincount(bids, weights=eb.astype(float), minlength=len(sizes)).astype(typ)
    score = np.zeros(len(c), dtype=typ)
    for e in tree:
        bid = bids[e]
        if sizes[bid] > 1 and a[bid] > 0 and b[bid] > 0:
            score[e] = (np.sqrt(b[bid] / a[bid]) * ea[e]
                        + np.sqrt(a[bid] / b[bid]) * eb[e]) / 4
    return score


def adaptive_reduction(g, start_k=20, max_k=10000, tol=.01, prec=80, certify=True):
    """A posteriori forest refinement; scores are heuristic, certificate is not.

    Split only previously contracted forest edges. Scores are the derivatives
    of the blockwise product budget with respect to the two edge energies.
    Retain every original intercluster edge and all masses after each split.
    """
    begun = time.perf_counter()
    part, tree, contractions = select_partition(g, start_k)
    contracted = set(tree[:contractions].tolist())
    bstart = time.perf_counter()
    blocks = cycle_blocks(g)
    block_seconds = time.perf_counter() - bstart
    rows = []
    accepted = False
    while True:
        tstart = time.perf_counter()
        x, y, info = trial_solve(g, part)
        diag = diagnostic_certificate(g, x, y, tree, blocks)
        rows.append(dict(**info, diagnostic=diag, iteration_seconds=time.perf_counter() - tstart))
        width = diag["relative_width"]
        if width is not None and width <= tol:
            accepted = True
            break
        k = info["core_states"]
        if k >= max_k or not contracted:
            break
        scores = refinement_scores(g, x, y, tree, blocks)
        candidates = np.asarray(sorted(contracted), dtype=np.int64)
        batch = min(max_k - k, max(20, k), len(candidates))
        chosen = candidates[np.argsort(-scores[candidates], kind="stable")[:batch]]
        contracted.difference_update(chosen.tolist())
        part = forest_partition(g, sorted(contracted))
    cert = interval_certificate(g, x, y, tree, prec, blocks) if certify else None
    if cert:
        accepted = cert["relative_width"] is not None and D(cert["relative_width"]) <= D(str(tol))
    return dict(iterations=rows, certificate=cert, accepted=accepted,
                block_preprocessing_seconds=block_seconds,
                total_seconds=time.perf_counter() - begun,
                acceptance_scope="relative_directional_mean_interval_width", tolerance=tol)


class Intervals:
    def __init__(self, prec=80):
        self.lo = decimal.Context(prec=prec, rounding=decimal.ROUND_FLOOR,
                                  Emin=-999999999, Emax=999999999)
        self.hi = decimal.Context(prec=prec, rounding=decimal.ROUND_CEILING,
                                  Emin=-999999999, Emax=999999999)
        self.prec = prec

    def add(self, a, b):
        return self.lo.add(a[0], b[0]), self.hi.add(a[1], b[1])

    def sub(self, a, b):
        return self.lo.subtract(a[0], b[1]), self.hi.subtract(a[1], b[0])

    def mul(self, a, b):
        return (min(self.lo.multiply(i, j) for i in a for j in b),
                max(self.hi.multiply(i, j) for i in a for j in b))

    def divpos(self, a, b):
        if b[0] <= 0:
            raise ValueError("Positive divisor lower bound required")
        return (min(self.lo.divide(i, j) for i in a for j in b),
                max(self.hi.divide(i, j) for i in a for j in b))

    def exp(self, a):
        # Decimal exp is correctly rounded, ROUND_HALF_EVEN. One neighbor
        # outward encloses the exact result even when exactness is unknown.
        return (self.lo.next_minus(self.lo.exp(a[0])),
                self.hi.next_plus(self.hi.exp(a[1])))

    def sqrtup(self, a):
        return self.hi.next_plus(self.hi.sqrt(a))

    @staticmethod
    def exact(x):
        d = D.from_float(float(x))
        return d, d


def interval_certificate(g: Graph, x, y, tree, prec=80, blocks=None):
    """Rigorous enclosure conditional on Python Decimal's documented rounding.

    The verification includes every original edge and mass, approximate-solve
    errors, tree routing and final square root. No cancellation is assumed exact.
    Optional input bands allow uniform certification over model coefficients.
    """
    tstart = time.perf_counter()
    iv = Intervals(prec)
    zero = (D(0), D(0))
    xx, yy = [iv.exact(z) for z in x], [iv.exact(z) for z in y]
    cc = g.c_bounds if g.c_bounds is not None else [iv.exact(z) for z in g.c]
    ww = g.w_bounds if g.w_bounds is not None else [iv.exact(z) for z in g.w]
    ra = [zero for _ in range(g.n)]
    ra[g.s] = (D(1), D(1))
    rb = list(ww)
    rb[g.t] = zero
    for e, (i, j) in enumerate(zip(g.u, g.v)):
        i, j = int(i), int(j)
        for pot, res in ((xx, ra), (yy, rb)):
            flux = iv.mul(cc[e], iv.sub(pot[i], pot[j]))
            res[i] = iv.sub(res[i], flux)
            res[j] = iv.add(res[j], flux)
    t0 = yy[g.s]
    for i in range(g.n):
        if i != g.t:
            t0 = iv.add(t0, iv.mul(xx[i], rb[i]))
    parent, pedge, order = root_tree(g, tree)
    edgeblock, sizes = cycle_blocks(g) if blocks is None else blocks
    ea, eb = [D(0) for _ in sizes], [D(0) for _ in sizes]
    jj = [zero for _ in sizes]
    for i in reversed(order[1:]):
        e = int(pedge[i])
        bid = int(edgeblock[e])
        # Decimal.__abs__ follows the ambient context (often precision 28).
        # copy_abs is exact and avoids silently shrinking an upper bound.
        aa, bb = max(z.copy_abs() for z in ra[i]), max(z.copy_abs() for z in rb[i])
        ea[bid] = iv.hi.add(ea[bid], iv.hi.divide(iv.hi.multiply(aa, aa), cc[e][0]))
        eb[bid] = iv.hi.add(eb[bid], iv.hi.divide(iv.hi.multiply(bb, bb), cc[e][0]))
        jj[bid] = iv.add(jj[bid], iv.divpos(iv.mul(ra[i], rb[i]), cc[e]))
        p = int(parent[i])
        ra[p], rb[p] = iv.add(ra[p], ra[i]), iv.add(rb[p], rb[i])
    radius, mid, jjall, eaall, eball = D(0), t0, zero, D(0), D(0)
    for k, size in enumerate(sizes):
        eaall, eball = iv.hi.add(eaall, ea[k]), iv.hi.add(eball, eb[k])
        jjall = iv.add(jjall, jj[k])
        if size == 1:
            # A bridge is always in the gradient subspace: no uncertainty.
            mid = iv.add(mid, jj[k])
        else:
            radius = iv.hi.add(radius, iv.hi.divide(iv.sqrtup(iv.hi.multiply(ea[k], eb[k])), D(2)))
            mid = iv.add(mid, (iv.lo.divide(jj[k][0], D(2)), iv.hi.divide(jj[k][1], D(2))))
    lower = max(D(0), iv.lo.subtract(mid[0], radius))
    upper = iv.hi.add(mid[1], radius)
    width = iv.hi.subtract(iv.hi.divide(upper, lower), D(1)) if lower > 0 else None
    return dict(lower=str(lower), upper=str(upper),
                relative_width=str(width) if width is not None else None,
                E_source_upper=str(eaall), E_mass_upper=str(eball),
                J_lower=str(jjall[0]), J_upper=str(jjall[1]),
                cycle_blocks=len(sizes), bridge_blocks=int((sizes == 1).sum()),
                global_product_radius_upper=str(iv.hi.divide(iv.sqrtup(iv.hi.multiply(eaall, eball)), D(2))),
                blockwise_radius_upper=str(radius),
                certificate_seconds=time.perf_counter() - tstart,
                precision=prec,
                coefficient_scope="supplied_coefficient_bands" if g.c_bounds else "exact_binary64_input_graph",
                arithmetic_scope="Python_Decimal_directed_rounding_conditional_certificate")


def exact_solve(g):
    """Independent Fraction Gaussian elimination, research checks only."""
    mask = [i for i in range(g.n) if i != g.t]
    pos = {i: j for j, i in enumerate(mask)}
    A = [[F(0) for _ in mask] for _ in mask]
    for i, j, c in zip(g.u, g.v, g.c):
        c = F(float(c))
        for a in (int(i), int(j)):
            if a in pos:
                A[pos[a]][pos[a]] += c
        if i in pos and j in pos:
            A[pos[i]][pos[j]] -= c
            A[pos[j]][pos[i]] -= c
    b = [F(float(g.w[i])) for i in mask]
    n = len(mask)
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ArithmeticError("zero exact pivot")
        for i in range(k + 1, n):
            factor = A[i][k] / pivot
            if factor:
                for j in range(k + 1, n):
                    A[i][j] -= factor * A[k][j]
                b[i] -= factor * b[k]
    x = [F(0) for _ in mask]
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x[pos[g.s]]


def graph(n, edges, masses, s=0, t=1):
    return Graph(n, np.asarray([e[0] for e in edges], dtype=np.int64),
                 np.asarray([e[1] for e in edges], dtype=np.int64),
                 np.asarray([e[2] for e in edges], dtype=float),
                 np.asarray(masses, dtype=float), s, t)


def rational_checks(count=100):
    rng = np.random.default_rng(20261015)
    rows = []
    for run in range(count):
        n = int(rng.integers(4, 12))
        edges = [(i, int(rng.integers(0, i)), float(rng.integers(1, 50)) / 16) for i in range(1, n)]
        for i in range(n):
            for j in range(i):
                if rng.random() < .2:
                    edges.append((i, j, float(rng.integers(1, 50)) / 32))
        g = graph(n, edges, rng.integers(1, 200, size=n) / 16)
        part, tree, _ = select_partition(g, int(rng.integers(2, n + 1)), False)
        # Random non-tree deletions test the arbitrary-potential verifier too.
        keep = np.ones(len(edges), dtype=bool)
        protected = set(tree.tolist())
        for e in range(len(edges)):
            if e not in protected and rng.random() < .3:
                keep[e] = False
        x, y, info = trial_solve(g, part, keep)
        cert = interval_certificate(g, x, y, tree, 80)
        exact = exact_solve(g)
        lower, upper = F(D(cert["lower"])), F(D(cert["upper"]))
        if not lower <= exact <= upper:
            raise AssertionError((run, cert, exact))
        rows.append(dict(run=run, states=n, edges=len(edges), core_states=info["core_states"],
                         deleted_edges=int((~keep).sum()), exact_mfpt=str(exact), **cert))
    # Stress the known source-/target-leaf distinction with arbitrarily slow leaf.
    examples = []
    for name, edges, masses in [
        ("source_weak_heavy_leaf", [(0, 1, 1), (0, 2, 2.0**-40)], [1, 1, 2.0**40]),
        ("target_weak_heavy_leaf", [(0, 1, 1), (1, 2, 2.0**-40)], [1, 1, 2.0**40]),
        ("internal_bottleneck_obstruction", [(0, 2, 2.0**-20), (2, 1, 1)], [1, 1, 2.0**20]),
    ]:
        g = graph(3, edges, masses)
        # In the obstruction, force z into the source cluster.
        if name == "internal_bottleneck_obstruction":
            part, tree = np.array([0, 1, 0]), np.array([0, 1])
        else:
            part, tree, _ = select_partition(g, 2)
        x, y, info = trial_solve(g, part)
        cert = interval_certificate(g, x, y, tree, 100)
        exact = exact_solve(g)
        assert F(D(cert["lower"])) <= exact <= F(D(cert["upper"]))
        examples.append(dict(name=name, exact_mfpt=str(exact), **info, **cert))
    return dict(seed=20261015, checks=count, failures=0, random_checks=rows, stress_examples=examples)


def synthetic(cluster_count=20, per_cluster=30, leaves=200):
    rng = np.random.default_rng(719)
    ncore = cluster_count * per_cluster
    n = ncore + leaves
    edges = []
    # Dense within-basin transitions; sparse slow nearest-basin links.
    for cl in range(cluster_count):
        nodes = range(cl * per_cluster, (cl + 1) * per_cluster)
        for i in nodes:
            for j in range(cl * per_cluster, i):
                edges.append((i, j, 1.0e8 * (1 + rng.random())))
    for cl in range(cluster_count - 1):
        edges.append((cl * per_cluster, (cl + 1) * per_cluster, 0.7 + rng.random()))
        edges.append((cl * per_cluster + 1, (cl + 1) * per_cluster + 1, 0.7 + rng.random()))
    w = np.exp(rng.normal(size=n))
    for z in range(leaves):
        attach = int(rng.integers(ncore))
        edges.append((attach, ncore + z, 1e-10 * (1 + rng.random())))
        w[ncore + z] *= 1e6
    return graph(n, edges, w, s=0, t=(cluster_count - 1) * per_cluster)


def run_reductions(g, ks, certify=True, prec=80):
    rows = []
    for k in ks:
        started = time.perf_counter()
        part, tree, contractions = select_partition(g, k)
        selection_seconds = time.perf_counter() - started
        try:
            x, y, info = trial_solve(g, part)
            row = dict(requested_states=k, contractions=contractions,
                       selection_seconds=selection_seconds, **info,
                       diagnostic=diagnostic_certificate(g, x, y, tree))
            if certify:
                row["certificate"] = interval_certificate(g, x, y, tree, prec)
            row["total_seconds"] = time.perf_counter() - started
        except Exception as exc:
            row = dict(requested_states=k, error=repr(exc),
                       selection_seconds=selection_seconds,
                       total_seconds=time.perf_counter() - started)
        rows.append(row)
    return rows


def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while data := f.read(1024 * 1024):
            h.update(data)
    return h.hexdigest()


def two_pi_band(prec=80):
    """Exact alternating-series bounds from Machin's identity, no stored pi."""
    eps = F(1, 10 ** (prec + 8))
    def atan_band(den):
        total, n = F(0), 0
        while True:
            term = F(1, (2 * n + 1) * den ** (2 * n + 1))
            if term < eps:
                return (total, total + term) if n % 2 == 0 else (total - term, total)
            total += term if n % 2 == 0 else -term
            n += 1
    al, ah = atan_band(5)
    bl, bh = atan_band(239)
    lower, upper = 2 * (16 * al - 4 * bh), 2 * (16 * ah - 4 * bl)
    iv = Intervals(prec)
    return (iv.lo.divide(D(lower.numerator), D(lower.denominator)),
            iv.hi.divide(D(upper.numerator), D(upper.denominator)))


def htst_time_interval(cert, prec=80):
    iv = Intervals(prec)
    scaled = iv.mul((D(cert["lower"]), D(cert["upper"])), two_pi_band(prec))
    return dict(lower=str(scaled[0]), upper=str(scaled[1]),
                units="reduced_Lennard_Jones_HTST_time",
                two_pi_enclosure="Machin_alternating_series_with_exact_Fraction_remainders")


def load_lj38(path, temp="0.2", intervals=False, prec=80, source_id=1, target_id=2):
    """Read full public decimal model; no unstated funnel labels or truncation."""
    start = time.perf_counter()
    path = Path(path)
    mins = np.loadtxt(path / "min.data")
    ts = np.loadtxt(path / "ts.data")
    u, v = ts[:, 3].astype(np.int64) - 1, ts[:, 4].astype(np.int64) - 1
    valid = u != v
    u, v, tsidx = u[valid], v[valid], np.flatnonzero(valid)
    adj = sparse.coo_matrix((np.ones(2 * len(u)), (np.r_[u, v], np.r_[v, u])), shape=(len(mins), len(mins))).tocsr()
    nc, comp = csgraph.connected_components(adj, directed=False)
    sizes = np.bincount(comp)
    chosen = int(np.argmax(sizes))
    selected = comp == chosen
    if not (selected[source_id - 1] and selected[target_id - 1]):
        raise ValueError("Requested IDs not both in largest component")
    nodeids = np.flatnonzero(selected)
    mapping = np.full(len(mins), -1, dtype=np.int64)
    mapping[nodeids] = np.arange(len(nodeids))
    edgeok = selected[u] & selected[v]
    u, v, tsidx = mapping[u[edgeok]], mapping[v[edgeok]], tsidx[edgeok]
    ee = float(mins[:, 0].min())
    ss = float(min(mins[:, 1].min(), ts[:, 1].min()))
    beta = 1.0 / float(temp)
    wc = np.exp(-beta * (mins[nodeids, 0] - ee) - (mins[nodeids, 1] - ss) / 2) / mins[nodeids, 2]
    cc = np.exp(-beta * (ts[tsidx, 0] - ee) - (ts[tsidx, 1] - ss) / 2) / ts[tsidx, 2]
    if np.any(cc <= 0) or np.any(wc <= 0):
        raise ArithmeticError("Float coefficients underflowed; precision route required")
    g = Graph(len(nodeids), u, v, cc, wc, int(mapping[source_id - 1]), int(mapping[target_id - 1]))
    receipt = dict(dataset="Cambridge_LJ38_public_full_network",
                   source_rows=len(mins), source_transition_states=len(ts),
                   nonself_transition_states=int(valid.sum()),
                   components=nc, component_states=g.n, component_edges=len(cc),
                   largest_component_fraction=float(selected.mean()),
                   source_original_1_based=source_id, target_original_1_based=target_id,
                   temperature=temp, inverse_temperature=beta,
                   prefactor_scope="c_uses_HTST_conductance_without_common_1_over_2pi;reported_raw_times_multiply_by_2pi_for_HTST_time",
                   minima_sha256=file_sha(path / "min.data"),
                   transition_states_sha256=file_sha(path / "ts.data"),
                   c_log10_range=[float(np.log10(cc).min()), float(np.log10(cc).max())],
                   w_log10_range=[float(np.log10(wc).min()), float(np.log10(wc).max())])
    receipt["float_load_seconds"] = time.perf_counter() - start
    if intervals:
        istart = time.perf_counter()
        iv = Intervals(prec)
        minrows = [line.split() for line in (path / "min.data").read_text().splitlines() if line.strip()]
        tsrows = [line.split() for line in (path / "ts.data").read_text().splitlines() if line.strip()]
        # The shifts are exact supplied decimal fields, common to w and c.
        e0 = min(D(row[0]) for row in minrows)
        s0 = min(min(D(row[1]) for row in minrows), min(D(row[1]) for row in tsrows))
        betaiv = iv.divpos((D(1), D(1)), (D(temp), D(temp)))
        def coeff(row):
            er, sr, order = D(row[0]), D(row[1]), D(row[2])
            ed = iv.sub((er, er), (e0, e0))
            sd = iv.sub((sr, sr), (s0, s0))
            ex = iv.sub((D(0), D(0)), iv.add(iv.mul(betaiv, ed), iv.divpos(sd, (D(2), D(2)))))
            return iv.divpos(iv.exp(ex), (order, order))
        g.w_bounds = [coeff(minrows[i]) for i in nodeids]
        g.c_bounds = [coeff(tsrows[e]) for e in tsidx]
        # Use midpoint-rounded source-decimal coefficients for trials too.
        g.w = np.asarray([float((a + b) / 2) for a, b in g.w_bounds])
        g.c = np.asarray([float((a + b) / 2) for a, b in g.c_bounds])
        receipt["interval_model_seconds"] = time.perf_counter() - istart
        receipt["coefficient_scope"] = "exact_source_decimal_energies_Hessians_symmetry_orders_and_decimal_temperature;outward_exponentials"
        receipt["coefficient_precision"] = prec
    receipt["all_loading_seconds"] = time.perf_counter() - start
    return g, receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["checks", "synthetic", "lj38"])
    ap.add_argument("--output", required=True)
    ap.add_argument("--path")
    ap.add_argument("--temperature", default="0.2")
    ap.add_argument("--source-id", type=int, default=1)
    ap.add_argument("--target-id", type=int, default=2)
    ap.add_argument("--ks", default="2,20,100")
    ap.add_argument("--interval-model", action="store_true")
    ap.add_argument("--no-certify", action="store_true")
    ap.add_argument("--precision", type=int, default=80)
    ap.add_argument("--full-baseline", action="store_true")
    ap.add_argument("--adaptive", action="store_true")
    ap.add_argument("--max-k", type=int, default=10000)
    args = ap.parse_args()
    started = time.perf_counter()
    if args.mode == "checks":
        result = rational_checks()
    else:
        if args.mode == "synthetic":
            g, receipt = synthetic(), dict(model="manufactured_cluster_chain_with_weak_heavy_appendages", scientific_scope="synthetic_diagnostic_only")
        else:
            g, receipt = load_lj38(args.path, args.temperature, args.interval_model, args.precision, args.source_id, args.target_id)
        result = dict(input=receipt, states=g.n, edges=len(g.c),
                      reductions=[] if args.adaptive else run_reductions(g, [int(k) for k in args.ks.split(",")], not args.no_certify, args.precision))
        if args.adaptive:
            result["adaptive"] = adaptive_reduction(g, max_k=args.max_k, prec=args.precision, certify=not args.no_certify)
            if args.mode == "lj38" and result["adaptive"]["certificate"]:
                result["adaptive"]["htst_time_interval"] = htst_time_interval(result["adaptive"]["certificate"], args.precision)
        if args.full_baseline:
            start = time.perf_counter()
            try:
                x, y, info = trial_solve(g)
                result["full_equilibrated_sparse_baseline"] = dict(**info, total_seconds=time.perf_counter() - start,
                    status="approximate_float64_direct_solve_not_automatically_certified")
                if not args.no_certify:
                    _, tree, _ = select_partition(g, g.n)
                    result["full_equilibrated_sparse_baseline"]["certificate"] = interval_certificate(g, x, y, tree, args.precision)
                    result["full_equilibrated_sparse_baseline"]["total_seconds_with_certificate"] = time.perf_counter() - start
            except Exception as exc:
                result["full_equilibrated_sparse_baseline"] = dict(error=repr(exc), total_seconds=time.perf_counter() - start)
    result["wall_seconds"] = time.perf_counter() - started
    result["versions"] = dict(numpy=np.__version__, decimal=decimal.__libmpdec_version__)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "random_checks"}, indent=2))


if __name__ == "__main__":
    main()
