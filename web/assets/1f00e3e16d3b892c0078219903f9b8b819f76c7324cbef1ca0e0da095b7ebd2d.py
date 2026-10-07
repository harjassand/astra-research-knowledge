"""Acquired one-pair heat-bath probabilities for explicit REAL rational line data.

No full partition oracle is accepted. This kernel is precisely the natural
route falsified by the balanced single-pair counterexample.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from initial_checks import det


def point_weight(lines, state):
    """Each line is (v, w, positive rational activity, optional name)."""
    selected = [lines[i] for i in sorted(state)]
    dimension = len(selected[0][0]) if selected else 0
    if 2*len(selected) != dimension:
        raise ValueError('A full basis must have exactly ambient_dimension/2 lines')
    columns = []
    activity = Q(1)
    for line in selected:
        v,w,a = line[:3]
        columns.extend((v,w))
        activity *= a
    matrix = [[column[i] for column in columns] for i in range(dimension)]
    value = det(matrix)
    return activity*value*value


def transition_distribution(lines, state):
    """Return exact rational probabilities of one-pair heat-bath update.

    Choose a selected line uniformly, keep the remaining columns, then
    choose a completion among the finite explicit list of line labels.
    Each conditional normalizer contains <= len(lines) determinant terms.
    The unconditional Z of the full basis law is never read or evaluated.
    """
    state = tuple(sorted(state))
    if point_weight(lines,state) <= 0:
        raise ValueError('Input state must have positive full-basis weight')
    probabilities = {}
    for removed in state:
        rest = tuple(i for i in state if i != removed)
        completions = {}
        for candidate in range(len(lines)):
            if candidate in rest:
                continue
            target = tuple(sorted(rest+(candidate,)))
            weight = point_weight(lines,target)
            if weight:
                completions[target] = weight
        normalizer = sum(completions.values(),Q(0))
        assert normalizer > 0
        for target,weight in completions.items():
            probabilities[target] = probabilities.get(target,Q(0)) + weight/(len(state)*normalizer)
    assert sum(probabilities.values(),Q(0)) == 1
    return probabilities
