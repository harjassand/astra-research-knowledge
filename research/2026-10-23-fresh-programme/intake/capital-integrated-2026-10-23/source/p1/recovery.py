"""Simplex probing of a known sparse symmetric matrix.

Research implementation, 23 October 2026.  No hidden matrix entries are used
by decode().  See PROOF.tex for the exact-real theorem and numerical limits.
"""
from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu


def simplex(q: int) -> np.ndarray:
    """q+1 unit vertices of a regular simplex, represented in R^q."""
    if q < 1:
        raise ValueError("q must be positive")
    u = np.zeros((q + 1, q))
    for k in range(q):
        d = np.sqrt((k + 1) * (k + 2))
        u[:k + 1, k] = 1.0 / d
        u[k + 1, k] = -(k + 1) / d
    return u * np.sqrt((q + 1) / q)


def adjacency(n: int, edges) -> sparse.csr_matrix:
    e = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    if e.size and (np.any(e < 0) or np.any(e >= n) or np.any(e[:, 0] == e[:, 1])):
        raise ValueError("invalid edge")
    e = np.sort(e, axis=1)
    if len(np.unique(e, axis=0)) != len(e):
        raise ValueError("duplicate edge")
    row = np.r_[e[:, 0], e[:, 1]]
    col = np.r_[e[:, 1], e[:, 0]]
    return sparse.csr_matrix((np.ones(len(row)), (row, col)), shape=(n, n))


class SimplexRecovery:
    def __init__(self, n: int, edges, colors, q: int):
        self.n = n
        self.q = q
        self.edges = np.asarray(sorted(tuple(sorted(e)) for e in edges), dtype=np.int64).reshape(-1, 2)
        self.colors = np.asarray(colors, dtype=np.int64)
        if self.colors.shape != (n,) or np.any(self.colors < 0) or np.any(self.colors > q):
            raise ValueError("colors must be in 0,...,q")
        self.A = adjacency(n, self.edges)
        self.degree = np.asarray(self.A.sum(axis=1)).ravel()
        if np.any(self.degree > q):
            raise ValueError("degree exceeds q")
        for i in range(n):
            closed = np.r_[i, self.A.indices[self.A.indptr[i]:self.A.indptr[i + 1]]]
            if len(np.unique(self.colors[closed])) != len(closed):
                raise ValueError("closed-neighborhood color collision")
        self.X = simplex(q)[self.colors]
        self.B = (sparse.diags(2 * q - self.degree) - self.A).tocsc()
        count, labels = sparse.csgraph.connected_components(self.A, directed=False)
        for c in range(count):
            if not np.any(self.degree[labels == c] < q):
                raise ValueError("a q-regular component makes this design noninjective")
        self.factor = splu(self.B)

    def matrix(self, coords) -> sparse.csr_matrix:
        """Orthonormal Frobenius coordinates: diagonal, then sqrt(2)*edges."""
        z = np.asarray(coords)
        if z.shape != (self.n + len(self.edges),):
            raise ValueError("coordinate shape")
        i, j = self.edges.T if len(self.edges) else (np.array([], dtype=int), np.array([], dtype=int))
        val = z[self.n:] / np.sqrt(2.0)
        return sparse.csr_matrix((np.r_[z[:self.n], val, val],
                                  (np.r_[np.arange(self.n), i, j],
                                   np.r_[np.arange(self.n), j, i])), shape=(self.n, self.n))

    def coordinates(self, h) -> np.ndarray:
        h = sparse.csr_matrix(h)
        off = np.asarray(h[self.edges[:, 0], self.edges[:, 1]]).ravel() if len(self.edges) else np.array([])
        return np.r_[h.diagonal(), np.sqrt(2.0) * off]

    def row_sum_matrix(self) -> sparse.csr_matrix:
        n, m = self.n, len(self.edges)
        i, j = self.edges.T if m else (np.array([], dtype=int), np.array([], dtype=int))
        return sparse.csr_matrix((np.r_[np.ones(n), np.full(2 * m, 1 / np.sqrt(2.0))],
                                  (np.r_[np.arange(n), i, j],
                                   np.r_[np.arange(n), n + np.arange(m), n + np.arange(m)])),
                                 shape=(n, n + m))

    def measurement_matrix(self) -> sparse.csr_matrix:
        """Explicit only for diagnostics; the production decoder avoids it."""
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for k in range(self.q):
                rows.append(i * self.q + k); cols.append(i); vals.append(self.X[i, k])
        for t, (i, j) in enumerate(self.edges):
            for k in range(self.q):
                rows.extend([i * self.q + k, j * self.q + k])
                cols.extend([self.n + t, self.n + t])
                vals.extend([self.X[j, k] / np.sqrt(2), self.X[i, k] / np.sqrt(2)])
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n * self.q, self.n + len(self.edges)))

    def adjoint_coordinates(self, y) -> np.ndarray:
        y = np.asarray(y)
        if y.shape != (self.n, self.q):
            raise ValueError("observation shape")
        diag = np.einsum('ij,ij->i', self.X, y)
        i, j = self.edges.T if len(self.edges) else (np.array([], dtype=int), np.array([], dtype=int))
        off = (np.einsum('ij,ij->i', self.X[j], y[i]) +
               np.einsum('ij,ij->i', self.X[i], y[j])) / np.sqrt(2.0)
        return np.r_[diag, off]

    def decode(self, y) -> sparse.csr_matrix:
        """Canonical least squares, using one n-dimensional SPD solve."""
        z = self.adjoint_coordinates(y)
        s = self.row_sum_matrix()
        a = self.factor.solve(s @ z)
        result = self.q / (self.q + 1) * (z + 2 * (s.T @ a))
        return self.matrix(result)


def complete_graph_lift(q: int, sheets: int, rng):
    """An ordinary random lift of K_(q+1); no expansion is assumed."""
    edges = []
    for c in range(q + 1):
        for d in range(c + 1, q + 1):
            perm = rng.permutation(sheets)
            edges.extend((c * sheets + i, d * sheets + int(perm[i])) for i in range(sheets))
    return (q + 1) * sheets, edges, np.repeat(np.arange(q + 1), sheets)


def torus(dimension: int, side: int):
    """Locally injective (2d+1)-coloring, requiring side divisible by 2d+1."""
    d, l = dimension, side
    q = 2 * d
    if l < 3 or l % (q + 1):
        raise ValueError("side must be >=3 and divisible by 2d+1")
    shape = (l,) * d
    coords = np.indices(shape).reshape(d, -1).T
    colors = (coords @ np.arange(1, d + 1)) % (q + 1)
    edges = []
    for i, x in enumerate(coords):
        for k in range(d):
            y = x.copy(); y[k] = (y[k] + 1) % l
            j = int(np.ravel_multi_index(tuple(y), shape))
            edges.append((i, j))
    return l ** d, sorted(set(tuple(sorted(e)) for e in edges)), colors
