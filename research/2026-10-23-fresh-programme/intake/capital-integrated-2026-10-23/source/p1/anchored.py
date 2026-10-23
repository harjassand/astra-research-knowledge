"""Full regular supports: one changed probe row and a local cycle witness.

The inverse uses the missing-edge Green decoder internally; the true unknown
has the full support, including the anchor edge.  No unknown entry is given
to the decoder.  The anchor is measured by the displayed cycle functional.
"""
from __future__ import annotations

import numpy as np
from scipy import sparse
from recovery import SimplexRecovery, adjacency, simplex


def triangle_cover(sheets, rng):
    """Random K_(3,3) lift, then replace each right vertex by its port triangle.

    Its three edge colors are inherited from the Latin-square coloring of
    K_(3,3).  No expansion assumption or rejection sampling is built in.
    """
    r = 3 * sheets
    base_edges = []
    full_edges = []
    for i in range(3):
        for j in range(3):
            perm = rng.permutation(sheets)
            color = (j - i) % 3 + 1
            for k in range(sheets):
                left = i * sheets + k
                right = j * sheets + int(perm[k])
                base_edges.append((left, r + right))
                full_edges.append((left, r + 3 * right + color - 1))
    for right in range(r):
        tri = [r + 3 * right + j for j in range(3)]
        full_edges.extend((tri[i], tri[j]) for i in range(3) for j in range(i + 1, 3))
    colors = np.r_[np.zeros(r, dtype=int), np.tile(np.arange(1, 4), r)]
    v = 0
    u = next(j for i, j in full_edges if i == v)
    right = (u - r) // 3
    tri = [r + 3 * right + j for j in range(3)]
    cycle = [u] + [j for j in tri if j != u]
    return 4 * r, full_edges, colors, v, cycle, (2 * r, base_edges)


class AnchoredRecovery:
    """A constructive left inverse with a q+1 dimensional correction solve.

    K is any valid bound on the F-to-operator norm of the internal missing-edge
    decoder.  If it is supplied, t*K < 1 is checked.  Omitting K is permitted
    for diagnostics, but does not certify the perturbation's invertibility.
    """

    def __init__(self, n, full_edges, colors, q, vertex, cycle, t, K=None):
        self.n, self.q, self.v = n, q, int(vertex)
        self.cycle = [int(i) for i in cycle]
        self.t = float(t)
        self.rho = np.sqrt(1 + self.t**2)
        if self.t <= 0 or (K is not None and self.t * K >= 1):
            raise ValueError("require t>0 and t*K<1")
        if len(self.cycle) < 3 or len(set(self.cycle)) != len(self.cycle):
            raise ValueError("cycle must be simple and have length at least three")
        self.u = self.cycle[0]
        self.full_edges = sorted(tuple(sorted(e)) for e in full_edges)
        self.A = adjacency(n, self.full_edges)
        if np.any(np.asarray(self.A.sum(axis=1)).ravel() != q):
            raise ValueError("full graph must be q-regular")
        if sparse.csgraph.connected_components(self.A, directed=False)[0] != 1:
            raise ValueError("full graph must be connected")
        neighbors = set(self.A.indices[self.A.indptr[self.v]:self.A.indptr[self.v+1]])
        if (neighbors | {self.v}).intersection(self.cycle) != {self.u}:
            raise ValueError("cycle must meet the closed neighborhood only at its anchor")
        eset = set(self.full_edges)
        for i, a in enumerate(self.cycle):
            b = self.cycle[(i+1) % len(self.cycle)]
            if tuple(sorted((a, b))) not in eset:
                raise ValueError("cycle edge absent")
        anchor = tuple(sorted((self.u, self.v)))
        missing_edges = [e for e in self.full_edges if e != anchor]
        self.base = SimplexRecovery(n, missing_edges, colors, q)
        # The full graph must also satisfy the local color hypothesis.
        for i in range(n):
            closed = np.r_[i, self.A.indices[self.A.indptr[i]:self.A.indptr[i+1]]]
            if len(np.unique(np.asarray(colors)[closed])) != q + 1:
                raise ValueError("full closed-neighborhood color collision")
        self.X0 = self.base.X.copy()
        norm_diff = np.sqrt(2 * (q+1) / q)
        self.h = (self.X0[self.cycle[1]] - self.X0[self.cycle[-1]]) / norm_diff
        self.Z = np.zeros((n, q))
        ell = len(self.cycle)
        for i, a in enumerate(self.cycle):
            self.Z[a] = (self.X0[self.cycle[(i+1) % ell]] - self.X0[self.cycle[(i-1) % ell]]) / (norm_diff * np.sqrt(ell))
        self.X = self.X0.copy()
        self.X[self.v] += self.t * self.h
        self.X /= self.rho
        self.H0 = (sparse.eye(n, format='csr') + self.A).tocsr()
        self.local = np.array(sorted(neighbors | {self.v}), dtype=int)
        # C_j = D(U_j), where U_j has row h at the jth local vertex.
        correction_columns = []
        for j in self.local:
            y = np.zeros((n, q)); y[j] = self.h
            correction_columns.append(self.base.coordinates(self.base.decode(y)))
        self.C = np.column_stack(correction_columns)
        self.RC = np.column_stack([self.local_column(self.base.matrix(self.C[:, j])) for j in range(q+1)])
        self.small = np.eye(q+1) + self.t * self.RC
        if K is not None:
            self.operator_bound = self.rho * (K + (q+1) * np.sqrt(ell) / self.t) / (1-self.t*K)
        else:
            self.operator_bound = None

    def local_column(self, h):
        return np.asarray(h[self.local, self.v].toarray()).ravel()

    def decode(self, y):
        y = np.asarray(y)
        if y.shape != (self.n, self.q):
            raise ValueError("observation shape")
        yt = self.rho * y
        beta = np.sqrt(len(self.cycle)) / self.t * np.sum(self.Z * yt)
        w = self.base.decode(yt) + beta * self.H0
        local = np.linalg.solve(self.small, self.local_column(w))
        correction = self.base.matrix(self.C @ local)
        return (w - self.t * correction).tocsr()

    def full_measurement_matrix(self):
        # Reuse the coordinate implementation on the full edge set, which is
        # valid for every X.  No decoder on the regular base is called.
        model = object.__new__(SimplexRecovery)
        model.n, model.q = self.n, self.q
        model.edges = np.asarray(self.full_edges, dtype=int)
        model.X = self.X
        return model.measurement_matrix()

    def full_matrix(self, coordinates):
        model = object.__new__(SimplexRecovery)
        model.n = self.n
        model.edges = np.asarray(self.full_edges, dtype=int)
        return model.matrix(coordinates)


class StarAnchoredRecovery:
    """Nonperturbative cubic construction: measure the three star edges first.

    For a triangle-expanded cubic bipartite graph, choose a color-0 vertex v.
    Its neighbors lie in three disjoint port triangles.  A unit direction h
    perpendicular to X0[v] has normalized cycle pairings 1,-1/2,-1/2.
    Every t>0 is allowed.  Exactly one grounded-Laplacian solve is needed per
    decoded observation after the three scalar cycle measurements.
    """

    def __init__(self, n, full_edges, colors, vertex=0, t=1.0, K=None):
        self.n, self.q, self.v, self.t = n, 3, int(vertex), float(t)
        if self.t <= 0:
            raise ValueError("t must be positive")
        self.rho = np.sqrt(1+self.t**2)
        self.full_edges = sorted(tuple(sorted(e)) for e in full_edges)
        self.A = adjacency(n, self.full_edges)
        if np.any(np.asarray(self.A.sum(axis=1)).ravel() != 3):
            raise ValueError("full graph must be cubic")
        colors = np.asarray(colors, dtype=int)
        if colors[self.v] != 0:
            raise ValueError("choose a color-0 vertex")
        self.neighbors = sorted((int(i) for i in self.A.indices[self.A.indptr[self.v]:self.A.indptr[self.v+1]]), key=lambda i:colors[i])
        if list(colors[self.neighbors]) != [1,2,3]:
            raise ValueError("neighbors must have the three port colors")
        without_star = [e for e in self.full_edges if self.v not in e]
        self.base = SimplexRecovery(n, without_star, colors, 3)
        self.X0 = self.base.X.copy()
        for i in range(n):
            closed=np.r_[i,self.A.indices[self.A.indptr[i]:self.A.indptr[i+1]]]
            if len(np.unique(colors[closed])) != 4:
                raise ValueError("full closed-neighborhood color collision")
        self.cycles=[]
        occupied=set()
        for u in self.neighbors:
            candidates=[int(i) for i in self.A.indices[self.A.indptr[u]:self.A.indptr[u+1]] if colors[i] != 0]
            if len(candidates)!=2 or self.A[candidates[0],candidates[1]] != 1:
                raise ValueError("a port triangle is missing")
            cycle=[u]+sorted(candidates,key=lambda i:colors[i])
            if occupied.intersection(cycle) or (set(self.neighbors)|{self.v}).intersection(cycle)!={u}:
                raise ValueError("anchor triangles must be disjoint and locally separated")
            occupied.update(cycle);self.cycles.append(cycle)
        self.h=(self.X0[self.cycles[0][1]]-self.X0[self.cycles[0][-1]])/np.sqrt(8/3)
        self.Z=np.zeros((3,n,3))
        for j,cycle in enumerate(self.cycles):
            for k,i in enumerate(cycle):
                self.Z[j,i]=(self.X0[cycle[(k+1)%3]]-self.X0[cycle[(k-1)%3]])/np.sqrt(8)
        self.pairings=np.array([self.Z[j,u]@self.h for j,u in enumerate(self.neighbors)])
        if np.min(np.abs(self.pairings))<1e-12:
            raise ValueError("vanishing cycle pairing")
        self.Xt=self.X0.copy();self.Xt[self.v]+=self.t*self.h
        self.X=self.Xt/self.rho
        self.anchor_gain=1/(self.t*np.min(np.abs(self.pairings)))
        self.operator_bound=None
        if K is not None:
            self.operator_bound=self.rho*(K+(1+K*np.sqrt(self.rho**2+4/3))*self.anchor_gain)

    def star_matrix(self, beta):
        beta=np.asarray(beta)
        return sparse.csr_matrix((np.r_[beta,beta],
             (np.r_[np.full(3,self.v),self.neighbors],np.r_[self.neighbors,np.full(3,self.v)])),shape=(self.n,self.n))

    def decode(self,y):
        y=np.asarray(y)
        if y.shape!=(self.n,3):
            raise ValueError("observation shape")
        yt=self.rho*y
        beta=np.einsum('kij,ij->k',self.Z,yt)/(self.t*self.pairings)
        star=self.star_matrix(beta)
        reduced=yt-star@self.Xt
        reduced[self.v]=(reduced[self.v]@self.Xt[self.v])/(self.rho**2)*self.X0[self.v]
        return (self.base.decode(reduced)+star).tocsr()

    def full_matrix(self,coordinates):
        model=object.__new__(SimplexRecovery)
        model.n=self.n;model.edges=np.asarray(self.full_edges,dtype=int)
        return model.matrix(coordinates)

    def full_measurement_matrix(self):
        model=object.__new__(SimplexRecovery)
        model.n=self.n;model.q=3;model.edges=np.asarray(self.full_edges,dtype=int);model.X=self.X
        return model.measurement_matrix()
