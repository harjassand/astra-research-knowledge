"""Exact finite rational check of weighted reservoir selection."""
from fractions import Fraction
import json


def enumerate_reservoir(weights):
    """Enumerate all replace/retain histories using exact probabilities."""
    histories = {None: Fraction(1)}
    total = 0
    for i, weight in enumerate(weights):
        total += weight
        replace = Fraction(weight, total)
        updated = {}
        for selected, probability in histories.items():
            updated[selected] = updated.get(selected, Fraction()) + probability * (1 - replace)
            updated[i] = updated.get(i, Fraction()) + probability * replace
        histories = updated
    return {selected: probability for selected, probability in histories.items() if probability}


cases = [[1], [1, 2], [2, 3, 5], [7, 1, 4, 9], [11, 2, 19, 5, 8]]
rows = []
for weights in cases:
    observed = enumerate_reservoir(weights)
    total = sum(weights)
    expected = {i: Fraction(w, total) for i, w in enumerate(weights)}
    assert observed == expected, (weights, observed, expected)
    rows.append({
        "weights": weights,
        "selected_probabilities": [str(observed[i]) for i in range(len(weights))],
        "matches_normalized_weights": True,
    })

print(json.dumps({"method": "exact Fraction enumeration", "cases": rows}, indent=2))
