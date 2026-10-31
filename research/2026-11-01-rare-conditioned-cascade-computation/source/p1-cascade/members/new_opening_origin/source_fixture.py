"""Synthetic count oracle and separate truth evaluator for the qubit experiment.

This file is not imported by learner.py.  Counts are binomial aggregates; the
corresponding laboratory preparations are charged, not individually simulated.
"""
from __future__ import annotations
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = np.array([I, X, Y, Z])


def ptm(kraus):
    return np.array([[np.trace(p @ sum((k @ q @ k.conj().T for k in kraus),
                                     np.zeros((2, 2), complex))).real / 2
                      for q in PAULI] for p in PAULI])


def make_source(initial_radius=0.73):
    # Noncommuting, irrational-in-pi Bloch rotations with rational entries.
    ux = (3 * I - 4j * X) / 5
    uy = (5 * I - 12j * Y) / 13
    p0, p1 = (I + Z) / 2, (I - Z) / 2
    g = 0.27
    d0 = np.diag([1.0, np.sqrt(1 - g)]).astype(complex)
    d1 = np.array([[0, np.sqrt(g)], [0, 0]], complex)
    kraus = {'X': [[ux]], 'Y': [[uy]], 'M': [[p0], [p1]],
             'D': [[d0], [d1]]}
    actions = {a: [ptm(ks) for ks in outcomes] for a, outcomes in kraus.items()}
    return actions, np.array([1., 0., 0., initial_radius]), kraus


PREPARATIONS = [(), ('X',), ('Y',), ('X', 'X')]
SINGULAR_PREPARATIONS = [(), ('X',), ('Y',), ('X', 'Y')]
TESTS = [None, (), ('X',), ('Y',)]


def advance_unobserved(actions, state, word):
    for a in word:
        state = sum(actions[a]) @ state
    return state


def test_event(actions, state, word):
    if word is None:
        return state[0]
    state = advance_unobserved(actions, state, word)
    return (actions['M'][0] @ state)[0]


def acquire(n_per_slot=100000000, seed=20261031, preparations=None, initial_radius=0.73):
    actions, initial, _ = make_source(initial_radius)
    rng = np.random.default_rng(seed)
    preparations = PREPARATIONS if preparations is None else preparations
    states = [advance_unobserved(actions, initial.copy(), p) for p in preparations]
    h = np.array([[test_event(actions, s, t) for s in states] for t in TESTS])
    hz = {a: [np.array([[test_event(actions, f @ s, t) for s in states]
                        for t in TESTS]) for f in fs] for a, fs in actions.items()}
    hh, count_h, n_h = h.copy(), np.zeros_like(h, int), np.zeros_like(h, int)
    hhs, count_z, n_z = {}, {}, {}
    bill = dict(independent_starts=0, native_calls=0, random_binomial_draws=0,
                maximum_experiment_length=0)

    def sample(p, prep, action, test):
        p = float(np.clip(p, 0, 1))
        k = int(rng.binomial(n_per_slot, p))
        depth = len(prep) + (action is not None) + (0 if test is None else len(test) + 1)
        bill['independent_starts'] += n_per_slot
        bill['native_calls'] += n_per_slot * depth
        bill['random_binomial_draws'] += 1
        bill['maximum_experiment_length'] = max(bill['maximum_experiment_length'], depth)
        return k

    for i, t in enumerate(TESTS):
        for j, p in enumerate(preparations):
            if i == 0:
                continue  # trace of a normalized preparation is exact.
            k = sample(h[i, j], p, None, t)
            count_h[i, j], n_h[i, j], hh[i, j] = k, n_per_slot, k / n_per_slot
    for a, tables in hz.items():
        hhs[a], count_z[a], n_z[a] = [], [], []
        for tab in tables:
            out, cnt, ns = tab.copy(), np.zeros_like(tab, int), np.zeros_like(tab, int)
            for i, t in enumerate(TESTS):
                for j, p in enumerate(preparations):
                    if i == 0 and len(tables) == 1:
                        continue
                    k = sample(tab[i, j], p, a, t)
                    cnt[i, j], ns[i, j], out[i, j] = k, n_per_slot, k / n_per_slot
            hhs[a].append(out)
            count_z[a].append(cnt)
            n_z[a].append(ns)
    data = dict(H=hh, shifted=hhs, n_H=n_h, n_shifted=n_z,
                counts_H=count_h, counts_shifted=count_z,
                reversible_actions=['X', 'Y'], initial_index=0,
                preparations=preparations, tests=TESTS, bill=bill,
                n_per_slot=n_per_slot, seed=seed)
    truth = dict(H=h, shifted=hz, actions=actions, initial=initial,
                 state_basis=np.column_stack(states))
    return data, truth
