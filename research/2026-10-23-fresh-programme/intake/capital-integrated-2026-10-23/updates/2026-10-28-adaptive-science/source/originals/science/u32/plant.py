"""Private synthetic CP instrument. Learners must never import this module.

Diagonal measure-and-prepare CP maps: K_{o,i,j}=sqrt(T_o[i,j])|i><j|.
The matrices are used only to generate integer joint-event counts and to score
the frozen learned model after acquisition. They are not learner information.
"""
import itertools
import numpy as np

INITIAL = np.array([1.0, 0.0])
TRANSITIONS = [np.array([[0.15, 0.10], [0.85, 0.90]]),
               np.array([[0.80, 0.65], [0.20, 0.35]])]
EMIT_ONE = [np.array([0.30, 0.70]), np.array([0.25, 0.75])]
T = {(a, o): TRANSITIONS[a] @ np.diag(EMIT_ONE[a] if o else 1-EMIT_ONE[a])
     for a in range(2) for o in range(2)}

def word_probability(actions, outcomes):
    x = INITIAL.copy()
    for a, o in zip(actions, outcomes):
        x = T[a, o] @ x
    return float(x.sum())

def word_table(actions):
    words = list(itertools.product(range(2), repeat=len(actions)))
    probabilities = np.array([word_probability(actions, w) for w in words])
    assert abs(probabilities.sum()-1) < 1e-12
    return words, probabilities

def core_and_shifts():
    preparations = [INITIAL, TRANSITIONS[0] @ INITIAL]
    effect = EMIT_ONE[1]
    h = np.array([[1., 1.], [effect @ x for x in preparations]])
    hz = {z: np.array([[float((m @ x).sum()) for x in preparations],
                      [float(effect @ m @ x) for x in preparations]])
          for z, m in T.items()}
    return h, hz
