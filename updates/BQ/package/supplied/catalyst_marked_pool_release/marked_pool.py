"""Certified endpoint likelihoods for a finite low-copy catalyst / large pool.

Model
-----
N exchangeable substrate molecules each occupy one of q free states.  While
free, molecules evolve independently with row generator Q.  One catalyst is
either free or bound to one substrate.  A Poisson candidate clock of rate
lambda runs continuously. At each candidate time when the catalyst is free,
one of the N free molecules is selected uniformly; if it is in state `bind`,
it binds. Bound complex releases at rates koff (to `bind`) and kcat (to
`product`). The physical binding intensity is therefore lambda*n_bind/N.

The candidate selection is also used as an auxiliary mark: every molecule
selected at an attempt is removed from an untouched pool, whether or not it
binds. Untouched molecules remain iid with law p(t)=p(0) exp(Qt). The code
tracks only the counts of marked molecules in each free state, a bound bit,
and the number of candidate attempts. Truncating attempts at K yields an
endpoint-likelihood lower bound; the missing mass is exactly a Poisson tail.

This module implements a finite-dimensional forward ODE and a small-N CME
reference. Floating-point ODE / matrix-exponential error is not included in
the analytic Poisson-tail certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import factorial, lgamma, log, exp
from typing import Iterable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm
from scipy.stats import poisson


def weak_compositions(total: int, q: int):
    """All q-tuples of nonnegative integers with sum <= total."""
    if q == 1:
        for x in range(total + 1):
            yield (x,)
        return
    # Recursive over first coordinate; only small K is intended.
    for x in range(total + 1):
        for rest in weak_compositions(total - x, q - 1):
            yield (x,) + rest


def multinomial_pmf(counts: tuple[int, ...], p: np.ndarray) -> float:
    if len(counts) != len(p) or any(x < 0 for x in counts) or sum(counts) < 0:
        return 0.0
    if sum(counts) == 0:
        return 1.0
    # Robustly handle zero probabilities without a 0*log(0) issue.
    if any(x > 0 and p_i <= 0 for x, p_i in zip(counts, p)):
        return 0.0
    n = sum(counts)
    ans = lgamma(n + 1) - sum(lgamma(x + 1) for x in counts)
    for x, p_i in zip(counts, p):
        if x:
            ans += x * log(float(p_i))
    return exp(ans)


def candidate_event_edges(state, N: int, catalysts: int, bind: int):
    """Auxiliary uniformized-candidate edges; coefficient -1 means constant 1.

    Each returned triple is (destination (j,b,n), coefficient state, weight).
    Unmarked-pool edges are later multiplied by p_t[coefficient].
    """
    j, b, n = state
    edges = []
    if b > 0:
        edges.append(((j + 1, b, n), -1, b / catalysts))
    free_fraction = (catalysts - b) / catalysts
    if free_fraction <= 0:
        return edges
    if b > 0:
        edges.append(((j + 1, b, n), -1, free_fraction * b / N))
    for a, na in enumerate(n):
        if not na:
            continue
        if a == bind:
            nn = list(n); nn[a] -= 1
            dest = (j + 1, b + 1, tuple(nn))
        else:
            dest = (j + 1, b, n)
        edges.append((dest, -1, free_fraction * na / N))
    untouched = N - sum(n) - b
    if untouched < 0:
        raise ValueError("tagged and bound particles exceed pool size")
    for a in range(len(n)):
        if a == bind:
            dest = (j + 1, b + 1, n)
        else:
            nn = list(n); nn[a] += 1
            dest = (j + 1, b, tuple(nn))
        if untouched:
            edges.append((dest, a, free_fraction * untouched / N))
    return edges


def build_between_event_generator(states, index, Q, bind, product, koff, kcat):
    """Row generator for free marked molecules and bound catalysts."""
    q = len(Q)
    rr, cc, vv = [], [], []
    for src, (j, b, n) in enumerate(states):
        exit_rate = 0.0
        for a in range(q):
            if n[a] == 0:
                continue
            for c in range(q):
                rate = n[a] * Q[a, c] if c != a else 0.0
                if rate > 0:
                    nn = list(n); nn[a] -= 1; nn[c] += 1
                    dst = index.get((j, b, tuple(nn)))
                    if dst is not None:
                        rr.append(src); cc.append(dst); vv.append(rate)
                    exit_rate += rate
        if b > 0:
            if koff > 0:
                nn = list(n); nn[bind] += 1
                dst = index.get((j, b - 1, tuple(nn)))
                if dst is not None:
                    rr.append(src); cc.append(dst); vv.append(b * koff)
                exit_rate += b * koff
            if kcat > 0:
                nn = list(n); nn[product] += 1
                dst = index.get((j, b - 1, tuple(nn)))
                if dst is not None:
                    rr.append(src); cc.append(dst); vv.append(b * kcat)
                exit_rate += b * kcat
        rr.append(src); cc.append(src); vv.append(-exit_rate)
    return coo_matrix((vv, (rr, cc)), shape=(len(states), len(states))).tocsr()


@dataclass
class MarkedResult:
    lower: float
    poisson_tail: float
    mass: float
    dimension: int
    rtol: float
    atol: float
    lower_by_event_count: np.ndarray

    def relative_cutoff(self, relative_tolerance: float, mean_candidates: float):
        """Smallest included event count with Poisson tail <= eps * lower.

        This is a *mathematical truncation* criterion. Floating-point ODE
        error still needs a separate numerical budget.
        """
        if not (0 < relative_tolerance < 1):
            raise ValueError("relative_tolerance must lie in (0,1)")
        cumulative = np.cumsum(self.lower_by_event_count)
        for k, lower_k in enumerate(cumulative):
            tail_k = float(poisson.sf(k, mean_candidates))
            if lower_k > 0 and tail_k <= relative_tolerance * lower_k:
                return {"K": k, "lower": float(lower_k), "tail": tail_k,
                        "relative_tail_bound": tail_k / float(lower_k)}
        raise ValueError("computed Kmax insufficient for requested relative tolerance")


class MarkedPoolLikelihood:
    def __init__(self, N: int, Q: np.ndarray, bind: int, product: int,
                 lam: float, koff: float, kcat: float, mu0: np.ndarray,
                 catalysts: int = 1):
        self.N = int(N)
        self.Q = np.asarray(Q, dtype=float)
        self.q = self.Q.shape[0]
        self.bind = int(bind)
        self.product = int(product)
        self.lam = float(lam)
        self.koff = float(koff)
        self.kcat = float(kcat)
        self.mu0 = np.asarray(mu0, dtype=float)
        self.catalysts = int(catalysts)
        assert self.Q.shape == (self.q, self.q)
        assert np.allclose(self.Q.sum(axis=1), 0.0)
        assert np.all(self.Q - np.diag(np.diag(self.Q)) >= -1e-14)
        assert len(self.mu0) == self.q and np.all(self.mu0 >= 0)
        assert abs(float(self.mu0.sum()) - 1) < 1e-12
        assert 0 <= self.bind < self.q and 0 <= self.product < self.q
        assert self.N >= 1 and self.lam >= 0 and self.koff >= 0 and self.kcat >= 0
        assert self.catalysts >= 1

    def _make_states(self, K: int):
        states = []
        for j in range(K + 1):
            for b in range(min(self.catalysts, j, self.N) + 1):
                for n in weak_compositions(min(j, self.N) - b, self.q):
                    states.append((j, b, n))
        index = {s: i for i, s in enumerate(states)}
        return states, index

    def solve(self, T: float, K: int, observed: tuple[int, ...],
              observed_bound: int | None = None, rtol: float = 2e-10,
              atol: float = 1e-13, max_step: float = np.inf) -> MarkedResult:
        """Return [lower, lower+Poisson(K-tail)] for one terminal count vector.

        `observed` is the q-vector of *free* substrate counts. If
        `observed_bound`, when supplied, adds that occupancy to the joint
        terminal event; the returned value is P(Y=y, B=observed_bound), not
        P(Y=y | B=observed_bound). Otherwise marginalize catalyst occupancy.
        """
        N, q, K = self.N, self.q, int(K)
        if len(observed) != q or any(int(y) < 0 for y in observed):
            raise ValueError("observed must be a nonnegative q-vector")
        obs = tuple(map(int, observed))
        states, ix = self._make_states(K)
        D = len(states)
        # R is the row generator for tracked free tags and bound catalysts.
        R = build_between_event_generator(states, ix, self.Q, self.bind,
                                          self.product, self.koff, self.kcat)

        # Candidate event edges. coef_state=-1 denotes constant 1; otherwise
        # multiply by p_t[coef_state]. The edge weights from a source state
        # sum to one for every t.
        esrc, edst, ecoef, eprob = [], [], [], []
        candidate_rate = self.catalysts * self.lam
        for src, (j, b, n) in enumerate(states):
            if j >= K:
                continue
            for dest, coef, weight in candidate_event_edges(
                    (j, b, n), N, self.catalysts, self.bind):
                esrc.append(src); edst.append(ix[dest])
                ecoef.append(coef); eprob.append(weight)
        esrc = np.asarray(esrc, dtype=np.int64)
        edst = np.asarray(edst, dtype=np.int64)
        ecoef = np.asarray(ecoef, dtype=np.int64)
        eprob = np.asarray(eprob, dtype=float)
        # Index edges by source to reduce scatter overhead if there are many.
        order = np.argsort(esrc)
        esrc, edst, ecoef, eprob = esrc[order], edst[order], ecoef[order], eprob[order]

        f0 = np.zeros(D)
        f0[ix[(0, 0, (0,) * q)]] = 1.0

        def rhs(t, f):
            out = R.T @ f - candidate_rate * f
            if candidate_rate and len(esrc):
                p = self.mu0 @ expm(self.Q * t)
                factors = np.where(ecoef < 0, 1.0, p[np.maximum(ecoef, 0)])
                np.add.at(out, edst, candidate_rate * eprob * factors * f[esrc])
            return out

        sol = solve_ivp(rhs, (0.0, T), f0, method="DOP853", rtol=rtol,
                        atol=atol, max_step=max_step)
        if not sol.success:
            raise RuntimeError(sol.message)
        f = sol.y[:, -1]
        pT = self.mu0 @ expm(self.Q * T)
        lower = 0.0
        lower_by_j = np.zeros(K + 1)
        for mass, (j, b, n) in zip(f, states):
            if mass <= 0 or (observed_bound is not None and b != observed_bound):
                continue
            residual = tuple(obs[a] - n[a] for a in range(q))
            U = N - sum(n) - b
            if U < 0 or any(x < 0 for x in residual) or sum(residual) != U:
                continue
            contribution = float(mass) * multinomial_pmf(residual, pT)
            lower += contribution
            lower_by_j[j] += contribution
        tail = float(poisson.sf(K, candidate_rate * T))
        return MarkedResult(lower, tail, float(f.sum()), D, rtol, atol,
                            lower_by_j)


def full_cme_endpoint(N: int, Q: np.ndarray, bind: int, product: int,
                      lam: float, koff: float, kcat: float, mu0: np.ndarray,
                      T: float, observed: tuple[int, ...],
                      observed_bound: int | None = None,
                      direction: str = "forward", catalysts: int = 1):
    """Small-N sparse CME reference using expm_multiply.

    `direction="forward"` propagates the initial law; `"adjoint"` propagates
    the endpoint indicator backward and then contracts with the initial law.
    The latter is the fair endpoint-query baseline when only one observation
    is requested.
    """
    q = len(mu0)
    states = []
    # For b bound complexes, free molecules sum to N-b.
    for b in range(min(catalysts, N) + 1):
        for n in weak_compositions(N - b, q):
            if sum(n) == N - b:
                states.append((b, n))
    ix = {s: i for i, s in enumerate(states)}
    rr, cc, vv = [], [], []
    for src, (b, n) in enumerate(states):
        exit_rate = 0.0
        for a in range(q):
            if n[a] == 0: continue
            for c in range(q):
                rate = n[a] * Q[a, c] if c != a else 0.0
                if rate > 0:
                    nn = list(n); nn[a] -= 1; nn[c] += 1
                    dst = ix[(b, tuple(nn))]
                    rr.append(src); cc.append(dst); vv.append(rate)
                    exit_rate += rate
        if b < catalysts and n[bind] > 0:
            rate = lam * (catalysts-b) * n[bind] / N
            nn = list(n); nn[bind] -= 1
            dst = ix[(b+1, tuple(nn))]
            rr.append(src); cc.append(dst); vv.append(rate); exit_rate += rate
        if b > 0:
            if koff > 0:
                nn = list(n); nn[bind] += 1
                dst = ix[(b-1, tuple(nn))]
                rr.append(src); cc.append(dst); vv.append(b*koff); exit_rate += b*koff
            if kcat > 0:
                nn = list(n); nn[product] += 1
                dst = ix[(b-1, tuple(nn))]
                rr.append(src); cc.append(dst); vv.append(b*kcat); exit_rate += b*kcat
        rr.append(src); cc.append(src); vv.append(-exit_rate)
    G = coo_matrix((vv, (rr, cc)), shape=(len(states), len(states))).tocsr()
    # Initial all N molecules distributed according to iid mu0: multinomial.
    f0 = np.zeros(len(states))
    for n in weak_compositions(N, q):
        if sum(n) == N:
            f0[ix[(0, n)]] = multinomial_pmf(n, mu0)
    obs = tuple(map(int, observed))
    if direction == "forward":
        fT = expm_multiply(G.T * T, f0)
        ans = 0.0
        for mass, (b, n) in zip(fT, states):
            if observed_bound is not None and b != observed_bound:
                continue
            if n == obs:
                ans += float(mass)
        return ans, len(states), float(fT.sum())
    if direction == "adjoint":
        ell = np.zeros(len(states))
        for i, (b, n) in enumerate(states):
            if (observed_bound is None or b == observed_bound) and n == obs:
                ell[i] = 1.0
        back = expm_multiply(G * T, ell)
        return float(f0 @ back), len(states), float("nan")
    raise ValueError("direction must be 'forward' or 'adjoint'")

