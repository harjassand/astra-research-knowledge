"""Noisy, reusable solvers acquired from verified requests.

This numerical prototype implements the halfspace update proved in MAIN_PROOF.
It never receives the hidden low-rank comparator. Source actions, directed
experiments, failed trials, model arithmetic and audit work are distinct.
Floating-point checks are reproducibility evidence, not interval certificates.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def hermitian(a):
    return (a + a.conj().T) / 2


@dataclass
class Counters:
    source_actions: int = 0
    trials: int = 0
    accepted: int = 0
    failed_trials: int = 0
    directed_experiments: int = 0
    updates: int = 0


class AcquiredSolver:
    def __init__(self, n, alpha, mu, upper, eta, threshold, action,
                 directed=0, audit=None):
        self.n = n
        self.alpha = np.asarray(alpha, dtype=float)
        self.k = len(self.alpha)
        self.mu, self.upper = float(mu), float(upper)
        self.eta, self.threshold = float(eta), float(threshold)
        if not (0 <= eta < threshold and threshold + eta < mu):
            raise ValueError('Need eta < threshold and threshold+eta < mu.')
        if np.min(self.alpha) < mu or np.max(self.alpha) > upper:
            raise ValueError('Scalar initialization must be in the spectral interval.')
        self.action, self.directed, self.audit = action, int(directed), audit
        self.q = np.zeros((n, 0), dtype=complex)
        self.d = np.zeros((self.k, 0, 0), dtype=complex)
        self.count = Counters()
        self.events = []

    @property
    def rank(self):
        return self.q.shape[1]

    def apply_model(self, theta, v):
        theta = np.asarray(theta)
        scalar = float(theta @ self.alpha)
        if not self.rank:
            return scalar * v
        small = np.einsum('j,jab->ab', theta, self.d)
        return scalar * v + self.q @ (small @ (self.q.conj().T @ v))

    def candidate(self, theta, b):
        theta = np.asarray(theta)
        scalar = float(theta @ self.alpha)
        if not self.rank:
            return b / scalar
        coordinates = self.q.conj().T @ b
        small = scalar*np.eye(self.rank) + np.einsum('j,jab->ab', theta, self.d)
        return b/scalar + self.q @ (np.linalg.solve(small, coordinates)-coordinates/scalar)

    def observe(self, theta, v, directed=False):
        theta = np.asarray(theta)
        y = np.zeros(self.n, dtype=complex)
        for j, coefficient in enumerate(theta):
            if coefficient:
                y += coefficient * self.action(j, v)
                self.count.source_actions += 1
        # A Hermitian source has real v*Av. Remove only the impossible
        # imaginary parallel component; this cannot enlarge action error.
        y -= 1j * np.imag(np.vdot(v, y)) * v
        r = y-self.apply_model(theta, v)
        a = float(np.linalg.norm(r))
        sym_norm = 0.5*(a*a + float(np.real(np.vdot(v, r)))**2)
        g2 = float(theta@theta) * sym_norm
        h = a*max(a-self.eta, 0.0)
        gain = h*h/g2 if g2 else 0.0
        if directed:
            self.count.directed_experiments += 1
        return {'v':v, 'y':y, 'r':r, 'a':a, 'g2':g2, 'h':h, 'gain':gain}

    def _extend_basis(self, vectors):
        old_rank = self.rank
        for vector in vectors:
            w = vector.astype(complex, copy=True)
            for _ in range(2):
                if self.rank:
                    w -= self.q @ (self.q.conj().T @ w)
            length = float(np.linalg.norm(w))
            # Numerical linear dependence decision, explicitly not an exact
            # rank certificate. No source-closure loop is performed here.
            if length > 1e-12 * max(1.0, float(np.linalg.norm(vector))):
                self.q = np.column_stack((self.q, w/length))
        if self.rank != old_rank:
            updated = np.zeros((self.k, self.rank, self.rank), dtype=complex)
            updated[:, :old_rank, :old_rank] = self.d
            self.d = updated

    def update(self, theta, observation):
        theta = np.asarray(theta)
        v, r = observation['v'], observation['r']
        before = self.audit(self) if self.audit else None
        self._extend_basis((v, r))
        vsmall, rsmall = self.q.conj().T@v, self.q.conj().T@r
        direction = hermitian(np.outer(rsmall, vsmall.conj()))
        step = observation['h']/observation['g2']
        clipping = 0.0
        for j in range(self.k):
            trial = hermitian(self.d[j]+step*theta[j]*direction)
            values, vectors = np.linalg.eigh(trial+self.alpha[j]*np.eye(self.rank))
            bounded = np.clip(values, self.mu, self.upper)
            clipping += float(np.sum((values-bounded)**2))
            self.d[j] = hermitian((vectors*(bounded-self.alpha[j]))@vectors.conj().T)
        self.count.updates += 1
        after = self.audit(self) if self.audit else None
        event = {'update':self.count.updates, 'rank':self.rank,
                 'residual_norm':observation['a'], 'exact_source_gain':observation['gain'],
                 'coefficient_norm_squared':float(theta@theta),
                 'squared_clipping_distance':clipping,
                 'potential_before':before, 'potential_after':after}
        self.events.append(event)

    def solve(self, theta, b, max_updates: int | None = None):
        """Serve one request, optionally limiting lifetime model updates.

        By default there is no implementation cap: termination is governed by
        the comparison bound in MAIN_PROOF. An explicit nonnegative
        ``max_updates`` limits the total model updates retained by this solver,
        including earlier requests. A failed check at that limit raises before
        another model update; accepted answers still carry their certificate.
        """
        if max_updates is not None:
            if not isinstance(max_updates, (int, np.integer)) or max_updates < 0:
                raise ValueError('max_updates must be a nonnegative integer or None.')
        theta = np.asarray(theta, dtype=float)
        if np.min(theta)<0 or abs(float(np.sum(theta))-1)>1e-10:
            raise ValueError('theta must be in the simplex.')
        b = np.asarray(b, dtype=complex)
        if not np.linalg.norm(b):
            return np.zeros_like(b), {'checks':0, 'certificate':0.0}
        trials_before = self.count.trials
        while True:
            x = self.candidate(theta, b)
            length = float(np.linalg.norm(x))
            observation = self.observe(theta, x/length)
            self.count.trials += 1
            if observation['a'] <= self.threshold:
                self.count.accepted += 1
                relative_bound = (observation['a']+self.eta)/(self.mu-observation['a']-self.eta)
                return x, {'checks':self.count.trials-trials_before,
                           'observed_defect':observation['a'],
                           'certificate':relative_bound}
            self.count.failed_trials += 1
            if max_updates is not None and self.count.updates >= max_updates:
                raise RuntimeError('Reached explicit lifetime update cap before certification.')
            observations = [observation]
            current = observation
            for _ in range(self.directed):
                if not current['a']:
                    break
                current = self.observe(theta, current['r']/current['a'], directed=True)
                if current['a'] > self.threshold:
                    observations.append(current)
            chosen = max(observations, key=lambda item:item['gain'])
            self.update(theta, chosen)

