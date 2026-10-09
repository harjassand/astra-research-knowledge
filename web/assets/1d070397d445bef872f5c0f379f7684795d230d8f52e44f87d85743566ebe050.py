"""Exact mutable Hopf--Lax likelihood engine for 1-D inviscid Burgers/LWR.

Model: u_t + (u^2/2)_x = 0 on R; u0 is constant on fixed finite cells,
with known constant exterior states. A local cell-state edit changes one
restricted Hopf--Lax candidate and applies a constant offset to all candidates
to its right. Per sensor endpoint, range-add/range-min is maintained by a
lazy segment tree. Cell-average observations are exact differences of the
Hopf--Lax potential.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import inf
from typing import Iterable
import numpy as np


class RangeMinAdd:
    """Lazy segment tree supporting half-open range addition, point set, min query."""
    def __init__(self, values):
        values = np.asarray(values, dtype=float)
        self.n = len(values)
        size = 1
        while size < self.n:
            size *= 2
        self.size = size
        self.mn = np.full(2 * size, np.inf)
        self.arg = np.full(2 * size, -1, dtype=np.int64)
        self.lazy = np.zeros(2 * size)
        self._journal = None
        self.mn[size:size+self.n] = values
        self.arg[size:size+self.n] = np.arange(self.n)
        for p in range(size - 1, 0, -1):
            self._pull(p)

    def _pull(self, p):
        self._touch(p)
        a, b = 2*p, 2*p+1
        if self.mn[a] <= self.mn[b]:
            self.mn[p], self.arg[p] = self.mn[a], self.arg[a]
        else:
            self.mn[p], self.arg[p] = self.mn[b], self.arg[b]

    def _apply(self, p, delta):
        self._touch(p)
        self.mn[p] += delta
        self.lazy[p] += delta

    def _push(self, p):
        z = self.lazy[p]
        if z:
            self._apply(2*p, z)
            self._apply(2*p+1, z)
            self._touch(p)
            self.lazy[p] = 0.0

    def _touch(self, p):
        if self._journal is not None and p not in self._journal:
            self._journal[p] = (self.mn[p], self.arg[p], self.lazy[p])

    def begin(self):
        if self._journal is not None:
            raise RuntimeError('nested tree transaction')
        self._journal = {}

    def commit(self):
        if self._journal is None:
            raise RuntimeError('no tree transaction')
        self._journal = None

    def rollback(self):
        if self._journal is None:
            raise RuntimeError('no tree transaction')
        for p, (mn, arg, lazy) in self._journal.items():
            self.mn[p], self.arg[p], self.lazy[p] = mn, arg, lazy
        self._journal = None

    def range_add(self, left, right, delta):
        if left >= right or delta == 0.0:
            return
        self._range_add(1, 0, self.size, left, right, delta)

    def _range_add(self, p, lo, hi, ql, qr, delta):
        if ql <= lo and hi <= qr:
            self._apply(p, delta)
            return
        self._push(p)
        mid = (lo + hi)//2
        if ql < mid:
            self._range_add(2*p, lo, mid, ql, qr, delta)
        if qr > mid:
            self._range_add(2*p+1, mid, hi, ql, qr, delta)
        self._pull(p)

    def point_set(self, index, value):
        self._point_set(1, 0, self.size, index, float(value))

    def _point_set(self, p, lo, hi, index, value):
        if hi-lo == 1:
            self._touch(p)
            self.mn[p] = value
            self.arg[p] = index
            self.lazy[p] = 0.0
            return
        self._push(p)
        mid = (lo+hi)//2
        if index < mid:
            self._point_set(2*p, lo, mid, index, value)
        else:
            self._point_set(2*p+1, mid, hi, index, value)
        self._pull(p)

    @property
    def minimum(self):
        return float(self.mn[1])

    @property
    def argmin(self):
        return int(self.arg[1])


@dataclass(frozen=True)
class Query:
    x: float
    t: float


@dataclass(frozen=True)
class ConvexFlux:
    """Differentiable strictly convex scalar flux and its Legendre dual."""
    f: object
    fp: object
    fstar: object


BURGERS = ConvexFlux(lambda u: 0.5*u*u, lambda u: u,
                     lambda z: 0.5*z*z)


class FenwickAreas:
    """Point updates and prefix sums for the primitive U0 at cell boundaries."""
    def __init__(self, areas):
        areas = np.asarray(areas, dtype=float)
        self.n = len(areas)
        self.tree = np.zeros(self.n+1)
        self.tree[1:] = areas
        for i in range(1, self.n+1):
            p = i + (i & -i)
            if p <= self.n:
                self.tree[p] += self.tree[i]
        self._journal = None

    def prefix(self, end):
        """Sum of entries with indices in [0,end)."""
        s, i = 0.0, end
        while i:
            s += self.tree[i]
            i -= i & -i
        return s

    def begin(self):
        if self._journal is not None:
            raise RuntimeError('nested Fenwick transaction')
        self._journal = {}

    def add(self, index, delta):
        i = index+1
        while i <= self.n:
            if self._journal is not None and i not in self._journal:
                self._journal[i] = self.tree[i]
            self.tree[i] += delta
            i += i & -i

    def commit(self):
        if self._journal is None:
            raise RuntimeError('no Fenwick transaction')
        self._journal = None

    def rollback(self):
        if self._journal is None:
            raise RuntimeError('no Fenwick transaction')
        for i, value in self._journal.items():
            self.tree[i] = value
        self._journal = None


class EditTransaction:
    """An exact state edit that can be committed or rolled back without drift."""
    def __init__(self, owner, j, old_state, no_op=False):
        self.owner, self.j, self.old_state = owner, j, old_state
        self.done = False
        self.no_op = no_op

    def commit(self):
        if self.done:
            raise RuntimeError('transaction already closed')
        if self.no_op:
            self.done = True
            return
        for tree in self.owner.trees:
            tree.commit()
        self.owner.areas.commit()
        self.done = True

    def rollback(self):
        if self.done:
            raise RuntimeError('transaction already closed')
        if self.no_op:
            self.done = True
            return
        for tree in self.owner.trees:
            tree.rollback()
        self.owner.areas.rollback()
        self.owner.states[self.j] = self.old_state
        self.done = True


def _candidate(query: Query, left: float, right: float, u: float,
               primitive_left: float | None, primitive_right: float | None,
               flux=BURGERS):
    """Restricted inf of U0(y)+t f*((x-y)/t) on one constant-state interval.

    primitive_left/right are values of U0 at finite endpoints; on an unbounded
    side only the finite anchor value is needed. Returns (cost, minimizer y).
    """
    x, t = query.x, query.t
    y0 = x - t*flux.fp(u)
    def end_cost(y, primitive):
        return primitive + t*flux.fstar((x-y)/t)
    def inner_cost(anchor, primitive):
        return primitive + u*(x-anchor) - t*flux.f(u)
    if left == -inf:
        # U0(y) = U0(right) + u*(y-right), y <= right.
        if y0 <= right:
            return inner_cost(right, primitive_right), y0
        return end_cost(right, primitive_right), right
    if right == inf:
        # U0(y) = U0(left) + u*(y-left), y >= left.
        if y0 >= left:
            return inner_cost(left, primitive_left), y0
        return end_cost(left, primitive_left), left
    if y0 < left:
        return end_cost(left, primitive_left), left
    if y0 > right:
        return end_cost(right, primitive_right), right
    return inner_cost(left, primitive_left), y0


class MutableHopfLax:
    """Exact O(log N) updates per observation endpoint for local cell edits.

    breaks: N+1 strictly increasing cell boundaries.
    states: N cellwise Burgers states.
    left_state/right_state: known exterior constants on (-inf, breaks[0]) and
      (breaks[-1], inf).
    queries: observation endpoints (x,t), t>0.
    """
    def __init__(self, breaks, states, queries: Iterable[Query],
                 left_state=0.0, right_state=0.0, flux=BURGERS):
        self.breaks = np.asarray(breaks, dtype=float)
        self.states = np.asarray(states, dtype=float).copy()
        if len(self.breaks) != len(self.states)+1:
            raise ValueError('breaks must have one more element than states')
        if np.any(np.diff(self.breaks) <= 0):
            raise ValueError('breaks must be strictly increasing')
        self.queries = tuple(queries)
        if any(q.t <= 0 for q in self.queries):
            raise ValueError('query times must be positive')
        self.left_state, self.right_state = float(left_state), float(right_state)
        self.flux = flux
        self.widths = np.diff(self.breaks)
        self.areas = FenwickAreas(self.states*self.widths)
        initial_primitive = np.r_[0.0, np.cumsum(self.states*self.widths)]
        self.trees = [RangeMinAdd(self._all_candidates(q,initial_primitive))
                      for q in self.queries]

    def _all_candidates(self, q, primitive):
        n = len(self.states)
        vals = np.empty(n+2)
        vals[0] = _candidate(q, -inf, self.breaks[0], self.left_state,
                             None, 0.0, self.flux)[0]
        for j in range(n):
            vals[j+1] = _candidate(q, self.breaks[j], self.breaks[j+1],
                                   self.states[j], primitive[j],
                                   primitive[j+1], self.flux)[0]
        vals[n+1] = _candidate(q, self.breaks[-1], inf, self.right_state,
                               primitive[n], None, self.flux)[0]
        return vals

    def potential(self, query_index):
        return self.trees[query_index].minimum

    def minimizer(self, query_index):
        """Return one minimizer y, from the argmin candidate interval."""
        q = self.queries[query_index]
        j = self.trees[query_index].argmin
        n = len(self.states)
        if j == 0:
            return _candidate(q, -inf, self.breaks[0], self.left_state,
                              None, 0.0, self.flux)[1]
        if j == n+1:
            return _candidate(q, self.breaks[-1], inf, self.right_state,
                              self.areas.prefix(n), None, self.flux)[1]
        k = j-1
        return _candidate(q, self.breaks[k], self.breaks[k+1], self.states[k],
                          self.areas.prefix(k), self.areas.prefix(k+1), self.flux)[1]

    def interval_average(self, left_query_index, right_query_index, width):
        return (self.potential(right_query_index)-self.potential(left_query_index))/width

    def update_cell(self, j, new_state):
        """Begin an exact local edit; commit or rollback the returned transaction.

        Work is O(Q log N), where Q is the number of observation endpoints.
        Rejected proposals restore every touched tree/Fenwick value from a
        journal, so rollback has no accumulated floating-point drift.
        """
        n = len(self.states)
        if not 0 <= j < n:
            raise IndexError(j)
        new_state = float(new_state)
        old = float(self.states[j])
        delta_area = (new_state-old)*self.widths[j]
        if new_state == old:
            return EditTransaction(self, j, old, no_op=True)
        for tree in self.trees:
            tree.begin()
        self.areas.begin()
        tx = EditTransaction(self, j, old)
        # All cells strictly to the right and the right exterior have their
        # primitive anchor raised by the same area increment.
        primitive_left = self.areas.prefix(j)
        primitive_right = primitive_left + new_state*self.widths[j]
        for q, tree in zip(self.queries, self.trees):
            tree.range_add(j+2, n+2, delta_area)
            v = _candidate(q, self.breaks[j], self.breaks[j+1], new_state,
                           primitive_left, primitive_right, self.flux)[0]
            tree.point_set(j+1, v)
        self.states[j] = new_state
        self.areas.add(j, delta_area)
        return tx

    def state_copy(self):
        return self.states.copy()


def direct_potential(breaks, states, q: Query, left_state=0.0, right_state=0.0,
                     flux=BURGERS):
    """O(N) reference evaluation by scanning every restricted interval."""
    breaks = np.asarray(breaks, dtype=float)
    states = np.asarray(states, dtype=float)
    widths = np.diff(breaks)
    primitive = np.r_[0.0, np.cumsum(states*widths)]
    vals = [_candidate(q, -inf, breaks[0], left_state, None, primitive[0], flux)[0]]
    vals.extend(_candidate(q, breaks[j], breaks[j+1], states[j],
                           primitive[j], primitive[j+1], flux)[0]
                for j in range(len(states)))
    vals.append(_candidate(q, breaks[-1], inf, right_state, primitive[-1], None, flux)[0])
    return min(vals)


def finite_volume_godunov(breaks, states, t_end, x_eval, left_state=0.0,
                          right_state=0.0, cfl=0.45, refinement=1):
    """Simple first-order Godunov reference on a fine uniform finite domain.

    Returns cell averages at t_end and the cell centers. This is a baseline,
    not part of the exact inference engine.
    """
    x0, x1 = breaks[0], breaks[-1]
    dx0 = np.min(np.diff(breaks))
    n = max(256*refinement,
            int(np.ceil((x1-x0)/dx0))*refinement)
    dx = (x1-x0)/n
    centers = x0 + (np.arange(n)+0.5)*dx
    # Piecewise-constant projection of exact initial profile onto FV grid.
    idx = np.searchsorted(breaks[1:-1], centers, side='right')
    u = np.asarray(states)[idx].copy()
    umax = max(abs(left_state), abs(right_state), float(np.max(np.abs(u))))
    dt_nom = cfl*dx/max(umax, 1e-15)
    t = 0.0
    ul = np.empty(n+1)
    ur = np.empty(n+1)
    while t < t_end:
        dt = min(dt_nom, t_end-t)
        ext = np.r_[left_state, u, right_state]
        a, b = ext[:-1], ext[1:]
        # Exact Burgers Godunov flux.
        f = np.empty(n+1)
        shock = a > b
        f[shock] = np.where((a[shock]+b[shock])/2 >= 0,
                            0.5*a[shock]**2, 0.5*b[shock]**2)
        rare = ~shock
        ar, br = a[rare], b[rare]
        fr = np.empty_like(ar)
        fr[(ar >= 0)] = 0.5*ar[(ar >= 0)]**2
        fr[(br <= 0)] = 0.5*br[(br <= 0)]**2
        cross = (ar < 0) & (br > 0)
        fr[cross] = 0.0
        f[rare] = fr
        u -= (dt/dx)*(f[1:]-f[:-1])
        t += dt
    return centers, u


def interval_average_from_grid(centers, u, a, b):
    # Approximate integral using piecewise constant grid overlap.
    dx = centers[1]-centers[0]
    edges = np.r_[centers[0]-dx/2, centers+dx/2]
    lo, hi = max(a, edges[0]), min(b, edges[-1])
    if hi <= lo:
        raise ValueError('sensor interval outside FV domain')
    i0 = max(0, np.searchsorted(edges, lo, side='right')-1)
    i1 = min(len(u)-1, np.searchsorted(edges, hi, side='left'))
    total = 0.0
    for i in range(i0, i1+1):
        overlap = max(0.0, min(hi, edges[i+1])-max(lo, edges[i]))
        total += overlap*u[i]
    return total/(hi-lo)
